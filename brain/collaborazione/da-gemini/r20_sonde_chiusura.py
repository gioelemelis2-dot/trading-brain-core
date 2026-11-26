"""Sonde indipendenti di chiusura per i rilievi aperti di R19 (#143–#149) e serie #124 (D1–D6).

Mandato 27/11/2026 (D-56, DGS-20):
- Una sonda per ciascun rilievo aperto: #143 (R19-02), #144 (R19-03), #145 (R19-04),
  #146a–e (R19-06), #147a–b (R19-07), #148 (R19-08, separata dall'orario invalido), #149 (R19-09).
- Almeno una sonda del percorso valido per ciascun rilievo (V-143..V-149), che deve restare riuscita
  dopo le correzioni.
- Serie completa delle sonde #124 (D1, D2, D3, D4, D5, D6a, D6b), incluse D4 e D5 assenti in R19.

Ogni sonda opera esclusivamente su copie temporanee e dati sintetici (nessun dato reale, rete bloccata),
legge lo stato effettivo (codice d'uscita / eccezione, esito tecnico, eventi della riserva, voci del
registro delle prove, chiamate al caricatore, file creati) e stampa su stdout una riga JSON pura:
  {"sonda", "rilievo", "atteso_dopo_la_correzione", "osservato", "difetto_presente"}
Nessuna scritta fissa interpretativa dentro i campi osservati; nessun percorso utente (D-28).
"""
import csv
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time as _time
from datetime import date, datetime, time, timedelta, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest import mock

RADICE_VERA = Path(__file__).resolve().parents[3]
if str(RADICE_VERA) not in sys.path:
    sys.path.insert(0, str(RADICE_VERA))

from brain.dati.pipeline import calendario as CAL                   # noqa: E402
from brain.dati.pipeline import dukascopy as DK                     # noqa: E402
from brain.laboratorio.esecuzione import caricatore as C            # noqa: E402
from brain.laboratorio.esecuzione import esegui_h002 as EH          # noqa: E402
from brain.laboratorio.esecuzione import esegui_verifica as EV      # noqa: E402
from brain.laboratorio.esecuzione import manifesto as MF            # noqa: E402
from brain.laboratorio.esecuzione import riserva as RV              # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S               # noqa: E402
from brain.laboratorio.simulatori import orb_londra as O            # noqa: E402
from brain.laboratorio.studi import pilota_ia02 as P                # noqa: E402
from brain.laboratorio.tests import mercato_sintetico as M          # noqa: E402
from brain.laboratorio.tests import test_esegui_verifica as TEV     # noqa: E402
from brain.laboratorio.verdetto import verdetto_d31 as V            # noqa: E402

ORA = "2026-11-22T12:00:00Z"
LETTURA = TEV.LETTURA
ACCESSORIE = TEV.ACCESSORIE
INIZIO = TEV.INIZIO
FINE = TEV.FINE
B_INIZIO = TEV.B_INIZIO
B_FINE = TEV.B_FINE
SVILUPPO = TEV.SVILUPPO

AMBIENTE_SENZA_RETE = dict(
    os.environ,
    HTTPS_PROXY="http://127.0.0.1:9",
    HTTP_PROXY="http://127.0.0.1:9",
    https_proxy="http://127.0.0.1:9",
    http_proxy="http://127.0.0.1:9",
    NO_PROXY="",
    no_proxy="",
)


def _pulisci_testo(valore: Any, sostituzioni: List[tuple]) -> Any:
    if isinstance(valore, str):
        out = valore
        for vecchio, nuovo in sostituzioni:
            if vecchio:
                out = out.replace(vecchio, nuovo)
        casa = str(Path.home())
        if casa:
            out = out.replace(casa, "~")
        return out
    if isinstance(valore, list):
        return [_pulisci_testo(x, sostituzioni) for x in valore]
    if isinstance(valore, dict):
        return {k: _pulisci_testo(v, sostituzioni) for k, v in valore.items()}
    return valore


def emetti(sonda: str, rilievo: str, atteso: str, osservato: dict, difetto_presente: bool,
           radici_tmp: Optional[List[Path]] = None) -> dict:
    sost = [(str(RADICE_VERA.resolve()), "<repo>"), (str(RADICE_VERA), "<repo>")]
    for p in (radici_tmp or []):
        sost.append((str(Path(p).resolve()), "<tmp>"))
        sost.append((str(p), "<tmp>"))
    riga = {
        "sonda": sonda,
        "rilievo": rilievo,
        "atteso_dopo_la_correzione": atteso,
        "osservato": _pulisci_testo(osservato, sost),
        "difetto_presente": bool(difetto_presente),
    }
    print(json.dumps(riga, ensure_ascii=False), flush=True)
    return riga


def _completa_feriali_non_chiusi(cache: Path, inizio: date, fine: date, simbolo: str = "XAUUSD") -> None:
    """Riempie con sedute neutre complete i feriali in O.esclusi ma fuori da calendario.chiusure_note,
    così la cache sintetica valida ha feriali_vuoti=[] e feriali_incompleti=[] anche per il caricatore."""
    da_riempire = set()
    g = inizio
    while g <= fine:
        if g.weekday() < 5 and g not in CAL.chiusure_note(g.year):
            f_bid = cache / simbolo / f"{g.isoformat()}.bi5"
            if f_bid.exists() and f_bid.stat().st_size == 0:
                da_riempire.add(g)
        g += timedelta(days=1)
    if not da_riempire:
        return
    nuovi_sha: Dict[tuple, tuple] = {}
    for g in sorted(da_riempire):
        minuti = M._minuti(g, None)
        for lato, cartella, spread in (("BID", simbolo, 0), ("ASK", f"{simbolo}_ASK", M.SPREAD)):
            corpo = M._bi5(minuti, spread)
            (cache / cartella / f"{g.isoformat()}.bi5").write_bytes(corpo)
            nuovi_sha[(lato, g.isoformat())] = (len(corpo), hashlib.sha256(corpo).hexdigest())
    for lato in ("BID", "ASK"):
        reg = cache / f"registro_scaricamento_{simbolo}_{lato}.csv"
        with open(reg, newline="", encoding="utf-8") as fh:
            righe = list(csv.DictReader(fh))
        for r in righe:
            chiave = (lato, r["giorno"])
            if chiave in nuovi_sha:
                n_byte, digest = nuovi_sha[chiave]
                r["esito"] = "dati"
                r["byte"] = str(n_byte)
                r["sha256"] = digest
        with open(reg, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=M.CAMPI)
            w.writeheader()
            w.writerows(righe)


def stato_registri(registro: Path, riserva: Path) -> dict:
    voci_prove = []
    if registro.exists():
        dati_p = S.leggi(registro)
        voci_prove = [
            {"ipotesi": e.get("ipotesi"), "ruolo": e.get("ruolo"),
             "variante": e.get("variante"), "esito": e.get("esito")}
            for e in dati_p.get("esecuzioni", [])
        ]
    stato_r = None
    eventi_r = []
    if riserva.exists():
        raw_r = json.loads(riserva.read_text(encoding="utf-8"))
        eventi_r = [e.get("tipo") for e in raw_r.get("eventi", [])]
        st = RV.stato(riserva)
        stato_r = {
            "giorni_consumati": st["giorni"]["consumato"],
            "giorni_prenotati": st["giorni"]["prenotato"],
            "aperture": [(a["id"], a["j"], a["alfa_j"], a["esito"]) for a in st["aperture"]],
            "rifiuti": [(r["id"], r["j_previsto"], r["fase"]) for r in st["rifiuti"]],
            "eventi_tipi": eventi_r,
        }
    return {"voci_registro_prove": voci_prove, "riserva": stato_r}


def esegui_isolato(scheda: Path, registro: Path, riserva: Path, id_: str, cache: Path, cache_sv: Path,
                   rapporto: Path, ora: str = ORA, patch_extra: Optional[list] = None) -> dict:
    chiamate = {"sviluppo": 0, "verifica": 0}
    vero_carica = C.carica

    def conta_carica(*a, **k):
        chiamate[a[4]] += 1
        return vero_carica(*a, **k)

    contesto_patch = [
        mock.patch.object(EV, "ANCORA_GIT", False),
        mock.patch.object(EV, "CONTROLLO_AMBIENTE", False),
        mock.patch.object(C, "carica", side_effect=conta_carica),
    ] + list(patch_extra or [])

    eccezione = None
    risultato = None
    attivi = []
    try:
        for p in contesto_patch:
            attivi.append(p)
            p.start()
        try:
            risultato = EV.esegui(scheda, registro, riserva, id_, cache, cache_sv, rapporto, ora)
        except Exception as e:
            eccezione = f"{type(e).__name__}: {e}"
    finally:
        for p in reversed(attivi):
            p.stop()

    orfani = sorted(x.name for x in rapporto.parent.iterdir() if x.name.startswith(f".{rapporto.name}.")) \
        if rapporto.parent.exists() else []
    st = stato_registri(registro, riserva)
    return {
        "eccezione": eccezione,
        "esito_tecnico": risultato["esito_tecnico"] if risultato else None,
        "esito": risultato["esito"] if risultato else None,
        "chiamate_caricatore": dict(chiamate),
        "voci_registro_prove": st["voci_registro_prove"],
        "riserva": st["riserva"],
        "file_creati": {
            "rapporto_file_regolare": rapporto.is_file() and not rapporto.is_symlink(),
            "rapporto_cartella": rapporto.is_dir(),
            "file_temporanei_orfani": orfani,
        },
    }


def prepara_repo_git(base: Path, ipotesi: str = "H-T127", id_: str = "P1", alfa_tot: float = 0.05,
                     inizio: date = LETTURA, fine: date = FINE, **campi_contratto):
    remoto = base / "remoto.git"
    repo = base / "repo"
    shutil.copytree(RADICE_VERA / "brain", repo / "brain", ignore=shutil.ignore_patterns("__pycache__"))
    for p in ((repo / EV.REL_REGISTRO_PROVE), (repo / EV.REL_RISERVA)):
        if p.exists():
            p.unlink()
    g = ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@invalid"]
    subprocess.run(["git", "init", "-q", "--bare", str(remoto)], check=True)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(g + ["checkout", "-q", "-b", "principale"], check=True)
    subprocess.run(g + ["remote", "add", "origin", str(remoto)], check=True)

    reg = repo / EV.REL_REGISTRO_PROVE
    ris = repo / EV.REL_RISERVA
    scheda = repo / "brain" / "laboratorio" / "ipotesi" / f"{ipotesi}.md"
    scheda.parent.mkdir(parents=True, exist_ok=True)
    scheda.write_text(TEV.testo_scheda(TEV.contratto(ipotesi, **campi_contratto)), encoding="utf-8")
    S.sigilla(reg, ipotesi, scheda, ["V-T"], ORA, codice=EV.impronte_codice(repo))
    RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), alfa_tot, ORA)
    RV.prenota(ris, id_, ipotesi, inizio, fine, S.impronta(scheda), ORA)
    subprocess.run(g + ["add", "-A"], check=True)
    subprocess.run(g + ["commit", "-q", "-m", "stato iniziale"], check=True)
    subprocess.run(g + ["push", "-q", "-u", "origin", "principale"], check=True, capture_output=True)
    return repo, reg, ris, scheda, g


def lancia_avvio_verifica(repo: Path, argomenti: List[str], env_extra: Optional[dict] = None) -> subprocess.CompletedProcess:
    env = dict(AMBIENTE_SENZA_RETE, **(env_extra or {}))
    return subprocess.run(
        [sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py", "verifica", *argomenti],
        cwd=str(repo), env=env, capture_output=True, text=True, timeout=180,
    )


# ==============================================================================================================
# PARTE 1 — SONDE SUI RILIEVI APERTI (#143–#149)
# ==============================================================================================================

def sonda_143(cache: Path, cache_sv: Path) -> dict:
    """#143 (R19-02): doppio --scheda con esca H-002, sigillo privo di esegui_verifica.py, e forma --scheda=PATH."""
    with tempfile.TemporaryDirectory(prefix="r20_143_") as td:
        base = Path(td)
        repo, reg, ris, scheda_vera, g = prepara_repo_git(base, ipotesi="H-T143", id_="P1")
        esca = repo / "brain" / "laboratorio" / "ipotesi" / "esca_H002.md"
        esca.write_text(TEV.testo_scheda(TEV.contratto("H-002")), encoding="utf-8")
        # Aggiunge un sigillo H-002 legittimo (che non contiene esegui_verifica.py)
        S.sigilla(reg, "H-002", esca, ["V-T"], ORA, codice=EH.impronte_codice(repo))
        # Aggiunge anche un sigillo H-INC privo di esegui_verifica.py ma con un solo --scheda
        scheda_inc = repo / "brain" / "laboratorio" / "ipotesi" / "H-INC143.md"
        scheda_inc.write_text(TEV.testo_scheda(TEV.contratto("H-INC143")), encoding="utf-8")
        codice_senza_ev = {k: v for k, v in EV.impronte_codice(repo).items()
                           if k != "brain/laboratorio/esecuzione/esegui_verifica.py"}
        S.sigilla(reg, "H-INC143", scheda_inc, ["V-T"], ORA, codice=codice_senza_ev)
        subprocess.run(g + ["add", "-A"], check=True)
        subprocess.run(g + ["commit", "-q", "-m", "sigilli esca e incompleto"], check=True)
        subprocess.run(g + ["push", "-q"], check=True, capture_output=True)

        # (c) Forma --scheda=PATH su codice integro
        rap_eq = base / "rap_eq.txt"
        r_eq = lancia_avvio_verifica(repo, [
            f"--scheda={scheda_vera}", "--registro", EV.REL_REGISTRO_PROVE, "--riserva", EV.REL_RISERVA,
            "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
            "--rapporto", str(rap_eq), "--ora", ORA,
        ])
        falso_manca_scheda = "manca --scheda" in r_eq.stderr

        # Ripristina eventuali scritture se --scheda=PATH avesse completato la verifica
        subprocess.run(g + ["checkout", "--", EV.REL_REGISTRO_PROVE, EV.REL_RISERVA], check=True)

        # Manomette esegui_verifica.py sul disco per verificare se avvio.py lo importa
        ev_file = repo / "brain" / "laboratorio" / "esecuzione" / "esegui_verifica.py"
        orig_ev = ev_file.read_text(encoding="utf-8")
        spia_doppio = base / "spia_doppio"
        spia_inc = base / "spia_incompleto"
        try:
            ev_file.write_text(f"open({str(spia_doppio)!r}, 'w').write('1')\n" + orig_ev, encoding="utf-8")
            r_dop = lancia_avvio_verifica(repo, [
                "--scheda", str(esca), "--scheda", str(scheda_vera),
                "--registro", EV.REL_REGISTRO_PROVE, "--riserva", EV.REL_RISERVA,
                "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
                "--rapporto", str(base / "rap_dop.txt"), "--ora", ORA,
            ])

            ev_file.write_text(f"open({str(spia_inc)!r}, 'w').write('1')\n" + orig_ev, encoding="utf-8")
            r_inc = lancia_avvio_verifica(repo, [
                "--scheda", str(scheda_inc),
                "--registro", EV.REL_REGISTRO_PROVE, "--riserva", EV.REL_RISERVA,
                "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
                "--rapporto", str(base / "rap_inc.txt"), "--ora", ORA,
            ])
        finally:
            ev_file.write_text(orig_ev, encoding="utf-8")

        st = stato_registri(reg, ris)
        oss = {
            "doppio_scheda": {
                "rc": r_dop.returncode,
                "codice_manomesso_importato": spia_doppio.exists(),
                "stderr_inizio": r_dop.stderr.strip()[:160],
            },
            "sigillo_senza_esegui_verifica": {
                "rc": r_inc.returncode,
                "codice_manomesso_importato": spia_inc.exists(),
                "stderr_inizio": r_inc.stderr.strip()[:160],
            },
            "forma_scheda_uguale": {
                "rc": r_eq.returncode,
                "stderr_contiene_manca_scheda": falso_manca_scheda,
                "stderr_inizio": r_eq.stderr.strip()[:160],
            },
            "registri_dopo_tentativi_manomessi": st,
        }
        difetto = (
            spia_doppio.exists()
            or spia_inc.exists()
            or r_dop.returncode != 2
            or r_inc.returncode != 2
            or falso_manca_scheda
        )
        return emetti(
            "S-143", "#143 (R19-02)",
            "FERMO prima degli import (rc=2, nessun import di esegui_verifica manomesso) sia con doppio --scheda sia "
            "con sigillo privo di esegui_verifica.py; --scheda=PATH gestito senza falso errore 'manca --scheda'",
            oss, difetto, [base],
        )


def sonda_144(cache: Path, cache_sv: Path) -> dict:
    """#144 (R19-03): 20 feriali vuoti (vuoto-200) e 5 feriali incompleti coerenti col CSV non devono dare 'promossa'."""
    with tempfile.TemporaryDirectory(prefix="r20_144_") as td:
        base = Path(td)
        sedute_finestra = EV.sedute(INIZIO, FINE)

        # Sottocaso A: 20 feriali vuoti coerenti col registro CSV
        c_vuoti = base / "cache_vuoti"
        shutil.copytree(cache, c_vuoti)
        bersagli_vuoti = {g.isoformat() for g in sedute_finestra[:20]}
        sha_vuoto = hashlib.sha256(b"").hexdigest()
        for lato, sub in (("BID", "XAUUSD"), ("ASK", "XAUUSD_ASK")):
            for g_iso in bersagli_vuoti:
                (c_vuoti / sub / f"{g_iso}.bi5").write_bytes(b"")
            reg_csv = c_vuoti / f"registro_scaricamento_XAUUSD_{lato}.csv"
            with open(reg_csv, newline="", encoding="utf-8") as fh:
                righe = list(csv.DictReader(fh))
            for r in righe:
                if r["giorno"] in bersagli_vuoti:
                    r["esito"] = "vuoto-200"
                    r["byte"] = "0"
                    r["sha256"] = sha_vuoto
            with open(reg_csv, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=M.CAMPI)
                w.writeheader()
                w.writerows(righe)

        reg_a, ris_a = base / "reg_a.json", base / "ris_a.json"
        RV.crea(ris_a, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        s_a = base / "H-144A.md"
        s_a.write_text(TEV.testo_scheda(TEV.contratto("H-144A")), encoding="utf-8")
        S.sigilla(reg_a, "H-144A", s_a, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris_a, "P1", "H-144A", LETTURA, FINE, S.impronta(s_a), ORA)
        es_a = esegui_isolato(s_a, reg_a, ris_a, "P1", c_vuoti, cache_sv, base / "rap_a.txt")
        rec_a = RV.prenotazione(ris_a, "P1").get("record")
        zeri_su_vuoti = sum(1 for c in (rec_a.get("coppie") or []) if c[0] in bersagli_vuoti and c[1] == 0 and c[2] == 0) \
            if rec_a else 0

        # Sottocaso B: 5 feriali incompleti (1 solo minuto alle 08:00 Londra) coerenti col registro CSV
        c_inc = base / "cache_inc"
        shutil.copytree(cache, c_inc)
        bersagli_inc = {g.isoformat() for g in sedute_finestra[:5]}
        for lato, sub, spread in (("BID", "XAUUSD", 0), ("ASK", "XAUUSD_ASK", M.SPREAD)):
            agg_sha = {}
            for g in sedute_finestra[:5]:
                un_minuto = M._minuti(g, True)[:1]
                corpo = M._bi5(un_minuto, spread)
                (c_inc / sub / f"{g.isoformat()}.bi5").write_bytes(corpo)
                agg_sha[g.isoformat()] = (len(corpo), hashlib.sha256(corpo).hexdigest())
            reg_csv = c_inc / f"registro_scaricamento_XAUUSD_{lato}.csv"
            with open(reg_csv, newline="", encoding="utf-8") as fh:
                righe = list(csv.DictReader(fh))
            for r in righe:
                if r["giorno"] in agg_sha:
                    nb, dg = agg_sha[r["giorno"]]
                    r["esito"] = "dati"
                    r["byte"] = str(nb)
                    r["sha256"] = dg
            with open(reg_csv, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=M.CAMPI)
                w.writeheader()
                w.writerows(righe)

        reg_b, ris_b = base / "reg_b.json", base / "ris_b.json"
        RV.crea(ris_b, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        s_b = base / "H-144B.md"
        s_b.write_text(TEV.testo_scheda(TEV.contratto("H-144B")), encoding="utf-8")
        S.sigilla(reg_b, "H-144B", s_b, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris_b, "P1", "H-144B", LETTURA, FINE, S.impronta(s_b), ORA)
        es_b = esegui_isolato(s_b, reg_b, ris_b, "P1", c_inc, cache_sv, base / "rap_b.txt")
        rec_b = RV.prenotazione(ris_b, "P1").get("record")
        zeri_su_inc = sum(1 for c in (rec_b.get("coppie") or []) if c[0] in bersagli_inc and c[1] == 0 and c[2] == 0) \
            if rec_b else 0

        def caso_accettabile(es, zeri):
            if es["eccezione"] is not None:
                return es["riserva"]["giorni_consumati"] == 0 and es["esito"] is None
            return es["esito"] == "non decidibile" and zeri == 0

        difetto = not (caso_accettabile(es_a, zeri_su_vuoti) and caso_accettabile(es_b, zeri_su_inc))
        oss = {
            "feriali_vuoti_20": dict(
                es_a,
                trade_verdetto=(rec_a.get("verdetto") or {}).get("trade") if rec_a else None,
                coppie_zero_sui_giorni_vuoti=zeri_su_vuoti,
            ),
            "feriali_incompleti_5": dict(
                es_b,
                trade_verdetto=(rec_b.get("verdetto") or {}).get("trade") if rec_b else None,
                coppie_zero_sui_giorni_incompleti=zeri_su_inc,
            ),
        }
        return emetti(
            "S-144", "#144 (R19-03)",
            "Feriali vuoti o incompleti della finestra non diventano sedute con K=0 né producono 'promossa': "
            "rifiuto prima dell'autorizzazione senza consumo oppure esito 'non decidibile'",
            oss, difetto, [base],
        )


def sonda_145(cache: Path, cache_sv: Path) -> dict:
    """#145 (R19-04): seconda verifica della stessa ipotesi/variante su ramo divergente con stesso j."""
    def prova_ramo_divergente(base_sub: Path, alfa_tot: float, m_val: int) -> dict:
        try:
            repo, reg, ris, scheda, g = prepara_repo_git(
                base_sub, ipotesi="H-R145", id_="P1", alfa_tot=alfa_tot, m=m_val,
            )
        except Exception as e:
            return {"eccezione_setup": f"{type(e).__name__}: {e}", "eccezione_esegui": "bloccato_alla_creazione",
                    "chiamate_caricatore": {"sviluppo": 0, "verifica": 0}, "eventi_aggiunti_su_ramo_b": 0}

        scheda_alt = repo / "brain" / "laboratorio" / "ipotesi" / "H-ALT145.md"
        scheda_alt.write_text(TEV.testo_scheda(TEV.contratto("H-ALT145", m=m_val)), encoding="utf-8")
        S.sigilla(reg, "H-ALT145", scheda_alt, ["V-T"], ORA, codice=EV.impronte_codice(repo))
        RV.prenota(ris, "P_ALT", "H-ALT145", B_INIZIO, B_FINE, S.impronta(scheda_alt), ORA)
        subprocess.run(g + ["add", "-A"], check=True)
        subprocess.run(g + ["commit", "-q", "-m", "due ipotesi"], check=True)
        subprocess.run(g + ["push", "-q", "origin", "principale"], check=True, capture_output=True)
        base_sha = subprocess.run(g + ["rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

        # Su principale: verifica H-R145 V-T registrata (j=1)
        RV.autorizza(ris, "P1", 2, "a" * 64, ORA, m=m_val)
        S.registra_esecuzioni(reg, "H-R145", [{"ruolo": "verifica", "variante": "V-T", "prenotazione": "P1"}], ORA)
        subprocess.run(g + ["add", "-A"], check=True)
        subprocess.run(g + ["commit", "-q", "-m", "H-R145 verificata su principale"], check=True)
        subprocess.run(g + ["push", "-q", "origin", "principale"], check=True, capture_output=True)

        # Su ramo_b divergente: autorizza H-ALT145 (j=1 == principale), rilascia P1, prenota P2 per H-R145 V-T
        subprocess.run(g + ["checkout", "-q", "-b", "ramo_b", base_sha], check=True)
        RV.autorizza(ris, "P_ALT", 2, "b" * 64, ORA, m=m_val)
        RV.rilascia(ris, "P1", ORA, "revisore", "test ramo divergente")
        RV.prenota(ris, "P2", "H-R145", LETTURA, FINE, S.impronta(scheda), ORA)
        subprocess.run(g + ["add", "-A"], check=True)
        subprocess.run(g + ["commit", "-q", "-m", "ramo_b j=1 e P2 su H-R145"], check=True)
        subprocess.run(g + ["push", "-q", "-u", "origin", "ramo_b"], check=True, capture_output=True)

        eventi_prima = len(json.loads(ris.read_text(encoding="utf-8"))["eventi"])
        chiamate = {"sviluppo": 0, "verifica": 0}
        vero_c = C.carica
        eccezione = None
        ris_esegui = None
        with mock.patch.object(EV, "RADICE", repo), mock.patch.object(EV, "ANCORA_GIT", True), \
                mock.patch.object(EV, "CONTROLLO_AMBIENTE", False), \
                mock.patch.object(C, "carica", side_effect=lambda *a, **k: (chiamate.__setitem__(a[4], chiamate[a[4]] + 1), vero_c(*a, **k))[1]):
            try:
                ris_esegui = EV.esegui(scheda, reg, ris, "P2", cache, cache_sv, base_sub / "rap.txt", ORA)
            except Exception as e:
                eccezione = f"{type(e).__name__}: {e}"
        eventi_dopo = len(json.loads(ris.read_text(encoding="utf-8"))["eventi"])
        st = stato_registri(reg, ris)
        return {
            "eccezione_esegui": eccezione,
            "esito_tecnico": ris_esegui["esito_tecnico"] if ris_esegui else None,
            "esito": ris_esegui["esito"] if ris_esegui else None,
            "chiamate_caricatore": chiamate,
            "eventi_aggiunti_su_ramo_b": eventi_dopo - eventi_prima,
            "registri_ramo_b": st,
        }

    with tempfile.TemporaryDirectory(prefix="r20_145_") as td:
        base = Path(td)
        (base / "alfa075").mkdir()
        (base / "alfa005").mkdir()
        c_075 = prova_ramo_divergente(base / "alfa075", 0.75, 5)
        c_005 = prova_ramo_divergente(base / "alfa005", 0.05, 1)
        difetto = (
            c_075["eccezione_esegui"] is None
            or c_005["eccezione_esegui"] is None
            or c_075["chiamate_caricatore"] != {"sviluppo": 0, "verifica": 0}
            or c_005["chiamate_caricatore"] != {"sviluppo": 0, "verifica": 0}
            or c_005["eventi_aggiunti_su_ramo_b"] > 0
        )
        return emetti(
            "S-145", "#145 (R19-04)",
            "Rifiuto con ValueError prima del controllo quota e prima di ogni lettura/scrittura sia con alfa alterato "
            "(0.75, m=5) sia con alfa D-38 (0.05, m=1) quando l'ipotesi/variante risulta già verificata nella storia git",
            {"ramo_divergente_alfa_075_m_5": c_075, "ramo_divergente_alfa_005_m_1": c_005},
            difetto, [base],
        )


def _minuti_doppio_confine_ora_legale(g: date, vinta_londra: bool, vinta_utc: bool) -> List[tuple]:
    """Seduta sintetica con candele 07:00–16:45 UTC per misurare l'effetto dell'ora legale (DGS-20):
    - d'estate (BST = UTC+1), Europe/London apre alle 07:00 UTC e chiude l'unica operazione alle 07:46 UTC
      con esito `vinta_londra`; un fuso privo di ora legale (UTC) ignora 07:00–07:59 UTC, apre alle 08:00 UTC
      ed esegue sull'onda delle 08:30–08:46 UTC con esito `vinta_utc`;
    - d'inverno (GMT = UTC+0), entrambi leggono 08:00 UTC con esito `vinta_londra`."""
    mezzanotte = datetime(g.year, g.month, g.day, tzinfo=timezone.utc)
    inizio_londra_utc = datetime.combine(g, time(8, 0), tzinfo=O.LONDRA).astimezone(timezone.utc)
    estate = (inizio_londra_utc.hour == 7)
    out = []
    t = datetime(g.year, g.month, g.day, 7, 0, tzinfo=timezone.utc)
    fine = datetime(g.year, g.month, g.day, 16, 45, tzinfo=timezone.utc)
    while t < fine:
        sec = int((t - mezzanotte).total_seconds())
        hm = (t.hour, t.minute)
        if estate:
            if hm < (7, 30):
                o = c = M.P
                lo, hi = M.P - 2_500, M.P + 2_500
            elif hm < (7, 46):
                o = c = M.P + 3_000
                lo, hi = o - 100, o + 100
            elif hm < (8, 0):
                o = c = M.P + 13_000 if vinta_londra else M.P - 3_000
                lo, hi = o - 100, o + 100
            elif hm < (8, 30):
                o = c = M.P
                lo, hi = M.P - 2_500, M.P + 2_500
            elif hm < (8, 46):
                o = c = M.P + 3_000
                lo, hi = o - 100, o + 100
            else:
                o = c = M.P + 13_000 if vinta_utc else M.P - 3_000
                lo, hi = o - 100, o + 100
        else:
            if hm < (8, 0):
                o = c = M.P
                lo, hi = M.P - 100, M.P + 100
            elif hm < (8, 30):
                o = c = M.P
                lo, hi = M.P - 2_500, M.P + 2_500
            elif hm < (8, 46):
                o = c = M.P + 3_000
                lo, hi = o - 100, o + 100
            else:
                o = c = M.P + 13_000 if vinta_londra else M.P - 3_000
                lo, hi = o - 100, o + 100
        out.append((sec, o, c, lo, hi, 1.0))
        t += timedelta(minutes=1)
    return out


def _scrivi_cache_doppio_confine(dest: Path, inizio: date, fine: date, p_londra: float, p_utc_estate: float,
                                 seme: int, simbolo: str = "XAUUSD") -> None:
    rnd = __import__("random").Random(seme)
    righe = {"BID": [], "ASK": []}
    for _lato, cartella in (("BID", simbolo), ("ASK", f"{simbolo}_ASK")):
        (dest / cartella).mkdir(parents=True, exist_ok=True)
    g = inizio
    while g <= fine:
        if g.weekday() < 5 and g not in CAL.chiusure_note(g.year):
            if g in O.esclusi(g.year):
                minuti = M._minuti(g, None)
            else:
                vl = rnd.random() < p_londra
                vu = rnd.random() < p_utc_estate
                minuti = _minuti_doppio_confine_ora_legale(g, vl, vu)
        else:
            minuti = None
        for lato, cartella, spread in (("BID", simbolo, 0), ("ASK", f"{simbolo}_ASK", M.SPREAD)):
            corpo = M._bi5(minuti, spread) if minuti else b""
            (dest / cartella / f"{g.isoformat()}.bi5").write_bytes(corpo)
            righe[lato].append({
                "ora_utc": "2026-11-22T00:00:00Z", "giorno": g.isoformat(), "lato": lato,
                "url": DK.url_giorno(simbolo, g, lato), "http": 200,
                "esito": "dati" if corpo else "vuoto-200", "byte": len(corpo),
                "sha256": hashlib.sha256(corpo).hexdigest(), "tentativi": 1,
            })
        g += timedelta(days=1)
    for lato, rr in righe.items():
        reg = dest / f"registro_scaricamento_{simbolo}_{lato}.csv"
        with open(reg, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=M.CAMPI)
            w.writeheader()
            w.writerows(rr)


def sonda_146a(cache: Path, cache_sv: Path) -> dict:
    """#146a (R19-06a, DGS-20): stesso caso sintetico con fusi diversi (Europe/London vs UTC senza ora legale estiva,
    più TZ d'ambiente), confrontando finestra, sedute, impronta dell'impegno, trade ed esito."""
    with tempfile.TemporaryDirectory(prefix="r20_146a_") as td:
        base = Path(td)
        c_ver_fuso = base / "cache_ver_fuso"
        c_sv_fuso = base / "cache_sv_fuso"
        # Sviluppo: positivo sia a 07:00 UTC sia a 08:00 UTC (supera lo screening in entrambi i fusi).
        # Verifica: positivo all'apertura vera di Londra (07:00 UTC d'estate -> promossa), negativo a 08:00 UTC d'estate (-> bocciata).
        _scrivi_cache_doppio_confine(c_sv_fuso, *SVILUPPO, p_londra=0.65, p_utc_estate=0.65, seme=31)
        _scrivi_cache_doppio_confine(c_ver_fuso, LETTURA, FINE, p_londra=0.65, p_utc_estate=0.10, seme=32)

        def corsa_con_fuso(etichetta: str, fuso_patch=None, tz_env: Optional[str] = None) -> dict:
            sub = base / etichetta
            sub.mkdir()
            reg, ris = sub / "reg.json", sub / "ris.json"
            RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
            scheda = sub / "H-146A.md"
            scheda.write_text(TEV.testo_scheda(TEV.contratto("H-146A")), encoding="utf-8")
            S.sigilla(reg, "H-146A", scheda, ["V-T"], ORA, codice=EV.impronte_codice())
            RV.prenota(ris, "P1", "H-146A", LETTURA, FINE, S.impronta(scheda), ORA)
            extra = [mock.patch.object(O, "LONDRA", fuso_patch)] if fuso_patch is not None else []
            vecchio_tz = os.environ.get("TZ")
            try:
                if tz_env is not None:
                    os.environ["TZ"] = tz_env
                    if hasattr(_time, "tzset"):
                        _time.tzset()
                es = esegui_isolato(scheda, reg, ris, "P1", c_ver_fuso, c_sv_fuso, sub / "rap.txt", patch_extra=extra)
            finally:
                if tz_env is not None:
                    if vecchio_tz is None:
                        os.environ.pop("TZ", None)
                    else:
                        os.environ["TZ"] = vecchio_tz
                    if hasattr(_time, "tzset"):
                        _time.tzset()
            p_st = RV.prenotazione(ris, "P1")
            rec = p_st.get("record")
            aut = p_st.get("autorizzazione")
            imp = aut.get("impegno") if aut else None
            return {
                "eccezione": es["eccezione"],
                "esito_tecnico": es["esito_tecnico"],
                "esito": es["esito"],
                "chiamate_caricatore": es["chiamate_caricatore"],
                "giorni_consumati": es["riserva"]["giorni_consumati"],
                "finestra": imp["finestra"] if imp else None,
                "sedute_count": len(imp["sedute"]) if imp else None,
                "impronta_impegno": aut["hash_dati"] if aut else None,
                "trade_verdetto": (rec.get("verdetto") or {}).get("trade") if rec else None,
                "media_verdetto": (rec.get("verdetto") or {}).get("media") if rec else None,
                "sedute_attive": (rec.get("verdetto") or {}).get("sedute_attive") if rec else None,
            }

        rif_londra = corsa_con_fuso("londra")
        fuso_utc = corsa_con_fuso("tzdata_utc", fuso_patch=timezone.utc)
        env_ny = corsa_con_fuso("env_ny", tz_env="America/New_York")

        fermato_prima = (
            fuso_utc["eccezione"] is not None
            and fuso_utc["giorni_consumati"] == 0
            and fuso_utc["chiamate_caricatore"] == {"sviluppo": 0, "verifica": 0}
        )
        difetto = not fermato_prima
        oss = {
            "riferimento_europe_london": rif_londra,
            "tzdata_londra_alterato_utc": fuso_utc,
            "env_tz_america_new_york": env_ny,
            "confronto_londra_vs_utc": {
                "stessa_finestra": rif_londra["finestra"] == fuso_utc["finestra"],
                "stesse_sedute": rif_londra["sedute_count"] == fuso_utc["sedute_count"],
                "stessa_impronta_impegno": (
                    rif_londra["impronta_impegno"] is not None
                    and rif_londra["impronta_impegno"] == fuso_utc["impronta_impegno"]
                ),
                "stessi_trade": rif_londra["trade_verdetto"] == fuso_utc["trade_verdetto"],
                "stesso_esito": rif_londra["esito"] == fuso_utc["esito"],
            },
        }
        return emetti(
            "S-146a", "#146a (R19-06a)",
            "Con dati del fuso di Londra alterati (senza regola europea dell'ora legale), fermo con ValueError "
            "prima dell'autorizzazione e della lettura (0 giorni consumati, 0 chiamate al caricatore)",
            oss, difetto, [base],
        )


def sonda_146b(cache: Path, cache_sv: Path) -> dict:
    """#146b (R19-06b): ambiente ricontrollato prima della scrittura dell'esito e alla ripresa (comportamento osservato)."""
    with tempfile.TemporaryDirectory(prefix="r20_146b_") as td:
        base = Path(td)
        estraneo = base / "modulo_estraneo.py"
        estraneo.write_text("X = 1\n", encoding="utf-8")

        # Sottocaso 1: modulo estraneo caricato durante la lettura di verifica (dopo il 1° controllo ambiente)
        sub1 = base / "pre_esito"
        repo1, reg1, ris1, scheda1, _ = prepara_repo_git(sub1, ipotesi="H-146B1", id_="P1")
        rap1 = sub1 / "rap1.txt"
        prog_pre_esito = "\n".join([
            "import json, sys, types",
            "from pathlib import Path",
            "from unittest import mock",
            f"sys.path.insert(0, {str(repo1)!r})",
            "sys._tb_avvio_controllato = True",
            "from brain.laboratorio.esecuzione import caricatore as C, esegui_verifica as EV",
            "vero_c = C.carica",
            "def carica_e_inquina(*a, **k):",
            "    out = vero_c(*a, **k)",
            "    if a[4] == 'verifica':",
            "        m = types.ModuleType('_estraneo_146b')",
            f"        m.__file__ = {str(estraneo)!r}",
            "        sys.modules['_estraneo_146b'] = m",
            "    return out",
            "with mock.patch.object(EV, 'ANCORA_GIT', False), mock.patch.object(EV, 'CONTROLLO_AMBIENTE', True), \\",
            "        mock.patch.object(C, 'carica', side_effect=carica_e_inquina):",
            "    try:",
            f"        r = EV.esegui(Path({str(scheda1)!r}), Path({str(reg1)!r}), Path({str(ris1)!r}), 'P1', "
            f"Path({str(cache)!r}), Path({str(cache_sv)!r}), Path({str(rap1)!r}), {ORA!r})",
            "        print(json.dumps({'ok': True, 'risultato': r}))",
            "    except Exception as e:",
            "        print(json.dumps({'ok': False, 'eccezione': f'{type(e).__name__}: {e}'}))",
        ])
        r1 = subprocess.run([sys.executable, "-I", "-S", "-B", "-c", prog_pre_esito],
                            cwd=str(repo1), env=AMBIENTE_SENZA_RETE, capture_output=True, text=True, timeout=180)
        es1 = json.loads(r1.stdout.strip()) if r1.stdout.strip() else {"ok": False, "stderr": r1.stderr.strip()[:200]}
        st1 = stato_registri(reg1, ris1)
        ruoli1 = [v["ruolo"] for v in st1["voci_registro_prove"]]
        esito_scritto_con_ambiente_sporco = ("esito" in ruoli1) or any(
            a[3] is not None for a in (st1["riserva"]["aperture"] if st1["riserva"] else [])
        )

        # Sottocaso 2: modulo estraneo presente in sys.modules alla ripresa (record già presente)
        sub2 = base / "ripresa"
        repo2, reg2, ris2, scheda2, _ = prepara_repo_git(sub2, ipotesi="H-146B2", id_="P1")
        rap2_iniz = sub2 / "rap2_iniz.txt"
        esegui_isolato(scheda2, reg2, ris2, "P1", cache, cache_sv, rap2_iniz)
        rap2_rip = sub2 / "rap2_ripresa.txt"
        prog_ripresa = "\n".join([
            "import json, sys, types",
            "from pathlib import Path",
            "from unittest import mock",
            f"sys.path.insert(0, {str(repo2)!r})",
            "sys._tb_avvio_controllato = True",
            "from brain.laboratorio.esecuzione import esegui_verifica as EV",
            "m = types.ModuleType('_estraneo_ripresa_146b')",
            f"m.__file__ = {str(estraneo)!r}",
            "sys.modules['_estraneo_ripresa_146b'] = m",
            "with mock.patch.object(EV, 'ANCORA_GIT', False), mock.patch.object(EV, 'CONTROLLO_AMBIENTE', True):",
            "    try:",
            f"        r = EV.esegui(Path({str(scheda2)!r}), Path({str(reg2)!r}), Path({str(ris2)!r}), 'P1', "
            f"Path({str(cache)!r}), Path({str(cache_sv)!r}), Path({str(rap2_rip)!r}), {ORA!r})",
            "        print(json.dumps({'ok': True, 'risultato': r}))",
            "    except Exception as e:",
            "        print(json.dumps({'ok': False, 'eccezione': f'{type(e).__name__}: {e}'}))",
        ])
        r2 = subprocess.run([sys.executable, "-I", "-S", "-B", "-c", prog_ripresa],
                            cwd=str(repo2), env=AMBIENTE_SENZA_RETE, capture_output=True, text=True, timeout=180)
        es2 = json.loads(r2.stdout.strip()) if r2.stdout.strip() else {"ok": False, "stderr": r2.stderr.strip()[:200]}
        ripresa_sporca_riuscita = bool(es2.get("ok")) or rap2_rip.exists()

        difetto = esito_scritto_con_ambiente_sporco or ripresa_sporca_riuscita
        oss = {
            "inquinamento_prima_dell_esito": {
                "risposta": es1,
                "esito_scritto_nei_registri": esito_scritto_con_ambiente_sporco,
                "registri": st1,
                "rapporto_creato": rap1.exists(),
            },
            "ambiente_sporco_alla_ripresa": {
                "risposta": es2,
                "rapporto_rigenerato_creato": rap2_rip.exists(),
            },
        }
        return emetti(
            "S-146b", "#146b (R19-06b)",
            "Fermo con ValueError sia quando un modulo estraneo viene caricato prima della scrittura dell'esito "
            "(nessun esito scritto), sia quando l'ambiente è sporco alla ripresa (nessun rapporto rigenerato)",
            oss, difetto, [base],
        )


def sonda_146c(cache: Path, cache_sv: Path) -> dict:
    """#146c (R19-06c): --ora invalida rifiutata prima dell'autorizzazione e della lettura (con --rapporto valido)."""
    with tempfile.TemporaryDirectory(prefix="r20_146c_") as td:
        base = Path(td)
        reg, ris = base / "reg.json", base / "ris.json"
        RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        scheda = base / "H-146C.md"
        scheda.write_text(TEV.testo_scheda(TEV.contratto("H-146C")), encoding="utf-8")
        S.sigilla(reg, "H-146C", scheda, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris, "P1", "H-146C", LETTURA, FINE, S.impronta(scheda), ORA)

        es = esegui_isolato(scheda, reg, ris, "P1", cache, cache_sv, base / "rapporto_valido.txt", ora="NON-UNA-DATA")
        difetto = (
            es["eccezione"] is None
            or es["riserva"]["giorni_consumati"] > 0
            or len(es["voci_registro_prove"]) > 0
            or es["chiamate_caricatore"] != {"sviluppo": 0, "verifica": 0}
        )
        return emetti(
            "S-146c", "#146c (R19-06c)",
            "Orario --ora non ISO-8601 UTC valido rifiutato con ValueError prima dell'autorizzazione e della lettura "
            "(0 giorni consumati, 0 chiamate al caricatore, 0 voci scritte nel registro delle prove)",
            es, difetto, [base],
        )


def sonda_146d(cache: Path, cache_sv: Path) -> dict:
    """#146d (R19-06d): veto_blocchi.soglia non finita (-Infinity, +Infinity, NaN) rifiutata al passo 1."""
    with tempfile.TemporaryDirectory(prefix="r20_146d_") as td:
        base = Path(td)
        esiti_contratto = {}
        for nome, val in (("meno_inf", float("-inf")), ("piu_inf", float("inf")), ("nan", float("nan"))):
            c = TEV.contratto("H-146D")
            c["veto_blocchi"] = dict(c["veto_blocchi"], soglia=val)
            f_s = base / f"scheda_{nome}.md"
            f_s.write_text(f"# H-146D\n\n```json contratto-h003\n{json.dumps(c)}\n```\n", encoding="utf-8")
            try:
                EV.leggi_contratto(f_s)
                esiti_contratto[nome] = {"accettata_da_leggi_contratto": True, "eccezione": None}
            except Exception as e:
                esiti_contratto[nome] = {"accettata_da_leggi_contratto": False, "eccezione": f"{type(e).__name__}: {e}"}

        # Corsa completa su -Infinity per misurare letture e scritture nei registri
        scheda_inf = base / "scheda_meno_inf.md"
        reg, ris = base / "reg.json", base / "ris.json"
        RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        S.sigilla(reg, "H-146D", scheda_inf, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris, "P1", "H-146D", LETTURA, FINE, S.impronta(scheda_inf), ORA)
        es_esegui = esegui_isolato(scheda_inf, reg, ris, "P1", cache, cache_sv, base / "rap.txt")

        difetto = (
            any(v["accettata_da_leggi_contratto"] for v in esiti_contratto.values())
            or es_esegui["chiamate_caricatore"] != {"sviluppo": 0, "verifica": 0}
            or len(es_esegui["voci_registro_prove"]) > 0
            or es_esegui["riserva"]["giorni_consumati"] > 0
        )
        return emetti(
            "S-146d", "#146d (R19-06d)",
            "Soglia del veto per blocchi non finita (-Inf, +Inf, NaN) rifiutata al passo 1 da leggi_contratto "
            "(SchedaNonConforme), con 0 chiamate al caricatore e 0 voci scritte nei registri",
            {"leggi_contratto": esiti_contratto, "esegui_meno_inf": es_esegui}, difetto, [base],
        )


def sonda_146e() -> dict:
    """#146e (R19-06e): ipotesi vuota o di soli spazi rifiutata al passo 1 da leggi_contratto."""
    with tempfile.TemporaryDirectory(prefix="r20_146e_") as td:
        base = Path(td)
        risultati = {}
        for nome, val in (("vuota", ""), ("spazi", "   ")):
            f_s = base / f"scheda_{nome}.md"
            f_s.write_text(TEV.testo_scheda(TEV.contratto(val)), encoding="utf-8")
            try:
                EV.leggi_contratto(f_s)
                risultati[nome] = {"accettata_da_leggi_contratto": True, "eccezione": None}
            except Exception as e:
                risultati[nome] = {"accettata_da_leggi_contratto": False, "eccezione": f"{type(e).__name__}: {e}"}
        difetto = any(v["accettata_da_leggi_contratto"] for v in risultati.values())
        return emetti(
            "S-146e", "#146e (R19-06e)",
            "Contratto H-003 con campo 'ipotesi' vuoto o di soli spazi rifiutato al passo 1 (SchedaNonConforme)",
            risultati, difetto, [base],
        )


def sonda_147a(cache: Path, cache_sv: Path) -> dict:
    """#147a (R19-07a, DGS-20): il manifesto controlla dominio e data dell'URL (separato dalla destinazione rapporto)."""
    with tempfile.TemporaryDirectory(prefix="r20_147a_") as td:
        base = Path(td)

        def prova_url(etichetta: str, url_falso: str) -> dict:
            sub = base / etichetta
            c_mod = sub / "cache"
            shutil.copytree(cache, c_mod)
            reg_csv = c_mod / "registro_scaricamento_XAUUSD_BID.csv"
            with open(reg_csv, newline="", encoding="utf-8") as fh:
                righe = list(csv.DictReader(fh))
            for r in righe:
                if r["giorno"] == INIZIO.isoformat():
                    r["url"] = url_falso
            with open(reg_csv, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=M.CAMPI)
                w.writeheader()
                w.writerows(righe)

            man = MF.manifesto(c_mod, "XAUUSD", LETTURA, FINE)
            reg, ris = sub / "reg.json", sub / "ris.json"
            RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
            scheda = sub / "H-147A.md"
            scheda.write_text(TEV.testo_scheda(TEV.contratto("H-147A")), encoding="utf-8")
            S.sigilla(reg, "H-147A", scheda, ["V-T"], ORA, codice=EV.impronte_codice())
            RV.prenota(ris, "P1", "H-147A", LETTURA, FINE, S.impronta(scheda), ORA)
            es = esegui_isolato(scheda, reg, ris, "P1", c_mod, cache_sv, sub / "rapporto_regolare.txt")
            return {"anomalie_manifesto": man["anomalie"], "esecuzione": es}

        url_vero = DK.url_giorno("XAUUSD", INIZIO, "BID")
        url_dom_falso = url_vero.replace("https://datafeed.dukascopy.com/", "https://evil.invalid/")
        url_data_falsa = DK.url_giorno("XAUUSD", date(2019, 5, 6), "BID")

        res_dom = prova_url("dominio_falso", url_dom_falso)
        res_data = prova_url("data_falsa", url_data_falsa)

        difetto = (
            not res_dom["anomalie_manifesto"]
            or not res_data["anomalie_manifesto"]
            or res_dom["esecuzione"]["eccezione"] is None
            or res_data["esecuzione"]["eccezione"] is None
            or res_dom["esecuzione"]["riserva"]["giorni_consumati"] > 0
            or res_data["esecuzione"]["riserva"]["giorni_consumati"] > 0
        )
        return emetti(
            "S-147a", "#147a (R19-07a)",
            "Anomalia segnalata dal manifesto sia per dominio falso sia per data dell'URL diversa da 'giorno'; "
            "rifiuto prima dell'autorizzazione con 0 giorni consumati",
            {"dominio_falso": res_dom, "data_falsa": res_data}, difetto, [base],
        )


def sonda_147b(cache: Path, cache_sv: Path) -> dict:
    """#147b (R19-07b): il manifesto esige sha256 di 64 cifre esadecimali sulle righe 'dati' prima di autorizzare."""
    with tempfile.TemporaryDirectory(prefix="r20_147b_") as td:
        base = Path(td)

        def prova_sha(etichetta: str, sha_falso: str) -> dict:
            sub = base / etichetta
            c_mod = sub / "cache"
            shutil.copytree(cache, c_mod)
            reg_csv = c_mod / "registro_scaricamento_XAUUSD_BID.csv"
            with open(reg_csv, newline="", encoding="utf-8") as fh:
                righe = list(csv.DictReader(fh))
            for r in righe:
                if r["giorno"] == INIZIO.isoformat():
                    r["sha256"] = sha_falso
            with open(reg_csv, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=M.CAMPI)
                w.writeheader()
                w.writerows(righe)

            man = MF.manifesto(c_mod, "XAUUSD", LETTURA, FINE)
            reg, ris = sub / "reg.json", sub / "ris.json"
            RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
            scheda = sub / "H-147B.md"
            scheda.write_text(TEV.testo_scheda(TEV.contratto("H-147B")), encoding="utf-8")
            S.sigilla(reg, "H-147B", scheda, ["V-T"], ORA, codice=EV.impronte_codice())
            RV.prenota(ris, "P1", "H-147B", LETTURA, FINE, S.impronta(scheda), ORA)
            es = esegui_isolato(scheda, reg, ris, "P1", c_mod, cache_sv, sub / "rapporto_regolare.txt")
            return {"anomalie_manifesto": man["anomalie"], "esecuzione": es}

        res_vuota = prova_sha("sha_vuota", "")
        res_malformata = prova_sha("sha_malformata", "ZZZ_NON_ESADECIMALE")

        difetto = (
            not res_vuota["anomalie_manifesto"]
            or not res_malformata["anomalie_manifesto"]
            or res_vuota["esecuzione"]["eccezione"] is None
            or res_malformata["esecuzione"]["eccezione"] is None
            or res_vuota["esecuzione"]["riserva"]["giorni_consumati"] > 0
            or res_malformata["esecuzione"]["riserva"]["giorni_consumati"] > 0
        )
        return emetti(
            "S-147b", "#147b (R19-07b)",
            "Riga 'dati' con sha256 vuota o non di 64 cifre esadecimali segnalata dal manifesto e rifiutata prima "
            "dell'autorizzazione (0 giorni di riserva consumati, 0 letture di verifica)",
            {"sha256_vuota": res_vuota, "sha256_malformata": res_malformata}, difetto, [base],
        )


def sonda_148(cache: Path, cache_sv: Path) -> dict:
    """#148 (R19-08, DGS-20): --rapporto che è una cartella esistente, con --ora VALIDA (condizioni separate)."""
    with tempfile.TemporaryDirectory(prefix="r20_148_") as td:
        base = Path(td)
        reg, ris = base / "reg.json", base / "ris.json"
        RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        scheda = base / "H-148.md"
        scheda.write_text(TEV.testo_scheda(TEV.contratto("H-148")), encoding="utf-8")
        S.sigilla(reg, "H-148", scheda, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris, "P1", "H-148", LETTURA, FINE, S.impronta(scheda), ORA)

        cartella_rapporto = base / "destinazione_e_cartella"
        cartella_rapporto.mkdir()

        es = esegui_isolato(scheda, reg, ris, "P1", cache, cache_sv, cartella_rapporto, ora=ORA)
        difetto = (
            es["eccezione"] is None
            or es["riserva"]["giorni_consumati"] > 0
            or len(es["riserva"]["aperture"]) > 0
            or es["chiamate_caricatore"]["verifica"] > 0
            or len(es["file_creati"]["file_temporanei_orfani"]) > 0
        )
        return emetti(
            "S-148", "#148 (R19-08)",
            "Destinazione --rapporto che punta a una cartella esistente (con --ora valida) rifiutata prima "
            "dell'autorizzazione: 0 giorni consumati, 0 aperture, 0 letture di verifica, 0 file temporanei orfani",
            es, difetto, [base],
        )


def sonda_149(cache: Path, cache_sv: Path) -> dict:
    """#149 (R19-09): confronto della quota in frazioni esatte: quota(0.15, 2, 1) == 0.025, nessun falso rifiuto."""
    with tempfile.TemporaryDirectory(prefix="r20_149_") as td:
        base = Path(td)
        q_val = RV.quota(0.15, 2, 1)
        uguale_0025 = (q_val == 0.025)

        reg, ris = base / "reg.json", base / "ris.json"
        scheda_0 = base / "H-149A.md"
        scheda_1 = base / "H-149B.md"
        scheda_0.write_text(TEV.testo_scheda(TEV.contratto("H-149A")), encoding="utf-8")
        scheda_1.write_text(TEV.testo_scheda(TEV.contratto("H-149B")), encoding="utf-8")
        S.sigilla(reg, "H-149A", scheda_0, ["V-T"], ORA, codice=EV.impronte_codice())
        S.sigilla(reg, "H-149B", scheda_1, ["V-T"], ORA, codice=EV.impronte_codice())

        try:
            RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.15, ORA)
            RV.prenota(ris, "P0", "H-149A", B_INIZIO, B_FINE, S.impronta(scheda_0), ORA)
            RV.autorizza(ris, "P0", 2, "a" * 64, ORA, m=1)
            RV.prenota(ris, "P1", "H-149B", LETTURA, FINE, S.impronta(scheda_1), ORA)
            es = esegui_isolato(scheda_1, reg, ris, "P1", cache, cache_sv, base / "rap.txt")
            falso_rifiuto_quota = (es["esito_tecnico"] == "rifiutata per quota")
        except Exception as e:
            es = {"eccezione_setup_riserva": f"{type(e).__name__}: {e}"}
            falso_rifiuto_quota = False

        difetto = (not uguale_0025) or falso_rifiuto_quota
        oss = {
            "quota_015_2_1": q_val,
            "uguale_a_0_025": uguale_0025,
            "falso_rifiuto_per_quota": falso_rifiuto_quota,
            "esecuzione_j2_alfa015": es,
        }
        return emetti(
            "S-149", "#149 (R19-09)",
            "Confronto in frazioni esatte: RV.quota(0.15, 2, 1) == 0.025 e nessun falso 'rifiutata per quota'",
            oss, difetto, [base],
        )


# ==============================================================================================================
# PARTE 2 — SONDE DEL PERCORSO VALIDO (D-56: ALMENO UNA PER RILIEVO #143–#149)
# ==============================================================================================================

def valida_143_lanciatore_e_scheda_normale(cache: Path, cache_sv: Path) -> dict:
    """V-143: corsa valida completa dal lanciatore 'avvio.py verifica' con '--scheda <file>' nella forma normale."""
    with tempfile.TemporaryDirectory(prefix="r20_v143_") as td:
        base = Path(td)
        repo, reg, ris, scheda, _ = prepara_repo_git(base, ipotesi="H-V143", id_="P1")
        rap = base / "rapporto_v143.txt"
        r = lancia_avvio_verifica(repo, [
            "--scheda", str(scheda), "--registro", EV.REL_REGISTRO_PROVE, "--riserva", EV.REL_RISERVA,
            "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
            "--rapporto", str(rap), "--ora", ORA,
        ])
        uscita = json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None
        st = stato_registri(reg, ris)
        ruoli = [v["ruolo"] for v in st["voci_registro_prove"]]
        valido = (
            r.returncode == 0
            and uscita is not None
            and uscita.get("esito_tecnico") == "completata"
            and uscita.get("esito") == "promossa"
            and uscita.get("chiamate_caricatore") == {"sviluppo": 1, "verifica": 1}
            and st["riserva"]["aperture"] == [("P1", 1, 0.025, "promossa")]
            and ruoli == ["sviluppo", "verifica", "esito"]
            and rap.is_file()
        )
        oss = {
            "rc": r.returncode,
            "uscita": uscita,
            "stderr_inizio": r.stderr.strip()[:160],
            "registri": st,
            "rapporto_creato": rap.is_file(),
        }
        return emetti(
            "V-143", "#143 — percorso valido",
            "Corsa valida dal lanciatore con '--scheda <percorso>' normale: rc=0, completata / promossa, "
            "sviluppo+verifica+esito registrati, rapporto creato",
            oss, not valido, [base],
        )


def valida_144_sedute_neutre_complete(cache_sv: Path) -> dict:
    """V-144: sedute complete senza operazioni (K=0 legittimo su dati presenti) restano ammesse e promosse."""
    with tempfile.TemporaryDirectory(prefix="r20_v144_") as td:
        base = Path(td)
        c_neutra = base / "cache_neutra"
        vere = M.scrivi(c_neutra, LETTURA, FINE, 0.6, 21, p_neutra=0.25)
        _completa_feriali_non_chiusi(c_neutra, LETTURA, FINE)
        reg, ris = base / "reg.json", base / "ris.json"
        RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        scheda = base / "H-V144.md"
        scheda.write_text(TEV.testo_scheda(TEV.contratto("H-V144")), encoding="utf-8")
        S.sigilla(reg, "H-V144", scheda, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris, "P1", "H-V144", LETTURA, FINE, S.impronta(scheda), ORA)

        es = esegui_isolato(scheda, reg, ris, "P1", c_neutra, cache_sv, base / "rap.txt")
        rec = RV.prenotazione(ris, "P1").get("record")
        neutre_attese = sum(1 for g, x in vere.items() if x is None and INIZIO <= g <= FINE)
        verd = (rec or {}).get("verdetto") or {}
        valido = (
            es["eccezione"] is None
            and es["esito_tecnico"] == "completata"
            and es["esito"] == "promossa"
            and verd.get("sedute") == 1000
            and verd.get("trade") == 1000 - neutre_attese
        )
        oss = dict(es, sedute_neutre_attese=neutre_attese, sedute=verd.get("sedute"), trade=verd.get("trade"))
        return emetti(
            "V-144", "#144 — percorso valido",
            "Con tutti i feriali completi e ~25% di sedute neutre senza segnali (K=0 legittimo), la verifica "
            "completa con esito 'promossa'",
            oss, not valido, [base],
        )


def valida_145_una_sola_verifica_ramo_principale(cache: Path, cache_sv: Path) -> dict:
    """V-145: una sola verifica sul ramo principale con ANCORA_GIT=True (alfa_tot=0.05, j=1) + ripresa identica."""
    with tempfile.TemporaryDirectory(prefix="r20_v145_") as td:
        base = Path(td)
        repo, reg, ris, scheda, g = prepara_repo_git(base, ipotesi="H-V145", id_="P1", alfa_tot=0.05)
        rap = base / "rap_v145.txt"
        r1 = lancia_avvio_verifica(repo, [
            "--scheda", str(scheda), "--registro", EV.REL_REGISTRO_PROVE, "--riserva", EV.REL_RISERVA,
            "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
            "--rapporto", str(rap), "--ora", ORA,
        ])
        u1 = json.loads(r1.stdout) if r1.returncode == 0 and r1.stdout.strip() else None
        subprocess.run(g + ["add", "-A"], check=True)
        subprocess.run(g + ["commit", "-q", "-m", "esito P1 su principale"], check=True)
        subprocess.run(g + ["push", "-q"], check=True, capture_output=True)
        rap.unlink(missing_ok=True)
        r2 = lancia_avvio_verifica(repo, [
            "--scheda", str(scheda), "--registro", EV.REL_REGISTRO_PROVE, "--riserva", EV.REL_RISERVA,
            "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
            "--rapporto", str(rap), "--ora", ORA,
        ])
        u2 = json.loads(r2.stdout) if r2.returncode == 0 and r2.stdout.strip() else None
        st = stato_registri(reg, ris)
        valido = (
            r1.returncode == 0 and u1 is not None and u1.get("esito") == "promossa"
            and r2.returncode == 0 and u2 is not None and u2.get("esito_tecnico") == "rapporto rigenerato"
            and u2.get("chiamate_caricatore") == {"sviluppo": 0, "verifica": 0}
            and st["riserva"]["aperture"] == [("P1", 1, 0.025, "promossa")]
        )
        oss = {"prima_corsa": {"rc": r1.returncode, "uscita": u1},
               "ripresa_stesso_ramo": {"rc": r2.returncode, "uscita": u2},
               "registri": st}
        return emetti(
            "V-145", "#145 — percorso valido",
            "Una sola verifica sul ramo principale (alfa_tot=0.05, j=1) riesce con 'promossa' e la successiva "
            "ripresa identica rigenera il rapporto senza rileggere i dati",
            oss, not valido, [base],
        )


def valida_146_ambiente_fuso_ora_contratto_validi(cache: Path, cache_sv: Path) -> dict:
    """V-146: ambiente isolato pulito, fuso Europe/London, --ora ISO-8601 UTC valida, soglia finita e ipotesi valida."""
    with tempfile.TemporaryDirectory(prefix="r20_v146_") as td:
        base = Path(td)
        repo, reg, ris, scheda, g = prepara_repo_git(base, ipotesi="H-V146", id_="P1")
        c_letto = EV.leggi_contratto(scheda)
        rap = base / "rap_v146.txt"
        r1 = lancia_avvio_verifica(repo, [
            "--scheda", str(scheda), "--registro", EV.REL_REGISTRO_PROVE, "--riserva", EV.REL_RISERVA,
            "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
            "--rapporto", str(rap), "--ora", "2026-11-26T09:00:00Z",
        ])
        u1 = json.loads(r1.stdout) if r1.returncode == 0 and r1.stdout.strip() else None
        subprocess.run(g + ["add", "-A"], check=True)
        subprocess.run(g + ["commit", "-q", "-m", "esito V146"], check=True)
        subprocess.run(g + ["push", "-q"], check=True, capture_output=True)
        r2 = lancia_avvio_verifica(repo, [
            "--scheda", str(scheda), "--registro", EV.REL_REGISTRO_PROVE, "--riserva", EV.REL_RISERVA,
            "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
            "--rapporto", str(rap), "--ora", "2026-11-26T09:05:00Z",
        ])
        u2 = json.loads(r2.stdout) if r2.returncode == 0 and r2.stdout.strip() else None
        valido = (
            c_letto["ipotesi"] == "H-V146"
            and math.isfinite(c_letto["veto_blocchi"]["soglia"])
            and r1.returncode == 0 and u1 is not None and u1.get("esito") == "promossa"
            and r2.returncode == 0 and u2 is not None and u2.get("esito_tecnico") == "rapporto rigenerato"
        )
        oss = {
            "ipotesi": c_letto["ipotesi"],
            "soglia_veto": c_letto["veto_blocchi"]["soglia"],
            "verifica_rc": r1.returncode,
            "verifica_esito": u1.get("esito") if u1 else None,
            "ripresa_rc": r2.returncode,
            "ripresa_esito_tecnico": u2.get("esito_tecnico") if u2 else None,
        }
        return emetti(
            "V-146", "#146 — percorso valido",
            "Con ambiente isolato pulito, fuso Europe/London regolare, --ora ISO-8601 UTC valida e contratto finito, "
            "sia la verifica sia la ripresa dal lanciatore riescono (rc=0)",
            oss, not valido, [base],
        )


def valida_147_manifesto_canonico(cache: Path, cache_sv: Path) -> dict:
    """V-147: registri dello scaricamento con URL Dukascopy canonici e sha256 esadecimali a 64 cifre passano."""
    with tempfile.TemporaryDirectory(prefix="r20_v147_") as td:
        base = Path(td)
        man = MF.manifesto(cache, "XAUUSD", LETTURA, FINE)
        reg, ris = base / "reg.json", base / "ris.json"
        RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        scheda = base / "H-V147.md"
        scheda.write_text(TEV.testo_scheda(TEV.contratto("H-V147")), encoding="utf-8")
        S.sigilla(reg, "H-V147", scheda, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris, "P1", "H-V147", LETTURA, FINE, S.impronta(scheda), ORA)
        es = esegui_isolato(scheda, reg, ris, "P1", cache, cache_sv, base / "rap.txt")
        valido = (
            man["anomalie"] == []
            and es["eccezione"] is None
            and es["esito_tecnico"] == "completata"
            and es["esito"] == "promossa"
        )
        oss = {"anomalie_manifesto": man["anomalie"], "voci_elenco": len(man["elenco"]), "esecuzione": es}
        return emetti(
            "V-147", "#147 — percorso valido",
            "Manifesto con URL Dukascopy canonici e sha256 esadecimali di 64 cifre dà anomalie=[] e verifica 'promossa'",
            oss, not valido, [base],
        )


def valida_148_rapporto_valido(cache: Path, cache_sv: Path) -> dict:
    """V-148: --rapporto valido (file regolare in sottocartella nuova, poi rigenerazione su file esistente)."""
    with tempfile.TemporaryDirectory(prefix="r20_v148_") as td:
        base = Path(td)
        reg, ris = base / "reg.json", base / "ris.json"
        RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        scheda = base / "H-V148.md"
        scheda.write_text(TEV.testo_scheda(TEV.contratto("H-V148")), encoding="utf-8")
        S.sigilla(reg, "H-V148", scheda, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris, "P1", "H-V148", LETTURA, FINE, S.impronta(scheda), ORA)

        percorso_rap = base / "sottocartella_nuova" / "rapporto_verifica.txt"
        es1 = esegui_isolato(scheda, reg, ris, "P1", cache, cache_sv, percorso_rap, ora=ORA)
        es2 = esegui_isolato(scheda, reg, ris, "P1", cache, cache_sv, percorso_rap, ora=ORA)
        rec = RV.record_esito(ris, "P1")
        coerente_col_record = (
            percorso_rap.is_file()
            and rec is not None
            and percorso_rap.read_text(encoding="utf-8") == EV.rapporto_da_record(rec)
        )
        valido = (
            es1["eccezione"] is None and es1["esito"] == "promossa"
            and es2["eccezione"] is None and es2["esito_tecnico"] == "rapporto rigenerato"
            and coerente_col_record
            and es1["file_creati"]["file_temporanei_orfani"] == []
            and es2["file_creati"]["file_temporanei_orfani"] == []
        )
        oss = {"prima_scrittura": es1, "sovrascrittura_ripresa": es2, "uguale_a_rapporto_da_record": coerente_col_record}
        return emetti(
            "V-148", "#148 — percorso valido",
            "Percorso --rapporto valido (file regolare nuovo e successiva rigenerazione) scritto atomicamente, "
            "coerente col record e senza file temporanei orfani",
            oss, not valido, [base],
        )


def valida_149_quota_esatta(cache: Path, cache_sv: Path) -> dict:
    """V-149: quota esatta D-38 (alfa_tot=0.05, j=1, m=1 -> 0.025) ammessa e completata con 'promossa'."""
    with tempfile.TemporaryDirectory(prefix="r20_v149_") as td:
        base = Path(td)
        q_d38 = RV.quota(0.05, 1, 1)
        reg, ris = base / "reg.json", base / "ris.json"
        RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        scheda = base / "H-V149.md"
        scheda.write_text(TEV.testo_scheda(TEV.contratto("H-V149")), encoding="utf-8")
        S.sigilla(reg, "H-V149", scheda, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris, "P1", "H-V149", LETTURA, FINE, S.impronta(scheda), ORA)
        es = esegui_isolato(scheda, reg, ris, "P1", cache, cache_sv, base / "rap.txt")
        valido = (
            q_d38 == 0.025
            and es["eccezione"] is None
            and es["esito_tecnico"] == "completata"
            and es["esito"] == "promossa"
            and es["riserva"]["aperture"] == [("P1", 1, 0.025, "promossa")]
            and es["riserva"]["rifiuti"] == []
        )
        oss = {"quota_005_1_1": q_d38, "esecuzione": es}
        return emetti(
            "V-149", "#149 — percorso valido",
            "Quota D-38 (alfa_tot=0.05, j=1, m=1) pari esattamente a 0.025: verifica ammessa e completata 'promossa'",
            oss, not valido, [base],
        )


# ==============================================================================================================
# PARTE 3 — SERIE COMPLETA DELLE SONDE #124 (D1, D2, D3, D4, D5, D6a, D6b)
# ==============================================================================================================

def sonde_124_complete() -> List[dict]:
    out = []

    # D1: screening k=300, somma esatta 75 + 2^-48 > 75 -> ammessa=True
    xs_d1 = [0.25] * 299 + [0.25 + math.ldexp(1.0, -48)]
    with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.1, 0.4)):
        s_d1 = V.screening([(x, 1) for x in xs_d1], 9, 0.9)
    out.append(emetti(
        "S-124-D1", "#124 D1",
        "screening() su k=300 con somma esatta 75 + 2^-48 (> +0.25 R): ammessa=True, cause=[]",
        {"ammessa": s_d1["ammessa"], "cause": s_d1["cause"], "media": s_d1["media"]},
        not (s_d1["ammessa"] is True and s_d1["cause"] == []),
    ))

    # D2: veto_blocchi k=250, somma esatta -62.5 - 2^-49 < -62.5 -> esito='fallito'
    xs_d2 = [-0.25] * 249 + [-0.25 - math.ldexp(1.0, -49)]
    vb_d2 = V.veto_blocchi([(x, 1) for x in xs_d2], soglia=-0.25, minimo_trade_blocco=50, ampiezza=250)
    out.append(emetti(
        "S-124-D2", "#124 D2",
        "veto_blocchi() su k=250 con somma esatta -62.5 - 2^-49 (< -0.25 R): esito='fallito'",
        {"esito": vb_d2["esito"], "medie": vb_d2["medie"]},
        vb_d2["esito"] != "fallito",
    ))

    # D3: veto_blocchi su serie costante uguale alla soglia (k=3, x=-0.4 + scansione 242 casi) -> esito='superato'
    falsi_veti = []
    for k in (3, 7, 29, 49, 250, 251, 300):
        valori_x = [num / 1000.0 for num in range(-400, 401)] + [p / q for p, q in ((-1, 3), (-1, 7), (-2, 7), (-1, 6), (-1, 9), (-1, 11), (-1, 13))]
        for x in valori_x:
            if math.fsum([x] * k) / k < x:
                vb = V.veto_blocchi([(x, 1)] * k, soglia=x, minimo_trade_blocco=1, ampiezza=k)
                if vb["esito"] != "superato":
                    falsi_veti.append((k, x, vb["esito"]))
    vb_k3 = V.veto_blocchi([(-0.4, 1)] * 3, soglia=-0.4, minimo_trade_blocco=1, ampiezza=3)
    out.append(emetti(
        "S-124-D3", "#124 D3",
        "veto_blocchi() su serie costante [(x,1)]*k con soglia=x (incluso k=3, x=-0.4 e tutti i casi con fsum/k < x): "
        "sempre esito='superato' (0 falsi veti)",
        {"k3_x_meno_04_esito": vb_k3["esito"], "falsi_veti_nella_scansione": len(falsi_veti)},
        vb_k3["esito"] != "superato" or len(falsi_veti) > 0,
    ))

    # D4 (mancante in R19): media descrittiva in verdetto() uguale al quoziente razionale esatto arrotondato UNA volta
    casi_d4 = {
        "k1000_250_piu_2m46": ([0.25] * 249 + [0.25 + math.ldexp(1.0, -48)]) * 4,
        "k1000_250_piu_2m42": ([0.25] * 249 + [0.25 + math.ldexp(1.0, -44)]) * 4,
        "k3_costante_meno_04": [-0.4, -0.4, -0.4],
        "k300_tripla_01_02_045": [0.1, 0.2, 0.45] * 100,
    }
    dettagli_d4 = {}
    divergenze_d4 = 0
    for nome_c, xs in casi_d4.items():
        cp = [(x, 1) for x in xs]
        attesa_flt = float(sum((Fraction(x) for x in xs), Fraction(0)) / len(xs))
        v_res = V.verdetto(cp, 5)
        uguale = (v_res["media"] == attesa_flt)
        if not uguale:
            divergenze_d4 += 1
        dettagli_d4[nome_c] = {"media_modulo": v_res["media"], "media_quoziente_esatto_float": attesa_flt, "uguale": uguale}
    out.append(emetti(
        "S-124-D4", "#124 D4",
        "Media descrittiva in verdetto() uguale a float(somma_esatta_Fraction / trade) (un solo arrotondamento finale)",
        {"casi": dettagli_d4, "divergenze": divergenze_d4},
        divergenze_d4 > 0,
    ))

    # D5 (mancante in R19): bordi esatti ±1e-9 su L_vicino_a_zero (screening + rapporto) e su vicini(lo, hi)
    cp_ok = [(0.6, 1) if i % 2 == 0 else (0.4, 1) for i in range(300)]
    bordi_screening = {}
    err_d5 = False
    clausola = "limite inferiore a meno di 1e-9 R [REGOLA] da 0 (non cambia l'esito; arrotondamento possibile, #124)"
    for et, val_l in (
        ("piu_1e9", 1e-9),
        ("meno_1e9", -1e-9),
        ("sotto_piu_1e9", math.nextafter(1e-9, 0.0)),
        ("sopra_meno_1e9", math.nextafter(-1e-9, 0.0)),
    ):
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(val_l, 0.5)):
            sr = V.screening(cp_ok, 9, 0.9)
        atteso_vic = abs(Fraction(val_l)) < Fraction(V.VICINANZA)
        rap_txt = V.rapporto_screening(sr)
        clausola_presente = clausola in rap_txt
        ok_caso = (sr["L_vicino_a_zero"] is atteso_vic) and (clausola_presente is atteso_vic)
        if not ok_caso:
            err_d5 = True
        bordi_screening[et] = {
            "L": val_l, "atteso": atteso_vic, "osservato": sr["L_vicino_a_zero"],
            "clausola_nel_rapporto": clausola_presente,
        }
    sr_zero = V.screening([(0.0, 0)] * 10, 9, 0.9)
    with mock.patch.object(P, "intervallo_bootstrap", return_value=(float("nan"), 0.5)):
        sr_inv = V.screening(cp_ok, 9, 0.9)
    if sr_zero["L_vicino_a_zero"] is not False or sr_inv["L_vicino_a_zero"] is not False:
        err_d5 = True

    bordi_vicini = {}
    for nome_v, lo, hi, soglia_f, quale in (
        ("L_piu_1e9", 0.20 + 1e-9, 0.5, V.SOGLIA_PROMOZIONE, "L"),
        ("L_meno_1e9", 0.20 - 1e-9, 0.5, V.SOGLIA_PROMOZIONE, "L"),
        ("U_piu_1e9", 0.0, 0.10 + 1e-9, V.SOGLIA_BOCCIATURA, "U"),
        ("U_meno_1e9", 0.0, 0.10 - 1e-9, V.SOGLIA_BOCCIATURA, "U"),
    ):
        estremo = lo if quale == "L" else hi
        att_flt = abs(Fraction(estremo) - Fraction(soglia_f)) < Fraction(V.VICINANZA)
        oss_vic = quale in V.vicini(lo, hi)
        if oss_vic != att_flt:
            err_d5 = True
        bordi_vicini[nome_v] = {"atteso_su_float": att_flt, "osservato": oss_vic}

    out.append(emetti(
        "S-124-D5", "#124 D5",
        "Bordi ±1e-9: L_vicino_a_zero strettamente < 1e-9 (False su ±1e-9, True su nextafter verso 0 con clausola "
        "#124 nel rapporto, False senza trade o con intervallo invalido); vicini(lo, hi) coerente sui float passati",
        {
            "screening_bordi": bordi_screening,
            "zero_trade_L_vicino": sr_zero["L_vicino_a_zero"],
            "intervallo_invalido_L_vicino": sr_inv["L_vicino_a_zero"],
            "vicini_soglia": bordi_vicini,
        },
        err_d5,
    ))

    # D6a e D6b: controlla_coppie indipendente dall'ordine degli addendi estremi ±1.5e308
    for cod, ril, perm in (
        ("S-124-D6a", "#124 D6a", [(1.5e308, 1), (-1.5e308, 1), (1.5e308, 1)]),
        ("S-124-D6b", "#124 D6b", [(1.5e308, 1), (1.5e308, 1), (-1.5e308, 1)]),
    ):
        try:
            V.controlla_coppie(perm)
            ecc = None
        except Exception as e:
            ecc = f"{type(e).__name__}: {e}"
        rifiutato_ok = ecc is not None and ecc.startswith("ValueError:")
        out.append(emetti(
            cod, ril,
            "controlla_coppie() rifiuta con ValueError le somme non finite indipendentemente dall'ordine degli addendi",
            {"eccezione": ecc},
            not rifiutato_ok,
        ))

    return out


def main() -> int:
    esigi_zero = "--esigi-zero-difetti" in sys.argv[1:]
    risultati = []
    with tempfile.TemporaryDirectory(prefix="r20_cache_") as tc:
        base_c = Path(tc)
        cache = base_c / "cache"
        cache_sv = base_c / "cache_sviluppo"
        M.scrivi(cache, LETTURA, FINE, 0.6, 11)
        M.scrivi(cache, B_INIZIO, B_FINE, 0.6, 12)
        M.scrivi(cache_sv, *SVILUPPO, 0.6, 13)
        _completa_feriali_non_chiusi(cache, LETTURA, FINE)
        _completa_feriali_non_chiusi(cache, B_INIZIO, B_FINE)
        _completa_feriali_non_chiusi(cache_sv, *SVILUPPO)

        # 1. Rilievi aperti (#143–#149)
        risultati.append(sonda_143(cache, cache_sv))
        risultati.append(sonda_144(cache, cache_sv))
        risultati.append(sonda_145(cache, cache_sv))
        risultati.append(sonda_146a(cache, cache_sv))
        risultati.append(sonda_146b(cache, cache_sv))
        risultati.append(sonda_146c(cache, cache_sv))
        risultati.append(sonda_146d(cache, cache_sv))
        risultati.append(sonda_146e())
        risultati.append(sonda_147a(cache, cache_sv))
        risultati.append(sonda_147b(cache, cache_sv))
        risultati.append(sonda_148(cache, cache_sv))
        risultati.append(sonda_149(cache, cache_sv))

        # 2. Percorsi validi (almeno uno per rilievo #143–#149)
        risultati.append(valida_143_lanciatore_e_scheda_normale(cache, cache_sv))
        risultati.append(valida_144_sedute_neutre_complete(cache_sv))
        risultati.append(valida_145_una_sola_verifica_ramo_principale(cache, cache_sv))
        risultati.append(valida_146_ambiente_fuso_ora_contratto_validi(cache, cache_sv))
        risultati.append(valida_147_manifesto_canonico(cache, cache_sv))
        risultati.append(valida_148_rapporto_valido(cache, cache_sv))
        risultati.append(valida_149_quota_esatta(cache, cache_sv))

        # 3. Serie completa #124 (D1–D6, incluse D4 e D5)
        risultati.extend(sonde_124_complete())

    if esigi_zero and any(r["difetto_presente"] for r in risultati):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
