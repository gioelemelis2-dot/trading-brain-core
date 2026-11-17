"""Avvio controllato dell'esecutore di H-002 (#95, 17/11/2026): i controlli PRIMA di importare il progetto.

Perché: i controlli dell'ambiente di `esegui_h002` (#61, #87, #88) girano dentro il programma, cioè DOPO gli import.
Un file estraneo (un bytecode preparato in __pycache__, un modulo con il nome di uno standard nella cartella di lancio,
un file sigillato modificato) viene eseguito all'import e può manomettere i controlli prima che partano: riprodotto il
17/11 con un .pyc che sostituisce importlib.util.cache_from_source («AMBIENTE OK»).

Questo file usa SOLO la libreria standard caricata con `-I` (la cartella di lancio non è nel percorso finché i
controlli non sono passati) e, prima di importare `brain`, controlla:
- modalità isolata (`-I -S`) e nessuna cartella esterna del bytecode (`-X pycache_prefix`);
- nessun file importabile nella cartella di lancio (.py, .pyc, .so, .pth, .zip, …) e nessuna cartella con un nome
  importabile, a parte `brain` (R14-01: una cartella `statistics/` con il solo `__init__.pyc` era un pacchetto);
- nessun bytecode o estensione compilata dentro `brain`;
- l'impronta SHA-256 di OGNI file sigillato con H-002 (sigillo nel registro canonico), letta dal disco.
Solo allora aggiunge il repository al percorso, segna l'avvio controllato e passa a `esegui_h002.main`.

Limite dichiarato: il lanciatore è la radice della fiducia. Chi lo modifica, o lancia il codice a mano senza di lui,
aggira i controlli; per questo è sigillato con il resto, è su GitHub e i revisori lo leggono.

Uso (dalla radice del repository):
  python3 -I -S -B brain/laboratorio/esecuzione/avvio.py --modalita sviluppo --rapporto <file>
"""
import hashlib
import json
import os
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
REGISTRO = "brain/laboratorio/registro_prove.json"
IPOTESI = "H-002"
IMPORTABILI = (".py", ".pyc", ".pyo", ".so", ".pyd", ".pth", ".zip", ".egg", ".whl")
COMPILATI = (".pyc", ".pyo", ".so", ".pyd", ".pth")


def controlla(radice: str) -> list:
    problemi = []
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):    # R14-09: anche -B
        problemi.append("eseguire con python3 -I -S -B")
    if getattr(sys, "pycache_prefix", None):
        problemi.append("eseguire senza -X pycache_prefix")
    for nome in sorted(os.listdir(radice)):
        if nome in ("brain", ".git"):
            continue
        p = os.path.join(radice, nome)
        if os.path.isdir(p):
            # R14-01: ogni cartella con un nome importabile può diventare un pacchetto (anche con il solo
            # __init__.pyc); ammesse solo cartelle con nomi non importabili (.vscode, dati-utente)
            if nome.isidentifier():
                problemi.append(f"{nome}/: cartella con un nome importabile nella cartella di lancio (spostarla)")
        elif nome.endswith(IMPORTABILI):
            problemi.append(f"{nome}: file importabile nella cartella di lancio")
    for cartella, sotto, file in os.walk(os.path.join(radice, "brain")):
        if "__pycache__" in sotto:
            problemi.append(f"{os.path.relpath(os.path.join(cartella, '__pycache__'), radice)}: bytecode non "
                            f"sigillato (cancellare le cartelle __pycache__)")
        problemi += [f"{os.path.relpath(os.path.join(cartella, f), radice)}: file compilato non sigillato"
                     for f in file if f.endswith(COMPILATI)]
    try:
        with open(os.path.join(radice, REGISTRO), encoding="utf-8") as fh:
            codice = [s for s in json.load(fh)["sigilli"] if s.get("ipotesi") == IPOTESI][0]["codice"]
        if not isinstance(codice, dict) or not codice:
            raise ValueError("codice vuoto")
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError):
        return problemi + [f"{REGISTRO}: nessun sigillo di {IPOTESI} con il codice: non si importa nulla"]
    for rel, impronta in sorted(codice.items()):
        try:
            with open(os.path.join(radice, rel), "rb") as fh:
                adesso = hashlib.sha256(fh.read()).hexdigest()
        except OSError:
            adesso = None
        if adesso != impronta:
            problemi.append(f"{rel}: diverso da quello sigillato")
    return problemi


def principale(argv=None) -> int:
    problemi = controlla(RADICE)
    if problemi:
        print(f"FERMO prima di importare il codice (#95): {problemi[:10]}", file=sys.stderr)
        return 2
    sys.path.insert(0, RADICE)
    sys._tb_avvio_controllato = True
    from brain.laboratorio.esecuzione.esegui_h002 import main
    return main(argv)


if __name__ == "__main__":
    sys.exit(principale())
