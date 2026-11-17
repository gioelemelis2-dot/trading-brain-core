#!/usr/bin/env python3
"""MANDATO R14 — Sonde di attacco e verifica (A.0, A, B).

Tutte le sonde girano in cartelle temporanee (tempfile.TemporaryDirectory) su dati inventati
con rete bloccata via HTTPS_PROXY=http://127.0.0.1:9. Non legge brain/dati/reali/ né cache vere.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import lzma
import marshal
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
import zipfile
import zlib
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

RECORD = struct.Struct(">iiiiif")


def verifica_rete_bloccata() -> str:
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
    if not proxy:
        raise RuntimeError("HTTPS_PROXY non impostato")
    try:
        urllib.request.urlopen("https://example.com", timeout=2)
    except Exception as exc:
        msg = f"bloccata ({proxy}): {type(exc).__name__}"
        print(f"[RETE] {msg}")
        return msg
    raise RuntimeError("RETE NON BLOCCATA")


def git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, check=check)


def giorno_bi5(base_p: int, delta: int) -> bytes:
    buf = bytearray()
    minuti = set(range(7 * 60 + 55, 9 * 60 + 11)) | set(range(7 * 60, 16 * 60 + 45, 2))
    for m in sorted(minuti):
        sec = m * 60
        if m < 9 * 60:
            o = c = base_p
            lo, hi = base_p - 2500, base_p + 2500
        elif m == 9 * 60:
            o, c = base_p + 2600, base_p + 3000
            lo, hi = o - 200, c + 200
        elif m == 9 * 60 + 1:
            o, c = base_p + 3000, base_p + delta
            lo, hi = min(o, c) - 200, max(o, c) + 200
        else:
            o = c = base_p + delta
            lo, hi = o - 200, o + 200
        buf += RECORD.pack(sec, o, c, lo, hi, 1.0)
    return lzma.compress(bytes(buf))


def prepara_cache(cache_dir: Path) -> None:
    db, da = cache_dir / "XAUUSD", cache_dir / "XAUUSD_ASK"
    db.mkdir(parents=True, exist_ok=True)
    da.mkdir(parents=True, exist_ok=True)
    bw, bl = cache_dir / ".bw.bi5", cache_dir / ".bl.bi5"
    aw, al = cache_dir / ".aw.bi5", cache_dir / ".al.bi5"
    bw.write_bytes(giorno_bi5(2000000, 12000))
    bl.write_bytes(giorno_bi5(2000000, -7000))
    aw.write_bytes(giorno_bi5(2000050, 12000))
    al.write_bytes(giorno_bi5(2000050, -7000))
    d = date(2005, 1, 1)
    n = 0
    while d <= date(2026, 11, 12):
        win = (n % 3 != 0)
        nome = f"{d.isoformat()}.bi5"
        os.link(bw if win else bl, db / nome)
        os.link(aw if win else al, da / nome)
        n += 1
        d += timedelta(days=1)


def prepara_repo_verificabile(radice_orig: Path, td: Path, cache: Path, nome: str = "repo", extra_prove: int = 0):
    bare = td / f"{nome}_origin.git"
    subprocess.run(["git", "init", "--bare", str(bare)], capture_output=True, text=True, check=True)
    repo = td / nome
    subprocess.run(["git", "clone", "--no-hardlinks", str(radice_orig), str(repo)],
                   capture_output=True, text=True, check=True)
    for pyc in (repo / "brain").rglob("__pycache__"):
        shutil.rmtree(pyc, ignore_errors=True)
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    git(repo, "remote", "set-url", "origin", str(bare))

    sys.path.insert(0, str(repo))
    try:
        from brain.laboratorio.esecuzione import sigillo as S, esegui_h002 as E, caricatore as C
        reg = repo / E.REL_REGISTRO
        codice = E.impronte_codice(repo)
        rob = E.nomi_robustezza()
        if extra_prove > 0:
            sh = repo / "brain/laboratorio/ipotesi/H-001-finta-r14.md"
            sh.write_text("# H-001 finta R14\n", encoding="utf-8")
            S.sigilla(reg, "H-001", sh, [f"V-{i}" for i in range(extra_prove)], "2026-11-16T10:00:00Z", codice, [])
        S.sigilla(reg, "H-002", E.SCHEDA, ["V-T", "V-S"], "2026-11-17T00:00:00Z", codice, rob)
        dati_sha = C.impronta_cache(cache / "XAUUSD", cache / "XAUUSD_ASK", *E.PERIODO_SVILUPPO)
        S.registra_esecuzione(reg, "H-002", {
            "ruolo": "sviluppo", "variante": "V-T",
            "periodo": [E.PERIODO_SVILUPPO[0].isoformat(), E.PERIODO_SVILUPPO[1].isoformat()],
            "cache": str(cache.resolve()), "dati_sha256": dati_sha,
            "n": 700, "r_medio": 0.25, "sharpe": 0.15, "promossa": True,
            "ripetizioni": 2000, "seme": 42, "rapporto_sha256": hashlib.sha256(b"svil").hexdigest(),
        }, "2026-11-17T01:00:00Z")
    finally:
        sys.path.remove(str(repo))
        for m in list(sys.modules):
            if m == "brain" or m.startswith("brain."):
                del sys.modules[m]

    git(repo, "add", "-A")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@invalid", "commit", "-m", f"semina {nome}")
    git(repo, "push", "-u", "origin", branch)
    return repo, bare, branch, reg


def sonda_1_avvio_init_pyc_completo(radice: Path, td: Path, cache: Path) -> None:
    print("\n--- SONDA S1 (#95 / A.0 / B.2): radice/statistics/__init__.pyc senza __init__.py (avvio -> verifica completa) ---")
    repo, _bare, _br, reg = prepara_repo_verificabile(radice, td, cache, nome="s1")
    spia = td / "s1_spia.txt"
    pkg = repo / "statistics"
    pkg.mkdir()
    import statistics as _real_s
    # Avvelena statistics.mean (+99.0) e maschera __file__ come proveniente dalla vera stdlib
    src_s = (
        Path(_real_s.__file__).read_text(encoding="utf-8")
        + "\nimport os as _os95, pathlib as _p95\n"
        + f"_p95.Path({str(spia)!r}).write_text('ESEGUITO_PRIMA_DI_ESEGUI_H002', encoding='utf-8')\n"
        + "__file__ = _os95.path.join(_os95.path.dirname(_os95.__file__), 'statistics.py')\n"
        + "_orig_mean_95 = mean\n"
        + "def mean(d): return _orig_mean_95(d) + 99.0\n"
    )
    code = compile(src_s, str(pkg / "__init__.py"), "exec")
    (pkg / "__init__.pyc").write_bytes(importlib.util.MAGIC_NUMBER + struct.pack("<III", 0, 0, 0) + marshal.dumps(code))

    rap = td / "s1_rapporto.md"
    r = subprocess.run(
        [sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py",
         "--modalita", "verifica", "--varianti", "V-T", "--cache", str(cache),
         "--rapporto", str(rap), "--ora", "2026-11-17T02:00:00Z"],
        cwd=str(repo), capture_output=True, text=True,
    )
    esiti = [e for e in json.loads(reg.read_text(encoding="utf-8"))["esecuzioni"] if e.get("ruolo") == "esito"]
    print(f"rc={r.returncode} spia={spia.exists()} rapporto={rap.exists()} esiti={esiti} stderr={r.stderr.strip()!r}")


def sonda_2_avvio_toctou_corsa(radice: Path, td: Path) -> None:
    print("\n--- SONDA S2 (#95 / A.0): finestra di corsa (TOCTOU) fra controlla() e import in avvio.py ---")
    repo = td / "s2_repo"
    shutil.copytree(radice / "brain", repo / "brain", ignore=shutil.ignore_patterns("__pycache__"))
    reg = repo / "brain/laboratorio/registro_prove.json"
    sys.path.insert(0, str(radice))
    from brain.laboratorio.esecuzione import esegui_h002 as E
    cod = E.impronte_codice(repo)
    sys.path.pop(0)
    reg.write_text(json.dumps({"prove": [], "sigilli": [{"ipotesi": "H-002", "codice": cod}], "esecuzioni": []}))

    crit = repo / "brain/laboratorio/esecuzione/criteri.py"
    orig_bytes = crit.read_bytes()
    spia = td / "s2_spia.txt"
    evil_bytes = (
        orig_bytes.decode("utf-8")
        + f"\nimport pathlib as _p_r; _p_r.Path({str(spia)!r}).write_text('TOCTOU_VINTO')\n"
        + f"_p_r.Path({str(crit)!r}).write_bytes({orig_bytes!r})\n"
    ).encode("utf-8")

    # Misura finestra controlla -> import e prova 15 gare reali con thread parallelo
    vittorie = 0
    tentativi = 15
    t_controlla_ms = []
    sys.path.insert(0, str(repo))
    from brain.laboratorio.esecuzione import avvio as AV
    for _ in range(5):
        t0 = time.perf_counter()
        AV.controlla(str(repo))
        t_controlla_ms.append((time.perf_counter() - t0) * 1000)
    sys.path.pop(0)

    for _ in range(tentativi):
        crit.write_bytes(orig_bytes)
        spia.unlink(missing_ok=True)
        stop = threading.Event()
        def writer():
            # Aspetta meta' del tempo medio di controlla(), poi scrive evil fino a stop
            time.sleep(max(0.001, (sum(t_controlla_ms) / len(t_controlla_ms)) / 1000.0 * 0.8))
            while not stop.is_set():
                crit.write_bytes(evil_bytes)
                time.sleep(0.0002)
        th = threading.Thread(target=writer, daemon=True)
        th.start()
        subprocess.run([sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py", "--help"],
                       cwd=str(repo), capture_output=True, text=True)
        stop.set()
        th.join(timeout=1)
        if spia.exists():
            vittorie += 1
    crit.write_bytes(orig_bytes)
    print(f"tempo_medio_controlla={sum(t_controlla_ms)/len(t_controlla_ms):.2f}ms vittorie_TOCTOU={vittorie}/{tentativi}")


def sonda_3_avvio_env_flags(radice: Path, td: Path) -> None:
    print("\n--- SONDA S3 (#95 / A.0 / #87 / #88 / #94d): env, omit -B, -X pycache_prefix, symlink, TZDIR ---")
    repo = td / "s3_repo"
    shutil.copytree(radice / "brain", repo / "brain", ignore=shutil.ignore_patterns("__pycache__"))
    sys.path.insert(0, str(radice))
    from brain.laboratorio.esecuzione import esegui_h002 as E
    cod = E.impronte_codice(repo)
    sys.path.pop(0)
    (repo / "brain/laboratorio/registro_prove.json").write_text(
        json.dumps({"prove": [], "sigilli": [{"ipotesi": "H-002", "codice": cod}], "esecuzioni": []})
    )
    # 1) Senza -I
    r_noi = subprocess.run([sys.executable, "-s", "-B", "brain/laboratorio/esecuzione/avvio.py", "--help"],
                           cwd=str(repo), capture_output=True, text=True)
    # 2) -X pycache_prefix
    r_pref = subprocess.run([sys.executable, "-I", "-S", "-B", "-X", f"pycache_prefix={td/'pyc'}",
                             "brain/laboratorio/esecuzione/avvio.py", "--help"],
                            cwd=str(repo), capture_output=True, text=True)
    # 3) -I -S senza -B: controlla() di avvio passa, ma import crea __pycache__ -> vediamo se esce con 2 o 0 su --help
    r_nob = subprocess.run([sys.executable, "-I", "-S", "brain/laboratorio/esecuzione/avvio.py", "--help"],
                           cwd=str(repo), capture_output=True, text=True)
    creati = list((repo / "brain").rglob("__pycache__"))
    for p in creati:
        shutil.rmtree(p, ignore_errors=True)
    # 4) .pth, .zip, .so, .py nella cartella di lancio
    esiti_ext = {}
    for ext in (".py", ".pyc", ".so", ".pth", ".zip"):
        f = repo / f"esca{ext}"
        f.write_bytes(b"")
        ro = subprocess.run([sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py", "--help"],
                            cwd=str(repo), capture_output=True, text=True)
        esiti_ext[ext] = ro.returncode
        f.unlink()
    # 5) TZDIR finto per #94d
    tzdir = td / "fake_tz" / "Europe"
    tzdir.mkdir(parents=True)
    # Copia UTC (offset fisso 0 tutto l'anno) come Europe/London
    import zoneinfo
    src_utc = None
    for base in zoneinfo.TZPATH:
        p = Path(base) / "UTC"
        if p.is_file():
            src_utc = p
            break
    tz_err = "no_system_tz"
    if src_utc:
        shutil.copyfile(src_utc, tzdir / "London")
        r_tz = subprocess.run(
            [sys.executable, "-I", "-S", "-B", "-c",
             "import sys; sys.path.insert(0, '.'); from brain.laboratorio.esecuzione.esegui_h002 import controlla_fuso; controlla_fuso()"],
            cwd=str(repo), env=dict(os.environ, TZDIR=str(td / "fake_tz")), capture_output=True, text=True,
        )
        tz_err = f"rc={r_tz.returncode} err={r_tz.stderr.strip().splitlines()[-1] if r_tz.stderr.strip() else ''}"
    print(f"no_I={r_noi.returncode} pycache_prefix={r_pref.returncode} no_B_help_rc={r_nob.returncode}(pycache_creati={len(creati)}) ext_rc={esiti_ext} fake_TZDIR={tz_err}")


def sonda_4_d86_storia_git(radice: Path, td: Path, cache: Path) -> None:
    print("\n--- SONDA S4 (#86, B.1, B.3): 2o registro, nuovo ramo, tag, rewrite+reflog, storia potata --depth 1 ---")
    repo, bare, br, reg = prepara_repo_verificabile(radice, td, cache, nome="s4", extra_prove=4)  # N_prima = 6
    commit_pre = git(repo, "rev-parse", "HEAD").stdout.strip()

    # Esegue 1a verifica ufficiale via avvio.py
    r1 = subprocess.run(
        [sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py",
         "--modalita", "verifica", "--varianti", "V-T", "--cache", str(cache),
         "--rapporto", str(td / "s4_r1.md"), "--ora", "2026-11-17T02:00:00Z"],
        cwd=str(repo), capture_output=True, text=True,
    )
    git(repo, "add", "brain/laboratorio/registro_prove.json")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@invalid", "commit", "-m", "post verifica 1")
    git(repo, "push", "origin", br)
    commit_post = git(repo, "rev-parse", "HEAD").stdout.strip()
    git(repo, "tag", "ver-v1", commit_post)

    # A) Secondo registro: bloccato
    reg2 = repo / "brain/laboratorio/registro_bis.json"
    shutil.copyfile(reg, reg2)
    r_2reg = subprocess.run(
        [sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py",
         "--modalita", "verifica", "--varianti", "V-T", "--registro", str(reg2), "--cache", str(cache),
         "--rapporto", str(td / "s4_2reg.md"), "--ora", "2026-11-17T03:00:00Z"],
        cwd=str(repo), capture_output=True, text=True,
    )

    # B) Nuovo ramo da commit_pre (con storia intera + tag presente): bloccato
    git(repo, "checkout", "-b", "rev/altro", commit_pre)
    git(repo, "push", "-u", "origin", "rev/altro")
    r_ramo = subprocess.run(
        [sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py",
         "--modalita", "verifica", "--varianti", "V-T", "--cache", str(cache),
         "--rapporto", str(td / "s4_ramo.md"), "--ora", "2026-11-17T03:30:00Z"],
        cwd=str(repo), capture_output=True, text=True,
    )

    # Tag che punta al commit post-verifica dopo eliminazione del ramo di verifica (su repo_tag)
    repo_tag = td / "s4_tag"
    subprocess.run(["git", "clone", "--no-hardlinks", str(bare), str(repo_tag)], capture_output=True, check=True)
    for pyc in (repo_tag / "brain").rglob("__pycache__"):
        shutil.rmtree(pyc, ignore_errors=True)
    git(repo_tag, "tag", "ver-v1", commit_post)
    git(repo_tag, "checkout", "-b", "rev/solo-tag", commit_pre)
    for b_del in git(repo_tag, "for-each-ref", "--format=%(refname:short)", "refs/heads/").stdout.split():
        if b_del != "rev/solo-tag":
            git(repo_tag, "branch", "-D", b_del)
    for r_del in git(repo_tag, "for-each-ref", "--format=%(refname)", "refs/remotes/origin/").stdout.split():
        git(repo_tag, "update-ref", "-d", r_del)
    git(repo_tag, "update-ref", "refs/remotes/origin/rev/solo-tag", commit_pre)
    git(repo_tag, "config", "branch.rev/solo-tag.remote", "origin")
    git(repo_tag, "config", "branch.rev/solo-tag.merge", "refs/heads/rev/solo-tag")
    r_tag = subprocess.run(
        [sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py",
         "--modalita", "verifica", "--varianti", "V-T", "--cache", str(cache),
         "--rapporto", str(td / "s4_tag.md"), "--ora", "2026-11-17T03:45:00Z"],
        cwd=str(repo_tag), capture_output=True, text=True,
    )

    # C) Riscrittura locale di refs/remotes/origin/ + eliminazione ramo e tag -> reflog resta su disco ma --all non lo legge
    repo_rew = td / "s4_rew"
    subprocess.run(["git", "clone", "--no-hardlinks", str(bare), str(repo_rew)], capture_output=True, check=True)
    for pyc in (repo_rew / "brain").rglob("__pycache__"):
        shutil.rmtree(pyc, ignore_errors=True)
    git(repo_rew, "checkout", "-b", "rev/riscritta", commit_pre)
    for b_del in git(repo_rew, "for-each-ref", "--format=%(refname:short)", "refs/heads/").stdout.split():
        if b_del != "rev/riscritta":
            git(repo_rew, "branch", "-D", b_del)
    for r_del in git(repo_rew, "for-each-ref", "--format=%(refname)", "refs/remotes/origin/").stdout.split():
        git(repo_rew, "update-ref", "-d", r_del)
    git(repo_rew, "update-ref", "refs/remotes/origin/rev/riscritta", commit_pre)
    git(repo_rew, "config", "branch.rev/riscritta.remote", "origin")
    git(repo_rew, "config", "branch.rev/riscritta.merge", "refs/heads/rev/riscritta")
    r_rew = subprocess.run(
        [sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py",
         "--modalita", "verifica", "--varianti", "V-T", "--cache", str(cache),
         "--rapporto", str(td / "s4_rew.md"), "--ora", "2026-11-17T04:00:00Z"],
        cwd=str(repo_rew), capture_output=True, text=True,
    )

    # D) Storia potata (--depth 1 --single-branch su ramo senza extra_prove -> N scende e verifica si ripete)
    # Rimuove anche extra_prove nel nuovo ramo prima del clone shallow
    git(repo, "checkout", "-b", "rev/n-basso", commit_pre)
    dati_n2 = json.loads(reg.read_text(encoding="utf-8"))
    n_prima = sum(1 for p in dati_n2["prove"] if p["ruolo"] == "selezionabile")
    dati_n2["prove"] = [p for p in dati_n2["prove"] if p["ipotesi"] == "H-002"]
    dati_n2["sigilli"] = [s for s in dati_n2["sigilli"] if s["ipotesi"] == "H-002"]
    reg.write_text(json.dumps(dati_n2, indent=2) + "\n", encoding="utf-8")
    git(repo, "add", "brain/laboratorio/registro_prove.json")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@invalid", "commit", "-m", "ramo n=2")
    git(repo, "push", "-u", "origin", "rev/n-basso")
    repo_sh = td / "s4_shallow"
    subprocess.run(["git", "clone", "--depth", "1", "--branch", "rev/n-basso", "--no-tags",
                    f"file://{bare}", str(repo_sh)],
                   capture_output=True, check=True)
    for pyc in (repo_sh / "brain").rglob("__pycache__"):
        shutil.rmtree(pyc, ignore_errors=True)
    r_sh = subprocess.run(
        [sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py",
         "--modalita", "verifica", "--varianti", "V-T", "--cache", str(cache),
         "--rapporto", str(td / "s4_shallow.md"), "--ora", "2026-11-17T05:00:00Z"],
        cwd=str(repo_sh), capture_output=True, text=True,
    )
    ver_sh = [e for e in json.loads((repo_sh / "brain/laboratorio/registro_prove.json").read_text())["esecuzioni"] if e["ruolo"] == "verifica"]
    n_dopo = ver_sh[-1].get("n_prove") if ver_sh else None
    print(f"r1_rc={r1.returncode} 2reg_rc={r_2reg.returncode} ramo_rc={r_ramo.returncode} tag_rc={r_tag.returncode}({r_tag.stderr.strip()}) rewrite_reflog_rc={r_rew.returncode} shallow_depth1_rc={r_sh.returncode} N_prima={n_prima}->N_dopo={n_dopo}")


def sonda_5_d89_d93_d94(radice: Path, td: Path) -> None:
    print("\n--- SONDA S5 (#89, #90, #93, #94a/c/e): verifiche puntuali ---")
    sys.path.insert(0, str(radice))
    from brain.dati.pipeline import dukascopy as DK
    from brain.laboratorio.esecuzione import riserva as RV, sigillo as S
    from brain.laboratorio.studi import potenza_soglia as PS

    g = date(2024, 1, 2)
    def mk(recs):
        b = bytearray()
        for r in recs:
            b += DK.RECORD.pack(*r)
        return lzma.compress(bytes(b))

    # #89: secondi non %60 e duplicato (anche con volume 0)
    ok_non60 = ok_dup = ok_desc = None
    try:
        DK.decodifica(mk([(601, 2000000, 2000100, 1999900, 2000200, 1.0)]), g, 3)
        ok_non60 = "ACCETTATO"
    except DK.ErroreDati as e:
        ok_non60 = f"RIFIUTATO({e})"
    try:
        DK.decodifica(mk([(600, 2000000, 2000100, 1999900, 2000200, 0.0),
                          (600, 2000000, 2000200, 1999900, 2000300, 1.0)]), g, 3)
        ok_dup = "ACCETTATO"
    except DK.ErroreDati as e:
        ok_dup = f"RIFIUTATO({e})"
    # Ordine decrescente
    try:
        DK.decodifica(mk([(1200, 2000000, 2000100, 1999900, 2000200, 1.0),
                          (600, 2000000, 2000100, 1999900, 2000200, 1.0)]), g, 3)
        ok_desc = "ACCETTATO"
    except DK.ErroreDati as e:
        ok_desc = f"RIFIUTATO({e})"

    # #93 e #94a: testa manomessa e j=True/1.0
    reg_ris = td / "ris_finta.json"
    reg_ris.write_text(json.dumps({
        "schema": "riserva/1",
        "riserva": {"inizio": "2005-01-01", "fine": "2023-10-31", "alfa_tot": 5.0, "protetta": None},
        "eventi": [],
    }))
    try:
        RV.stato(reg_ris)
        r93 = "ACCETTATO"
    except ValueError as e:
        r93 = f"RIFIUTATO({e})"

    reg_j = td / "ris_j.json"
    RV.crea(reg_j, date(2005, 1, 1), date(2023, 10, 31), 0.05, "2026-11-17T00:00:00Z")
    RV.prenota(reg_j, "id1", "H-002", date(2005, 1, 1), date(2005, 12, 31), "h", "2026-11-17T00:00:00Z")
    dati_j = json.loads(reg_j.read_text())
    dati_j["eventi"].append({"tipo": "autorizzazione", "id": "id1", "j": True, "n_globale": 2,
                             "hash_dati": "abc", "m": 1, "alfa_j": 0.025, "ora": "2026-11-17T00:00:00Z"})
    reg_j.write_text(json.dumps(dati_j))
    try:
        RV.stato(reg_j)
        r94a = "ACCETTATO"
    except ValueError as e:
        r94a = f"RIFIUTATO({e})"

    # #94e: dominio simula vs n_per_potenza con sigma <= 0 quando mu <= soglia
    try:
        PS.simula(2.0, 1.5, 50, 0.15, "stima")
        r94e_sim = "ACCETTATO"
    except ValueError as e:
        r94e_sim = f"RIFIUTATO({e})"
    n_neg_sig = PS.n_per_potenza(-0.1, -5.0, 0.15, 0.8, "stima")

    print(f"d89_non60={ok_non60} | d89_dup={ok_dup} | d89_desc={ok_desc}")
    print(f"d93={r93} | d94a_j_bool={r94a} | d94e_simula={r94e_sim} | n_per_potenza_neg_sigma={n_neg_sig!r}")
    sys.path.remove(str(radice))


def sonda_6_esporta_e_riconta(radice: Path, td: Path) -> None:
    print("\n--- SONDA S6 (#72-#84 / B.4): esporta_redatto e riconta su dati inventati ---")
    sys.path.insert(0, str(radice))
    from brain.governance import esporta_redatto as ER
    from brain.governance.censimento import riconta as RC

    grepo = td / "s6_grepo"
    grepo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=str(grepo), check=True)
    subprocess.run(["git", "-C", str(grepo), "config", "user.name", "T"], check=True)
    subprocess.run(["git", "-C", str(grepo), "config", "user.email", "t@invalid"], check=True)
    (grepo / "note_u16.bin").write_bytes("Cartella privata: /Users/alice_inventata/segreto.txt\n".encode("utf-16-le"))
    zb = io.BytesIO()
    with zipfile.ZipFile(zb, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("segreto.txt", "Titolare: Mario Rossi\n")
    (grepo / "finto.dat").write_bytes(b"PREF" + zb.getvalue())
    (grepo / "dati.zlib").write_bytes(zlib.compress(b"Titolare: Mario Rossi\n"))
    subprocess.run(["git", "-C", str(grepo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(grepo), "commit", "-q", "-m", "init"], check=True)

    # 1) UTF-16LE /Users/alice_inventata (non passato in --sostituisci)
    out1 = td / "s6_u16.zip"
    res1 = ER.esporta(grepo, "HEAD", out1, [("Mario Rossi", "<titolare>")], escludi=["finto.dat", "dati.zlib"])
    with zipfile.ZipFile(out1) as z:
        leaked_u16 = z.read("note_u16.bin").decode("utf-16-le")

    # 2) ZIP DEFLATED con prefisso 4 byte + stream zlib con "Mario Rossi" dato in --sostituisci
    out2 = td / "s6_arch.zip"
    res2 = ER.esporta(grepo, "HEAD", out2, [("Mario Rossi", "<titolare>")], escludi=["note_u16.bin"])
    with zipfile.ZipFile(out2) as z:
        inner = zipfile.ZipFile(io.BytesIO(z.read("finto.dat")[4:])).read("segreto.txt").decode("utf-8")
        unz = zlib.decompress(z.read("dati.zlib")).decode("utf-8")

    # 3) riconta edge cases
    d_under = RC.date_riserva("file_1434326400.csv")
    d_lett = RC.date_riserva("XAU1434326400000")
    d_ok = RC.date_riserva("XAUUSD_20150615.csv")
    sys.path.remove(str(radice))

    print(f"UTF16_/Users_passato={res1} contenuto={leaked_u16.strip()!r}")
    print(f"ZIP_PREF+ZLIB_passato={res2} zip_inner={inner.strip()!r} zlib_inner={unz.strip()!r}")
    print(f"riconta_ts_underscore={d_under} riconta_ts_lettere={d_lett} riconta_compact_ok={d_ok}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", type=Path, default=Path(__file__).resolve().parents[3])
    args = ap.parse_args()
    radice = args.radice.resolve()

    verifica_rete_bloccata()
    with tempfile.TemporaryDirectory(prefix="r14_sonde_") as td_str:
        td = Path(td_str)
        cache = td / "cache_finta"
        prepara_cache(cache)

        sonda_1_avvio_init_pyc_completo(radice, td, cache)
        sonda_2_avvio_toctou_corsa(radice, td)
        sonda_3_avvio_env_flags(radice, td)
        sonda_4_d86_storia_git(radice, td, cache)
        sonda_5_d89_d93_d94(radice, td)
        sonda_6_esporta_e_riconta(radice, td)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
