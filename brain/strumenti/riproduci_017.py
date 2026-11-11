"""Riproduzione della tabella della lezione 0.17 (manuale v1) a partire da CSV OHLC giornalieri.

Specifica dei dati e delle scelte di calcolo: dati/RICHIESTA-DATI-0.17.md
Ogni scelta ambigua del v1 è un parametro esplicito (C1–C10).

Uso:
    python3 riproduci_017.py FILE.csv [FILE2.csv ...] [--log] [--range-su open|prev_close|close]
    python3 riproduci_017.py --test          # test su casi costruiti a mano + serie SIMULATA

Nessuna dipendenza esterna: solo libreria standard, per poter essere eseguito ovunque.
"""
from __future__ import annotations

import argparse
import csv
import math
import random
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path

P_NORMALE_3SIGMA = 0.0026998  # P(|Z| > 3) per la normale standard


@dataclass
class Barra:
    data: str
    o: float
    h: float
    l: float
    c: float


@dataclass
class Scelte:
    log_rendimenti: bool = False          # C1
    range_su: str = "prev_close"          # C4: "prev_close" | "open" | "close"
    positivo_stretto: bool = True         # C5
    sequenze_sovrapposte: bool = True     # C6
    ma_giorni: int = 200                  # C10
    ma_include_oggi: bool = True          # C10


def leggi_csv(percorso: Path) -> list[Barra]:
    with percorso.open(newline="", encoding="utf-8") as f:
        righe = list(csv.DictReader(f))
    barre = [Barra(r["date"], float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"])) for r in righe]
    controlla(barre)
    return barre


def controlla(barre: list[Barra]) -> None:
    """Validazione minima: ordine cronologico, date uniche, coerenza OHLC."""
    date = [b.data for b in barre]
    if date != sorted(date):
        raise ValueError("date non in ordine cronologico")
    if len(set(date)) != len(date):
        raise ValueError("date duplicate")
    for b in barre:
        if not (b.l <= min(b.o, b.c) and b.h >= max(b.o, b.c)):
            raise ValueError(f"OHLC incoerente il {b.data}: {b}")


def curtosi_in_eccesso(x: list[float]) -> float:
    """Stimatore campionario corretto (lo stesso di pandas.Series.kurt)."""
    n = len(x)
    m = statistics.fmean(x)
    s2 = sum((v - m) ** 2 for v in x) / (n - 1)
    m4 = sum((v - m) ** 4 for v in x)
    return (n * (n + 1) * m4 / ((n - 1) * (n - 2) * (n - 3) * s2 ** 2)
            - 3 * (n - 1) ** 2 / ((n - 2) * (n - 3)))


def calcola(barre: list[Barra], sc: Scelte = Scelte()) -> dict[str, float]:
    if len(barre) < sc.ma_giorni + 5:
        raise ValueError("serie troppo corta")
    r = []
    for prec, b in zip(barre, barre[1:]):
        r.append(math.log(b.c / prec.c) if sc.log_rendimenti else b.c / prec.c - 1)
    media, ds = statistics.fmean(r), statistics.stdev(r)

    oltre = sum(1 for v in r if abs(v - media) > 3 * ds) / len(r)

    def base_range(i: int) -> float:  # i = indice in barre (>= 1)
        return {"prev_close": barre[i - 1].c, "open": barre[i].o, "close": barre[i].c}[sc.range_su]
    rng = [(barre[i].h - barre[i].l) / base_range(i) for i in range(1, len(barre))]
    range_med = statistics.median(rng)

    su = [(v > 0) if sc.positivo_stretto else (v >= 0) for v in r]
    giu = [v < 0 for v in r]

    def condizionata(prima: list[bool], filtro=None) -> tuple[float, int]:
        casi, i = [], 3
        while i < len(r):
            if all(prima[i - 3:i]) and (filtro is None or filtro(i)):
                casi.append(su[i])
                i += 1 if sc.sequenze_sovrapposte else 4
            else:
                i += 1
        return (sum(casi) / len(casi) if casi else float("nan")), len(casi)

    p_su_dopo_3su, n_3su = condizionata(su)
    p_su_dopo_3giu, n_3giu = condizionata(giu)

    # Media mobile: r[i] è il rendimento del giorno barre[i+1]; il segnale è alla chiusura di barre[i].
    chiusure = [b.c for b in barre]

    def sotto_ma(i: int) -> bool:
        fine = i + 1 if sc.ma_include_oggi else i      # barre[i] è il giorno del segnale
        if fine < sc.ma_giorni:
            return False
        ma = statistics.fmean(chiusure[fine - sc.ma_giorni:fine])
        return chiusure[i] < ma
    p_3giu_sotto, n_3giu_sotto = condizionata(giu, filtro=sotto_ma)

    # Gap: rispetto alla chiusura precedente, in multipli del range mediano.
    piccoli, grandi = [], []
    for i in range(1, len(barre) if range_med > 0 else 1):
        prec, b = barre[i - 1], barre[i]
        gap = (b.o - prec.c) / prec.c
        if gap == 0:
            continue
        chiuso = (b.l <= prec.c) if gap > 0 else (b.h >= prec.c)
        multiplo = abs(gap) / range_med
        if multiplo < 0.25:
            piccoli.append(chiuso)
        elif multiplo > 1:
            grandi.append(chiuso)

    return {
        "S1_media_%": 100 * media,
        "S1_devstd_%": 100 * ds,
        "S2_curtosi_eccesso": curtosi_in_eccesso(r),
        "S3_oltre_3sigma_vs_normale_x": oltre / P_NORMALE_3SIGMA,
        "S4_range_mediano_%": 100 * range_med,
        "S5_p_positivo_%": 100 * sum(su) / len(su),
        "S6_p_su_dopo_3su_%": 100 * p_su_dopo_3su, "S6_n": n_3su,
        "S7_p_su_dopo_3giu_%": 100 * p_su_dopo_3giu, "S7_n": n_3giu,
        "S8_gap_piccoli_chiusi_%": 100 * sum(piccoli) / len(piccoli) if piccoli else float("nan"),
        "S8_n": len(piccoli),
        "S9_gap_grandi_chiusi_%": 100 * sum(grandi) / len(grandi) if grandi else float("nan"),
        "S9_n": len(grandi),
        "S10_p_su_dopo_3giu_sotto_ma_%": 100 * p_3giu_sotto, "S10_n": n_3giu_sotto,
        "n_giorni": len(r),
    }


# ---------------------------------------------------------------- test

def serie_simulata(n: int = 2600, seme: int = 17) -> list[Barra]:
    """DATI SIMULATI (moto geometrico browniano). Solo per testare il codice."""
    rnd = random.Random(seme)
    barre, c = [], 100.0
    for k in range(n):
        o = c * math.exp(rnd.gauss(0, 0.003))
        intraday = [o]
        for _ in range(8):
            intraday.append(intraday[-1] * math.exp(rnd.gauss(0.0002 / 8, 0.011 / math.sqrt(8))))
        c = intraday[-1]
        barre.append(Barra(f"S{k:05d}", o, max(intraday), min(intraday), c))
    return barre


def _test() -> None:
    # 1) Caso costruito a mano: chiusure 100,101,102,103,104,103,102,101,100,101 ...
    chiusure = [100, 101, 102, 103, 104, 103, 102, 101, 100, 101]
    barre = [Barra(f"T{k:02d}", c, c + 1, c - 1, c) for k, c in enumerate(chiusure)]
    sc = Scelte(ma_giorni=1)
    # Sequenze di 3 rialzi: 100>101>102>103 -> poi 104 (su); 101>102>103>104 -> poi 103 (giù)
    r = calcola(barre, sc)
    assert abs(r["S6_p_su_dopo_3su_%"] - 50.0) < 1e-9 and r["S6_n"] == 2, r
    # Sequenze di 3 cali: 104>103>102>101 -> poi 100 (giù); 103>102>101>100 -> poi 101 (su)
    assert abs(r["S7_p_su_dopo_3giu_%"] - 50.0) < 1e-9 and r["S7_n"] == 2, r
    # Curtosi: confronto con valore noto (dati 1..5 -> -1.2)
    assert abs(curtosi_in_eccesso([1, 2, 3, 4, 5]) - (-1.2)) < 1e-9
    print("Test su casi costruiti a mano: OK")

    # 2) Serie SIMULATA: controlla solo che i valori siano nel campo atteso per un GBM
    sim = calcola(serie_simulata())
    assert abs(sim["S2_curtosi_eccesso"]) < 1.0, "un GBM non dovrebbe avere code grasse"
    assert 0.3 < sim["S3_oltre_3sigma_vs_normale_x"] < 2.5
    print("Test su serie SIMULATA (GBM, nessuna coda grassa attesa): OK")
    print("  [SIMULATO] curtosi in eccesso = %.2f, eventi oltre 3σ = %.2f× la normale"
          % (sim["S2_curtosi_eccesso"], sim["S3_oltre_3sigma_vs_normale_x"]))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--log", action="store_true", help="rendimenti logaritmici (C1)")
    ap.add_argument("--range-su", default="prev_close", choices=["prev_close", "open", "close"])
    ap.add_argument("--sequenze-non-sovrapposte", action="store_true")
    a = ap.parse_args()
    if a.test:
        _test()
        return
    if not a.files:
        ap.error("indicare almeno un CSV oppure --test")
    sc = Scelte(log_rendimenti=a.log, range_su=a.range_su, sequenze_sovrapposte=not a.sequenze_non_sovrapposte)
    for p in a.files:
        res = calcola(leggi_csv(p), sc)
        print(f"\n== {p.name}  [DATI REALI: verificare fonte e metadati]")
        for k, v in res.items():
            print(f"  {k:32s} {v:10.3f}" if isinstance(v, float) else f"  {k:32s} {v:10d}")


if __name__ == "__main__":
    sys.exit(main())
