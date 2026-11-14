"""Replica indipendente del programma di screening H-002 v3.1 (§6-§8).

Scritta alla cieca prima di leggere brain/laboratorio/esecuzione/criteri.py,
esegui_h002.py, sigillo.py e caricatore.py, partendo da H-002-ORB-v3.md (§6-§8)
e dal simulatore revisionato brain/laboratorio/simulatori/orb_londra.py.
"""
from __future__ import annotations

import math
import random
from dataclasses import replace
from datetime import date
from pathlib import Path
import sys
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from brain.laboratorio.simulatori import orb_londra as O  # noqa: E402
from brain.laboratorio.esecuzione import sintetico as SN  # noqa: E402


RIPETIZIONI_CASUALI = 1000
SEME_CASUALE_DEFAULT = 20261115


def _percentile_rango_vicino(valori_ordinati: List[float], q: float) -> float:
    if not valori_ordinati:
        raise ValueError("lista vuota per percentile")
    idx = max(0, min(len(valori_ordinati) - 1, math.ceil(q * len(valori_ordinati)) - 1))
    return valori_ordinati[idx]


def _confronto_casuale(
    giorni: List[O.Giorno],
    par: O.Parametri,
    tr_base: List[dict],
    n_rip: int = RIPETIZIONI_CASUALI,
    seme: int = SEME_CASUALE_DEFAULT,
) -> dict:
    """1.000 estrazioni casuali 50/50 sugli stessi giorni d'ingresso della variante (§6)."""
    if not tr_base:
        return {"ripetizioni": n_rip, "perc95": None, "media_casuali": None}
    m_buy = {t["data"]: t["r"] for t in O.specchio(giorni, par, lato_fisso="acquisto")}
    m_sell = {t["data"]: t["r"] for t in O.specchio(giorni, par, lato_fisso="vendita")}
    date_strat = [t["data"] for t in tr_base]

    rng = random.Random(seme)
    medie: List[float] = []
    for _ in range(n_rip):
        rs = []
        for d in date_strat:
            lato = "acquisto" if rng.random() < 0.5 else "vendita"
            r_val = m_buy.get(d) if lato == "acquisto" else m_sell.get(d)
            if r_val is not None:
                rs.append(r_val)
        medie.append(sum(rs) / len(rs) if rs else 0.0)
    medie.sort()
    return {
        "ripetizioni": n_rip,
        "perc95": _percentile_rango_vicino(medie, 0.95),
        "media_casuali": sum(medie) / len(medie),
    }


def _benchmark_su_giorni_comuni(
    giorni: List[O.Giorno],
    par: O.Parametri,
    tr_base: List[dict],
    lato_fisso: str,
) -> dict:
    bench_tr = O.specchio(giorni, par, lato_fisso=lato_fisso)
    strat_map = {t["data"]: t["r"] for t in tr_base}
    bench_map = {t["data"]: t["r"] for t in bench_tr}
    comuni = sorted(set(strat_map) & set(bench_map))
    if not comuni:
        return {"n_comuni": 0, "r_strat": None, "r_bench": None, "batte": False}
    r_s = sum(strat_map[d] for d in comuni) / len(comuni)
    r_b = sum(bench_map[d] for d in comuni) / len(comuni)
    return {"n_comuni": len(comuni), "r_strat": r_s, "r_bench": r_b, "batte": r_s > r_b}


def _prove_robustezza(
    bid: Dict,
    ask: Dict,
    par_base: O.Parametri,
    r_base: Optional[float],
) -> Tuple[Dict[str, dict], bool]:
    lista_par: List[Tuple[str, O.Parametri]] = [
        ("range_20", replace(par_base, or_minuti=20)),
        ("range_45", replace(par_base, or_minuti=45)),
    ]
    if par_base.target_r is not None:
        lista_par.extend([
            ("target_1.2", replace(par_base, target_r=1.2)),
            ("target_2.0", replace(par_base, target_r=2.0)),
        ])
    lista_par.extend([
        ("tetto_1.6", replace(par_base, tetto=1.6)),
        ("tetto_2.5", replace(par_base, tetto=2.5)),
    ])

    risultati: Dict[str, dict] = {}
    veto = False
    for nome, p in lista_par:
        tr = O.trade(O.prepara(bid, ask, p), p)
        m = O.metriche(tr)
        r_rob = m.get("r_medio") if m["n"] > 0 else None
        bocciata = (
            r_rob is None
            or r_rob <= 0.0
            or (r_base is not None and r_base > 0.0 and r_rob < 0.5 * r_base)
        )
        if bocciata:
            veto = True
        risultati[nome] = {"n": m["n"], "r_medio": r_rob, "veto": bocciata}
    return risultati, veto


def valuta_variante_sviluppo(
    bid: Dict,
    ask: Dict,
    nome_variante: str,
    par_base: O.Parametri,
    seme_casuale: int = SEME_CASUALE_DEFAULT,
) -> dict:
    giorni = O.prepara(bid, ask, par_base)
    tr = O.trade(giorni, par_base)
    m = O.metriche(tr)

    if m["n"] == 0:
        return {
            "variante": nome_variante,
            "n": 0,
            "r_medio": None,
            "sharpe": None,
            "dd_max": None,
            "r_vendite": None,
            "casuale": {"perc95": None},
            "bench_acquisto": {"n_comuni": 0, "r_strat": None, "r_bench": None, "batte": False},
            "bench_vendita": {"n_comuni": 0, "r_strat": None, "r_bench": None, "batte": False},
            "stress": {"n": 0, "r_medio": None},
            "robustezza": {},
            "veto_robustezza": True,
            "criteri": {f"c{i}": False for i in range(1, 10)},
            "promossa": False,
        }

    r_medio = m["r_medio"]
    sharpe = m["sharpe"]
    dd_max = m["dd_max"]
    r_vendite = m["r_vendite"]
    n_vendite = m["n_vendite"]

    casuale = _confronto_casuale(giorni, par_base, tr, seme=seme_casuale)
    b_acq = _benchmark_su_giorni_comuni(giorni, par_base, tr, "acquisto")
    b_ven = _benchmark_su_giorni_comuni(giorni, par_base, tr, "vendita")

    par_stress = replace(par_base, stress=0.20)
    tr_stress = O.trade(O.prepara(bid, ask, par_stress), par_stress)
    m_stress = O.metriche(tr_stress)
    r_stress = m_stress.get("r_medio") if m_stress["n"] > 0 else None

    rob, veto_rob = _prove_robustezza(bid, ask, par_base, r_medio)

    criteri = {
        "c1_r_medio": r_medio >= 0.05,
        "c2_sharpe": sharpe is not None and sharpe >= 0.06,
        "c3_n_min": m["n"] >= 300,
        "c4_casuale": casuale["perc95"] is not None and r_medio > casuale["perc95"],
        "c5_benchmark": b_acq["batte"] and b_ven["batte"],
        "c6_vendite": n_vendite > 0 and r_vendite is not None and r_vendite >= -0.05,
        "c7_dd": dd_max < 12.0,
        "c8_robustezza": not veto_rob,
        "c9_stress": r_stress is not None and r_stress > 0.0,
    }
    return {
        "variante": nome_variante,
        "n": m["n"],
        "r_medio": r_medio,
        "sharpe": sharpe,
        "dd_max": dd_max,
        "r_vendite": r_vendite,
        "n_vendite": n_vendite,
        "casuale": casuale,
        "bench_acquisto": b_acq,
        "bench_vendita": b_ven,
        "stress": {"n": m_stress["n"], "r_medio": r_stress},
        "robustezza": rob,
        "veto_robustezza": veto_rob,
        "criteri": criteri,
        "promossa": all(criteri.values()),
    }


def esegui_sui_tre_mercati() -> List[dict]:
    mercati = [
        ("casuale", SN.mercato(date(2024, 1, 1), 800, seme=3, sd=0.7)),
        ("vantaggio_spinta", SN.mercato(date(2024, 1, 1), 800, seme=3, sd=0.7, spinta=0.01)),
        ("sola_tendenza_deriva", SN.mercato(date(2024, 1, 1), 800, seme=3, sd=0.7, deriva=0.01)),
    ]
    out: List[dict] = []
    for nome_m, (bid, ask) in mercati:
        for nome_v, par in (("V-T", O.V_T), ("V-S", O.V_S)):
            ris = valuta_variante_sviluppo(bid, ask, nome_v, par)
            ris["mercato"] = nome_m
            out.append(ris)
    return out


def main() -> None:
    for r in esegui_sui_tre_mercati():
        falliti = [k for k, v in r["criteri"].items() if not v]
        print(
            f"[{r['mercato']:20s} | {r['variante']}] n={r['n']} R={r['r_medio']:.5f} "
            f"Sh={r['sharpe']:.5f} DD={r['dd_max']:.3f} R_vend={r['r_vendite']:.5f} "
            f"p95={r['casuale']['perc95']:.5f} b_acq={r['bench_acquisto']['r_bench']:.5f} "
            f"b_ven={r['bench_vendita']['r_bench']:.5f} stress={r['stress']['r_medio']:.5f} "
            f"veto={r['veto_robustezza']} promossa={r['promossa']} falliti={falliti}"
        )
        for kn, rv in r["robustezza"].items():
            print(f"   rob {kn:10s}: n={rv['n']} R={rv['r_medio']:.5f} veto={rv['veto']}")


if __name__ == "__main__":
    main()
