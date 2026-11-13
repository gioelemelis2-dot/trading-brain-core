"""Studio 1 (esplorativo, SOLO periodo di sviluppo): come si muove XAUUSD per ora, per sessione, per timeframe e
nei piccoli range. Richiesta dell'utente del 14/11/2026.

Cosa NON è: non è un test di strategia e non dà segnali. Descrive i dati di sviluppo per generare ipotesi, che poi
vanno scritte, sigillate e verificate sul periodo sigillato (DA-26). Non vede «le istituzioni»: il volume è quello di
Dukascopy, non quello di tutto il mercato.

Dati: candele BID da 1 minuto della cache Dukascopy (brain/dati/reali/cache_dukascopy/XAUUSD/AAAA-MM-GG.bi5).
Rifiuta qualunque data prima del 15/11/2023 (verifica sigillata).
Ore in ora italiana (Europe/Rome); sessioni nei fusi delle borse, come l'indicatore TradingView tb_sessioni.pine.

Uso (dalla radice del repository, sul Mac):
  python3 -s -B brain/laboratorio/studi/studio_sessioni.py --inizio 2025-11-13 --fine 2026-11-12
Scrive il riepilogo a schermo e in brain/laboratorio/studi/risultati/ (solo statistiche aggregate, nessun prezzo).
"""
import argparse
import random
import statistics
import sys
from collections import defaultdict
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

RADICE = Path(__file__).resolve().parents[3]
if str(RADICE) not in sys.path:
    sys.path.insert(0, str(RADICE))

from brain.dati.pipeline.dukascopy import SCALA, decodifica   # noqa: E402

SVILUPPO_DA = date(2023, 11, 15)
ROMA = ZoneInfo("Europe/Rome")
SESSIONI = {"Tokyo": ("Asia/Tokyo", time(9, 0), time(15, 0)),
            "Londra": ("Europe/London", time(8, 0), time(16, 30)),
            "New York": ("America/New_York", time(9, 30), time(16, 0))}
MINUTI_GIORNO_PIENO = 600            # giorni con meno minuti scambiati (domeniche, festivi) esclusi dalle statistiche giornaliere
SPREAD_SCENARI = (0.20, 0.35, 0.50)  # USD: IPOTESI per confronto, da sostituire con gli spread misurati sui conti demo
Minuto = Tuple[datetime, float, float, float, float, float]       # orario UTC, open, high, low, close, volume


# ---------------------------------------------------------------------------------------------------------------
# Dati
# ---------------------------------------------------------------------------------------------------------------
def carica_minuti(cache: Path, inizio: date, fine: date) -> Tuple[List[Minuto], int]:
    """Minuti scambiati dal giorno `inizio` al giorno `fine` compresi; restituisce anche i giorni assenti dalla cache."""
    if inizio < SVILUPPO_DA:
        raise ValueError(f"{inizio} è prima del {SVILUPPO_DA}: periodo di VERIFICA SIGILLATA, non si analizza")
    if fine < inizio:
        raise ValueError("fine prima di inizio")
    minuti, mancanti, g = [], 0, inizio
    while g <= fine:
        f = Path(cache) / f"{g.isoformat()}.bi5"
        if not f.exists():
            mancanti += 1
        elif f.stat().st_size:
            for t, o, h, lo, c, v in decodifica(f.read_bytes(), g, SCALA["XAUUSD"]):
                minuti.append((t, float(o), float(h), float(lo), float(c), float(v)))
        g += timedelta(days=1)
    minuti.sort(key=lambda m: m[0])
    return minuti, mancanti


def sessione_di(t: datetime) -> Optional[str]:
    """Prima sessione che contiene l'istante UTC `t` (Londra e New York si sovrappongono: conta New York)."""
    trovata = None
    for nome, (fuso, da, a) in SESSIONI.items():
        locale = t.astimezone(ZoneInfo(fuso)).time()
        if da <= locale < a:
            trovata = nome
    return trovata


def in_sessione(t: datetime, nome: str) -> bool:
    fuso, da, a = SESSIONI[nome]
    return da <= t.astimezone(ZoneInfo(fuso)).time() < a


def _ohlc(gruppo: List[Minuto]) -> Tuple[float, float, float, float]:
    return gruppo[0][1], max(m[2] for m in gruppo), min(m[3] for m in gruppo), gruppo[-1][4]


def per_giorno(minuti: List[Minuto]) -> Dict[date, List[Minuto]]:
    giorni: Dict[date, List[Minuto]] = defaultdict(list)
    for m in minuti:
        giorni[m[0].astimezone(ROMA).date()].append(m)
    return {g: ms for g, ms in giorni.items() if len(ms) >= MINUTI_GIORNO_PIENO}


# ---------------------------------------------------------------------------------------------------------------
# 1. Ore del giorno
# ---------------------------------------------------------------------------------------------------------------
def studio_ore(giorni: Dict[date, List[Minuto]]) -> dict:
    """Per ogni ora italiana: escursione media, movimento netto medio (assoluto e con segno), volume medio; e in quale
    ora il giorno fa il suo massimo e il suo minimo."""
    per_ora: Dict[int, list] = defaultdict(list)
    ora_max: Dict[int, int] = defaultdict(int)
    ora_min: Dict[int, int] = defaultdict(int)
    for ms in giorni.values():
        ore: Dict[int, List[Minuto]] = defaultdict(list)
        for m in ms:
            ore[m[0].astimezone(ROMA).hour].append(m)
        for h, gruppo in ore.items():
            o, hi, lo, c = _ohlc(gruppo)
            per_ora[h].append((hi - lo, c - o, sum(m[5] for m in gruppo)))
        massimo = max(ms, key=lambda m: m[2])
        minimo = min(ms, key=lambda m: m[3])
        ora_max[massimo[0].astimezone(ROMA).hour] += 1
        ora_min[minimo[0].astimezone(ROMA).hour] += 1
    n = len(giorni)
    righe = []
    for h in sorted(per_ora):
        v = per_ora[h]
        righe.append({"ora": h, "n": len(v), "escursione": statistics.mean(x[0] for x in v),
                      "netto_assoluto": statistics.mean(abs(x[1]) for x in v),
                      "netto_con_segno": statistics.mean(x[1] for x in v),
                      "volume": statistics.mean(x[2] for x in v),
                      "massimo_del_giorno_pct": 100 * ora_max[h] / n, "minimo_del_giorno_pct": 100 * ora_min[h] / n})
    return {"giorni": n, "righe": righe}


# ---------------------------------------------------------------------------------------------------------------
# 2. Sessioni
# ---------------------------------------------------------------------------------------------------------------
def studio_sessioni(giorni: Dict[date, List[Minuto]]) -> dict:
    """Per sessione: escursione, movimento netto, efficienza (|netto| / escursione), quota dell'escursione del giorno.
    Fra sessioni: stessa direzione della precedente; New York che rompe massimo o minimo di Londra."""
    dati: Dict[str, list] = defaultdict(list)
    stessa_dir = {"Londra dopo Tokyo": [], "New York dopo Londra": []}
    rottura = {"sopra": 0, "sotto": 0, "entrambi": 0, "nessuno": 0}
    for ms in giorni.values():
        _, dh, dl, _ = _ohlc(ms)
        sess = {}
        for nome in SESSIONI:
            gruppo = [m for m in ms if in_sessione(m[0], nome)]
            if len(gruppo) < 30:
                continue
            o, hi, lo, c = _ohlc(gruppo)
            sess[nome] = (o, hi, lo, c)
            dati[nome].append((hi - lo, c - o, (abs(c - o) / (hi - lo)) if hi > lo else 0.0,
                               (hi - lo) / (dh - dl) if dh > dl else 0.0))
        for chiave, (a, b) in (("Londra dopo Tokyo", ("Tokyo", "Londra")), ("New York dopo Londra", ("Londra", "New York"))):
            if a in sess and b in sess and sess[a][3] != sess[a][0] and sess[b][3] != sess[b][0]:
                stessa_dir[chiave].append((sess[a][3] > sess[a][0]) == (sess[b][3] > sess[b][0]))
        if "Londra" in sess and "New York" in sess:
            ny = [m for m in ms if in_sessione(m[0], "New York") and not in_sessione(m[0], "Londra")]
            if ny:
                sopra = max(m[2] for m in ny) > sess["Londra"][1]
                sotto = min(m[3] for m in ny) < sess["Londra"][2]
                rottura["entrambi" if sopra and sotto else "sopra" if sopra else "sotto" if sotto else "nessuno"] += 1
    righe = [{"sessione": nome, "n": len(v), "escursione": statistics.mean(x[0] for x in v),
              "netto_assoluto": statistics.mean(abs(x[1]) for x in v), "netto_con_segno": statistics.mean(x[1] for x in v),
              "efficienza": statistics.mean(x[2] for x in v), "quota_del_giorno": statistics.mean(x[3] for x in v)}
             for nome, v in dati.items() if v]
    return {"righe": righe,
            "stessa_direzione_pct": {k: (100 * sum(v) / len(v) if v else None) for k, v in stessa_dir.items()},
            "stessa_direzione_n": {k: len(v) for k, v in stessa_dir.items()},
            "new_york_dopo_la_chiusura_di_londra": rottura}


# ---------------------------------------------------------------------------------------------------------------
# 3. Timeframe e costi
# ---------------------------------------------------------------------------------------------------------------
def candele(minuti: List[Minuto], passo: int) -> List[Minuto]:
    """Candele da `passo` minuti allineate all'ora UTC (solo intervalli con almeno un minuto scambiato)."""
    gruppi: Dict[datetime, List[Minuto]] = defaultdict(list)
    for m in minuti:
        t = m[0]
        gruppi[t.replace(minute=t.minute - t.minute % passo, second=0, microsecond=0)].append(m)
    out = []
    for t in sorted(gruppi):
        o, h, lo, c = _ohlc(gruppi[t])
        out.append((t, o, h, lo, c, sum(m[5] for m in gruppi[t])))
    return out


def studio_timeframe(minuti: List[Minuto]) -> dict:
    """Escursione mediana delle candele da 1, 5 e 15 minuti per sessione, e quanto ne mangerebbe lo spread negli
    scenari SPREAD_SCENARI (ipotesi, non misure)."""
    righe = []
    for passo in (1, 5, 15):
        per_sess: Dict[str, list] = defaultdict(list)
        for c in candele(minuti, passo):
            per_sess[sessione_di(c[0]) or "fuori sessione"].append(c[2] - c[3])
        for nome, v in sorted(per_sess.items()):
            med = statistics.median(v)
            righe.append({"timeframe": f"{passo}m", "sessione": nome, "candele": len(v), "escursione_mediana": med,
                          "spread_su_escursione_pct": {s: (100 * s / med if med else None) for s in SPREAD_SCENARI}})
    return {"righe": righe}


# ---------------------------------------------------------------------------------------------------------------
# 4. Piccoli range (compressioni) sulle candele da 5 minuti
# ---------------------------------------------------------------------------------------------------------------
def studio_compressioni(minuti: List[Minuto], finestra: int = 12, dopo: int = 12, soglia: float = 0.5,
                        giorni_rif: int = 20) -> dict:
    """Compressione: escursione delle ultime `finestra` candele da 5 minuti < `soglia` × la mediana delle escursioni
    di 1 ora dei `giorni_rif` giorni PRECEDENTI (niente dati futuri). Per ogni compressione (senza sovrapposizioni):
    nelle `dopo` candele successive il prezzo esce sopra, sotto, da entrambi i lati o resta dentro; quanto si allontana
    (in multipli dell'ampiezza del range); se esce e poi richiude dentro (falsa rottura).
    Parametri ESPLORATIVI scelti da Claude prima di guardare i risultati: cambiarli conta come un'altra prova."""
    b = candele(minuti, 5)
    giorno_di = [c[0].astimezone(ROMA).date() for c in b]
    escursioni_ora: Dict[date, list] = defaultdict(list)
    for i in range(finestra - 1, len(b)):
        w = b[i - finestra + 1:i + 1]
        escursioni_ora[giorno_di[i]].append(max(c[2] for c in w) - min(c[3] for c in w))
    mediana_giorno = {g: statistics.median(v) for g, v in escursioni_ora.items()}
    giorni_ordinati = sorted(mediana_giorno)
    riferimento = {}
    for k, g in enumerate(giorni_ordinati):
        prec = giorni_ordinati[max(0, k - giorni_rif):k]
        if len(prec) == giorni_rif:
            riferimento[g] = statistics.median(mediana_giorno[p] for p in prec)
    esiti: Dict[str, Dict[str, int]] = defaultdict(lambda: {"sopra": 0, "sotto": 0, "entrambi": 0, "dentro": 0,
                                                             "falsa_rottura": 0})
    escursione_fuori: Dict[str, list] = defaultdict(list)
    i = finestra - 1
    while i < len(b) - dopo:
        rif = riferimento.get(giorno_di[i])
        w = b[i - finestra + 1:i + 1]
        alto, basso = max(c[2] for c in w), min(c[3] for c in w)
        ampiezza = alto - basso
        contiguo = (w[-1][0] - w[0][0]) == timedelta(minutes=5 * (finestra - 1))
        if rif is None or not contiguo or ampiezza <= 0 or ampiezza >= soglia * rif:
            i += 1
            continue
        nome = sessione_di(b[i][0]) or "fuori sessione"
        seguito = b[i + 1:i + 1 + dopo]
        sopra = max(c[2] for c in seguito) > alto
        sotto = min(c[3] for c in seguito) < basso
        chiave = "entrambi" if sopra and sotto else "sopra" if sopra else "sotto" if sotto else "dentro"
        esiti[nome][chiave] += 1
        if sopra or sotto:
            fuori = max(max(c[2] for c in seguito) - alto, basso - min(c[3] for c in seguito))
            escursione_fuori[nome].append(fuori / ampiezza)
            if basso <= seguito[-1][4] <= alto:
                esiti[nome]["falsa_rottura"] += 1
        i += finestra                                                      # niente compressioni sovrapposte
    return {"parametri": {"finestra_candele_5m": finestra, "candele_dopo": dopo, "soglia": soglia,
                          "giorni_di_riferimento": giorni_rif},
            "per_sessione": {k: dict(v, n=sum(v[x] for x in ("sopra", "sotto", "entrambi", "dentro")),
                                     uscita_mediana_in_ampiezze=(statistics.median(escursione_fuori[k])
                                                                 if escursione_fuori[k] else None))
                             for k, v in sorted(esiti.items())}}


# ---------------------------------------------------------------------------------------------------------------
# 5. Confronto casuale
# ---------------------------------------------------------------------------------------------------------------
def segni_casuali(minuti: List[Minuto], seme: int = 20261114) -> List[Minuto]:
    """Stessi orari, stesse ampiezze dei movimenti e delle code dei minuti veri, ma direzione di ogni minuto estratta
    a caso: conserva quando e quanto si muove il prezzo, toglie ogni struttura di direzione. Uno «schema» che compare
    anche qui non dice nulla sul mercato."""
    rng = random.Random(seme)
    out, prezzo = [], (minuti[0][1] if minuti else 0.0)
    for t, o, h, lo, c, v in minuti:
        corpo = abs(c - o) * rng.choice((1, -1))
        nuovo_o, nuovo_c = prezzo, prezzo + corpo
        sopra, sotto = h - max(o, c), min(o, c) - lo
        out.append((t, nuovo_o, max(nuovo_o, nuovo_c) + sopra, min(nuovo_o, nuovo_c) - sotto, nuovo_c, v))
        prezzo = nuovo_c
    return out


# ---------------------------------------------------------------------------------------------------------------
# Rapporto
# ---------------------------------------------------------------------------------------------------------------
def rapporto(inizio: date, fine: date, mancanti: int, ore: dict, sess: dict, tf: dict, comp: dict) -> str:
    r = [f"# Studio 1 · XAUUSD per ora, sessione, timeframe e piccoli range ({inizio} → {fine})", "",
         "Periodo di SVILUPPO. Esplorativo: genera ipotesi, non le dimostra. Ore italiane. Prezzi BID Dukascopy.",
         f"Giorni con dati pieni: {ore['giorni']}; giorni assenti dalla cache: {mancanti}.", "",
         "## 1. Ore del giorno", "",
         "| Ora | Escursione media (USD) | Movimento netto medio assoluto | Netto medio con segno | Volume medio | "
         "Massimo del giorno qui | Minimo del giorno qui |", "|---|---|---|---|---|---|---|"]
    r += [f"| {x['ora']:02d} | {x['escursione']:.2f} | {x['netto_assoluto']:.2f} | {x['netto_con_segno']:+.2f} | "
          f"{x['volume']:.0f} | {x['massimo_del_giorno_pct']:.1f}% | {x['minimo_del_giorno_pct']:.1f}% |"
          for x in ore["righe"]]
    r += ["", "## 2. Sessioni", "", "| Sessione | Giorni | Escursione media | Netto assoluto | Netto con segno | "
          "Efficienza (netto/escursione) | Quota dell'escursione del giorno |", "|---|---|---|---|---|---|---|"]
    r += [f"| {x['sessione']} | {x['n']} | {x['escursione']:.2f} | {x['netto_assoluto']:.2f} | "
          f"{x['netto_con_segno']:+.2f} | {x['efficienza']:.2f} | {100 * x['quota_del_giorno']:.0f}% |"
          for x in sess["righe"]]
    r += ["", "Stessa direzione della sessione precedente: " + "; ".join(
        f"{k} {v:.1f}% su {sess['stessa_direzione_n'][k]}" for k, v in sess["stessa_direzione_pct"].items()
        if v is not None),
          "New York dopo la chiusura di Londra rispetto al massimo e al minimo di Londra: " +
          ", ".join(f"{k} {v}" for k, v in sess["new_york_dopo_la_chiusura_di_londra"].items()), "",
          "## 3. Timeframe e costi (spread = scenari ipotetici, non misure)", "",
          "| Timeframe | Sessione | Candele | Escursione mediana (USD) | " +
          " | ".join(f"spread {s:.2f}" for s in SPREAD_SCENARI) + " |", "|---|---|---|---|" + "---|" * len(SPREAD_SCENARI)]
    r += [f"| {x['timeframe']} | {x['sessione']} | {x['candele']} | {x['escursione_mediana']:.2f} | " +
          " | ".join(f"{x['spread_su_escursione_pct'][s]:.0f}%" for s in SPREAD_SCENARI) + " |" for x in tf["righe"]]
    p = comp["parametri"]
    r += ["", f"## 4. Piccoli range (5 minuti: {p['finestra_candele_5m']} candele sotto {p['soglia']} × la mediana "
          f"dei {p['giorni_di_riferimento']} giorni precedenti; esito nelle {p['candele_dopo']} candele dopo)", "",
          "| Sessione | Compressioni | Esce sopra | Esce sotto | Entrambi | Resta dentro | Falsa rottura | "
          "Uscita mediana (× ampiezza) |", "|---|---|---|---|---|---|---|---|"]
    for k, v in comp["per_sessione"].items():
        n = v["n"] or 1
        u = v["uscita_mediana_in_ampiezze"]
        r.append(f"| {k} | {v['n']} | {100 * v['sopra'] / n:.0f}% | {100 * v['sotto'] / n:.0f}% | "
                 f"{100 * v['entrambi'] / n:.0f}% | {100 * v['dentro'] / n:.0f}% | {100 * v['falsa_rottura'] / n:.0f}% | "
                 f"{'' if u is None else f'{u:.2f}'} |")
    return "\n".join(r) + "\n"


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("--inizio", default="2025-11-13")
    a.add_argument("--fine", default="2026-11-12")
    a.add_argument("--cache", default=str(RADICE / "brain" / "dati" / "reali" / "cache_dukascopy" / "XAUUSD"))
    x = a.parse_args(argv)
    inizio, fine = date.fromisoformat(x.inizio), date.fromisoformat(x.fine)
    try:
        minuti, mancanti = carica_minuti(Path(x.cache), inizio, fine)
    except ValueError as e:
        print(f"FERMO: {e}", file=sys.stderr)
        return 2
    if not minuti:
        print("FERMO: nessun dato nella cache per il periodo", file=sys.stderr)
        return 1
    giorni = per_giorno(minuti)
    testo = rapporto(inizio, fine, mancanti, studio_ore(giorni), studio_sessioni(giorni), studio_timeframe(minuti),
                     studio_compressioni(minuti))
    finti = segni_casuali(minuti)
    gf = per_giorno(finti)
    confronto = rapporto(inizio, fine, mancanti, studio_ore(gf), studio_sessioni(gf), studio_timeframe(finti),
                         studio_compressioni(finti))
    testo += ("\n---\n\n# CONFRONTO CASUALE: stessi minuti con direzione estratta a caso\n\n"
              "Conta solo ciò che nei dati veri si discosta CHIARAMENTE da qui.\n\n" + confronto.split("\n", 1)[1])
    out = Path(__file__).resolve().parent / "risultati" / f"studio_sessioni_{inizio}_{fine}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(testo, encoding="utf-8")
    print(testo)
    print(f"Salvato in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
