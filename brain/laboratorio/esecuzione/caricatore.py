"""Caricatore dei minuti BID e ASK dalle cache Dukascopy (`cache_dukascopy/XAUUSD` e `cache_dukascopy/XAUUSD_ASK`)
nel formato dei simulatori: dizionari `datetime UTC → (open, high, low, close)` in float.

Due modalità (DA-26):
- «sviluppo»: rifiuta qualunque data prima del 15/11/2023;
- «verifica»: parte solo se la scheda risulta sigillata nel registro delle prove e con la stessa impronta, e
  rifiuta qualunque data dal 15/11/2023 in poi.
"""
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple

from ...dati.pipeline import dukascopy as DK
from . import sigillo as S

INIZIO_SVILUPPO = date(2023, 11, 15)
FINE_VERIFICA = date(2023, 10, 31)          # PROVVISORIA (DA-26 «circa il 31/10/2023»): embargo chiuso (P7, A8)
MODALITA = ("sviluppo", "verifica")
Quota = Tuple[float, float, float, float]


def _leggi_cache(cartella: Path, inizio: date, fine: date, simbolo: str) -> Tuple[Dict[datetime, Quota], int]:
    out: Dict[datetime, Quota] = {}
    mancanti = 0
    giorno = inizio
    while giorno <= fine:
        f = Path(cartella) / f"{giorno.isoformat()}.bi5"
        if not f.exists():
            mancanti += 1
        else:
            dati = f.read_bytes()
            if dati:                                              # file vuoto: giorno senza dati, già annotato
                for t, o, h, l, c, _v in DK.decodifica(dati, giorno, DK.SCALA[simbolo]):
                    out[t] = (float(o), float(h), float(l), float(c))
        giorno += timedelta(days=1)
    return out, mancanti


def carica(cartella_bid: Path, cartella_ask: Path, inizio: date, fine: date, modalita: str,
           registro: Optional[Path] = None, ipotesi: Optional[str] = None, scheda: Optional[Path] = None,
           simbolo: str = "XAUUSD") -> Tuple[Dict[datetime, Quota], Dict[datetime, Quota], dict]:
    if modalita not in MODALITA:
        raise ValueError(f"modalità {modalita!r} non in {MODALITA}")
    if fine < inizio:
        raise ValueError(f"periodo vuoto: {inizio} → {fine}")
    if modalita == "sviluppo":
        if inizio < INIZIO_SVILUPPO:
            raise ValueError(f"sviluppo dal {INIZIO_SVILUPPO} in poi: {inizio} è nel periodo sigillato (DA-26)")
    else:
        if registro is None or ipotesi is None or scheda is None:
            raise S.NonSigillata("la verifica richiede registro, ipotesi e scheda sigillata")
        S.controlla_sigillo(registro, ipotesi, scheda)
        if fine > FINE_VERIFICA:
            raise ValueError(f"la verifica finisce il {FINE_VERIFICA} (poi embargo e sviluppo): {fine} è oltre")
    bid, mb = _leggi_cache(cartella_bid, inizio, fine, simbolo)
    ask, ma = _leggi_cache(cartella_ask, inizio, fine, simbolo)
    info = {"modalita": modalita, "inizio": inizio.isoformat(), "fine": fine.isoformat(),
            "giorni_bid_mancanti": mb, "giorni_ask_mancanti": ma, "minuti_bid": len(bid), "minuti_ask": len(ask)}
    return bid, ask, info
