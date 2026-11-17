"""Rendiconto dell'intersezione BID/ASK al minuto e dei buchi (17/11/2026; richiesta del DGS, DGS-05 P5: «i due
strumenti non bastano a dimostrare l'intersezione al minuto»).

Strumento di CONTORNO: non fa parte del candidato sigillato e non decide nulla. Per ogni seduta feriale aperta
(chiusure note escluse; vigilie a parte, solo il primo terzo come nel caricatore) confronta la griglia attesa della
sessione di Londra (08:00–16:45, 525 minuti) con i due lati della cache e conta:
- minuti COMUNI VALIDI (BID e ASK presenti, ASK ≥ BID su apertura e chiusura: il confronto avviene solo qui dentro);
- comuni non validi (ASK sotto BID), solo BID, solo ASK, mancanti su entrambi;
- minuti comuni validi per terzo, e il BUCO più lungo (minuti consecutivi non comuni-validi, bordi compresi);
- lo stato dei file per lato: ok, mancante, vuoto, illeggibile.
Per anno: sedute, file, percentili, e una GRIGLIA DIAGNOSTICA di soglie (quante sedute sarebbero ammissibili con
ciascuna). Le soglie NON sono decise qui: le decide il titolare, guardando anche l'effetto dei buchi su segnali ed
esiti (DGS-05, addendum §4). Stampa SOLO conteggi, percentuali e date: MAI prezzi.

Uso (dalla radice del repository, a scaricamento finito; --cache = cartella con XAUUSD e XAUUSD_ASK):
  python3 -s -B -m brain.laboratorio.studi.intersezione_bid_ask --cache brain/dati/reali/cache_dukascopy \\
      --inizio 2005-01-01 --fine 2023-10-31 --json intersezione.json
"""
import argparse
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path

from ...dati.pipeline import dukascopy as DK
from ...dati.pipeline.calendario import chiusure_note, giorni_corti
from ..esecuzione.caricatore import MINUTI_SESSIONE, SESSIONE
from ..simulatori.orb_londra import _utc
from .taratura_completezza import percentili

PLURALE = {"mancante": "mancanti", "vuoto": "vuoti", "illeggibile": "illeggibili"}
GRIGLIA_DIAGNOSTICA = ((0.98, 0.95, 5), (0.95, 0.90, 15), (0.90, 0.80, 30), (0.5, 0.25, MINUTI_SESSIONE))


def _leggi(f: Path, giorno: date, simbolo: str):
    if not f.exists():
        return "mancante", {}
    dati = f.read_bytes()
    if not dati:
        return "vuoto", {}
    try:
        minuti = DK.decodifica(dati, giorno, DK.SCALA[simbolo])
    except DK.ErroreDati:
        return "illeggibile", {}
    return "ok", {m[0]: (m[1], m[4]) for m in minuti}                 # (apertura, chiusura): solo per il confronto


def esamina_seduta(cache: Path, giorno: date, simbolo: str = "XAUUSD", corta: bool = False) -> dict:
    stato_b, bid = _leggi(Path(cache) / simbolo / f"{giorno.isoformat()}.bi5", giorno, simbolo)
    stato_a, ask = _leggi(Path(cache) / f"{simbolo}_ASK" / f"{giorno.isoformat()}.bi5", giorno, simbolo)
    inizio = _utc(giorno, SESSIONE[0])
    terzo = MINUTI_SESSIONE // 3
    griglia = terzo if corta else MINUTI_SESSIONE
    conta = {"comuni_validi": 0, "comuni_non_validi": 0, "solo_bid": 0, "solo_ask": 0, "mancanti": 0}
    terzi = [0, 0, 0]
    buco = buco_max = 0
    for k in range(griglia):
        t = inizio + timedelta(minutes=k)
        b, a = bid.get(t), ask.get(t)
        valido = False
        if b is not None and a is not None:
            if a[0] >= b[0] and a[1] >= b[1]:
                conta["comuni_validi"] += 1
                terzi[k // terzo] += 1
                valido = True
            else:
                conta["comuni_non_validi"] += 1
        elif b is not None:
            conta["solo_bid"] += 1
        elif a is not None:
            conta["solo_ask"] += 1
        else:
            conta["mancanti"] += 1
        buco = 0 if valido else buco + 1
        buco_max = max(buco_max, buco)
    return dict(conta, giorno=giorno.isoformat(), stati=[stato_b, stato_a], griglia=griglia,
                terzi=terzi[:1] if corta else terzi, buco_max=buco_max)


def esamina(cache: Path, inizio: date, fine: date, simbolo: str = "XAUUSD") -> dict:
    sedute, vigilie = [], []
    g = inizio
    while g <= fine:
        if g.weekday() < 5 and g not in chiusure_note(g.year):
            corta = g in giorni_corti(g.year)
            (vigilie if corta else sedute).append(esamina_seduta(cache, g, simbolo, corta))
        g += timedelta(days=1)
    anni = {}
    for s in sedute + vigilie:
        a = anni.setdefault(s["giorno"][:4], {"sedute": 0, "vigilie": 0, "con_entrambi_i_file": 0,
                                              "mancanti_bid": 0, "mancanti_ask": 0, "vuoti_bid": 0, "vuoti_ask": 0,
                                              "illeggibili_bid": 0, "illeggibili_ask": 0})
        a["vigilie" if s["griglia"] < MINUTI_SESSIONE else "sedute"] += 1
        a["con_entrambi_i_file"] += s["stati"] == ["ok", "ok"]
        for stato, lato in zip(s["stati"], ("bid", "ask")):
            if stato != "ok":
                a[f"{PLURALE[stato]}_{lato}"] += 1
    for anno, a in anni.items():
        delle = [s for s in sedute if s["giorno"][:4] == anno]
        a["quota_comuni"] = percentili([round(s["comuni_validi"] / s["griglia"], 4) for s in delle])
        a["terzo_minimo"] = percentili([min(s["terzi"]) for s in delle])
        a["buco_max"] = percentili([s["buco_max"] for s in delle])
    return {"sedute": sedute, "vigilie": vigilie, "anni": anni}


def ammissibili(e: dict, quota_seduta: float, quota_terzo: float, buco_massimo: int) -> list:
    """Sedute (e vigilie) che passerebbero queste soglie: DIAGNOSTICA, la scelta spetta al titolare."""
    fuori = []
    for s in e["sedute"] + e["vigilie"]:
        if s["comuni_validi"] < math.ceil(quota_seduta * s["griglia"] - 1e-9):
            continue
        if any(t < math.ceil(quota_terzo * (MINUTI_SESSIONE // 3) - 1e-9) for t in s["terzi"]):
            continue
        if s["buco_max"] > buco_massimo:
            continue
        fuori.append(s["giorno"])
    return sorted(fuori)


def tabella(e: dict) -> str:
    righe = ["Rendiconto dell'intersezione BID/ASK (solo conteggi; minuti comuni validi = BID e ASK presenti, "
             "ASK ≥ BID)", "",
             "| anno | sedute | vigilie | entrambi i file | mancanti B/A | vuoti B/A | illeggibili B/A | "
             "quota comuni p1/p50 | terzo minimo p1/p50 | buco max p50/max |", "|---|---|---|---|---|---|---|---|---|---|"]
    for anno, a in sorted(e["anni"].items()):
        q, t, b = a.get("quota_comuni") or {}, a.get("terzo_minimo") or {}, a.get("buco_max") or {}
        righe.append(f"| {anno} | {a['sedute']} | {a['vigilie']} | {a['con_entrambi_i_file']} | "
                     f"{a['mancanti_bid']}/{a['mancanti_ask']} | {a['vuoti_bid']}/{a['vuoti_ask']} | "
                     f"{a['illeggibili_bid']}/{a['illeggibili_ask']} | {q.get('p1', '—')}/{q.get('p50', '—')} | "
                     f"{t.get('p1', '—')}/{t.get('p50', '—')} | {b.get('p50', '—')}/{b.get('max', '—')} |")
    totale = len(e["sedute"]) + len(e["vigilie"])
    righe += ["", "Griglia DIAGNOSTICA (non è una decisione: le soglie le sceglie il titolare):", "",
              "| quota seduta | quota per terzo | buco massimo | sedute ammissibili |", "|---|---|---|---|"]
    for qs, qt, bm in GRIGLIA_DIAGNOSTICA:
        righe.append(f"| {qs} | {qt} | {bm} | {len(ammissibili(e, qs, qt, bm))} su {totale} |")
    return "\n".join(righe)


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    a.add_argument("--cache", required=True, type=Path, help="cartella che contiene XAUUSD e XAUUSD_ASK")
    a.add_argument("--inizio", required=True, type=date.fromisoformat)
    a.add_argument("--fine", required=True, type=date.fromisoformat)
    a.add_argument("--simbolo", default="XAUUSD", choices=sorted(DK.SCALA))
    a.add_argument("--json", type=Path, help="scrive anche il rendiconto completo (solo conteggi e date)")
    x = a.parse_args(argv)
    if x.fine < x.inizio:
        print(f"ERRORE: --fine {x.fine} prima di --inizio {x.inizio}", file=sys.stderr)
        return 2
    if not (x.cache / x.simbolo).is_dir() or not (x.cache / f"{x.simbolo}_ASK").is_dir():
        print(f"ERRORE: in {x.cache} servono le cartelle {x.simbolo} e {x.simbolo}_ASK", file=sys.stderr)
        return 2
    e = esamina(x.cache, x.inizio, x.fine, x.simbolo)
    print(tabella(e))
    if x.json:
        x.json.write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
