"""Mandato R12-bis (Compito A3): terzo attacco al programma dei criteri su origin/feat/esecutore-h002.

Sonde nuove (tutte su dati sintetici in tempdir):
- A3-P1: Scelte/superfici residue (--ora non validata; API K.verifica T=2 senza trade_min; A23 copertura < 10%
         non controllata in screening/verifica; verifica controlla str(cache) e non dati_sha256 / sostituzione
         file sullo stesso percorso cache).
- A3-P2: Esecuzione di codice fuori da FILE_CODICE: moduli brain.* importati ma assenti da FILE_CODICE
         (__init__.py, brain/guardian/g0/valori.py, brain/laboratorio/backtester/portfolio.py), iniezione via
         PYTHONPATH / shadowing stdlib che supera 100% impronte_codice(), e C.carica che non passa codice=.
- A3-P3: Aggiramento feriali_vuoti tramite file .bi5 con 1 solo minuto fittizio alle 00:00 UTC (volume=0,
         fuori sessione Londra): C.carica e CLI accettano dati privi dell'intera sessione ORB.
- A3-P4: Falsi positivi di feriali_vuoti su chiusure reali dell'oro non coperte da C.chiusure_note
         (es. osservanze Capodanno/Natale su lunedì 2 gennaio 2006/2012/2017/2023 o lunedì 26 dicembre 2022).
- A3-P5: Manomissione silenziosa di registro_prove.json (modifica promossa false->true, riduzione N prove,
         cancellazione esecuzione verifica, variante "V-T taroccata" accettata da S.registra_esecuzione).
- A3-P6: Conferma presenza residua del fallback all'indietro DGS-03 in orb_londra.py (uscita su minuto < 16:30).
- A3-P7: Disallineamento tra sigillo.controlla_sigillo(codice=None) in caricatore vs esegui_h002.

Mutanti nuovi (MC01..MC07) in copia isolata di brain/ in tempdir.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import contextlib
from datetime import date, datetime, timedelta, timezone
import io
import json
import lzma
import os
from pathlib import Path
import shutil
import subprocess
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

ORA = "2026-11-16T00:45:00Z"


def _cli(argv):
    out, err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = E.main(argv)
    except SystemExit as exc:
        rc = int(exc.code) if isinstance(exc.code, int) else 2
    return rc, out.getvalue(), err.getvalue()


def _bi5_uno(hour: int = 0, vol: float = 1.0) -> bytes:
    raw = DK.RECORD.pack(hour * 3600, 2000_000, 2000_000, 2000_000, 2000_000, vol)
    return lzma.compress(raw, format=lzma.FORMAT_ALONE)


def _crea_cache_completa(cache_dir: Path, inizio: date, fine: date, b_reali: dict, a_reali: dict,
                         salta_date: set = None) -> None:
    salta_date = salta_date or set()
    SN.scrivi_cache(b_reali, cache_dir / "XAUUSD", inizio=inizio, fine=fine)
    SN.scrivi_cache(a_reali, cache_dir / "XAUUSD_ASK", inizio=inizio, fine=fine)
    pad = _bi5_uno(hour=0, vol=1.0)
    real_dates = {t.date() for t in b_reali}
    g = inizio
    while g <= fine:
        if g in salta_date:
            for sub in ("XAUUSD", "XAUUSD_ASK"):
                (cache_dir / sub / f"{g.isoformat()}.bi5").write_bytes(b"")
        elif g.weekday() < 5 and g not in real_dates:
            for sub in ("XAUUSD", "XAUUSD_ASK"):
                (cache_dir / sub / f"{g.isoformat()}.bi5").write_bytes(pad)
        g += timedelta(days=1)


def sonda_p1_scelte_e_cache_path(base: Path) -> dict:
    # 1. --ora arbitraria non validata; cache sullo stesso path sostituita dopo sviluppo -> verifica usa path uguale ma cache diversa
    d = base / "a3_p1"
    d.mkdir()
    scheda = d / "H-002.md"
    scheda.write_text("# H-002\n", encoding="utf-8")
    reg, cpath, rvf = d / "reg.json", d / "cache_unica", d / "vf.md"
    cod = E.impronte_codice()
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=cod)
    # Popolo cpath prima con un mercato A, registro sviluppo come promosso con cache=str(cpath)
    sv_i, sv_f = E.PERIODO_SVILUPPO
    b_sv, a_sv = SN.mercato(sv_i, 10, seme=1, sd=0.7)
    _crea_cache_completa(cpath, sv_i, sv_f, b_sv, a_sv)
    _, _, info_sv = C.carica(cpath / "XAUUSD", cpath / "XAUUSD_ASK", sv_i, sv_f, "sviluppo", reg, "H-002", scheda)
    S.registra_esecuzione(reg, "H-002", {
        "ruolo": "sviluppo", "variante": "V-T", "promossa": True,
        "cache": str(cpath.resolve()), "dati_sha256": info_sv["dati_sha256"],
    }, "ora-falsa-qualsiasi")

    # Sostituisco il contenuto della directory cpath con dati di verifica (o cambio target di symlink/contenuti)
    shutil.rmtree(cpath)
    vf_i, vf_f = E.PERIODO_VERIFICA
    b_vf, a_vf = SN.mercato(date(2023, 6, 1), 60, seme=4, sd=0.7, spinta=0.02)
    _crea_cache_completa(cpath, vf_i, vf_f, b_vf, a_vf)
    rc_vf, _, err_vf = _cli([
        "--modalita", "verifica", "--varianti", "V-T", "--rapporto", str(rvf),
        "--registro", str(reg), "--scheda", str(scheda), "--cache", str(cpath), "--ora", "STRINGA_NON_ISO",
    ])

    # Check K.verifica T=2 e A23 in criteri
    tr2 = [{"data": date(2023, 1, 2), "lato": "acquisto", "r": 1.0},
           {"data": date(2023, 1, 3), "lato": "acquisto", "r": 1.05}]
    kv2 = K.verifica(tr2, n_prove=2, anni=range(2023, 2024))
    return {
        "ora_arbitraria_e_cache_stesso_path_rc": rc_vf,
        "err": err_vf.strip(),
        "verifica_eseguita": rc_vf == 0,
        "api_k_verifica_2_trade_promossa": kv2["promossa"],
    }


def sonda_p2_codice_fuori_sigillo(base: Path) -> dict:
    # 1. Quali moduli brain.* sono caricati da esegui_h002 ma NON stanno in FILE_CODICE?
    sigillati = {str((REPO_ROOT / f).resolve()) for f in E.FILE_CODICE}
    non_sigillati = sorted({
        Path(m.__file__).resolve().relative_to(REPO_ROOT).as_posix()
        for name, m in sys.modules.items()
        if name.startswith("brain") and getattr(m, "__file__", None)
        and str(Path(m.__file__).resolve()) not in sigillati
    })

    # 2. Dimostrazione in copia temporanea: modifico brain/guardian/g0/valori.py (importato da dsr.py -> FILE_CODICE)
    # o brain/laboratorio/esecuzione/__init__.py -> codice arbitrario eseguito mentre impronte_codice() == sigillo["codice"]!
    d = base / "a3_p2"
    d.mkdir()
    radice = d / "repo"
    shutil.copytree(REPO_ROOT / "brain", radice / "brain",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "cache_dukascopy", "partizioni", "*.csv", "da-gemini"))
    marker = d / "pwned_marker.txt"
    init_non_sigillato = radice / "brain" / "laboratorio" / "esecuzione" / "__init__.py"
    init_orig = init_non_sigillato.read_text(encoding="utf-8") if init_non_sigillato.exists() else ""
    init_non_sigillato.write_text(
        init_orig + f"\nfrom pathlib import Path as _P\n_P({str(marker)!r}).write_text('ESEGUITO_FUORI_FILE_CODICE', encoding='utf-8')\n",
        encoding="utf-8",
    )
    scheda = d / "H-002.md"
    scheda.write_text("# H-002\n", encoding="utf-8")
    reg, cpath, rsv = d / "reg.json", d / "cache", d / "sv.md"
    sv_i, sv_f = E.PERIODO_SVILUPPO
    b_sv, a_sv = SN.mercato(sv_i, 10, seme=1, sd=0.7)
    _crea_cache_completa(cpath, sv_i, sv_f, b_sv, a_sv)
    # Nota: sigilliamo con le impronte ORIGINALI di FILE_CODICE (il sigillo viene accettato!)
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=E.impronte_codice())
    env = dict(os.environ, PYTHONPATH=str(radice))
    proc = subprocess.run(
        [sys.executable, "-s", "-B", "-m", "brain.laboratorio.esecuzione.esegui_h002",
         "--modalita", "sviluppo", "--rapporto", str(rsv), "--registro", str(reg),
         "--scheda", str(scheda), "--cache", str(cpath), "--ora", ORA],
        cwd=str(radice), env=env, capture_output=True, text=True, timeout=120,
    )

    # 3. C.carica non verifica codice= del sigillo
    reg_man = d / "reg_badcode.json"
    S.sigilla(reg_man, "H-002", scheda, ["V-T", "V-S"], ORA, codice={"fake": "0" * 64})
    _, _, info_c = C.carica(cpath / "XAUUSD", cpath / "XAUUSD_ASK", sv_i, sv_f, "sviluppo", reg_man, "H-002", scheda)
    return {
        "moduli_brain_caricati_fuori_FILE_CODICE": non_sigillati,
        "rc_con___init___manomesso": proc.returncode,
        "codice_esterno_eseguito": marker.exists() and marker.read_text(encoding="utf-8") == "ESEGUITO_FUORI_FILE_CODICE",
        "c_carica_ignora_codice_sigillo": info_c["minuti_bid"] > 0,
    }


def sonda_p3_aggira_feriali_vuoti(base: Path) -> dict:
    # Tutti i feriali di PERIODO_SVILUPPO hanno SOLO 1 tick alle 00:00 UTC con vol=0.0 -> fuori ORB -> 0 candele utili,
    # ma info["feriali_vuoti_bid/ask"] == [] e E.main termina con rc == 0!
    d = base / "a3_p3"
    d.mkdir()
    scheda = d / "H-002.md"
    scheda.write_text("# H-002\n", encoding="utf-8")
    reg, cpath, rsv = d / "reg.json", d / "cache_1tick", d / "sv.md"
    sv_i, sv_f = E.PERIODO_SVILUPPO
    _crea_cache_completa(cpath, sv_i, sv_f, {}, {})
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=E.impronte_codice())
    _, _, info = C.carica(cpath / "XAUUSD", cpath / "XAUUSD_ASK", sv_i, sv_f, "sviluppo", reg, "H-002", scheda)
    rc, _, err = _cli(["--modalita", "sviluppo", "--rapporto", str(rsv), "--registro", str(reg),
                       "--scheda", str(scheda), "--cache", str(cpath), "--ora", ORA])
    sv_rec = [e for e in S.leggi(reg)["esecuzioni"] if e["ruolo"] == "sviluppo"]
    return {
        "feriali_vuoti_bid": info["feriali_vuoti_bid"],
        "feriali_vuoti_ask": info["feriali_vuoti_ask"],
        "minuti_bid": info["minuti_bid"],
        "cli_sviluppo_rc": rc,
        "trade_registrati": [e["n"] for e in sv_rec],
        "aggirato_con_0_trade": rc == 0 and all(e["n"] == 0 for e in sv_rec),
        "err": err.strip(),
    }


def sonda_p4_falsi_positivi_chiusure_oro(base: Path) -> dict:
    # Chiusure reali/osservate di Capodanno o Natale su giorni feriali (quando 1/1 o 25/12 cade di sabato/domenica)
    chiusure_osservate_verifica = [
        date(2005, 12, 26),  # lun 26 dic 2005 (25 dic era domenica)
        date(2006, 1, 2),    # lun 2 gen 2006 (1 gen era domenica)
        date(2011, 12, 26),  # lun 26 dic 2011 (25 dic era domenica)
        date(2012, 1, 2),    # lun 2 gen 2012 (1 gen era domenica)
        date(2016, 12, 26),  # lun 26 dic 2016 (25 dic era domenica)
        date(2017, 1, 2),    # lun 2 gen 2017 (1 gen era domenica)
        date(2021, 12, 24),  # ven 24 dic 2021 (25 dic era sabato - chiusura anticipata/osservata US/UK)
        date(2022, 12, 26),  # lun 26 dic 2022 (25 dic era domenica)
        date(2023, 1, 2),    # lun 2 gen 2023 (1 gen era domenica)
    ]
    non_riconosciute = [g.isoformat() for g in chiusure_osservate_verifica if g not in C.chiusure_note(g.year)]

    d = base / "a3_p4"
    d.mkdir()
    scheda = d / "H-002.md"
    scheda.write_text("# H-002\n", encoding="utf-8")
    reg, cpath, rvf = d / "reg.json", d / "cache_holiday", d / "vf.md"
    vf_i, vf_f = E.PERIODO_VERIFICA
    b_vf, a_vf = SN.mercato(date(2023, 6, 1), 60, seme=4, sd=0.7, spinta=0.02)
    # Tutto pieno TRANNE 2023-01-02 (lunedì osservato di Capodanno 2023, file 0 byte come chiusura Dukascopy)
    _crea_cache_completa(cpath, vf_i, vf_f, b_vf, a_vf, salta_date={date(2023, 1, 2)})
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=E.impronte_codice())
    S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": True,
                                         "cache": str(cpath.resolve())}, ORA)
    rc, _, err = _cli(["--modalita", "verifica", "--varianti", "V-T", "--rapporto", str(rvf),
                       "--registro", str(reg), "--scheda", str(scheda), "--cache", str(cpath), "--ora", ORA])
    return {
        "chiusure_osservate_non_in_chiusure_note": non_riconosciute,
        "rc_verifica_con_2023_01_02_vuoto": rc,
        "bloccata_come_feriale_vuoto": rc == 2 and "2023-01-02" in err,
        "err": err.strip(),
    }


def sonda_p5_manomissione_registro(base: Path) -> dict:
    d = base / "a3_p5"
    d.mkdir()
    scheda = d / "H-002.md"
    scheda.write_text("# H-002\n", encoding="utf-8")
    reg, cpath, rsv, rvf = d / "reg.json", d / "cache_tamper", d / "sv.md", d / "vf.md"
    vf_i, vf_f = E.PERIODO_VERIFICA
    b_vf, a_vf = SN.mercato(date(2023, 6, 1), 60, seme=4, sd=0.7, spinta=0.02)
    _crea_cache_completa(cpath, vf_i, vf_f, b_vf, a_vf)
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=E.impronte_codice())
    # Simulo 10 prove (sviluppo) fallite su V-T
    for k in range(10):
        S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": False,
                                             "cache": str(cpath.resolve())}, ORA)
    # 1. Manomissione diretta JSON: riduco prove selezionabili a 1, giro promossa False -> True
    raw = json.loads(reg.read_text(encoding="utf-8"))
    raw["prove"] = [{"ipotesi": "H-002", "variante": "V-T", "ruolo": "selezionabile", "ora": ORA}]
    for e in raw["esecuzioni"]:
        if e.get("ruolo") == "sviluppo":
            e["promossa"] = True
    reg.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    rc_after_tamper, _, err1 = _cli(["--modalita", "verifica", "--varianti", "V-T", "--rapporto", str(rvf),
                                     "--registro", str(reg), "--scheda", str(scheda), "--cache", str(cpath), "--ora", ORA])
    n_prove_taroccato = S.n_prove(S.leggi(reg))

    # 2. Cancello verifica dal JSON e la rieseguo una seconda volta!
    raw2 = json.loads(reg.read_text(encoding="utf-8"))
    raw2["esecuzioni"] = [e for e in raw2["esecuzioni"] if e.get("ruolo") not in ("verifica", "esito")]
    reg.write_text(json.dumps(raw2, indent=2), encoding="utf-8")
    rc_replay, _, err2 = _cli(["--modalita", "verifica", "--varianti", "V-T", "--rapporto", str(d / "vf2.md"),
                               "--registro", str(reg), "--scheda", str(scheda), "--cache", str(cpath), "--ora", ORA])

    # 3. Suffisso libero nella variante registrata da S.registra_esecuzione
    rec_suf = S.registra_esecuzione(reg, "H-002", {"ruolo": "robustezza", "variante": "V-T taroccata_extra"}, ORA)
    return {
        "rc_verifica_su_promossa_manomessa_e_prove_ridotte": rc_after_tamper,
        "err1": err1.strip(),
        "n_prove_letto_dopo_manomissione": n_prove_taroccato,
        "rc_seconda_verifica_dopo_cancellazione": rc_replay,
        "err2": err2.strip(),
        "accetta_variante_con_suffisso": rec_suf["variante"] == "V-T taroccata_extra",
    }


def sonda_p6_dgs03_fallback_indietro() -> dict:
    b, a = SN.mercato(date(2024, 1, 1), 60, seme=3, sd=0.7)
    tr = O.trade(O.prepara(b, a, O.V_S), O.V_S)
    t_ch = [t for t in tr if t["motivo"] != "stop"]
    d0 = t_ch[0]["data"]
    b_cut = {k: v for k, v in b.items() if k.date() != d0 or k.hour < 16}
    a_cut = {k: v for k, v in a.items() if k.date() != d0 or k.hour < 16}
    tr_cut = [t for t in O.trade(O.prepara(b_cut, a_cut, O.V_S), O.V_S) if t["data"] == d0]
    return {
        "giorno_troncato": d0.isoformat(),
        "n_trade": len(tr_cut),
        "prezzo_uscita_trade": tr_cut[0]["uscita"] if tr_cut else None,
        "motivo": tr_cut[0]["motivo"] if tr_cut else None,
        "fallback_indietro_attivo": bool(tr_cut and tr_cut[0]["motivo"] == "fine sessione senza quotazioni"),
    }


def sonda_p7_controlla_sigillo_senza_codice(base: Path) -> dict:
    d = base / "a3_p7"
    d.mkdir()
    scheda = d / "H-002.md"
    scheda.write_text("# H-002\n", encoding="utf-8")
    reg = d / "reg.json"
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice={"solo_chiave": "abc"})
    s_no_code = S.controlla_sigillo(reg, "H-002", scheda)
    try:
        S.controlla_sigillo(reg, "H-002", scheda, codice=E.impronte_codice())
        con_codice_bloccato = False
    except (S.NonSigillata, ValueError):
        con_codice_bloccato = True
    return {"passa_senza_codice": bool(s_no_code), "blocca_con_codice": con_codice_bloccato}


NUOVI_MUTANTI_A3 = [
    (
        "MC01",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        "        sigillo = S.controlla_sigillo(x.registro, IPOTESI, x.scheda, codice=impronte_codice())   # §10 e codice",
        "        sigillo = S.controlla_sigillo(x.registro, IPOTESI, x.scheda)   # §10 senza codice",
        "omette verifica impronte codice nel CLI esegui_h002",
    ),
    (
        "MC02",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        "            if cache_sviluppo != {str(cache)}:                                    # R11-S6: stessi dati",
        "            if False and cache_sviluppo != {str(cache)}:                          # disattiva R11-S6",
        "disattiva il vincolo che sviluppo e verifica usino la stessa cache",
    ),
    (
        "MC03",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        "                or not info[\"minuti_ask\"] or info[\"feriali_vuoti_bid\"] or info[\"feriali_vuoti_ask\"]:  # P6, R11-S2",
        "                or not info[\"minuti_ask\"] or info[\"feriali_vuoti_bid\"]:  # ignora feriali_vuoti_ask",
        "omette feriali_vuoti_ask nel controllo dati incompleti",
    ),
    (
        "MC04",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        "        if x.rapporto.is_dir():                                                # R11-S4: prima di registrare",
        "        if False and x.rapporto.is_dir():                                      # disattiva R11-S4",
        "disattiva controllo --rapporto directory prima della registrazione",
    ),
    (
        "MC05",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        "FILE_CODICE = (\"brain/laboratorio/simulatori/orb_londra.py\", \"brain/laboratorio/esecuzione/criteri.py\",",
        "FILE_CODICE = (\"brain/laboratorio/simulatori/orb_londra.py\",",
        "rimuove criteri.py dalla lista FILE_CODICE sigillata",
    ),
    (
        "MC06",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        "        if sorted(sigillo[\"varianti\"]) != sorted(VARIANTI):                    # N giusto (P3 di Gemini)",
        "        if not sigillo[\"varianti\"]:                                            # accetta N qualsiasi >= 1",
        "disattiva controllo numero esatto di varianti sigillate (P3)",
    ),
    (
        "MC07",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        "            da_verificare = [v for v in VARIANTI if esiti_sviluppo.get(v)\n"
        "                             and all(bool(e.get(\"promossa\")) for e in esiti_sviluppo[v])]          # P1",
        "            da_verificare = [v for v in VARIANTI if esiti_sviluppo.get(v)\n"
        "                             and any(bool(e.get(\"promossa\")) for e in esiti_sviluppo[v])]          # P1 all->any",
        "cambia all(...) in any(...) sugli esiti di sviluppo ammessi in verifica",
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


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo-sonde", action="store_true")
    ap.add_argument("--solo-mutanti", action="store_true")
    args = ap.parse_args()
    if not args.solo_mutanti:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            print("A3-P1:", sonda_p1_scelte_e_cache_path(base))
            print("A3-P2:", sonda_p2_codice_fuori_sigillo(base))
            print("A3-P3:", sonda_p3_aggira_feriali_vuoti(base))
            print("A3-P4:", sonda_p4_falsi_positivi_chiusure_oro(base))
            print("A3-P5:", sonda_p5_manomissione_registro(base))
            print("A3-P6:", sonda_p6_dgs03_fallback_indietro())
            print("A3-P7:", sonda_p7_controlla_sigillo_senza_codice(base))
    if not args.solo_sonde:
        print("=== A3 MUTANTI (MC01..MC07) ===")
        with ThreadPoolExecutor(max_workers=2) as pool:
            for m in pool.map(_run_mut, NUOVI_MUTANTI_A3):
                print("MUTANTE:", m)


if __name__ == "__main__":
    main()
