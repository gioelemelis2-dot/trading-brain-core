"""[CLAUDE · VERIFICA INDIPENDENTE] Calcolo ESATTO (catena di Markov, nessun campionamento)
del modello di challenge descritto da prop_risk_engine_v2.py, scritto senza riusarne il codice.

Modello (come dichiarato da Gemini):
- equity in frazione del capitale iniziale; rischio fisso risk_pct per trade (non composto)
- esito netto: +(RR - cost)*risk con prob. p, -(1 + cost)*risk con prob. 1-p, trade i.i.d.
- trades_per_day trade al giorno; controlli dopo ogni trade, in quest'ordine:
  max loss statico (equity <= -ML) -> daily loss (equity <= equity_mezzanotte - DL) -> target
- V2: al primo raggiungimento del target la fase è superata (target congelato; i giorni minimi
  si completano senza rischio) -> la probabilità non dipende da min_days.
- V1 (ricostruita da UNA riga del documento di Gemini; il codice V1 non è stato consegnato):
  il target conta solo se day >= min_days; prima si continua a operare a piena size.
Aritmetica esatta su reticolo intero (frazioni), così da evitare errori di arrotondamento.
"""
from fractions import Fraction as F
from collections import defaultdict
import math, json, sys


def reticolo(risk, rr, cost):
    risk, rr, cost = F(str(risk)), F(str(rr)), F(str(cost))
    w, l = (rr - cost) * risk, -(1 + cost) * risk
    # unità = massimo comun divisore razionale di w e |l|
    from math import gcd
    den = (w.denominator * l.denominator) // gcd(w.denominator, l.denominator)
    wi, li = int(w * den), int(l * den)
    g = gcd(wi, abs(li))
    unit = F(g, den)
    return unit, wi // g, li // g


def soglia_le(x, unit):  # equity_units * unit <= x  <=>  equity_units <= floor(x/unit)
    return math.floor(x / unit)


def soglia_ge(x, unit):  # equity_units * unit >= x  <=>  equity_units >= ceil(x/unit)
    return math.ceil(x / unit)


def fase(p, risk, rr, cost, tpd, max_days, target, dl=0.05, ml=0.10, min_days=4, versione="v2"):
    unit, w, l = reticolo(risk, rr, cost)
    ML = soglia_le(-F(str(ml)), unit)
    DLu = F(str(dl)) / unit
    TG = soglia_ge(F(str(target)), unit)
    esiti = defaultdict(float)
    dist = {0: 1.0}
    for day in range(1, max_days + 1):
        nuova = defaultdict(float)
        for e0, pr0 in dist.items():
            floor_dl = math.floor(e0 - DLu)  # equity <= e0*unit - dl  <=> e <= floor(e0 - dl/unit)
            stati = {e0: pr0}
            for _ in range(tpd):
                st2 = defaultdict(float)
                for e, pr in stati.items():
                    for d, q in ((w, p), (l, 1 - p)):
                        e2 = e + d
                        if e2 <= ML:
                            esiti["max_loss"] += pr * q
                        elif e2 <= floor_dl:
                            esiti["daily_loss"] += pr * q
                        elif e2 >= TG and (versione == "v2" or day >= min_days):
                            esiti["pass"] += pr * q
                        else:
                            st2[e2] += pr * q
                stati = st2
            for e, pr in stati.items():
                nuova[e] += pr
        dist = nuova
    esiti["timeout"] += sum(dist.values())
    return dict(esiti)


def challenge(p, risk, rr, cost, tpd, max_days, versione="v2", t1=0.10, t2=0.05):
    a = fase(p, risk, rr, cost, tpd, max_days, t1, versione=versione)
    b = fase(p, risk, rr, cost, tpd, max_days, t2, versione=versione)
    pa = a.get("pass", 0)
    out = {k: a.get(k, 0) + pa * b.get(k, 0) for k in ("max_loss", "daily_loss", "timeout")}
    out["pass"] = pa * b.get("pass", 0)
    return out


if __name__ == "__main__":
    gem = json.load(open(sys.argv[1]))
    N = 10000
    righe = []
    griglia = [("swing_2tpd", r, 2, 60) for r in (0.0025, 0.005, 0.0075, 0.01, 0.015, 0.02)] + \
              [("intraday_6tpd", r, 6, 25) for r in (0.005, 0.01)]
    print(f"{'blocco':14s} {'rischio':>7s} {'esito':10s} {'esatto':>8s} {'Gemini MC':>9s} {'z':>6s}")
    zmax = 0
    for blocco, r, tpd, md in griglia:
        ex = challenge(0.40, r, 2.0, 0.05, tpd, md)
        g = gem[blocco][f"{r:.4f}"]
        for k in ("pass", "max_loss", "daily_loss", "timeout"):
            pe = ex.get(k, 0.0); pm = g[k]["rate"]
            se = math.sqrt(max(pe * (1 - pe), 1e-12) / N)
            z = (pm - pe) / se if pe > 0 else float("nan")
            zmax = max(zmax, abs(z)) if pe > 0 else zmax
            print(f"{blocco:14s} {r:7.4f} {k:10s} {pe:8.4f} {pm:9.4f} {z:6.2f}")
            righe.append(dict(blocco=blocco, rischio=r, esito=k, esatto=pe, gemini=pm, z=z))
    print("max |z| =", round(zmax, 2))
    json.dump(righe, open(sys.argv[2], "w"), indent=1)
