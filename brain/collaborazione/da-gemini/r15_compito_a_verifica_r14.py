#!/usr/bin/env python3
"""MANDATO R15 (Compito A) — Verifica rilievi BANCO-02 e R14 (#86-#104) adattati al registro canonico.

Verifica:
- Tutti gli attacchi BANCO-02 (#86-#91) ed R14 (#96-#104) sul registro canonico `brain/laboratorio/registro_prove.json`
  e lanciatore `brain/laboratorio/esecuzione/avvio.py`: stampa «ATTACCO RESPINTO» per ogni controllo chiuso.
- Mutanti N68, N69 (su copia temporanea contro TestAvvioR14) e X25, X26, X27 (contro test_esporta_redatto).
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
import time
import urllib.request
import zipfile
import zlib
from datetime import date, timedelta
from pathlib import Path

RECORD = struct.Struct(">iiiiif")


def verifica_rete_bloccata() -> None:
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
    if not proxy:
        raise RuntimeError("HTTPS_PROXY non impostato")
    try:
        urllib.request.urlopen("https://example.com", timeout=2)
    except Exception as exc:
        print(f"[RETE] bloccata ({proxy}): {type(exc).__name__}")
        return
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


def clona_e_sigilla(radice_orig: Path, td: Path, cache: Path, nome: str, extra_prove: int = 0):
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
            sh = repo / "brain/laboratorio/ipotesi/H-001-finta-r15.md"
            sh.write_text("# H-001 finta R15\n", encoding="utf-8")
            S.sigilla(reg, "H-001", sh, [f"V-{i}" for i in range(extra_prove)], "2026-11-16T10:00:00Z", codice, [])
        S.sigilla(reg, "H-002", E.SCHEDA, ["V-T", "V-S"], "2026-11-17T00:00:00Z", codice, rob)
        dati_sha = C.impronta_cache(cache / "XAUUSD", cache / "XAUUSD_ASK", *E.PERIODO_SVILUPPO)
        S.registra_esecuzione(reg, "H-002", {
            "ruolo": "sviluppo", "variante": "V-T",
            "periodo": [E.PERIODO_SVILUPPO[0].isoformat(), E.PERIODO_SVILUPPO[1].isoformat()],
            "cache": str(cache.resolve()), "dati_sha256": dati_sha,
            "n": 700, "r_medio": 0.25, "sharpe": 0.15, "promossa": True,
            "ripetizioni": 1000, "seme": 42, "rapporto_sha256": hashlib.sha256(b"svil").hexdigest(),
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


def run_avvio(repo: Path, args_cli: list, env_extra: dict = None) -> subprocess.CompletedProcess:
    env = dict(os.environ, **(env_extra or {}))
    return subprocess.run(
        [sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py", *args_cli],
        cwd=str(repo), capture_output=True, text=True, env=env,
    )


def verifica_attacchi(radice: Path, td: Path, cache: Path) -> None:
    print("\n=== PARTE 1: Rilancio BANCO-02 & Sonde R14 su registro canonico + avvio.py ===")

    # 1) #86 (A: 2o registro; B: nuovo ramo; #98a: depth 1; #98b: update-ref + reflog)
    repo, bare, br, reg = clona_e_sigilla(radice, td, cache, "a86", extra_prove=4)
    commit_pre = git(repo, "rev-parse", "HEAD").stdout.strip()
    r1 = run_avvio(repo, ["--modalita", "verifica", "--varianti", "V-T", "--cache", str(cache),
                          "--rapporto", str(td / "r86_1.md"), "--ora", "2026-11-17T02:00:00Z"])
    assert r1.returncode == 0, r1.stderr
    git(repo, "add", "brain/laboratorio/registro_prove.json")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@invalid", "commit", "-m", "post ver 1")
    git(repo, "push", "origin", br)

    reg_alt = repo / "brain/laboratorio/registro_alt.json"
    shutil.copyfile(reg, reg_alt)
    git(repo, "add", "brain/laboratorio/registro_alt.json")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@invalid", "commit", "-m", "alt")
    git(repo, "push", "origin", br)
    r_2reg = run_avvio(repo, ["--modalita", "verifica", "--varianti", "V-T", "--registro", str(reg_alt),
                              "--cache", str(cache), "--rapporto", str(td / "r86_2reg.md"), "--ora", "2026-11-17T02:10:00Z"])
    print(f"[#86a 2o registro] rc={r_2reg.returncode} -> {'ATTACCO RESPINTO' if r_2reg.returncode != 0 else 'ATTACCO RIUSCITO'}")

    git(repo, "checkout", "-b", "rev/altro", commit_pre)
    git(repo, "push", "-u", "origin", "rev/altro")
    r_ramo = run_avvio(repo, ["--modalita", "verifica", "--varianti", "V-T", "--cache", str(cache),
                              "--rapporto", str(td / "r86_ramo.md"), "--ora", "2026-11-17T02:20:00Z"])
    print(f"[#86b ramo nuovo] rc={r_ramo.returncode} -> {'ATTACCO RESPINTO' if r_ramo.returncode != 0 else 'ATTACCO RIUSCITO'}")

    # #98a: clone --depth 1
    repo_sh = td / "a86_sh"
    subprocess.run(["git", "clone", "--depth", "1", "--branch", "rev/altro", "--no-tags", f"file://{bare}", str(repo_sh)],
                   capture_output=True, check=True)
    for pyc in (repo_sh / "brain").rglob("__pycache__"):
        shutil.rmtree(pyc, ignore_errors=True)
    r_sh = run_avvio(repo_sh, ["--modalita", "verifica", "--varianti", "V-T", "--cache", str(cache),
                               "--rapporto", str(td / "r86_sh.md"), "--ora", "2026-11-17T02:30:00Z"])
    print(f"[#98a storia parziale --depth 1] rc={r_sh.returncode} err={r_sh.stderr.strip()!r} -> {'ATTACCO RESPINTO' if r_sh.returncode != 0 else 'ATTACCO RIUSCITO'}")

    # #98b: riscrittura locale + branch -D lasciando il reflog su disco
    repo_ref = td / "a86_reflog"
    shutil.copytree(repo, repo_ref)
    for pyc in (repo_ref / "brain").rglob("__pycache__"):
        shutil.rmtree(pyc, ignore_errors=True)
    git(repo_ref, "checkout", "-b", "rev/riscritta", commit_pre)
    for b_del in git(repo_ref, "for-each-ref", "--format=%(refname:short)", "refs/heads/").stdout.split():
        if b_del != "rev/riscritta":
            git(repo_ref, "branch", "-D", b_del)
    for r_del in git(repo_ref, "for-each-ref", "--format=%(refname)", "refs/remotes/origin/").stdout.split():
        git(repo_ref, "update-ref", "-d", r_del)
    git(repo_ref, "update-ref", "refs/remotes/origin/rev/riscritta", commit_pre)
    git(repo_ref, "config", "branch.rev/riscritta.remote", "origin")
    git(repo_ref, "config", "branch.rev/riscritta.merge", "refs/heads/rev/riscritta")
    r_reflog = run_avvio(repo_ref, ["--modalita", "verifica", "--varianti", "V-T", "--cache", str(cache),
                                    "--rapporto", str(td / "r86_reflog.md"), "--ora", "2026-11-17T02:40:00Z"])
    print(f"[#98b reflog] rc={r_reflog.returncode} err={r_reflog.stderr.strip()!r} -> {'ATTACCO RESPINTO' if r_reflog.returncode != 0 else 'ATTACCO RIUSCITO'}")

    # 2) #87 (__pycache__/criteri.<tag>.pyc), #88 (sysconfig.py CWD), #96 (RADICE/statistics/__init__.pyc)
    repo2, _b2, _br2, _reg2 = clona_e_sigilla(radice, td, cache, "a87")
    crit = repo2 / "brain/laboratorio/esecuzione/criteri.py"
    st = crit.stat()
    spia87 = td / "spia87.txt"
    pyc_dir = crit.parent / "__pycache__"
    pyc_dir.mkdir(exist_ok=True)
    pyc_file = pyc_dir / f"criteri.{sys.implementation.cache_tag}.pyc"
    code87 = compile(crit.read_text(encoding="utf-8") + f"\nimport pathlib; pathlib.Path({str(spia87)!r}).write_text('X')\n",
                     str(crit), "exec")
    pyc_file.write_bytes(importlib.util.MAGIC_NUMBER + struct.pack("<III", 0, int(st.st_mtime) & 0xFFFFFFFF, st.st_size & 0xFFFFFFFF) + marshal.dumps(code87))
    r87 = run_avvio(repo2, ["--modalita", "verifica", "--varianti", "V-T", "--cache", str(cache),
                            "--rapporto", str(td / "r87.md"), "--ora", "2026-11-17T02:00:00Z"])
    shutil.rmtree(pyc_dir)
    print(f"[#87 __pycache__ .pyc] rc={r87.returncode} spia={spia87.exists()} -> {'ATTACCO RESPINTO' if (r87.returncode != 0 and not spia87.exists()) else 'ATTACCO RIUSCITO'}")

    spia88 = td / "spia88.txt"
    (repo2 / "sysconfig.py").write_text(f"import pathlib; pathlib.Path({str(spia88)!r}).write_text('X')\n", encoding="utf-8")
    r88 = run_avvio(repo2, ["--modalita", "verifica", "--varianti", "V-T", "--cache", str(cache),
                            "--rapporto", str(td / "r88.md"), "--ora", "2026-11-17T02:00:00Z"])
    (repo2 / "sysconfig.py").unlink()
    print(f"[#88 sysconfig.py CWD] rc={r88.returncode} spia={spia88.exists()} -> {'ATTACCO RESPINTO' if (r88.returncode != 0 and not spia88.exists()) else 'ATTACCO RIUSCITO'}")

    spia96 = td / "spia96.txt"
    st_dir = repo2 / "statistics"
    st_dir.mkdir()
    import statistics as _rs
    src_s = Path(_rs.__file__).read_text(encoding="utf-8") + f"\nimport pathlib; pathlib.Path({str(spia96)!r}).write_text('X')\n"
    (st_dir / "__init__.pyc").write_bytes(importlib.util.MAGIC_NUMBER + struct.pack("<III", 0, 0, 0) + marshal.dumps(compile(src_s, "statistics", "exec")))
    r96 = run_avvio(repo2, ["--modalita", "verifica", "--varianti", "V-T", "--cache", str(cache),
                            "--rapporto", str(td / "r96.md"), "--ora", "2026-11-17T02:00:00Z"])
    shutil.rmtree(st_dir)
    print(f"[#96 statistics/__init__.pyc] rc={r96.returncode} spia={spia96.exists()} -> {'ATTACCO RESPINTO' if (r96.returncode != 0 and not spia96.exists()) else 'ATTACCO RIUSCITO'}")

    # 3) #89, #90 (esiti multipli / senza verifica), #91 (esito prima del controllo/rapporto)
    sys.path.insert(0, str(radice))
    from brain.dati.pipeline import dukascopy as DK
    from brain.laboratorio.esecuzione import sigillo as S
    from brain.laboratorio.studi import potenza_soglia as PS
    from brain.governance import esporta_redatto as ER
    from brain.governance.censimento import riconta as RC
    sys.path.remove(str(radice))

    b_non60 = lzma.compress(DK.RECORD.pack(601, 2000000, 2000100, 1999900, 2000200, 1.0))
    b_dup = lzma.compress(DK.RECORD.pack(600, 2000000, 2000100, 1999900, 2000200, 1.0) +
                          DK.RECORD.pack(600, 2000000, 2000200, 1999900, 2000300, 1.0))
    r89_1 = r89_2 = False
    try:
        DK.decodifica(b_non60, date(2024, 1, 2), 3)
    except DK.ErroreDati:
        r89_1 = True
    try:
        DK.decodifica(b_dup, date(2024, 1, 2), 3)
    except DK.ErroreDati:
        r89_2 = True
    print(f"[#89 bi5 non allineato/dup] rifiutati={r89_1 and r89_2} -> {'ATTACCO RESPINTO' if (r89_1 and r89_2) else 'ATTACCO RIUSCITO'}")

    reg90 = td / "reg90.json"
    sh90 = td / "s90.md"
    sh90.write_text("# s\n")
    S.sigilla(reg90, "H-002", sh90, ["V-T", "V-S"], "2026-11-17T00:00:00Z")
    r90_senza = r90_dup = False
    try:
        S.registra_esecuzione(reg90, "H-002", {"ruolo": "esito", "variante": "V-T", "promossa": True}, "2026-11-17T01:00:00Z")
    except ValueError:
        r90_senza = True
    S.registra_esecuzione(reg90, "H-002", {"ruolo": "verifica", "variante": "V-T", "n_prove": 2}, "2026-11-17T01:01:00Z")
    S.registra_esecuzione(reg90, "H-002", {"ruolo": "esito", "variante": "V-T", "promossa": False}, "2026-11-17T01:02:00Z")
    try:
        S.registra_esecuzione(reg90, "H-002", {"ruolo": "esito", "variante": "V-T", "promossa": True}, "2026-11-17T01:03:00Z")
    except ValueError:
        r90_dup = True
    print(f"[#90 esiti senza verifica / multipli] bloccati={r90_senza and r90_dup} -> {'ATTACCO RESPINTO' if (r90_senza and r90_dup) else 'ATTACCO RIUSCITO'}")

    # #91: manomissione criteri.py dopo "verifica" scritta nel registro -> controlla_ambiente prima di esito!
    repo91, _b91, _br91, reg91 = clona_e_sigilla(radice, td, cache, "a91")
    rap91 = td / "r91.md"
    proc = subprocess.Popen(
        [sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py",
         "--modalita", "verifica", "--varianti", "V-T", "--cache", str(cache),
         "--rapporto", str(rap91), "--ora", "2026-11-17T02:00:00Z"],
        cwd=str(repo91), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    t0 = time.monotonic()
    mod = False
    crit91 = repo91 / "brain/laboratorio/esecuzione/criteri.py"
    while proc.poll() is None:
        if not mod:
            try:
                if any(e.get("ruolo") == "verifica" for e in json.loads(reg91.read_text()).get("esecuzioni", [])):
                    crit91.write_text(crit91.read_text() + "\n# tamper #91\n", encoding="utf-8")
                    mod = True
                    break
            except Exception:
                pass
        if time.monotonic() - t0 > 90:
            break
        time.sleep(0.01)
    proc.communicate(timeout=120)
    esiti91 = [e for e in json.loads(reg91.read_text())["esecuzioni"] if e.get("ruolo") == "esito"]
    print(f"[#91 esito prima controllo finale] mod={mod} rc={proc.returncode} esiti={len(esiti91)} rap={rap91.exists()} -> {'ATTACCO RESPINTO' if (proc.returncode != 0 and not esiti91 and not rap91.exists()) else 'ATTACCO RIUSCITO'}")

    # 4) #99, #100 (esporta_redatto), #101 (potenza_soglia), #102 (riconta)
    grepo = td / "grepo"
    grepo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=str(grepo), check=True)
    subprocess.run(["git", "-C", str(grepo), "config", "user.name", "T"], check=True)
    subprocess.run(["git", "-C", str(grepo), "config", "user.email", "t@invalid"], check=True)
    (grepo / "u16.txt").write_bytes("/Users/alice_inventata/segreto.txt\n".encode("utf-16-le"))
    zb = io.BytesIO()
    with zipfile.ZipFile(zb, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("s.txt", "Autore: Mario Rossi\n")
    (grepo / "pref.dat").write_bytes(b"PREF" + zb.getvalue())
    (grepo / "raw.zlib").write_bytes(zlib.compress(b"Autore: Mario Rossi\n"))
    subprocess.run(["git", "-C", str(grepo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(grepo), "commit", "-q", "-m", "init"], check=True)

    r99 = r100a = r100b = False
    try:
        ER.esporta(grepo, "HEAD", td / "out99.zip", [("Mario Rossi", "<titolare>")], escludi=["pref.dat", "raw.zlib"])
    except ValueError:
        r99 = True
    try:
        ER.esporta(grepo, "HEAD", td / "out100a.zip", [("Mario Rossi", "<titolare>")], escludi=["u16.txt", "raw.zlib"])
    except ValueError:
        r100a = True
    try:
        ER.esporta(grepo, "HEAD", td / "out100b.zip", [("Mario Rossi", "<titolare>")], escludi=["u16.txt", "pref.dat"])
    except ValueError:
        r100b = True
    print(f"[#99 UTF-16 /Users & #100 PREF+ZIP / zlib] bloccati={r99 and r100a and r100b} -> {'ATTACCO RESPINTO' if (r99 and r100a and r100b) else 'ATTACCO RIUSCITO'}")

    r101 = False
    try:
        PS.n_per_potenza(-0.1, -5.0, 0.15, 0.8, "stima")
    except ValueError:
        r101 = True
    print(f"[#101 n_per_potenza sigma<=0] bloccato={r101} -> {'ATTACCO RESPINTO' if r101 else 'ATTACCO RIUSCITO'}")

    d_u = RC.date_riserva("file_1434326400.csv")
    d_l = RC.date_riserva("XAU1434326400000")
    d_hex = RC.date_riserva("a" * 16 + "1434326400")
    r102 = (d_u == ["2015-06-15"] and d_l == ["2015-06-15"] and d_hex == [])
    print(f"[#102 riconta ts_lettere/underscore vs hex] {d_u} {d_l} hex={d_hex} -> {'ATTACCO RESPINTO' if r102 else 'ATTACCO RIUSCITO'}")


def verifica_mutanti_r14(radice: Path, td: Path) -> None:
    print("\n=== PARTE 2: Verifica mutanti N68, N69 e X25–X27 ===")
    # N68, N69 su TestAvvioR14 (escluso test_senza_meno_b già rosso su Apple Python 3.9 per -I=>dont_write_bytecode)
    suite_avvio = [
        "brain.laboratorio.tests.test_esegui_h002.TestAvvioR14.test_cartella_importabile_con_solo_init_pyc_rifiutata",
        "brain.laboratorio.tests.test_esegui_h002.TestAvvioR14.test_cartelle_non_importabili_ammesse",
        "brain.laboratorio.tests.test_esegui_h002.TestAvvioR14.test_archivi_nella_radice_rifiutati",
        "brain.laboratorio.tests.test_esegui_h002.TestAvvioR14.test_senza_meno_i_si_ferma",
    ]
    # N69 verifica direttamente la riga `-X pycache_prefix` di TestAvvioR14 senza la sub-asserzione -B
    casi = [
        ("N68", "brain/laboratorio/esecuzione/avvio.py",
         'IMPORTABILI = (".py", ".pyc", ".pyo", ".so", ".pyd", ".pth", ".zip", ".egg", ".whl")',
         'IMPORTABILI = (".py", ".pyc", ".pyo", ".so", ".pyd", ".pth")',
         suite_avvio),
        ("N69", "brain/laboratorio/esecuzione/avvio.py",
         '    if getattr(sys, "pycache_prefix", None):\n        problemi.append("eseguire senza -X pycache_prefix")',
         '    if False:\n        problemi.append("eseguire senza -X pycache_prefix")',
         ["brain.laboratorio.tests.test_esegui_h002.TestAvvioControllato.test_copia_pulita_arriva_alla_riga_di_comando",
          "brain.laboratorio.tests.test_esegui_h002.TestAvvioR14.test_archivi_nella_radice_rifiutati"]),
        ("X25", "brain/governance/esporta_redatto.py",
         '            except UnicodeDecodeError:                                # R14-04, R14-05: niente binari\n                non_testo.append(m.name)\n                continue',
         '            except UnicodeDecodeError:\n                file.append((m.name, dati, _sha(dati)))\n                continue',
         ["brain.governance.test_esporta_redatto"]),
        ("X26", "brain/governance/esporta_redatto.py",
         'PERCORSI_MAC_BYTE.search(d.replace(b"\\0", b""))',
         'PERCORSI_MAC_BYTE.search(d)',
         ["brain.governance.test_esporta_redatto"]),
        ("X27", "brain/governance/esporta_redatto.py",
         '    if non_testo:\n        raise ValueError(f"file che non è testo UTF-8, non controllabili (archivi, binari, altre codifiche): "\n                         f"{non_testo[:20]}; escluderli con --escludi (l\'esclusione è dichiarata nel pacchetto)")',
         '    if False:\n        pass',
         ["brain.governance.test_esporta_redatto"]),
    ]
    # Verifica N69 con micro-test inline sull'effettivo blocco -X pycache_prefix nel processo figlio
    for mid, rel, old, new, suite in casi:
        copia = td / f"mut_{mid}"
        shutil.copytree(radice / "brain", copia / "brain", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        f = copia / rel
        t = f.read_text(encoding="utf-8")
        assert old in t, f"{mid}: pattern assente in {rel}"
        f.write_text(t.replace(old, new, 1), encoding="utf-8")
        if mid == "N69":
            # Registra un sigillo minimo e lancia avvio.py con -X pycache_prefix come fa TestAvvioR14 riga 1095
            (copia / "brain/laboratorio/registro_prove.json").write_text(json.dumps({"prove": [], "sigilli": [{"ipotesi": "H-002", "codice": {"brain/laboratorio/esecuzione/avvio.py": "0"}}], "esecuzioni": []}))
            r = subprocess.run([sys.executable, "-I", "-S", "-B", "-X", f"pycache_prefix={td/'xpyc'}",
                                "brain/laboratorio/esecuzione/avvio.py", "--help"], cwd=str(copia), capture_output=True, text=True)
            killed = ("pycache_prefix" not in r.stderr and r.returncode == 0)
            # Invertiamo: per N69 verifico se il test ufficiale fallirebbe se la riga 1091 fosse senza -B check:
            # eseguiamo controlla() di avvio.py mutato vs non mutato con -X pycache_prefix!
            out_mut = subprocess.run([sys.executable, "-I", "-S", "-B", "-X", f"pycache_prefix={td/'xpyc'}", "-c",
                                      "import sys; sys.path.insert(0, '.'); from brain.laboratorio.esecuzione import avvio; print(avvio.controlla('.'))"],
                                     cwd=str(copia), capture_output=True, text=True)
            out_ok = subprocess.run([sys.executable, "-I", "-S", "-B", "-X", f"pycache_prefix={td/'xpyc'}", "-c",
                                     "import sys; sys.path.insert(0, '.'); from brain.laboratorio.esecuzione import avvio; print(avvio.controlla('.'))"],
                                    cwd=str(radice), capture_output=True, text=True)
            print(f"[N69 verifica logica -X pycache_prefix] orig_ha_errore={'pycache_prefix' in out_ok.stdout} mut_senza_errore={'pycache_prefix' not in out_mut.stdout} (nota: in unittest Apple 3.9 TestAvvioR14 riga 1093 fallisce prima su -B)")
        else:
            r = subprocess.run([sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", *suite],
                               cwd=str(copia), capture_output=True, text=True)
            stato = "UCCISO" if r.returncode != 0 else "SOPRAVVISSUTO"
            print(f"[{stato}] {mid} (rc={r.returncode})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", type=Path, default=Path(__file__).resolve().parents[3])
    args = ap.parse_args()
    radice = args.radice.resolve()

    verifica_rete_bloccata()
    with tempfile.TemporaryDirectory(prefix="r15_compito_a_") as td_str:
        td = Path(td_str)
        cache = td / "cache_finta"
        prepara_cache(cache)
        verifica_attacchi(radice, td, cache)
        verifica_mutanti_r14(radice, td)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
