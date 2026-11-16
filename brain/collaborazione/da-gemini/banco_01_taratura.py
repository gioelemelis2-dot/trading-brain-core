"""Mandato BANCO-01: banco di taratura del motore sulla filiera completa su mercati inventati.

Esegue `sintetico.mercato(date(2024, 1, 1), 800, seme=seme, sd=0.7, spinta=sp)` +
`esegui_h002.esegui_sviluppo(bid, ask)` (orb_londra + 9 criteri v3.1, senza DSR)
su 8 livelli di spinta × 25 semi (200 mercati sintetici, 400 valutazioni V-T/V-S),
usando al massimo 2 processi in parallelo e zero dati/rete reali.
"""
from __future__ import annotations

from collections import Counter
from datetime import date
import json
import math
import multiprocessing as mp
from pathlib import Path
from statistics import mean, stdev
import sys
import time

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from brain.laboratorio.esecuzione import esegui_h002 as E  # noqa: E402
from brain.laboratorio.esecuzione import sintetico as SN  # noqa: E402
from brain.laboratorio.studi import potenza_soglia as PS  # noqa: E402

INIZIO = date(2024, 1, 1)
GIORNI = 800
SD = 0.7
SPINTE = (0.0, 0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05)
SEMI = tuple(range(1001, 1026))  # 25 semi per livello -> 200 mercati totali
MAX_PROCESSI = 2
Z95 = PS.Z95
SOGLIA_IA02 = 0.15


def _valuta_uno(args):
    spinta, seme = args
    bid, ask = SN.mercato(INIZIO, GIORNI, seme=seme, sd=SD, spinta=spinta)
    ris = E.esegui_sviluppo(bid, ask)
    righe = []
    for var in ("V-T", "V-S"):
        rv = ris["varianti"][var]
        m = rv["metriche"]
        n = m.get("n", 0)
        r_med = m.get("r_medio")
        es = m.get("errore_std")
        sh = m.get("sharpe")
        sd_camp = (es * math.sqrt(n)) if (es is not None and n > 0) else None
        scr = rv["screening"]
        falliti = [c["nome"] for c in scr["criteri"] if not c["passa"]]
        lim_inf = (r_med - Z95 * es) if (r_med is not None and es is not None) else None
        righe.append({
            "spinta": spinta,
            "seme": seme,
            "variante": var,
            "n": n,
            "r_medio": r_med,
            "errore_std": es,
            "sd_camp": sd_camp,
            "sharpe": sh,
            "lim_inf_95": lim_inf,
            "promossa_v31": bool(scr["promossa"]),
            "stima_ge_015": r_med is not None and r_med >= SOGLIA_IA02,
            "limite_ge_015": lim_inf is not None and lim_inf >= SOGLIA_IA02,
            "criteri_falliti": falliti,
        })
    return righe


def main() -> None:
    t0 = time.monotonic()
    lavori = [(sp, se) for sp in SPINTE for se in SEMI]
    righe = []
    # Regola 2: al massimo 2 processi in parallelo
    with mp.get_context("spawn").Pool(MAX_PROCESSI) as pool:
        for pacchetto in pool.map(_valuta_uno, lavori):
            righe.extend(pacchetto)
    dt = time.monotonic() - t0

    riepilogo = []
    for var in ("V-T", "V-S"):
        for sp in SPINTE:
            sub = [r for r in righe if r["variante"] == var and r["spinta"] == sp]
            k = len(sub)
            ns = [r["n"] for r in sub]
            rs = [r["r_medio"] for r in sub if r["r_medio"] is not None]
            ess = [r["errore_std"] for r in sub if r["errore_std"] is not None]
            sds = [r["sd_camp"] for r in sub if r["sd_camp"] is not None]
            shs = [r["sharpe"] for r in sub if r["sharpe"] is not None]

            mu_hat = mean(rs)
            sd_hat = mean(sds)
            n_hat = mean(ns)
            es_hat = mean(ess)
            sh_hat = mean(shs)
            sd_r_tra_semi = stdev(rs) if len(rs) > 1 else 0.0

            p_v31 = sum(1 for r in sub if r["promossa_v31"]) / k
            p_stima = sum(1 for r in sub if r["stima_ge_015"]) / k
            p_limite = sum(1 for r in sub if r["limite_ge_015"]) / k

            prev_stima = PS.prob_promozione(mu_hat, sd_hat, round(n_hat), SOGLIA_IA02, "stima")
            prev_limite = PS.prob_promozione(mu_hat, sd_hat, round(n_hat), SOGLIA_IA02, "limite")
            prev_stima_semi = mean(PS.prob_promozione(mu_hat, r["sd_camp"], r["n"], SOGLIA_IA02, "stima") for r in sub)
            prev_limite_semi = mean(PS.prob_promozione(mu_hat, r["sd_camp"], r["n"], SOGLIA_IA02, "limite") for r in sub)

            cont_fall = Counter()
            for r in sub:
                cont_fall.update(r["criteri_falliti"])

            riepilogo.append({
                "variante": var,
                "spinta": sp,
                "n_semi": k,
                "n_medio": round(n_hat, 1),
                "n_min": min(ns),
                "n_max": max(ns),
                "r_medio": round(mu_hat, 6),
                "sd_r_tra_semi": round(sd_r_tra_semi, 6),
                "errore_std_medio": round(es_hat, 6),
                "sd_trade_medio": round(sd_hat, 6),
                "sharpe_medio": round(sh_hat, 6),
                "promo_v31_cnt": sum(1 for r in sub if r["promossa_v31"]),
                "promo_v31": round(p_v31, 4),
                "promo_stima_015_cnt": sum(1 for r in sub if r["stima_ge_015"]),
                "promo_stima_015": round(p_stima, 4),
                "promo_limite_015_cnt": sum(1 for r in sub if r["limite_ge_015"]),
                "promo_limite_015": round(p_limite, 4),
                "prev_ps_stima": round(prev_stima, 4),
                "prev_ps_limite": round(prev_limite, 4),
                "prev_ps_stima_per_seme": round(prev_stima_semi, 4),
                "prev_ps_limite_per_seme": round(prev_limite_semi, 4),
                "diff_stima_pp": round((p_stima - prev_stima) * 100.0, 2),
                "diff_limite_pp": round((p_limite - prev_limite) * 100.0, 2),
                "criteri_falliti": dict(sorted(cont_fall.items())),
            })

    out_path = Path(__file__).resolve().parent / "banco_01_risultati.json"
    out_path.write_text(json.dumps({
        "parametri": {
            "inizio": INIZIO.isoformat(),
            "giorni": GIORNI,
            "sd": SD,
            "spinte": list(SPINTE),
            "semi": list(SEMI),
            "max_processi": MAX_PROCESSI,
            "z95": Z95,
            "soglia_ia02": SOGLIA_IA02,
            "durata_s": round(dt, 2),
        },
        "riepilogo": riepilogo,
        "grezzi": righe,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Completato in {dt:.1f}s ({len(righe)} valutazioni). Salvato {out_path.name}")
    for row in riepilogo:
        print(
            f"{row['variante']} sp={row['spinta']:<5} n={row['n_medio']:>5.1f} "
            f"R={row['r_medio']:+.4f} sd={row['sd_trade_medio']:.4f} ES={row['errore_std_medio']:.4f} SR={row['sharpe_medio']:+.4f} | "
            f"v3.1={row['promo_v31']*100:>5.1f}% ({row['promo_v31_cnt']:>2}/{row['n_semi']}) | "
            f"stima={row['promo_stima_015']*100:>5.1f}% vs PS={row['prev_ps_stima']*100:>5.1f}% ({row['diff_stima_pp']:+.1f}pp) | "
            f"lim={row['promo_limite_015']*100:>5.1f}% vs PS={row['prev_ps_limite']*100:>5.1f}% ({row['diff_limite_pp']:+.1f}pp)"
        )


if __name__ == "__main__":
    main()
