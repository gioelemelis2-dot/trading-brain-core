"""[CLAUDE · VERIFICA] Test di mutazione sulla suite di Gemini.
Ogni mutante è una COPIA del motore con un singolo difetto plausibile, scritta in una cartella separata
(verifiche/mutanti/Mxx/). L'originale non viene toccato. Si esegue la suite ORIGINALE (collegamento simbolico)
contro ogni mutante: un buon test fallisce (= 'ucciso')."""
import os, subprocess, sys, shutil
SRC, TEST, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
orig = open(SRC).read()
MUT = {
 "M01 V1: nessun congelamento, target valido solo da min_days": [
    ("            if target_locked:\n                # Target già raggiunto prima di min_days:\n                # Si operano micro-lotti simbolici a rischio zero per soddisfare il regolamento\n                continue\n", ""),
    ("            if equity >= target_pct:\n                target_locked = True\n                target_hit_day = day\n",
     "            if equity >= target_pct and day >= min_days:\n                return (\"pass\", day, equity)\n")],
 "M02 congelamento attivato ma si continua a operare": [
    ("                continue\n\n            # Determinazione", "                pass\n\n            # Determinazione")],
 "M03 pavimento giornaliero statico (dal capitale iniziale)": [
    ("daily_loss_floor = midnight_equity - max_daily_loss_pct", "daily_loss_floor = 0.0 - max_daily_loss_pct")],
 "M04 disuguaglianza stretta sul max loss": [
    ("            if equity <= -max_overall_loss_pct:\n                return (\"max_loss\", day, equity)",
     "            if equity < -max_overall_loss_pct:\n                return (\"max_loss\", day, equity)")],
 "M05 target controllato PRIMA delle barriere": [
    ("            # Barriere\n", "            if equity >= target_pct:\n                target_locked = True\n                target_hit_day = day\n                continue\n            # Barriere\n")],
 "M06 costi ignorati": [("r_net = r_gross - scenario.cost_r", "r_net = r_gross")],
 "M07 Markov: P(L|W) sbagliata (usa P(L|L))": [
    ("prob_loss = (p_loss_base - scenario.p_loss_given_loss * p_loss_base) / scenario.win_rate if scenario.win_rate > 0 else 1.0",
     "prob_loss = scenario.p_loss_given_loss")],
 "M08 MAE: soglia daily loss ignorata durante il trade": [
    ("                if floating_intra_equity <= daily_loss_floor:\n                    return (\"daily_loss\", day, floating_intra_equity)\n", "")],
 "M09 fase 2 con target della fase 1": [("fase2_target, max_daily_loss", "fase1_target, max_daily_loss")],
 "M10 giorni di superamento sottostimati (ignora min_days)": [
    ("        if target_locked and day >= min_days:\n            return (\"pass\", day, equity)",
     "        if target_locked:\n            return (\"pass\", target_hit_day, equity)")],
 "M11 pavimento giornaliero al 4%": [("max_daily_loss_pct: float = 0.05", "max_daily_loss_pct: float = 0.04")],
}
risultati = []
for nome, subs in MUT.items():
    code = orig
    for a, b in subs:
        assert a in code, f"sostituzione non trovata per {nome}: {a[:60]!r}"
        code = code.replace(a, b, 1)
    d = os.path.join(OUT, nome.split()[0]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "prop_risk_engine_v2.py"), "w").write(code)
    t = os.path.join(d, "test_prop_risk_v2.py")
    if not os.path.lexists(t): os.symlink(TEST, t)
    r = subprocess.run([sys.executable, "-s", t], cwd=d, capture_output=True, text=True, env={"PATH": os.environ["PATH"]})
    esito = "UCCISO" if r.returncode != 0 else "SOPRAVVISSUTO"
    risultati.append((nome, esito)); print(f"{esito:13s} {nome}")
print(f"\nMutanti uccisi dalla suite di Gemini: {sum(e=='UCCISO' for _,e in risultati)}/{len(risultati)}")
