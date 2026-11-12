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
- i dati stanno in `dati/` (esclusa da git) o nella cartella indicata da TRADING_JOURNAL_DIR.

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
import secrets
import sys
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

SCHEMA = "journal/1"
SCHEMA_ANCORA = "ancora/1"
FILE_ANCORA = "ancora_integrita.json"
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


def _leggi_ancora(path: Path):
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _scrivi_ancora(path: Path, ancora: dict) -> None:
    """Scrittura atomica: file temporaneo e poi sostituzione."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
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
    """Orario ISO-8601 in UTC (`…Z` o `+00:00`, anche con frazioni di secondo). Rifiuta orari senza fuso o non UTC."""
    if not isinstance(s, str):
        raise ValueError(f"{campo}: orario non testuale ({s!r})")
    try:
        t = datetime.fromisoformat(s)
    except ValueError:
        raise ValueError(f"{campo}: orario non ISO-8601 ({s!r})") from None
    if t.tzinfo is None or t.utcoffset() != timedelta(0):
        raise ValueError(f"{campo}: orario non in UTC ({s!r})")
    return t


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
    if registro == "trade" and "aderenza" in dati and dati["aderenza"] not in (1, 2, 3, 4, 5):
        raise ValueError("aderenza: intero da 1 a 5")
    if registro == "decisione" and not isinstance(dati["deroga"], bool):
        raise ValueError("deroga: vero o falso")
    if registro == "decisione" and dati["deroga"] and not dati.get("motivo_deroga"):
        raise ValueError("una deroga richiede il motivo")
    if registro == "previsione" and "chiude" not in dati:
        p = dati["probabilita"]
        if not isinstance(p, (int, float)) or not 0 <= p <= 1:
            raise ValueError("probabilita: numero tra 0 e 1")
    if registro == "previsione" and "esito" in dati:
        if dati["esito"] not in (0, 1):
            raise ValueError("esito: 0 o 1")
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
            date.fromisoformat(str(dati["data"]))
        except ValueError:
            raise ValueError(f"data: non è una data ISO-8601 ({dati['data']!r})") from None
        if "ore_sonno" in dati and not 0 <= _decimale("ore_sonno", dati["ore_sonno"]) <= 24:
            raise ValueError("ore_sonno: tra 0 e 24")


def aggiungi(registro: str, dati: dict, cartella: Path | None = None) -> dict:
    """Aggiunge un record validato, con id, data di registrazione e hash della riga precedente."""
    valida(registro, dati)
    cartella = cartella or cartella_dati()
    cartella.mkdir(parents=True, exist_ok=True)
    path = cartella / f"{registro}.jsonl"
    righe = _righe(path)
    ids = {json.loads(r)["id"] for r in righe}
    for rif in ("corregge", "chiude"):
        if rif in dati and dati[rif] not in ids:
            raise ValueError(f"{rif}: il record {dati[rif]!r} non esiste nel registro {registro}")
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
    Restituisce l'elenco dei problemi (vuoto = integro)."""
    cartella = cartella or cartella_dati()
    problemi = []
    if impronta_attesa is not None:
        ancora = _leggi_ancora(percorso_ancora(cartella))
        if ancora is None:
            problemi.append("ancora assente ma impronta attesa fornita: journal cancellato, spostato o sostituito")
        elif _sha(_canonico(ancora)) != impronta_attesa:
            problemi.append("l'impronta dell'ancora non coincide con quella annotata: journal modificato dopo l'annotazione")
    for registro in REGISTRI:
        prec = GENESI
        for i, riga in enumerate(_righe(cartella / f"{registro}.jsonl"), 1):
            try:
                rec = json.loads(riga)
                valida(registro, rec["dati"])
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
    Chiave: id dell'originale. Anche `chiude` è ricondotto all'originale."""
    radice, finali = {}, {}
    for riga in _righe(path):
        rec = json.loads(riga)
        d = rec["dati"]
        r = radice.get(d["corregge"], d["corregge"]) if "corregge" in d else rec["id"]
        radice[rec["id"]] = r
        finali[r] = dict(d, chiude=radice.get(d["chiude"], d["chiude"])) if "chiude" in d else d
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
            per_autore.setdefault(d["autore"], []).append((d["probabilita"] - esiti[pid]) ** 2)
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
