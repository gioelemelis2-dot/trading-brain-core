"""Journal del Trading Brain (D-16, D-20, D-23): registri di sola aggiunta, con catena di hash.

Registri (un file JSON Lines ciascuno, nella cartella dati):
- trade.jsonl       operazioni (MISURE: dalla piattaforma o dichiarate dall'utente, con `fonte`)
- decisione.jsonl   raccomandazione del G0, decisione dell'utente, eventuale deroga e motivo
- stato.jsonl       sonno e stato emotivo: DATI PERSONALI SENSIBILI, facoltativi, mai inviati a servizi esterni
                    senza consenso esplicito
- previsione.jsonl  previsioni probabilistiche (utente, Claude, Gemini) e loro esito, per il Brier score

Regole:
- nessuna riga si modifica: una correzione è un nuovo record con `corregge` = id del record corretto;
- ogni riga contiene `prec_hash` (SHA-256 della riga precedente): la catena scopre modifiche e cancellazioni
  delle righe che hanno un successore;
- ANCORA DI INTEGRITÀ (`ancora_integrita.json`): per ogni registro, numero di righe e SHA-256 dell'ultima riga,
  aggiornata da `aggiungi` e controllata da `verifica`. Scopre anche modifica dell'ultima riga, troncamento della
  coda e riscrittura completa della catena. LIMITE: se l'ancora sta nella stessa cartella dei dati, chi riscrive
  i dati può riscrivere anche l'ancora. Per una protezione contro la manomissione deliberata, tenere l'ancora in
  un percorso separato (TRADING_JOURNAL_ANCHOR) e annotare altrove l'impronta stampata da `ancora`;
- i dati stanno in `dati/` (esclusa da git) o nella cartella indicata da TRADING_JOURNAL_DIR;
- `aggiungi` lavora sotto un LOCK ESCLUSIVO (`.journal.lock` nella cartella dei dati): `fcntl.flock` su Unix,
  altrimenti un file di lock creato in modo esclusivo. Scritture concorrenti non rompono catena e ancora;
- orari: formato unico `AAAA-MM-GGTHH:MM:SS[.frazione da 1 a 6 cifre]` con `Z` o `+00:00`, identico su ogni versione
  di Python (dalla 3.9): un journal valido su una macchina lo è anche sulle altre.

Uso:
  python3 -m journal.journal aggiungi <registro> '<json>'
  python3 -m journal.journal verifica [--impronta <sha256>]
  python3 -m journal.journal ancora                   (impronta dell'ancora, da annotare fuori dal journal)
  python3 -m journal.journal brier
  python3 -m journal.journal sigilla '<json>'          (impegno per una stima sigillata, DA-07)
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import socket
import sys
import time
from contextlib import contextmanager
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

try:
    import fcntl
except ImportError:                     # non Unix: ripiego sul file di lock esclusivo
    fcntl = None

SCHEMA = "journal/1"
SCHEMA_ANCORA = "ancora/1"
FILE_ANCORA = "ancora_integrita.json"
FILE_LOCK = ".journal.lock"
ATTESA_LOCK_S = 30.0                    # attesa massima del lock prima di un errore esplicito
GENESI = "0" * 64
REGISTRI = {
    "trade": {"simbolo", "direzione", "aperto_utc", "ingresso", "stop", "quantita", "fonte"},
    "decisione": {"raccomandazione", "decisione", "deroga", "fonte"},
    "stato": {"data", "fonte"},
    "previsione": {"autore", "evento", "scadenza_utc", "probabilita", "fonte"},
}
FACOLTATIVI = {
    "trade": {"chiuso_utc", "uscita", "pnl_conto", "commissioni", "target", "setup", "checklist", "aderenza",
              "deviazioni", "note", "corregge"},
    "decisione": {"scheda", "motivo_deroga", "regole_coinvolte", "trade", "note", "corregge"},
    "stato": {"ore_sonno", "stato_emotivo", "note", "corregge"},
    "previsione": {"modello", "impegno", "esito", "esito_utc", "chiude", "note", "corregge"},
}


def cartella_dati() -> Path:
    return Path(os.environ.get("TRADING_JOURNAL_DIR", Path(__file__).resolve().parent / "dati"))


def percorso_ancora(cartella: Path) -> Path:
    """TRADING_JOURNAL_ANCHOR (file) se impostata; altrimenti `ancora_integrita.json` nella cartella dei dati."""
    env = os.environ.get("TRADING_JOURNAL_ANCHOR")
    return Path(env) if env else cartella / FILE_ANCORA


def percorso_lock(cartella: Path) -> Path:
    return cartella / FILE_LOCK


def _pid_attivo(pid: int) -> bool:
    """Il processo `pid` è ancora in esecuzione su questa macchina? Nel dubbio: sì (un lock non si ruba).
    Unix: os.kill(pid, 0). Windows: OpenProcess/GetExitCodeProcess (os.kill su Windows TERMINEREBBE il processo)."""
    if os.name == "nt":                                          # non verificato in questo repository (nessun Windows)
        import ctypes
        k = ctypes.windll.kernel32
        h = k.OpenProcess(0x1000, False, pid)                    # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return k.GetLastError() == 5                         # accesso negato: il processo esiste
        try:
            codice = ctypes.c_ulong()
            return not k.GetExitCodeProcess(h, ctypes.byref(codice)) or codice.value == 259   # STILL_ACTIVE
        finally:
            k.CloseHandle(h)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except OSError:                                              # per esempio PermissionError: esiste
        return True
    return True


def _lock_orfano(path: Path):
    """Contenuto del file di lock se è ORFANO e recuperabile in sicurezza, altrimenti None. Recuperabile solo se:
    contenuto leggibile, stesso host, processo non più attivo e lock più vecchio di 2 × ATTESA_LOCK_S."""
    try:
        testo = path.read_text(encoding="utf-8")
        info = json.loads(testo)
        pid, host, t = info["pid"], info["host"], float(info["t"])
    except (OSError, ValueError, KeyError, TypeError):
        return None
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0 or host != socket.gethostname():
        return None
    if time.time() - t <= 2 * ATTESA_LOCK_S or _pid_attivo(pid):
        return None
    return testo


@contextmanager
def _lock_esclusivo(cartella: Path, facoltativo: bool = False):
    """Lock esclusivo sulla cartella dei dati, con attesa massima ATTESA_LOCK_S e poi TimeoutError (mai una scrittura
    non protetta). Unix: `fcntl.flock` su un file aperto con O_CLOEXEC, rilasciato anche se il processo termina.
    Altrimenti: file creato con O_EXCL (atomico anche su Windows) con PID, host e orario, rimosso alla fine; un lock
    ORFANO (stesso host, processo terminato, più vecchio di 2 × ATTESA_LOCK_S) è recuperato, ogni altro lock si attende.
    `facoltativo`: se il file di lock non si può creare (cartella in sola lettura), si procede senza lock."""
    if not facoltativo:
        cartella.mkdir(parents=True, exist_ok=True)
    path = percorso_lock(cartella)
    scadenza = time.monotonic() + ATTESA_LOCK_S
    if fcntl is not None:
        try:
            fd = os.open(path, os.O_RDWR | os.O_CREAT | getattr(os, "O_CLOEXEC", 0), 0o600)
        except OSError:
            if not facoltativo:
                raise
            yield
            return
        try:
            while True:
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= scadenza:
                        raise TimeoutError(f"journal bloccato da un altro processo ({path})") from None
                    time.sleep(0.02)
            try:
                yield
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)
        return
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            break
        except PermissionError:
            if not facoltativo:
                raise
            yield
            return
        except FileExistsError:
            orfano = _lock_orfano(path)
            if orfano is not None:
                try:                                             # ricontrollo: si rimuove solo il lock giudicato orfano
                    if path.read_text(encoding="utf-8") == orfano:
                        path.unlink()
                except OSError:
                    pass
                continue
            if time.monotonic() >= scadenza:
                raise TimeoutError(f"journal bloccato: esiste {path}. Un altro processo sta scrivendo, oppure "
                                   f"un'interruzione ha lasciato il lock: se nessun processo è attivo, rimuoverlo "
                                   f"a mano") from None
            time.sleep(0.02)
    try:
        try:
            os.write(fd, json.dumps({"pid": os.getpid(), "host": socket.gethostname(), "t": time.time()}).encode("utf-8"))
        finally:
            os.close(fd)
        yield
    finally:
        path.unlink()


def _leggi_ancora(path: Path):
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _scrivi_ancora(path: Path, ancora: dict) -> None:
    """Scrittura atomica: file temporaneo e poi sostituzione."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")      # unico per processo
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(json.dumps(ancora, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    os.replace(tmp, path)


def _canonico(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha(testo: str) -> str:
    return hashlib.sha256(testo.encode("utf-8")).hexdigest()


def _righe(path: Path) -> list[str]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [r.rstrip("\n") for r in f if r.strip()]


# Campi numerici e orari validati all'INGRESSO (un record malformato, una volta nella catena, è immutabile).
POSITIVI = {"trade": ("ingresso", "stop", "quantita", "uscita", "target")}
FINITI = {"trade": ("pnl_conto", "commissioni"), "stato": ("ore_sonno",)}
ORARI = {"trade": ("aperto_utc", "chiuso_utc"), "previsione": ("scadenza_utc", "esito_utc")}
# Formati unici, indipendenti dalla versione di Python (fromisoformat di 3.11+ accetta molto più di quello di 3.9).
_ORARIO = re.compile(r"([0-9]{4}-[0-9]{2}-[0-9]{2})T([0-9]{2}:[0-9]{2}:[0-9]{2})(?:\.([0-9]{1,6}))?(?:Z|\+00:00)")
_DATA = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


def _decimale(campo: str, x) -> Decimal:
    """Numero finito come Decimal, dalla sua rappresentazione testuale. Rifiuta booleani, testo non numerico,
    NaN e infiniti."""
    if isinstance(x, bool):
        raise ValueError(f"{campo}: valore booleano non ammesso")
    try:
        d = Decimal(str(x))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{campo}: non è un numero ({x!r})") from None
    if not d.is_finite():
        raise ValueError(f"{campo}: numero non finito ({x!r})")
    return d


def orario_utc(campo: str, s) -> datetime:
    """Orario UTC nel formato unico `AAAA-MM-GGTHH:MM:SS[.frazione da 1 a 6 cifre]` seguito da `Z` o `+00:00`.
    Prima di `datetime.fromisoformat` la frazione è portata a 6 cifre e `Z` diventa `+00:00`: Python 3.9 e 3.10 non
    accettano né `Z` né frazioni diverse da 3 o 6 cifre. Rifiuta orari senza fuso, non UTC o inesistenti."""
    if not isinstance(s, str):
        raise ValueError(f"{campo}: orario non testuale ({s!r})")
    m = _ORARIO.fullmatch(s)
    if not m:
        raise ValueError(f"{campo}: orario non nel formato AAAA-MM-GGTHH:MM:SS[.frazione] con Z o +00:00 ({s!r})")
    frazione = (m.group(3) or "").ljust(6, "0")
    try:
        return datetime.fromisoformat(f"{m.group(1)}T{m.group(2)}.{frazione}+00:00")
    except ValueError:
        raise ValueError(f"{campo}: orario inesistente ({s!r})") from None


def _in_testo(x):
    """Decimal → testo (precisione esatta nel JSON, come per i prezzi), anche dentro liste e dizionari."""
    if isinstance(x, Decimal):
        return str(x)
    if isinstance(x, dict):
        return {k: _in_testo(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_in_testo(v) for v in x]
    return x


def valida(registro: str, dati: dict) -> None:
    if registro not in REGISTRI:
        raise ValueError(f"registro sconosciuto: {registro}")
    richiesti = {"autore", "chiude", "esito", "fonte"} if (registro == "previsione" and "chiude" in dati) \
        else REGISTRI[registro]
    mancanti = richiesti - set(dati)
    if mancanti:
        raise ValueError(f"campi obbligatori mancanti: {sorted(mancanti)}")
    ignoti = set(dati) - REGISTRI[registro] - FACOLTATIVI[registro]
    if ignoti:
        raise ValueError(f"campi non previsti: {sorted(ignoti)}")
    if registro == "trade" and dati["direzione"] not in ("long", "short"):
        raise ValueError("direzione: long o short")
    # `type(x) is int`: in Python True == 1, quindi un booleano passerebbe per un intero.
    if registro == "trade" and "aderenza" in dati and (type(dati["aderenza"]) is not int or dati["aderenza"] not in range(1, 6)):
        raise ValueError("aderenza: intero da 1 a 5")
    if registro == "decisione" and not isinstance(dati["deroga"], bool):
        raise ValueError("deroga: vero o falso")
    if registro == "decisione" and dati["deroga"] and not dati.get("motivo_deroga"):
        raise ValueError("una deroga richiede il motivo")
    if registro == "previsione" and "chiude" not in dati:
        p = dati["probabilita"]
        if not isinstance(p, (int, float, Decimal, str)) or not 0 <= _decimale("probabilita", p) <= 1:     # _decimale rifiuta i booleani
            raise ValueError("probabilita: numero finito tra 0 e 1 (int, float, Decimal o testo numerico; non un booleano)")
    if registro == "previsione" and "chiude" not in dati and ({"esito", "esito_utc"} & set(dati)):
        raise ValueError("esito ed esito_utc stanno solo in un record di esito (con chiude), non in una previsione")
    if registro == "previsione" and "esito" in dati:
        if type(dati["esito"]) is not int or dati["esito"] not in (0, 1):
            raise ValueError("esito: intero 0 o 1 (non un booleano)")
    for campo in POSITIVI.get(registro, ()):
        if campo in dati and _decimale(campo, dati[campo]) <= 0:
            raise ValueError(f"{campo}: deve essere maggiore di zero ({dati[campo]!r})")
    for campo in FINITI.get(registro, ()):
        if campo in dati:
            _decimale(campo, dati[campo])
    orari = {campo: orario_utc(campo, dati[campo]) for campo in ORARI.get(registro, ()) if campo in dati}
    if registro == "trade" and "chiuso_utc" in orari and orari["chiuso_utc"] < orari["aperto_utc"]:
        raise ValueError("chiuso_utc precede aperto_utc")
    if registro == "stato":
        try:
            if not _DATA.fullmatch(str(dati["data"])):
                raise ValueError
            date.fromisoformat(str(dati["data"]))
        except ValueError:
            raise ValueError(f"data: non è una data ISO-8601 ({dati['data']!r})") from None
        if "ore_sonno" in dati and not 0 <= _decimale("ore_sonno", dati["ore_sonno"]) <= 24:
            raise ValueError("ore_sonno: tra 0 e 24")


def controlla_riferimenti(registro: str, dati: dict, precedenti: list[dict]) -> None:
    """Coerenza di `corregge` e `chiude` rispetto ai record precedenti dello stesso registro (`precedenti`: record
    completi, in ordine). Regole:
    - `corregge` e `chiude` puntano a un record esistente;
    - nel registro delle previsioni un record è una PREVISIONE (senza `chiude`) o un ESITO (con `chiude`):
      (a) `corregge` collega record della stessa natura (previsione → previsione, esito → esito);
      (b) `chiude` punta all'id RADICE di una previsione (l'originale, non una sua correzione né un esito);
      (c) una previsione ha al più un esito originale: un esito successivo deve usare `corregge`, e la correzione
          di un esito chiude la stessa previsione dell'esito corretto (non sposta la chiusura)."""
    per_id = {r["id"]: r["dati"] for r in precedenti}
    for rif in ("corregge", "chiude"):
        if rif in dati and dati[rif] not in per_id:
            raise ValueError(f"{rif}: il record {dati[rif]!r} non esiste nel registro {registro}")
    if registro != "previsione":
        return
    esito = "chiude" in dati
    if "corregge" in dati:
        corretto = per_id[dati["corregge"]]
        if ("chiude" in corretto) != esito:
            natura = lambda e: "un esito" if e else "una previsione"
            raise ValueError(f"corregge: {natura(esito)} non può correggere {natura('chiude' in corretto)} "
                             f"({dati['corregge']})")
    if not esito:
        return
    bersaglio = per_id[dati["chiude"]]
    if "chiude" in bersaglio:
        raise ValueError(f"chiude: {dati['chiude']} è un esito, non una previsione")
    if "corregge" in bersaglio:
        raise ValueError(f"chiude: {dati['chiude']} è una correzione; indicare l'id radice della previsione "
                         f"({bersaglio['corregge']} o il suo originale)")
    if "corregge" in dati:
        if per_id[dati["corregge"]]["chiude"] != dati["chiude"]:
            raise ValueError(f"la correzione di un esito deve chiudere la stessa previsione "
                             f"({per_id[dati['corregge']]['chiude']}), non {dati['chiude']}")
        return
    gia = [r["id"] for r in precedenti if r["dati"].get("chiude") == dati["chiude"] and "corregge" not in r["dati"]]
    if gia:
        raise ValueError(f"previsione {dati['chiude']} già chiusa da {gia[0]}: per cambiare l'esito usare corregge")


def aggiungi(registro: str, dati: dict, cartella: Path | None = None) -> dict:
    """Aggiunge un record validato, con id, data di registrazione e hash della riga precedente.
    Lettura delle righe, scrittura e aggiornamento dell'ancora avvengono sotto lock esclusivo.
    I Decimal sono registrati come testo (precisione esatta)."""
    dati = _in_testo(dati)
    valida(registro, dati)
    cartella = cartella or cartella_dati()
    with _lock_esclusivo(cartella):
        path = cartella / f"{registro}.jsonl"
        righe = _righe(path)
        controlla_riferimenti(registro, dati, [json.loads(r) for r in righe])
        rec = {"schema": SCHEMA, "registro": registro, "id": f"{registro[:3].upper()}-{len(righe) + 1:05d}",
               "registrato_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "prec_hash": _sha(righe[-1]) if righe else GENESI, "dati": dati}
        riga = _canonico(rec)
        with open(path, "a", encoding="utf-8") as f:
            f.write(riga + "\n")
        pa = percorso_ancora(cartella)
        ancora = _leggi_ancora(pa) or {"schema": SCHEMA_ANCORA, "registri": {}}
        ancora["registri"][registro] = {"righe": len(righe) + 1, "ultimo_hash": _sha(riga)}
        ancora["aggiornato_utc"] = rec["registrato_utc"]
        _scrivi_ancora(pa, ancora)
    return rec


def verifica(cartella: Path | None = None, impronta_attesa: str | None = None) -> list[str]:
    """Controlla la catena di hash, lo schema di ogni registro e l'ancora. Con `impronta_attesa` (annotata fuori dal
    journal con `ancora`) rileva anche la cancellazione totale di dati e ancora o la loro sostituzione.
    Restituisce l'elenco dei problemi (vuoto = integro). Lavora sotto lo stesso lock di `aggiungi`, così non vede una
    scrittura a metà (riga scritta, ancora non ancora aggiornata)."""
    cartella = cartella or cartella_dati()
    if not cartella.is_dir():
        return _verifica(cartella, impronta_attesa)
    with _lock_esclusivo(cartella, facoltativo=True):
        return _verifica(cartella, impronta_attesa)


def _verifica(cartella: Path, impronta_attesa: str | None) -> list[str]:
    problemi = []
    if impronta_attesa is not None:
        ancora = _leggi_ancora(percorso_ancora(cartella))
        if ancora is None:
            problemi.append("ancora assente ma impronta attesa fornita: journal cancellato, spostato o sostituito")
        elif _sha(_canonico(ancora)) != impronta_attesa:
            problemi.append("l'impronta dell'ancora non coincide con quella annotata: journal modificato dopo l'annotazione")
    for registro in REGISTRI:
        prec, letti = GENESI, []
        for i, riga in enumerate(_righe(cartella / f"{registro}.jsonl"), 1):
            try:
                rec = json.loads(riga)
                valida(registro, rec["dati"])
                controlla_riferimenti(registro, rec["dati"], letti)
                letti.append(rec)
            except (ValueError, KeyError) as e:
                problemi.append(f"{registro} riga {i}: {e}")
                prec = _sha(riga)
                continue
            if rec.get("prec_hash") != prec:
                problemi.append(f"{registro} riga {i}: catena interrotta (riga precedente modificata o rimossa)")
            prec = _sha(riga)
    problemi += _verifica_ancora(cartella)
    return problemi


def _verifica_ancora(cartella: Path) -> list[str]:
    """Confronta ogni registro con l'ancora: numero di righe e hash dell'ultima riga."""
    ancora = _leggi_ancora(percorso_ancora(cartella))
    presenti = {r for r in REGISTRI if _righe(cartella / f"{r}.jsonl")}
    if ancora is None:
        return [f"ancora di integrità assente ({percorso_ancora(cartella)}): impossibile controllare ultima riga, "
                f"troncamento e riscrittura"] if presenti else []
    problemi = []
    attesi = ancora.get("registri", {})
    for registro in sorted(presenti | set(attesi)):
        righe = _righe(cartella / f"{registro}.jsonl")
        a = attesi.get(registro)
        if a is None:
            problemi.append(f"{registro}: registro non presente nell'ancora")
            continue
        ultimo = _sha(righe[-1]) if righe else None
        if a["righe"] != len(righe) or a["ultimo_hash"] != ultimo:
            problemi.append(f"{registro}: non coincide con l'ancora ({len(righe)} righe contro {a['righe']} attese"
                            f"{'' if a['ultimo_hash'] == ultimo else '; ultima riga diversa'}): ultima riga "
                            f"modificata, coda troncata o registro riscritto")
    return problemi


def impronta_ancora(cartella: Path | None = None) -> str:
    """SHA-256 dell'ancora in forma canonica: da annotare fuori dal journal (commit, messaggio, nota)."""
    ancora = _leggi_ancora(percorso_ancora(cartella or cartella_dati()))
    if ancora is None:
        raise ValueError("nessuna ancora: il journal è vuoto o l'ancora è stata rimossa")
    return _sha(_canonico(ancora))


def versioni_finali(path: Path) -> dict:
    """Applica le correzioni: per ogni record originale restituisce l'ultima versione dei dati.
    Una correzione (`corregge`) può puntare all'originale o a una correzione precedente: si risale all'originale.
    Chiave: id dell'originale. Anche `chiude` è ricondotto all'originale.
    Solleva ValueError se il file contiene riferimenti fantasma (un id non ancora presente) o incoerenti (correzione
    fra record di natura diversa, esito che chiude un esito): file manomesso o scritto a mano."""
    radice, esito, finali = {}, {}, {}
    for riga in _righe(path):
        rec = json.loads(riga)
        d = rec["dati"]
        e = "chiude" in d
        for rif in ("corregge", "chiude"):
            if rif in d and d[rif] not in radice:
                raise ValueError(f"{path.name} {rec['id']}: {rif} {d[rif]!r} non precede il record "
                                 f"(riferimento fantasma o file manomesso)")
        if "corregge" in d and esito[d["corregge"]] != e:
            raise ValueError(f"{path.name} {rec['id']}: corregge {d['corregge']!r}, record di natura diversa")
        if e and esito[d["chiude"]]:
            raise ValueError(f"{path.name} {rec['id']}: chiude {d['chiude']!r}, che è un esito e non una previsione")
        r = radice[d["corregge"]] if "corregge" in d else rec["id"]
        radice[rec["id"]], esito[rec["id"]] = r, e
        finali[r] = dict(d, chiude=radice[d["chiude"]]) if e else d
    return finali


def brier(cartella: Path | None = None) -> dict:
    """Brier score per autore, sulle previsioni risolte, DOPO aver applicato le correzioni (`corregge`).
    Esiti da record con `chiude` = id della previsione; vale l'ultima versione di previsione ed esito."""
    cartella = cartella or cartella_dati()
    finali = versioni_finali(cartella / "previsione.jsonl")
    prev = {k: d for k, d in finali.items() if "chiude" not in d}
    esiti = {d["chiude"]: d["esito"] for d in finali.values() if "chiude" in d}
    per_autore = {}
    for pid, d in prev.items():
        if pid in esiti:
            p = float(_decimale("probabilita", d["probabilita"]))      # int, float o testo (Decimal registrato)
            per_autore.setdefault(d["autore"], []).append((p - esiti[pid]) ** 2)
    return {a: {"n": len(v), "brier": sum(v) / len(v)} for a, v in per_autore.items()}


def sigilla(payload: dict) -> dict:
    """Impegno per una stima sigillata (DA-07): SHA-256(nonce segreto di 256 bit || JSON canonico).
    Si registra solo `impegno`; nonce e contenuto si rivelano all'apertura. Non è una firma e non prova l'autore."""
    nonce = secrets.token_hex(32)
    return {"impegno": _sha(nonce + _canonico(payload)), "nonce": nonce, "contenuto": payload}


def verifica_sigillo(impegno: str, nonce: str, payload: dict) -> bool:
    return secrets.compare_digest(impegno, _sha(nonce + _canonico(payload)))


def main(argv=None) -> int:
    a = argv if argv is not None else sys.argv[1:]
    if a[:1] == ["aggiungi"] and len(a) == 3:
        print(_canonico(aggiungi(a[1], json.loads(a[2]))))
    elif a[:1] == ["verifica"] and (len(a) == 1 or (len(a) == 3 and a[1] == "--impronta")):
        p = verifica(impronta_attesa=a[2] if len(a) == 3 else None)
        print("\n".join(p) if p else "journal integro")
        return 1 if p else 0
    elif a == ["ancora"]:
        print(impronta_ancora())
    elif a == ["brier"]:
        print(json.dumps(brier(), ensure_ascii=False, indent=2))
    elif a[:1] == ["sigilla"] and len(a) == 2:
        print(json.dumps(sigilla(json.loads(a[1])), ensure_ascii=False, indent=2))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
