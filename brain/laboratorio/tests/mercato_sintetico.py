"""Mercato SINTETICO per le prove del percorso di verifica (#127, DGS-15). Solo dati inventati, nessuna rete.

Ogni seduta di Londra (feriale, fuori dalle festività inglesi) ha gli stessi minuti dalle 08:00 alle 16:45 di Londra:
- range d'apertura 08:00–08:30 di 5,000 USD attorno a P = 1.200,000 (BID); ASK = BID + 0,300;
- la candela 08:30–08:45 chiude a P + 3,000, sopra il massimo del range: segnale d'acquisto;
- dalle 08:46 il prezzo va a P + 13,000 (giornata «vinta»: tocca il target di 1,5 R) oppure a P − 3,000 (giornata
  «persa»: tocca lo stop), e resta lì fino alla fine della sessione.
Con le regole di H-002 (orb_londra, variante V-T) una giornata vinta vale +1,42236 R e una persa −1,08054 R; le prime
20 sedute di una lettura servono da storia (mediane), quindi la scheda dichiara le date accessorie.
Fine settimana e festività hanno il file vuoto. Ogni file finisce nel registro dello scaricamento, con la sua impronta,
come fa `scarica_cache`.
"""
import csv
import hashlib
import lzma
import random
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Dict, Iterable, List

from brain.dati.pipeline import dukascopy as DK
from brain.laboratorio.simulatori import orb_londra as O

P = 1_200_000                      # prezzo × 10^3
SPREAD = 300
CAMPI = ("ora_utc", "giorno", "lato", "url", "http", "esito", "byte", "sha256", "tentativi")
R_VINTA = 1.42236
R_PERSA = -1.08054


def seduta(g: date) -> bool:
    return g.weekday() < 5 and g not in O.esclusi(g.year)


def sedute(inizio: date, fine: date) -> List[date]:
    out, g = [], inizio
    while g <= fine:
        if seduta(g):
            out.append(g)
        g += timedelta(days=1)
    return out


def fine_per_sedute(inizio: date, n: int) -> date:
    """L'ultima data di una finestra che, da `inizio`, contiene esattamente `n` sedute."""
    g, k = inizio, 0
    while True:
        if seduta(g):
            k += 1
            if k == n:
                return g
        g += timedelta(days=1)


def _minuti(g: date, vinta: bool) -> List[tuple]:
    mezzanotte = datetime(g.year, g.month, g.day, tzinfo=timezone.utc)
    out = []
    t = O._utc(g, time(8, 0))
    fine = O._utc(g, time(16, 45))
    while t < fine:
        sec = int((t - mezzanotte).total_seconds())
        locale = t.astimezone(O.LONDRA).time()
        if locale < time(8, 30):
            o = c = P
            lo, hi = P - 2_500, P + 2_500
        elif locale < time(8, 46):
            o = c = P + 3_000
            lo, hi = o - 100, o + 100
        else:
            o = c = P + 13_000 if vinta else P - 3_000
            lo, hi = o - 100, o + 100
        out.append((sec, o, c, lo, hi, 1.0))
        t += timedelta(minutes=1)
    return out


def _bi5(record: Iterable[tuple], spread: int = 0) -> bytes:
    grezzo = b"".join(DK.RECORD.pack(s, o + spread, c + spread, lo + spread, hi + spread, v) for s, o, c, lo, hi, v in record)
    return lzma.compress(grezzo, format=lzma.FORMAT_ALONE)


def scrivi(cache: Path, inizio: date, fine: date, p_vinta: float, seme: int, simbolo: str = "XAUUSD") -> Dict[date, bool]:
    """Scrive i file BID e ASK di ogni giorno di calendario e i due registri dello scaricamento. Restituisce, per ogni
    seduta, se è vinta (il «vero» del mercato sintetico)."""
    r = random.Random(seme)
    esiti: Dict[date, bool] = {}
    righe = {"BID": [], "ASK": []}
    for lato, cartella in (("BID", simbolo), ("ASK", f"{simbolo}_ASK")):
        (Path(cache) / cartella).mkdir(parents=True, exist_ok=True)
    g = inizio
    while g <= fine:
        if seduta(g):
            esiti[g] = r.random() < p_vinta
            minuti = _minuti(g, esiti[g])
        else:
            minuti = None
        for lato, cartella, spread in (("BID", simbolo, 0), ("ASK", f"{simbolo}_ASK", SPREAD)):
            corpo = _bi5(minuti, spread) if minuti else b""
            (Path(cache) / cartella / f"{g.isoformat()}.bi5").write_bytes(corpo)
            righe[lato].append({"ora_utc": "2026-11-22T00:00:00Z", "giorno": g.isoformat(), "lato": lato,
                                "url": DK.url_giorno(simbolo, g, lato), "http": 200,
                                "esito": "dati" if corpo else "vuoto-200", "byte": len(corpo),
                                "sha256": hashlib.sha256(corpo).hexdigest(), "tentativi": 1})
        g += timedelta(days=1)
    for lato, rr in righe.items():
        reg = Path(cache) / f"registro_scaricamento_{simbolo}_{lato}.csv"
        nuovo = not reg.exists()
        with open(reg, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=CAMPI)
            if nuovo:
                w.writeheader()
            w.writerows(rr)
    return esiti
