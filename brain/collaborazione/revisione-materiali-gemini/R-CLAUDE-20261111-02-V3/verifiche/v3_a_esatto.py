"""[CLAUDE · VERIFICA V3] (A) Confronto dei risultati V3 con il calcolo ESATTO (strumenti della seconda revisione).
Uso: python3 -I v3_a_esatto.py <cartella verifiche V2 di Claude> <simulations_v3_raw.json>"""
import sys, json, math; sys.path.insert(0, sys.argv[1])
from c1_esatto_challenge import challenge
from c4b_markov_esatto import due_fasi
d = json.load(open(sys.argv[2])); N = 10000
def riga(nome, esatto, mc):
    se = math.sqrt(max(esatto*(1-esatto), 1e-12)/N); z = (mc-esatto)/se
    print(f"  {nome:44s} esatto {esatto:.4f}  V3 {mc:.4f}  z {z:+.2f}")
print("Regime senza limite di tempo (2 trade/giorno); esatto con 6000 giorni per fase:")
for r in (0.0025, 0.005, 0.0075, 0.01):
    ex = challenge(0.40, r, 2.0, 0.05, 2, 6000); v = d["modern_unlimited_days"][f"{r:.4f}"]
    riga(f"rischio {r:.4f} pass", ex["pass"], v["pass"]["rate"]); riga(f"rischio {r:.4f} max loss", ex["max_loss"], v["max_loss"]["rate"])
    print(f"    probabilità residua di 'in corso' dopo 6000 giorni: {ex['timeout']:.2e}")
print("Regime con 60 giorni:")
for r in (0.0025, 0.005, 0.0075, 0.01):
    ex = challenge(0.40, r, 2.0, 0.05, 2, 60); v = d["legacy_fixed_days"][f"{r:.4f}"]
    riga(f"rischio {r:.4f} pass", ex["pass"], v["pass"]["rate"])
print("Markov P(L|L)=0,80 con partenza stazionaria, swing 1%, 60 giorni:")
ms = due_fasi(p=0.40, pll=0.80, risk=0.01, tpd=2, max_days=60, init="S")
riga("pass", ms[0], d["markov_clustering_impact"]["markov_swing_1pct"]["pass"]["rate"])
riga("max loss", ms[2], d["markov_clustering_impact"]["markov_swing_1pct"]["max_loss"]["rate"])
