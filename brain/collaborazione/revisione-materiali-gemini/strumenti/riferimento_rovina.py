"""Riferimento INDIPENDENTE per la revisione di studi di "rovina operativa" su challenge di prop firm.

Scritto da Claude PRIMA di vedere il codice di Gemini, per avere un termine di confronto
che non dipenda dalle stesse scelte. Non è il motore del Brain: è uno strumento di revisione.

Modello (volutamente semplice e dichiarato):
- Unità di griglia = una frazione fissa del capitale INIZIALE (rischio fisso in valuta, non composto).
- Ogni trade dà +vincita (prob. p) oppure -perdita (prob. 1-p), in unità intere; trade indipendenti.
- Al più `trade_giorno` trade al giorno; i limiti si controllano dopo ogni trade (solo P/L chiuso).
- Barriere:  equity >= target            -> SUPERATA (assorbente)
             equity <= -max_loss          -> FALLITA  (statica rispetto al capitale iniziale)
             P/L del giorno <= -daily_loss -> FALLITA  (riferito al saldo di inizio giornata)
- Orizzonte: `giorni_max` giorni (None = molto lungo); a fine orizzonte lo stato è "in corso".
- I giorni minimi di trading non cambiano la probabilità di superamento (si possono completare
  con operazioni trascurabili): sono ignorati, scelta da dichiarare nel confronto.

Due calcoli:
  esatto()  -> catena di Markov sui giorni (programmazione dinamica), senza campionamento
  monte_carlo() -> simulazione con seme dichiarato  [SIMULATO]

Uso:  python3 riferimento_rovina.py --test
      python3 riferimento_rovina.py --p 0.45 --vincita 2 --perdita 1 --target 10 --max-loss 10 \
                                    --daily-loss 5 --trade-giorno 3 --giorni 60 --n 10000
"""
from __future__ import annotations

import argparse
import math
import random
from collections import defaultdict


def _giornata(e0: int, p: float, w: int, l: int, target: int, max_loss: int,
              daily: int | None, k: int) -> tuple[float, float, dict[int, float]]:
    """Da equity e0 a inizio giornata: (P superata, P fallita, distribuzione equity a fine giornata)."""
    stati = {0: 1.0}  # P/L intraday -> probabilità
    sup = fal = 0.0
    for _ in range(k):
        nuovi: dict[int, float] = defaultdict(float)
        for pnl, pr in stati.items():
            for d, q in ((w, p), (-l, 1 - p)):
                x, e = pnl + d, e0 + pnl + d
                if e >= target:
                    sup += pr * q
                elif e <= -max_loss or (daily is not None and x <= -daily):
                    fal += pr * q
                else:
                    nuovi[x] += pr * q
        stati = nuovi
    return sup, fal, {e0 + x: pr for x, pr in stati.items()}


def esatto(p: float, w: int, l: int, target: int, max_loss: int, daily: int | None,
           k: int, giorni: int) -> dict[str, float]:
    dist = {0: 1.0}
    sup = fal = 0.0
    cache: dict[int, tuple] = {}
    for _ in range(giorni):
        nuova: dict[int, float] = defaultdict(float)
        for e, pr in dist.items():
            if e not in cache:
                cache[e] = _giornata(e, p, w, l, target, max_loss, daily, k)
            s, f, fine = cache[e]
            sup += pr * s
            fal += pr * f
            for e2, q in fine.items():
                nuova[e2] += pr * q
        dist = nuova
    return {"superata": sup, "fallita": fal, "in_corso": max(0.0, 1 - sup - fal)}


def monte_carlo(p: float, w: int, l: int, target: int, max_loss: int, daily: int | None,
                k: int, giorni: int, n: int, seme: int = 12345) -> dict[str, float]:
    rnd = random.Random(seme)
    cont = {"superata": 0, "fallita": 0, "in_corso": 0}
    for _ in range(n):
        e, esito = 0, "in_corso"
        for _g in range(giorni):
            pnl = 0
            for _t in range(k):
                d = w if rnd.random() < p else -l
                pnl += d
                e += d
                if e >= target:
                    esito = "superata"; break
                if e <= -max_loss or (daily is not None and pnl <= -daily):
                    esito = "fallita"; break
            if esito != "in_corso":
                break
        cont[esito] += 1
    return {k_: v / n for k_, v in cont.items()}


def errore_standard(prob: float, n: int) -> float:
    return math.sqrt(prob * (1 - prob) / n)


def rovina_classica(p: float, a: int, b: int) -> float:
    """Gambler's ruin a passi ±1: probabilità di arrivare a +a prima di -b (vincita/perdita unitarie)."""
    if p == 0.5:
        return b / (a + b)
    r = (1 - p) / p
    return (1 - r ** b) / (1 - r ** (a + b))


def _test() -> None:
    # 1) Senza limite giornaliero e con orizzonte molto lungo, ±1: deve coincidere con la rovina classica.
    for p, a, b in ((0.5, 10, 10), (0.5, 10, 5), (0.52, 10, 10), (0.45, 8, 12)):
        ex = esatto(p, 1, 1, a, b, None, 5, 4000)
        teo = rovina_classica(p, a, b)
        assert abs(ex["superata"] - teo) < 1e-6, (p, a, b, ex, teo)
    print("Test 1 (rovina classica, formula chiusa): OK")
    # 2) Il limite giornaliero può solo ridurre la probabilità di superamento.
    senza = esatto(0.45, 2, 1, 10, 10, None, 3, 60)["superata"]
    con = esatto(0.45, 2, 1, 10, 10, 5, 3, 60)["superata"]
    assert con <= senza + 1e-12
    print("Test 2 (limite giornaliero non aumenta il superamento): OK")
    # 3) Monte Carlo entro 4 errori standard dal valore esatto.  [SIMULATO]
    ex = esatto(0.45, 2, 1, 10, 10, 5, 3, 60)
    mc = monte_carlo(0.45, 2, 1, 10, 10, 5, 3, 60, n=10000, seme=7)
    for k_ in ex:
        se = errore_standard(ex[k_], 10000)
        assert abs(mc[k_] - ex[k_]) < 4 * se + 1e-9, (k_, mc, ex)
    print("Test 3 (Monte Carlo n=10.000 coerente con il valore esatto): OK")
    print("  esatto  :", {k_: round(v, 4) for k_, v in ex.items()})
    print("  [SIMULATO] MC:", {k_: round(v, 4) for k_, v in mc.items()},
          f" errore standard ≈ {100*errore_standard(ex['superata'], 10000):.2f} punti %")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--p", type=float, default=0.45)
    ap.add_argument("--vincita", type=int, default=2)
    ap.add_argument("--perdita", type=int, default=1)
    ap.add_argument("--target", type=int, default=10)
    ap.add_argument("--max-loss", type=int, default=10)
    ap.add_argument("--daily-loss", type=int, default=5)
    ap.add_argument("--trade-giorno", type=int, default=3)
    ap.add_argument("--giorni", type=int, default=60)
    ap.add_argument("--n", type=int, default=10000)
    ap.add_argument("--seme", type=int, default=12345)
    a = ap.parse_args()
    if a.test:
        _test(); return
    args = (a.p, a.vincita, a.perdita, a.target, a.max_loss, a.daily_loss, a.trade_giorno, a.giorni)
    ex = esatto(*args)
    mc = monte_carlo(*args, n=a.n, seme=a.seme)
    print("esatto:", {k: round(v, 4) for k, v in ex.items()})
    print(f"[SIMULATO] MC n={a.n} seme={a.seme}:", {k: round(v, 4) for k, v in mc.items()})
    print("errore standard MC sul superamento ≈ %.2f punti %%" % (100 * errore_standard(ex["superata"], a.n)))


if __name__ == "__main__":
    main()
