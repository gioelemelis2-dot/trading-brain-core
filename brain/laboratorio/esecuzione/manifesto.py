"""Manifesto dei dati di una finestra di verifica (DGS-14 Q1, DGS-15 punto 3), 22/11/2026.

Prima dell'autorizzazione, SENZA aprire i file della finestra:
1. si ricava dal calendario l'insieme ATTESO: un file per giorno di calendario (la cache Dukascopy ha un file per
   giorno UTC, anche nel fine settimana) per ciascun lato BID e ASK, più le date accessorie che la scheda dichiara
   (giorni prima dell'inizio letti dal simulatore; per le regole di H-002 nessuno: la sessione di Londra sta nel
   giorno UTC);
2. si confronta con i due registri dello scaricamento (`registro_scaricamento_<SIMBOLO>_<LATO>.csv`), che hanno lo
   SHA-256 di ogni file scaricato o trovato in cache. Emergono come ANOMALIE, anche se i file presenti hanno
   l'impronta giusta:
   - un giorno atteso senza una riga valida («omesso»);
   - più righe valide DISCORDANTI per lo stesso giorno e lato («voce doppia»; D-59, A1: le righe identiche in
     indirizzo, classe del contenuto, byte e impronta si unificano e restano nella traccia «doppioni», anomalia di
     processo che non blocca; un passaggio vuoto → dati blocca finché non c'è una regola di revisione esplicita);
   - una riga del lato opposto nel registro di un lato, o un indirizzo del lato opposto («lato sbagliato»);
   - un indirizzo di un altro mercato («mercato sbagliato»);
3. i giorni in quarantena (regola di qualità del consuntivo) restano nell'elenco, con lo stato «quarantena».
Il risultato è l'elenco canonico ordinato [mercato, lato, giorno, stato, sha256], la sua impronta e l'istantanea dei
registri (nome e SHA-256 del file). Va nell'impegno dell'autorizzazione (riserva/2). Dopo l'autorizzazione il
caricatore verifica, file per file, che i byte passati al decodificatore abbiano l'impronta dell'elenco.
Il manifesto legge solo i registri (nomi, date, impronte), mai i file dei dati né i prezzi.
"""
import csv
import hashlib
import io
import json
import re
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ...dati.pipeline import dukascopy as DK

LATI = ("ASK", "BID")
VALIDI = ("dati", "in-cache-non-registrato", "404", "vuoto-200", "vuoto-204")
SENZA_DATI = ("404", "vuoto-200", "vuoto-204")
CONTENUTO = ("dati", "in-cache-non-registrato")      # D-59: come è stato osservato il file, non che cosa contiene
CARTELLA = {"BID": "{simbolo}", "ASK": "{simbolo}_ASK"}


def insieme_atteso(simbolo: str, inizio: date, fine: date, accessorie: int = 0) -> List[Tuple[str, str, str]]:
    if fine < inizio:
        raise ValueError(f"finestra rovesciata {inizio} → {fine}")
    if type(accessorie) is not int or accessorie < 0:
        raise ValueError(f"date accessorie {accessorie!r}: serve un intero ≥ 0")
    giorni, g = [], inizio - timedelta(days=accessorie)
    while g <= fine:
        giorni.append(g.isoformat())
        g += timedelta(days=1)
    return sorted((simbolo, lato, x) for lato in LATI for x in giorni)


def _lato_dell_indirizzo(url: str) -> Optional[str]:
    for lato in LATI:
        if url.endswith(f"/{lato}_candles_min_1.bi5"):
            return lato
    return None


def _righe(corpo: bytes) -> List[dict]:
    return list(csv.DictReader(io.StringIO(corpo.decode("utf-8"), newline="")))


def _classe(esito: str) -> str:
    return "contenuto" if esito in CONTENUTO else esito


def _identita(r: dict) -> tuple:
    """D-59 (A1, DGS-18 Q2): fonte, mercato, lato e data (l'indirizzo), classe del contenuto, byte e impronta. Ora,
    tentativi, codice HTTP ed esito dentro la stessa classe sono provenienza, non identità."""
    return r.get("url"), _classe(r.get("esito")), str(r.get("byte")), r.get("sha256")


def impronta_elenco(elenco: list) -> str:
    testo = json.dumps(elenco, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(testo.encode("ascii")).hexdigest()


def manifesto(cache: Path, simbolo: str, inizio: date, fine: date, accessorie: int = 0,
              quarantena: Optional[Dict[str, str]] = None) -> dict:
    quarantena = dict(quarantena or {})
    atteso = insieme_atteso(simbolo, inizio, fine, accessorie)
    valide: Dict[Tuple[str, str], List[dict]] = {}
    anomalie: List[str] = []
    registri = []
    for lato in LATI:
        reg = Path(cache) / f"registro_scaricamento_{simbolo}_{lato}.csv"
        if not reg.is_file() or reg.is_symlink():
            raise ValueError(f"registro dello scaricamento mancante o non regolare: {reg.name}")
        corpo = reg.read_bytes()                     # una sola lettura: l'impronta è di ciò che si analizza
        registri.append([reg.name, hashlib.sha256(corpo).hexdigest()])
        for r in _righe(corpo):
            if r.get("esito") not in VALIDI:
                continue
            giorno, url = r.get("giorno") or "", r.get("url") or ""
            if r.get("lato") != lato:
                anomalie.append(f"lato sbagliato: riga {r.get('lato')} nel registro {lato} ({giorno})")
                continue
            if f"/{simbolo}/" not in url:
                anomalie.append(f"mercato sbagliato: {simbolo} {lato} {giorno} (indirizzo di un altro mercato)")
                continue
            if _lato_dell_indirizzo(url) != lato:
                anomalie.append(f"lato sbagliato: {simbolo} {lato} {giorno} (indirizzo {_lato_dell_indirizzo(url)})")
                continue
            try:                                                       # #147 (R19-07a): dominio, data, mercato, lato
                atteso_url = DK.url_giorno(simbolo, date.fromisoformat(giorno), lato)
            except ValueError:
                atteso_url = None
            if url != atteso_url:
                anomalie.append(f"indirizzo diverso da quello atteso: {simbolo} {lato} {giorno}")
                continue
            if not re.fullmatch(r"[0-9a-f]{64}", r.get("sha256") or ""):       # #147 (R19-07b)
                anomalie.append(f"impronta non valida: {simbolo} {lato} {giorno}")
                continue
            valide.setdefault((lato, giorno), []).append(r)
    elenco, doppioni = [], []
    for s, lato, giorno in atteso:
        righe = valide.get((lato, giorno), [])
        if len(righe) > 1:
            if len({_identita(r) for r in righe}) > 1:
                classi = {_classe(r["esito"]) for r in righe}
                motivo = ("passaggio vuoto → dati: serve una regola di revisione esplicita"
                          if "contenuto" in classi and classi & set(SENZA_DATI) else "discordanti")
                anomalie.append(f"voce doppia: {s} {lato} {giorno} ({len(righe)} righe valide, {motivo})")
                continue
            doppioni.append({"lato": lato, "giorno": giorno, "righe": len(righe), "sha256": righe[0]["sha256"],
                             "esiti": sorted({r["esito"] for r in righe})})   # D-59: traccia, non blocco
        if not righe:
            anomalie.append(f"omesso: {s} {lato} {giorno}")
            continue
        r = righe[0]
        stato = "quarantena" if giorno in quarantena else "nessun dato" if r["esito"] in SENZA_DATI else "dati"
        elenco.append([s, lato, giorno, stato, r.get("sha256") or ""])
    return {"simbolo": simbolo, "inizio": inizio.isoformat(), "fine": fine.isoformat(), "accessorie": accessorie,
            "registri": registri, "quarantena": quarantena, "elenco": elenco, "anomalie": anomalie,
            "doppioni": doppioni,
            "impronta_elenco": impronta_elenco(elenco)}


def attese(m: dict) -> Dict[Tuple[str, str], str]:
    """Per il caricatore: (lato, giorno) → SHA-256 atteso dei byte del file."""
    return {(x[1], x[2]): x[4] for x in m["elenco"]}
