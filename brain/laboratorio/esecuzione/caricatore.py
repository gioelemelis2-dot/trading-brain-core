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
QUOTA_TERZO = 0.25                          # PROVVISORIA (#63): minuti minimi in ciascun terzo della sessione


def _completo(tempi, giorno: date, corto: bool) -> bool:
    """Metà dei minuti della sessione e almeno un quarto in ciascun terzo (#63: 263 minuti tutti nel pomeriggio non
    fanno un giorno completo); nelle vigilie (chiusura anticipata) basta il primo terzo, il mattino."""
    a, b = _utc(giorno, SESSIONE[0]), _utc(giorno, SESSIONE[1])
    durata = (b - a) / 3
    terzi = [0, 0, 0]
    for t in set(tempi):                                            # #85: minuti distinti
        if a <= t < b:
            terzi[min(2, int((t - a) / durata))] += 1
    minimo_terzo = math.ceil(QUOTA_TERZO * MINUTI_SESSIONE / 3)
    if corto:
        return terzi[0] >= minimo_terzo
    return sum(terzi) >= math.ceil(QUOTA_SESSIONE * MINUTI_SESSIONE) and all(n >= minimo_terzo for n in terzi)


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


class FileDifforme(ValueError):
    """DGS-14 Q1: un file della finestra mancante, non previsto o con byte diversi dal manifesto autorizzato."""


def _leggi_cache(cartella: Path, inizio: date, fine: date, simbolo: str, impronta, lato: str = "", attese=None):
    """Minuti, giorni senza file, giorni feriali con il file vuoto o senza minuti (fuori dalle chiusure note), giorni
    feriali con meno della QUOTA_SESSIONE dei minuti della sessione di Londra (fuori da chiusure e vigilie: #49, un
    solo minuto a mezzanotte non fa un giorno con i dati). Aggiorna `impronta` con nome e SHA-256 di ogni file letto."""
    out: Dict[datetime, Quota] = {}
    mancanti = 0
    feriali_vuoti = []
    incompleti = []
    giorno = inizio
    while giorno <= fine:
        f = Path(cartella) / f"{giorno.isoformat()}.bi5"
        if f.is_symlink():                                       # #126: un giorno «prestato» da un'altra cartella
            raise ValueError(f"{f}: collegamento simbolico nella cache, non un file scaricato")
        atteso = None if attese is None else attese.get((lato, giorno.isoformat()))
        if attese is not None and atteso is None:
            raise FileDifforme(f"{lato} {giorno}: giorno letto ma assente dal manifesto autorizzato")
        if not f.exists():
            if atteso is not None:
                raise FileDifforme(f"{lato} {giorno}: file del manifesto sparito dopo l'autorizzazione")
            mancanti += 1
        else:
            dati = f.read_bytes()                                    # gli STESSI byte: impronta, poi decodifica
            if atteso is not None and hashlib.sha256(dati).hexdigest() != atteso:
                raise FileDifforme(f"{lato} {giorno}: byte diversi dal manifesto autorizzato")
            _aggiorna_impronta(impronta, cartella, giorno, dati)
            minuti = DK.decodifica(dati, giorno, DK.SCALA[simbolo]) if dati else []
            for t, o, h, l, c, _v in minuti:
                out[t] = (float(o), float(h), float(l), float(c))
            if giorno.weekday() < 5 and giorno not in chiusure_note(giorno.year):
                if not minuti:
                    feriali_vuoti.append(giorno.isoformat())
                elif not _completo([m[0] for m in minuti], giorno, giorno in giorni_corti(giorno.year)):
                    incompleti.append(giorno.isoformat())
        giorno += timedelta(days=1)
    return out, mancanti, feriali_vuoti, incompleti


def _cartelle_distinte(cartella_bid: Path, cartella_ask: Path) -> None:
    """#126 (Gemini R18-02): BID e ASK devono stare in due cartelle vere e diverse."""
    for c in (cartella_bid, cartella_ask):
        if c.is_symlink():
            raise ValueError(f"{c}: la cartella della cache è un collegamento simbolico")
    if cartella_bid.resolve() == cartella_ask.resolve():
        raise ValueError(f"BID e ASK nella stessa cartella ({cartella_bid}): lo spread sarebbe zero")


def _ask_diverso_dal_bid(bid: Dict[datetime, Quota], ask: Dict[datetime, Quota]) -> None:
    """#126: un giorno in cui ogni minuto dell'ASK è identico al BID è una copia (sui dati veri lo spread non è mai
    zero per un giorno intero): si ferma il caricamento e si indica il giorno."""
    giorni: Dict[date, bool] = {}
    for t, q in ask.items():
        if t in bid:
            g = t.date()
            giorni[g] = giorni.get(g, True) and bid[t] == q
    copiati = sorted(g.isoformat() for g, uguale in giorni.items() if uguale)
    if copiati:
        raise ValueError(f"ASK identico al BID in {len(copiati)} giorni ({', '.join(copiati[:5])}): "
                         "copia o collegamento della cache BID")


def carica(cartella_bid: Path, cartella_ask: Path, inizio: date, fine: date, modalita: str,
           registro: Optional[Path] = None, ipotesi: Optional[str] = None, scheda: Optional[Path] = None,
           simbolo: str = "XAUUSD", attese=None) -> Tuple[Dict[datetime, Quota], Dict[datetime, Quota], dict]:
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
    _cartelle_distinte(Path(cartella_bid), Path(cartella_ask))
    impronta = hashlib.sha256()
    bid, mb, vb, ib = _leggi_cache(cartella_bid, inizio, fine, simbolo, impronta, "BID", attese)
    ask, ma, va, ia = _leggi_cache(cartella_ask, inizio, fine, simbolo, impronta, "ASK", attese)
    _ask_diverso_dal_bid(bid, ask)
    info = {"modalita": modalita, "inizio": inizio.isoformat(), "fine": fine.isoformat(),
            "giorni_bid_mancanti": mb, "giorni_ask_mancanti": ma, "minuti_bid": len(bid), "minuti_ask": len(ask),
            "feriali_vuoti_bid": vb, "feriali_vuoti_ask": va, "feriali_incompleti_bid": ib,
            "feriali_incompleti_ask": ia, "dati_sha256": impronta.hexdigest(), "byte_verificati": attese is not None}
    return bid, ask, info
