"""Diagnosi del manifesto sui registri dello scaricamento (23/11/2026, revisione critica dopo DGS-17).

Strumento di CONTORNO: non fa parte del candidato sigillato, non decide nulla e non tocca la riserva di verifica.
Il manifesto (`esecuzione/manifesto.py`) blocca ogni finestra che ha anche una sola anomalia nei registri. Non è
mai stato confrontato con i registri VERI: il BID fino al 07/06/2009 è stato scaricato prima che esistesse il
registro per giorno, e `--riprova-vuoti` aggiunge una seconda riga valida per lo stesso giorno. Questa diagnosi
applica lo STESSO manifesto a un periodo e conta le anomalie per tipo, lato e anno; per le voci doppie dice quali
esiti si sommano (per esempio «vuoto-200+dati»). Con il controllo dei byte (predefinito) calcola anche l'impronta
di ogni file atteso e la confronta con quella del registro, senza decodificarlo: «impronta diversa», «file mancante».

Stampa e scrive SOLO conteggi e date: mai impronte, mai prezzi. Codici d'uscita: 0 nessuna anomalia, 1 anomalie,
2 argomenti non validi.
Uso (dalla radice del repository; --cache = cartella con i due registri e le cartelle XAUUSD e XAUUSD_ASK):
  python3 -s -B -m brain.laboratorio.studi.diagnosi_manifesto --cache brain/dati/reali/cache_dukascopy \\
      --inizio 2005-01-01 --fine 2023-11-11 --json diagnosi_manifesto.json
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

from ..esecuzione import manifesto as MF

DATA = re.compile(r"\d{4}-\d{2}-\d{2}")
LATO = re.compile(r"\b(ASK|BID)\b")


def _lato_e_giorno(anomalia: str):
    reg = re.search(r"nel registro (ASK|BID)", anomalia)
    lato = reg.group(1) if reg else LATO.search(anomalia).group(1)
    return lato, DATA.search(anomalia).group(0)


def _conta(d: dict, tipo: str, lato: str, giorno: str) -> None:
    anni = d["per_tipo"].setdefault(tipo, {}).setdefault(lato, {})
    anni[giorno[:4]] = anni.get(giorno[:4], 0) + 1
    d["date"].setdefault(tipo, []).append(f"{lato} {giorno}")


def diagnosi(cache: Path, simbolo: str, inizio: date, fine: date, byte: bool = True) -> dict:
    cache = Path(cache)
    m = MF.manifesto(cache, simbolo, inizio, fine)
    d = {"simbolo": simbolo, "inizio": inizio.isoformat(), "fine": fine.isoformat(), "giorni_attesi": {},
         "per_tipo": {}, "voci_doppie_esiti": {}, "date": {}, "byte_controllati": {}, "doppioni_unificati": {}}
    for _, lato, _ in MF.insieme_atteso(simbolo, inizio, fine):
        d["giorni_attesi"][lato] = d["giorni_attesi"].get(lato, 0) + 1
    esiti = {}
    for lato in MF.LATI:
        corpo = (cache / f"registro_scaricamento_{simbolo}_{lato}.csv").read_bytes()
        for r in MF._righe(corpo):
            if r.get("esito") in MF.VALIDI and r.get("lato") == lato:
                esiti.setdefault((lato, r.get("giorno")), []).append(r["esito"])
    for a in m["anomalie"]:
        tipo = a.split(":", 1)[0]
        lato, giorno = _lato_e_giorno(a)
        _conta(d, tipo, lato, giorno)
        if tipo == "voce doppia":
            chiave = "+".join(esiti.get((lato, giorno), []))
            d["voci_doppie_esiti"][chiave] = d["voci_doppie_esiti"].get(chiave, 0) + 1
    for x in m["doppioni"]:                                  # D-59: anomalia di processo, contata a parte
        anni = d["doppioni_unificati"].setdefault(x["lato"], {})
        anni[x["giorno"][:4]] = anni.get(x["giorno"][:4], 0) + 1
    if byte:
        for _, lato, giorno, _, impronta in m["elenco"]:
            f = cache / MF.CARTELLA[lato].format(simbolo=simbolo) / f"{giorno}.bi5"
            if not f.is_file():
                _conta(d, "file mancante", lato, giorno)
                continue
            d["byte_controllati"][lato] = d["byte_controllati"].get(lato, 0) + 1
            if hashlib.sha256(f.read_bytes()).hexdigest() != impronta:
                _conta(d, "impronta diversa", lato, giorno)
    d["pulito"] = not d["per_tipo"]
    return d


def tabella(d: dict) -> str:
    righe = [f"Diagnosi del manifesto {d['simbolo']} {d['inizio']} → {d['fine']}",
             f"giorni attesi per lato: {d['giorni_attesi']}; file controllati: {d['byte_controllati'] or 'nessuno'}"]
    if d["pulito"]:
        righe.append("NESSUNA ANOMALIA")
    for tipo, lati in sorted(d["per_tipo"].items()):
        for lato, anni in sorted(lati.items()):
            righe.append(f"{tipo:17} {lato}: " + ", ".join(f"{a} {n}" for a, n in sorted(anni.items())))
    for chiave, n in sorted(d["voci_doppie_esiti"].items()):
        righe.append(f"voci doppie con esiti {chiave}: {n}")
    for lato, anni in sorted(d["doppioni_unificati"].items()):
        righe.append(f"doppioni identici unificati (anomalia di processo, D-59) {lato}: "
                     + ", ".join(f"{a} {n}" for a, n in sorted(anni.items())))
    return "\n".join(righe)


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    a.add_argument("--cache", required=True, type=Path, help="cartella con i registri, XAUUSD e XAUUSD_ASK")
    a.add_argument("--inizio", required=True, type=date.fromisoformat)
    a.add_argument("--fine", required=True, type=date.fromisoformat)
    a.add_argument("--simbolo", default="XAUUSD")
    a.add_argument("--senza-byte", action="store_true", help="non calcola le impronte dei file")
    a.add_argument("--json", type=Path, help="scrive anche la diagnosi completa (solo conteggi e date)")
    x = a.parse_args(argv)
    if x.fine < x.inizio:
        print(f"ERRORE: --fine {x.fine} prima di --inizio {x.inizio}", file=sys.stderr)
        return 2
    if not x.cache.is_dir():
        print(f"ERRORE: cartella {x.cache} inesistente", file=sys.stderr)
        return 2
    d = diagnosi(x.cache, x.simbolo, x.inizio, x.fine, byte=not x.senza_byte)
    print(tabella(d))
    if x.json:
        x.json.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if d["pulito"] else 1


if __name__ == "__main__":
    sys.exit(main())
