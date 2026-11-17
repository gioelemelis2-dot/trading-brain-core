#!/usr/bin/env python3
"""BANCO-02 (#88): avvelenamento della libreria standard tramite sysconfig.py falso nella CWD.

Lanciando il comando documentato (python3 -I -S -B -c "import sys; sys.path.insert(0, '.'); ..."),
una CWD fittizia in /tmp ospita sysconfig.py + statistics.py falsi: controlla_ambiente legge
sysconfig.get_paths() avvelenato e accetta statistics.py come libreria standard.
Stampa la riga finale ATTACCO RIUSCITO oppure ATTACCO RESPINTO.
"""
import argparse
import hashlib
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
    reg_rel = "brain/laboratorio/prove/registro_d88.json"
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
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@invalid", "commit", "-m", "semina d88")
    git(repo, "push", "-u", "origin", branch)
    return repo, reg_rel


def piazza_finti_stdlib(repo: Path, marker_file: Path, real_stdlib: Path, real_tzpath) -> None:
    # sysconfig.py falso in CWD (= repo): dichiara CWD come "stdlib" e vera stdlib come "platstdlib"
    (repo / "sysconfig.py").write_text(
        "from pathlib import Path\n"
        f"_CWD = {str(repo.resolve())!r}\n"
        f"_REAL_STDLIB = {str(real_stdlib.resolve())!r}\n"
        f"_REAL_TZPATH = {real_tzpath!r}\n"
        "def get_paths(scheme=None, vars=None, expand=True):\n"
        "    return {\n"
        "        'stdlib': _CWD,\n"
        "        'platstdlib': _REAL_STDLIB,\n"
        "        'purelib': '/nonexistent-purelib',\n"
        "        'platlib': '/nonexistent-platlib',\n"
        "    }\n"
        "def get_path(name, scheme=None, vars=None, expand=True):\n"
        "    return get_paths()[name]\n"
        "def get_config_vars(*args):\n"
        "    return {'TZPATH': _REAL_TZPATH}\n"
        "def get_config_var(name):\n"
        "    return _REAL_TZPATH if name == 'TZPATH' else None\n"
        "def get_platform():\n"
        "    return 'macosx'\n",
        encoding="utf-8",
    )
    # statistics.py falso in CWD: trucca mean() per gonfiare il risultato mantenendo median/stdev reali
    real_stats = (real_stdlib / "statistics.py").read_text(encoding="utf-8")
    (repo / "statistics.py").write_text(
        real_stats
        + f"\nfrom pathlib import Path as _Path88\n"
        + f"_Path88({str(marker_file)!r}).write_text('STATISTICS_AVVELENATO\\n', encoding='utf-8')\n"
        + "_real_mean_88 = mean\n"
        + "def mean(data):\n"
        + "    _v = _real_mean_88(data)\n"
        + "    return _v + 5.0 if isinstance(_v, (int, float)) else _v\n",
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", type=Path, default=Path(__file__).resolve().parents[4])
    args = ap.parse_args()

    verifica_rete_bloccata()
    import sysconfig as _real_sc
    real_stdlib = Path(os.__file__).resolve().parent
    real_tzpath = _real_sc.get_config_var("TZPATH")
    with tempfile.TemporaryDirectory(prefix="banco02_d88_") as td_str:
        td = Path(td_str)
        cache = td / "cache_finta"
        prepara_cache(cache)
        repo, reg_rel = prepara_repo_finto(args.radice.resolve(), td, cache)
        marker = td / "marker_sysconfig.txt"
        piazza_finti_stdlib(repo, marker, real_stdlib, real_tzpath)

        rapporto_out = td / "rapporto_88.md"
        codice_cli = (
            "import sys; sys.path.insert(0, '.'); "
            "from brain.laboratorio.esecuzione.esegui_h002 import main; "
            "sys.exit(main())"
        )
        r = subprocess.run(
            [sys.executable, "-I", "-S", "-B", "-c", codice_cli,
             "--modalita", "verifica", "--varianti", "V-T",
             "--registro", reg_rel, "--cache", str(cache),
             "--rapporto", str(rapporto_out), "--ora", "2026-11-17T02:00:00Z"],
            cwd=str(repo), capture_output=True, text=True,
        )
        esiti = [e for e in json.loads((repo / reg_rel).read_text())["esecuzioni"] if e.get("ruolo") == "esito"]
        print(f"[CLI DOCUMENTATO] rc={r.returncode} marker_esiste={marker.exists()} esiti={esiti} stderr={r.stderr.strip()!r}")

        if r.returncode == 0 and marker.exists():
            print("ATTACCO RIUSCITO")
        else:
            print("ATTACCO RESPINTO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
