"""Mandato R11 (feat/esecutore-h002 @ 83c8956):
1. Riesecuzione delle sonde R7 (P1..P7, con verifica end-to-end da CLI).
2. Confronto replica_criteri_h002 (adeguata ad A2 e A3) vs esegui_h002 (differenza 0).
3. Secondo attacco: 7 nuove sonde (R11-S1..S7) e 7 nuovi mutanti (MR01..MR07).
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import contextlib
from datetime import date, datetime, timedelta, timezone
import io
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from brain.laboratorio.esecuzione import caricatore as C  # noqa: E402
from brain.laboratorio.esecuzione import criteri as K  # noqa: E402
from brain.laboratorio.esecuzione import esegui_h002 as E  # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S  # noqa: E402
from brain.laboratorio.esecuzione import sintetico as SN  # noqa: E402
from brain.laboratorio.simulatori import orb_londra as O  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import replica_criteri_h002 as R  # noqa: E402

ORA = "2026-11-15T03:00:00Z"


def _cli(argv):
    buf_out, buf_err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        rc = E.main(argv)
    return rc, buf_out.getvalue(), buf_err.getvalue()


def check_r7_probes() -> dict:
    ris = {}
    # P1: verifica su variante bocciata o senza sviluppo -> ora deve dare rc=2
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg, cache, rap_sv, rap_vf = d / "reg.json", d / "cache", d / "sv.md", d / "vf.md"
        b1, a1 = SN.mercato(date(2024, 1, 1), 120, seme=3, sd=0.7)
        SN.scrivi_cache(b1, cache / "XAUUSD", inizio=date(2024, 1, 1), fine=date(2024, 4, 29))
        SN.scrivi_cache(a1, cache / "XAUUSD_ASK", inizio=date(2024, 1, 1), fine=date(2024, 4, 29))
        b2, a2 = SN.mercato(date(2010, 1, 1), 120, seme=4, sd=0.7, spinta=0.01)
        SN.scrivi_cache(b2, cache / "XAUUSD", inizio=date(2010, 1, 1), fine=date(2010, 4, 29))
        SN.scrivi_cache(a2, cache / "XAUUSD_ASK", inizio=date(2010, 1, 1), fine=date(2010, 4, 29))
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
        rc_sv, _, _ = _cli(["--modalita", "sviluppo", "--inizio", "2024-01-01", "--fine", "2024-04-29",
                            "--rapporto", str(rap_sv), "--registro", str(reg), "--scheda", str(scheda),
                            "--cache", str(cache), "--ora", ORA, "--ripetizioni", "50"])
        rc_vf, _, err_vf = _cli(["--modalita", "verifica", "--varianti", "V-T", "--inizio", "2010-01-01",
                                 "--fine", "2010-04-29", "--rapporto", str(rap_vf), "--registro", str(reg),
                                 "--scheda", str(scheda), "--cache", str(cache), "--ora", ORA])
        ris["P1"] = {"rc_sv": rc_sv, "rc_vf": rc_vf, "bloccata": rc_vf == 2, "err": err_vf.strip()}

    # P2: chiamata separata (--varianti V-T quando entrambe promosse) -> rc=2
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg, cache, rap = d / "reg.json", d / "cache", d / "vf.md"
        b, a = SN.mercato(date(2010, 1, 1), 60, seme=4, sd=0.7, spinta=0.01)
        SN.scrivi_cache(b, cache / "XAUUSD", inizio=date(2010, 1, 1), fine=date(2010, 3, 1))
        SN.scrivi_cache(a, cache / "XAUUSD_ASK", inizio=date(2010, 1, 1), fine=date(2010, 3, 1))
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
        S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": True}, ORA)
        S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-S", "promossa": True}, ORA)
        rc_sep, _, err_sep = _cli(["--modalita", "verifica", "--varianti", "V-T", "--inizio", "2010-01-01",
                                   "--fine", "2010-03-01", "--rapporto", str(rap), "--registro", str(reg),
                                   "--scheda", str(scheda), "--cache", str(cache), "--ora", ORA])
        ris["P2"] = {"rc_separata": rc_sep, "bloccata": rc_sep == 2, "err": err_sep.strip()}

    # P3: sigillo con 1 sola variante -> rc=2
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg, cache, rap = d / "reg.json", d / "cache", d / "sv.md"
        b, a = SN.mercato(date(2024, 1, 1), 60, seme=3, sd=0.7)
        SN.scrivi_cache(b, cache / "XAUUSD", inizio=date(2024, 1, 1), fine=date(2024, 2, 29))
        SN.scrivi_cache(a, cache / "XAUUSD_ASK", inizio=date(2024, 1, 1), fine=date(2024, 2, 29))
        S.sigilla(reg, "H-002", scheda, ["V-T"], ORA)
        rc_n1, _, err_n1 = _cli(["--modalita", "sviluppo", "--inizio", "2024-01-01", "--fine", "2024-02-29",
                                 "--rapporto", str(rap), "--registro", str(reg), "--scheda", str(scheda),
                                 "--cache", str(cache), "--ora", ORA])
        ris["P3"] = {"rc_n1": rc_n1, "bloccata": rc_n1 == 2, "err": err_n1.strip()}

    # P4 (ex P6 Claude): cache vuota non brucia verifica -> rc=2 e esecuzioni invariate
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg, cache_vuota, rap = d / "reg.json", d / "cache_inesistente", d / "vf.md"
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
        S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": True}, ORA)
        S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-S", "promossa": False}, ORA)
        rc_vuota, _, err_vuota = _cli(["--modalita", "verifica", "--varianti", "V-T", "--inizio", "2010-01-01",
                                       "--fine", "2010-02-28", "--rapporto", str(rap), "--registro", str(reg),
                                       "--scheda", str(scheda), "--cache", str(cache_vuota), "--ora", ORA])
        esec_vf = [e for e in S.leggi(reg)["esecuzioni"] if e["ruolo"] == "verifica"]
        ris["P4"] = {"rc_vuota": rc_vuota, "bloccata": rc_vuota == 2 and len(esec_vf) == 0, "err": err_vuota.strip()}

    # P5 (ex P4 Claude): CLI verifica passa tutti gli anni inclusi quelli a 0 trade
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg, cache, rap = d / "reg.json", d / "cache", d / "vf.md"
        b, a = SN.mercato(date(2010, 1, 1), 60, seme=2, sd=0.7, spinta=0.03)
        SN.scrivi_cache(b, cache / "XAUUSD", inizio=date(2008, 1, 1), fine=date(2010, 3, 1))
        SN.scrivi_cache(a, cache / "XAUUSD_ASK", inizio=date(2008, 1, 1), fine=date(2010, 3, 1))
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
        S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": True}, ORA)
        rc_anni, _, _ = _cli(["--modalita", "verifica", "--varianti", "V-T", "--inizio", "2008-01-01",
                              "--fine", "2010-03-01", "--rapporto", str(rap), "--registro", str(reg),
                              "--scheda", str(scheda), "--cache", str(cache), "--ora", ORA])
        riga_q = [r for r in rap.read_text(encoding="utf-8").splitlines() if "quota di anni solari" in r][0]
        ris["P5"] = {"rc": rc_anni, "quota_riportata": riga_q.split("|")[3].strip(),
                     "bloccata": riga_q.split("|")[3].strip() == "0.3333"}

    # P6 (ex P5 Claude): confronto casuale usa stessi giorni S∩C∩V in valuta_variante
    dlist = [date(2025, 1, 1) + timedelta(days=k) for k in range(150)]
    class _Sim:
        @staticmethod
        def prepara(b, a, p): return []
        @staticmethod
        def trade(g, p): return [{"data": x, "lato": "acquisto", "r": 0.02} for x in dlist[:100]] + [
            {"data": x, "lato": "acquisto", "r": 0.50} for x in dlist[100:]]
        @staticmethod
        def specchio(g, p, lato_fisso=None, lati=None):
            return [{"data": x, "lato": "acquisto", "r": 0.50} for x in dlist[:100]] if lato_fisso == "acquisto" else [
                {"data": x, "lato": "vendita", "r": -0.30} for x in dlist[:100]]
        @staticmethod
        def metriche(tr): return O.metriche(tr)
    v_out = E.valuta_variante(_Sim(), E._Giorni(_Sim(), {}, {}), O.V_T, {}, 0.2, 1000, 42)
    ris["P6"] = {"r_strategia_casuale": v_out["casuale"]["r_strategia"],
                 "sopra": v_out["casuale"]["sopra"],
                 "copertura": round(v_out["casuale"]["copertura"], 6),
                 "bloccata": abs(v_out["casuale"]["r_strategia"] - 0.02) < 1e-12 and not v_out["casuale"]["sopra"]}

    # P7: embargo 2023-11-01..2023-11-14 rifiutato in verifica
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg, cache = d / "reg.json", d / "cache"
        b, a = SN.mercato(date(2023, 11, 1), 20, seme=9, sd=0.7)
        SN.scrivi_cache(b, cache / "XAUUSD")
        SN.scrivi_cache(a, cache / "XAUUSD_ASK")
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
        try:
            C.carica(cache / "XAUUSD", cache / "XAUUSD_ASK", date(2023, 11, 1), date(2023, 11, 14),
                     "verifica", reg, "H-002", scheda)
            ris["P7"] = {"bloccata": False}
        except ValueError as exc:
            ris["P7"] = {"bloccata": True, "err": str(exc)}
    return ris


def check_task2_replica() -> dict:
    mercati = [
        ("casuale", SN.mercato(date(2024, 1, 1), 800, seme=3, sd=0.7)),
        ("vantaggio_spinta", SN.mercato(date(2024, 1, 1), 800, seme=3, sd=0.7, spinta=0.01)),
        ("sola_tendenza_deriva", SN.mercato(date(2024, 1, 1), 800, seme=3, sd=0.7, deriva=0.01)),
    ]
    sviluppo_righe = []
    max_diff_det = 0.0
    max_diff_p95 = 0.0
    for nome_m, (bid, ask) in mercati:
        c_sv = E.esegui_sviluppo(bid, ask)
        for v, par in (("V-T", O.V_T), ("V-S", O.V_S)):
            g_res = R.valuta_variante_sviluppo(bid, ask, v, par)
            cx = c_sv["varianti"][v]
            cm = cx["metriche"]
            diffs = [
                abs(g_res["n"] - cm["n"]),
                abs(g_res["r_medio"] - cm["r_medio"]),
                abs(g_res["sharpe"] - cm["sharpe"]),
                abs(g_res["dd_max"] - cm["dd_max"]),
                abs(g_res["r_vendite"] - cm["r_vendite"]),
                abs(g_res["casuale"]["r_comuni"] - cx["casuale"]["r_strategia"]),
                abs(g_res["casuale"]["copertura"] - cx["casuale"]["copertura"]),
                abs(g_res["bench_acquisto"]["r_strat"] - cx["benchmark"]["r_strategia"]),
                abs(g_res["bench_acquisto"]["r_bench"] - cx["benchmark"]["r_compro"]),
                abs(g_res["bench_vendita"]["r_bench"] - cx["benchmark"]["r_vendo"]),
                abs(g_res["stress"]["r_medio"] - cx["r_stress"]),
                float(g_res["veto_robustezza"] != cx["veto"]),
                float(g_res["promossa"] != cx["screening"]["promossa"]),
            ]
            for kn, rv in g_res["robustezza"].items():
                ck = kn.replace("_", " ").replace("range 20", "range 20'").replace("range 45", "range 45'").replace(
                    "target 1.2", "target 1,2").replace("target 2.0", "target 2,0").replace(
                    "tetto 1.6", "tetto 1,6").replace("tetto 2.5", "tetto 2,5")
                diffs.append(abs(rv["r_medio"] - cx["robustezza"][ck]))
            d_det = max(diffs)
            d_p95 = abs(g_res["casuale"]["perc95"] - cx["casuale"]["percentile_95"])
            max_diff_det = max(max_diff_det, d_det)
            max_diff_p95 = max(max_diff_p95, d_p95)
            sviluppo_righe.append({
                "mercato": nome_m, "variante": v, "n": g_res["n"],
                "r_medio": round(g_res["r_medio"], 8),
                "r_comuni": round(g_res["casuale"]["r_comuni"], 8),
                "copertura": round(g_res["casuale"]["copertura"], 6),
                "p95_diff": round(d_p95, 6),
                "max_diff_det": d_det,
                "promossa": g_res["promossa"],
            })

    # Confronto su verifica (con anni 2008..2013 inclusi anni a 0 trade)
    bv, av = SN.mercato(date(2010, 1, 1), 800, seme=4, sd=0.7, spinta=0.01)
    anni = range(2008, 2014)
    c_vf = E.esegui_verifica(bv, av, ["V-T", "V-S"], n_prove=2, anni=anni)
    tr_vt = O.trade(O.prepara(bv, av, O.V_T), O.V_T)
    tr_vs = O.trade(O.prepara(bv, av, O.V_S), O.V_S)
    sh_vt = O.metriche(tr_vt)["sharpe"]
    sh_vs = O.metriche(tr_vs)["sharpe"]
    g_vt = R.valuta_variante_verifica(tr_vt, 2, anni, sharpe_altre=[sh_vs])
    g_vs = R.valuta_variante_verifica(tr_vs, 2, anni, sharpe_altre=[sh_vt])
    c_vt_q = [c["valore"] for c in c_vf["varianti"]["V-T"]["verifica"]["criteri"] if c["nome"].startswith("quota")][0]
    c_vt_u = [c["valore"] for c in c_vf["varianti"]["V-T"]["verifica"]["criteri"] if c["nome"].startswith("ultimi")][0]
    c_vs_q = [c["valore"] for c in c_vf["varianti"]["V-S"]["verifica"]["criteri"] if c["nome"].startswith("quota")][0]
    diff_vf = max(
        abs(g_vt["dsr"] - c_vf["varianti"]["V-T"]["verifica"]["dsr"]),
        abs(g_vs["dsr"] - c_vf["varianti"]["V-S"]["verifica"]["dsr"]),
        abs(g_vt["quota_anni"] - c_vt_q),
        abs(g_vt["ultimi_5"] - c_vt_u),
        abs(g_vs["quota_anni"] - c_vs_q),
        float(g_vt["promossa"] != c_vf["varianti"]["V-T"]["verifica"]["promossa"]),
        float(g_vs["promossa"] != c_vf["varianti"]["V-S"]["verifica"]["promossa"]),
    )
    return {"sviluppo": sviluppo_righe, "max_diff_det_sviluppo": max_diff_det,
            "max_diff_p95": round(max_diff_p95, 6), "diff_verifica_A3": diff_vf,
            "verifica_vt_quota": round(g_vt["quota_anni"], 6), "verifica_vt_promossa": g_vt["promossa"]}


def check_r11_second_attack() -> dict:
    out = {}

    # S1: Verifica sigillata senza trade_min né finestra minima: T=2 trade in verifica passano; e finestra ridotta 2023-07..2023-10 passa via CLI
    tr2 = [{"data": date(2023, 9, 5), "lato": "acquisto", "r": 1.0},
           {"data": date(2023, 10, 10), "lato": "acquisto", "r": 1.05}]
    kv2 = K.verifica(tr2, n_prove=2, anni=range(2023, 2024))
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg, cache, rap = d / "reg.json", d / "cache", d / "vf.md"
        # Finestra ridotta ad arte: 2022-08-01 .. 2023-10-31 invece di 2005..2023 (457 giorni = ~230 trade, solo 2022-2023)
        b, a = SN.mercato(date(2022, 8, 1), 457, seme=4, sd=0.7, spinta=0.015)
        SN.scrivi_cache(b, cache / "XAUUSD", inizio=date(2022, 8, 1), fine=date(2023, 10, 31))
        SN.scrivi_cache(a, cache / "XAUUSD_ASK", inizio=date(2022, 8, 1), fine=date(2023, 10, 31))
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
        S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": True}, ORA)
        rc_short, _, _ = _cli(["--modalita", "verifica", "--varianti", "V-T", "--inizio", "2022-08-01",
                               "--fine", "2023-10-31", "--rapporto", str(rap), "--registro", str(reg),
                               "--scheda", str(scheda), "--cache", str(cache), "--ora", ORA])
        txt = rap.read_text(encoding="utf-8") if rap.exists() else ""
    out["S1"] = {
        "k_verifica_2_trade_promossa": kv2["promossa"],
        "k_verifica_2_trade_dsr": round(kv2["dsr"], 6),
        "cli_finestra_ridotta_2022_2023_rc": rc_short,
        "cli_finestra_ridotta_promossa": "PROMOSSA IN VERIFICA" in txt,
    }

    # S2: File .bi5 da 0 byte nei feriali aggirano P6 (dati incompleti) e bruciano la verifica
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg, cache, rap = d / "reg.json", d / "cache", d / "vf.md"
        # 8 anni (2008..2015) di file .bi5 vuoti da 0 byte, e solo 60 giorni reali nel 2016!
        b, a = SN.mercato(date(2016, 1, 1), 60, seme=2, sd=0.7, spinta=0.03)
        SN.scrivi_cache(b, cache / "XAUUSD", inizio=date(2008, 1, 1), fine=date(2016, 2, 29))
        SN.scrivi_cache(a, cache / "XAUUSD_ASK", inizio=date(2008, 1, 1), fine=date(2016, 2, 29))
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
        S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": True}, ORA)
        rc_empty, _, _ = _cli(["--modalita", "verifica", "--varianti", "V-T", "--inizio", "2008-01-01",
                               "--fine", "2016-02-29", "--rapporto", str(rap), "--registro", str(reg),
                               "--scheda", str(scheda), "--cache", str(cache), "--ora", ORA])
        verifiche = [e for e in S.leggi(reg)["esecuzioni"] if e["ruolo"] == "verifica"]
    out["S2"] = {"rc_8_anni_bi5_vuoti": rc_empty, "verifica_bruciata": len(verifiche) == 1}

    # S3: CLI --ripetizioni 1 e --seme non registrati né controllati in sviluppo sbloccano verifica
    # Costruiamo mercato con r_medio ~ 0.06..0.08 ma sotto p95(1000) o mostriamo tramite CLI con cache reale/sintetica:
    # verifichiamo sia effetto su K.confronto_casuale che persistenza su registro con --ripetizioni 1
    esiti_border = [(0.40, -0.25)] * 200  # media lato casuale = +0.075, p95(1000) > 0.09
    c_1000 = K.confronto_casuale(esiti_border, 0.08, ripetizioni=1000, seme=20261115)
    seme_win = next(s for s in range(1, 50) if K.confronto_casuale(esiti_border, 0.08, ripetizioni=1, seme=s)["sopra"])
    c_1 = K.confronto_casuale(esiti_border, 0.08, ripetizioni=1, seme=seme_win)
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg, cache, rap = d / "reg.json", d / "cache", d / "sv.md"
        b, a = SN.mercato(date(2024, 1, 1), 60, seme=3, sd=0.7)
        SN.scrivi_cache(b, cache / "XAUUSD", inizio=date(2024, 1, 1), fine=date(2024, 2, 29))
        SN.scrivi_cache(a, cache / "XAUUSD_ASK", inizio=date(2024, 1, 1), fine=date(2024, 2, 29))
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
        rc_rep1, _, _ = _cli(["--modalita", "sviluppo", "--inizio", "2024-01-01", "--fine", "2024-02-29",
                              "--ripetizioni", "1", "--seme", str(seme_win),
                              "--rapporto", str(rap), "--registro", str(reg), "--scheda", str(scheda),
                              "--cache", str(cache), "--ora", ORA])
        sv_rec = [e for e in S.leggi(reg)["esecuzioni"] if e["ruolo"] == "sviluppo"][0]
    out["S3"] = {
        "c1000_sopra": c_1000["sopra"],
        "c1_seme_vincente": seme_win,
        "c1_sopra": c_1["sopra"],
        "cli_ripetizioni_1_rc": rc_rep1,
        "chiavi_salvate_in_sviluppo": sorted(sv_rec.keys()),
        "manca_ripetizioni_e_seme_in_registro": ("ripetizioni" not in sv_rec and "seme" not in sv_rec),
    }

    # S4: --rapporto che punta a una directory (OSError) brucia verifica; verifica non salva esito né rapporto_sha256; registrazione multi-variante non atomica
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg, cache, rap_dir = d / "reg.json", d / "cache", d / "cartella_rapporto"
        rap_dir.mkdir()
        b, a = SN.mercato(date(2010, 1, 1), 60, seme=4, sd=0.7, spinta=0.01)
        SN.scrivi_cache(b, cache / "XAUUSD", inizio=date(2010, 1, 1), fine=date(2010, 2, 28))
        SN.scrivi_cache(a, cache / "XAUUSD_ASK", inizio=date(2010, 1, 1), fine=date(2010, 2, 28))
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
        S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": True}, ORA)
        S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-S", "promossa": True}, ORA)
        try:
            rc_dir, _, _ = _cli(["--modalita", "verifica", "--varianti", "V-T,V-S", "--inizio", "2010-01-01",
                                 "--fine", "2010-02-28", "--rapporto", str(rap_dir), "--registro", str(reg),
                                 "--scheda", str(scheda), "--cache", str(cache), "--ora", ORA])
        except OSError as exc:
            rc_dir = f"OSError:{type(exc).__name__}"
        vf_rec = [e for e in S.leggi(reg)["esecuzioni"] if e["ruolo"] == "verifica"]
    out["S4"] = {
        "rc_rapporto_dir": rc_dir,
        "esec_verifica_bruciate": len(vf_rec),
        "chiavi_verifica_in_registro": sorted(vf_rec[0].keys()) if vf_rec else [],
        "manca_esito_e_sha256": vf_rec and ("promossa" not in vf_rec[0] and "rapporto_sha256" not in vf_rec[0]),
    }

    # S5: copertura casuale < 10% promossa senza vincolo
    dlist = [date(2024, 1, 1) + timedelta(days=k) for k in range(350)]
    class _SimCov:
        @staticmethod
        def prepara(b, a, p): return []
        @staticmethod
        def trade(g, p):
            return [{"data": x, "lato": "acquisto" if k % 2 == 0 else "vendita", "r": 0.35 if k % 4 < 2 else 0.15}
                    for k, x in enumerate(dlist)]
        @staticmethod
        def specchio(g, p, lato_fisso=None, lati=None):
            # Solo 20 giorni su 350 hanno entrambi i benchmark (copertura = 5.71%)
            return [{"data": x, "lato": lato_fisso, "r": -0.10} for x in dlist[:20]]
        @staticmethod
        def metriche(tr): return O.metriche(tr)
    res_cov = E.valuta_variante(_SimCov(), E._Giorni(_SimCov(), {}, {}), O.V_T,
                                {"rob": {"target_r": 1.2}}, 0.0, 200, 7)
    out["S5"] = {
        "copertura": round(res_cov["casuale"]["copertura"], 6),
        "n_comuni_bench": res_cov["benchmark"]["n_comuni"],
        "promossa_nonostante_copertura_5_7pct": res_cov["screening"]["promossa"],
    }

    # S6: esegui_verifica API default anni=None + sviluppo su cache A sblocca verifica su cache B senza traccia
    bv, av = SN.mercato(date(2010, 1, 1), 800, seme=4, sd=0.7, spinta=0.01)
    res_api_none = E.esegui_verifica(bv, av, ["V-T"], n_prove=2)  # anni=None default!
    q_api = [c["valore"] for c in res_api_none["varianti"]["V-T"]["verifica"]["criteri"]
             if c["nome"].startswith("quota")][0]
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg, c_sint, c_real, r_sv, r_vf = d / "reg.json", d / "c_finta", d / "c_vera", d / "sv.md", d / "vf.md"
        b1, a1 = SN.mercato(date(2024, 1, 1), 650, seme=3, sd=0.7, spinta=0.03)  # finta cache con spinta
        SN.scrivi_cache(b1, c_sint / "XAUUSD", inizio=date(2024, 1, 1), fine=date(2025, 10, 11))
        SN.scrivi_cache(a1, c_sint / "XAUUSD_ASK", inizio=date(2024, 1, 1), fine=date(2025, 10, 11))
        b2, a2 = SN.mercato(date(2010, 1, 1), 60, seme=3, sd=0.7)  # altra cache in verifica
        SN.scrivi_cache(b2, c_real / "XAUUSD", inizio=date(2010, 1, 1), fine=date(2010, 3, 1))
        SN.scrivi_cache(a2, c_real / "XAUUSD_ASK", inizio=date(2010, 1, 1), fine=date(2010, 3, 1))
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
        rc1, _, _ = _cli(["--modalita", "sviluppo", "--inizio", "2024-01-01", "--fine", "2025-10-11",
                          "--rapporto", str(r_sv), "--registro", str(reg), "--scheda", str(scheda),
                          "--cache", str(c_sint), "--ora", ORA, "--ripetizioni", "50"])
        rc2, _, _ = _cli(["--modalita", "verifica", "--varianti", "V-T,V-S", "--inizio", "2010-01-01",
                          "--fine", "2010-03-01", "--rapporto", str(r_vf), "--registro", str(reg),
                          "--scheda", str(scheda), "--cache", str(c_real), "--ora", ORA])
    out["S6"] = {"api_esegui_verifica_default_anni_none_quota": round(q_api, 4),
                 "sviluppo_su_cache_A_rc": rc1, "sblocca_verifica_su_cache_B_rc": rc2}

    # S7: sigillo.registra_esecuzione accetta variante inventata / non presente nel sigillo
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg = d / "reg.json"
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
        rec = S.registra_esecuzione(reg, "H-002", {"ruolo": "verifica", "variante": "INVENTATA"}, ORA)
    out["S7"] = {"accetta_variante_inventata": rec["variante"] == "INVENTATA"}

    return out


NUOVI_MUTANTI_R11 = [
    (
        "MR01",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        "if info[\"giorni_bid_mancanti\"] or info[\"giorni_ask_mancanti\"] or not info[\"minuti_bid\"] \\",
        "if info[\"giorni_bid_mancanti\"] or not info[\"minuti_bid\"] \\",
        "omette il controllo giorni_ask_mancanti (P6 asimmetrico su ASK)",
    ),
    (
        "MR02",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        "                or not info[\"minuti_ask\"]:                                    # P6: niente si registra",
        "                :",
        "omette il controllo not info[\"minuti_ask\"] (file ASK presenti ma vuoti)",
    ),
    (
        "MR03",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        "                if e[\"ipotesi\"] == x.ipotesi and e[\"ruolo\"] == \"sviluppo\":",
        "                if e[\"ruolo\"] == \"sviluppo\":",
        "toglie filtro e[\"ipotesi\"] == x.ipotesi negli esiti di sviluppo (fuga cross-ipotesi)",
    ),
    (
        "MR04",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        "            fatte = [e for e in S.leggi(x.registro)[\"esecuzioni\"] if e[\"ipotesi\"] == x.ipotesi\n"
        "                     and e[\"ruolo\"] == \"verifica\" and e.get(\"variante\") in promosse]",
        "            fatte = [e for e in S.leggi(x.registro)[\"esecuzioni\"] if True\n"
        "                     and e[\"ruolo\"] == \"verifica\" and e.get(\"variante\") in promosse]",
        "toglie filtro e[\"ipotesi\"] == x.ipotesi nel controllo verifica già fatta",
    ),
    (
        "MR05",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        "            ris = esegui_sviluppo(bid, ask, ripetizioni=x.ripetizioni, seme=x.seme)",
        "            ris = esegui_sviluppo(bid, ask, ripetizioni=x.ripetizioni)",
        "ignora --seme passato da CLI in esegui_sviluppo",
    ),
    (
        "MR06",
        "brain/laboratorio/esecuzione/criteri.py",
        "        _criterio(f\"DSR (N = {n_prove})\", dsr, f\"≥ {dsr_min}\", _ge(dsr, dsr_min)),",
        "        _criterio(f\"DSR (N = {n_prove})\", dsr, f\"≥ {dsr_min}\", dsr is not None and dsr > dsr_min),",
        "cambia DSR >= dsr_min in > dsr_min al bordo esatto 0.95",
    ),
    (
        "MR07",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        "                    \"sharpe\": m.get(\"sharpe\"), \"promossa\": r[\"screening\"][\"promossa\"],",
        "                    \"sharpe\": m.get(\"sharpe\"), \"promossa\": True,",
        "registra promossa=True nello sviluppo CLI ignorando l'esito reale dello screening",
    ),
]


def _run_mut(args):
    cod, rel, target, repl, desc = args
    with tempfile.TemporaryDirectory() as tmp:
        radice = Path(tmp) / "repo"
        shutil.copytree(REPO_ROOT / "brain", radice / "brain",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "cache_dukascopy", "partizioni", "*.csv", "da-gemini"))
        p = radice / rel
        orig = p.read_text(encoding="utf-8")
        assert orig.count(target) == 1, f"{cod}: target non univoco in {rel}"
        p.write_text(orig.replace(target, repl, 1), encoding="utf-8")
        env = dict(os.environ, PYTHONPATH=str(radice))
        proc = subprocess.run(
            [sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "-f",
             "brain.laboratorio.tests.test_orb_londra",
             "brain.laboratorio.tests.test_esecuzione",
             "brain.laboratorio.tests.test_esegui_h002"],
            cwd=str(radice), env=env, capture_output=True, text=True, timeout=240,
        )
        return {"codice": cod, "stato": "VIVO" if proc.returncode == 0 else "UCCISO", "rc": proc.returncode, "desc": desc}


def run_mutanti() -> list:
    with ThreadPoolExecutor(max_workers=2) as pool:
        return list(pool.map(_run_mut, NUOVI_MUTANTI_R11))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo-sonde", action="store_true")
    ap.add_argument("--solo-mutanti", action="store_true")
    args = ap.parse_args()
    if not args.solo_mutanti:
        print("=== TASK 1 (SONDE R7 SU 83c8956) ===")
        for k, v in check_r7_probes().items():
            print(k, v)
        print("=== TASK 2 (REPLICA A2+A3 VS ESEGUI_H002) ===")
        t2 = check_task2_replica()
        for r in t2["sviluppo"]:
            print("SVILUPPO:", r)
        print("RIEPILOGO_T2:", {k: v for k, v in t2.items() if k != "sviluppo"})
        print("=== TASK 3 (SECONDO ATTACCO S1..S7) ===")
        for k, v in check_r11_second_attack().items():
            print(k, v)
    if not args.solo_sonde:
        print("=== TASK 3 (NUOVI MUTANTI MR01..MR07) ===")
        for m in run_mutanti():
            print("MUTANTE:", m)


if __name__ == "__main__":
    main()
