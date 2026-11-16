"""Mandato R13 · Compito B: attacco alle correzioni nuove (#48, #49, #50, #51).

Sonde:
- B-#48: moduli_brain vs import dinamici (importlib, __import__, exec), pacchetti senza __init__.py,
         PYTHONPATH che ombra brain/ o librerie standard mentre impronte_codice(RADICE) resta valida,
         file .pth e sitecustomize.py senza -s/-I.
- B-#49: completezza caricatore (#49): aggiramento soglia 263 minuti con 263 min fuori ORB (12:22-16:45),
         esclusione giorni_corti (24/12, 31/12 passano con 1 solo tick 00:00 UTC), test falsi positivi
         su cambio ora legale UK/US, vol=0 scartati da decodifica, e mezze giornate fuori da 24/12 e 31/12.
- B-#50: calendario (#50) su tutti gli anni 2005-2023: audit completo chiusure_note e giorni_corti,
         evidenziando chiusure UK (Santo Stefano 26/12, Lunedì dell'Angelo, martedì 28/12) tollerate vuote
         anche se l'oro NY quota normalmente e sovrapposizioni giorni_corti / chiusure_note.
- B-#51: controlla_ancora (#51): test reali con repo git temporaneo su symlink (interno tracciato ->
         JSONDecodeError non catturato da ValueError!; symlink non tracciato a file tracciato),
         commit riscritti (git commit --amend), voci non ancora committate fra sviluppo e verifica,
         HEAD staccata su commit precedente, registro su altro ramo.
"""
from __future__ import annotations

import contextlib
from datetime import date, datetime, time, timedelta, timezone
import io
import json
import lzma
import os
from pathlib import Path
import shutil
import site
import subprocess
import sys
import tempfile
from unittest.mock import patch
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
DA_GEMINI = Path(__file__).resolve().parent
if str(DA_GEMINI) not in sys.path:
    sys.path.insert(0, str(DA_GEMINI))

from brain.dati.pipeline import calendario as CAL  # noqa: E402
from brain.dati.pipeline import dukascopy as DK  # noqa: E402
from brain.laboratorio.esecuzione import caricatore as C  # noqa: E402
from brain.laboratorio.esecuzione import esegui_h002 as E  # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S  # noqa: E402
from brain.laboratorio.esecuzione import sintetico as SN  # noqa: E402
from brain.laboratorio.simulatori import orb_londra as O  # noqa: E402

ORA = "2026-11-16T01:00:00Z"


def _bi5_minuti(giorno: date, minuti_utc: list, vol: float = 1.0) -> bytes:
    recs = []
    for t in minuti_utc:
        sec = t.hour * 3600 + t.minute * 60
        recs.append(DK.RECORD.pack(sec, 2000_000, 2000_000, 2000_000, 2000_000, vol))
    return lzma.compress(b"".join(recs), format=lzma.FORMAT_ALONE) if recs else b""


def _cache_sviluppo_valida(cache_dir: Path, override_giorno: dict = None) -> None:
    override_giorno = override_giorno or {}
    sv_i, sv_f = E.PERIODO_SVILUPPO
    b, a = SN.mercato(sv_i, (sv_f - sv_i).days + 1, seme=3, sd=0.7)
    SN.scrivi_cache(b, cache_dir / "XAUUSD", inizio=sv_i, fine=sv_f)
    SN.scrivi_cache(a, cache_dir / "XAUUSD_ASK", inizio=sv_i, fine=sv_f)
    for g, corpo in override_giorno.items():
        for sub in ("XAUUSD", "XAUUSD_ASK"):
            (cache_dir / sub / f"{g.isoformat()}.bi5").write_bytes(corpo)


def _init_git_repo(repo: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=str(repo), check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "T"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@invalid"], check=True)


def sonda_b_48_codice_fuori_impronte(base: Path) -> dict:
    # 1. Import dinamici + namespace package senza __init__.py ignorati da moduli_brain
    d = base / "b48"
    d.mkdir()
    rad = d / "repo_dyn"
    shutil.copytree(REPO_ROOT / "brain", rad / "brain",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "cache_dukascopy", "partizioni", "*.csv", "da-gemini"))
    ns_dir = rad / "brain" / "ns_senza_init"
    ns_dir.mkdir()
    (ns_dir / "nascosto.py").write_text("X = 42\n", encoding="utf-8")
    (rad / "brain" / "laboratorio" / "esecuzione" / "dinamico_helper.py").write_text("Y = 99\n", encoding="utf-8")
    es_path = rad / "brain" / "laboratorio" / "esecuzione" / "esegui_h002.py"
    es_orig = es_path.read_text(encoding="utf-8")
    # Aggiungiamo importlib + __import__ + exec in esegui_h002.py
    es_path.write_text(
        es_orig + "\nimport importlib\nimportlib.import_module('brain.ns_senza_init.nascosto')\n__import__('brain.laboratorio.esecuzione.dinamico_helper')\n",
        encoding="utf-8",
    )
    lista_mod = E.moduli_brain(rad)
    mancano_dinamici = (
        "brain/ns_senza_init/nascosto.py" not in lista_mod
        and "brain/laboratorio/esecuzione/dinamico_helper.py" not in lista_mod
    )

    # 2. PYTHONPATH che ombra brain/laboratorio/esecuzione/criteri.py (o stdlib) + sitecustomize.py + .pth!
    #    Nota: eseguire python3 SENZA modificare RADICE -> impronte_codice(RADICE) combacia al 100% col sigillo!
    d2 = d / "repo_pypath"
    shutil.copytree(REPO_ROOT / "brain", d2 / "brain",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "cache_dukascopy", "partizioni", "*.csv", "da-gemini"))
    _init_git_repo(d2)
    scheda = d2 / "H-002.md"
    scheda.write_text("# H-002\n", encoding="utf-8")
    reg, cache, rap = d2 / "reg.json", d / "cache_48", d / "sv.md"
    _cache_sviluppo_valida(cache)
    # Sigilliamo con il repo pulito d2
    cod_pulito = E.impronte_codice(d2)
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA, codice=cod_pulito)
    subprocess.run(["git", "-C", str(d2), "add", "."], check=True)
    subprocess.run(["git", "-C", str(d2), "commit", "-q", "-m", "clean"], check=True)

    # Ora prepariamo cartella esterna shadow su PYTHONPATH:
    shadow = d / "shadow_pypath"
    (shadow / "brain" / "laboratorio" / "esecuzione").mkdir(parents=True)
    (shadow / "brain" / "__init__.py").write_text("", encoding="utf-8")
    (shadow / "brain" / "laboratorio" / "__init__.py").write_text("", encoding="utf-8")
    marker_pth = d / "pth_ran.txt"
    marker_site = d / "sitecust_ran.txt"
    marker_crit = d / "crit_shadow_ran.txt"
    (shadow / "sitecustomize.py").write_text(
        f"from pathlib import Path; Path({str(marker_site)!r}).write_text('SITE_OK')\n",
        encoding="utf-8",
    )
    (shadow / "evil.pth").write_text(
        f"import pathlib; pathlib.Path({str(marker_pth)!r}).write_text('PTH_OK')\n",
        encoding="utf-8",
    )
    # Copiamo criteri.py originale ma con hook per marcare l'esecuzione ombrata!
    crit_orig = (d2 / "brain" / "laboratorio" / "esecuzione" / "criteri.py").read_text(encoding="utf-8")
    # Inoltre ombriamo solo `statistics`? No: con `site.addsitedir` o PYTHONPATH prima del repo, Python importa `shadow/brain/...`
    # Se shadow non ha gli altri file `brain/`, Python fallirebbe l'import se `shadow/brain/__init__.py` oscura `d2/brain` ->
    # quindi in `shadow` copiamo `brain` (con hook in criteri.py) e mettiamo d2 al secondo posto!
    shutil.copytree(d2 / "brain", shadow / "brain", dirs_exist_ok=True)
    (shadow / "brain" / "laboratorio" / "esecuzione" / "criteri.py").write_text(
        crit_orig + f"\nfrom pathlib import Path as _P; _P({str(marker_crit)!r}).write_text('CRIT_SHADOW')\n",
        encoding="utf-8",
    )

    # Caso A: invocazione standard `python3` senza `-s` con PYTHONPATH=shadow (ma RADICE dentro `d2` rimane intatto!)
    env_a = dict(os.environ, PYTHONPATH=f"{shadow}{os.pathsep}{d2}")
    # Nota: se eseguiamo `d2/.../esegui_h002.py` per path, `__file__` è dentro `d2` -> RADICE = `d2`!
    proc_shadow = subprocess.run(
        [sys.executable, "-B", str(d2 / "brain" / "laboratorio" / "esecuzione" / "esegui_h002.py"),
         "--modalita", "sviluppo", "--rapporto", str(rap), "--registro", str(reg),
         "--scheda", str(scheda), "--cache", str(cache), "--ora", ORA],
        cwd=str(d2), env=env_a, capture_output=True, text=True, timeout=180,
    )

    # Caso B: .pth dentro cartella site aggiuntiva elaborata da `site`
    # Nota: PYTHONPATH non processa i file .pth (solo sys.path), mentre PYTHONUSERBASE/site-packages sì se senza `-s`!
    user_sp = Path(site.getusersitepackages() if False else d / "userbase" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages")
    user_sp.mkdir(parents=True, exist_ok=True)
    (user_sp / "evil_user.pth").write_text(
        f"import pathlib; pathlib.Path({str(marker_pth)!r}).write_text('PTH_OK')\n",
        encoding="utf-8",
    )
    env_b = dict(os.environ, PYTHONUSERBASE=str(d / "userbase"))
    proc_pth = subprocess.run(
        [sys.executable, "-B", "-m", "brain.laboratorio.esecuzione.esegui_h002", "--help"],
        cwd=str(d2), env=env_b, capture_output=True, text=True, timeout=60,
    )
    return {
        "dinamici_e_namespace_fuori_moduli_brain": mancano_dinamici,
        "rc_con_PYTHONPATH_shadow_criteri_e_sitecustomize": proc_shadow.returncode,
        "sitecustomize_eseguito": marker_site.exists(),
        "criteri_ombrato_eseguito_mentre_sigillo_d2_valido": marker_crit.exists(),
        "pth_via_PYTHONUSERBASE_eseguito_senza_s": proc_pth.returncode == 0 and marker_pth.exists(),
    }


def sonda_b_49_completezza_sessione(base: Path) -> dict:
    d = base / "b49"
    d.mkdir()
    scheda = d / "H-002.md"
    scheda.write_text("# H-002\n", encoding="utf-8")
    reg = d / "reg.json"
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)

    # 1. Aggiramento #49: 263 minuti dalle 12:22 alle 16:44 Londra (= zero minuti nel range 08:00-08:30!)
    g_agg = date(2024, 3, 15)
    t_start = datetime.combine(g_agg, time(12, 22), tzinfo=ZoneInfo("Europe/London")).astimezone(timezone.utc)
    min_dopo_orb = [t_start + timedelta(minutes=k) for k in range(263)]
    c1 = d / "c_aggira"
    _cache_sviluppo_valida(c1, {g_agg: _bi5_minuti(g_agg, min_dopo_orb, vol=1.0)})
    _, _, info1 = C.carica(c1 / "XAUUSD", c1 / "XAUUSD_ASK", E.PERIODO_SVILUPPO[0], E.PERIODO_SVILUPPO[1],
                           "sviluppo", reg, "H-002", scheda)
    # Check anche su 2024-12-24 (giorno corto): 1 solo tick alle 00:00 UTC passa come valido!
    g_corto = date(2024, 12, 24)
    c2 = d / "c_corto"
    _cache_sviluppo_valida(c2, {g_corto: _bi5_minuti(g_corto, [datetime(2024, 12, 24, 0, 0, tzinfo=timezone.utc)], vol=1.0)})
    _, _, info2 = C.carica(c2 / "XAUUSD", c2 / "XAUUSD_ASK", E.PERIODO_SVILUPPO[0], E.PERIODO_SVILUPPO[1],
                           "sviluppo", reg, "H-002", scheda)

    # 2. Check falsi positivi:
    #    (a) cambio ora legale (2024-03-29 vs 2024-04-01 UK e 2024-11-01/04 US): mercato sintetico completo -> nessun incompleto?
    #    (b) giorno con 525 record ma vol=0.0 (zero scambi) vs mezza giornata reale 240 min (08:00-12:00) fuori 24/12 e 31/12
    g_vol0 = date(2024, 5, 10)
    t_800 = datetime.combine(g_vol0, time(8, 0), tzinfo=ZoneInfo("Europe/London")).astimezone(timezone.utc)
    min_525 = [t_800 + timedelta(minutes=k) for k in range(525)]
    c3 = d / "c_vol0"
    _cache_sviluppo_valida(c3, {g_vol0: _bi5_minuti(g_vol0, min_525, vol=0.0)})
    _, _, info3 = C.carica(c3 / "XAUUSD", c3 / "XAUUSD_ASK", E.PERIODO_SVILUPPO[0], E.PERIODO_SVILUPPO[1],
                           "sviluppo", reg, "H-002", scheda)

    g_half = date(2024, 7, 3)  # vigilia 4 luglio (240 min 08:00-12:00 < 263 min)
    t_h = datetime.combine(g_half, time(8, 0), tzinfo=ZoneInfo("Europe/London")).astimezone(timezone.utc)
    c4 = d / "c_half"
    _cache_sviluppo_valida(c4, {g_half: _bi5_minuti(g_half, [t_h + timedelta(minutes=k) for k in range(240)], vol=1.0)})
    _, _, info4 = C.carica(c4 / "XAUUSD", c4 / "XAUUSD_ASK", E.PERIODO_SVILUPPO[0], E.PERIODO_SVILUPPO[1],
                           "sviluppo", reg, "H-002", scheda)

    # E giorno di cambio ora legale su cache normale (info1 su giorni DST): incompleti?
    return {
        "aggirato_263min_dopo_orb_incompleti": info1["feriali_incompleti_bid"],
        "aggirato_24_12_1tick_00utc_incompleti": info2["feriali_incompleti_bid"],
        "aggirato_24_12_1tick_00utc_vuoti": info2["feriali_vuoti_bid"],
        "vol_0_tutto_il_giorno_diventa_feriale_vuoto": info3["feriali_vuoti_bid"],
        "mezza_giornata_240min_3luglio_diventa_incompleta": info4["feriali_incompleti_bid"],
    }


def sonda_b_50_calendario_2005_2023() -> dict:
    # Analisi completa 2005-2023 di CAL.chiusure_note e CAL.giorni_corti
    tutti_giorni = []
    boxing_day_feriali = []
    lunedi_angelo = []
    martedi_dic28 = []
    sovrapposizioni_corte = []
    for a in range(2005, 2024):
        cn = CAL.chiusure_note(a)
        gc = CAL.giorni_corti(a)
        tutti_giorni.extend(sorted(d.isoformat() for d in cn if d.weekday() < 5))
        if date(a, 12, 26).weekday() < 5:
            boxing_day_feriali.append(date(a, 12, 26).isoformat())
        pa_lun = CAL.pasqua(a) + timedelta(days=1)
        lunedi_angelo.append(pa_lun.isoformat())
        if date(a, 12, 28) in cn and date(a, 12, 28).weekday() < 5:
            martedi_dic28.append(date(a, 12, 28).isoformat())
        for x in sorted(cn & gc):
            if x.weekday() < 5:
                sovrapposizioni_corte.append(x.isoformat())
    return {
        "tot_chiusure_note_feriali_2005_2023": len(tutti_giorni),
        "boxing_day_feriali_tollerati_vuoti": boxing_day_feriali,
        "lunedi_angelo_tollerati_vuoti": len(lunedi_angelo),
        "martedi_dic28_tollerati_vuoti": martedi_dic28,
        "giorni_corti_anche_in_chiusure_note": sovrapposizioni_corte,
    }


def _setup_git_reg(repo: Path):
    repo.mkdir(parents=True, exist_ok=True)
    _init_git_repo(repo)
    scheda = repo / "H-002.md"
    scheda.write_text("# H-002\n", encoding="utf-8")
    reg = repo / "reg.json"
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
    S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": False}, ORA)
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "c1"], check=True)
    return scheda, reg


def sonda_b_51_controlla_ancora(base: Path) -> dict:
    d = base / "b51"
    d.mkdir()
    out = {}

    # 1a. Symlink verso esterno -> bloccato
    r1 = d / "r1"
    _, reg1 = _setup_git_reg(r1)
    ext = d / "esterno.json"
    ext.write_text(reg1.read_text(encoding="utf-8"), encoding="utf-8")
    sym_ext = r1 / "sym_ext.json"
    sym_ext.symlink_to(ext)
    try:
        S.controlla_ancora(sym_ext, r1)
        out["symlink_esterno"] = "PASSATO"
    except ValueError as e:
        out["symlink_esterno"] = f"BLOCCATO:{e}"

    # 1b. Symlink tracciato in git che punta a reg1.json -> `git show HEAD:sym` restituisce il testo del path -> json.loads CRASHA!
    sym_tracked = r1 / "sym_tracked.json"
    sym_tracked.symlink_to("reg.json")
    subprocess.run(["git", "-C", str(r1), "add", "sym_tracked.json"], check=True)
    subprocess.run(["git", "-C", str(r1), "commit", "-q", "-m", "sym"], check=True)
    # Se controllo su un symlink non tracciato `sym_untracked -> reg.json`:
    sym_untracked = r1 / "sym_untracked.json"
    sym_untracked.symlink_to(reg1)
    try:
        S.controlla_ancora(sym_untracked, r1)
        out["symlink_interno_non_tracciato_a_reg1"] = "PASSATO_SILENZIOSAMENTE"
    except Exception as e:
        out["symlink_interno_non_tracciato_a_reg1"] = f"{type(e).__name__}:{e}"

    # 1c. Symlink puntante a reg1 passato ad altra cartella (se symlink sostituito con link a altro file tracciato!)
    r_trk_link = r1 / "link_in_git"
    r_trk_link.symlink_to("link_target_reg.json")
    (r1 / "link_target_reg.json").write_text(reg1.read_text(encoding="utf-8"), encoding="utf-8")
    subprocess.run(["git", "-C", str(r1), "add", "link_in_git", "link_target_reg.json"], check=True)
    subprocess.run(["git", "-C", str(r1), "commit", "-q", "-m", "sym2"], check=True)
    try:
        S.controlla_ancora(r_trk_link, r1)
        out["symlink_interno_tracciato_a_json"] = "PASSATO"
    except ValueError as e:
        out["symlink_interno_tracciato_a_json"] = f"BLOCCATO:{e}"

    # 2. Commit riscritto localmente (git commit --amend): controlla_ancora controlla solo HEAD locale, non origin!
    r2 = d / "r2"
    _, reg2 = _setup_git_reg(r2)
    raw = json.loads(reg2.read_text(encoding="utf-8"))
    raw["esecuzioni"][0]["promossa"] = True
    reg2.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    subprocess.run(["git", "-C", str(r2), "add", "reg.json"], check=True)
    subprocess.run(["git", "-C", str(r2), "commit", "-q", "--amend", "-m", "rewritten"], check=True)
    try:
        S.controlla_ancora(reg2, r2)
        out["commit_riscritto_amend"] = "PASSATO"
    except ValueError as e:
        out["commit_riscritto_amend"] = f"BLOCCATO:{e}"

    # 3. File NON ancora committato: HEAD ha solo `sigilla`, sviluppo avviene ma non viene committato,
    #    poi si manomette sviluppo prima della verifica (o si modifica codice con ANCORA_GIT=False prima di sigillare)!
    r3 = d / "r3"
    r3.mkdir()
    _init_git_repo(r3)
    sc3 = r3 / "H-002.md"
    sc3.write_text("# H-002\n", encoding="utf-8")
    reg3 = r3 / "reg.json"
    S.sigilla(reg3, "H-002", sc3, ["V-T", "V-S"], ORA)
    subprocess.run(["git", "-C", str(r3), "add", "."], check=True)
    subprocess.run(["git", "-C", str(r3), "commit", "-q", "-m", "solo_sigillo"], check=True)
    # Aggiungo sviluppo (non committato) poi lo falsifico False -> True senza committare
    S.registra_esecuzione(reg3, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": False}, ORA)
    raw3 = json.loads(reg3.read_text(encoding="utf-8"))
    raw3["esecuzioni"][0]["promossa"] = True
    reg3.write_text(json.dumps(raw3, indent=2), encoding="utf-8")
    try:
        S.controlla_ancora(reg3, r3)
        out["voci_non_committate_manomesse"] = "PASSATO"
    except ValueError as e:
        out["voci_non_committate_manomesse"] = f"BLOCCATO:{e}"

    # 4. HEAD staccata su commit precedente (dove verifica non c'era ancora) + cancellazione verifica locale
    r4 = d / "r4"
    _, reg4 = _setup_git_reg(r4)
    c1_sha = subprocess.run(["git", "-C", str(r4), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    S.registra_esecuzione(reg4, "H-002", {"ruolo": "verifica", "variante": "V-T"}, ORA)
    subprocess.run(["git", "-C", str(r4), "add", "reg.json"], check=True)
    subprocess.run(["git", "-C", str(r4), "commit", "-q", "-m", "c2_con_verifica"], check=True)
    subprocess.run(["git", "-C", str(r4), "checkout", "-q", c1_sha], check=True)  # HEAD staccata su c1
    try:
        S.controlla_ancora(reg4, r4)
        out["head_staccata_su_c1_cancella_verifica"] = "PASSATO"
    except ValueError as e:
        out["head_staccata_su_c1_cancella_verifica"] = f"BLOCCATO:{e}"

    # 5. Registro su un altro ramo: checkout ramo `altro` dove verifica non esiste vs ramo `main`
    r5 = d / "r5"
    _, reg5 = _setup_git_reg(r5)
    subprocess.run(["git", "-C", str(r5), "branch", "senza_verifica"], check=True)
    S.registra_esecuzione(reg5, "H-002", {"ruolo": "verifica", "variante": "V-T"}, ORA)
    subprocess.run(["git", "-C", str(r5), "add", "reg.json"], check=True)
    subprocess.run(["git", "-C", str(r5), "commit", "-q", "-m", "con_verifica"], check=True)
    subprocess.run(["git", "-C", str(r5), "checkout", "-q", "senza_verifica"], check=True)
    try:
        S.controlla_ancora(reg5, r5)
        out["registro_altro_ramo"] = "PASSATO"
    except ValueError as e:
        out["registro_altro_ramo"] = f"BLOCCATO:{e}"

    return out


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        print("B-#48:", sonda_b_48_codice_fuori_impronte(base))
        print("B-#49:", sonda_b_49_completezza_sessione(base))
        print("B-#50:", sonda_b_50_calendario_2005_2023())
        print("B-#51:", sonda_b_51_controlla_ancora(base))


if __name__ == "__main__":
    main()
