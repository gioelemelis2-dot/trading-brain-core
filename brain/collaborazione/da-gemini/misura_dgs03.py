"""Misura riproducibile di DGS-03 sul periodo di sviluppo (2023-11-15 -> 2026-11-12).

Non legge MAI dati del periodo di verifica sigillata (<= 2023-10-31).
Calcola i tre numeri richiesti per V-T e V-S:
1) frequenza della condizione 'nessun minuto eseguibile in [16:30, 16:45)' (fine sessione senza quotazioni);
2) impatto escludendo quei trade (n, R medio, verdetto di screening);
3) impatto correggendo in avanti dalle 16:30 senza ripiegare prima delle 16:30 (n, R medio, verdetto).
"""
import argparse
from dataclasses import replace
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from statistics import mean, median, stdev
import sys

RADICE = Path(__file__).resolve().parents[3]
if str(RADICE) not in sys.path:
    sys.path.insert(0, str(RADICE))

from brain.laboratorio.esecuzione import caricatore as C  # noqa: E402
from brain.laboratorio.esecuzione import criteri as K  # noqa: E402
from brain.laboratorio.esecuzione import esegui_h002 as E  # noqa: E402
from brain.laboratorio.simulatori import orb_londra as O  # noqa: E402


class _SimEscludi:
    """Wrapper di orb_londra che esclude da `trade` (e dai benchmark/casuale sugli stessi giorni) i DGS-03."""

    @staticmethod
    def prepara(bid, ask, par):
        return O.prepara(bid, ask, par)

    @staticmethod
    def trade(giorni, par):
        return [t for t in O.trade(giorni, par) if t["motivo"] != "fine sessione senza quotazioni"]

    @staticmethod
    def specchio(giorni, par, lato_fisso=None, lati=None):
        esclusi_d = {t["data"] for t in O.trade(giorni, par) if t["motivo"] == "fine sessione senza quotazioni"}
        return [t for t in O.specchio(giorni, par, lato_fisso=lato_fisso, lati=lati) if t["data"] not in esclusi_d]

    @staticmethod
    def metriche(tr):
        return O.metriche(tr)

    resoconto = staticmethod(O.resoconto)


class _SimForwardOnly:
    """Variante forward-only per DGS-03: se [16:30, 16:45) non ha minuti eseguibili, NON ripiega sul
    minuto prima delle 16:30, ma attende in avanti la prima quotazione eseguibile >= 16:30 nella giornata
    (eseguendo stop/target minuto per minuto nell'attesa ed uscendo all'apertura del primo minuto >= 16:30)."""

    @staticmethod
    def prepara(bid, ask, par=O.V_T):
        giorni = O.prepara(bid, ask, par)
        per_data = {}
        for t in sorted(bid):
            per_data.setdefault(t.astimezone(O.LONDRA).date(), []).append(t)
        ask_t = set(ask)

        def eseguibile(t):
            return t in ask_t and ask[t][0] >= bid[t][0] and ask[t][3] >= bid[t][3]

        out = []
        for g in giorni:
            if not (g.valido and g.minuti):
                out.append(g)
                continue
            fine = O._utc(g.data, par.fine_sessione)
            if g.minuti[-1][0] >= fine:
                out.append(g)
                continue
            # [16:30, 16:45) era vuoto: guarda SOLO in avanti dalle 16:30 (>= 16:45 nella giornata)
            dopo_forward = [t for t in per_data.get(g.data, []) if t >= fine and eseguibile(t)][:1]
            if not dopo_forward:
                # Nessuna quotazione eseguibile >= 16:30 in tutta la giornata restante: esce con i minuti fino a fine giornata senza chiudere prima delle 16:30
                out.append(replace(g, minuti=g.minuti, motivo="nessuna quotazione >= 16:30"))
            else:
                nuovi = list(g.minuti) + [(t, bid[t], ask[t]) for t in dopo_forward]
                out.append(replace(g, minuti=nuovi))
        return out

    @staticmethod
    def _simula(giorno, lato, par, stop_livello=None):
        if not giorno.minuti:
            return None
        fine = O._utc(giorno.data, par.fine_sessione)
        if giorno.minuti[-1][0] < fine:
            raise RuntimeError(f"DGS-03 forward-only non risolvibile in giornata per {giorno.data}: 0 minuti >= 16:30")
        return O.simula(giorno, lato, par, stop_livello=stop_livello)

    @classmethod
    def trade(cls, giorni, par):
        out = []
        for g in giorni:
            if g.valido and g.lato:
                r = cls._simula(g, g.lato, par)
                if r:
                    out.append(r)
        return out

    @classmethod
    def specchio(cls, giorni, par, lato_fisso=None, lati=None):
        if any(g.valido and g.minuti and g.minuti[-1][0] < O._utc(g.data, par.fine_sessione) for g in giorni):
            raise RuntimeError("Giorno senza quotazioni >= 16:30")
        return O.specchio(giorni, par, lato_fisso=lato_fisso, lati=lati)

    @staticmethod
    def metriche(tr):
        return O.metriche(tr)

    resoconto = staticmethod(O.resoconto)


def _prova_sintetica_forward() -> dict:
    """Verifica su un caso sintetico stile Caso d'oro #8 (buco 16:30..16:44, ripresa alle 16:50) che la
    correzione forward-only diverga davvero dal fallback all'indietro."""
    d = date(2026, 1, 7)
    bid, ask = {}, {}
    # 20 sessioni precedenti 08:00..16:45 (range A=5, spread=0.1)
    for k in range(1, 45):
        g = d - timedelta(days=k)
        if g.weekday() >= 5 or g in O.esclusi(g.year):
            continue
        t0 = O._utc(g, time(8, 0))
        for m in range(9 * 60):
            t = t0 + timedelta(minutes=m)
            lo, hi = (1998.0, 2003.0) if m < 30 else (2000.0, 2000.5)
            bid[t] = (lo, hi, lo, lo)
            ask[t] = (lo + 0.1, hi + 0.1, lo + 0.1, lo + 0.1)
        if sum(1 for dt in {x.date() for x in bid} if dt < d) >= 21:
            break
    # Giorno test: range 1998..2002, rottura 08:30..08:44 a 2003, poi sale fino a 16:29 (2011.8),
    # buco 16:30..16:49, riprende alle 16:50 a 2005.0 (crollo dopo 16:30!)
    t0 = O._utc(d, time(8, 0))
    for m in range(8 * 60 + 30):  # 08:00 .. 16:29
        t = t0 + timedelta(minutes=m)
        if m < 30:
            p = (2000.0, 2002.0, 1998.0, 2000.0)
        elif m < 45:
            p = (2001.0, 2003.5, 2000.5, 2003.0)
        elif m == 45:
            p = (2003.0, 2003.5, 2002.5, 2003.2)
        else:
            p = (2011.8, 2012.0, 2011.5, 2011.8)
        bid[t] = p
        ask[t] = tuple(x + 0.3 for x in p)
    t_1650 = O._utc(d, time(16, 50))
    bid[t_1650] = (2005.0, 2005.2, 2004.8, 2005.0)
    ask[t_1650] = (2005.3, 2005.5, 2005.1, 2005.3)
    tr_base = O.trade(O.prepara(bid, ask, O.V_S), O.V_S)
    tr_fwd = _SimForwardOnly.trade(_SimForwardOnly.prepara(bid, ask, O.V_S), O.V_S)
    return {
        "base_motivo": tr_base[-1]["motivo"],
        "base_uscita": round(tr_base[-1]["uscita"], 4),
        "base_r": round(tr_base[-1]["r"], 5),
        "fwd_motivo": tr_fwd[-1]["motivo"],
        "fwd_uscita": round(tr_fwd[-1]["uscita"], 4),
        "fwd_r": round(tr_fwd[-1]["r"], 5),
    }


def _riassunto(v: str, res_v: dict, sim, prep, par) -> dict:
    tr = sim.trade(prep(par), par)
    sq = [t for t in tr if t["motivo"] == "fine sessione senza quotazioni"]
    motivi = {}
    for t in tr:
        motivi[t["motivo"]] = motivi.get(t["motivo"], 0) + 1
    m = res_v["metriche"]
    return {
        "variante": v,
        "n": m["n"],
        "r_medio": m["r_medio"],
        "sharpe": m["sharpe"],
        "dd_max": m["dd_max"],
        "promossa": res_v["screening"]["promossa"],
        "criteri_passati": sum(1 for c in res_v["screening"]["criteri"] if c["passa"]),
        "criteri_totali": len(res_v["screening"]["criteri"]),
        "veto": res_v["veto"],
        "n_dgs03": len(sq),
        "pct_dgs03": (100.0 * len(sq) / m["n"]) if m["n"] else 0.0,
        "motivi": motivi,
    }


def _dettaglio_trade(giorni, par) -> list:
    """Restituisce per ogni trade eseguito anche la distanza dallo stop e il costo diretto dello slittamento."""
    out = []
    for g in giorni:
        if not (g.valido and g.lato):
            continue
        t = O.simula(g, g.lato, par)
        if not t:
            continue
        t0, b0, a0 = g.minuti[0]
        su = (g.lato == "acquisto")
        stop = g.ra_basso if su else g.ra_alto
        entrata_mkt = a0[0] if su else b0[0]
        dist_mkt = abs(entrata_mkt - stop)
        dist_exec = abs(t["entrata"] - stop)
        perd_stop_comm = dist_exec + par.slip_uscita + par.stress + par.commissione
        slip_usc_eff = 0.0 if t["motivo"] == "target" else (par.slip_uscita + par.stress)
        slip_usd_oz = (par.slip_ingresso + par.stress) + slip_usc_eff
        slip_dir_r = (slip_usd_oz * t["once"]) / par.rischio_usd
        comm_dir_r = (par.commissione * t["once"]) / par.rischio_usd
        out.append(dict(
            t,
            dist_mkt=dist_mkt,
            dist_exec=dist_exec,
            perd_stop_comm=perd_stop_comm,
            slip_usd_oz=slip_usd_oz,
            slip_dir_r=slip_dir_r,
            comm_dir_r=comm_dir_r,
            r_lordo_dir=t["r"] + slip_dir_r,
            r_lordo_puro_dir=t["r"] + slip_dir_r + comm_dir_r,
        ))
    return out


def _stat_lista(xs: list) -> dict:
    s = sorted(xs)
    return {
        "media": mean(s),
        "mediana": median(s),
        "sd": stdev(s) if len(s) > 1 else 0.0,
        "min": s[0],
        "max": s[-1],
        "somma": sum(s),
    }


def _misura_4(bid, ask) -> None:
    print("=== QUARTA MISURA: LORDO SENZA SLITTAMENTO/STRESS, DISTANZA STOP, COSTO SLITTAMENTO IN R ===")
    prep = E._Giorni(O, bid, ask)
    rob_noslip = {
        v: {rn: {k: val for k, val in ch.items()} for rn, ch in E.ROBUSTEZZA[v].items()}
        for v in E.VARIANTI
    }
    var_noslip = {v: replace(par, slip_ingresso=0.0, slip_uscita=0.0, stress=0.0) for v, par in E.VARIANTI.items()}
    var_lordo_puro = {
        v: replace(par, slip_ingresso=0.0, slip_uscita=0.0, stress=0.0, commissione=0.0)
        for v, par in E.VARIANTI.items()
    }
    res_noslip = E.esegui_sviluppo(bid, ask, varianti=var_noslip, robustezza=rob_noslip, stress=0.0)
    res_lordo_puro = E.esegui_sviluppo(bid, ask, varianti=var_lordo_puro, robustezza=rob_noslip, stress=0.0)

    for v, par_base in E.VARIANTI.items():
        det_base = _dettaglio_trade(prep(par_base), par_base)
        giorni_base = prep(par_base)
        det_noslip_stessi_g = _dettaglio_trade(giorni_base, var_noslip[v])
        det_puro_stessi_g = _dettaglio_trade(giorni_base, var_lordo_puro[v])
        det_noslip = _dettaglio_trade(prep(var_noslip[v]), var_noslip[v])

        # Scomposizione esatta vinti nella baseline
        fs_vinti = sum(1 for x in det_base if x["motivo"] == "fine sessione" and x["r"] > 0)
        tgt_vinti = sum(1 for x in det_base if x["motivo"] == "target" and x["r"] > 0)
        stop_vinti = sum(1 for x in det_base if x["motivo"] == "stop" and x["r"] > 0)

        # Confronto appaiato per data tra baseline e senza slip (con comm 0.07)
        map_base = {x["data"]: x for x in det_base}
        map_ns = {x["data"]: x for x in det_noslip}
        comuni = sorted(set(map_base) & set(map_ns))
        diff_sim_r = [map_ns[d]["r"] - map_base[d]["r"] for d in comuni]
        solo_base = sorted(set(map_base) - set(map_ns))
        solo_ns = sorted(set(map_ns) - set(map_base))
        cambi_motivo = sum(1 for d in comuni if map_ns[d]["motivo"] != map_base[d]["motivo"])

        print(f"--- {v} ---")
        print("Baseline breakdown vinti:", {
            "n": len(det_base),
            "vinti_tot": sum(1 for x in det_base if x["r"] > 0),
            "pct_vinti": 100.0 * sum(1 for x in det_base if x["r"] > 0) / len(det_base),
            "target_vinti": tgt_vinti,
            "fine_sessione_vinti": fs_vinti,
            "stop_vinti": stop_vinti,
        })
        print("Distanza stop USD |entrata_mkt - stop| (senza slip):", _stat_lista([x["dist_mkt"] for x in det_base]))
        print("Distanza stop USD |entrata_exec - stop| (baseline, +0.10):", _stat_lista([x["dist_exec"] for x in det_base]))
        print("Perdita attesa allo stop + comm USD/oz (baseline):", _stat_lista([x["perd_stop_comm"] for x in det_base]))
        print("Once baseline:", _stat_lista([x["once"] for x in det_base]))
        print("Costo diretto slittamento in R (trade-by-trade su path fisso, tutti):", _stat_lista([x["slip_dir_r"] for x in det_base]))
        for mot in sorted({x["motivo"] for x in det_base}):
            xs = [x["slip_dir_r"] for x in det_base if x["motivo"] == mot]
            print(f"  Costo diretto slip in R [{mot}] (n={len(xs)}):", _stat_lista(xs))
        print("Costo diretto commissione in R (0.07 USD/oz):", _stat_lista([x["comm_dir_r"] for x in det_base]))
        print("R medio lordo diretto a path fisso (con comm 0.07):", mean(x["r_lordo_dir"] for x in det_base))
        print("R medio lordo diretto a path fisso (anche senza comm):", mean(x["r_lordo_puro_dir"] for x in det_base))
        print("Sim sugli STESSI giorni base SENZA slip/stress (con comm 0.07):", {
            "n": len(det_noslip_stessi_g),
            "vinti_pct": 100.0 * sum(1 for x in det_noslip_stessi_g if x["r"] > 0) / len(det_noslip_stessi_g),
            "r_medio": mean(x["r"] for x in det_noslip_stessi_g),
            "motivi": {m: sum(1 for x in det_noslip_stessi_g if x["motivo"] == m) for m in sorted({x["motivo"] for x in det_noslip_stessi_g})},
        })
        print("Sim sugli STESSI giorni base LORDO PURO (senza slip/stress/comm 0.0):", {
            "n": len(det_puro_stessi_g),
            "vinti_pct": 100.0 * sum(1 for x in det_puro_stessi_g if x["r"] > 0) / len(det_puro_stessi_g),
            "r_medio": mean(x["r"] for x in det_puro_stessi_g),
        })

        r_ns = res_noslip["varianti"][v]
        m_ns = r_ns["metriche"]
        print("Simulazione completa SENZA slittamento/stress (con comm 0.07):", {
            "n": m_ns["n"],
            "vinti_pct": 100.0 * m_ns["vinti"],
            "r_medio": m_ns["r_medio"],
            "sharpe": m_ns["sharpe"],
            "dd_max": m_ns["dd_max"],
            "r_acquisti": m_ns["r_acquisti"],
            "r_vendite": m_ns["r_vendite"],
            "casuale_p95": r_ns["casuale"]["percentile_95"],
            "bench_compro": r_ns["benchmark"]["r_compro"],
            "bench_vendo": r_ns["benchmark"]["r_vendo"],
            "veto": r_ns["veto"],
            "promossa": r_ns["screening"]["promossa"],
            "criteri_passati": [(c["nome"], c["passa"]) for c in r_ns["screening"]["criteri"]],
        })
        print("Confronto appaiato (sim senza slip vs baseline):", {
            "comuni": len(comuni),
            "solo_base": len(solo_base),
            "solo_no_slip": len(solo_ns),
            "cambi_motivo_uscita": cambi_motivo,
            "delta_R_sim_appaiato": _stat_lista(diff_sim_r),
        })

        r_p = res_lordo_puro["varianti"][v]
        m_p = r_p["metriche"]
        print("Simulazione completa LORDO PURO (senza slip/stress/comm 0.07):", {
            "n": m_p["n"],
            "vinti_pct": 100.0 * m_p["vinti"],
            "r_medio": m_p["r_medio"],
            "sharpe": m_p["sharpe"],
            "dd_max": m_p["dd_max"],
            "veto": r_p["veto"],
            "promossa": r_p["screening"]["promossa"],
            "criteri_passati": sum(1 for c in r_p["screening"]["criteri"] if c["passa"]),
        })


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", type=Path,
                    default=Path("/Users/gioele/Downloads/trading-brain-core/brain/dati/reali/cache_dukascopy"))
    args = ap.parse_args()

    print("=== CONTROLLO SINTETICO DIVERGENZA FORWARD-ONLY VS BASELINE ===")
    print(_prova_sintetica_forward())

    ini, fine = E.PERIODO_SVILUPPO
    bid, ask, info = C.carica(args.cache / E.SIMBOLO, args.cache / f"{E.SIMBOLO}_ASK", ini, fine, "sviluppo")
    print("=== DATI SVILUPPO ===")
    print({k: (len(v) if isinstance(v, list) else v) for k, v in info.items()},
          "ripetizioni:", K.RIPETIZIONI, "seme:", K.SEME)

    # 1) Scansione calendario su tutti i feriali non esclusi
    per_data = {}
    for t in sorted(bid):
        per_data.setdefault(t.astimezone(O.LONDRA).date(), []).append(t)
    ask_t = set(ask)
    d = ini
    feriali_non_esclusi = 0
    senza_finestra_uscita = []
    while d <= fine:
        if d.weekday() < 5 and d not in O.esclusi(d.year):
            feriali_non_esclusi += 1
            t1630, t1645 = O._utc(d, time(16, 30)), O._utc(d, time(16, 45))
            ts = per_data.get(d, [])
            ex = [t for t in ts if t1630 <= t < t1645 and t in ask_t and ask[t][0] >= bid[t][0] and ask[t][3] >= bid[t][3]]
            if not ex:
                senza_finestra_uscita.append(d.isoformat())
        d += timedelta(days=1)
    print(f"Feriali non esclusi ({ini}..{fine}): {feriali_non_esclusi}, senza [16:30, 16:45): {len(senza_finestra_uscita)}")

    # 2) Baseline, Esclusione, Forward-only
    scenarios = [("BASELINE", O), ("ESCLUSIONE", _SimEscludi), ("FORWARD_ONLY", _SimForwardOnly)]
    for nome_scen, sim in scenarios:
        res = E.esegui_sviluppo(bid, ask, sim=sim)
        prep = E._Giorni(sim, bid, ask)
        print(f"=== {nome_scen} ===")
        for v, par in E.VARIANTI.items():
            print(_riassunto(v, res["varianti"][v], sim, prep, par))

    # 3) Quarta misura: R medio lordo senza slittamento/stress, distanza stop USD, costo slittamento in R
    _misura_4(bid, ask)


if __name__ == "__main__":
    main()
