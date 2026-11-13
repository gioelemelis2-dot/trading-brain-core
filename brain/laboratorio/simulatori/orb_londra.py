"""Simulatore minuto per minuto di H-002 v2 (rottura del range di apertura di Londra su XAUUSD).

Esegue SOLO le regole scritte in brain/laboratorio/ipotesi/H-002-ORB-v2.md: ogni scostamento è un errore.
Prezzi: minuti BID e ASK di Dukascopy (float). Segnali e range sui BID; esecuzioni dal lato giusto:
- acquisto: entra all'ASK, stop quando il BID tocca RA basso, target e uscita al BID;
- vendita: entra al BID, stop quando l'ASK tocca RA alto, target e uscita all'ASK.
Un minuto è eseguibile solo se esistono sia il BID sia l'ASK.

Non apre dati da solo e non sceglie periodi: riceve i minuti dal chiamante, che deve rispettare DA-26.
"""
from dataclasses import dataclass, replace
from datetime import date, datetime, time, timedelta, timezone
from math import floor, sqrt
from statistics import mean, median, pstdev
from typing import Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

LONDRA = ZoneInfo("Europe/London")
Quota = Tuple[float, float, float, float]                      # open, high, low, close


@dataclass(frozen=True)
class Parametri:
    or_minuti: int = 30
    ultimo_segnale: time = time(15, 15)                        # ora di APERTURA dell'ultima candela di segnale
    fine_sessione: time = time(16, 30)
    target_r: Optional[float] = 1.5                            # None = variante V-S (uscita a fine sessione)
    tetto: float = 2.0                                         # A ≤ tetto × mediana delle 20 sessioni valide precedenti
    a_min: float = 3.0                                         # A ≥ 6 × 0,50 USD
    sessioni_rif: int = 20
    minuti_or_min: float = 0.8
    rischio_min_a: float = 0.25
    commissione: float = 0.07                                  # USD per oncia, andata e ritorno
    slip_ingresso: float = 0.10
    slip_uscita: float = 0.20                                  # stop e uscita a fine sessione
    stress: float = 0.0                                        # USD in più contro, su ingresso e uscita
    rischio_usd: float = 500.0                                 # 0,5% di 100.000 USD (capitale fisso)


V_T = Parametri()
V_S = Parametri(target_r=None)


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
    mese = (h + l_ - 7 * m + 114) // 31
    giorno = (h + l_ - 7 * m + 114) % 31 + 1
    return date(anno, mese, giorno)


def esclusi(anno: int) -> set:
    """Giorni esclusi noti in anticipo (§3): 24, 25, 26 e 31 dicembre, 1° gennaio, Venerdì Santo, lunedì di Pasqua."""
    p = pasqua(anno)
    return {date(anno, 12, 24), date(anno, 12, 25), date(anno, 12, 26), date(anno, 12, 31), date(anno, 1, 1),
            p - timedelta(days=2), p + timedelta(days=1)}


def _utc(giorno: date, ora: time) -> datetime:
    return datetime.combine(giorno, ora, tzinfo=LONDRA).astimezone(timezone.utc)


@dataclass
class Giorno:
    data: date
    a: float
    ra_alto: float
    ra_basso: float
    valido: bool                      # tutte le condizioni del §3, filtro dell'ampiezza compreso
    motivo: str
    lato: Optional[str] = None        # "acquisto" / "vendita" / None
    minuti: Optional[list] = None     # minuti eseguibili dall'ingresso al primo minuto ≥ fine sessione compreso


def prepara(bid: Dict[datetime, Quota], ask: Dict[datetime, Quota], par: Parametri = V_T) -> List[Giorno]:
    """Un Giorno per ogni data di Londra con almeno un minuto BID nella sessione. Usa SOLO dati fino al momento di
    ogni decisione: mediana delle sessioni PRECEDENTI, segnale su candele complete, ingresso al minuto dopo."""
    per_data: Dict[date, list] = {}
    for t in sorted(bid):
        per_data.setdefault(t.astimezone(LONDRA).date(), []).append(t)
    storico_a: List[float] = []
    out = []
    ask_t = set(ask)
    for g in sorted(per_data):
        inizio, fine_or = _utc(g, time(8, 0)), _utc(g, time(8, 0)) + timedelta(minutes=par.or_minuti)
        fine = _utc(g, par.fine_sessione)
        or_t = [t for t in per_data[g] if inizio <= t < fine_or]
        if g.weekday() >= 5 or g in esclusi(g.year) or len(or_t) < par.minuti_or_min * par.or_minuti:
            continue
        alto, basso = max(bid[t][1] for t in or_t), min(bid[t][2] for t in or_t)
        a = alto - basso
        rif = median(storico_a[-par.sessioni_rif:]) if len(storico_a) >= par.sessioni_rif else None
        storico_a.append(a)                                     # la mediana usa solo le sessioni precedenti
        if rif is None:
            out.append(Giorno(g, a, alto, basso, False, "meno di 20 sessioni precedenti"))
            continue
        if a > par.tetto * rif:
            out.append(Giorno(g, a, alto, basso, False, "range oltre il tetto"))
            continue
        if a < par.a_min:
            out.append(Giorno(g, a, alto, basso, False, "range sotto il minimo dei costi"))
            continue
        giorno = Giorno(g, a, alto, basso, True, "valido")
        # candele BID da 15 minuti allineate in UTC, aperte fra la fine del range e l'ultimo segnale
        primo = fine_or + timedelta(minutes=(-fine_or.minute) % 15)
        ultimo = _utc(g, par.ultimo_segnale)
        t_candela = primo
        while t_candela <= ultimo:
            dentro = [t for t in per_data[g] if t_candela <= t < t_candela + timedelta(minutes=15)]
            if dentro:
                chiusura = bid[dentro[-1]][3]
                lato = "acquisto" if chiusura > alto else "vendita" if chiusura < basso else None
                if lato:
                    eseguibili = [t for t in per_data[g]
                                  if t in ask_t and t >= t_candela + timedelta(minutes=15)]
                    sessione = [t for t in eseguibili if t < fine]
                    dopo = [t for t in eseguibili if t >= fine][:1]
                    if sessione:
                        giorno.lato = lato
                        giorno.minuti = [(t, bid[t], ask[t]) for t in sessione + dopo]
                    else:
                        giorno.motivo = "nessun minuto eseguibile dopo il segnale"
                    break
            t_candela += timedelta(minutes=15)
        out.append(giorno)
    return out


def simula(giorno: Giorno, lato: str, par: Parametri, stop_livello: Optional[float] = None) -> Optional[dict]:
    """Un trade nella direzione `lato` dal primo minuto di `giorno.minuti`. Lo stop predefinito è il lato opposto del
    range; per i benchmark e il confronto casuale si passa `stop_livello` (stessa distanza, dalla parte giusta).
    Restituisce None se il trade non si fa (prezzo già oltre lo stop, rischio < 0,25 A)."""
    if not giorno.minuti:
        return None
    fine = _utc(giorno.data, par.fine_sessione)
    t0, b0, a0 = giorno.minuti[0]
    su = lato == "acquisto"
    if su:
        stop = giorno.ra_basso if stop_livello is None else stop_livello
        if b0[0] <= stop:
            return None
        entrata = a0[0] + par.slip_ingresso + par.stress
    else:
        stop = giorno.ra_alto if stop_livello is None else stop_livello
        if a0[0] >= stop:
            return None
        entrata = b0[0] - par.slip_ingresso - par.stress
    rischio = abs(entrata - stop)
    if rischio < par.rischio_min_a * giorno.a:
        return None
    target = None if par.target_r is None else (entrata + par.target_r * rischio if su else
                                                entrata - par.target_r * rischio)
    uscita, motivo = None, None
    for k, (t, b, a) in enumerate(giorno.minuti):
        if t >= fine:                                                    # fine sessione: apertura del minuto
            uscita = (b[0] - par.slip_uscita - par.stress) if su else (a[0] + par.slip_uscita + par.stress)
            motivo = "fine sessione"
            break
        tocca_stop = b[2] <= stop if su else a[1] >= stop
        if tocca_stop:
            uscita = (stop - par.slip_uscita - par.stress) if su else (stop + par.slip_uscita + par.stress)
            motivo = "stop"
            break
        if k > 0 and target is not None:                                 # nel minuto d'ingresso conta solo lo stop
            if (b[1] >= target) if su else (a[2] <= target):
                uscita, motivo = target, "target"
                break
    if uscita is None:                                                   # nessun minuto dopo la fine: ultimo prezzo
        t, b, a = giorno.minuti[-1]
        uscita = (b[3] - par.slip_uscita - par.stress) if su else (a[3] + par.slip_uscita + par.stress)
        motivo = "fine dati"
    per_oncia = (uscita - entrata) if su else (entrata - uscita)
    perdita_allo_stop = (entrata - (stop - par.slip_uscita - par.stress)) if su else \
        ((stop + par.slip_uscita + par.stress) - entrata)
    once = floor(par.rischio_usd / (perdita_allo_stop + par.commissione))
    if once < 1:
        return None
    netto = once * (per_oncia - par.commissione)
    return {"data": giorno.data, "lato": lato, "entrata": entrata, "uscita": uscita, "motivo": motivo,
            "once": once, "r": netto / par.rischio_usd}


def trade(giorni: List[Giorno], par: Parametri) -> List[dict]:
    """I trade della strategia: un giorno valido con segnale, direzione della rottura."""
    out = []
    for g in giorni:
        if g.valido and g.lato:
            r = simula(g, g.lato, par)
            if r:
                out.append(r)
    return out


def specchio(giorni: List[Giorno], par: Parametri, lato_fisso: Optional[str] = None,
             lati: Optional[Dict[date, str]] = None) -> List[dict]:
    """Benchmark: stessi giorni e orari d'ingresso della strategia, direzione fissa (`lato_fisso`) o data per giorno
    (`lati`), stop alla STESSA distanza della strategia ma dalla parte giusta."""
    out = []
    for g in giorni:
        if not (g.valido and g.lato):
            continue
        base = simula(g, g.lato, par)
        if base is None:
            continue
        lato = lato_fisso or lati[g.data]
        if lato == g.lato:
            out.append(base)
            continue
        distanza = abs(base["entrata"] - (g.ra_basso if g.lato == "acquisto" else g.ra_alto))
        t0, b0, a0 = g.minuti[0]
        entrata = (a0[0] + par.slip_ingresso + par.stress) if lato == "acquisto" else \
            (b0[0] - par.slip_ingresso - par.stress)
        stop = entrata - distanza if lato == "acquisto" else entrata + distanza
        r = simula(replace(g, a=0.0), lato, par, stop_livello=stop)            # a=0: niente filtro sul rischio
        if r:
            out.append(r)
    return out


def metriche(tr: List[dict]) -> dict:
    if not tr:
        return {"n": 0}
    rs = [x["r"] for x in tr]
    cum = picco = dd = 0.0
    serie = peggiore = 0
    for r in rs:
        cum += r
        picco = max(picco, cum)
        dd = max(dd, picco - cum)
        serie = serie + 1 if r < 0 else 0
        peggiore = max(peggiore, serie)
    sd = pstdev(rs) if len(rs) > 1 else 0.0
    per_anno: Dict[int, list] = {}
    for x in tr:
        per_anno.setdefault(x["data"].year, []).append(x["r"])
    vendite = [x["r"] for x in tr if x["lato"] == "vendita"]
    acquisti = [x["r"] for x in tr if x["lato"] == "acquisto"]
    return {"n": len(rs), "vinti": sum(1 for r in rs if r > 0) / len(rs), "r_medio": mean(rs),
            "sharpe": (mean(rs) / sd) if sd > 0 else None, "dd_max": dd, "serie_perdite": peggiore,
            "r_acquisti": mean(acquisti) if acquisti else None, "n_acquisti": len(acquisti),
            "r_vendite": mean(vendite) if vendite else None, "n_vendite": len(vendite),
            "per_anno": {k: (len(v), mean(v)) for k, v in sorted(per_anno.items())},
            "errore_std": (sd / sqrt(len(rs))) if len(rs) > 1 else None}
