"""[CLAUDE · VERIFICA V3] (F) C-09/C-10 con lo strumento esatto indipendente di Claude; (G) intervallo di Wilson della V3
contro una formula scritta da Claude; (H) z-score di STR-002 con le due convenzioni."""
import sys, math; sys.path.insert(0, sys.argv[1]); sys.path.insert(0, sys.argv[2])
from c8_kelly_barriera import rovina_esatta, ms, f_star
from prop_risk_engine_v3 import wilson_confidence_interval as wv3
m_n, s2_n = ms(0.40, 2.0, 0.05); m_g, s2_g = ms(0.40, 2.0, 0.0)
print(f"(F) Var[R] netto {s2_n:.4f} (i costi spostano entrambi gli esiti: la varianza non cambia) · lordo {s2_g:.4f}")
print(f"    f* con costi {100*f_star(m_n, s2_n):.4f}% · senza costi {100*f_star(m_g, s2_g):.4f}%  (risposta di Gemini: Var 2,233 e 0,448%)")
ex, _ = rovina_esatta(0.40, 0.01, 2.0, 0.0, ferma_al_target=0.10)
th = 2 * m_g / s2_g * 1.0   # per unità di rischio 1% -> D=T=10 unità
diff = (math.exp(th * 10) - 1) / (math.exp(th * 20) - 1)
print(f"    C-10 (rischio 1%, senza costi, target +10%, stop -10%): rovina esatta {100*ex:.4f}% · diffusione {100*diff:.4f}%  (Gemini: 12,5739% / 13,5656%)")
def wilson(k, n, z=1.959963984540054):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
mx = max(max(abs(a - b) for a, b in zip(wv3(k, 10000), wilson(k, 10000))) for k in (0, 1, 17, 688, 4054, 5000, 9955, 10000))
print(f"(G) Wilson V3 vs formula indipendente: massima differenza {mx:.2e}")
for nome, n, p0 in (("filtro 1,2", 345, 0.477), ("filtro 0,70", 966, 0.612)):
    print(f"(H) {nome}: z con errore sotto H0 (test score) {(0.70-p0)/math.sqrt(p0*(1-p0)/n):.2f} · con errore osservato (Wald) {(0.70-p0)/math.sqrt(0.7*0.3/n):.2f}")
