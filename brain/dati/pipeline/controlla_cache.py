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
import sys
from datetime import date, timedelta
from pathlib import Path
from statistics import median
from typing import Dict, Optional

from . import dukascopy as DK

QUOTA_CORTI = 0.5


def pasqua(anno: int) -> date:
    """Domenica di Pasqua (calendario gregoriano, algoritmo anonimo di Meeus/Jones/Butcher)."""
    a, b, c = anno % 19, anno // 100, anno % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    return date(anno, (h + l_ - 7 * m + 114) // 31, (h + l_ - 7 * m + 114) % 31 + 1)


def chiusure_note(anno: int) -> set:
    return {date(anno, 1, 1), date(anno, 12, 25), pasqua(anno) - timedelta(days=2)}


def _data(nome: str) -> Optional[date]:
    try:
        return date.fromisoformat(nome[:-4]) if nome.endswith(".bi5") else None
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
    if not file and (inizio is None or fine is None):
        return {"cartella": str(cartella), "anni": {}, "tmp_residui": tmp, "pulito": False}
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
                    n = len(DK.decodifica(dati, g, DK.SCALA[simbolo]))         # solo il numero dei minuti
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
            "tmp_residui": tmp, "pulito": pulito}


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
    righe.append("ESITO: " + ("PULITO" if e["pulito"] else "DA SISTEMARE (vedi sopra)") +
                 " — i giorni corti vanno guardati, ma non rendono la cache sporca")
    return "\n".join(righe)


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    a.add_argument("cartelle", nargs="+", type=Path)
    a.add_argument("--inizio", type=date.fromisoformat)
    a.add_argument("--fine", type=date.fromisoformat)
    a.add_argument("--json", type=Path)
    x = a.parse_args(argv)
    esiti = []
    for c in x.cartelle:
        e = esamina(c, x.inizio, x.fine)
        esiti.append(e)
        print(testo(e), "\n")
    if x.json:
        x.json.write_text(json.dumps(esiti, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0 if all(e["pulito"] for e in esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
