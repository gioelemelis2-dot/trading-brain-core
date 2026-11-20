"""Costi del broker dai tick esportati da MetaTrader 5 (18/11/2026; Gate 1, DA-25).

Legge il file dei tick esportato dalla versione desktop di MT5 (Simboli → Tick → Esporta; colonne <DATE> <TIME> <BID>
<ASK> <LAST> <VOLUME> <FLAGS>, separate da tabulazioni) e calcola:
- lo spread (ASK − BID, in USD per oncia) per ora UTC: numero di tick, mediana, media, 90° percentile, massimo;
- lo stesso per la sessione di Londra (08:00–16:45 UTC);
- il costo di un trade in R per diverse distanze dello stop: (spread mediano + commissione per lotto / contratto) / stop.
SICUREZZA:
- rifiuta l'intero file se contiene anche un solo tick anteriore al 15/11/2023 UTC: quella è la riserva sigillata (D-29);
- non stampa mai prezzi, solo spread e costi.
L'ora del server non è UTC: --fuso-server è lo scarto in ore del server rispetto a UTC nel periodo esportato. Conviene
esportare un periodo senza cambio dell'ora legale.

Uso:
  python3 -s -B -m brain.dati.pipeline.costi_tick --tick XAUUSD_tick.csv --fuso-server 2 --commissione 6 \\
      --contratto 100 --stop 3,5,10,15,20
"""
import argparse
import math
import sys
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from statistics import median

INIZIO_SVILUPPO = datetime(2023, 11, 15, tzinfo=timezone.utc)
TESTA = ["<DATE>", "<TIME>", "<BID>", "<ASK>"]
LONDRA = (time(8, 0), time(16, 45))


def _ora(data: str, ora: str) -> datetime:
    formato = "%Y.%m.%d %H:%M:%S.%f" if "." in ora else "%Y.%m.%d %H:%M:%S"
    return datetime.strptime(f"{data} {ora}", formato)


def leggi(percorso, fuso_server: float):
    """(istante UTC, bid, ask) per ogni tick con entrambi i lati noti. Rifiuta il file se tocca la riserva."""
    righe = Path(percorso).read_text(encoding="utf-8").splitlines()
    if not righe or righe[0].split("\t")[:4] != TESTA:
        raise ValueError(f"intestazione non riconosciuta: {righe[0][:60] if righe else '(vuoto)'!r}; atteso il formato "
                         f"dei tick esportati da MetaTrader 5")
    bid = ask = None
    out = []
    for r in righe[1:]:
        if not r.strip():
            continue
        c = r.split("\t")
        n = _ora(c[0], c[1])                                            # ora del server dichiarata (#120)
        t = datetime.combine(n.date(), n.time(), tzinfo=timezone(timedelta(hours=fuso_server))).astimezone(timezone.utc)
        if t < INIZIO_SVILUPPO:
            raise ValueError(f"tick del {t:%Y-%m-%d %H:%M} UTC, anteriore al 15/11/2023: periodo della riserva "
                             f"sigillata. File rifiutato per intero; esportare solo dal 15/11/2023 in poi")
        if c[2].strip():
            bid = float(c[2])
        if c[3].strip():
            ask = float(c[3])
        if bid is not None and ask is not None:
            out.append((t, bid, ask))
    return out


def _statistiche(valori: list) -> dict:
    o = sorted(valori)
    return {"n": len(o), "mediana": median(o), "media": sum(o) / len(o), "p90": o[math.ceil(0.9 * len(o)) - 1],
            "max": o[-1]}


def spread_per_ora(tick: list) -> dict:
    per_ora, londra, anomali = {}, [], 0
    for t, b, a in tick:
        s = a - b
        if s < 0:
            anomali += 1
            continue
        per_ora.setdefault(t.hour, []).append(s)
        if LONDRA[0] <= t.time() < LONDRA[1]:
            londra.append(s)
    return {"ore": {h: _statistiche(v) for h, v in sorted(per_ora.items())},
            "londra": _statistiche(londra) if londra else None, "anomali": anomali}


def costo_in_r(spread: float, commissione_lotto: float, contratto: float, stop: float) -> float:
    if not stop > 0:
        raise ValueError(f"distanza dello stop {stop!r} non positiva")
    return (spread + commissione_lotto / contratto) / stop


def _f(x: float, cifre: int = 2) -> str:
    return f"{x:.{cifre}f}".replace(".", ",")


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    a.add_argument("--tick", required=True, type=Path)
    a.add_argument("--fuso-server", required=True, type=float, help="ore del server rispetto a UTC (es. 2)")
    a.add_argument("--commissione", type=float, default=6.0, help="USD per lotto, andata e ritorno")
    a.add_argument("--contratto", type=float, default=100.0, help="once per lotto")
    a.add_argument("--stop", default="3,5,10,15,20", help="distanze dello stop in USD per oncia")
    x = a.parse_args(argv)
    try:
        tick = leggi(x.tick, x.fuso_server)
    except (OSError, ValueError) as e:
        print(f"ERRORE: {e}", file=sys.stderr)
        return 2
    if not tick:
        print("ERRORE: nessun tick con BID e ASK", file=sys.stderr)
        return 2
    r = spread_per_ora(tick)
    print(f"Spread del broker (USD per oncia), {len(tick)} tick dal {tick[0][0]:%Y-%m-%d} al {tick[-1][0]:%Y-%m-%d}, "
          f"ore UTC. Tick con ASK < BID esclusi: {r['anomali']}.\n")
    print("| ora UTC | tick | mediana | media | 90° percentile | massimo |\n|---|---|---|---|---|---|")
    for h, s in r["ore"].items():
        print(f"| {h:02d} | {s['n']} | {_f(s['mediana'])} | {_f(s['media'])} | {_f(s['p90'])} | {_f(s['max'])} |")
    rif = r["londra"] or _statistiche([v for v in (a_ - b_ for _, b_, a_ in tick) if v >= 0])
    nome = "sessione di Londra (08:00–16:45 UTC)" if r["londra"] else "tutto il periodo (nessun tick a Londra)"
    print(f"\nRiferimento per i costi: spread mediano nella {nome} = {_f(rif['mediana'])} USD "
          f"(90° percentile {_f(rif['p90'])}). Commissione {_f(x.commissione)} USD per lotto di {x.contratto:g} once.\n")
    print("| stop (USD/oncia) | costo in R con spread mediano | costo in R con 90° percentile |\n|---|---|---|")
    for st in (float(v) for v in x.stop.split(",")):
        print(f"| {_f(st)} | {_f(costo_in_r(rif['mediana'], x.commissione, x.contratto, st), 3)} | "
              f"{_f(costo_in_r(rif['p90'], x.commissione, x.contratto, st), 3)} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
