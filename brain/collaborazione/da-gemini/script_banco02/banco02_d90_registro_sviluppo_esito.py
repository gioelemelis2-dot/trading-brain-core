#!/usr/bin/env python3
"""BANCO-02 (#90): voce di sviluppo scritta a mano nel registro (e registrazione arbitraria di esito).

Dimostra che una voce 'sviluppo' scritta a mano nel JSON del registro con promossa=True (senza
mai eseguire esegui_sviluppo) viene accettata da esegui_h002 --modalita verifica come prova valida
di promozione sullo screening, e che sigillo.registra_esecuzione accetta esiti multipli contraddittori.
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", type=Path, default=Path(__file__).resolve().parents[4])
    args = ap.parse_args()

    verifica_rete_bloccata()
    with tempfile.TemporaryDirectory(prefix="banco02_d90_") as td_str:
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

        reg_rel = "brain/laboratorio/prove/registro_d90.json"
        reg = repo / reg_rel
        S.sigilla(reg, E.IPOTESI, E.SCHEDA, ["V-T", "V-S"], "2026-11-17T00:00:00Z",
                  E.impronte_codice(repo), E.nomi_robustezza())

        # Scrittura A MANO di una voce 'sviluppo' nel JSON del registro (nessuno screening mai eseguito)
        dati_sha = C.impronta_cache(cache / "XAUUSD", cache / "XAUUSD_ASK", *E.PERIODO_SVILUPPO)
        dati_reg = json.loads(reg.read_text(encoding="utf-8"))
        dati_reg["esecuzioni"].append({
            "ipotesi": E.IPOTESI,
            "ruolo": "sviluppo",
            "variante": "V-T",
            "periodo": [E.PERIODO_SVILUPPO[0].isoformat(), E.PERIODO_SVILUPPO[1].isoformat()],
            "cache": str(cache.resolve()),
            "dati_sha256": dati_sha,
            "n": 999,
            "r_medio": 0.99,
            "sharpe": 0.88,
            "promossa": True,
            "ripetizioni": 2000,
            "seme": 42,
            "rapporto_sha256": hashlib.sha256(b"rapporto inesistente scritto a mano").hexdigest(),
            "ora": "2026-11-17T01:00:00Z",
        })
        reg.write_text(json.dumps(dati_reg, indent=2) + "\n", encoding="utf-8")

        # Verifica secondaria: anche registra_esecuzione accetta esiti multipli contraddittori sullo stesso ruolo
        esiti_contraddittori = False
        reg_multi = td / "reg_multi_esito.json"
        S.sigilla(reg_multi, E.IPOTESI, E.SCHEDA, ["V-T", "V-S"], "2026-11-17T00:00:00Z")
        try:
            S.registra_esecuzione(reg_multi, E.IPOTESI, {"ruolo": "esito", "variante": "V-T", "promossa": True}, "2026-11-17T01:00:00Z")
            S.registra_esecuzione(reg_multi, E.IPOTESI, {"ruolo": "esito", "variante": "V-T", "promossa": False}, "2026-11-17T01:05:00Z")
            esiti_contraddittori = (len([e for e in S.leggi(reg_multi)["esecuzioni"] if e["ruolo"] == "esito"]) == 2)
        except Exception as exc:
            print(f"[ESITI CONTRADDITTORI] bloccati: {exc}")

        git(repo, "add", reg_rel)
        git(repo, "-c", "user.name=Test", "-c", "user.email=test@invalid", "commit", "-m", "sviluppo a mano")
        git(repo, "push", "-u", "origin", branch)

        rapporto_out = td / "rapporto_90.md"
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
        ruoli = [e["ruolo"] for e in json.loads(reg.read_text())["esecuzioni"]]
        print(f"[VERIFICA CON SVILUPPO A MANO] rc={r.returncode} rapporto={rapporto_out.exists()} ruoli={ruoli} esiti_contraddittori={esiti_contraddittori} stderr={r.stderr.strip()!r}")

        if r.returncode == 0 and rapporto_out.exists():
            print("ATTACCO RIUSCITO")
        else:
            print("ATTACCO RESPINTO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
