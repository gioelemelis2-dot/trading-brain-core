"""[CLAUDE · VERIFICA V3.3, adattato da v32_a_esatto.py] (A) Valori 'esatti' usati nei test V3.2 contro il calcolo esatto indipendente;
(B) effetto esatto del mutante V10 (MAE troncato a 0,5R) sulle configurazioni dei test;
(C) MAE con R:R != 2 ATTRAVERSO IL MOTORE sull'intera sfida a due fasi: esatto contro motore V3.3.
Uso: python3 -s v32_a_esatto.py <verifiche V2 Claude> <cartella con prop_risk_engine_v3_3.py>"""
import sys, math
from collections import defaultdict
from fractions import Fraction as Fr
sys.path.insert(0, sys.argv[1]); sys.path.insert(1, sys.argv[2])
from c1_esatto_challenge import challenge, fase, reticolo, soglia_le, soglia_ge
import prop_risk_engine_v3_3 as eng

def mu_per(p, b):
    lo, hi = -10.0, 10.0
    pw = lambda m: (1/(1+b)) if abs(m) < 1e-12 else (math.exp(2*m) - 1) / (math.exp(2*m) - math.exp(-2*m*b))
    for _ in range(200):
        mid = (lo + hi) / 2; lo, hi = (mid, hi) if pw(mid) < p else (lo, mid)
    return (lo + hi) / 2

def F(d, b, mu, cap=None):   # P(MAE <= -d | vincita); con cap: MAE troncato a -cap (mutante V10)
    if cap is not None and d > cap: return 0.0
    if d >= 1: return 0.0
    if d <= 0: return 1.0
    s = (lambda x: x) if abs(mu) < 1e-12 else (lambda x: 1 - math.exp(-2*mu*x))
    P = lambda x, up, lo: (s(x) - s(lo)) / (s(up) - s(lo))
    return (1 - P(0, b, -d)) * P(-d, b, -1) / P(0, b, -1)

def fase_mae(p, risk, rr, cost, tpd, md, target, mae=True, cap=None, dl=0.05, ml=0.10):
    unit, w, l = reticolo(risk, rr, cost); u = float(unit)
    ML = soglia_le(-Fr(str(ml)), unit); DLu = Fr(str(dl)) / unit; TG = soglia_ge(Fr(str(target)), unit)
    mu = mu_per(p, rr); es = defaultdict(float); dist = {0: 1.0}
    for _ in range(md):
        nd = defaultdict(float)
        for e0, pr0 in dist.items():
            fl = math.floor(e0 - DLu); floor_eq = e0 * u - dl; st = {e0: pr0}
            for _ in range(tpd):
                st2 = defaultdict(float)
                for e, pr in st.items():
                    eq = e * u
                    if mae:
                        f_ml = F((eq + ml) / risk, rr, mu, cap); f_dl = F((eq - floor_eq) / risk, rr, mu, cap)
                        es["max_loss"] += pr * p * f_ml
                        es["daily_loss"] += pr * p * max(0.0, f_dl - f_ml)
                        pw = p * (1 - max(f_ml, f_dl))
                    else:
                        pw = p
                    for d, q in ((w, pw), (l, 1 - p)):
                        e2 = e + d
                        if e2 <= ML: es["max_loss"] += pr * q
                        elif e2 <= fl: es["daily_loss"] += pr * q
                        elif e2 >= TG: es["pass"] += pr * q
                        else: st2[e2] += pr * q
                st = st2
            for k, v in st.items(): nd[k] += v
        dist = nd
    es["timeout"] += sum(dist.values()); return es

def due(**kw):
    a = fase_mae(target=0.10, **kw); b = fase_mae(target=0.05, **kw)
    out = {k: a.get(k, 0) + a["pass"] * b.get(k, 0) for k in ("max_loss", "daily_loss", "timeout")}
    out["pass"] = a["pass"] * b["pass"]; return out

def z(x, p, n): return (x - p) / math.sqrt(max(p * (1 - p), 1e-12) / n)

print("(A) Valori di riferimento (i valori 'test' citati sono quelli della V3.2)")
f1 = fase(0.40, 0.01, 2.0, 0.05, 2, 60, 0.10); f2 = fase(0.40, 0.01, 2.0, 0.05, 2, 60, 0.05)
print(f"  Fase 1 isolata, swing 1%, 60 g: esatto {f1['pass']:.4f}  (test: ~0.776)")
print(f"  Fase 2 isolata, swing 1%, 60 g: esatto {f2['pass']:.4f}  (test: 0.8596, tolleranza 0.025)")
print(f"  Differenza P2 - P1: {f2['pass']-f1['pass']:+.4f}  (test richiede > +0.05)")
mu1 = mu_per(0.5, 1.0); mu2 = mu_per(0.4, 2.0)
print(f"  mu(WR .50, R:R 1) = {mu1:.3e}; F(0.5) = {F(0.5, 1.0, mu1):.6f} (test 1/3); P(daily_loss al 1o trade) = {0.5*F(0.5,1.0,mu1):.6f} (test 1/6)")
print(f"  mu(WR .40, R:R 2) = {mu2:.6f} (test 0.0975 ± 0.001); F(0.5) = {F(0.5, 2.0, mu2):.6f} (test 0.3981 ± 0.01)")
ga = [("Senza limite 0,50%", challenge(0.40, 0.005, 2.0, 0.05, 2, 6000)['pass'], 0.9108),
      ("Senza limite 1,00%", challenge(0.40, 0.01, 2.0, 0.05, 2, 6000)['pass'], 0.7034),
      ("Swing 60 g 1,00%", challenge(0.40, 0.01, 2.0, 0.05, 2, 60)['pass'], 0.6686),
      ("Intraday 1% con MAE", due(p=0.40, risk=0.01, rr=2.0, cost=0.05, tpd=6, md=25)['pass'], 0.3884)]
for nome, ex, dich in ga: print(f"  Gruppo A, {nome:22s}: esatto {ex:.4f}  dichiarato nel test {dich:.4f}")

print("\n(B) Mutante V10 (MAE troncato a 0,5R): effetto esatto")
print(f"  Test RR=1 (rischio 10%, floor 5%): P(daily_loss) con V10 = {0.5*F(0.5,1.0,mu1,cap=0.5):.6f} contro 1/6 senza: IDENTICO per costruzione")
b1 = due(p=0.40, risk=0.01, rr=2.0, cost=0.05, tpd=6, md=25)
b10 = due(p=0.40, risk=0.01, rr=2.0, cost=0.05, tpd=6, md=25, cap=0.5)
se = math.sqrt(b1['pass'] * (1 - b1['pass']) / 3000)
print(f"  Gruppo A intraday MAE: pass esatto {b1['pass']:.4f}, con V10 {b10['pass']:.4f}; scarto {b10['pass']-b1['pass']:+.4f} = {(b10['pass']-b1['pass'])/se:+.2f} SE (n=3000, soglia 4 SE)")
b0 = due(p=0.40, risk=0.01, rr=2.0, cost=0.05, tpd=6, md=25, mae=False)
print(f"  Effetto esatto del MAE: {100*(b1['pass']-b0['pass']):+.2f} punti; con V10: {100*(b10['pass']-b0['pass']):+.2f} punti")

print("\n(C) MAE con R:R != 2 attraverso il motore, sfida completa a due fasi (esatto contro motore V3.3, n=20000, seme 7)")
for (p, rr, risk, tpd, md) in ((0.55, 1.0, 0.01, 6, 25), (0.30, 3.0, 0.01, 6, 25), (0.55, 1.0, 0.02, 2, 60), (0.30, 3.0, 0.015, 4, 30)):
    ex = due(p=p, risk=risk, rr=rr, cost=0.05, tpd=tpd, md=md)
    sc = eng.PropSimulationScenarioV3_3("x", p, rr, cost_r=0.05, use_brownian_mae=True)
    r = eng.run_full_challenge_v3_3(7, sc, risk, tpd, md, 20000)
    riga = "  ".join(f"{k} {r[k]['rate']:.4f}/{ex[k]:.4f} (z {z(r[k]['rate'], ex[k], 20000):+.2f})" for k in ("pass", "daily_loss", "max_loss"))
    print(f"  WR {p} R:R {rr} rischio {risk:.3f} {tpd} t/g {md} g: motore/esatto  {riga}")
