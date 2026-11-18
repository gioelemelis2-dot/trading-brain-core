#!/usr/bin/env python3
"""MANDATO R16 (Compito B) — Taratura estesa su mercati inventati.

- B1 (NULLO): spinta=0.0, deriva=0.0, 100 semi (1..100).
- B2 (VANTAGGIO PIANTATO): spinta=0.005 (50 semi 1..50) e spinta=0.01 (50 semi 1..50).
Stessi parametri di R15 (sd=0.5, spread=0.3, prezzo=2000.0, periodo sviluppo 2023-11-15..2026-11-12).
Usa al più 2 worker in parallelo; solo dati inventati in memoria, rete bloccata.
"""
import argparse
import json
import math
import os
import sys
import time
import urllib.request
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from statistics import mean, stdev

RADICE = Path(__file__).resolve().parents[3]


def verifica_rete_bloccata() -> None:
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
    if not proxy:
        raise RuntimeError("HTTPS_PROXY non impostato")
    try:
        urllib.request.urlopen("https://example.com", timeout=2)
    except Exception as exc:
        print(f"[RETE] bloccata ({proxy}): {type(exc).__name__}")
        return
    raise RuntimeError("RETE NON BLOCCATA")


def wilson_ci95(k: int, n: int):
    z = 1.959963984540054
    p = k / n
    denom = 1.0 + z * z / n
    centro = (p + z * z / (2.0 * n)) / denom
    meta = (z * math.sqrt((p * (1.0 - p) + z * z / (4.0 * n)) / n)) / denom
    return max(0.0, centro - meta), min(1.0, centro + meta)


def _esegui_singolo(task):
    spinta, seme = task
    sys.path.insert(0, str(RADICE))
    from brain.laboratorio.esecuzione import esegui_h002 as E, sintetico as SN

    inizio, fine = E.PERIODO_SVILUPPO
    giorni = (fine - inizio).days + 1
    bid, ask = SN.mercato(inizio, giorni, seme=seme, spinta=spinta, deriva=0.0)
    ris = E.esegui_sviluppo(bid, ask)
    out = {"spinta": spinta, "seme": seme, "varianti": {}}
    for v, d in ris["varianti"].items():
        m = d["metriche"]
        criteri = d["screening"]["criteri"]
        out["varianti"][v] = {
            "n": m.get("n", 0),
            "r_medio": m.get("r_medio"),
            "errore_std": m.get("errore_std"),
            "sharpe": m.get("sharpe"),
            "dd_max": m.get("dd_max"),
            "r_vendite": m.get("r_vendite"),
            "r_stress": d.get("r_stress"),
            "veto": d.get("veto"),
            "promossa": d["screening"]["promossa"],
            "falliti": [c["nome"] for c in criteri if not c["passa"]],
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()

    verifica_rete_bloccata()
    t0 = time.perf_counter()

    compiti = (
        [(0.0, s) for s in range(1, 101)]
        + [(0.005, s) for s in range(1, 51)]
        + [(0.01, s) for s in range(1, 51)]
    )

    risultati = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for res in pool.map(_esegui_singolo, compiti):
            risultati.append(res)

    t_tot = time.perf_counter() - t0
    json_path = Path(__file__).with_name("r16_taratura_risultati.json")
    json_path.write_text(json.dumps({"tempo_s": t_tot, "totale_mercati": len(compiti), "righe": risultati},
                                    indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    sys.path.insert(0, str(RADICE))
    from brain.laboratorio.studi.collaudo_ia02 import clopper_pearson

    print(f"\n=== RIEPILOGO TARATURA ESTESA (tot={len(risultati)} mercati, {args.workers} worker, tempo={t_tot:.1f}s) ===")
    for sp, n_semi in ((0.0, 100), (0.005, 50), (0.01, 50)):
        sub = [r for r in risultati if r["spinta"] == sp]
        any_prom = sum(1 for r in sub if any(v["promossa"] for v in r["varianti"].values()))
        w_lo, w_hi = wilson_ci95(any_prom, n_semi)
        cp_lo, cp_hi = clopper_pearson(any_prom, n_semi, 0.95)
        print(f"\n-- spinta={sp:.3f} (N={n_semi}) | V-T o V-S promossa: {any_prom}/{n_semi} ({any_prom/n_semi:.1%}) | "
              f"Wilson [{w_lo:.1%}, {w_hi:.1%}] | CP [{cp_lo:.1%}, {cp_hi:.1%}] --")
        for var in ("V-T", "V-S"):
            vd = [r["varianti"][var] for r in sub]
            k_prom = sum(1 for x in vd if x["promossa"])
            w0, w1 = wilson_ci95(k_prom, n_semi)
            c0, c1 = clopper_pearson(k_prom, n_semi, 0.95)
            ns = [x["n"] for x in vd]
            rs = [x["r_medio"] for x in vd if x["r_medio"] is not None]
            r_mean = mean(rs)
            r_se = stdev(rs) / math.sqrt(len(rs))
            fails = Counter(nome for x in vd for nome in x["falliti"])
            top_fails = ", ".join(f"{k}: {v}/{n_semi}" for k, v in fails.most_common())
            prom_seeds = [r["seme"] for r in sub if r["varianti"][var]["promossa"]]
            under300 = sum(1 for n in ns if n < 300)
            print(f"  {var}: prom={k_prom}/{n_semi} ({k_prom/n_semi:.1%}, W[{w0:.1%},{w1:.1%}], CP[{c0:.1%},{c1:.1%}]) | "
                  f"n={mean(ns):.1f} (min={min(ns)},max={max(ns)},<300={under300}) | R={r_mean:+.4f}±{r_se:.4f} | "
                  f"fallimenti=[{top_fails}] | semi_prom={prom_seeds}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
