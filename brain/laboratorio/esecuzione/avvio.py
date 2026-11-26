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
Verifica sul percorso ordinario D-31 (D-51, PIANO-D51 §3.3): il primo argomento è `verifica`; l'ipotesi si legge dal
contratto H-003 della scheda (`--scheda`) e si controlla il codice sigillato per QUELL'ipotesi, poi `esegui_verifica`:
  python3 -I -S -B brain/laboratorio/esecuzione/avvio.py verifica --scheda <file> --registro … --riserva … …
"""
import hashlib
import json
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
REGISTRO = "brain/laboratorio/registro_prove.json"
IPOTESI = "H-002"
IMPORTABILI = (".py", ".pyc", ".pyo", ".so", ".pyd", ".pth", ".zip", ".egg", ".whl")
COMPILATI = (".pyc", ".pyo", ".so", ".pyd", ".pth")


def scheda_indicata(argv: list):
    """(percorso, problema): l'UNICA --scheda, nella forma «--scheda X» o «--scheda=X» (#143, R19-02: prima si
    leggeva la prima occorrenza mentre l'esecutore usava l'ultima)."""
    trovate, i = [], 0
    while i < len(argv):
        a = argv[i]
        if a == "--scheda":
            if i + 1 >= len(argv):
                return None, "manca il valore di --scheda"
            trovate.append(argv[i + 1])
            i += 2
            continue
        if a.startswith("--scheda="):
            trovate.append(a[len("--scheda="):])
        i += 1
    if len(trovate) != 1:
        return None, "manca --scheda" if not trovate else f"--scheda ripetuta {len(trovate)} volte: ne serve una sola"
    return trovate[0], None


def ipotesi_della_scheda(argv: list):
    """(ipotesi, problema): l'ipotesi dal blocco «json contratto-h003» della scheda indicata con --scheda."""
    percorso, problema = scheda_indicata(argv)
    if problema:
        return None, problema
    try:
        with open(percorso, encoding="utf-8") as fh:
            blocchi = re.findall(r"```json contratto-h003\n(.*?)\n```", fh.read(), re.S)
        if len(blocchi) != 1:
            return None, f"{percorso}: nessun contratto H-003 (un solo blocco «json contratto-h003»)"
        ipotesi = json.loads(blocchi[0]).get("ipotesi")
    except (OSError, ValueError, AttributeError) as e:
        return None, f"{percorso}: contratto H-003 illeggibile ({e})"
    if not isinstance(ipotesi, str) or not ipotesi:
        return None, f"{percorso}: contratto H-003 senza ipotesi"
    return ipotesi, None


RICHIESTI_VERIFICA = ("brain/laboratorio/esecuzione/esegui_verifica.py", "brain/laboratorio/esecuzione/avvio.py")


def controlla(radice: str, ipotesi: str = IPOTESI, richiesti: tuple = ()) -> list:
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
            codice = [s for s in json.load(fh)["sigilli"] if s.get("ipotesi") == ipotesi][0]["codice"]
        if not isinstance(codice, dict) or not codice:
            raise ValueError("codice vuoto")
        mancanti = [f for f in richiesti if f not in codice]                 # #143: il sigillo copre ciò che si esegue
        if mancanti:
            return problemi + [f"{REGISTRO}: il sigillo di {ipotesi} non contiene {', '.join(mancanti)}: non si importa nulla"]
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError):
        return problemi + [f"{REGISTRO}: nessun sigillo di {ipotesi} con il codice: non si importa nulla"]
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
    argv = list(sys.argv[1:] if argv is None else argv)
    verifica = bool(argv) and argv[0] == "verifica"
    if verifica:                                                       # D-51: percorso ordinario D-31
        argv = argv[1:]
        ipotesi, problema = ipotesi_della_scheda(argv)
        problemi = [problema] if problema else controlla(RADICE, ipotesi, RICHIESTI_VERIFICA)
    else:
        problemi = controlla(RADICE)
    if problemi:
        print(f"FERMO prima di importare il codice (#95): {problemi[:10]}", file=sys.stderr)
        return 2
    sys.path.insert(0, RADICE)
    sys._tb_avvio_controllato = True
    if verifica:                                                       # #143: la scheda controllata è l'unica eseguibile
        sys._tb_scheda_controllata = os.path.realpath(scheda_indicata(argv)[0])
    if verifica:
        from brain.laboratorio.esecuzione.esegui_verifica import main as main_verifica
        return main_verifica(argv)
    from brain.laboratorio.esecuzione.esegui_h002 import main
    return main(argv)


if __name__ == "__main__":
    sys.exit(principale())
