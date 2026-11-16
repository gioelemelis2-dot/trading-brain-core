"""Mandato R12-bis (Compiti A1 e A2) su origin/feat/esecutore-h002 (ccdac1f).

- A1: Riesegue tutte le sonde R7 (P1..P7) e R11 (S1..S7), dichiarando ogni
  adeguamento reso necessario dai cambi di interfaccia (rimozione di --inizio,
  --fine, --ripetizioni, --seme da CLI; sigillo.codice obbligatorio; verifica
  vincolata alla stessa cache dello sviluppo; periodi fissi PERIODO_SVILUPPO e
  PERIODO_VERIFICA).
- A2: Riesegue replica_criteri_h002 vs esegui_h002 sui 3 mercati sintetici e
  sulla verifica, stampando esplicitamente le coperture sui criteri 4 e 5
  (A23 >= 90%) e confermando differenza 0.
"""
from __future__ import annotations

import contextlib
from datetime import date, datetime, time, timedelta, timezone
import io
import lzma
from pathlib import Path
import random
import shutil
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from brain.dati.pipeline import dukascopy as DK  # noqa: E402
from brain.laboratorio.esecuzione import caricatore as C  # noqa: E402
from brain.laboratorio.esecuzione import criteri as K  # noqa: E402
from brain.laboratorio.esecuzione import esegui_h002 as E  # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S  # noqa: E402
from brain.laboratorio.esecuzione import sintetico as SN  # noqa: E402
from brain.laboratorio.simulatori import orb_londra as O  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import replica_criteri_h002 as R  # noqa: E402

ORA = "2026-11-16T00:30:00Z"


def _cli(argv):
    out, err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = E.main(argv)
    except SystemExit as exc:
        rc = int(exc.code) if isinstance(exc.code, int) else 2
    return rc, out.getvalue(), err.getvalue()


def _bi5_singolo_minuto() -> bytes:
    """Un record valido alle 00:00 UTC (fuori sessione Londra 07:30-17:00 -> 0 trade)."""
    raw = DK.RECORD.pack(0, 2000_000, 2000_000, 2000_000, 2000_000, 1.0)
    return lzma.compress(raw, format=lzma.FORMAT_ALONE)


def _scrivi_cache_veloce(cache_dir: Path, inizio: date, fine: date, dati_bid: dict, dati_ask: dict,
                         riempi_altri_feriali: bool = True) -> None:
    """Scrive una cache Dukascopy sintetica completa su [inizio, fine] in tempi rapidi."""
    SN.scrivi_cache(dati_bid, cache_dir / "XAUUSD", inizio=inizio, fine=fine)
    SN.scrivi_cache(dati_ask, cache_dir / "XAUUSD_ASK", inizio=inizio, fine=fine)
    if not riempi_altri_feriali:
        return
    pad = _bi5_singolo_minuto()
    giorni_con_dati = {t.date() for t in dati_bid}
    g = inizio
    while g <= fine:
        if g.weekday() < 5 and g not in giorni_con_dati:
            for sub in ("XAUUSD", "XAUUSD_ASK"):
                p = cache_dir / sub / f"{g.isoformat()}.bi5"
                if p.stat().st_size == 0:
                    p.write_bytes(pad)
        g += timedelta(days=1)


def _prepara_ambiente_base(radice: Path):
    scheda = radice / "H-002.md"
    scheda.write_text("# H-002 test\n", encoding="utf-8")
    # Cache sviluppo: mercato casuale su PERIODO_SVILUPPO (bocciato nello screening)
    c_sv_no = radice / "cache_sv_casuale"
    sv_i, sv_f = E.PERIODO_SVILUPPO
    b_sv, a_sv = SN.mercato(sv_i, (sv_f - sv_i).days + 1, seme=3, sd=0.7)
    SN.scrivi_cache(b_sv, c_sv_no / "XAUUSD", inizio=sv_i, fine=sv_f)
    SN.scrivi_cache(a_sv, c_sv_no / "XAUUSD_ASK", inizio=sv_i, fine=sv_f)

    # Cache verifica completa (2005-01-01..FINE_VERIFICA): 2023 con trade positivi, 2005..2022 feriali a 1 minuto 00:00 UTC
    c_vf = radice / "cache_vf"
    vf_i, vf_f = E.PERIODO_VERIFICA
    b_vf, a_vf = SN.mercato(date(2023, 1, 2), (vf_f - date(2023, 1, 2)).days + 1, seme=4, sd=0.7, spinta=0.03)
    _scrivi_cache_veloce(c_vf, vf_i, vf_f, b_vf, a_vf, riempi_altri_feriali=True)
    return scheda, c_sv_no, c_vf


def check_r7(base: Path, scheda: Path, c_sv_no: Path, c_vf: Path) -> dict:
    cod = E.impronte_codice()
    ris = {}

    # P1: verifica su variante bocciata -> bloccata (adeguamento: tolto --inizio/--fine/--ripetizioni; sigilla con codice=cod)
    d = base / "p1"
    d.mkdir()
    reg, rsv, rvf = d / "reg.json", d / "sv.md", d / "vf.md"
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=cod)
    rc_sv, _, err_sv = _cli(["--modalita", "sviluppo", "--rapporto", str(rsv), "--registro", str(reg),
                             "--scheda", str(scheda), "--cache", str(c_sv_no), "--ora", ORA])
    rc_vf, _, err_vf = _cli(["--modalita", "verifica", "--varianti", "V-T", "--rapporto", str(rvf),
                             "--registro", str(reg), "--scheda", str(scheda), "--cache", str(c_sv_no), "--ora", ORA])
    ris["P1"] = {"rc_sv": rc_sv, "err_sv": err_sv.strip(), "rc_vf": rc_vf, "bloccata": rc_vf == 2, "err_vf": err_vf.strip()}

    # P2: chiamata verifica separata (--varianti V-T quando entrambe promosse) -> bloccata
    d = base / "p2"
    d.mkdir()
    reg, rvf = d / "reg.json", d / "vf.md"
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=cod)
    S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": True,
                                         "cache": str(c_vf.resolve())}, ORA)
    S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-S", "promossa": True,
                                         "cache": str(c_vf.resolve())}, ORA)
    rc_p2, _, err_p2 = _cli(["--modalita", "verifica", "--varianti", "V-T", "--rapporto", str(rvf),
                             "--registro", str(reg), "--scheda", str(scheda), "--cache", str(c_vf), "--ora", ORA])
    ris["P2"] = {"rc": rc_p2, "bloccata": rc_p2 == 2, "err": err_p2.strip()}

    # P3: sigillo con N=1 variante -> bloccato
    d = base / "p3"
    d.mkdir()
    reg, rsv = d / "reg.json", d / "sv.md"
    S.sigilla(reg, "H-002", scheda, ["V-T"], ORA, codice=cod)
    rc_p3, _, err_p3 = _cli(["--modalita", "sviluppo", "--rapporto", str(rsv), "--registro", str(reg),
                             "--scheda", str(scheda), "--cache", str(c_sv_no), "--ora", ORA])
    ris["P3"] = {"rc": rc_p3, "bloccata": rc_p3 == 2, "err": err_p3.strip()}

    # P4: cache vuota/inesistente in verifica non brucia la verifica
    d = base / "p4"
    d.mkdir()
    reg, c_vuota, rvf = d / "reg.json", d / "inesistente", d / "vf.md"
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=cod)
    S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": True,
                                         "cache": str(c_vuota.resolve())}, ORA)
    S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-S", "promossa": False,
                                         "cache": str(c_vuota.resolve())}, ORA)
    rc_p4, _, err_p4 = _cli(["--modalita", "verifica", "--varianti", "V-T", "--rapporto", str(rvf),
                             "--registro", str(reg), "--scheda", str(scheda), "--cache", str(c_vuota), "--ora", ORA])
    vf_rec = [e for e in S.leggi(reg)["esecuzioni"] if e["ruolo"] == "verifica"]
    ris["P4"] = {"rc": rc_p4, "verifica_registrata": len(vf_rec), "bloccata": rc_p4 == 2 and len(vf_rec) == 0,
                 "err": err_p4.strip()}

    # P5: verifica CLI conta TUTTI gli anni solari del periodo [2005..2023], inclusi quelli a 0 trade (2005..2022)
    d = base / "p5"
    d.mkdir()
    reg, rvf = d / "reg.json", d / "vf.md"
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=cod)
    S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": True,
                                         "cache": str(c_vf.resolve())}, ORA)
    S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-S", "promossa": False,
                                         "cache": str(c_vf.resolve())}, ORA)
    rc_p5, _, err_p5 = _cli(["--modalita", "verifica", "--varianti", "V-T", "--rapporto", str(rvf),
                             "--registro", str(reg), "--scheda", str(scheda), "--cache", str(c_vf), "--ora", ORA])
    esito_rec = [e for e in S.leggi(reg)["esecuzioni"] if e["ruolo"] == "esito"]
    ris["P5"] = {
        "rc": rc_p5, "err": err_p5.strip(),
        "quota_anni": round(esito_rec[0]["quota_anni"], 6) if esito_rec else None,
        "attesa_1_su_19": round(1 / 19, 6),
        "bloccata": bool(esito_rec and abs(esito_rec[0]["quota_anni"] - 1 / 19) < 1e-4),
    }

    # P6: confronto casuale usa stessi giorni S∩C∩V
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
    ris["P6"] = {"r_strategia_casuale": v_out["casuale"]["r_strategia"], "sopra": v_out["casuale"]["sopra"],
                 "copertura": round(v_out["casuale"]["copertura"], 4),
                 "bloccata": abs(v_out["casuale"]["r_strategia"] - 0.02) < 1e-12 and not v_out["casuale"]["sopra"]}

    # P7: embargo 2023-11-01..2023-11-14 rifiutato in verifica
    d = base / "p7"
    d.mkdir()
    reg, ce = d / "reg.json", d / "cache_emb"
    b, a = SN.mercato(date(2023, 11, 1), 20, seme=9, sd=0.7)
    SN.scrivi_cache(b, ce / "XAUUSD")
    SN.scrivi_cache(a, ce / "XAUUSD_ASK")
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=cod)
    try:
        C.carica(ce / "XAUUSD", ce / "XAUUSD_ASK", date(2023, 11, 1), date(2023, 11, 14),
                 "verifica", reg, "H-002", scheda)
        ris["P7"] = {"bloccata": False}
    except ValueError as exc:
        ris["P7"] = {"bloccata": True, "err": str(exc)}
    return ris


def check_r11(base: Path, scheda: Path, c_sv_no: Path, c_vf: Path) -> dict:
    cod = E.impronte_codice()
    ris = {}

    # S1: --inizio / --fine rifiutati da argparse; verifica cosa fa ancora K.verifica a livello API su T=2
    rc_arg, _, err_arg = _cli(["--modalita", "verifica", "--varianti", "V-T", "--inizio", "2022-08-01",
                               "--fine", "2023-10-31", "--rapporto", str(base / "x.md")])
    tr2 = [{"data": date(2023, 9, 5), "lato": "acquisto", "r": 1.0},
           {"data": date(2023, 10, 10), "lato": "acquisto", "r": 1.05}]
    kv2 = K.verifica(tr2, n_prove=2, anni=range(2023, 2024))
    ris["S1"] = {"cli_rifiuta_inizio_fine": rc_arg == 2, "cli_err": err_arg.strip().splitlines()[-1] if err_arg else "",
                 "api_k_verifica_2_trade_promossa": kv2["promossa"]}

    # S2: feriali con .bi5 da 0 byte bloccati in verifica senza bruciare verifica
    d = base / "s2"
    d.mkdir()
    reg, ce, rvf = d / "reg.json", d / "cache_0byte", d / "vf.md"
    b, a = SN.mercato(date(2023, 9, 1), 60, seme=2, sd=0.7, spinta=0.03)
    _scrivi_cache_veloce(ce, E.PERIODO_VERIFICA[0], E.PERIODO_VERIFICA[1], b, a, riempi_altri_feriali=False)
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=cod)
    S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": True,
                                         "cache": str(ce.resolve())}, ORA)
    rc_s2, _, err_s2 = _cli(["--modalita", "verifica", "--varianti", "V-T", "--rapporto", str(rvf),
                             "--registro", str(reg), "--scheda", str(scheda), "--cache", str(ce), "--ora", ORA])
    vf_rec = [e for e in S.leggi(reg)["esecuzioni"] if e["ruolo"] == "verifica"]
    ris["S2"] = {"rc": rc_s2, "verifica_bruciata": len(vf_rec) > 0, "bloccata": rc_s2 == 2 and len(vf_rec) == 0,
                 "err": err_s2.strip()}

    # S3: --ripetizioni / --seme rifiutati da CLI e valori fissi registrati in sviluppo
    rc_r1, _, _ = _cli(["--modalita", "sviluppo", "--ripetizioni", "1", "--rapporto", str(base / "y.md")])
    d = base / "s3"
    d.mkdir()
    reg, rsv = d / "reg.json", d / "sv.md"
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=cod)
    rc_s3, _, _ = _cli(["--modalita", "sviluppo", "--rapporto", str(rsv), "--registro", str(reg),
                        "--scheda", str(scheda), "--cache", str(c_sv_no), "--ora", ORA])
    sv_rec = [e for e in S.leggi(reg)["esecuzioni"] if e["ruolo"] == "sviluppo"][0]
    ris["S3"] = {"cli_rifiuta_ripetizioni": rc_r1 == 2, "rc_sviluppo": rc_s3,
                 "ripetizioni_salvate": sv_rec.get("ripetizioni"), "seme_salvato": sv_rec.get("seme"),
                 "bloccata": rc_r1 == 2 and sv_rec.get("ripetizioni") == 1000 and sv_rec.get("seme") == 20261115}

    # S4: --rapporto dir non brucia verifica; rapporto valido registra esito + rapporto_sha256
    d = base / "s4"
    d.mkdir()
    reg, rdir, rvf = d / "reg.json", d / "dir_rap", d / "vf.md"
    rdir.mkdir()
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=cod)
    S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": True,
                                         "cache": str(c_vf.resolve())}, ORA)
    rc_dir, _, err_dir = _cli(["--modalita", "verifica", "--varianti", "V-T", "--rapporto", str(rdir),
                               "--registro", str(reg), "--scheda", str(scheda), "--cache", str(c_vf), "--ora", ORA])
    vf_dopo_dir = [e for e in S.leggi(reg)["esecuzioni"] if e["ruolo"] == "verifica"]
    rc_ok, _, _ = _cli(["--modalita", "verifica", "--varianti", "V-T", "--rapporto", str(rvf),
                        "--registro", str(reg), "--scheda", str(scheda), "--cache", str(c_vf), "--ora", ORA])
    esiti = [e for e in S.leggi(reg)["esecuzioni"] if e["ruolo"] == "esito"]
    ris["S4"] = {"rc_dir": rc_dir, "bruciata_dopo_dir": len(vf_dopo_dir) > 0, "rc_ok": rc_ok,
                 "esito_salvato": bool(esiti),
                 "chiavi_esito": sorted(esiti[0].keys()) if esiti else [],
                 "bloccata": rc_dir == 2 and len(vf_dopo_dir) == 0 and bool(esiti and "rapporto_sha256" in esiti[0])}

    # S5: copertura casuale < 10% (A23) in valuta_variante -> vediamo se bloccata ora!
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
            return [{"data": x, "lato": lato_fisso, "r": -0.10} for x in dlist[:20]]
        @staticmethod
        def metriche(tr): return O.metriche(tr)
    res_cov = E.valuta_variante(_SimCov(), E._Giorni(_SimCov(), {}, {}), O.V_T,
                                {"rob": {"target_r": 1.2}}, 0.0, 200, 7)
    ris["S5"] = {"copertura": round(res_cov["casuale"]["copertura"], 6),
                 "promossa_con_copertura_5_7pct": res_cov["screening"]["promossa"],
                 "bloccata": not res_cov["screening"]["promossa"]}

    # S6: cache A sviluppo vs cache B verifica -> bloccata! Inoltre esegui_verifica ora richiede anni obbligatorio
    bv, av = SN.mercato(date(2010, 1, 1), 800, seme=4, sd=0.7, spinta=0.01)
    try:
        E.esegui_verifica(bv, av, ["V-T"], n_prove=2)
        anni_obbligatorio = False
    except TypeError:
        anni_obbligatorio = True
    res_api = E.esegui_verifica(bv, av, ["V-T"], n_prove=2, anni=range(2008, 2013))
    q_api = [c["valore"] for c in res_api["varianti"]["V-T"]["verifica"]["criteri"]
             if c["nome"].startswith("quota")][0]
    d = base / "s6"
    d.mkdir()
    reg, rvf = d / "reg.json", d / "vf.md"
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=cod)
    S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": True,
                                         "cache": str(c_sv_no.resolve())}, ORA)
    rc_s6, _, err_s6 = _cli(["--modalita", "verifica", "--varianti", "V-T", "--rapporto", str(rvf),
                             "--registro", str(reg), "--scheda", str(scheda), "--cache", str(c_vf), "--ora", ORA])
    ris["S6"] = {"rc_cache_diversa": rc_s6, "bloccata": rc_s6 == 2 and anni_obbligatorio,
                 "anni_obbligatorio": anni_obbligatorio,
                 "err": err_s6.strip(),
                 "api_esegui_verifica_quota_con_anni": round(q_api, 4)}

    # S7: sigillo.registra_esecuzione con variante inventata -> ora bloccata?
    d = base / "s7"
    d.mkdir()
    reg = d / "reg.json"
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=cod)
    try:
        S.registra_esecuzione(reg, "H-002", {"ruolo": "verifica", "variante": "INVENTATA"}, ORA)
        s7_bloccata = False
        s7_err = ""
    except ValueError as exc:
        s7_bloccata = True
        s7_err = str(exc)
    ris["S7"] = {"bloccata": s7_bloccata, "err": s7_err}
    return ris


def check_replica_a2() -> dict:
    mercati = [
        ("casuale", SN.mercato(date(2024, 1, 1), 800, seme=3, sd=0.7)),
        ("vantaggio_spinta", SN.mercato(date(2024, 1, 1), 800, seme=3, sd=0.7, spinta=0.01)),
        ("sola_tendenza_deriva", SN.mercato(date(2024, 1, 1), 800, seme=3, sd=0.7, deriva=0.01)),
    ]
    righe = []
    max_diff_det = 0.0
    max_diff_p95 = 0.0
    min_cov_c4 = 1.0
    min_cov_c5 = 1.0
    for nome_m, (bid, ask) in mercati:
        c_sv = E.esegui_sviluppo(bid, ask)
        for v, par in (("V-T", O.V_T), ("V-S", O.V_S)):
            g_res = R.valuta_variante_sviluppo(bid, ask, v, par)
            cx = c_sv["varianti"][v]
            cm = cx["metriche"]
            cov_c4 = cx["casuale"]["copertura"]
            cov_c5 = cx["benchmark"]["n_comuni"] / cm["n"]
            min_cov_c4 = min(min_cov_c4, cov_c4, g_res["casuale"]["copertura"])
            min_cov_c5 = min(min_cov_c5, cov_c5, g_res["bench_acquisto"]["n_comuni"] / g_res["n"],
                             g_res["bench_vendita"]["n_comuni"] / g_res["n"])
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
            righe.append({
                "mercato": nome_m, "variante": v, "n": g_res["n"],
                "cov_c4": round(cov_c4, 6), "cov_c5": round(cov_c5, 6),
                "max_diff_det": d_det, "p95_diff": round(d_p95, 6), "promossa": g_res["promossa"],
            })

    bv, av = SN.mercato(date(2010, 1, 1), 800, seme=4, sd=0.7, spinta=0.01)
    anni = range(2008, 2014)
    c_vf = E.esegui_verifica(bv, av, ["V-T", "V-S"], n_prove=2, anni=anni)
    tr_vt = O.trade(O.prepara(bv, av, O.V_T), O.V_T)
    tr_vs = O.trade(O.prepara(bv, av, O.V_S), O.V_S)
    g_vt = R.valuta_variante_verifica(tr_vt, 2, anni, sharpe_altre=[O.metriche(tr_vs)["sharpe"]])
    g_vs = R.valuta_variante_verifica(tr_vs, 2, anni, sharpe_altre=[O.metriche(tr_vt)["sharpe"]])
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
    return {
        "righe": righe,
        "min_cov_c4": round(min_cov_c4, 6),
        "min_cov_c5": round(min_cov_c5, 6),
        "max_diff_det_sviluppo": max_diff_det,
        "max_diff_p95": round(max_diff_p95, 6),
        "diff_verifica": diff_vf,
    }


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        scheda, c_sv_no, c_vf = _prepara_ambiente_base(base)
        print("=== A1: SONDE R7 (P1..P7) ===")
        for k, v in check_r7(base, scheda, c_sv_no, c_vf).items():
            print(k, v)
        print("=== A1: SONDE R11 (S1..S7) ===")
        for k, v in check_r11(base, scheda, c_sv_no, c_vf).items():
            print(k, v)
    print("=== A2: REPLICA CRITERI (A23, C4/C5 >= 90%, DIFF 0) ===")
    rep = check_replica_a2()
    for r in rep["righe"]:
        print("SVILUPPO:", r)
    print("RIEPILOGO_A2:", {k: v for k, v in rep.items() if k != "righe"})


if __name__ == "__main__":
    main()
