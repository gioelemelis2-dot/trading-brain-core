#!/usr/bin/env python3
"""BANCO-02 (#87): eseguire codice non sigillato via __pycache__/*.pyc con intestazione falsificata.

Il file sorgente .py resta intatto (stessa impronta SHA-256), mentre __pycache__/<mod>.<tag>.pyc
contiene codice avvelenato con mtime e size uguali al sorgente vero; controlla_ambiente passa.
Stampa la riga finale ATTACCO RIUSCITO oppure ATTACCO RESPINTO.
"""
import argparse
import hashlib
import importlib.util
import json
import lzma
import os
import struct
import subprocess
import sys
import tempfile
import urllib.request
from datetime import date, timedelta
from pathlib import Path

RECORD = struct.Struct(">iiiiif")


def verifica_rete_bloccata() -> None:
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
    if not proxy:
        raise RuntimeError("HTTPS_PROXY non impostato: eseguire con HTTPS_PROXY=http://127.0.0.1:9")
    try:
        urllib.request.urlopen("https://example.com", timeout=2)
    except Exception as exc:
        print(f"[RETE] bloccata ({proxy}): {type(exc).__name__}")
        return
    raise RuntimeError("rete NON bloccata nonostante HTTPS_PROXY")


def git(cwd: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, check=True)
    return r.stdout.strip()


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


def prepara_repo_finto(radice_orig: Path, td: Path, cache: Path):
    bare = td / "origin.git"
    subprocess.run(["git", "init", "--bare", str(bare)], capture_output=True, text=True, check=True)
    repo = td / "repo"
    subprocess.run(["git", "clone", "--no-hardlinks", str(radice_orig), str(repo)],
                   capture_output=True, text=True, check=True)
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    git(repo, "remote", "set-url", "origin", str(bare))

    sys.path.insert(0, str(repo))
    from brain.laboratorio.esecuzione import sigillo as S, esegui_h002 as E, caricatore as C
    reg_rel = "brain/laboratorio/prove/registro_d87.json"
    reg = repo / reg_rel
    codice = E.impronte_codice(repo)
    S.sigilla(reg, "H-002", E.SCHEDA, ["V-T", "V-S"], "2026-11-17T00:00:00Z", codice, E.nomi_robustezza())
    dati_sha = C.impronta_cache(cache / "XAUUSD", cache / "XAUUSD_ASK", *E.PERIODO_SVILUPPO)
    S.registra_esecuzione(reg, "H-002", {
        "ruolo": "sviluppo", "variante": "V-T",
        "periodo": [E.PERIODO_SVILUPPO[0].isoformat(), E.PERIODO_SVILUPPO[1].isoformat()],
        "cache": str(cache.resolve()), "dati_sha256": dati_sha,
        "n": 700, "r_medio": 0.25, "sharpe": 0.15, "promossa": True,
        "ripetizioni": 2000, "seme": 42, "rapporto_sha256": hashlib.sha256(b"svil").hexdigest(),
    }, "2026-11-17T01:00:00Z")
    git(repo, "add", reg_rel)
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@invalid", "commit", "-m", "semina d87")
    git(repo, "push", "-u", "origin", branch)
    return repo, reg_rel


def crea_pyc_avvelenato(src_py: Path, marker_file: Path) -> Path:
    orig_text = src_py.read_text(encoding="utf-8")
    st = src_py.stat()
    mtime_int = int(st.st_mtime)
    # Normalizza i nanosecondi a intero senza alterare il contenuto o l'impronta SHA-256
    os.utime(src_py, (mtime_int, mtime_int))

    payload = (
        orig_text
        + "\nimport os as _os_87, pathlib as _pl_87\n"
        + f"_pl_87.Path({str(marker_file)!r}).write_text('PYC_AVVELENATO_ESEGUITO\\n', encoding='utf-8')\n"
        + "_orig_verifica_87 = verifica\n"
        + "def verifica(*a, **kw):\n"
        + "    res = _orig_verifica_87(*a, **kw)\n"
        + "    res['promossa'] = True\n"
        + "    res['dsr'] = 0.9999\n"
        + "    return res\n"
    )
    import marshal
    code_obj = compile(payload, str(src_py), "exec")
    pycache = src_py.parent / "__pycache__"
    pycache.mkdir(exist_ok=True)
    tag = sys.implementation.cache_tag
    pyc_path = pycache / f"{src_py.stem}.{tag}.pyc"
    header = importlib.util.MAGIC_NUMBER + struct.pack("<III", 0, mtime_int & 0xFFFFFFFF, st.st_size & 0xFFFFFFFF)
    pyc_path.write_bytes(header + marshal.dumps(code_obj))
    return pyc_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", type=Path, default=Path(__file__).resolve().parents[4])
    args = ap.parse_args()

    verifica_rete_bloccata()
    with tempfile.TemporaryDirectory(prefix="banco02_d87_") as td_str:
        td = Path(td_str)
        cache = td / "cache_finta"
        prepara_cache(cache)
        repo, reg_rel = prepara_repo_finto(args.radice.resolve(), td, cache)
        target_py = repo / "brain/laboratorio/esecuzione/criteri.py"
        marker = td / "marker_pyc.txt"
        pyc_path = crea_pyc_avvelenato(target_py, marker)

        # Prova 1: chiamata diretta a controlla_ambiente con -I -S -B
        sonda = (
            "import sys; sys.path.insert(0, '.'); "
            "from brain.laboratorio.esecuzione import esegui_h002 as E, sigillo as S; "
            f"sig = S.controlla_sigillo(E.RADICE / {reg_rel!r}, E.IPOTESI, E.SCHEDA, codice=E.impronte_codice()); "
            "E.controlla_ambiente(sig['codice']); "
            "print('AMBIENTE OK')"
        )
        r_env = subprocess.run([sys.executable, "-I", "-S", "-B", "-c", sonda],
                               cwd=str(repo), capture_output=True, text=True)
        print(f"[SONDA AMBIENTE] rc={r_env.returncode} pyc={pyc_path.name} stdout={r_env.stdout.strip()!r} stderr={r_env.stderr.strip()!r}")

        marker.unlink(missing_ok=True)
        # Prova 2: esecuzione completa documentata --modalita verifica
        rapporto_out = td / "rapporto_87.md"
        codice_cli = (
            "import sys; sys.path.insert(0, '.'); "
            "from brain.laboratorio.esecuzione.esegui_h002 import main; "
            "sys.exit(main())"
        )
        r_cli = subprocess.run(
            [sys.executable, "-I", "-S", "-B", "-c", codice_cli,
             "--modalita", "verifica", "--varianti", "V-T",
             "--registro", reg_rel, "--cache", str(cache),
             "--rapporto", str(rapporto_out), "--ora", "2026-11-17T02:00:00Z"],
            cwd=str(repo), capture_output=True, text=True,
        )
        reg_esiti = [e for e in json.loads((repo / reg_rel).read_text())["esecuzioni"] if e.get("ruolo") == "esito"]
        print(f"[CLI VERIFICA] rc={r_cli.returncode} marker_esiste={marker.exists()} esiti={reg_esiti} stderr={r_cli.stderr.strip()!r}")

        if "AMBIENTE OK" in r_env.stdout and r_cli.returncode == 0 and marker.exists():
            print("ATTACCO RIUSCITO")
        else:
            print("ATTACCO RESPINTO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
