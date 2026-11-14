"""Analisi statistica ed esplorativa su H-002 (sviluppo 2023-11-15 -> 2026-11-12, commit 99474bb).

Copre i punti 1, 3, 4, 5 e la base numerica del punto 6 (incertezza e riclassificazione a 3 verdetti).
Dichiarazione: le sezioni 3, 4, 5 sono ESPLORATIVE e NON costituiscono prove né criteri di promozione.
"""
from dataclasses import replace
from math import sqrt
from pathlib import Path
import random
from statistics import NormalDist, mean, stdev
import sys

RADICE = Path(__file__).resolve().parents[3]
if str(RADICE) not in sys.path:
    sys.path.insert(0, str(RADICE))

from brain.laboratorio.esecuzione import caricatore as C  # noqa: E402
from brain.laboratorio.esecuzione import criteri as K  # noqa: E402
from brain.laboratorio.esecuzione import esegui_h002 as E  # noqa: E402
from brain.laboratorio.simulatori import orb_londra as O  # noqa: E402

Z95 = NormalDist().inv_cdf(0.975)  # 1.959963984540054


def _stats(rs: list) -> dict:
    n = len(rs)
    if n == 0:
        return {"n": 0}
    m = mean(rs)
    sd = stdev(rs) if n > 1 else 0.0
    es = (sd / sqrt(n)) if n > 1 else None
    lo = (m - Z95 * es) if es is not None else None
    hi = (m + Z95 * es) if es is not None else None
    return {
        "n": n,
        "vinti": sum(1 for x in rs if x > 0),
        "vinti_pct": 100.0 * sum(1 for x in rs if x > 0) / n,
        "r_medio": m,
        "sd": sd,
        "es": es,
        "ic95": (lo, hi),
        "somma": sum(rs),
    }


def _casuale_dettaglio(giorni, par, ripetizioni: int = K.RIPETIZIONI, seme: int = K.SEME) -> dict:
    tr = O.trade(giorni, par)
    strat = {x["data"]: x["r"] for x in tr}
    compro = {x["data"]: x["r"] for x in O.specchio(giorni, par, lato_fisso="acquisto")}
    vendo = {x["data"]: x["r"] for x in O.specchio(giorni, par, lato_fisso="vendita")}
    comuni = [d for d in sorted(strat) if d in compro and d in vendo]
    esiti = [(compro[d], vendo[d]) for d in comuni]
    r_strat = mean(strat[d] for d in comuni)
    rng = random.Random(seme)
    medie = [sum(e[rng.randrange(2)] for e in esiti) / len(esiti) for _ in range(ripetizioni)]
    mu_c = mean(medie)
    sd_c = stdev(medie)
    p95 = K.percentile(medie, 0.95)
    pct_lt = 100.0 * sum(1 for x in medie if x < r_strat) / len(medie)
    pct_le = 100.0 * sum(1 for x in medie if x <= r_strat) / len(medie)
    z_rand = (r_strat - mu_c) / sd_c
    return {
        "n": len(esiti),
        "seme": seme,
        "ripetizioni": ripetizioni,
        "r_strategia": r_strat,
        "media_casuale": mu_c,
        "sd_casuale": sd_c,
        "percentile_95": p95,
        "pct_sotto": pct_lt,
        "pct_minore_uguale": pct_le,
        "z_casuale": z_rand,
        "min_casuale": min(medie),
        "max_casuale": max(medie),
    }


def _decili(coppie: list) -> list:
    """`coppie`: lista di (ampiezza_A, r). Ritorna 10 decili con statistiche ed IC 95%."""
    ord_c = sorted(coppie, key=lambda x: x[0])
    n = len(ord_c)
    out = []
    for i in range(10):
        a = (n * i) // 10
        b = (n * (i + 1)) // 10
        blocco = ord_c[a:b]
        st = _stats([r for _, r in blocco])
        st["decile"] = i + 1
        st["a_min"] = blocco[0][0]
        st["a_max"] = blocco[-1][0]
        out.append(st)
    return out


def _classifica_soglia(m: float, es: float, soglia: float, op: str = ">=") -> str:
    lo, hi = m - Z95 * es, m + Z95 * es
    if op == ">=":
        if lo >= soglia:
            return "promossa"
        if hi < soglia:
            return "bocciata"
        return "non decidibile"
    # op == ">"
    if lo > soglia:
        return "promossa"
    if hi <= soglia:
        return "bocciata"
    return "non decidibile"


def main() -> None:
    cache = Path("/Users/gioele/Downloads/trading-brain-core/brain/dati/reali/cache_dukascopy")
    ini, fine = E.PERIODO_SVILUPPO
    bid, ask, info = C.carica(cache / E.SIMBOLO, cache / f"{E.SIMBOLO}_ASK", ini, fine, "sviluppo")
    print("Z95:", Z95, "DATI:", info["dati_sha256"])

    prep = E._Giorni(O, bid, ask)

    # --- PUNTO 1: CONFRONTO CASUALE DETTAGLIATO ---
    print("\n=== PUNTO 1: CONFRONTO CASUALE (seme=20261115, rip=1000) ===")
    for v, par in E.VARIANTI.items():
        g_base = prep(par)
        print(f"{v} NETTA:", _casuale_dettaglio(g_base, par))
        par_ns = replace(par, slip_ingresso=0.0, slip_uscita=0.0, stress=0.0)
        print(f"{v} NO-SLIP (stessi 456 giorni):", _casuale_dettaglio(g_base, par_ns))
        par_puro = replace(par_ns, commissione=0.0)
        print(f"{v} LORDO PURO (stessi 456 giorni):", _casuale_dettaglio(g_base, par_puro))

    # --- PUNTO 3: DECILI DI AMPIEZZA + RANGE 20'/30'/45' ---
    print("\n=== PUNTO 3A: DECILI DI AMPIEZZA DEL RANGE A (EXPLORATIVO) ===")
    for v, par in E.VARIANTI.items():
        g_base = prep(par)
        amap_base = {g.data: g.a for g in g_base}
        tr_base = O.trade(g_base, par)
        print(f"-- {v} BASELINE NETTA (n={len(tr_base)}) --")
        for d in _decili([(amap_base[t["data"]], t["r"]) for t in tr_base]):
            print(d)

        par_puro = replace(par, slip_ingresso=0.0, slip_uscita=0.0, stress=0.0, commissione=0.0)
        g_puro = prep(par_puro)
        amap_puro = {g.data: g.a for g in g_puro}
        tr_puro = O.trade(g_puro, par_puro)
        print(f"-- {v} LORDO PURO COMPLETO CON FILTRO ALLARGATO (n={len(tr_puro)}) --")
        for d in _decili([(amap_puro[t["data"]], t["r"]) for t in tr_puro]):
            print(d)
        base_set = {t["data"] for t in tr_base}
        extra = [t["r"] for t in tr_puro if t["data"] not in base_set]
        stessi = [t["r"] for t in tr_puro if t["data"] in base_set]
        print(f"  Confronto 456 base vs 198 extra in LORDO PURO ({v}):")
        print("    456 base:", _stats(stessi))
        print("    198 extra (range stretto):", _stats(extra))

    print("\n=== PUNTO 3B: RANGE 20' CONTRO 30' CONTRO 45' (ESPLORATIVO) ===")
    for v, par in E.VARIANTI.items():
        for minuti in (20, 30, 45):
            p = replace(par, or_minuti=minuti)
            tr = O.trade(prep(p), p)
            st = _stats([t["r"] for t in tr])
            p_puro = replace(p, slip_ingresso=0.0, slip_uscita=0.0, stress=0.0, commissione=0.0)
            tr_p = O.trade(prep(p), p_puro)
            st_p = _stats([t["r"] for t in tr_p])
            print(f"{v} range {minuti}' NETTA:", st)
            print(f"{v} range {minuti}' LORDO PURO (stessi giorni del filtro {minuti}'):", st_p)

    # --- PUNTO 4: DIREZIONE (ACQUISTI VS VENDITE) ---
    print("\n=== PUNTO 4: ACQUISTI VS VENDITE (ESPLORATIVO) ===")
    for v, par in E.VARIANTI.items():
        g_base = prep(par)
        tr_net = O.trade(g_base, par)
        par_ns = replace(par, slip_ingresso=0.0, slip_uscita=0.0, stress=0.0)
        tr_ns = O.trade(g_base, par_ns)
        par_puro = replace(par_ns, commissione=0.0)
        tr_puro = O.trade(g_base, par_puro)
        for et, tr in [("NETTA", tr_net), ("NO-SLIP(comm0.07)", tr_ns), ("LORDO_PURO", tr_puro)]:
            for lato in ("acquisto", "vendita"):
                rs = [t["r"] for t in tr if t["lato"] == lato]
                print(f"{v} {et} {lato}:", _stats(rs))

    # --- PUNTO 5: TEMPO (PER ANNO SOLARE) ---
    print("\n=== PUNTO 5: PER ANNO SOLARE (ESPLORATIVO) ===")
    for v, par in E.VARIANTI.items():
        g_base = prep(par)
        tr_net = O.trade(g_base, par)
        par_puro = replace(par, slip_ingresso=0.0, slip_uscita=0.0, stress=0.0, commissione=0.0)
        tr_puro = O.trade(g_base, par_puro)
        for et, tr in [("NETTA", tr_net), ("LORDO_PURO", tr_puro)]:
            anni = sorted({t["data"].year for t in tr})
            for a in anni:
                rs = [t["r"] for t in tr if t["data"].year == a]
                print(f"{v} {et} {a}:", _stats(rs))

    # --- PUNTO 6: RICLASSIFICAZIONE A 3 VERDETTI (H-002 BASELINE + LORDO) ---
    print("\n=== PUNTO 6: INCERTEZZA SU TUTTI I CRITERI DI H-002 (BASELINE) ===")
    for v, par in E.VARIANTI.items():
        g_base = prep(par)
        tr = O.trade(g_base, par)
        st = _stats([t["r"] for t in tr])
        st_v = _stats([t["r"] for t in tr if t["lato"] == "vendita"])
        tr_str = O.trade(g_base, replace(par, stress=E.STRESS))
        st_str = _stats([t["r"] for t in tr_str])
        print(f"{v} C1 R_medio (soglia >= 0.05):", st, "-> verdetto:", _classifica_soglia(st["r_medio"], st["es"], 0.05, ">="))
        print(f"{v} C6 R_vendite (soglia >= -0.05):", st_v, "-> verdetto:", _classifica_soglia(st_v["r_medio"], st_v["es"], -0.05, ">="))
        print(f"{v} C9 R_stress (soglia > 0):", st_str, "-> verdetto:", _classifica_soglia(st_str["r_medio"], st_str["es"], 0.0, ">"))
        for rname, cambi in E.ROBUSTEZZA[v].items():
            p_r = replace(par, **cambi)
            st_r = _stats([t["r"] for t in O.trade(prep(p_r), p_r)])
            print(f"  {v} rob {rname} (soglia > 0):", st_r, "-> verdetto:", _classifica_soglia(st_r["r_medio"], st_r["es"], 0.0, ">"))
        # Benchmark & Casuale anche con diff appaiata
        compro = {x["data"]: x["r"] for x in O.specchio(g_base, par, lato_fisso="acquisto")}
        vendo = {x["data"]: x["r"] for x in O.specchio(g_base, par, lato_fisso="vendita")}
        strat = {x["data"]: x["r"] for x in tr}
        comuni = sorted(set(strat) & set(compro) & set(vendo))
        for bname, bmap in [("compro", compro), ("vendo", vendo)]:
            diff = [strat[d] - bmap[d] for d in comuni]
            st_d = _stats(diff)
            print(f"  {v} diff appaiata vs {bname} (soglia > 0):", st_d, "-> verdetto:", _classifica_soglia(st_d["r_medio"], st_d["es"], 0.0, ">"))


if __name__ == "__main__":
    main()
