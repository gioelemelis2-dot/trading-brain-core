"""Mercati INVENTATI per provare i programmi (dati simulati, mai reali: non servono a valutare strategie).

`mercato` genera minuti BID e ASK (ASK = BID + spread fisso) dalle 07:30 alle 17:00 di Londra dei giorni lavorativi,
con una passeggiata casuale a seme fisso. Opzioni:
- `deriva`: tendenza per minuto in tutta la giornata (mercato che sale o scende, senza vantaggio della rottura);
- `spinta`: vantaggio NOTO della rottura di Londra. Dopo la chiusura della prima candela da 15 minuti fuori dal range
  08:00–08:30 (stessa definizione della scheda H-002), il prezzo si muove di `spinta` per minuto nella direzione
  della rottura fino alla fine della giornata.
`scrivi_cache` salva i minuti nel formato .bi5 di Dukascopy, per provare anche il caricatore.
"""
import lzma
import random
from datetime import date, datetime, time, timedelta, timezone
from math import sqrt
from pathlib import Path
from typing import Dict, Tuple
from zoneinfo import ZoneInfo

from ...dati.pipeline import dukascopy as DK

LONDRA = ZoneInfo("Europe/London")
UTC = timezone.utc
Quota = Tuple[float, float, float, float]


def mercato(inizio: date, giorni: int, seme: int, sd: float = 0.5, spread: float = 0.3, spinta: float = 0.0,
            deriva: float = 0.0, prezzo: float = 2000.0) -> Tuple[Dict[datetime, Quota], Dict[datetime, Quota]]:
    rng = random.Random(seme)
    bid: Dict[datetime, Quota] = {}
    ask: Dict[datetime, Quota] = {}
    p = prezzo
    passo = sd / sqrt(3)
    for k in range(giorni):
        g = inizio + timedelta(days=k)
        if g.weekday() >= 5:
            continue
        p += rng.gauss(0.0, 5 * sd)                                 # salto della notte
        t0 = datetime.combine(g, time(7, 30), tzinfo=LONDRA).astimezone(UTC)
        alto = basso = None
        verso = 0.0
        for m in range(9 * 60 + 30):                                # 07:30 → 17:00 di Londra
            minuto = 7 * 60 + 30 + m                                # minuti dalla mezzanotte di Londra
            o = p
            percorso = [o]
            for _ in range(3):
                percorso.append(percorso[-1] + (deriva + verso * spinta) / 3 + rng.gauss(0.0, passo))
            c = percorso[-1]
            h, l = max(percorso), min(percorso)
            t = t0 + timedelta(minutes=m)
            bid[t] = (o, h, l, c)
            ask[t] = (o + spread, h + spread, l + spread, c + spread)
            p = c
            if 480 <= minuto < 510:                                 # range di apertura 08:00–08:30
                alto = h if alto is None else max(alto, h)
                basso = l if basso is None else min(basso, l)
            # chiusura di una candela da 15 minuti aperta fra le 08:30 e le 15:15 (Londra è a ore intere da UTC)
            if verso == 0.0 and 510 <= minuto <= 15 * 60 + 29 and (minuto + 1) % 15 == 0:
                verso = 1.0 if c > alto else -1.0 if c < basso else 0.0
    return bid, ask


def scrivi_cache(minuti: Dict[datetime, Quota], cartella: Path, cifre: int = 3) -> int:
    """Un file .bi5 per giorno UTC (formato Dukascopy: secondi, open, close, low, high, volume). Restituisce i file."""
    cartella = Path(cartella)
    cartella.mkdir(parents=True, exist_ok=True)
    per_giorno: Dict[date, list] = {}
    for t in sorted(minuti):
        per_giorno.setdefault(t.date(), []).append(t)
    scala = 10 ** cifre
    for g, ts in per_giorno.items():
        record = []
        for t in ts:
            o, h, l, c = (round(x * scala) for x in minuti[t])
            record.append(DK.RECORD.pack(t.hour * 3600 + t.minute * 60, o, c, l, h, 1.0))
        (cartella / f"{g.isoformat()}.bi5").write_bytes(lzma.compress(b"".join(record), format=lzma.FORMAT_ALONE))
    return len(per_giorno)
