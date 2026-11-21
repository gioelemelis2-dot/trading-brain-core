"""Esegue TUTTE le suite di test del Brain, una per processo, con la rete bloccata (regola del progetto: nessuna rete
e nessun dato vero nei test). Trova i file da solo: un test nuovo non può restare fuori per dimenticanza.
#135 (Gemini R18-11): una suite è verde solo se esegue almeno un test e non li salta tutti; l'elenco delle suite
trovate deve coincidere con `suite_attese.txt` (un file rinominato o cancellato non sparisce in silenzio).
Uso (dalla radice del repository): python3 -s -B .github/scripts/esegui_test.py
"""
import os
import re
import subprocess
import sys
import time
from pathlib import Path

RADICE = Path(__file__).resolve().parents[2]
ELENCO = Path(__file__).resolve().with_name("suite_attese.txt")
ESEGUITI = re.compile(r"^Ran (\d+) tests? in", re.M)
SALTATI = re.compile(r"skipped=(\d+)")
ESCLUSI = ("brain/collaborazione/",)          # copie di lavoro di revisori esterni, non suite del progetto
SENZA_RETE = dict(os.environ, HTTPS_PROXY="http://127.0.0.1:9", HTTP_PROXY="http://127.0.0.1:9",
                  https_proxy="http://127.0.0.1:9", http_proxy="http://127.0.0.1:9", NO_PROXY="", no_proxy="")


def suite():
    """(nome, comando, cartella) per ogni suite."""
    out = []
    for f in sorted(RADICE.glob("brain/**/test_*.py")):
        rel = f.relative_to(RADICE).as_posix()
        if rel.startswith(ESCLUSI) or rel.startswith("brain/guardian/"):
            continue
        modulo = rel[:-3].replace("/", ".")
        out.append((modulo, [sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", modulo], RADICE))
    out.append(("brain/guardian (discover)",
                [sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "discover", "-s", "test"],
                RADICE / "brain" / "guardian"))
    return out


def esito_suite(codice: int, uscita: str):
    """(verde, motivo) dall'uscita di unittest: almeno un test eseguito, codice 0, esito OK, non tutti saltati."""
    eseguiti = ESEGUITI.findall(uscita)
    if not eseguiti:
        return False, "uscita di unittest non riconosciuta"
    n = int(eseguiti[-1])
    if n == 0:
        return False, "nessun test eseguito"
    if codice != 0:
        return False, f"codice d'uscita {codice}"
    ultima = (uscita.strip().splitlines() or [""])[-1].strip()
    if not ultima.startswith("OK"):
        return False, f"esito {ultima!r}"
    s = SALTATI.search(ultima)
    saltati = int(s.group(1)) if s else 0
    if saltati >= n:
        return False, f"tutti saltati ({saltati} su {n})"
    return True, f"{n} test" + (f", {saltati} saltati" if saltati else "")


def leggi_elenco(file: Path) -> list:
    righe = (r.strip() for r in file.read_text(encoding="utf-8").splitlines())
    return [r for r in righe if r and not r.startswith("#")]


def confronta_elenco(trovate, attese):
    """(attese che mancano, trovate che non sono nell'elenco)."""
    return [a for a in attese if a not in trovate], [t for t in trovate if t not in attese]


def main() -> int:
    falliti = []
    tutte = suite()
    mancanti, nuove = confronta_elenco([n for n, _c, _d in tutte], leggi_elenco(ELENCO))
    for nome in mancanti:
        print(f"KO  suite attesa ma non trovata (rinominata o cancellata?): {nome}", flush=True)
    for nome in nuove:
        print(f"KO  suite nuova non elencata in {ELENCO.name}: {nome}", flush=True)
    falliti += mancanti + nuove
    for nome, cmd, cartella in tutte:
        t0 = time.time()
        r = subprocess.run(cmd, cwd=cartella, env=SENZA_RETE, capture_output=True, text=True)
        verde, motivo = esito_suite(r.returncode, r.stderr)
        print(f"{'OK ' if verde else 'KO '} {time.time() - t0:6.1f}s  {nome}  ·  {motivo}", flush=True)
        if not verde:
            falliti.append(nome)
            print(r.stderr[-4000:], flush=True)
    print(f"\n{'TUTTO VERDE' if not falliti else 'FALLITI: ' + ', '.join(falliti)} "
          f"(Python {sys.version.split()[0]})")
    return 1 if falliti else 0


if __name__ == "__main__":
    sys.exit(main())
