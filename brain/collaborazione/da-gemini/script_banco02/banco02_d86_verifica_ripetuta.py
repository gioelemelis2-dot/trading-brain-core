#!/usr/bin/env python3
"""BANCO-02 (#86): ripetere la verifica di H-002 (dati inventati).

Vettore A: secondo file di registro dentro il repository con N ridotto (N prima vs N dopo).
Vettore B: nuovo ramo git creato da un commit precedente alla prima verifica, con tracciamento remoto proprio.
Stampa la riga finale ATTACCO RIUSCITO oppure ATTACCO RESPINTO.
"""
import argparse
import hashlib
import json
import lzma
import os
import shutil
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


def prepara_repo_finto(radice_orig: Path, td: Path):
    bare = td / "origin.git"
    subprocess.run(["git", "init", "--bare", str(bare)], capture_output=True, text=True, check=True)
    repo = td / "repo"
    # Copia dell'albero tracciato al commit corrente del worktree di riferimento
    subprocess.run(["git", "clone", "--no-hardlinks", str(radice_orig), str(repo)],
                   capture_output=True, text=True, check=True)
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    git(repo, "remote", "set-url", "origin", str(bare))
    git(repo, "push", "-u", "origin", branch)
    return repo, bare, branch


def esegui_comando_documentato(repo: Path, extra_args: list) -> subprocess.CompletedProcess:
    codice = (
        "import sys; sys.path.insert(0, '.'); "
        "from brain.laboratorio.esecuzione.esegui_h002 import main; "
        "sys.exit(main())"
    )
    return subprocess.run(
        [sys.executable, "-I", "-S", "-B", "-c", codice, *extra_args],
        cwd=str(repo),
        capture_output=True,
        text=True,
    )


def semina_registro(repo: Path, reg_rel: str, cache: Path, extra_prove: int) -> None:
    sys.path.insert(0, str(repo))
    from brain.laboratorio.esecuzione import sigillo as S, esegui_h002 as E, caricatore as C
    reg = repo / reg_rel
    scheda = E.SCHEDA
    codice = E.impronte_codice(repo)
    rob = E.nomi_robustezza()
    if extra_prove > 0:
        scheda_alt = repo / "brain/laboratorio/ipotesi/H-001-finta-d86.md"
        scheda_alt.write_text("# H-001 finta per N iniziale\n", encoding="utf-8")
        S.sigilla(reg, "H-001", scheda_alt, [f"V-{i}" for i in range(extra_prove)], "2026-11-16T10:00:00Z", codice, [])
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], "2026-11-17T00:00:00Z", codice, rob)
    dati_sha = C.impronta_cache(cache / "XAUUSD", cache / "XAUUSD_ASK", *E.PERIODO_SVILUPPO)
    for var in ("V-T",):
        S.registra_esecuzione(reg, "H-002", {
            "ruolo": "sviluppo", "variante": var,
            "periodo": [E.PERIODO_SVILUPPO[0].isoformat(), E.PERIODO_SVILUPPO[1].isoformat()],
            "cache": str(cache.resolve()), "dati_sha256": dati_sha,
            "n": 700, "r_medio": 0.25, "sharpe": 0.15, "promossa": True,
            "ripetizioni": 2000, "seme": 42, "rapporto_sha256": hashlib.sha256(b"svil").hexdigest(),
        }, "2026-11-17T01:00:00Z")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", type=Path, default=Path(__file__).resolve().parents[4])
    args = ap.parse_args()

    verifica_rete_bloccata()
    with tempfile.TemporaryDirectory(prefix="banco02_d86_") as td_str:
        td = Path(td_str)
        cache = td / "cache_finta"
        prepara_cache(cache)
        repo, bare, branch = prepara_repo_finto(args.radice.resolve(), td)

        reg1_rel = "brain/laboratorio/prove/registro_d86_principale.json"
        semina_registro(repo, reg1_rel, cache, extra_prove=4)  # 4 prove + 2 (H-002) => N = 6
        git(repo, "add", "-A")
        git(repo, "-c", "user.name=Test", "-c", "user.email=test@invalid", "commit", "-m", "semina reg1")
        git(repo, "push", "origin", branch)
        commit_pre_verifica = git(repo, "rev-parse", "HEAD")

        reg1 = repo / reg1_rel
        n_prima = sum(1 for p in json.loads(reg1.read_text())["prove"] if p["ruolo"] == "selezionabile")
        r1 = esegui_comando_documentato(repo, [
            "--modalita", "verifica", "--varianti", "V-T",
            "--registro", reg1_rel, "--cache", str(cache),
            "--rapporto", str(td / "rapporto1.md"), "--ora", "2026-11-17T02:00:00Z",
        ])
        print(f"[RUN 1 orig] rc={r1.returncode} N_prima={n_prima} stderr={r1.stderr.strip()!r}")
        if r1.returncode != 0:
            print("ATTACCO RESPINTO")
            return 0
        git(repo, "add", reg1_rel)
        git(repo, "-c", "user.name=Test", "-c", "user.email=test@invalid", "commit", "-m", "post verifica 1")
        git(repo, "push", "origin", branch)

        # Vettore A: secondo file di registro con solo H-002 (N ridotto da 6 a 2)
        reg2_rel = "brain/laboratorio/prove/registro_d86_secondo.json"
        semina_registro(repo, reg2_rel, cache, extra_prove=0)
        git(repo, "add", reg2_rel)
        git(repo, "-c", "user.name=Test", "-c", "user.email=test@invalid", "commit", "-m", "semina reg2")
        git(repo, "push", "origin", branch)
        n_vettore_a = sum(1 for p in json.loads((repo / reg2_rel).read_text())["prove"] if p["ruolo"] == "selezionabile")
        r_a = esegui_comando_documentato(repo, [
            "--modalita", "verifica", "--varianti", "V-T",
            "--registro", reg2_rel, "--cache", str(cache),
            "--rapporto", str(td / "rapporto_a.md"), "--ora", "2026-11-17T03:00:00Z",
        ])
        print(f"[VETTORE A: 2o registro] rc={r_a.returncode} N_prima={n_prima} N_dopo={n_vettore_a} stderr={r_a.stderr.strip()!r}")

        # Vettore B: nuovo ramo creato dal commit precedente alla prima verifica, su reg1_rel
        git(repo, "checkout", "-f", "-b", "rev/verifica-bis", commit_pre_verifica)
        git(repo, "push", "-u", "origin", "rev/verifica-bis")
        n_vettore_b = sum(1 for p in json.loads(reg1.read_text())["prove"] if p["ruolo"] == "selezionabile")
        r_b = esegui_comando_documentato(repo, [
            "--modalita", "verifica", "--varianti", "V-T",
            "--registro", reg1_rel, "--cache", str(cache),
            "--rapporto", str(td / "rapporto_b.md"), "--ora", "2026-11-17T04:00:00Z",
        ])
        esec_b = [e["ruolo"] for e in json.loads(reg1.read_text())["esecuzioni"]]
        print(f"[VETTORE B: ramo nuovo] rc={r_b.returncode} N_prima={n_prima} N_dopo={n_vettore_b} ruoli_reg1={esec_b} stderr={r_b.stderr.strip()!r}")

        if r_a.returncode == 0 or r_b.returncode == 0:
            print("ATTACCO RIUSCITO")
        else:
            print("ATTACCO RESPINTO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
