"""Confronto giorno per giorno e trade per trade tra la replica Gemini e Claude (`orb_londra`)."""
from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
import sys
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[4]
GEMINI_DIR = Path(__file__).resolve().parents[1]
for p in (str(REPO_ROOT), str(GEMINI_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from brain.laboratorio.simulatori import orb_londra as claude  # noqa: E402
from replica_h002 import genera_dati, replica  # noqa: E402


TOLL = 1e-9

MAPPA_MOTIVI_CLAUDE = {
    "valido": None,
    "fine settimana o festivo": "fine_settimana_o_festivo",
    "minuti del range insufficienti": "minuti_range_insufficienti",
    "meno di 20 sessioni precedenti": "storico_insufficiente",
    "range oltre il tetto": "tetto_ampiezza",
    "manca lo spread delle sessioni precedenti": "spread_storici_insufficienti",
    "range sotto il minimo dei costi": "minimo_ampiezza",
    "nessun minuto eseguibile dopo il segnale": "nessun_minuto_dopo_segnale",
    "ingresso oltre la candela successiva": "ingresso_scaduto",
}

MAPPA_USCITA_CLAUDE = {
    "target": "TARGET",
    "stop": "STOP",
    "fine sessione": "FINE_SESSIONE",
    "fine sessione senza quotazioni": "FINE_SESSIONE",
}

MAPPA_LATO_CLAUDE = {
    "acquisto": "BUY",
    "vendita": "SELL",
}


def _converti_per_claude(
    minuti: List[replica.MinutoMercato],
) -> Tuple[Dict[datetime, claude.Quota], Dict[datetime, claude.Quota]]:
    bid: Dict[datetime, claude.Quota] = {}
    ask: Dict[datetime, claude.Quota] = {}
    for m in minuti:
        bid[m.open_time_utc] = (
            float(m.bid_open),
            float(m.bid_high),
            float(m.bid_low),
            float(m.bid_close),
        )
        if m.ask_open is not None:
            assert m.ask_high is not None and m.ask_low is not None and m.ask_close is not None
            ask[m.open_time_utc] = (
                float(m.ask_open),
                float(m.ask_high),
                float(m.ask_low),
                float(m.ask_close),
            )
    return bid, ask


def _vicini(a: float, b: float, toll: float = TOLL) -> bool:
    return abs(a - b) <= toll


def _mappa_giorni_claude(
    giorni_claude: List[claude.Giorno],
    bid: Dict[datetime, claude.Quota],
    par: claude.Parametri,
) -> Dict[object, dict]:
    per_data: Dict[object, dict] = {}
    for g in giorni_claude:
        per_data[g.data] = {
            "valido": g.valido,
            "motivo": MAPPA_MOTIVI_CLAUDE.get(g.motivo, g.motivo),
            "motivo_raw": g.motivo,
            "lato": MAPPA_LATO_CLAUDE.get(g.lato) if g.lato else None,
            "ra_alto": g.ra_alto,
            "ra_basso": g.ra_basso,
            "a": g.a,
            "entrabile": g.minuti is not None,
        }
    date_bid = {t.astimezone(claude.LONDRA).date() for t in bid}
    for d in sorted(date_bid):
        if d in per_data:
            continue
        if d.weekday() >= 5 or d in claude.esclusi(d.year):
            motivo = "fine_settimana_o_festivo"
        else:
            motivo = "minuti_range_insufficienti"
        per_data[d] = {
            "valido": False,
            "motivo": motivo,
            "motivo_raw": motivo,
            "lato": None,
            "ra_alto": None,
            "ra_basso": None,
            "a": None,
            "entrabile": False,
        }
    return per_data


def _confronta_lista_trade(
    nome: str,
    tg: List[replica.TradeEseguito],
    tc: List[dict],
) -> List[dict]:
    diff: List[dict] = []
    map_g = {t.data: t for t in tg}
    map_c = {t["data"]: t for t in tc}
    tutte = sorted(set(map_g) | set(map_c))
    for d in tutte:
        a = map_g.get(d)
        b = map_c.get(d)
        if a is None or b is None:
            diff.append({
                "tipo": "trade_mancante",
                "serie": nome,
                "data": d,
                "gemini": a,
                "claude": b,
            })
            continue
        c_lato = MAPPA_LATO_CLAUDE[b["lato"]]
        c_uscita_motivo = MAPPA_USCITA_CLAUDE.get(b["motivo"], b["motivo"])
        problemi = []
        if a.lato != c_lato:
            problemi.append(f"lato {a.lato}!={c_lato}")
        if not _vicini(float(a.prezzo_ingresso), b["entrata"]):
            problemi.append(f"entrata {float(a.prezzo_ingresso):.6f}!={b['entrata']:.6f}")
        if not _vicini(float(a.prezzo_uscita), b["uscita"]):
            problemi.append(f"uscita {float(a.prezzo_uscita):.6f}!={b['uscita']:.6f}")
        if a.motivo_uscita != c_uscita_motivo:
            problemi.append(f"motivo_uscita {a.motivo_uscita}!={c_uscita_motivo}")
        if a.once != b["once"]:
            problemi.append(f"once {a.once}!={b['once']}")
        if not _vicini(float(a.r_netto), b["r"]):
            problemi.append(f"r {float(a.r_netto):.12f}!={b['r']:.12f}")
        if problemi:
            diff.append({
                "tipo": "trade_diverso",
                "serie": nome,
                "data": d,
                "problemi": problemi,
                "gemini": a,
                "claude": b,
            })
    return diff


def esegui_confronto(semi: Tuple[int, ...] = (101, 202, 303)) -> dict:
    configurazioni = [
        ("V-T", "V-T", 30, Decimal("1.5"), Decimal("2"), False, claude.V_T),
        ("V-S", "V-S", 30, Decimal("1.5"), Decimal("2"), False, claude.V_S),
        ("V-T_stress", "V-T", 30, Decimal("1.5"), Decimal("2"), True, replace(claude.V_T, stress=0.20)),
        ("V-S_stress", "V-S", 30, Decimal("1.5"), Decimal("2"), True, replace(claude.V_S, stress=0.20)),
        ("RA20", "V-T", 20, Decimal("1.5"), Decimal("2"), False, replace(claude.V_T, or_minuti=20)),
        ("RA45", "V-T", 45, Decimal("1.5"), Decimal("2"), False, replace(claude.V_T, or_minuti=45)),
        ("target1.2", "V-T", 30, Decimal("1.2"), Decimal("2"), False, replace(claude.V_T, target_r=1.2)),
        ("target2.0", "V-T", 30, Decimal("2.0"), Decimal("2"), False, replace(claude.V_T, target_r=2.0)),
        ("tetto1.6", "V-T", 30, Decimal("1.5"), Decimal("1.6"), False, replace(claude.V_T, tetto=1.6)),
        ("tetto2.5", "V-T", 30, Decimal("1.5"), Decimal("2.5"), False, replace(claude.V_T, tetto=2.5)),
    ]
    riepilogo: List[dict] = []
    totale_giorni = 0
    totale_trade_strat = 0
    totale_trade_bench = 0

    for seme in semi:
        minuti = genera_dati.genera_serie_anno(seme)
        bid, ask = _converti_per_claude(minuti)
        for label, var_g, ra_m, tgt_m, tet_m, stress_flag, par_c in configurazioni:
            res_g = replica.esegui_replica(
                minuti,
                variante=var_g,
                ra_minuti=ra_m,
                target_mult=tgt_m,
                tetto_mult=tet_m,
                stress=stress_flag,
            )
            giorni_c = claude.prepara(bid, ask, par_c)
            trade_c = claude.trade(giorni_c, par_c)
            resoc_c = claude.resoconto(bid, ask, par_c)

            map_gc = _mappa_giorni_claude(giorni_c, bid, par_c)
            map_gg = {g.data: g for g in res_g.giorni}
            diff_giorni = []
            for d in sorted(set(map_gg) | set(map_gc)):
                gg = map_gg.get(d)
                gc = map_gc.get(d)
                if gg is None or gc is None:
                    diff_giorni.append(("giorno_mancante", d, gg, gc))
                    continue
                prob = []
                if gg.valido != gc["valido"]:
                    prob.append(f"valido {gg.valido}!={gc['valido']}")
                if gg.motivo_esclusione != gc["motivo"]:
                    prob.append(f"motivo {gg.motivo_esclusione}!={gc['motivo']}")
                if gg.segnale_direzione != gc["lato"]:
                    prob.append(f"segnale {gg.segnale_direzione}!={gc['lato']}")
                if prob:
                    diff_giorni.append(("giorno_diverso", d, prob, gg, gc))

            diff_trade = _confronta_lista_trade("strategia", res_g.trades, trade_c)

            met_g = replica.calcola_metriche(res_g.trades)
            met_c = claude.metriche(trade_c)
            diff_metriche: List[str] = []
            if met_g["num_trade"] != met_c["n"]:
                diff_metriche.append(f"n {met_g['num_trade']}!={met_c['n']}")
            if met_g["num_trade"] > 0:
                for kg, kc in (
                    ("win_rate", "vinti"),
                    ("r_medio", "r_medio"),
                    ("sharpe", "sharpe"),
                    ("drawdown_max", "dd_max"),
                ):
                    vg, vc = met_g[kg], met_c[kc]
                    if (vg is None) != (vc is None) or (vg is not None and not _vicini(vg, vc)):
                        diff_metriche.append(f"{kc} {vg}!={vc}")
                if met_g["perdite_consecutive_max"] != met_c["serie_perdite"]:
                    diff_metriche.append(
                        f"serie_perdite {met_g['perdite_consecutive_max']}!={met_c['serie_perdite']}"
                    )

            diff_bench: List[dict] = []
            if label in ("V-T", "V-S", "V-T_stress"):
                bench_buy_c = claude.specchio(giorni_c, par_c, lato_fisso="acquisto")
                bench_sell_c = claude.specchio(giorni_c, par_c, lato_fisso="vendita")
                diff_bench.extend(_confronta_lista_trade("bench_buy", res_g.trades_compro, bench_buy_c))
                diff_bench.extend(_confronta_lista_trade("bench_sell", res_g.trades_vendo, bench_sell_c))
                totale_trade_bench += len(res_g.trades_compro) + len(res_g.trades_vendo)

            totale_giorni += len(res_g.giorni)
            totale_trade_strat += len(res_g.trades)
            riepilogo.append({
                "seme": seme,
                "config": label,
                "n_giorni_g": len(res_g.giorni),
                "n_trade_g": len(res_g.trades),
                "n_trade_c": len(trade_c),
                "neg_spread_g": res_g.minuti_spread_negativo,
                "neg_spread_c": resoc_c["minuti_spread_negativo"],
                "diff_giorni": diff_giorni,
                "diff_trade": diff_trade,
                "diff_bench": diff_bench,
                "diff_metriche": diff_metriche,
            })

    return {
        "totale_giorni_confrontati": totale_giorni,
        "totale_trade_strategia": totale_trade_strat,
        "totale_trade_benchmark": totale_trade_bench,
        "righe": riepilogo,
    }


def esegui_sonde_mirate() -> List[dict]:
    """Sonde sintetiche mirate su casi di bordo per verificare divergenze tra codice di Claude e scheda."""
    from datetime import date, time, timedelta
    esiti: List[dict] = []

    def _costruisci_giornata(d: date, ask_window_fn):
        base_t = datetime.combine(d, time(8, 0), tzinfo=claude.LONDRA).astimezone(timezone.utc)
        out: List[replica.MinutoMercato] = []
        for m in range(0, 600):
            t_utc = base_t + timedelta(minutes=m)
            t_lon = t_utc.astimezone(claude.LONDRA).time()
            if time(8, 0) <= t_lon < time(8, 45):
                bo, bh, bl, bc = Decimal("2000"), Decimal("2002"), Decimal("1998"), Decimal("2000")
            elif t_lon >= time(8, 45) and t_lon < time(9, 0):
                bo = bh = bl = bc = Decimal("2003")
            else:
                bo = bh = bl = bc = Decimal("2003")
            sp = ask_window_fn(t_lon)
            if sp is None:
                out.append(replica.MinutoMercato(t_utc, bo, bh, bl, bc))
            else:
                out.append(
                    replica.MinutoMercato(
                        t_utc, bo, bh, bl, bc, bo + sp, bh + sp, bl + sp, bc + sp
                    )
                )
        return out

    # Costruisci 20 sessioni di storia (gen 2026) con ASK variabile per sonde spread
    def _serie_con_storia(ask_storia_fn, ask_oggi_fn=lambda _: Decimal("0.20")):
        d_target = date(2026, 2, 10)
        giorni_ok = []
        cur = d_target
        while len(giorni_ok) < 20:
            cur -= timedelta(days=1)
            if not replica.is_giorno_escluso(cur):
                giorni_ok.append(cur)
        minuti: List[replica.MinutoMercato] = []
        for idx, d in enumerate(reversed(giorni_ok)):
            fn = ask_storia_fn if idx < 7 else (lambda _: Decimal("0.20"))
            minuti.extend(_costruisci_giornata(d, fn))
        minuti.extend(_costruisci_giornata(d_target, ask_oggi_fn))
        return d_target, minuti

    # Sonda 1: RA=45 con ASK solo in [08:30, 08:45) su 7 sessioni storiche
    d1, m1 = _serie_con_storia(lambda t: Decimal("0.20") if time(8, 30) <= t < time(8, 45) else None)
    b1, a1 = _converti_per_claude(m1)
    gc45 = [g for g in claude.prepara(b1, a1, replace(claude.V_T, or_minuti=45)) if g.data == d1][0]
    gg45 = [g for g in replica.esegui_replica(m1, ra_minuti=45).giorni if g.data == d1][0]
    esiti.append({
        "sonda": "RA45_spread_in_0830_0845",
        "gemini": (gg45.valido, gg45.motivo_esclusione),
        "claude": (gc45.valido, gc45.motivo),
    })

    # Sonda 2: ASK disponibile solo dopo le 16:45 (es. 17:00) nelle 7 sessioni storiche
    d2, m2 = _serie_con_storia(lambda t: Decimal("0.20") if t >= time(17, 0) else None)
    b2, a2 = _converti_per_claude(m2)
    gc_late = [g for g in claude.prepara(b2, a2, claude.V_T) if g.data == d2][0]
    gg_late = [g for g in replica.esegui_replica(m2).giorni if g.data == d2][0]
    esiti.append({
        "sonda": "spread_solo_dopo_1645",
        "gemini": (gg_late.valido, gg_late.motivo_esclusione),
        "claude": (gc_late.valido, gc_late.motivo),
    })

    # Sonda 3: ASK < BID alle 17:00 (oltre 16:45) su giornata valida con segnale
    d3, m3 = _serie_con_storia(
        lambda _: Decimal("0.20"),
        lambda t: Decimal("-0.50") if t == time(17, 0) else Decimal("0.20"),
    )
    b3, a3 = _converti_per_claude(m3)
    gc_neg = [g for g in claude.prepara(b3, a3, claude.V_T) if g.data == d3][0]
    rg_neg = replica.esegui_replica(m3)
    tg_neg = [t for t in rg_neg.trades if t.data == d3][0]
    esiti.append({
        "sonda": "minuti_scartati_dopo_1645",
        "gemini_trade_scartati": tg_neg.minuti_scartati,
        "gemini_resoconto_neg": rg_neg.minuti_spread_negativo,
        "claude_giorno_scartati": gc_neg.minuti_scartati,
        "claude_resoconto_neg": claude.resoconto(b3, a3, claude.V_T)["minuti_spread_negativo"],
    })
    return esiti


def main() -> None:
    ris = esegui_confronto()
    print(
        f"Totale giorni-config: {ris['totale_giorni_confrontati']} | "
        f"trade strategia (Gemini): {ris['totale_trade_strategia']} | "
        f"trade benchmark (Gemini): {ris['totale_trade_benchmark']}"
    )
    for r in ris["righe"]:
        dg = len(r["diff_giorni"])
        dt = len(r["diff_trade"])
        db = len(r["diff_bench"])
        dm = len(r["diff_metriche"])
        ns = f"{r['neg_spread_g']} vs {r['neg_spread_c']}"
        print(
            f"[seme={r['seme']} {r['config']:10s}] giorni={r['n_giorni_g']} "
            f"trade={r['n_trade_g']}/{r['n_trade_c']} "
            f"neg_spread={ns} | diff_giorni={dg} diff_trade={dt} diff_bench={db} diff_metriche={dm}"
        )
        for item in r["diff_giorni"][:15]:
            print("  G:", item[:3])
        for item in r["diff_trade"][:15]:
            print("  T:", item["data"], item.get("problemi", item["tipo"]))
        for item in r["diff_bench"][:15]:
            print("  B:", item["serie"], item["data"], item.get("problemi", item["tipo"]))
        if dm:
            print("  M:", r["diff_metriche"])

    print("\n--- SONDE MIRATE ---")
    for s in esegui_sonde_mirate():
        print(s)


if __name__ == "__main__":
    main()
