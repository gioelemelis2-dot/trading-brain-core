#!/usr/bin/env python3
"""BANCO-02 (#91): 'esito' scritto nel registro prima del controllo finale controlla_ambiente.

Avvia esegui_h002 --modalita verifica in un repository fittizio: superato il controllo iniziale,
appena viene creata la cartella di --rapporto (subito dopo controlla_ambiente iniziale), il padre
altera criteri.py su disco. Il controllo finale fallisce (rc!=0, nessun rapporto scritto), ma
il registro contiene gia 'verifica' ed 'esito'.
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
import time
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", type=Path, default=Path(__file__).resolve().parents[4])
    args = ap.parse_args()

    verifica_rete_bloccata()
    with tempfile.TemporaryDirectory(prefix="banco02_d91_") as td_str:
        td = Path(td_str)
        cache = td / "cache_finta"
        prepara_cache(cache)

        bare = td / "origin.git"
        subprocess.run(["git", "init", "--bare", str(bare)], capture_output=True, text=True, check=True)
        repo = td / "repo"
        subprocess.run(["git", "clone", "--no-hardlinks", str(args.radice.resolve()), str(repo)],
                       capture_output=True, text=True, check=True)
        branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
        git(repo, "remote", "set-url", "origin", str(bare))

        sys.path.insert(0, str(repo))
        from brain.laboratorio.esecuzione import sigillo as S, esegui_h002 as E, caricatore as C

        reg_rel = "brain/laboratorio/prove/registro_d91.json"
        reg = repo / reg_rel
        S.sigilla(reg, E.IPOTESI, E.SCHEDA, ["V-T", "V-S"], "2026-11-17T00:00:00Z",
                  E.impronte_codice(repo), E.nomi_robustezza())
        dati_sha = C.impronta_cache(cache / "XAUUSD", cache / "XAUUSD_ASK", *E.PERIODO_SVILUPPO)
        S.registra_esecuzione(reg, E.IPOTESI, {
            "ruolo": "sviluppo", "variante": "V-T",
            "periodo": [E.PERIODO_SVILUPPO[0].isoformat(), E.PERIODO_SVILUPPO[1].isoformat()],
            "cache": str(cache.resolve()), "dati_sha256": dati_sha,
            "n": 700, "r_medio": 0.25, "sharpe": 0.15, "promossa": True,
            "ripetizioni": 2000, "seme": 42, "rapporto_sha256": hashlib.sha256(b"svil").hexdigest(),
        }, "2026-11-17T01:00:00Z")
        git(repo, "add", reg_rel)
        git(repo, "-c", "user.name=Test", "-c", "user.email=test@invalid", "commit", "-m", "semina d91")
        git(repo, "push", "-u", "origin", branch)

        # Cartella sentinella che viene creata subito DOPO il controllo_ambiente iniziale
        sentinella_dir = td / "sentinella_post_inizio"
        rapporto_out = sentinella_dir / "rapporto_91.md"
        criteri_py = repo / "brain/laboratorio/esecuzione/criteri.py"

        codice_cli = (
            "import sys; sys.path.insert(0, '.'); "
            "from brain.laboratorio.esecuzione.esegui_h002 import main; "
            "sys.exit(main())"
        )
        proc = subprocess.Popen(
            [sys.executable, "-I", "-S", "-B", "-c", codice_cli,
             "--modalita", "verifica", "--varianti", "V-T",
             "--registro", reg_rel, "--cache", str(cache),
             "--rapporto", str(rapporto_out), "--ora", "2026-11-17T02:00:00Z"],
            cwd=str(repo), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        t_start = time.monotonic()
        modificato = False
        while proc.poll() is None:
            if not modificato:
                try:
                    dati_cur = json.loads(reg.read_text(encoding="utf-8"))
                    ha_ver = any(e.get("ruolo") == "verifica" for e in dati_cur.get("esecuzioni", []))
                except Exception:
                    ha_ver = False
                if ha_ver:
                    criteri_py.write_text(
                        criteri_py.read_text(encoding="utf-8") + "\n# manomissione dopo verifica, prima di esito/fine (#91)\n",
                        encoding="utf-8",
                    )
                    modificato = True
                    break
            if time.monotonic() - t_start > 90.0:
                break
            time.sleep(0.01)
        stdout, stderr = proc.communicate(timeout=120)

        esecuzioni = json.loads(reg.read_text(encoding="utf-8"))["esecuzioni"]
        ruoli = [e["ruolo"] for e in esecuzioni]
        ha_esito = any(e["ruolo"] == "esito" for e in esecuzioni)
        print(f"[FINE CONTROLLO] modificato={modificato} rc={proc.returncode} rapporto_esiste={rapporto_out.exists()} ruoli={ruoli} stderr={stderr.strip()!r}")

        if proc.returncode != 0 and not rapporto_out.exists() and ha_esito:
            print("ATTACCO RIUSCITO")
        else:
            print("ATTACCO RESPINTO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
