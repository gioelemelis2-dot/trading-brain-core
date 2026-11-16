"""Caricatore dei minuti BID e ASK dalle cache Dukascopy (`cache_dukascopy/XAUUSD` e `cache_dukascopy/XAUUSD_ASK`)
nel formato dei simulatori: dizionari `datetime UTC → (open, high, low, close)` in float.

Due modalità (DA-26):
- «sviluppo»: rifiuta qualunque data prima del 15/11/2023 e, come la verifica, parte solo con la scheda sigillata;
- «verifica»: parte solo se la scheda risulta sigillata nel registro delle prove e con la stessa impronta, e
  rifiuta qualunque data dal 15/11/2023 in poi.
"""
import hashlib
import math
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple

from ...dati.pipeline import dukascopy as DK
from ...dati.pipeline.calendario import chiusure_note, giorni_corti
from ..simulatori.orb_londra import _utc
from . import sigillo as S

INIZIO_SVILUPPO = date(2023, 11, 15)
FINE_VERIFICA = date(2023, 10, 31)          # PROVVISORIA (DA-26 «circa il 31/10/2023»): embargo chiuso (P7, A8)
MODALITA = ("sviluppo", "verifica")
Quota = Tuple[float, float, float, float]


SESSIONE = (time(8, 0), time(16, 45))       # sessione di base, ora di Londra (scheda H-002 v3.1 §6)
QUOTA_SESSIONE = 0.5                        # PROVVISORIA (#49): da confermare con i conteggi dei minuti della cache vera
MINUTI_SESSIONE = 525


def _aggiorna_impronta(impronta, cartella: Path, giorno: date, dati: bytes) -> None:
    impronta.update(f"{Path(cartella).name}/{giorno.isoformat()}:{hashlib.sha256(dati).hexdigest()}\n".encode())


def impronta_cache(cartella_bid: Path, cartella_ask: Path, inizio: date, fine: date) -> str:
    """La stessa impronta `dati_sha256` del caricatore, senza decodificare: serve a controllare, al momento della
    verifica, che i dati dello sviluppo siano ancora quelli registrati (#51)."""
    impronta = hashlib.sha256()
    for cartella in (cartella_bid, cartella_ask):
        giorno = inizio
        while giorno <= fine:
            f = Path(cartella) / f"{giorno.isoformat()}.bi5"
            if f.exists():
                _aggiorna_impronta(impronta, cartella, giorno, f.read_bytes())
            giorno += timedelta(days=1)
    return impronta.hexdigest()


def _leggi_cache(cartella: Path, inizio: date, fine: date, simbolo: str, impronta):
    """Minuti, giorni senza file, giorni feriali con il file vuoto o senza minuti (fuori dalle chiusure note), giorni
    feriali con meno della QUOTA_SESSIONE dei minuti della sessione di Londra (fuori da chiusure e vigilie: #49, un
    solo minuto a mezzanotte non fa un giorno con i dati). Aggiorna `impronta` con nome e SHA-256 di ogni file letto."""
    out: Dict[datetime, Quota] = {}
    mancanti = 0
    feriali_vuoti = []
    incompleti = []
    minimo = math.ceil(QUOTA_SESSIONE * MINUTI_SESSIONE)
    giorno = inizio
    while giorno <= fine:
        f = Path(cartella) / f"{giorno.isoformat()}.bi5"
        if not f.exists():
            mancanti += 1
        else:
            dati = f.read_bytes()
            _aggiorna_impronta(impronta, cartella, giorno, dati)
            minuti = DK.decodifica(dati, giorno, DK.SCALA[simbolo]) if dati else []
            for t, o, h, l, c, _v in minuti:
                out[t] = (float(o), float(h), float(l), float(c))
            if giorno.weekday() < 5 and giorno not in chiusure_note(giorno.year):
                if not minuti:
                    feriali_vuoti.append(giorno.isoformat())
                elif giorno not in giorni_corti(giorno.year):
                    a, b = _utc(giorno, SESSIONE[0]), _utc(giorno, SESSIONE[1])
                    if sum(1 for t, *_ in minuti if a <= t < b) < minimo:
                        incompleti.append(giorno.isoformat())
        giorno += timedelta(days=1)
    return out, mancanti, feriali_vuoti, incompleti


def carica(cartella_bid: Path, cartella_ask: Path, inizio: date, fine: date, modalita: str,
           registro: Optional[Path] = None, ipotesi: Optional[str] = None, scheda: Optional[Path] = None,
           simbolo: str = "XAUUSD") -> Tuple[Dict[datetime, Quota], Dict[datetime, Quota], dict]:
    if modalita not in MODALITA:
        raise ValueError(f"modalità {modalita!r} non in {MODALITA}")
    if fine < inizio:
        raise ValueError(f"periodo vuoto: {inizio} → {fine}")
    # Il sigillo si controlla in ENTRAMBE le modalità (incidente del 14/11, difetto #41: script esterni avevano
    # letto i dati veri dello sviluppo prima del sigillo, perché qui il controllo c'era solo per la verifica).
    if registro is None or ipotesi is None or scheda is None:
        raise S.NonSigillata(f"la modalità {modalita} richiede registro, ipotesi e scheda sigillata")
    S.controlla_sigillo(registro, ipotesi, scheda)
    if modalita == "sviluppo":
        if inizio < INIZIO_SVILUPPO:
            raise ValueError(f"sviluppo dal {INIZIO_SVILUPPO} in poi: {inizio} è nel periodo sigillato (DA-26)")
    else:
        if fine > FINE_VERIFICA:
            raise ValueError(f"la verifica finisce il {FINE_VERIFICA} (poi embargo e sviluppo): {fine} è oltre")
    impronta = hashlib.sha256()
    bid, mb, vb, ib = _leggi_cache(cartella_bid, inizio, fine, simbolo, impronta)
    ask, ma, va, ia = _leggi_cache(cartella_ask, inizio, fine, simbolo, impronta)
    info = {"modalita": modalita, "inizio": inizio.isoformat(), "fine": fine.isoformat(),
            "giorni_bid_mancanti": mb, "giorni_ask_mancanti": ma, "minuti_bid": len(bid), "minuti_ask": len(ask),
            "feriali_vuoti_bid": vb, "feriali_vuoti_ask": va, "feriali_incompleti_bid": ib,
            "feriali_incompleti_ask": ia, "dati_sha256": impronta.hexdigest()}
    return bid, ask, info
