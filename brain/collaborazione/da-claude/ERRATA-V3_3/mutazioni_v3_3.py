"""Errata V3.3, T-01: test di mutazione sulla suite di Gemini (test_prop_risk_v3_3.py) PIÙ i test dell'errata
(test_errata_v3_3.py). Un mutante è ucciso se almeno una delle due suite fallisce.
V01-V12: gli stessi mutanti della revisione V3.1 (v31_d_mutazioni.py), adattati ai nomi della V3.3.
V13-V22: mutanti della revisione V3.2; V23-V25: nuovi, sul codice riscritto in V3.3
(campionatore, guardia asimmetrica, validazione). Ogni mutante è una copia del motore con UN difetto, in una cartella separata, con una COPIA
del file di test; l'originale non è toccato.
Uso: python3 -s mutazioni_v3_3.py <prop_risk_engine_v3_3.py> <test_prop_risk_v3_3.py> <test_errata_v3_3.py> <cartella mutanti>"""
import os, shutil, subprocess, sys
SRC, TEST, ERR, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
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
 # --- nuovi mutanti V3.2 ---
 "V13 IC di Kelly al 95% calcolato con z=1 (N-01 reintrodotto)": [
   ("z = statistics.NormalDist().inv_cdf(0.5 + confidence_level / 2.0)", "z = 1.0 if abs(confidence_level - 0.95) < 1e-4 else statistics.NormalDist().inv_cdf(0.5 + confidence_level / 2.0)")],
 "V14 SE di E[R] senza il fattore (R:R+1)": [("se_expected_r = (reward_to_risk + 1.0) * se_wr", "se_expected_r = reward_to_risk * se_wr")],
 "V15 IC di Kelly: costo ignorato nel valore atteso": [
   ("expected_r = (win_rate * reward_to_risk) - ((1.0 - win_rate) * 1.0) - cost_r", "expected_r = (win_rate * reward_to_risk) - ((1.0 - win_rate) * 1.0)")],
 "V16 risolutore MAE senza controlli di ammissibilita e convergenza": [
   ("if win_rate < val_low or win_rate > val_high:", "if False:"),
   ("if abs(final_p - win_rate) >= 1e-7:", "if False:")],
 "V17 giorni minimi ignorati (pass al raggiungimento del target)": [("if target_locked and day >= min_days:", "if target_locked:")],
 "V18 Markov: P(L|W) = 1 - P(L|L) (stazionarieta persa)": [
   ("self.p_loss_given_win = (p_loss_base - self.p_loss_given_loss * p_loss_base) / self.win_rate", "self.p_loss_given_win = 1.0 - self.p_loss_given_loss")],
 "V19 Lomax: esponente -alpha invece di -1/alpha": [("** (-1.0 / scenario.slippage_tail_alpha)", "** (-scenario.slippage_tail_alpha)")],
 "V20 Lomax: tetto 3R ignorato": [("slip = min(scenario.slippage_cap_r, max(0.0, raw_slip))", "slip = max(0.0, raw_slip)")],
 "V21 Wilson: z=1 al posto di 1,96 (IC 95% del JSON)": [
   ("z = statistics.NormalDist().inv_cdf(0.5 + confidence / 2.0)", "z = 1.0 if abs(confidence - 0.95) < 1e-4 else statistics.NormalDist().inv_cdf(0.5 + confidence / 2.0)")],
 "V22 campionatore MAE: soglia mu~0 a 0,1 (disallineata dal risolutore)": [("    if abs(mu) < 1e-7:\n        m = (a * b", "    if abs(mu) < 1e-1:\n        m = (a * b")],

 "V23 campionatore riscritto: term1 = c1 invece di c1*A": [("term1 = num_c1 * (1.0 + 1.0 / den_c1)", "term1 = num_c1 * (1.0 / den_c1)")],
 "V24 guardia asimmetrica: ramo mu<0 senza il fattore R:R": [("den = math.exp(-2.0 * mu_val * reward_to_risk) - exp_neg", "den = math.exp(-2.0 * mu_val) - exp_neg")],
 "V25 validazione max_days < min_days rimossa": [("if max_days < min_days:", "if False:")],
}
ris = []
for nome, subs in M.items():
    c = orig
    for a, b in subs:
        assert c.count(a) == 1, (nome, a[:60], c.count(a)); c = c.replace(a, b, 1)
    assert c != orig, nome
    d = os.path.join(OUT, nome.split()[0]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "prop_risk_engine_v3_3.py"), "w").write(c)
    t = os.path.join(d, "test_prop_risk_v3_3.py"); shutil.copyfile(TEST, t)
    env = {"PATH": os.environ["PATH"], "PYTHONPATH": d, "PYTHONDONTWRITEBYTECODE": "1"}
    chk = subprocess.run([sys.executable, "-s", "-B", "-c", "import prop_risk_engine_v3_3 as e; print(e.__file__)"], cwd=d, capture_output=True, text=True, env=env)
    assert chk.stdout.strip() == os.path.join(d, "prop_risk_engine_v3_3.py"), chk
    te = os.path.join(d, "test_errata_v3_3.py"); shutil.copyfile(ERR, te)
    falliti, rc = [], 0
    for tt, etichetta in ((t, "G"), (te, "E")):
        r = subprocess.run([sys.executable, "-s", "-B", tt], cwd=d, capture_output=True, text=True, timeout=600, env=env)
        rc |= r.returncode
        falliti += [etichetta + ":" + l.split()[1] for l in r.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:", "UNEXPECTED SUCCESS:"))]
    e = "UCCISO" if rc else "SOPRAVVISSUTO"; ris.append((nome.split()[0], e))
    print(f"{e:13s} {nome}" + (f"  [{', '.join(falliti)}]" if falliti else ""))
k = lambda lst: sum(1 for _, e in lst if e == "UCCISO")
a = [x for x in ris if x[0] in [f"V{i:02d}" for i in range(2, 26)]]
print("\nLegenda: G = suite di Gemini, E = test dell'errata")
print(f"Mutanti V02-V25 (non equivalenti) uccisi: {k(a)}/{len(a)}")
print(f"Tutti i mutanti V01-V25 uccisi: {k(ris)}/{len(ris)}")
