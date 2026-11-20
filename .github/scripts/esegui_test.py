"""Esegue TUTTE le suite di test del Brain, una per processo, con la rete bloccata (regola del progetto: nessuna rete
e nessun dato vero nei test). Trova i file da solo: un test nuovo non può restare fuori per dimenticanza.
Uso (dalla radice del repository): python3 -s -B .github/scripts/esegui_test.py
"""
import os
import subprocess
import sys
import time
from pathlib import Path

RADICE = Path(__file__).resolve().parents[2]
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


def main() -> int:
    falliti = []
    for nome, cmd, cartella in suite():
        t0 = time.time()
        r = subprocess.run(cmd, cwd=cartella, env=SENZA_RETE, capture_output=True, text=True)
        ultima = (r.stderr.strip().splitlines() or ["(nessun output)"])[-1]
        esito = "OK " if r.returncode == 0 else "KO "
        print(f"{esito} {time.time() - t0:6.1f}s  {nome}  ·  {ultima}", flush=True)
        if r.returncode != 0:
            falliti.append(nome)
            print(r.stderr[-4000:], flush=True)
    print(f"\n{'TUTTO VERDE' if not falliti else 'FALLITI: ' + ', '.join(falliti)} "
          f"(Python {sys.version.split()[0]})")
    return 1 if falliti else 0


if __name__ == "__main__":
    sys.exit(main())
