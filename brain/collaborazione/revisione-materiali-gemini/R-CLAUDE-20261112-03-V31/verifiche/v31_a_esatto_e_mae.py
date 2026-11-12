"""[CLAUDE · VERIFICA V3.1] (A) Tutti i risultati V3.1 contro il calcolo ESATTO; (B) effetto ESATTO del MAE browniano
(prima solo simulato). Per un trade vincente partito dall'equity e, la probabilità di toccare durante il trade il max loss
o il daily loss è F(d) = P(MAE <= -d | vincita), in forma chiusa (moto browniano con deriva, barriere -1 e +R:R).
Uso: python3 -I v31_a_esatto_e_mae.py <verifiche V2 Claude> <simulations_v3_1_raw.json>"""
import sys, json, math
from collections import defaultdict
from fractions import Fraction as Fr
sys.path.insert(0, sys.argv[1])
from c1_esatto_challenge import challenge, reticolo, soglia_le, soglia_ge
from c4b_markov_esatto import due_fasi

def mu_per(p, b):
    lo, hi = -10.0, 10.0
    pw = lambda m: (1/(1+b)) if abs(m) < 1e-12 else (math.exp(2*m) - 1) / (math.exp(2*m) - math.exp(-2*m*b))
    for _ in range(200):
        mid = (lo + hi) / 2; lo, hi = (mid, hi) if pw(mid) < p else (lo, mid)
    return (lo + hi) / 2

def F(d, b, mu):   # P(MAE <= -d | vincita), 0 < d < 1 ; 0 se d >= 1
    if d >= 1: return 0.0
    if d <= 0: return 1.0
    s = (lambda x: x) if abs(mu) < 1e-12 else (lambda x: 1 - math.exp(-2*mu*x))
    P = lambda x, up, lo: (s(x) - s(lo)) / (s(up) - s(lo))
    return (1 - P(0, b, -d)) * P(-d, b, -1) / P(0, b, -1)

def fase_mae(p, risk, rr, cost, tpd, md, target, mae=True, dl=0.05, ml=0.10):
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
                    if mae:   # ordine V3.1: max loss prima del daily loss
                        f_ml = F((eq + ml) / risk, rr, mu); f_dl = F((eq - floor_eq) / risk, rr, mu)
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

d = json.load(open(sys.argv[2])); N = 10000
def z(mc, ex): return (mc - ex) / math.sqrt(max(ex*(1-ex), 1e-12) / N)
print("(A) Regime senza limite (6000 giorni) e 60 giorni, 2 trade/giorno")
for blocco, md in (("modern_unlimited_days", 6000), ("legacy_fixed_days", 60)):
    for r in (0.0025, 0.005, 0.0075, 0.01):
        ex = challenge(0.40, r, 2.0, 0.05, 2, md); v = d[blocco][f"{r:.4f}"]
        print(f"  {blocco:22s} {r:.4f}  pass esatto {ex['pass']:.4f}  V3.1 {v['pass']['rate']:.4f}  z {z(v['pass']['rate'], ex['pass']):+.2f}")
ms = due_fasi(p=0.40, pll=0.80, risk=0.01, tpd=2, max_days=60, init="S")
mk = d["markov_clustering_impact"]["markov_swing_1pct"]["pass"]["rate"]
print(f"  Markov stazionario swing 1%: esatto {ms[0]:.4f}  V3.1 {mk:.4f}  z {z(mk, ms[0]):+.2f}")
print("\n(B) Effetto ESATTO del MAE browniano, intraday 1%, 6 trade/giorno, 25 giorni")
b0 = due(p=0.40, risk=0.01, rr=2.0, cost=0.05, tpd=6, md=25, mae=False)
b1 = due(p=0.40, risk=0.01, rr=2.0, cost=0.05, tpd=6, md=25, mae=True)
m = d["paired_crn_mae_impact"]; base, con = m["base_intraday_1pct"], m["mae_intraday_1pct"]
for k in ("pass", "daily_loss", "max_loss"):
    print(f"  {k:10s} senza MAE esatto {b0[k]:.4f} (V3.1 {base[k]['rate']:.4f}) · con MAE esatto {b1[k]:.4f} (V3.1 {con[k]['rate']:.4f}, z {z(con[k]['rate'], b1[k]):+.2f}) · effetto esatto {100*(b1[k]-b0[k]):+.2f} punti (V3.1 {100*(con[k]['rate']-base[k]['rate']):+.2f})")
print(f"  sfide 'passate solo con MAE' dichiarate da V3.1: {m.get('impossible_passes_count')}")
s1 = due(p=0.40, risk=0.01, rr=2.0, cost=0.05, tpd=2, md=60, mae=True); s0 = challenge(0.40, 0.01, 2.0, 0.05, 2, 60)
print(f"  Swing 1%, 60 giorni: effetto esatto del MAE sul superamento {100*(s1['pass']-s0['pass']):+.2f} punti")
