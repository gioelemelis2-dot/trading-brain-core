"""Controllo d'integrità della cache Dukascopy (un file .bi5 per giorno UTC), anno per anno.

Conta e basta: NON restituisce né stampa prezzi, quindi si può eseguire anche sul periodo di verifica sigillato
(DA-26: nessuno guarda dati, grafici o risultati di quel periodo; i conteggi strutturali sono ammessi, come il
conteggio dei buchi per anno già previsto in DA-26).

Per ogni anno:
- giorni di calendario del periodo, file presenti, giorni senza file;
- giorni feriali con file vuoto o senza minuti, separati dalle chiusure note dell'oro (1/1, 25/12, Venerdì Santo);
- file illeggibili (compressione danneggiata, file troncato, record non validi);
- giorni «corti»: feriali con meno della metà dei minuti mediani dei feriali di quell'anno (da guardare: possono
  essere chiusure anticipate vere, oppure scaricamenti incompleti);
- minuti totali, prima e ultima data con dati.
In più: i file temporanei rimasti (`.AAAA-MM-GG.tmp`, per esempio dopo uno spegnimento durante lo scaricamento).

Uso (dalla radice del repository):
  python3 -s -B -m brain.dati.pipeline.controlla_cache brain/dati/reali/cache_dukascopy/XAUUSD \\
      brain/dati/reali/cache_dukascopy/XAUUSD_ASK
Opzioni: --inizio AAAA-MM-GG --fine AAAA-MM-GG (periodo atteso), --json FILE (esito completo).
"""
import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from statistics import median
from typing import Dict, Optional

from . import dukascopy as DK
from .calendario import chiusure_note, pasqua  # noqa: F401  (pasqua: interfaccia storica)

QUOTA_CORTI = 0.5


NOME_GIORNO = re.compile(r"\d{4}-\d{2}-\d{2}\.bi5")


def _data(nome: str) -> Optional[date]:
    """Solo AAAA-MM-GG.bi5 (#82: da Python 3.11 fromisoformat accetta anche «20100308»)."""
    if not NOME_GIORNO.fullmatch(nome):
        return None
    try:
        return date.fromisoformat(nome[:-4])
    except ValueError:
        return None


def esamina(cartella: Path, inizio: Optional[date] = None, fine: Optional[date] = None,
            simbolo: str = "XAUUSD") -> dict:
    cartella = Path(cartella)
    if not cartella.is_dir():
        raise FileNotFoundError(f"cartella della cache inesistente: {cartella}")
    file: Dict[date, Path] = {}
    for p in cartella.iterdir():
        g = _data(p.name)
        if g is not None:
            file[g] = p
    tmp = sorted(p.name for p in cartella.iterdir() if p.name.startswith(".") and p.name.endswith(".tmp"))
    # #82: file messi da parte dallo scaricatore e .bi5 con nomi non validi (informazione, non sporcano la cache)
    altri = {"messi_da_parte": sorted(p.name for p in cartella.iterdir() if p.name.endswith(".rovinato")),
             "file_estranei": sorted(p.name for p in cartella.iterdir()
                                     if p.name.endswith(".bi5") and _data(p.name) is None)}
    if not file and (inizio is None or fine is None):
        return {"cartella": str(cartella), "anni": {}, "tmp_residui": tmp, "pulito": False, **altri}
    inizio = inizio or min(file)
    fine = fine or max(file)
    anni: Dict[str, dict] = {}
    minuti_feriali: Dict[str, Dict[date, int]] = {}
    g = inizio
    while g <= fine:
        a = anni.setdefault(str(g.year), {"giorni": 0, "file": 0, "mancanti": 0, "feriali_vuoti": [],
                                          "chiusure_note_vuote": [], "illeggibili": [], "corti": [],
                                          "minuti": 0, "prima_data": None, "ultima_data": None})
        a["giorni"] += 1
        if g not in file:
            a["mancanti"] += 1
        else:
            a["file"] += 1
            dati = file[g].read_bytes()
            n = 0
            if dati:
                try:
                    n = len({m[0] for m in DK.decodifica(dati, g, DK.SCALA[simbolo])})   # minuti distinti (#85)
                except DK.ErroreDati:
                    a["illeggibili"].append(g.isoformat())
                    n = None
            if n:
                a["minuti"] += n
                a["prima_data"] = a["prima_data"] or g.isoformat()
                a["ultima_data"] = g.isoformat()
                if g.weekday() < 5:
                    minuti_feriali.setdefault(str(g.year), {})[g] = n
            elif n == 0 and g.weekday() < 5:
                (a["chiusure_note_vuote"] if g in chiusure_note(g.year) else a["feriali_vuoti"]).append(g.isoformat())
        g += timedelta(days=1)
    for anno, per_giorno in minuti_feriali.items():
        soglia = QUOTA_CORTI * median(per_giorno.values())
        anni[anno]["corti"] = [d.isoformat() for d, n in sorted(per_giorno.items()) if n < soglia]
    pulito = bool(file) and not tmp and all(
        a["mancanti"] == 0 and not a["feriali_vuoti"] and not a["illeggibili"] for a in anni.values())
    return {"cartella": str(cartella), "inizio": inizio.isoformat(), "fine": fine.isoformat(), "anni": anni,
            "tmp_residui": tmp, "pulito": pulito, **altri}


def testo(e: dict) -> str:
    righe = [f"Cache: {e['cartella']}  ({e.get('inizio', '—')} → {e.get('fine', '—')})",
             "anno | giorni | file | senza file | feriali vuoti | chiusure note vuote | illeggibili | corti | "
             "minuti | prima data | ultima data"]
    for anno, a in sorted(e["anni"].items()):
        righe.append(f"{anno} | {a['giorni']} | {a['file']} | {a['mancanti']} | {len(a['feriali_vuoti'])} | "
                     f"{len(a['chiusure_note_vuote'])} | {len(a['illeggibili'])} | {len(a['corti'])} | "
                     f"{a['minuti']} | {a['prima_data'] or '—'} | {a['ultima_data'] or '—'}")
    for chiave, nome in (("feriali_vuoti", "feriali vuoti"), ("illeggibili", "illeggibili"), ("corti", "corti")):
        tutte = [d for a in e["anni"].values() for d in a[chiave]]
        if tutte:
            righe.append(f"{nome} ({len(tutte)}), primi: {', '.join(tutte[:15])}")
    righe.append(f"file temporanei rimasti: {len(e['tmp_residui'])} {e['tmp_residui'][:10]}")
    for chiave, nome in (("messi_da_parte", "file messi da parte dallo scaricatore (rovinati, poi riscaricati)"),
                         ("file_estranei", ".bi5 con nome non valido (ignorati)")):
        if e.get(chiave):
            righe.append(f"{nome}: {len(e[chiave])} {e[chiave][:10]}")
    righe.append("ESITO: " + ("PULITO" if e["pulito"] else "DA SISTEMARE (vedi sopra)") +
                 " — i giorni corti vanno guardati, ma non rendono la cache sporca")
    return "\n".join(righe)


def confronta(cartella_bid: Path, cartella_ask: Path, inizio: date, fine: date) -> dict:
    """BID e ASK insieme (per la fine dello scaricamento): giorni con il file da un lato solo, o vuoti da un lato
    solo. Solo nomi e date: nessun prezzo."""
    senza_ask, senza_bid, vuoto_lato = [], [], []
    g, giorni = inizio, 0
    while g <= fine:
        fb = Path(cartella_bid) / f"{g.isoformat()}.bi5"
        fa = Path(cartella_ask) / f"{g.isoformat()}.bi5"
        giorni += 1
        if fb.exists() and not fa.exists():
            senza_ask.append(g.isoformat())
        elif fa.exists() and not fb.exists():
            senza_bid.append(g.isoformat())
        elif fb.exists() and fa.exists() and (fb.stat().st_size > 0) != (fa.stat().st_size > 0):
            vuoto_lato.append(g.isoformat())
        g += timedelta(days=1)
    return {"giorni": giorni, "senza_file_ask": senza_ask, "senza_file_bid": senza_bid,
            "vuoto_da_un_lato": vuoto_lato,
            "allineati": not (senza_ask or senza_bid or vuoto_lato)}


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    a.add_argument("cartelle", nargs="+", type=Path)
    a.add_argument("--inizio", type=date.fromisoformat)
    a.add_argument("--fine", type=date.fromisoformat)
    a.add_argument("--json", type=Path)
    a.add_argument("--ask", type=Path, help="cartella ASK da confrontare con la prima cartella (BID)")
    x = a.parse_args(argv)
    if x.inizio and x.fine and x.inizio > x.fine:                     # #74: periodo invertito = zero giorni
        print("ERRORE: --inizio è dopo --fine", file=sys.stderr)
        return 2
    if x.ask and not (x.inizio and x.fine):
        print("ERRORE: --ask richiede --inizio e --fine", file=sys.stderr)
        return 2
    esiti = []
    for c in x.cartelle:
        e = esamina(c, x.inizio, x.fine)
        esiti.append(e)
        print(testo(e), "\n")
    allineati = True
    if x.ask:
        r = confronta(x.cartelle[0], x.ask, x.inizio, x.fine)
        allineati = r["allineati"]
        print(f"CONFRONTO BID/ASK su {r['giorni']} giorni: "
              + ("ALLINEATI" if allineati else "NON allineati"))
        for chiave, nome in (("senza_file_ask", "con BID ma senza file ASK"),
                             ("senza_file_bid", "con ASK ma senza file BID"),
                             ("vuoto_da_un_lato", "vuoti da un lato solo")):
            if r[chiave]:
                print(f"  {nome} ({len(r[chiave])}): {', '.join(r[chiave][:15])}")
        esiti.append(r)
    if x.json:
        x.json.write_text(json.dumps(esiti, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0 if all(e.get("pulito", True) for e in esiti) and allineati else 1


if __name__ == "__main__":
    sys.exit(main())
