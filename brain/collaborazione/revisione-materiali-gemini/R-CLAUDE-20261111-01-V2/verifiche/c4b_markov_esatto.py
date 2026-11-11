"""[CLAUDE · VERIFICA] Esatto con esiti a catena di Markov (stato = equity, ultimo esito).
Misura: (i) effetto del clustering rispetto agli esiti i.i.d.; (ii) effetto dello stato iniziale
'vincita' usato dal motore di Gemini rispetto a uno stato iniziale stazionario."""
import sys, math, os; sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from collections import defaultdict
from c1_esatto_challenge import reticolo, soglia_le, soglia_ge, challenge
from fractions import Fraction as F

def fase_mk(p, pll, risk, tpd, max_days, target, init="W", rr=2.0, cost=0.05, dl=0.05, ml=0.10):
    unit, w, l = reticolo(risk, rr, cost); ML = soglia_le(-F(str(ml)), unit); DLu = F(str(dl))/unit; TG = soglia_ge(F(str(target)), unit)
    plw = (1-p)*(1-pll)/p
    if init == "W": dist = {(0, 0): 1.0}
    else: dist = {(0, 1): 1-p, (0, 0): p}     # stazionaria: 1=ultima perdita
    es = defaultdict(float)
    for _ in range(max_days):
        nuova = defaultdict(float)
        for (e0, s0), pr0 in dist.items():
            fl = math.floor(e0 - DLu); st = {(e0, s0): pr0}
            for _ in range(tpd):
                st2 = defaultdict(float)
                for (e, s), pr in st.items():
                    pl = pll if s == 1 else plw
                    for d, q, s2 in ((w, 1-pl, 0), (l, pl, 1)):
                        e2 = e + d
                        if e2 <= ML: es["max_loss"] += pr*q
                        elif e2 <= fl: es["daily_loss"] += pr*q
                        elif e2 >= TG: es["pass"] += pr*q
                        else: st2[(e2, s2)] += pr*q
                st = st2
            for k, v in st.items(): nuova[k] += v
        dist = nuova
    es["timeout"] += sum(dist.values()); return es

def due_fasi(**kw):
    a = fase_mk(target=0.10, **kw); b = fase_mk(target=0.05, **kw)
    return a["pass"]*b["pass"], a["daily_loss"]+a["pass"]*b["daily_loss"], a["max_loss"]+a["pass"]*b["max_loss"]

if __name__ == "__main__":
    print(f"{'config':16s} {'i.i.d.':>8s} {'Markov init W':>14s} {'Markov staz.':>13s}  (prob. di superare entrambe le fasi; DL e ML tra parentesi)")
    for r, tpd, md in [(0.005,2,60),(0.01,2,60),(0.005,6,25),(0.01,6,25)]:
        iid = challenge(0.40, r, 2.0, 0.05, tpd, md)
        mw = due_fasi(p=0.40, pll=0.80, risk=r, tpd=tpd, max_days=md, init="W")
        ms = due_fasi(p=0.40, pll=0.80, risk=r, tpd=tpd, max_days=md, init="S")
        print(f"r={r:.3f} tpd={tpd}  {iid['pass']:8.4f} {mw[0]:14.4f} {ms[0]:13.4f}   DL: {iid['daily_loss']:.3f}/{mw[1]:.3f}/{ms[1]:.3f}  ML: {iid['max_loss']:.3f}/{mw[2]:.3f}/{ms[2]:.3f}")
