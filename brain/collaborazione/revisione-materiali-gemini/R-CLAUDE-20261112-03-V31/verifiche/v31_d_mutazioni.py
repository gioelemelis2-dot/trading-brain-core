"""[CLAUDE · VERIFICA V3.1] Test di mutazione sulla suite ORIGINALE di Gemini (test_prop_risk_v3_1.py).
Ogni mutante è una copia del motore con UN difetto plausibile, in una cartella separata; l'originale non è toccato."""
import os, subprocess, sys
SRC, TEST, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
orig = open(SRC).read()
M = {
 "V01 fase 2 senza nuovi generatori (accoppiamento parziale)": [
   ("rng_out_p2 = random.Random((base_i + 500_000) & 0xFFFFFFFF)", "rng_out_p2 = rng_out_p1"),
   ("rng_mae_p2 = random.Random((base_i + 600_000) & 0xFFFFFFFF)", "rng_mae_p2 = rng_mae_p1")],
 "V02 deriva fissa 0,09754 (P-02 annullata)": [
   ("self.brownian_mu = solve_brownian_drift_for_scenario(self.win_rate, self.reward_to_risk)", "self.brownian_mu = 0.09754")],
 "V03 il motore passa R:R 2 fisso al campionatore MAE": [
   ("sample_brownian_mae_given_win(rng_mae, scenario.reward_to_risk, scenario.brownian_mu)", "sample_brownian_mae_given_win(rng_mae, 2.0, scenario.brownian_mu)")],
 "V04 durante il trade daily loss prima del max loss (P-05 annullata)": [
   ("""                if floating_intra_equity <= -max_overall_loss_pct:
                    return ("max_loss", day, floating_intra_equity)
                if floating_intra_equity <= daily_loss_floor:
                    return ("daily_loss", day, floating_intra_equity)""",
    """                if floating_intra_equity <= daily_loss_floor:
                    return ("daily_loss", day, floating_intra_equity)
                if floating_intra_equity <= -max_overall_loss_pct:
                    return ("max_loss", day, floating_intra_equity)""")],
 "V05 costi ignorati": [("r_net = r_gross - scenario.cost_r", "r_net = r_gross")],
 "V06 Markov: partenza sempre da vincita (C-01 annullata)": [
   ("last_outcome_was_loss = (rng_outcome.random() >= scenario.win_rate)", "last_outcome_was_loss = False")],
 "V07 fase 2 con il target della fase 1": [("fase2_target, max_daily_loss, max_overall_loss, min_days", "fase1_target, max_daily_loss, max_overall_loss, min_days")],
 "V08 nessun controllo daily loss durante il trade": [
   ("""                if floating_intra_equity <= daily_loss_floor:
                    return ("daily_loss", day, floating_intra_equity)
""", "")],
 "V09 pavimento giornaliero statico": [("daily_loss_floor = midnight_equity - max_daily_loss_pct", "daily_loss_floor = 0.0 - max_daily_loss_pct")],
 "V10 MAE troncato a -0,5R (escursioni profonde perse)": [("m = min(0.999, max(0.0, m))", "m = min(0.5, max(0.0, m))")],
 "V11 MAE: fattore 2 dimenticato nell'inversione": [("m = math.log(max(1e-15, y)) / (2.0 * mu)", "m = math.log(max(1e-15, y)) / (mu)")],
 "V12 bug min_days della V1 reintrodotto": [
   ("""            if equity >= target_pct:
                target_locked = True
                target_hit_day = day""", """            if equity >= target_pct and day >= min_days:
                return ("pass", day, equity)""")],
}
ris = []
for nome, subs in M.items():
    c = orig
    for a, b in subs:
        assert a in c, (nome, a[:50]); c = c.replace(a, b, 1)
    d = os.path.join(OUT, nome.split()[0]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "prop_risk_engine_v3_1.py"), "w").write(c)
    t = os.path.join(d, "test_prop_risk_v3_1.py")
    if not os.path.lexists(t): os.symlink(TEST, t)
    r = subprocess.run([sys.executable, "-s", "-B", t], cwd=d, capture_output=True, text=True, timeout=600,
                       env={"PATH": os.environ["PATH"], "PYTHONPATH": d})
    falliti = [l.split()[1] for l in r.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
    e = "UCCISO" if r.returncode else "SOPRAVVISSUTO"; ris.append(e)
    print(f"{e:13s} {nome}" + (f"  [{', '.join(falliti)}]" if falliti else ""))
print(f"\nMutanti uccisi dalla suite V3.1: {ris.count('UCCISO')}/{len(ris)}")
