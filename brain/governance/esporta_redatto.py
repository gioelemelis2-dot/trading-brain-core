"""Esportazione redatta del repository per i revisori esterni (richiesta del DGS, DGS-10; difetto #43), 16/11/2026.

Perché: nel pacchetto dato al DGS c'erano nome, utente GitHub e percorsi del Mac dell'utente. Il repository li
conserva (sono la storia: rapporti di Gemini, censimento), ma il pacchetto per i revisori non deve contenerli.

Cosa fa:
- prende ESATTAMENTE il contenuto di un commit (`git archive`), non la cartella di lavoro;
- nei file di testo sostituisce, senza distinguere maiuscole e minuscole, le stringhe date al lancio (le più lunghe
  per prime) e ogni nome utente nei percorsi del Mac (`/Users/<nome>` → `/Users/<utente>`);
- i file binari restano come sono;
- se una delle stringhe date resta anche in un solo file (per esempio un binario) o in un nome di file, si FERMA
  e non scrive il pacchetto;
- aggiunge `MANIFEST.tsv` (percorso, SHA-256 e byte del file esportato, righe, se è stato redatto, SHA-256 del file
  originale nel commit) e `LEGGIMI-PACCHETTO.md` (commit, regole, come verificare);
- il pacchetto va FUORI dal repository.

Le stringhe da togliere si passano al lancio e non sono scritte nel repository. Lo strumento non le stampa.

Uso:
  python3 -s -B -m brain.governance.esporta_redatto --uscita /percorso/pacchetto.zip \\
      --sostituisci "Nome Cognome=<titolare>" --sostituisci "utente-github=<utente-github>" --sostituisci "nome=<utente>"
"""
import argparse
import hashlib
import io
import os
import re
import subprocess
import sys
import tarfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple

RADICE = Path(__file__).resolve().parents[2]
PERCORSI_MAC = re.compile(r"/Users/(?!<utente>)[^/\s\"'`<>]+")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def esporta(repo: Path, rev: str, uscita: Path, sostituzioni: List[Tuple[str, str]]) -> dict:
    repo, uscita = Path(repo).resolve(), Path(uscita).resolve()
    if uscita == repo or repo in uscita.parents:
        raise ValueError(f"il pacchetto va fuori dal repository ({repo})")
    if not sostituzioni or any(not a for a, _ in sostituzioni):
        raise ValueError("servono le stringhe da togliere (--sostituisci VECCHIO=NUOVO)")
    commit = subprocess.run(["git", "-C", str(repo), "rev-parse", rev], capture_output=True, text=True,
                            check=True).stdout.strip()
    archivio = subprocess.run(["git", "-C", str(repo), "archive", "--format=tar", commit], capture_output=True,
                              check=True).stdout
    regole = [(re.compile(re.escape(a), re.I), b) for a, b in sorted(sostituzioni, key=lambda x: -len(x[0]))]
    controlli = [re.compile(re.escape(a.encode("utf-8")), re.I) for a, _ in sostituzioni]
    file = []
    with tarfile.open(fileobj=io.BytesIO(archivio)) as t:
        for m in t.getmembers():
            if not m.isfile():
                continue
            dati = t.extractfile(m).read()
            try:
                testo = dati.decode("utf-8")
            except UnicodeDecodeError:
                nuovo = dati
            else:
                for rx, b in regole:
                    testo = rx.sub(b, testo)
                nuovo = PERCORSI_MAC.sub("/Users/<utente>", testo).encode("utf-8")
            file.append((m.name, nuovo, _sha(dati)))
    residui = sorted({n for n, d, _ in file if any(rx.search(d) or rx.search(n.encode("utf-8")) for rx in controlli)})
    if residui:
        raise ValueError(f"dati personali ancora presenti (non redigibili) in: {residui[:20]}")
    redatti = sum(1 for _, d, o in file if _sha(d) != o)
    manifest = ["percorso\tsha256\tbyte\trighe\tredatto\tsha256_originale"]
    for n, d, o in sorted(file):
        righe = d.count(b"\n")
        redatto = "sì" if _sha(d) != o else "no"
        manifest.append(f"{n}\t{_sha(d)}\t{len(d)}\t{righe}\t{redatto}\t{o}")
    leggimi = (f"# Pacchetto per i revisori (redatto)\n\n"
               f"- **Commit:** `{commit}` (contenuto esatto del commit, poi redatto)\n"
               f"- **Creato:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
               f"- **File:** {len(file)}, di cui **{redatti} redatti**\n\n"
               f"**Redazione:** nei file di testo nome, utente GitHub e nome utente del computer sono sostituiti da "
               f"segnaposto (`<titolare>`, `<utente-github>`, `<utente>`), e ogni percorso `/Users/<nome>` diventa "
               f"`/Users/<utente>`. I binari sono invariati. Per questo l'impronta dei file redatti differisce da "
               f"quella nel repository: `MANIFEST.tsv` riporta entrambe (`sha256` del file nel pacchetto, "
               f"`sha256_originale` nel commit).\n\n"
               f"**Verifica:** ricalcolare lo SHA-256 di ogni file e confrontarlo con la colonna `sha256`; per i file "
               f"con `redatto = no` l'impronta coincide con quella del commit su GitHub.\n")
    uscita.parent.mkdir(parents=True, exist_ok=True)
    tmp = uscita.with_name(f".{uscita.name}.tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n, d, _ in sorted(file):
            z.writestr(n, d)
        z.writestr("MANIFEST.tsv", "\n".join(manifest) + "\n")
        z.writestr("LEGGIMI-PACCHETTO.md", leggimi)
    os.replace(tmp, uscita)
    return {"file": len(file), "redatti": redatti, "commit": commit}


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    a.add_argument("--repo", type=Path, default=RADICE)
    a.add_argument("--rev", default="HEAD")
    a.add_argument("--uscita", type=Path, required=True)
    a.add_argument("--sostituisci", action="append", default=[], help="VECCHIO=NUOVO (ripetibile)")
    x = a.parse_args(argv)
    coppie = []
    for s in x.sostituisci:
        if "=" not in s or not s.split("=", 1)[0]:
            print("ERRORE: --sostituisci vuole VECCHIO=NUOVO", file=sys.stderr)
            return 2
        coppie.append(tuple(s.split("=", 1)))
    try:
        r = esporta(x.repo, x.rev, x.uscita, coppie)
    except (ValueError, subprocess.CalledProcessError) as e:
        print(f"FERMO: {e}", file=sys.stderr)
        return 2
    print(f"pacchetto scritto: {x.uscita} — commit {r['commit'][:7]}, {r['file']} file, {r['redatti']} redatti")
    return 0


if __name__ == "__main__":
    sys.exit(main())
