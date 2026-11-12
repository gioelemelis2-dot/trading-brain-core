"""[CLAUDE · VERIFICA V3.3] (1) Campionatore MAE riscritto (expm1, guardia asimmetrica) contro F(d) in aritmetica
decimale a 60 cifre: per u fissato, m(u) deve soddisfare F(m) = u oppure 1 - u. (2) Cifre complete dei valori esatti
della sfida a due fasi (swing 1%, 60 giorni), da confrontare con 0,780000 / 0,857200 / 0,668616 dichiarati.
Uso: python3 -s v33_f_precisione.py <verifiche V2 Claude> <cartella con prop_risk_engine_v3_3.py>"""
import sys
from decimal import Decimal as D, getcontext
sys.path.insert(0, sys.argv[1]); sys.path.insert(1, sys.argv[2])
from c1_esatto_challenge import fase
import prop_risk_engine_v3_3 as E
getcontext().prec = 60
def F(d, b, mu):
    d, b, mu = D(repr(d)), D(repr(b)), D(repr(mu))
    s = lambda x: 1 - (-2 * mu * x).exp()
    P = lambda x, up, lo: (s(x) - s(lo)) / (s(up) - s(lo))
    return (1 - P(D(0), b, -d)) * P(-d, b, D(-1)) / P(D(0), b, D(-1))
class U:
    def __init__(s, v): s.v = v
    def random(s): return s.v
print("(1) Campionatore V3.3 contro F(d) in precisione decimale (9 valori di u per configurazione)")
for wr, rr in ((0.40, 2.0), (0.99, 500.0), (0.9999995, 50.0), (0.05, 0.1), (0.9, 0.02), (0.999, 2.0)):
    mu = E.PropSimulationScenarioV3_3("x", wr, rr, use_brownian_mae=True).brownian_mu
    errs = []
    for u in (0.001, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99, 0.999):
        m = -E.sample_brownian_mae_given_win(U(u), rr, mu)
        if 0 < m < 0.999:
            f = F(m, rr, mu); errs.append(min(abs(f - D(1 - u)), abs(f - D(u))))
    print(f"  WR {wr} R:R {rr} mu {mu:+.5f}: errore massimo {float(max(errs)):.2e} su {len(errs)} punti")
f1 = fase(0.40, 0.01, 2.0, 0.05, 2, 60, 0.10)["pass"]; f2 = fase(0.40, 0.01, 2.0, 0.05, 2, 60, 0.05)["pass"]
print("\n(2) Valori esatti, cifre complete")
print(f"  Fase 1 {float(f1):.10f} (dichiarato 0,780000)  Fase 2 {float(f2):.10f} (dichiarato 0,857200)  prodotto {float(f1 * f2):.10f} (dichiarato 0,668616)")
