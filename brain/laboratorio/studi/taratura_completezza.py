"""Taratura della soglia «giorno completo» sui conteggi della cache vera (le soglie QUOTA_SESSIONE e QUOTA_TERZO
del caricatore sono PROVVISORIE finché i conteggi veri non le confermano: #49, #63).

Legge una cartella della cache (.bi5), conta per ogni giorno feriale i minuti nella sessione di Londra e in
ciascuno dei tre terzi, e mostra: percentili, e quanti giorni cadrebbero sotto una griglia di soglie. Le vigilie
(24/12, 31/12) sono contate a parte; le chiusure note sono escluse. Stampa SOLO conteggi, percentili e date:
MAI prezzi. La decisione sulla soglia resta all'utente.

Uso (dalla radice del repository, a scaricamento finito, per ciascun lato):
  python3 -s -B -m brain.laboratorio.studi.taratura_completezza --cache brain/dati/reali/cache_dukascopy/XAUUSD \\
      --inizio 2005-01-01 --fine 2023-10-31
"""
import argparse
import math
import sys
from datetime import date, timedelta
from pathlib import Path

from ...dati.pipeline import dukascopy as DK
from ...dati.pipeline.calendario import chiusure_note, giorni_corti
from ..esecuzione.caricatore import MINUTI_SESSIONE, QUOTA_SESSIONE, QUOTA_TERZO, SESSIONE
from ..simulatori.orb_londra import _utc


def _terzi(tempi, giorno: date):
    a, b = _utc(giorno, SESSIONE[0]), _utc(giorno, SESSIONE[1])
    durata = (b - a) / 3
    t3 = [0, 0, 0]
    for t in tempi:
        if a <= t < b:
            t3[min(2, int((t - a) / durata))] += 1
    return t3


def esamina(cartella: Path, inizio: date, fine: date, simbolo: str = "XAUUSD") -> dict:
    per_giorno, vigilie = [], []
    vuoti = 0
    g = inizio
    while g <= fine:
        f = Path(cartella) / f"{g.isoformat()}.bi5"
        if g.weekday() < 5 and g not in chiusure_note(g.year) and f.exists():
            dati = f.read_bytes()
            if not dati:
                vuoti += 1
            else:
                minuti = DK.decodifica(dati, g, DK.SCALA[simbolo])
                t3 = _terzi([m[0] for m in minuti], g)
                voce = {"giorno": g.isoformat(), "sessione": sum(t3), "terzi": t3}
                (vigilie if g in giorni_corti(g.year) else per_giorno).append(voce)
        g += timedelta(days=1)
    return {"per_giorno": per_giorno, "vigilie": vigilie, "giorni_con_dati": len(per_giorno),
            "feriali_vuoti": vuoti}


def verifica_quote(e: dict, quota_sessione: float = QUOTA_SESSIONE, quota_terzo: float = QUOTA_TERZO) -> dict:
    """Con queste soglie, quali giorni risulterebbero incompleti (stessa regola del caricatore)."""
    min_s = math.ceil(quota_sessione * MINUTI_SESSIONE)
    min_t = math.ceil(quota_terzo * MINUTI_SESSIONE / 3)
    sotto = [g["giorno"] for g in e["per_giorno"]
             if g["sessione"] < min_s or any(t < min_t for t in g["terzi"])]
    sotto_vigilie = [g["giorno"] for g in e["vigilie"] if g["terzi"][0] < min_t]
    return {"quota_sessione": quota_sessione, "quota_terzo": quota_terzo,
            "sotto": sotto, "sotto_vigilie": sotto_vigilie}


def percentili(valori) -> dict:
    if not valori:
        return {}
    v = sorted(valori)
    def _p(q):
        return v[min(len(v) - 1, max(0, math.ceil(q / 100 * len(v)) - 1))]
    out = {"min": v[0]}
    out.update({f"p{q}": _p(q) for q in (1, 5, 10, 25, 50)})
    out["max"] = v[-1]
    return out


def tabella(e: dict) -> str:
    righe = [f"Giorni con dati: {e['giorni_con_dati']} (vigilie a parte: {len(e['vigilie'])}; "
             f"feriali vuoti: {e['feriali_vuoti']})",
             f"Minuti in sessione, percentili: {percentili([g['sessione'] for g in e['per_giorno']])}",
             f"Minuti del terzo più scarso, percentili: {percentili([min(g['terzi']) for g in e['per_giorno']])}",
             "", "| quota sessione | quota terzo | giorni sotto | primi |", "|---|---|---|---|"]
    for qs, qt in ((0.6, 0.3), (0.5, 0.25), (0.4, 0.2), (0.3, 0.15), (0.2, 0.1)):
        r = verifica_quote(e, qs, qt)
        righe.append(f"| {qs} | {qt} | {len(r['sotto'])} | {', '.join(r['sotto'][:6])} |")
    r = verifica_quote(e)
    righe += ["", f"Con le soglie ATTUALI del caricatore ({QUOTA_SESSIONE} sessione, {QUOTA_TERZO} per terzo): "
                  f"{len(r['sotto'])} giorni sotto: {', '.join(r['sotto'][:20])}"
                  + (f"; vigilie sotto: {', '.join(r['sotto_vigilie'])}" if r["sotto_vigilie"] else ""),
              "La soglia giusta la decide l'utente: questa tabella dà solo i conteggi."]
    return "\n".join(righe)


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    a.add_argument("--cache", required=True, type=Path, help="cartella del lato (XAUUSD o XAUUSD_ASK)")
    a.add_argument("--inizio", required=True, type=date.fromisoformat)
    a.add_argument("--fine", required=True, type=date.fromisoformat)
    a.add_argument("--simbolo", default="XAUUSD", choices=sorted(DK.SCALA))
    x = a.parse_args(argv)
    if x.fine < x.inizio:
        print(f"ERRORE: --fine {x.fine} prima di --inizio {x.inizio}", file=sys.stderr)
        return 2
    print(tabella(esamina(x.cache, x.inizio, x.fine, x.simbolo)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
