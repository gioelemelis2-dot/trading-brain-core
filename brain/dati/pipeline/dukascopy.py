"""Gate 2: storico Dukascopy XAU/USD (candele BID da 1 minuto) aggregato a 15 minuti, ingestione e sigillo OOS.

Uso (dalla RADICE del repository, sul proprio computer; dal container cloud il server rifiuta le richieste):
  python3 -s -B -m brain.dati.pipeline.dukascopy --anni 3

Cosa fa, in ordine:
1. scarica, un giorno alla volta, https://datafeed.dukascopy.com/datafeed/XAUUSD/AAAA/MM/GG/BID_candles_min_1.bi5
   (MM da 00 a 11), con pause fra le richieste, nuovi tentativi su 429/5xx e una cache locale dei file grezzi;
2. decodifica le candele da 1 minuto, scarta i minuti senza scambi (volume 0) e aggrega a 15 minuti (UTC);
3. CONTROLLA i dati e si ferma se non tornano: OHLC incoerenti, prezzi fuori dalla banda plausibile dell'anno o
   salti oltre il 25% fra candele consecutive (segni di una scala sbagliata), ordine non crescente; classifica i
   buchi temporali (pausa giornaliera, fine settimana, festività) e si ferma sui buchi anomali in orario di
   mercato, salvo --accetta-buchi;
4. scrive brain/dati/reali/XAUUSD_15m.csv (escluso da git) e XAUUSD_15m.meta.json (fonte, periodo, SHA-256, buchi);
5. ingestione con DataIngestionPipeline;
6. SOLO con --partizione FILE (DA-26 decisa): partizione per date in blocchi con embargo (partizione_date.py),
   commitment.json in brain/dati/reali/partizioni/XAUUSD_15m_date/, nonce segreto FUORI dal repository. Il periodo
   da scaricare è preso dal file. Senza --partizione nulla viene sigillato (la vecchia divisione 70/30 per numero
   di candele non c'è più: rilievo di Gemini G-20261113-01).

Esempio: prima solo dati (--anni 15), poi, decisa la partizione, lo stesso comando con --partizione: i giorni già
scaricati vengono dalla cache.

Formato dei file (NON documentato ufficialmente da Dukascopy: dedotto, e per questo controllato al punto 3):
LZMA; record di 24 byte big-endian = secondi dall'inizio del giorno UTC (int32), open, close, low, high (int32,
prezzo × SCALA), volume (float32). Per XAUUSD la SCALA è 1000 (0,001 USD).
"""
from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import lzma
import os
import platform
import struct
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

URL = "https://datafeed.dukascopy.com/datafeed/{simbolo}/{anno:04d}/{mese0:02d}/{giorno:02d}/BID_candles_min_1.bi5"
SCALA = {"XAUUSD": 3}                       # cifre decimali: prezzo = intero × 10^-3
RECORD = struct.Struct(">iiiiif")           # secondi, open, close, low, high, volume
QUINDICI = timedelta(minutes=15)
# Bande di prezzo plausibili per anno: (primo anno, ultimo anno, minimo, massimo). STIMA di Claude, larga apposta:
# servono solo a scoprire una scala sbagliata (×10 o ÷10 esce dalla banda di ogni periodo), non a validare i
# prezzi, che si confrontano con una seconda fonte (MT5). Un anno senza banda ferma: la banda si aggiunge a mano.
BANDE = {"XAUUSD": ((2003, 2007, Decimal("200"), Decimal("1200")),
                    (2008, 2012, Decimal("500"), Decimal("2500")),
                    (2013, 2019, Decimal("900"), Decimal("2200")),
                    (2020, 2030, Decimal("1200"), Decimal("10000")))}
SALTO_MAX = Decimal("1.25")                 # chiusura -> apertura successiva: oltre +25% o sotto -20% si ferma
RADICE = Path(__file__).resolve().parents[3]
PAUSA_S = 1.5                               # Dukascopy limita le richieste: meglio lenti che bloccati


class ErroreDati(ValueError):
    """Dati che non tornano: ci si ferma, non si corregge in silenzio."""


# ---------------------------------------------------------------------------------------------------------------
# Scaricamento
# ---------------------------------------------------------------------------------------------------------------
def url_giorno(simbolo: str, giorno: date) -> str:
    return URL.format(simbolo=simbolo, anno=giorno.year, mese0=giorno.month - 1, giorno=giorno.day)


def scarica_http(url: str, tentativi: int = 10, attesa: Callable[[float], None] = time.sleep,
                 apri=urllib.request.urlopen) -> Optional[bytes]:
    """Contenuto dell'URL; None se il giorno non esiste (404) o è vuoto. Nuovi tentativi con attesa crescente su
    429/5xx ed errori di rete (rispettando Retry-After): 5, 10, 20, … secondi fino a 5 minuti, circa 20 minuti in
    tutto prima di arrendersi. User-Agent generico: nessun dato personale."""
    richiesta = urllib.request.Request(url, headers={"User-Agent": "trading-brain-dati/1.0"})
    for n in range(tentativi):
        try:
            with apri(richiesta, timeout=60) as r:
                dati = r.read()
            return dati or None
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code != 429 and e.code < 500:
                raise
            ritardo = float(e.headers.get("Retry-After") or 0) if e.headers else 0.0
        except (urllib.error.URLError, OSError, http.client.HTTPException):   # rete, timeout (anche socket.timeout
            # di Python 3.9, che non è un TimeoutError), connessioni chiuse, risposte troncate
            ritardo = 0.0
        attesa(max(ritardo, min(300.0, 5.0 * 2 ** n)))
    raise ConnectionError(f"{url}: nessuna risposta valida dopo {tentativi} tentativi")


def scarica_giorno(simbolo: str, giorno: date, cache: Optional[Path], scarica: Callable[[str], Optional[bytes]]):
    """bi5 grezzo del giorno, dalla cache se presente. Un giorno senza dati viene annotato in cache come vuoto."""
    if cache is not None:
        f = cache / f"{giorno.isoformat()}.bi5"
        if f.exists():
            return f.read_bytes() or None
    try:
        dati = scarica(url_giorno(simbolo, giorno))
    except ConnectionError as e:                     # nell'URL i mesi partono da 00: si dichiara la data vera
        raise ConnectionError(f"giorno {giorno.isoformat()} (nell'URL il mese parte da 00): {e}") from None
    if cache is not None:
        cache.mkdir(parents=True, exist_ok=True)
        tmp = cache / f".{giorno.isoformat()}.tmp"
        tmp.write_bytes(dati or b"")
        os.replace(tmp, cache / f"{giorno.isoformat()}.bi5")
    return dati


# ---------------------------------------------------------------------------------------------------------------
# Decodifica e aggregazione
# ---------------------------------------------------------------------------------------------------------------
def decodifica(dati: bytes, giorno: date, cifre: int) -> List[tuple]:
    """Minuti con scambi: (orario UTC, open, high, low, close, volume). Prezzi in Decimal esatti (intero × 10^-cifre).
    Solleva ErroreDati su file troncato o OHLC incoerente (per esempio campi in un ordine diverso dal previsto)."""
    grezzo = lzma.decompress(dati)
    if len(grezzo) % RECORD.size:
        raise ErroreDati(f"{giorno}: {len(grezzo)} byte, non multiplo di {RECORD.size} (file troncato o formato diverso)")
    inizio = datetime(giorno.year, giorno.month, giorno.day, tzinfo=timezone.utc)
    minuti = []
    for sec, o, c, lo, hi, vol in RECORD.iter_unpack(grezzo):
        if vol <= 0:
            continue                                           # minuto senza scambi (mercato chiuso o fermo)
        o, c, lo, hi = (Decimal(x).scaleb(-cifre) for x in (o, c, lo, hi))
        if not (lo <= min(o, c) and hi >= max(o, c)):
            raise ErroreDati(f"{giorno} +{sec}s: OHLC incoerente (o={o} h={hi} l={lo} c={c})")
        minuti.append((inizio + timedelta(seconds=sec), o, hi, lo, c, Decimal(repr(round(vol, 6)))))
    return minuti


def aggrega(minuti: List[tuple], passo: timedelta = QUINDICI) -> List[dict]:
    """Candele da `passo` allineate all'ora UTC: open del primo minuto, high massimo, low minimo, close dell'ultimo,
    volume sommato. Solo intervalli con almeno un minuto scambiato."""
    secondi = int(passo.total_seconds())
    gruppi: Dict[datetime, List[tuple]] = {}
    for m in sorted(minuti, key=lambda x: x[0]):
        t = m[0]
        ts = int(t.timestamp())
        gruppi.setdefault(datetime.fromtimestamp(ts - ts % secondi, tz=timezone.utc), []).append(m)
    return [{"open_time": t, "close_time": t + passo, "open": g[0][1], "high": max(x[2] for x in g),
             "low": min(x[3] for x in g), "close": g[-1][4], "volume": sum((x[5] for x in g), Decimal(0))}
            for t, g in sorted(gruppi.items())]


# ---------------------------------------------------------------------------------------------------------------
# Controlli
# ---------------------------------------------------------------------------------------------------------------
def classifica_buco(fine: datetime, inizio_successivo: datetime) -> str:
    """Tipo di buco fra la chiusura di una candela e l'apertura della successiva. «Fine settimana» solo se il buco
    contiene un SABATO UTC intero (un buco che comincia domenica sera e copre il lunedì non lo è)."""
    durata = inizio_successivo - fine
    mezzanotte = datetime(fine.year, fine.month, fine.day, tzinfo=fine.tzinfo)
    if fine > mezzanotte:
        mezzanotte += timedelta(days=1)
    sabato = mezzanotte + timedelta(days=(5 - mezzanotte.weekday()) % 7)
    if inizio_successivo >= sabato + timedelta(days=1) and durata <= timedelta(days=4):
        return "fine settimana"
    if durata <= timedelta(hours=2) and 20 <= fine.hour <= 23:
        return "pausa giornaliera"
    if durata > timedelta(hours=2):
        return "festività o chiusura lunga (da verificare)"
    return "ANOMALO (in orario di mercato)"


def banda(simbolo: str, anno: int) -> Tuple[Decimal, Decimal]:
    for primo, ultimo, minimo, massimo in BANDE.get(simbolo, ()):
        if primo <= anno <= ultimo:
            return minimo, massimo
    raise ErroreDati(f"{simbolo}: nessuna banda di prezzo plausibile per il {anno} (aggiungerla in BANDE)")


def controlla(candele: List[dict], simbolo: str = "XAUUSD") -> dict:
    """Solleva ErroreDati su prezzi fuori dalla banda dell'anno, salti di scala fra candele consecutive, OHLC
    incoerenti o ordine non crescente. Restituisce il rapporto sui buchi (conteggi per tipo ed elenco dei non
    ordinari)."""
    if not candele:
        raise ErroreDati("nessuna candela")
    buchi: Dict[str, int] = {}
    elenco = []
    for i, c in enumerate(candele):
        prezzo_min, prezzo_max = banda(simbolo, c["open_time"].year)
        for k in ("open", "high", "low", "close"):
            if not prezzo_min <= c[k] <= prezzo_max:
                raise ErroreDati(f"{c['open_time'].isoformat()}: {k} = {c[k]} fuori da [{prezzo_min}; {prezzo_max}] "
                                 f"(scala o strumento sbagliati?)")
        if not (c["low"] <= min(c["open"], c["close"]) and c["high"] >= max(c["open"], c["close"])):
            raise ErroreDati(f"{c['open_time'].isoformat()}: OHLC incoerente")
        if i:
            p = candele[i - 1]
            if c["open_time"] < p["close_time"]:
                raise ErroreDati(f"{c['open_time'].isoformat()}: ordine non crescente o sovrapposizione")
            rapporto = c["open"] / p["close"]
            if rapporto > SALTO_MAX or rapporto < 1 / SALTO_MAX:
                raise ErroreDati(f"{c['open_time'].isoformat()}: salto da {p['close']} a {c['open']} fra candele "
                                 f"consecutive (scala sbagliata in un giorno?)")
            if c["open_time"] > p["close_time"]:
                tipo = classifica_buco(p["close_time"], c["open_time"])
                buchi[tipo] = buchi.get(tipo, 0) + 1
                if tipo not in ("fine settimana", "pausa giornaliera"):
                    elenco.append({"da": p["close_time"].isoformat(), "a": c["open_time"].isoformat(), "tipo": tipo})
    return {"buchi_per_tipo": buchi, "buchi_da_verificare": elenco,
            "anomali": sum(1 for b in elenco if b["tipo"].startswith("ANOMALO"))}


# ---------------------------------------------------------------------------------------------------------------
# Scrittura, ingestione e partizione
# ---------------------------------------------------------------------------------------------------------------
def _z(t: datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def scrivi_csv(candele: List[dict], path: Path) -> str:
    """CSV nel formato di DataIngestionPipeline; restituisce lo SHA-256 del file."""
    righe = ["open_time,close_time,open,high,low,close,volume"]
    righe += [f"{_z(c['open_time'])},{_z(c['close_time'])},{c['open']},{c['high']},{c['low']},{c['close']},"
              f"{c['volume']}" for c in candele]
    testo = "\n".join(righe) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(testo, encoding="utf-8")
    os.replace(tmp, path)
    return hashlib.sha256(testo.encode("utf-8")).hexdigest()


def periodo_da_partizione(partizione: dict) -> Tuple[date, date]:
    """Primo e ultimo giorno da scaricare: dall'inizio del primo blocco al giorno prima della fine (esclusa)
    dell'ultimo."""
    from .partizione_date import valida
    blocchi = valida(partizione)
    return blocchi[0]["inizio_utc"].date(), blocchi[-1]["fine_utc"].date() - timedelta(days=1)


def esegui(simbolo: str, inizio: date, fine: date, cartella_reali: Path, cartella_nonce: Path,
           scarica: Callable[[str], Optional[bytes]], cache: Optional[Path], accetta_buchi: bool = False,
           pausa: Callable[[], None] = lambda: time.sleep(PAUSA_S), stampa=print,
           partizione: Optional[dict] = None, partizione_sha256: Optional[str] = None) -> dict:
    """Pipeline completa del Gate 2. Restituisce il riepilogo (scritto anche nel file .meta.json). Sigilla solo
    se `partizione` è data (DA-26)."""
    from .ingestion import DataIngestionPipeline
    from . import partizione_date

    if partizione is not None:
        partizione_date.valida(partizione)
        if partizione["simbolo"] != simbolo:
            raise ErroreDati(f"partizione per {partizione['simbolo']}, dati di {simbolo}")
        if not isinstance(partizione_sha256, str):
            raise ValueError("partizione_sha256 obbligatorio con la partizione")

    cifre = SCALA[simbolo]
    minuti, giorni_vuoti, giorno = [], 0, inizio
    while giorno <= fine:
        dati = scarica_giorno(simbolo, giorno, cache, scarica)
        if dati:
            minuti += decodifica(dati, giorno, cifre)
        else:
            giorni_vuoti += 1
        if giorno.toordinal() % 30 == 0:
            stampa(f"  {giorno.isoformat()}: {len(minuti)} minuti finora")
        giorno += timedelta(days=1)
        pausa()
    candele = aggrega(minuti)
    rapporto = controlla(candele, simbolo)
    if rapporto["anomali"] and not accetta_buchi:
        raise ErroreDati(f"{rapporto['anomali']} buchi anomali in orario di mercato (vedi elenco): fermo. "
                         f"Primi: {rapporto['buchi_da_verificare'][:5]}. Per procedere comunque: --accetta-buchi")
    csv_path = cartella_reali / f"{simbolo}_15m.csv"
    sha_csv = scrivi_csv(candele, csv_path)

    adesso = datetime.now(timezone.utc)
    pipeline = DataIngestionPipeline(simbolo, "15m", max_allowed_utc=adesso, max_gap_seconds=6 * 86400)
    validate = pipeline.parse_csv_stream(csv_path)
    if len(validate) != len(candele):
        raise ErroreDati("l'ingestione non ha riletto tutte le candele scritte")
    if partizione is None:
        info_partizione: object = "non decisa (DA-26): nessun sigillo. Rilanciare con --partizione FILE"
    else:
        out_dir = cartella_reali / "partizioni" / f"{simbolo}_15m_date"
        comm = partizione_date.partiziona(validate, partizione, out_dir, cartella_nonce, partizione_sha256)
        info_partizione = {
            "partizione_sha256": partizione_sha256, "embargo_giorni": comm["embargo_giorni"],
            "candele_escluse": comm["candele_escluse"],
            "blocchi": [{k: b[k] for k in ("nome", "ruolo", "inizio", "fine", "candele", "prima_utc", "ultima_utc")}
                        for b in comm["blocchi"]],
            "commitment_json_sha256": hashlib.sha256((out_dir / "commitment.json").read_bytes()).hexdigest(),
        }
    meta = {
        "schema": "dati-reali-meta/1", "simbolo": simbolo, "timeframe": "15m", "lato": "BID",
        "fonte": URL.replace("{simbolo}", simbolo), "scala_prezzi": f"intero × 10^-{cifre}",
        "scaricato_utc": _z(adesso), "python": platform.python_version(),
        "periodo_richiesto": [inizio.isoformat(), fine.isoformat()], "giorni_senza_dati": giorni_vuoti,
        "minuti_scambiati": len(minuti), "candele_15m": len(candele),
        "prima_candela_utc": _z(candele[0]["open_time"]), "ultima_candela_utc": _z(candele[-1]["close_time"]),
        "csv": csv_path.name, "csv_sha256": sha_csv, "controlli": rapporto, "partizione": info_partizione,
        "licenza": "da verificare nei termini d'uso di Dukascopy: per questo il CSV resta fuori da git",
    }
    meta_path = cartella_reali / f"{simbolo}_15m.meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return meta


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("--simbolo", default="XAUUSD", choices=sorted(SCALA))
    a.add_argument("--anni", type=float, default=3.0)
    a.add_argument("--fine", help="ultimo giorno (AAAA-MM-GG, UTC); predefinito: ieri")
    a.add_argument("--nonce-dir", default=str(Path.home() / ".trading_brain" / "nonce"),
                   help="cartella del nonce segreto del sigillo OOS: FUORI dal repository")
    a.add_argument("--accetta-buchi", action="store_true", help="procedi anche con buchi anomali (elencati nel meta)")
    a.add_argument("--pausa", type=float, default=PAUSA_S, help="secondi fra una richiesta e l'altra")
    a.add_argument("--partizione", help="file TOML della partizione per date (DA-26): periodo e blocchi da sigillare")
    x = a.parse_args(argv)
    from . import partizione_date
    partizione = sha_partizione = None
    if x.partizione:
        try:
            partizione, sha_partizione = partizione_date.leggi(Path(x.partizione))
            inizio, fine = periodo_da_partizione(partizione)
        except (OSError, ValueError) as e:
            print(f"ERRORE nel file di partizione: {e}", file=sys.stderr)
            return 2
    else:
        fine = date.fromisoformat(x.fine) if x.fine else (datetime.now(timezone.utc).date() - timedelta(days=1))
        inizio = fine - timedelta(days=int(round(365.25 * x.anni)))
    reali = RADICE / "brain" / "dati" / "reali"
    nonce = Path(x.nonce_dir).expanduser() / f"{x.simbolo}_15m_date"
    if RADICE in nonce.resolve().parents:
        print("ERRORE: il nonce deve stare fuori dal repository", file=sys.stderr)
        return 2
    print(f"Gate 2: {x.simbolo} 15m dal {inizio} al {fine} (Dukascopy, BID). Cache: {reali / 'cache_dukascopy'}")
    try:
        meta = esegui(x.simbolo, inizio, fine, reali, nonce, scarica_http, reali / "cache_dukascopy" / x.simbolo,
                      accetta_buchi=x.accetta_buchi, pausa=lambda: time.sleep(x.pausa),
                      partizione=partizione, partizione_sha256=sha_partizione)
    except FileExistsError as e:
        print(f"FERMO: esiste già un nonce ({e.filename}). Un nuovo sigillo renderebbe inverificabile quello vecchio: "
              f"non cancellarlo; usare un'altra --nonce-dir solo se il vecchio sigillo non è mai stato pubblicato.",
              file=sys.stderr)
        return 2
    except ErroreDati as e:
        print(f"FERMO, dati non validi: {e}", file=sys.stderr)
        return 1
    except ConnectionError as e:
        print(f"DUKASCOPY NON RISPONDE: {e}\nRilanciare più tardi lo stesso comando: i giorni già scaricati restano "
              f"in cache e non vengono richiesti di nuovo.", file=sys.stderr)
        return 3
    print(json.dumps({k: meta[k] for k in ("candele_15m", "prima_candela_utc", "ultima_candela_utc", "csv_sha256",
                                           "partizione")}, ensure_ascii=False, indent=2))
    print(f"Buchi: {meta['controlli']['buchi_per_tipo']}; da verificare: {len(meta['controlli']['buchi_da_verificare'])}")
    if partizione is None:
        print("Nessun sigillo: decidere la partizione (DA-26) e rilanciare con --partizione FILE "
              "(i dati vengono dalla cache). Non pubblicare nulla come sigillo.")
    else:
        print(f"Nonce segreto (NON versionare, NON cancellare, conservare): {nonce / 'sealed_nonce.secret'}")
        print(f"Poi, con l'autorizzazione dell'utente: git add brain/dati/reali/{x.simbolo}_15m.meta.json "
              f"brain/dati/reali/partizioni/{x.simbolo}_15m_date/commitment.json {x.partizione}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
