#!/usr/bin/env python3
"""MANDATO R14 (Compito B) — 7 mutanti nuovi sui controlli introdotti per #72–#95.

Esegue la suite di test pertinenti su copie temporanee mutate per verificare quali mutazioni
vengono uccise dai test ufficiali e quali sopravvivono (copertura mancante).
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path


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


MUTANTI = [
    (
        "M-R14-01",
        "avvio.py: rimuove .zip/.whl/.egg da IMPORTABILI",
        "brain/laboratorio/esecuzione/avvio.py",
        'IMPORTABILI = (".py", ".pyc", ".pyo", ".so", ".pyd", ".pth", ".zip", ".egg", ".whl")',
        'IMPORTABILI = (".py", ".pyc", ".pyo", ".so", ".pyd", ".pth")',
        [
            "brain.laboratorio.tests.test_esegui_h002.TestAvvioControllato.test_copia_pulita_arriva_alla_riga_di_comando",
            "brain.laboratorio.tests.test_esegui_h002.TestAvvioControllato.test_modulo_nella_cartella_di_lancio_rifiutato_prima_di_eseguirlo",
            "brain.laboratorio.tests.test_esegui_h002.TestAvvioControllato.test_file_sigillato_modificato_rifiutato_prima_di_eseguirlo",
            "brain.laboratorio.tests.test_esegui_h002.TestAvvioControllato.test_senza_sigillo_o_senza_modalita_isolata_si_ferma",
        ],
    ),
    (
        "M-R14-02",
        "avvio.py: rimuove controllo -X pycache_prefix",
        "brain/laboratorio/esecuzione/avvio.py",
        '    if getattr(sys, "pycache_prefix", None):\n        problemi.append("eseguire senza -X pycache_prefix")',
        '    if False:\n        problemi.append("eseguire senza -X pycache_prefix")',
        [
            "brain.laboratorio.tests.test_esegui_h002.TestAvvioControllato.test_copia_pulita_arriva_alla_riga_di_comando",
            "brain.laboratorio.tests.test_esegui_h002.TestAvvioControllato.test_modulo_nella_cartella_di_lancio_rifiutato_prima_di_eseguirlo",
            "brain.laboratorio.tests.test_esegui_h002.TestAvvioControllato.test_file_sigillato_modificato_rifiutato_prima_di_eseguirlo",
            "brain.laboratorio.tests.test_esegui_h002.TestAvvioControllato.test_senza_sigillo_o_senza_modalita_isolata_si_ferma",
        ],
    ),
    (
        "M-R14-03",
        "sigillo.py: versioni_nella_storia guarda solo HEAD invece di --all (#86)",
        "brain/laboratorio/esecuzione/sigillo.py",
        'elenco = _git(radice, "rev-list", "--all", "--", rel)',
        'elenco = _git(radice, "rev-list", "HEAD", "--", rel)',
        ["brain.laboratorio.tests.test_esegui_h002.TestVerificaUnaVoltaNellaStoria"],
    ),
    (
        "M-R14-04",
        "esegui_h002.py: usa min() invece di max() su N nella storia (#86)",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        'n = max([S.n_prove(S.leggi(x.registro))] + [S.n_prove(d) for d in storia])   # #86: N non scende',
        'n = min([S.n_prove(S.leggi(x.registro))] + [S.n_prove(d) for d in storia])',
        ["brain.laboratorio.tests.test_esegui_h002.TestVerificaUnaVoltaNellaStoria"],
    ),
    (
        "M-R14-05",
        "esporta_redatto.py: toglie utf-32-le, utf-32-be e cp1252 da CODIFICHE (#72)",
        "brain/governance/esporta_redatto.py",
        'CODIFICHE = ("utf-8", "utf-16-le", "utf-16-be", "utf-32-le", "utf-32-be", "latin-1", "cp1252")',
        'CODIFICHE = ("utf-8", "utf-16-le", "utf-16-be", "latin-1")',
        ["brain.governance.test_esporta_redatto"],
    ),
    (
        "M-R14-06",
        "esporta_redatto.py: FIRME_ARCHIVI ridotto a soli ZIP e gzip (#72)",
        "brain/governance/esporta_redatto.py",
        'FIRME_ARCHIVI = (b"PK\\x03\\x04", b"\\x1f\\x8b", b"7z\\xbc\\xaf\\x27\\x1c", b"\\xfd7zXZ", b"BZh", b"Rar!")',
        'FIRME_ARCHIVI = (b"PK\\x03\\x04", b"\\x1f\\x8b")',
        ["brain.governance.test_esporta_redatto"],
    ),
    (
        "M-R14-07",
        "potenza_soglia.py: n_per_potenza salta controllo regola quando mu <= soglia (#94e)",
        "brain/laboratorio/studi/potenza_soglia.py",
        '    _spostamento(regola)                                               # #94: regola controllata sempre\n    if mu <= soglia:',
        '    if mu <= soglia:',
        ["brain.laboratorio.tests.test_potenza_soglia"],
    ),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", type=Path, default=Path(__file__).resolve().parents[3])
    args = ap.parse_args()
    radice = args.radice.resolve()

    verifica_rete_bloccata()
    with tempfile.TemporaryDirectory(prefix="r14_mutanti_") as td_str:
        td = Path(td_str)
        # Controllo M00 su tutte le target suite usate sopra
        visti = set()
        for *_rest, suite in MUTANTI:
            chiave = tuple(suite)
            if chiave in visti:
                continue
            visti.add(chiave)
            m00 = td / f"M00_{len(visti)}"
            shutil.copytree(radice / "brain", m00 / "brain", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            r0 = subprocess.run([sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", *suite],
                                cwd=str(m00), capture_output=True, text=True)
            print(f"[M00 BASE] suite={suite[0]} rc={r0.returncode}")
            if r0.returncode != 0:
                print(r0.stderr)
                return 1

        uccisi, vivi = 0, 0
        for mid, desc, rel, vecchia, nuova, suite in MUTANTI:
            copia = td / mid
            shutil.copytree(radice / "brain", copia / "brain", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            target = copia / rel
            testo = target.read_text(encoding="utf-8")
            assert vecchia in testo, f"{mid}: target non trovato in {rel}"
            mutato = testo.replace(vecchia, nuova, 1)
            compile(mutato, str(target), "exec")
            target.write_text(mutato, encoding="utf-8")
            r = subprocess.run(
                [sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", *suite],
                cwd=str(copia), capture_output=True, text=True,
            )
            stato = "UCCISO" if r.returncode != 0 else "SOPRAVVISSUTO"
            if r.returncode != 0:
                uccisi += 1
            else:
                vivi += 1
            print(f"[{stato}] {mid} ({desc}) -> rc={r.returncode}")
        print(f"RIEPILOGO MUTANTI NUOVI: uccisi={uccisi}/{len(MUTANTI)}, sopravvissuti={vivi}/{len(MUTANTI)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
