#!/usr/bin/env python3
"""MANDATO R15 (Compito B) — Taratura empirica del banco su mercati inventati (sintetico.mercato).

- B1 (NULLO): 20 semi (1..20) con deriva=0.0, spinta=0.0 sul periodo di sviluppo (2023-11-15..2026-11-12).
- B2 (VANTAGGIO PIANTATO): 20 semi (1..20) per ciascuna delle 3 intensità spinta in {0.005, 0.01, 0.02}.
- B3: Frequenza di fallimento per ciascuno dei 9 criteri + analisi di dove si perde il segnale.
- Verifica aggiuntiva di coerenza: 1 seme passato attraverso sintetico.scrivi_cache -> caricatore.carica.
Usa al più 2 worker in parallelo; solo dati inventati in cartelle temporanee con rete bloccata.
"""
import argparse
import json
import math
import os
import sys
import tempfile
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
    if n == 0:
        return 0.0, 0.0
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
            "motivi_veto": d.get("motivi_veto"),
            "promossa": d["screening"]["promossa"],
            "falliti": [c["nome"] for c in criteri if not c["passa"]],
        }
    return out


def verifica_roundtrip_cache(radice: Path) -> None:
    sys.path.insert(0, str(radice))
    from brain.laboratorio.esecuzione import caricatore as C, esegui_h002 as E, sigillo as S, sintetico as SN

    inizio, fine = E.PERIODO_SVILUPPO
    giorni = (fine - inizio).days + 1
    bid, ask = SN.mercato(inizio, giorni, seme=1, spinta=0.02)
    r_mem = E.esegui_sviluppo(bid, ask)

    with tempfile.TemporaryDirectory(prefix="r15_b_cache_") as td_str:
        td = Path(td_str)
        reg = td / "reg.json"
        sh = td / "scheda.md"
        sh.write_text("# scheda finta\n")
        S.sigilla(reg, E.IPOTESI, sh, ["V-T", "V-S"], "2026-11-17T00:00:00Z")
        cb, ca = td / "XAUUSD", td / "XAUUSD_ASK"
        SN.scrivi_cache(bid, cb, inizio=inizio, fine=fine)
        SN.scrivi_cache(ask, ca, inizio=inizio, fine=fine)
        bid_c, ask_c, info = C.carica(cb, ca, inizio, fine, "sviluppo", reg, E.IPOTESI, sh)
        r_disk = E.esegui_sviluppo(bid_c, ask_c)

    vt_mem = r_mem["varianti"]["V-T"]["metriche"]["r_medio"]
    vt_disk = r_disk["varianti"]["V-T"]["metriche"]["r_medio"]
    print(f"[ROUNDTRIP scrivi_cache -> caricatore.carica] minuti={info['minuti_bid']} incomp={info['feriali_incompleti_bid']} R_mem={vt_mem:.6f} R_disk={vt_disk:.6f}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", type=Path, default=RADICE)
    ap.add_argument("--semi", type=int, default=20)
    ap.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()

    verifica_rete_bloccata()
    t_start = time.perf_counter()
    verifica_roundtrip_cache(args.radice.resolve())

    griglia = [0.0, 0.005, 0.01, 0.02]
    semi = list(range(1, args.semi + 1))
    compiti = [(sp, s) for sp in griglia for s in semi]

    risultati = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for res in pool.map(_esegui_singolo, compiti):
            risultati.append(res)

    t_tot = time.perf_counter() - t_start
    json_path = Path(__file__).with_name("r15_taratura_risultati.json")
    json_path.write_text(json.dumps({"tempo_s": t_tot, "semi": semi, "griglia": griglia, "righe": risultati},
                                    indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\n=== RIEPILOGO TARATURA (N={len(semi)} semi x {len(griglia)} livelli, {args.workers} worker, tempo={t_tot:.1f}s) ===")
    for sp in griglia:
        sub = [r for r in risultati if r["spinta"] == sp]
        any_prom = sum(1 for r in sub if any(v["promossa"] for v in r["varianti"].values()))
        lo_any, hi_any = wilson_ci95(any_prom, len(sub))
        print(f"\n-- spinta={sp:.3f} | almeno una variante promossa (V-T o V-S): {any_prom}/{len(sub)} ({any_prom/len(sub):.1%}, IC95 Wilson [{lo_any:.1%}, {hi_any:.1%}]) --")
        for var in ("V-T", "V-S"):
            vd = [r["varianti"][var] for r in sub]
            k_prom = sum(1 for x in vd if x["promossa"])
            lo, hi = wilson_ci95(k_prom, len(vd))
            ns = [x["n"] for x in vd]
            rs = [x["r_medio"] for x in vd if x["r_medio"] is not None]
            r_mean = mean(rs) if rs else 0.0
            r_se = (stdev(rs) / math.sqrt(len(rs))) if len(rs) > 1 else 0.0
            fails = Counter(nome for x in vd for nome in x["falliti"])
            top_fails = ", ".join(f"{k}: {v}/{len(vd)}" for k, v in fails.most_common())
            print(f"  {var}: prom={k_prom}/{len(vd)} ({k_prom/len(vd):.1%}, IC95 [{lo:.1%}, {hi:.1%}]) | "
                  f"n_medio={mean(ns):.1f} | R_medio={r_mean:+.4f}±{r_se:.4f} | fallimenti=[{top_fails}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
