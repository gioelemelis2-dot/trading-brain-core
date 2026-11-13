"""Studio 2 (esplorativo, SOLO periodo di sviluppo): micro-range a 1 minuto su XAUUSD. Domande dell'utente del
14/11/2026: è meglio entrare contro il range o sulla rottura? Range disegnato con le ombre o con le chiusure? Quante
volte il prezzo tocca i bordi prima di rompere? Target al bordo opposto o a metà?

Modello di riferimento (calcolo esatto, non simulazione): in un mercato casuale senza deriva il prezzo arriva a una
distanza a prima che a una distanza b con probabilità b / (a + b). Quindi, prima dei costi:
- contro il range dal bordo, stop 0,25 A oltre il bordo, target a metà (0,5 A): 0,25 / 0,75 = 33,3% = pareggio esatto;
- stesso ingresso, target al bordo opposto (1 A): 0,25 / 1,25 = 20,0% = pareggio esatto;
- sulla rottura, target +0,5 A e stop −0,5 A: 50% = pareggio esatto.
Nessuna geometria ha vantaggio in un mercato casuale: un vantaggio esiste solo se i dati veri si discostano da questi
numeri (ritorno verso il centro dentro i range per il «contro», continuazione per la «rottura»). Per questo ogni
tabella è affiancata dal confronto casuale (stessi minuti, direzione estratta a caso) e da intervalli di confidenza.

Definizioni (decise PRIMA di guardare i risultati; ogni scelta fatta DOPO, guardando queste tabelle, conta come prova):
- range: ultimi W = 10 minuti consecutivi; alto e basso dalle ombre (massimo e minimo) oppure dalle chiusure;
  ampiezza A; valido se A ≤ 0,5 × la mediana delle ampiezze a 10 minuti dei 20 giorni precedenti e A ≥ 1 USD;
- tocco: il prezzo (ombra o chiusura, secondo il modo) arriva entro 0,1 A dal bordo; un nuovo tocco dello stesso
  bordo vale solo dopo che una chiusura è tornata a metà range;
- rottura: il prezzo (ombra o chiusura) supera il bordo di più di 0,1 A; il range scade dopo 60 minuti;
- tocchi contati DOPO la formazione del range (i minuti che lo formano non contano);
- ingresso: con le ombre al livello dell'ordine (contro: limite a 0,1 A dal bordo; rottura: stop a 0,1 A oltre il
  bordo); con le chiusure alla chiusura del minuto. Stop e target a distanze fisse DALL'INGRESSO (contro: stop 0,25 A,
  target 0,5 A «circa metà» o 1 A «circa bordo opposto»; rottura: ±0,5 A), così i pareggi sopra restano esatti;
- esiti dal minuto successivo, sempre con i prezzi veri (massimi e minimi): se in un minuto si toccano stop e target,
  conta lo stop. Prezzi BID: i costi (spread, commissione) NON sono inclusi; il rapporto costo / A è riportato a parte.

Uso (dalla radice del repository, sul Mac):
  python3 -s -B brain/laboratorio/studi/studio_range.py --inizio 2023-11-15 --fine 2026-11-12
"""
import argparse
import math
import statistics
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from typing import Callable, Dict, List, Optional

RADICE = Path(__file__).resolve().parents[3]
if str(RADICE) not in sys.path:
    sys.path.insert(0, str(RADICE))

from brain.laboratorio.studi.studio_sessioni import (ROMA, Minuto, carica_minuti, segni_casuali,  # noqa: E402
                                                     sessione_di)

W, ORIZZONTE, TAU, EPS, SOGLIA, GIORNI_RIF, A_MIN = 10, 60, 0.1, 0.1, 0.5, 20, 1.0
STOP_CONTRO, STOP_ROTTURA, TARGET_ROTTURA = 0.25, 0.5, 0.5


def wilson(successi: int, n: int, z: float = 1.96):
    """Intervallo di confidenza al 95% di una proporzione (Wilson). (None, None) se n = 0."""
    if n == 0:
        return None, None
    p = successi / n
    den = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / den
    mezzo = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return centro - mezzo, centro + mezzo


def esito(minuti: List[Minuto], j: int, entrata: float, target: float, stop: float, orizzonte: int = ORIZZONTE,
          stesso_minuto: bool = False):
    """Dal minuto successivo a j: 'target' se il prezzo arriva prima al target, 'stop' se prima allo stop (anche se nello
    stesso minuto), 'tempo' se nessuno dei due entro `orizzonte` minuti. Funziona per acquisti e vendite.
    stesso_minuto=True (ingresso con ordine DENTRO il minuto j): lo stop toccato nel minuto j conta (non si sa se
    prima o dopo l'esecuzione: scelta prudente); il target nel minuto j non conta."""
    su = target > entrata
    if stesso_minuto:
        m = minuti[j]
        if (m[3] <= stop) if su else (m[2] >= stop):
            return "stop"
    for m in minuti[j + 1:j + 1 + orizzonte]:
        colpito_stop = m[3] <= stop if su else m[2] >= stop
        colpito_target = m[2] >= target if su else m[3] <= target
        if colpito_stop:
            return "stop"
        if colpito_target:
            return "target"
    return "tempo"


def ampiezze_di_riferimento(minuti: List[Minuto], modo: str) -> Dict[date, float]:
    """Per ogni giorno: mediana, nei GIORNI_RIF giorni precedenti, delle mediane giornaliere delle ampiezze a W minuti."""
    per_giorno: Dict[date, list] = defaultdict(list)
    for i in range(W - 1, len(minuti)):
        f = minuti[i - W + 1:i + 1]
        if f[-1][0] - f[0][0] != timedelta(minutes=W - 1):
            continue
        alto, basso = _bordi(f, modo)
        per_giorno[f[-1][0].astimezone(ROMA).date()].append(alto - basso)
    mediane = {g: statistics.median(v) for g, v in per_giorno.items()}
    giorni = sorted(mediane)
    rif = {}
    for k, g in enumerate(giorni):
        prec = giorni[max(0, k - GIORNI_RIF):k]
        if len(prec) == GIORNI_RIF:
            rif[g] = statistics.median(mediane[p] for p in prec)
    return rif


def _bordi(finestra: List[Minuto], modo: str):
    if modo == "ombre":
        return max(m[2] for m in finestra), min(m[3] for m in finestra)
    return max(m[4] for m in finestra), min(m[4] for m in finestra)


def analizza(minuti: List[Minuto], modo: str, riferimento: Optional[Callable[[date], Optional[float]]] = None) -> dict:
    """Scorre i minuti, trova i range (solo minuti passati), conta tocchi e rotture e misura gli esiti dei trade
    contro il range (a ogni tocco) e sulla rottura."""
    if modo not in ("ombre", "chiusure"):
        raise ValueError(modo)
    if riferimento is None:
        rif = ampiezze_di_riferimento(minuti, modo)
        riferimento = rif.get
    rotture_con_tocchi: Dict[int, int] = defaultdict(int)       # rotture avvenute con n tocchi totali
    raggiunti: Dict[int, int] = defaultdict(int)                # range che hanno avuto almeno n tocchi
    lato_ultimo_tocco = {"stesso": 0, "opposto": 0}
    contro: Dict[tuple, Dict[str, int]] = defaultdict(lambda: defaultdict(int))   # (n-esimo tocco, target) → esiti
    rottura: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))     # classe di tocchi → esiti
    ampiezze, sessioni = [], defaultdict(int)
    scaduti = 0
    i = W - 1
    while i < len(minuti) - 1:
        f = minuti[i - W + 1:i + 1]
        if f[-1][0] - f[0][0] != timedelta(minutes=W - 1):
            i += 1
            continue
        alto, basso = _bordi(f, modo)
        a = alto - basso
        r = riferimento(f[-1][0].astimezone(ROMA).date())
        if r is None or a < A_MIN or a > SOGLIA * r:
            i += 1
            continue
        ampiezze.append(a)
        sessioni[sessione_di(f[-1][0]) or "fuori sessione"] += 1
        meta = (alto + basso) / 2                                       # serve a riarmare i tocchi
        tocchi = {"alto": 0, "basso": 0}
        armato = {"alto": True, "basso": True}
        ultimo = None
        fine = min(len(minuti) - 1, i + ORIZZONTE)
        j, rotto = i + 1, None
        while j <= fine:
            m = minuti[j]
            if m[0] - minuti[j - 1][0] > timedelta(minutes=1):          # buco nei dati: il range si chiude
                break
            su, giu = (m[2], m[3]) if modo == "ombre" else (m[4], m[4])
            rompe = su > alto + EPS * a or giu < basso - EPS * a
            # Con le chiusure, una chiusura oltre il bordo è una rottura, non un ingresso contro. Con le ombre l'ordine
            # limite al bordo viene eseguito appena il prezzo lo tocca, ANCHE se poi nello stesso minuto rompe:
            # escludere quei trade selezionerebbe solo i vincenti (errore trovato dalla calibrazione casuale).
            if rompe and modo == "chiusure":
                rotto = "su" if su > alto + EPS * a else "giu"
                break
            for lato, vicino in (("alto", su >= alto - TAU * a), ("basso", giu <= basso + TAU * a)):
                if vicino and armato[lato]:
                    n_tocco = tocchi[lato] + 1
                    if not rompe:                                         # il minuto che rompe non è un tocco
                        tocchi[lato] = n_tocco
                        armato[lato] = False
                        ultimo = lato
                    segno = -1 if lato == "alto" else 1                  # contro: vendo in alto, compro in basso
                    bordo = alto if lato == "alto" else basso
                    entrata = (bordo + segno * TAU * a) if modo == "ombre" else m[4]
                    stop = entrata - segno * STOP_CONTRO * a
                    for nome_t, dist in (("circa metà (0,5 A)", 0.5), ("circa bordo opposto (1 A)", 1.0)):
                        contro[(min(n_tocco, 5), nome_t)][esito(minuti, j, entrata, entrata + segno * dist * a,
                                                                     stop, stesso_minuto=(modo == "ombre"))] += 1
            if rompe:
                rotto = "su" if su > alto + EPS * a else "giu"
                break
            if m[4] <= meta:
                armato["alto"] = True
            if m[4] >= meta:
                armato["basso"] = True
            j += 1
        totale = tocchi["alto"] + tocchi["basso"]
        for n in range(0, totale + 1):
            raggiunti[n] += 1
        if rotto is None:
            scaduti += 1
            i = j + W - 1                       # il prossimo range si forma solo con minuti nuovi
            continue
        rotture_con_tocchi[totale] += 1
        if ultimo is not None:
            lato_ultimo_tocco["stesso" if (ultimo == "alto") == (rotto == "su") else "opposto"] += 1
        segno = 1 if rotto == "su" else -1
        entrata = ((alto if rotto == "su" else basso) + segno * EPS * a) if modo == "ombre" else minuti[j][4]
        classe = "0-1 tocchi" if totale <= 1 else "2-3 tocchi" if totale <= 3 else "4+ tocchi"
        rottura[classe][esito(minuti, j, entrata, entrata + segno * TARGET_ROTTURA * a,
                              entrata - segno * STOP_ROTTURA * a, stesso_minuto=(modo == "ombre"))] += 1
        i = j + W                               # il prossimo range comincia dopo il minuto della rottura
    return {"modo": modo, "range": len(ampiezze), "scaduti": scaduti,
            "ampiezza_mediana": statistics.median(ampiezze) if ampiezze else None, "sessioni": dict(sessioni),
            "rotture_con_tocchi": dict(rotture_con_tocchi), "raggiunti": dict(raggiunti),
            "lato_ultimo_tocco": lato_ultimo_tocco,
            "contro": {k: dict(v) for k, v in contro.items()}, "rottura": {k: dict(v) for k, v in rottura.items()}}


def rischio_rottura(r: dict, n_max: int = 6) -> List[tuple]:
    """Probabilità che il range si rompa con esattamente n tocchi, fra quelli che ne hanno avuti almeno n
    (rischio condizionato: «dopo n tocchi, rompe prima di toccare ancora?»)."""
    out = []
    for n in range(0, n_max + 1):
        base = r["raggiunti"].get(n, 0)
        rotti = r["rotture_con_tocchi"].get(n, 0)
        out.append((n, base, rotti))
    return out


def _pct(s: int, n: int) -> str:
    if n == 0:
        return "—"
    lo, hi = wilson(s, n)
    return f"{100 * s / n:.1f}% [{100 * lo:.0f}–{100 * hi:.0f}] su {n}"


def rapporto(inizio: date, fine: date, risultati: Dict[str, dict]) -> str:
    """risultati: chiavi '<modo>' e '<modo> casuale'."""
    t = [f"# Studio 2 · Micro-range a 1 minuto su XAUUSD ({inizio} → {fine})", "",
         "Periodo di SVILUPPO. Esplorativo: genera ipotesi, non le dimostra. Prezzi BID, costi NON inclusi.",
         "Riferimento di un mercato casuale (calcolo esatto): contro il range con target a metà 33,3%, con target al "
         "bordo opposto 20,0%, sulla rottura 50,0%. Sono i valori di pareggio. Con le OMBRE la regola prudente dentro "
         "il minuto abbassa questi valori di 2–4 punti (calibrazione su prezzi casuali): il confronto giusto è sempre "
         "la colonna «casuale», che passa dallo stesso codice. Fra parentesi l'intervallo di confidenza al 95%.", ""]
    for modo in ("ombre", "chiusure"):
        vero, caso = risultati[modo], risultati[f"{modo} casuale"]
        t += [f"## Range disegnato con le {modo.upper()}", "",
              f"Range trovati: {vero['range']} (casuale {caso['range']}); scaduti senza rottura in 60 minuti: "
              f"{vero['scaduti']} (casuale {caso['scaduti']}). Ampiezza mediana: "
              f"{'—' if vero['ampiezza_mediana'] is None else format(vero['ampiezza_mediana'], '.2f')} USD. "
              f"Per sessione: {vero['sessioni']}.", "",
              "### Dopo n tocchi, rompe prima del tocco successivo?", "",
              "| Tocchi | Dati veri | Casuale |", "|---|---|---|"]
        rv, rc = rischio_rottura(vero), rischio_rottura(caso)
        t += [f"| {n} | {_pct(a, b)} | {_pct(c, d)} |" for (n, b, a), (_, d, c) in zip(rv, rc)]
        lv, lc = vero["lato_ultimo_tocco"], caso["lato_ultimo_tocco"]
        t += ["", f"Rottura dal lato dell'ultimo tocco: {_pct(lv['stesso'], lv['stesso'] + lv['opposto'])} "
                  f"(casuale {_pct(lc['stesso'], lc['stesso'] + lc['opposto'])}).", "",
              "### Contro il range, a ogni tocco (stop 0,25 A oltre il bordo)", "",
              "| Tocco n. | Target | Vince (dati veri) | Vince (casuale) | Pareggio | Scadute (veri) |", "|---|---|---|---|---|---|"]
        for (n, nome_t) in sorted(vero["contro"]):
            ev = vero["contro"][(n, nome_t)]
            ec = caso["contro"].get((n, nome_t), {})
            nv = ev.get("target", 0) + ev.get("stop", 0)
            nc = ec.get("target", 0) + ec.get("stop", 0)
            t.append(f"| {n}{'+' if n == 5 else ''} | {nome_t} | {_pct(ev.get('target', 0), nv)} | "
                     f"{_pct(ec.get('target', 0), nc)} | {'33,3%' if '0,5' in nome_t else '20,0%'} | "
                     f"{ev.get('tempo', 0)} |")
        t += ["", "### Sulla rottura (target +0,5 A, stop −0,5 A dall'ingresso)", "",
              "| Tocchi prima della rottura | Vince (dati veri) | Vince (casuale) | Pareggio | Scadute (veri) |",
              "|---|---|---|---|---|"]
        for classe in sorted(vero["rottura"]):
            ev, ec = vero["rottura"][classe], caso["rottura"].get(classe, {})
            t.append(f"| {classe} | {_pct(ev.get('target', 0), ev.get('target', 0) + ev.get('stop', 0))} | "
                     f"{_pct(ec.get('target', 0), ec.get('target', 0) + ec.get('stop', 0))} | 50,0% | "
                     f"{ev.get('tempo', 0)} |")
        t.append("")
    t += ["## Attenzione", "",
          "- Molti confronti: con circa 40 celle, 2 risultano «fuori» per puro caso. Un indizio vale solo se è ampio, "
          "coerente fra ombre e chiusure e lontano dal casuale.",
          "- Scegliere ora una combinazione (modo, contro o rottura, target, numero di tocchi, sessione) vuol dire "
          "averne considerate molte: vanno contate tutte come prove (DA-19) quando la regola scelta andrà sulla "
          "verifica sigillata.",
          "- I costi non sono inclusi. Con spread e commissione di circa 0,40 USD a operazione, il rapporto costo / A "
          "sposta il pareggio verso l'alto: va calcolato con l'ampiezza mediana sopra."]
    return "\n".join(t) + "\n"


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("--inizio", default="2023-11-15")
    a.add_argument("--fine", default="2026-11-12")
    a.add_argument("--cache", default=str(RADICE / "brain" / "dati" / "reali" / "cache_dukascopy" / "XAUUSD"))
    x = a.parse_args(argv)
    inizio, fine = date.fromisoformat(x.inizio), date.fromisoformat(x.fine)
    try:
        minuti, _ = carica_minuti(Path(x.cache), inizio, fine)
    except ValueError as e:
        print(f"FERMO: {e}", file=sys.stderr)
        return 2
    if not minuti:
        print("FERMO: nessun dato nella cache per il periodo", file=sys.stderr)
        return 1
    finti = segni_casuali(minuti)
    risultati = {}
    for modo in ("ombre", "chiusure"):
        risultati[modo] = analizza(minuti, modo)
        risultati[f"{modo} casuale"] = analizza(finti, modo)
    testo = rapporto(inizio, fine, risultati)
    out = Path(__file__).resolve().parent / "risultati" / f"studio_range_{inizio}_{fine}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(testo, encoding="utf-8")
    print(testo)
    print(f"Salvato in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
