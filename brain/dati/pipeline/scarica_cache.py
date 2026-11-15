"""Scaricatore «solo cache» di Dukascopy: riempie la cache .bi5 di un periodo, senza aggregare e senza scrivere CSV.

Perché esiste (15/11/2026): lo scaricamento storico si era fermato allo spegnimento del Mac (BID fino al 07/06/2009,
ASK quasi assente). Il comando della pipeline completa (`dukascopy.py`) non ha una data d'inizio e aspetta anche sui
giorni già in cache; alla fine tiene in memoria i minuti di tutto il periodo e scrive un CSV a 15 minuti con i prezzi
in chiaro, che per la verifica non serve (il caricatore legge la cache). Qui:
- si scarica solo il periodo richiesto, saltando senza attese i giorni già in cache;
- ogni giorno scaricato è controllato (decodifica) e scritto in modo atomico, forzato su disco: niente file a metà;
- ogni richiesta va in un registro CSV (ora UTC, giorno, lato, URL, codice HTTP, esito, byte, SHA-256, tentativi),
  scritto e forzato su disco subito: dopo uno spegnimento il registro dice fin dove si era arrivati;
- esiti distinti: «dati», «404», «vuoto-200»; si FERMA su errore HTTP sconosciuto, file danneggiato o rete assente,
  senza scrivere quel giorno.
Non stampa mai prezzi.

Uso (dalla radice del repository; --cache = cartella che contiene XAUUSD e XAUUSD_ASK):
  python3 -s -B -m brain.dati.pipeline.scarica_cache --lato BID --inizio 2009-06-08 --fine 2023-11-11 \\
      --cache brain/dati/reali/cache_dukascopy
Codici d'uscita: 0 finito; 2 argomenti non validi; 3 rete o Dukascopy non rispondono (rilanciare più tardi lo stesso
comando: riparte dal primo giorno mancante); 4 errore HTTP sconosciuto o file danneggiato (fermarsi e segnalarlo).
"""
import argparse
import csv
import hashlib
import os
import sys
import time
import urllib.error
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

from . import dukascopy as DK

CAMPI = ("ora_utc", "giorno", "lato", "url", "http", "esito", "byte", "sha256", "tentativi")


class Fermo(Exception):
    """Errore che richiede un controllo umano: HTTP sconosciuto o file danneggiato."""


def _scrivi_atomico(percorso: Path, dati: bytes) -> None:
    tmp = percorso.with_name(f".{percorso.stem}.tmp")
    with open(tmp, "wb") as f:
        f.write(dati)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, percorso)


def _registra(registro: Path, riga: dict) -> None:
    nuovo = not registro.exists()
    registro.parent.mkdir(parents=True, exist_ok=True)
    with open(registro, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPI)
        if nuovo:
            w.writeheader()
        w.writerow(riga)
        f.flush()
        os.fsync(f.fileno())


def scarica_periodo(simbolo: str, lato: str, inizio: date, fine: date, cache: Path, registro: Path,
                    richiesta: Callable = DK.richiesta_http, pausa: Callable[[], None] = lambda: time.sleep(DK.PAUSA_S),
                    stampa=print, ora=lambda: datetime.now(timezone.utc)) -> dict:
    cache = Path(cache)
    cache.mkdir(parents=True, exist_ok=True)
    conta = {"in_cache": 0, "dati": 0, "404": 0, "vuoto-200": 0}
    g = inizio
    while g <= fine:
        f = cache / f"{g.isoformat()}.bi5"
        if f.exists():
            conta["in_cache"] += 1
            g += timedelta(days=1)
            continue
        url = DK.url_giorno(simbolo, g, lato)
        riga = {"ora_utc": ora().strftime("%Y-%m-%dT%H:%M:%SZ"), "giorno": g.isoformat(), "lato": lato, "url": url,
                "http": "", "esito": "", "byte": 0, "sha256": "", "tentativi": ""}
        try:
            codice, dati, tentativi = richiesta(url)
        except urllib.error.HTTPError as e:
            _registra(registro, dict(riga, http=e.code, esito=f"http-{e.code}"))
            raise Fermo(f"{g.isoformat()} {lato}: risposta HTTP {e.code} da Dukascopy ({url}). Fermo: segnalarlo "
                        f"prima di rilanciare") from None
        except ConnectionError:
            _registra(registro, dict(riga, esito="nessuna-risposta"))
            raise
        corpo = dati or b""
        esito = "dati" if corpo else ("404" if codice == 404 else "vuoto-200")
        riga.update(http=codice, esito=esito, byte=len(corpo), sha256=hashlib.sha256(corpo).hexdigest(),
                    tentativi=tentativi)
        if corpo:
            try:
                DK.decodifica(corpo, g, DK.SCALA[simbolo])                # solo controllo: nessun prezzo esce
            except DK.ErroreDati as e:
                _registra(registro, dict(riga, esito="danneggiato"))
                raise Fermo(f"{g.isoformat()} {lato}: file scaricato non valido ({e}). Fermo: segnalarlo") from None
        _scrivi_atomico(f, corpo)
        _registra(registro, riga)
        conta[esito] += 1
        if (g - inizio).days % 30 == 0:
            stampa(f"{g.isoformat()} {lato}: {conta}", flush=True)
        pausa()
        g += timedelta(days=1)
    stampa(f"FINITO {lato} {inizio} → {fine}: {conta}", flush=True)
    return conta


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    a.add_argument("--simbolo", default="XAUUSD", choices=sorted(DK.SCALA))
    a.add_argument("--lato", default="BID", choices=DK.LATI)
    a.add_argument("--inizio", required=True, type=date.fromisoformat)
    a.add_argument("--fine", required=True, type=date.fromisoformat)
    a.add_argument("--cache", required=True, type=Path, help="cartella che contiene XAUUSD e XAUUSD_ASK")
    a.add_argument("--registro", type=Path, help="CSV del registro (predefinito: nella cartella --cache)")
    a.add_argument("--pausa", type=float, default=DK.PAUSA_S, help="secondi fra una richiesta e l'altra")
    x = a.parse_args(argv)
    if x.fine < x.inizio:
        print(f"ERRORE: --fine {x.fine} prima di --inizio {x.inizio}", file=sys.stderr)
        return 2
    cartella = x.cache / (x.simbolo if x.lato == "BID" else f"{x.simbolo}_{x.lato}")
    registro = x.registro or (x.cache / f"registro_scaricamento_{x.simbolo}_{x.lato}.csv")
    print(f"Scarico {x.simbolo} {x.lato} dal {x.inizio} al {x.fine} in {cartella}; registro {registro}", flush=True)
    try:
        scarica_periodo(x.simbolo, x.lato, x.inizio, x.fine, cartella, registro,
                        pausa=lambda: time.sleep(x.pausa))
    except ConnectionError as e:
        print(f"RETE O DUKASCOPY NON RISPONDONO: {e}. Rilanciare più tardi lo stesso comando.", file=sys.stderr, flush=True)
        return 3
    except Fermo as e:
        print(f"FERMO: {e}", file=sys.stderr, flush=True)
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
