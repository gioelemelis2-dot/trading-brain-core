"""Journal del Trading Brain (D-16, D-20, D-23): registri di sola aggiunta, con catena di hash.

Registri (un file JSON Lines ciascuno, nella cartella dati):
- trade.jsonl       operazioni (MISURE: dalla piattaforma o dichiarate dall'utente, con `fonte`)
- decisione.jsonl   raccomandazione del G0, decisione dell'utente, eventuale deroga e motivo
- stato.jsonl       sonno e stato emotivo: DATI PERSONALI SENSIBILI, facoltativi, mai inviati a servizi esterni
                    senza consenso esplicito
- previsione.jsonl  previsioni probabilistiche (utente, Claude, Gemini) e loro esito, per il Brier score

Regole:
- nessuna riga si modifica: una correzione è un nuovo record con `corregge` = id del record corretto;
- ogni riga contiene `prec_hash` (SHA-256 della riga precedente): `verifica` scopre modifiche e cancellazioni;
- i dati stanno in `dati/` (esclusa da git) o nella cartella indicata da TRADING_JOURNAL_DIR.

Uso:
  python3 -m journal.journal aggiungi <registro> '<json>'
  python3 -m journal.journal verifica
  python3 -m journal.journal brier
  python3 -m journal.journal sigilla '<json>'          (impegno per una stima sigillata, DA-07)
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "journal/1"
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


def _canonico(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha(testo: str) -> str:
    return hashlib.sha256(testo.encode("utf-8")).hexdigest()


def _righe(path: Path) -> list[str]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [r.rstrip("\n") for r in f if r.strip()]


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


def aggiungi(registro: str, dati: dict, cartella: Path | None = None) -> dict:
    """Aggiunge un record validato, con id, data di registrazione e hash della riga precedente."""
    valida(registro, dati)
    cartella = cartella or cartella_dati()
    cartella.mkdir(parents=True, exist_ok=True)
    path = cartella / f"{registro}.jsonl"
    righe = _righe(path)
    rec = {"schema": SCHEMA, "registro": registro, "id": f"{registro[:3].upper()}-{len(righe) + 1:05d}",
           "registrato_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "prec_hash": _sha(righe[-1]) if righe else GENESI, "dati": dati}
    with open(path, "a", encoding="utf-8") as f:
        f.write(_canonico(rec) + "\n")
    return rec


def verifica(cartella: Path | None = None) -> list[str]:
    """Controlla la catena di hash e lo schema di ogni registro. Restituisce l'elenco dei problemi (vuoto = integro)."""
    cartella = cartella or cartella_dati()
    problemi = []
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
    return problemi


def brier(cartella: Path | None = None) -> dict:
    """Brier score per autore, sulle previsioni risolte. Esiti da record con `chiude` = id della previsione."""
    cartella = cartella or cartella_dati()
    prev, esiti = {}, {}
    for riga in _righe(cartella / "previsione.jsonl"):
        rec = json.loads(riga)
        d = rec["dati"]
        if "chiude" in d:
            esiti[d["chiude"]] = d["esito"]
        else:
            prev[rec["id"]] = d
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
    elif a == ["verifica"]:
        p = verifica()
        print("\n".join(p) if p else "journal integro")
        return 1 if p else 0
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
