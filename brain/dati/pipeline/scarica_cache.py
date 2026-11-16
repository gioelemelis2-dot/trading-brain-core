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
  senza scrivere quel giorno;
- con --continua-su-http un errore HTTP sconosciuto (es. 403) si registra («http-<codice>»), il giorno resta SENZA
  file (quindi «mancante» per controlla_cache, mai scambiato per «nessun dato») e si va avanti; ci si ferma comunque
  dopo 20 errori HTTP di fila, segno di un blocco vero e non di un giorno isolato;
- alla ripresa ogni file già in cache è controllato (decodifica): uno rovinato (spegnimento improvviso) si mette da
  parte come `.<giorno>.rovinato` e si riscarica; uno buono senza riga nel registro (interruzione fra scrittura e
  registrazione) si registra come «in-cache-non-registrato» (#53, rilievo R12bis-B-02);
- risposte con codici diversi da 200, 204 e 404 si trattano come errori HTTP; i vuoti si registrano col codice vero
  («vuoto-200», «vuoto-204», #54);
- con --riprova-vuoti i giorni feriali salvati vuoti si richiedono di nuovo (un 404 temporaneo non resta per sempre,
  #55).
Non stampa mai prezzi.

Uso (dalla radice del repository; --cache = cartella che contiene XAUUSD e XAUUSD_ASK):
  python3 -s -B -m brain.dati.pipeline.scarica_cache --lato BID --inizio 2009-06-08 --fine 2023-11-11 \\
      --cache brain/dati/reali/cache_dukascopy
Codici d'uscita: 0 finito; 2 argomenti non validi; 3 rete o Dukascopy non rispondono (rilanciare più tardi lo stesso
comando: riparte dal primo giorno mancante); 4 errore HTTP sconosciuto o file danneggiato (fermarsi e segnalarlo);
5 finito, ma con giorni in errore HTTP (solo con --continua-su-http: segnalare il registro; i giorni restano mancanti).
"""
import argparse
import csv
import fcntl
import hashlib
import os
import sys
import time
import urllib.error
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

from . import dukascopy as DK

MAX_HTTP_DI_FILA = 20
CAMPI = ("ora_utc", "giorno", "lato", "url", "http", "esito", "byte", "sha256", "tentativi")


class Fermo(Exception):
    """Errore che richiede un controllo umano: HTTP sconosciuto o file danneggiato."""


def _forza(fd: int) -> None:
    """Forza su disco. Su macOS fsync lascia i dati nella cache del disco: serve F_FULLFSYNC (difetto #47, 20 giorni
    persi allo spegnimento del 16/11). Dove manca o è rifiutato (Linux, alcune cartelle), fsync."""
    if hasattr(fcntl, "F_FULLFSYNC"):
        try:
            fcntl.fcntl(fd, fcntl.F_FULLFSYNC)
            return
        except OSError:
            pass
    os.fsync(fd)


def _scrivi_atomico(percorso: Path, dati: bytes) -> None:
    tmp = percorso.with_name(f".{percorso.stem}.tmp")
    with open(tmp, "wb") as f:
        f.write(dati)
        f.flush()
        _forza(f.fileno())
    os.replace(tmp, percorso)
    cartella = os.open(percorso.parent, os.O_RDONLY)      # anche lo spostamento deve arrivare sul disco
    try:
        _forza(cartella)
    finally:
        os.close(cartella)


def _registra(registro: Path, riga: dict) -> None:
    nuovo = not registro.exists()
    registro.parent.mkdir(parents=True, exist_ok=True)
    with open(registro, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPI)
        if nuovo:
            w.writeheader()
        w.writerow(riga)
        f.flush()
        _forza(f.fileno())


def _gia_registrati(registro: Path) -> set:
    if not Path(registro).exists():
        return set()
    with open(registro, encoding="utf-8", newline="") as f:
        return {r["giorno"] for r in csv.DictReader(f)
                if r.get("esito") in ("dati", "404", "in-cache-non-registrato") or (r.get("esito") or "").startswith("vuoto-")}


def scarica_periodo(simbolo: str, lato: str, inizio: date, fine: date, cache: Path, registro: Path,
                    richiesta: Callable = None, pausa: Callable[[], None] = lambda: time.sleep(DK.PAUSA_S),
                    stampa=print, ora=lambda: datetime.now(timezone.utc), continua_su_http: bool = False,
                    riprova_vuoti: bool = False) -> dict:
    richiesta = richiesta or DK.richiesta_http       # risolta ora, non alla definizione: sostituibile nei test
    cache = Path(cache)
    cache.mkdir(parents=True, exist_ok=True)
    conta = {"in_cache": 0, "dati": 0, "404": 0, "vuoto-200": 0, "http": 0, "rovinati": 0, "registrati_dopo": 0}
    registrati = _gia_registrati(registro)
    di_fila = 0
    g = inizio
    while g <= fine:
        f = cache / f"{g.isoformat()}.bi5"
        url = DK.url_giorno(simbolo, g, lato)
        riga = {"ora_utc": ora().strftime("%Y-%m-%dT%H:%M:%SZ"), "giorno": g.isoformat(), "lato": lato, "url": url,
                "http": "", "esito": "", "byte": 0, "sha256": "", "tentativi": ""}
        if f.exists():
            corpo = f.read_bytes()
            impronta = hashlib.sha256(corpo).hexdigest()
            rovinato = False
            if corpo:
                try:
                    DK.decodifica(corpo, g, DK.SCALA[simbolo])
                except DK.ErroreDati:
                    rovinato = True
            if rovinato:                                                  # si conserva da parte e si riscarica
                os.replace(f, cache / f".{g.isoformat()}.rovinato")
                _registra(registro, dict(riga, esito="rovinato-in-cache", byte=len(corpo), sha256=impronta))
                conta["rovinati"] += 1
            elif not (riprova_vuoti and not corpo and g.weekday() < 5):
                if g.isoformat() not in registrati:
                    _registra(registro, dict(riga, esito="in-cache-non-registrato", byte=len(corpo), sha256=impronta))
                    registrati.add(g.isoformat())
                    conta["registrati_dopo"] += 1
                conta["in_cache"] += 1
                g += timedelta(days=1)
                continue
        try:
            codice, dati, tentativi = richiesta(url)
            if codice not in (200, 204, 404):                            # 206 o altro: non si accetta (#54)
                raise urllib.error.HTTPError(url, codice, "risposta inattesa", {}, None)
        except urllib.error.HTTPError as e:
            _registra(registro, dict(riga, http=e.code, esito=f"http-{e.code}"))
            if continua_su_http:
                conta["http"] += 1
                di_fila += 1
                if di_fila >= MAX_HTTP_DI_FILA:
                    raise Fermo(f"{MAX_HTTP_DI_FILA} errori HTTP di fila (ultimo {g.isoformat()} {lato}: {e.code}). "
                                f"Blocco vero: fermarsi e segnalarlo") from None
                pausa()
                g += timedelta(days=1)
                continue
            raise Fermo(f"{g.isoformat()} {lato}: risposta HTTP {e.code} da Dukascopy ({url}). Fermo: segnalarlo "
                        f"prima di rilanciare") from None
        except ConnectionError:
            _registra(registro, dict(riga, esito="nessuna-risposta"))
            raise
        corpo = dati or b""
        esito = "dati" if corpo else ("404" if codice == 404 else f"vuoto-{codice}")
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
        registrati.add(g.isoformat())
        conta[esito] = conta.get(esito, 0) + 1
        di_fila = 0
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
    a.add_argument("--continua-su-http", action="store_true",
                   help="su errore HTTP sconosciuto registra, lascia il giorno mancante e prosegue (codice 5 alla fine)")
    a.add_argument("--riprova-vuoti", action="store_true", help="richiede di nuovo i giorni feriali salvati vuoti")
    x = a.parse_args(argv)
    if x.fine < x.inizio:
        print(f"ERRORE: --fine {x.fine} prima di --inizio {x.inizio}", file=sys.stderr)
        return 2
    if x.pausa < 0:
        print(f"ERRORE: --pausa {x.pausa} negativa", file=sys.stderr)
        return 2
    cartella = x.cache / (x.simbolo if x.lato == "BID" else f"{x.simbolo}_{x.lato}")
    registro = x.registro or (x.cache / f"registro_scaricamento_{x.simbolo}_{x.lato}.csv")
    print(f"Scarico {x.simbolo} {x.lato} dal {x.inizio} al {x.fine} in {cartella}; registro {registro}", flush=True)
    try:
        conta = scarica_periodo(x.simbolo, x.lato, x.inizio, x.fine, cartella, registro,
                                pausa=lambda: time.sleep(x.pausa), continua_su_http=x.continua_su_http,
                                riprova_vuoti=x.riprova_vuoti)
    except ConnectionError as e:
        print(f"RETE O DUKASCOPY NON RISPONDONO: {e}. Rilanciare più tardi lo stesso comando.", file=sys.stderr, flush=True)
        return 3
    except Fermo as e:
        print(f"FERMO: {e}", file=sys.stderr, flush=True)
        return 4
    if conta["http"]:
        print(f"FINITO CON {conta['http']} GIORNI IN ERRORE HTTP: restano mancanti; vedere il registro {registro}",
              file=sys.stderr, flush=True)
        return 5
    return 0


if __name__ == "__main__":
    sys.exit(main())
