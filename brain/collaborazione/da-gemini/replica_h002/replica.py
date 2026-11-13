"""Replica indipendente di H-002 v3.1 (ORB di Londra su XAUUSD), §2-§7.

Scritta in completa cecita' rispetto a brain/laboratorio/simulatori/orb_londra.py
partendo unicamente da brain/laboratorio/ipotesi/H-002-ORB-v3.md (commit a79a342).
Compatibile con Python 3.9, sola libreria standard.
"""
from __future__ import annotations

import math
import statistics
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from typing import Dict, List, Optional, Sequence, Set, Tuple
from zoneinfo import ZoneInfo

LONDRA = ZoneInfo("Europe/London")
UTC = timezone.utc

COMMISSIONE_RT = Decimal("0.07")
SLIPPAGE_INGRESSO = Decimal("0.10")
SLIPPAGE_USCITA = Decimal("0.20")
STRESS_EXTRA = Decimal("0.20")
CAPITALE_FISSO = Decimal("100000")
RISCHIO_FRAZIONE = Decimal("0.005")
BUDGET_R = CAPITALE_FISSO * RISCHIO_FRAZIONE  # 500 USD


AMBIGUITA: List[Dict[str, str]] = [
    {
        "id": "AMB-01",
        "sezione": "§2 righe 23-26",
        "descrizione": (
            "Minuto con ASK < BID in apertura o chiusura: la scheda dice 'non si usa "
            "(come se mancasse)' per le esecuzioni, mentre 'Segnali e range: sui minuti BID'. "
            "Non precisa se un minuto con ASK < BID vada escluso anche dal computo dei minuti "
            "BID di RA e candele 15m."
        ),
        "scelta_replica": (
            "I minuti BID formano sempre RA (almeno 80%) e candele 15m anche se ASK manca o "
            "ASK < BID; i minuti 'eseguibili' (BID e ASK presenti, ask_open>=bid_open e "
            "ask_close>=bid_close) servono solo per spread, ingresso, stop, target e fine sessione."
        ),
    },
    {
        "id": "AMB-02",
        "sezione": "§3 riga 51",
        "descrizione": (
            "Spread del costo di riferimento: 'primo minuto eseguibile dalle 08:30 in poi'. "
            "Manca un limite superiore orario (es. entro le 16:30 della sessione di Londra o fine giornata) "
            "e non dice se per robustezza RA=20/45 resti 08:30 o segua fine_RA."
        ),
        "scelta_replica": (
            "Cerca il primo minuto eseguibile nell'intervallo della sessione da 08:30 a fine "
            "finestra operativa [08:30, 16:45) ora di Londra, fisso a 08:30 anche con RA=20/45 "
            "(lettura letterale della riga 51)."
        ),
    },
    {
        "id": "AMB-03",
        "sezione": "§3 righe 48-55 e §6 riga 111",
        "descrizione": (
            "Ordine di priorita' dei motivi di esclusione del giorno dentro il §3 quando "
            "coesistono piu' condizioni (es. tetto A > 2*med vs spread < 15/20 vs minimo A < 6*costo)."
        ),
        "scelta_replica": (
            "Priorita': (1) fine_settimana_o_festivo; (2) range_insufficiente (<80% minuti); "
            "(3) storico_sessioni_insufficiente (<20 sessioni base); (4) tetto_ampiezza "
            "(A > 2*med_A); (5) spread_insufficienti (<15 con spread nelle ultime 20); "
            "(6) minimo_ampiezza (A < 6*costo_rif)."
        ),
    },
    {
        "id": "AMB-04",
        "sezione": "§4.2-4.4 e §5 righe 93-96",
        "descrizione": (
            "Nello scenario di stress, lo stress (+0,20) sposta il prezzo d'ingresso eseguito (§4.2) "
            "e la dimensione (§5), ma non e' esplicitato se alteri anche 'rischio >= 0,25*A' (§4.3) "
            "e il livello target 'ingresso +- 1,5 * rischio' (§4.4)."
        ),
        "scelta_replica": (
            "Applico letteralmente §4.2-4.4: entry_exec include slittamento d'ingresso + stress, "
            "e rischio = |entry_exec - stop_level| e target = entry_exec +- target_mult * rischio "
            "usano entry_exec dello scenario corrente."
        ),
    },
    {
        "id": "AMB-05",
        "sezione": "§4.4 righe 79-80 e §4.5",
        "descrizione": (
            "Se la candela 15m chiude fuori dal range ma l'uscita di fine sessione cade in fallback "
            "(nessun minuto eseguibile in [16:30, 16:45)), chiusura all'ultimo minuto eseguibile "
            "prima delle 16:30: potrebbe essere gia' il minuto d'ingresso stesso."
        ),
        "scelta_replica": (
            "Scorro tutti i minuti eseguibili dal minuto d'ingresso con open_time < 16:30 "
            "controllando prima i trigger intrabarra; se a fine ciclo (<16:30) la posizione e' ancora "
            "aperta e non esiste alcun minuto eseguibile in [16:30, 16:45), chiudo al close di "
            "quell'ultimo minuto eseguibile < 16:30 (sempre esistente perche' almeno entry_min < 15:45)."
        ),
    },
    {
        "id": "AMB-06",
        "sezione": "§6 righe 105-107",
        "descrizione": (
            "Nei benchmark direzionali ('compro sempre' / 'vendo sempre'): 'stessa distanza' "
            "rispetto al trade opposto della strategia non specifica se sia |entry_exec - stop_level| "
            "o la distanza tra prezzi raw, ne' se il benchmark usi lo scenario base o anche lo stress."
        ),
        "scelta_replica": (
            "Usa lo stesso scenario (base o stress) e impone stop_level_bench = entry_exec_bench "
            "-+ rischio_strategia (BUY: entry_exec - rischio_strategia; SELL: entry_exec + "
            "rischio_strategia), verificando poi comunque la condizione di validita' all'ingresso "
            "(BID > stop per BUY; ASK < stop per SELL; once >= 1)."
        ),
    },
    {
        "id": "AMB-07",
        "sezione": "§6 riga 110",
        "descrizione": (
            "'numero di minuti con spread negativo nelle sessioni di base, dalle 08:00 alle 16:45': "
            "non precisa se 'spread negativo' si misuri solo su apertura/chiusura (coerente con §2 riga 24) "
            "o anche su high/low."
        ),
        "scelta_replica": (
            "Coerentemente con §2 riga 24, un minuto ha spread negativo / non eseguibile se "
            "manca ASK/BID oppure ask_open < bid_open oppure ask_close < bid_close, e viene "
            "conteggiato nelle sole sessioni di base nell'intervallo [08:00, 16:45) ora di Londra."
        ),
    },
    {
        "id": "AMB-08",
        "sezione": "§3 riga 43",
        "descrizione": (
            "Per i giorni sostitutivi dei bank holiday UK quando Natale/Santo Stefano/Capodanno cadono "
            "nel fine settimana, si segue la regola standard gov.uk (lunedì / martedì sostitutivo)."
        ),
        "scelta_replica": (
            "Implementazione standard gov.uk England & Wales: Jan 1 (sub lun se sab/dom), "
            "Dec 25/26 (sub lun/mar se sab/dom) + straordinari espliciti 2011-2023 + 24/31 dic e 1 gen."
        ),
    },
]


@dataclass(frozen=True)
class MinutoMercato:
    """Singolo minuto 1m UTC con candela BID obbligatoria ed eventuale candela ASK."""

    open_time_utc: datetime
    bid_open: Decimal
    bid_high: Decimal
    bid_low: Decimal
    bid_close: Decimal
    ask_open: Optional[Decimal] = None
    ask_high: Optional[Decimal] = None
    ask_low: Optional[Decimal] = None
    ask_close: Optional[Decimal] = None

    @property
    def spread_valido(self) -> bool:
        if (
            self.ask_open is None
            or self.ask_high is None
            or self.ask_low is None
            or self.ask_close is None
        ):
            return False
        return self.ask_open >= self.bid_open and self.ask_close >= self.bid_close

    @property
    def has_spread_negativo(self) -> bool:
        if self.ask_open is None or self.ask_close is None:
            return False
        return self.ask_open < self.bid_open or self.ask_close < self.bid_close


@dataclass(frozen=True)
class GiornoValutato:
    data: date
    sessione_base: bool
    valido: bool
    motivo_esclusione: Optional[str]
    ra_alto: Optional[Decimal] = None
    ra_basso: Optional[Decimal] = None
    ampiezza: Optional[Decimal] = None
    mediana_a: Optional[Decimal] = None
    costo_rif: Optional[Decimal] = None
    segnale_direzione: Optional[str] = None  # "BUY" | "SELL" | None
    segnale_fine_utc: Optional[datetime] = None


@dataclass(frozen=True)
class TradeEseguito:
    data: date
    lato: str  # "BUY" | "SELL"
    prezzo_ingresso: Decimal
    prezzo_uscita: Decimal
    motivo_uscita: str  # "STOP" | "TARGET" | "FINE_SESSIONE"
    once: int
    r_netto: Decimal
    minuti_scartati: int = 0
    minuto_ingresso_utc: Optional[datetime] = None
    minuto_uscita_utc: Optional[datetime] = None


@dataclass
class EsitoSimulazione:
    giorni: List[GiornoValutato]
    trades: List[TradeEseguito]
    minuti_spread_negativo: int
    conteggio_motivi: Dict[str, int]
    metriche: Dict[str, object]
    benchmark_compro: Dict[str, object] = field(default_factory=dict)
    benchmark_vendo: Dict[str, object] = field(default_factory=dict)
    trades_compro: List[TradeEseguito] = field(default_factory=list)
    trades_vendo: List[TradeEseguito] = field(default_factory=list)


def _pasqua_occidentale(anno: int) -> date:
    """Algoritmo gregoriano anonimo per la domenica di Pasqua."""
    a = anno % 19
    b = anno // 100
    c = anno % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mese = (h + l - 7 * m + 114) // 31
    giorno = ((h + l - 7 * m + 114) % 31) + 1
    return date(anno, mese, giorno)


def _primo_lunedi(anno: int, mese: int) -> date:
    d = date(anno, mese, 1)
    offset = (0 - d.weekday()) % 7
    return d + timedelta(days=offset)


def _ultimo_lunedi(anno: int, mese: int) -> date:
    if mese == 12:
        d = date(anno, 12, 31)
    else:
        d = date(anno, mese + 1, 1) - timedelta(days=1)
    offset = (d.weekday() - 0) % 7
    return d - timedelta(days=offset)


def _sostitutivo_lunedimartedi(d: date) -> date:
    if d.weekday() == 5:  # sabato -> lunedi'
        return d + timedelta(days=2)
    if d.weekday() == 6:  # domenica -> lunedi'
        return d + timedelta(days=1)
    return d


def giorni_esclusi_anno(anno: int) -> Set[date]:
    """Festivi Inghilterra e Galles + sostitutivi + straordinari + 24/25/26/31 dic e 1 gen (§3)."""
    esclusi: Set[date] = set()

    # Capodanno + sostitutivo
    capodanno = date(anno, 1, 1)
    esclusi.add(capodanno)
    esclusi.add(_sostitutivo_lunedimartedi(capodanno))

    # Pasqua
    pasqua = _pasqua_occidentale(anno)
    esclusi.add(pasqua - timedelta(days=2))  # Venerdi' Santo
    esclusi.add(pasqua + timedelta(days=1))  # Lunedi' di Pasqua

    # Primo lunedi' di maggio (spostato nel 2020)
    if anno == 2020:
        esclusi.add(date(2020, 5, 8))
    else:
        esclusi.add(_primo_lunedi(anno, 5))

    # Ultimo lunedi' di maggio (spostato nel 2012 e 2022)
    if anno == 2012:
        esclusi.add(date(2012, 6, 4))
    elif anno == 2022:
        esclusi.add(date(2022, 6, 2))
    else:
        esclusi.add(_ultimo_lunedi(anno, 5))

    # Ultimo lunedi' di agosto
    esclusi.add(_ultimo_lunedi(anno, 8))

    # Natale e Santo Stefano + sostitutivi
    natale = date(anno, 12, 25)
    santo_stefano = date(anno, 12, 26)
    esclusi.add(natale)
    esclusi.add(santo_stefano)
    if natale.weekday() == 4:  # ven 25, sab 26 -> lun 28
        esclusi.add(date(anno, 12, 28))
    elif natale.weekday() == 5:  # sab 25, dom 26 -> lun 27 e mar 28
        esclusi.add(date(anno, 12, 27))
        esclusi.add(date(anno, 12, 28))
    elif natale.weekday() == 6:  # dom 25, lun 26 -> mar 27
        esclusi.add(date(anno, 12, 27))

    # Vigilia e San Silvestro (§3 riga 46)
    esclusi.add(date(anno, 12, 24))
    esclusi.add(date(anno, 12, 31))

    # Aggiunte straordinarie esplicite (§3 riga 43)
    straordinari = {
        date(2011, 4, 29),
        date(2012, 6, 5),
        date(2022, 6, 3),
        date(2022, 9, 19),
        date(2023, 5, 8),
    }
    for d in straordinari:
        if d.year == anno:
            esclusi.add(d)

    return esclusi


def is_giorno_escluso(giorno: date) -> bool:
    if giorno.weekday() >= 5:
        return True
    return giorno in giorni_esclusi_anno(giorno.year)


def _raggruppa_per_giorno_londra(
    minuti: Sequence[MinutoMercato],
) -> Dict[date, List[Tuple[datetime, MinutoMercato]]]:
    per_giorno: Dict[date, List[Tuple[datetime, MinutoMercato]]] = {}
    for m in sorted(minuti, key=lambda x: x.open_time_utc):
        if m.open_time_utc.tzinfo is None:
            raise ValueError("I timestamp dei minuti devono avere timezone esplicito (UTC).")
        t_lon = m.open_time_utc.astimezone(LONDRA)
        per_giorno.setdefault(t_lon.date(), []).append((t_lon, m))
    return per_giorno


def _simula_trade_singolo(
    data: date,
    lato: str,
    entry_exec: Decimal,
    stop_level: Decimal,
    target_level: Optional[Decimal],
    once: int,
    minuti_post_ingresso: Sequence[Tuple[datetime, MinutoMercato]],
    minuti_scartati: int,
    stress: bool,
) -> TradeEseguito:
    """Scorre minuto per minuto dal minuto d'ingresso seguendo §4.3-4.5."""
    stress_add = STRESS_EXTRA if stress else Decimal("0")
    slip_out = SLIPPAGE_USCITA + stress_add

    fine_1630 = datetime.combine(data, time(16, 30), tzinfo=LONDRA)
    fine_1645 = datetime.combine(data, time(16, 45), tzinfo=LONDRA)

    # Minuto di ingresso e' sempre il primo della sequenza (< 15:45)
    entry_t_lon, entry_m = minuti_post_ingresso[0]

    ultimo_eseguibile_pre_1630: Optional[Tuple[datetime, MinutoMercato]] = None

    for idx, (t_lon, m) in enumerate(minuti_post_ingresso):
        if not m.spread_valido:
            continue

        # Uscita di fine sessione in [16:30, 16:45): all'apertura PRIMA di stop e target (§4.4)
        if fine_1630 <= t_lon < fine_1645:
            if lato == "BUY":
                exit_px = m.bid_open - slip_out
            else:
                exit_px = m.ask_open + slip_out  # type: ignore[operator]
            diff = (exit_px - entry_exec) if lato == "BUY" else (entry_exec - exit_px)
            r_net = (Decimal(once) * (diff - COMMISSIONE_RT)) / BUDGET_R
            return TradeEseguito(
                data=data,
                lato=lato,
                prezzo_ingresso=entry_exec,
                prezzo_uscita=exit_px,
                motivo_uscita="FINE_SESSIONE",
                once=once,
                r_netto=r_net,
                minuti_scartati=minuti_scartati,
                minuto_ingresso_utc=entry_m.open_time_utc,
                minuto_uscita_utc=m.open_time_utc,
            )

        if t_lon >= fine_1645:
            # Nessun minuto eseguibile in [16:30, 16:45): chiudi alla chiusura dell'ultimo < 16:30
            break

        ultimo_eseguibile_pre_1630 = (t_lon, m)

        # Minuto di ingresso (idx == 0): conta solo lo stop (§4.5)
        is_entry_min = idx == 0
        if lato == "BUY":
            stop_hit = m.bid_low <= stop_level
            target_hit = (not is_entry_min) and (target_level is not None) and (m.bid_high >= target_level)
            if stop_hit:
                exit_px = min(stop_level, m.bid_open) - slip_out
                diff = exit_px - entry_exec
                r_net = (Decimal(once) * (diff - COMMISSIONE_RT)) / BUDGET_R
                return TradeEseguito(
                    data=data,
                    lato=lato,
                    prezzo_ingresso=entry_exec,
                    prezzo_uscita=exit_px,
                    motivo_uscita="STOP",
                    once=once,
                    r_netto=r_net,
                    minuti_scartati=minuti_scartati,
                    minuto_ingresso_utc=entry_m.open_time_utc,
                    minuto_uscita_utc=m.open_time_utc,
                )
            if target_hit:
                assert target_level is not None
                exit_px = target_level
                diff = exit_px - entry_exec
                r_net = (Decimal(once) * (diff - COMMISSIONE_RT)) / BUDGET_R
                return TradeEseguito(
                    data=data,
                    lato=lato,
                    prezzo_ingresso=entry_exec,
                    prezzo_uscita=exit_px,
                    motivo_uscita="TARGET",
                    once=once,
                    r_netto=r_net,
                    minuti_scartati=minuti_scartati,
                    minuto_ingresso_utc=entry_m.open_time_utc,
                    minuto_uscita_utc=m.open_time_utc,
                )
        else:  # SELL
            stop_hit = m.ask_high >= stop_level  # type: ignore[operator]
            target_hit = (
                (not is_entry_min)
                and (target_level is not None)
                and (m.ask_low <= target_level)  # type: ignore[operator]
            )
            if stop_hit:
                exit_px = max(stop_level, m.ask_open) + slip_out  # type: ignore[type-var]
                diff = entry_exec - exit_px
                r_net = (Decimal(once) * (diff - COMMISSIONE_RT)) / BUDGET_R
                return TradeEseguito(
                    data=data,
                    lato=lato,
                    prezzo_ingresso=entry_exec,
                    prezzo_uscita=exit_px,
                    motivo_uscita="STOP",
                    once=once,
                    r_netto=r_net,
                    minuti_scartati=minuti_scartati,
                    minuto_ingresso_utc=entry_m.open_time_utc,
                    minuto_uscita_utc=m.open_time_utc,
                )
            if target_hit:
                assert target_level is not None
                exit_px = target_level
                diff = entry_exec - exit_px
                r_net = (Decimal(once) * (diff - COMMISSIONE_RT)) / BUDGET_R
                return TradeEseguito(
                    data=data,
                    lato=lato,
                    prezzo_ingresso=entry_exec,
                    prezzo_uscita=exit_px,
                    motivo_uscita="TARGET",
                    once=once,
                    r_netto=r_net,
                    minuti_scartati=minuti_scartati,
                    minuto_ingresso_utc=entry_m.open_time_utc,
                    minuto_uscita_utc=m.open_time_utc,
                )

    # Fallback (§4.4 riga 80): chiusura dell'ultimo minuto eseguibile prima delle 16:30
    assert ultimo_eseguibile_pre_1630 is not None
    _, last_m = ultimo_eseguibile_pre_1630
    if lato == "BUY":
        exit_px = last_m.bid_close - slip_out
        diff = exit_px - entry_exec
    else:
        exit_px = last_m.ask_close + slip_out  # type: ignore[operator]
        diff = entry_exec - exit_px
    r_net = (Decimal(once) * (diff - COMMISSIONE_RT)) / BUDGET_R
    return TradeEseguito(
        data=data,
        lato=lato,
        prezzo_ingresso=entry_exec,
        prezzo_uscita=exit_px,
        motivo_uscita="FINE_SESSIONE",
        once=once,
        r_netto=r_net,
        minuti_scartati=minuti_scartati,
        minuto_ingresso_utc=entry_m.open_time_utc,
        minuto_uscita_utc=last_m.open_time_utc,
    )


def calcola_metriche(trades: Sequence[TradeEseguito]) -> Dict[str, object]:
    n = len(trades)
    if n == 0:
        return {
            "num_trade": 0,
            "win_rate": 0.0,
            "r_medio": 0.0,
            "r_somma": 0.0,
            "sharpe": None,
            "drawdown_max": 0.0,
            "perdite_consecutive_max": 0,
            "acquisti": {"num_trade": 0, "r_medio": 0.0, "r_somma": 0.0},
            "vendite": {"num_trade": 0, "r_medio": 0.0, "r_somma": 0.0},
            "per_anno": {},
        }

    rs = [float(t.r_netto) for t in trades]
    wins = sum(1 for r in rs if r > 0.0)
    r_sum = sum(rs)
    r_mean = r_sum / n

    sharpe: Optional[float]
    if n >= 2:
        sd = statistics.stdev(rs)
        sharpe = (r_mean / sd) if sd > 0.0 else None
    else:
        sharpe = None

    equity = 0.0
    peak = 0.0
    max_dd = 0.0
    streak = 0
    max_streak = 0
    for r in rs:
        equity += r
        if equity > peak:
            peak = equity
        dd = peak - equity
        if dd > max_dd:
            max_dd = dd
        if r < 0.0:
            streak += 1
            if streak > max_streak:
                max_streak = streak
        else:
            streak = 0

    def _sub(items: List[TradeEseguito]) -> Dict[str, object]:
        if not items:
            return {"num_trade": 0, "r_medio": 0.0, "r_somma": 0.0}
        vals = [float(t.r_netto) for t in items]
        return {"num_trade": len(vals), "r_medio": sum(vals) / len(vals), "r_somma": sum(vals)}

    per_anno: Dict[int, List[TradeEseguito]] = {}
    for t in trades:
        per_anno.setdefault(t.data.year, []).append(t)

    return {
        "num_trade": n,
        "win_rate": wins / n,
        "r_medio": r_mean,
        "r_somma": r_sum,
        "sharpe": sharpe,
        "drawdown_max": max_dd,
        "perdite_consecutive_max": max_streak,
        "acquisti": _sub([t for t in trades if t.lato == "BUY"]),
        "vendite": _sub([t for t in trades if t.lato == "SELL"]),
        "per_anno": {anno: _sub(ts) for anno, ts in sorted(per_anno.items())},
    }


def esegui_replica(
    minuti: Sequence[MinutoMercato],
    variante: str = "V-T",
    ra_minuti: int = 30,
    target_mult: Decimal = Decimal("1.5"),
    tetto_mult: Decimal = Decimal("2"),
    stress: bool = False,
) -> EsitoSimulazione:
    """Esegue l'intera simulazione §2-§7 sui minuti dati."""
    if variante not in ("V-T", "V-S"):
        raise ValueError(f"Variante non valida: {variante}")

    minuti_req = int(math.ceil(0.8 * ra_minuti))  # 24/30, 16/20, 36/45
    per_giorno = _raggruppa_per_giorno_londra(minuti)
    if not per_giorno:
        return EsitoSimulazione([], [], 0, {}, calcola_metriche([]))

    # Iteriamo su tutte le date presenti nei dati (o anche su tutto l'intervallo di calendario?
    # Le date senza alcun minuto nei dati possono essere sab/dom/festivi oppure buchi totali:
    # per coerenza coi giorni effettivamente passati al feed, consideriamo l'intervallo min..max
    # dei giorni presenti oppure solo le date presenti. Qui prendiamo tutte le date da min a max
    # se almeno 1 minuto, oppure tutte le date nei dati: meglio tutte le date con almeno un minuto
    # più eventuali festivi? No: un feed Dukascopy di mercato non ha sabati/domeniche o festivi senza scambi!
    # Quindi iteriamo sulle date presenti nel feed in ordine crescente.)
    date_ordinate = sorted(per_giorno.keys())

    # Storico delle sole "sessioni di base" (§3 riga 39): tuple (ampiezza, spread_0830)
    storico_base: List[Tuple[Decimal, Optional[Decimal]]] = []

    giorni_valutati: List[GiornoValutato] = []
    trades: List[TradeEseguito] = []
    bench_buy_trades: List[TradeEseguito] = []
    bench_sell_trades: List[TradeEseguito] = []
    minuti_spread_negativo = 0
    conteggio_motivi: Dict[str, int] = {}

    stress_add = STRESS_EXTRA if stress else Decimal("0")
    slip_in = SLIPPAGE_INGRESSO + stress_add
    slip_out = SLIPPAGE_USCITA + stress_add

    for d in date_ordinate:
        lista_giorno = per_giorno[d]

        # Finestra temporale del giorno in ora di Londra
        t_0800 = datetime.combine(d, time(8, 0), tzinfo=LONDRA)
        t_ra_fine = t_0800 + timedelta(minutes=ra_minuti)
        t_0830 = datetime.combine(d, time(8, 30), tzinfo=LONDRA)
        t_1515 = datetime.combine(d, time(15, 15), tzinfo=LONDRA)
        t_1645 = datetime.combine(d, time(16, 45), tzinfo=LONDRA)

        # 1. Priorita' 1: fine settimana o festivo (§6 riga 111)
        if is_giorno_escluso(d):
            motivo = "fine_settimana_o_festivo"
            conteggio_motivi[motivo] = conteggio_motivi.get(motivo, 0) + 1
            giorni_valutati.append(GiornoValutato(d, False, False, motivo))
            continue

        # Minuti BID nel range di apertura [08:00, 08:00 + ra_minuti)
        minuti_ra = [(t_lon, m) for t_lon, m in lista_giorno if t_0800 <= t_lon < t_ra_fine]
        if len(minuti_ra) < minuti_req:
            motivo = "minuti_range_insufficienti"
            conteggio_motivi[motivo] = conteggio_motivi.get(motivo, 0) + 1
            giorni_valutati.append(GiornoValutato(d, False, False, motivo))
            continue

        # Sessione di base valida! Conteggia minuti con spread negativo in [08:00, 16:45) (§6 riga 110)
        for t_lon, m in lista_giorno:
            if t_0800 <= t_lon < t_1645 and m.has_spread_negativo:
                minuti_spread_negativo += 1

        ra_alto = max(m.bid_high for _, m in minuti_ra)
        ra_basso = min(m.bid_low for _, m in minuti_ra)
        ampiezza = ra_alto - ra_basso

        # Spread del giorno corrente per il registro delle sessioni di base (usato SOLO dai giorni futuri!):
        # primo minuto eseguibile in [08:30, 16:45) (§3 riga 51)
        spread_oggi: Optional[Decimal] = None
        for t_lon, m in lista_giorno:
            if t_0830 <= t_lon < t_1645 and m.spread_valido:
                assert m.ask_open is not None
                spread_oggi = m.ask_open - m.bid_open
                break

        # Salviamo lo snapshot delle 20 sessioni di base PRECEDENTI prima di appendere oggi
        if len(storico_base) < 20:
            motivo = "storico_insufficiente"
            conteggio_motivi[motivo] = conteggio_motivi.get(motivo, 0) + 1
            giorni_valutati.append(
                GiornoValutato(d, True, False, motivo, ra_alto, ra_basso, ampiezza)
            )
            storico_base.append((ampiezza, spread_oggi))
            continue

        ultime_20 = storico_base[-20:]
        storico_base.append((ampiezza, spread_oggi))

        med_a = statistics.median([x[0] for x in ultime_20])
        if ampiezza > tetto_mult * med_a:
            motivo = "tetto_ampiezza"
            conteggio_motivi[motivo] = conteggio_motivi.get(motivo, 0) + 1
            giorni_valutati.append(
                GiornoValutato(d, True, False, motivo, ra_alto, ra_basso, ampiezza, med_a)
            )
            continue

        spread_validi = [x[1] for x in ultime_20 if x[1] is not None]
        if len(spread_validi) < 15:
            motivo = "spread_storici_insufficienti"
            conteggio_motivi[motivo] = conteggio_motivi.get(motivo, 0) + 1
            giorni_valutati.append(
                GiornoValutato(d, True, False, motivo, ra_alto, ra_basso, ampiezza, med_a)
            )
            continue

        med_spread = statistics.median(spread_validi)
        costo_rif = med_spread + COMMISSIONE_RT + SLIPPAGE_INGRESSO + SLIPPAGE_USCITA
        if ampiezza < Decimal("6") * costo_rif:
            motivo = "minimo_ampiezza"
            conteggio_motivi[motivo] = conteggio_motivi.get(motivo, 0) + 1
            giorni_valutati.append(
                GiornoValutato(
                    d, True, False, motivo, ra_alto, ra_basso, ampiezza, med_a, costo_rif
                )
            )
            continue

        # Giorno valido (§3)! Costruzione candele BID da 15m allineate in UTC
        # Prima quarta d'ora >= t_ra_fine fino alle 15:15 incluse (con RA=20m parte alle 08:30!)
        # Notiamo che per t_ra_fine = 08:20 -> 08:30; per 08:30 -> 08:30; per 08:45 -> 08:45.
        if ra_minuti == 20:
            primo_slot_lon = t_0830
        else:
            ts_fine = int(t_ra_fine.astimezone(UTC).timestamp())
            rem = ts_fine % 900
            ts_primo = ts_fine if rem == 0 else (ts_fine + (900 - rem))
            primo_slot_lon = datetime.fromtimestamp(ts_primo, tz=UTC).astimezone(LONDRA)

        ultimo_slot_lon = t_1515

        # Raggruppa minuti BID in blocchi da 15m allineati in UTC
        blocchi_15m: Dict[datetime, List[MinutoMercato]] = {}
        for _, m in lista_giorno:
            ts_m = int(m.open_time_utc.timestamp())
            slot_utc = datetime.fromtimestamp(ts_m - (ts_m % 900), tz=UTC)
            blocchi_15m.setdefault(slot_utc, []).append(m)

        segnale_dir: Optional[str] = None
        segnale_fine_utc: Optional[datetime] = None

        cur_lon = primo_slot_lon
        while cur_lon <= ultimo_slot_lon:
            slot_utc = cur_lon.astimezone(UTC)
            minuti_candela = blocchi_15m.get(slot_utc)
            if minuti_candela:
                chiusura_bid = minuti_candela[-1].bid_close
                if chiusura_bid > ra_alto:
                    segnale_dir = "BUY"
                    segnale_fine_utc = slot_utc + timedelta(minutes=15)
                    break
                if chiusura_bid < ra_basso:
                    segnale_dir = "SELL"
                    segnale_fine_utc = slot_utc + timedelta(minutes=15)
                    break
            cur_lon += timedelta(minutes=15)

        giorni_valutati.append(
            GiornoValutato(
                d,
                True,
                True,
                None,
                ra_alto,
                ra_basso,
                ampiezza,
                med_a,
                costo_rif,
                segnale_dir,
                segnale_fine_utc,
            )
        )

        if segnale_dir is None or segnale_fine_utc is None:
            continue

        # Cerca il primo minuto eseguibile in [segnale_fine_utc, segnale_fine_utc + 15m)
        fine_finestra_ingresso_utc = segnale_fine_utc + timedelta(minutes=15)
        idx_ingresso: Optional[int] = None

        for idx, (t_lon, m) in enumerate(lista_giorno):
            if m.open_time_utc < segnale_fine_utc:
                continue
            if not m.spread_valido:
                continue
            if m.open_time_utc < fine_finestra_ingresso_utc:
                idx_ingresso = idx
                break
            else:
                break

        if idx_ingresso is None:
            continue

        # Conta tutti i minuti con spread negativo/non eseguibile dopo il segnale fino alle 16:45 (§6 riga 112)
        minuti_scartati_giorno = sum(
            1
            for t_lon, m in lista_giorno
            if segnale_fine_utc <= m.open_time_utc and t_lon < t_1645 and m.has_spread_negativo
        )

        _, entry_m = lista_giorno[idx_ingresso]
        assert entry_m.ask_open is not None

        # Controllo "prezzo gia' oltre lo stop" (§4.3 riga 67)
        if segnale_dir == "BUY":
            if entry_m.bid_open <= ra_basso:
                continue
            stop_level = ra_basso
            entry_exec = entry_m.ask_open + slip_in
            rischio = entry_exec - stop_level
            stop_exit_nom = stop_level - slip_out
            perdita_stop_oncia = entry_exec - stop_exit_nom
            target_level = (entry_exec + target_mult * rischio) if variante == "V-T" else None
        else:
            if entry_m.ask_open >= ra_alto:
                continue
            stop_level = ra_alto
            entry_exec = entry_m.bid_open - slip_in
            rischio = stop_level - entry_exec
            stop_exit_nom = stop_level + slip_out
            perdita_stop_oncia = stop_exit_nom - entry_exec
            target_level = (entry_exec - target_mult * rischio) if variante == "V-T" else None

        if rischio < Decimal("0.25") * ampiezza:
            continue

        denom = perdita_stop_oncia + COMMISSIONE_RT
        if denom <= Decimal("0"):
            continue
        once = int(BUDGET_R // denom)
        if once < 1:
            continue

        minuti_da_ingresso = lista_giorno[idx_ingresso:]
        trade_main = _simula_trade_singolo(
            d,
            segnale_dir,
            entry_exec,
            stop_level,
            target_level,
            once,
            minuti_da_ingresso,
            minuti_scartati_giorno,
            stress=stress,
        )
        trades.append(trade_main)

        # Benchmark direzionali (§6 righe 105-107)
        for bench_dir, dest in (("BUY", bench_buy_trades), ("SELL", bench_sell_trades)):
            if bench_dir == segnale_dir:
                dest.append(trade_main)
            else:
                if bench_dir == "BUY":
                    b_entry = entry_m.ask_open + slip_in
                    b_stop = b_entry - rischio
                    if entry_m.bid_open <= b_stop:
                        continue
                    b_perdita = (b_entry - (b_stop - slip_out)) + COMMISSIONE_RT
                    b_once = int(BUDGET_R // b_perdita)
                    if b_once < 1:
                        continue
                    b_target = (b_entry + target_mult * rischio) if variante == "V-T" else None
                else:
                    b_entry = entry_m.bid_open - slip_in
                    b_stop = b_entry + rischio
                    if entry_m.ask_open >= b_stop:
                        continue
                    b_perdita = ((b_stop + slip_out) - b_entry) + COMMISSIONE_RT
                    b_once = int(BUDGET_R // b_perdita)
                    if b_once < 1:
                        continue
                    b_target = (b_entry - target_mult * rischio) if variante == "V-T" else None

                dest.append(
                    _simula_trade_singolo(
                        d,
                        bench_dir,
                        b_entry,
                        b_stop,
                        b_target,
                        b_once,
                        minuti_da_ingresso,
                        minuti_scartati_giorno,
                        stress=stress,
                    )
                )

    return EsitoSimulazione(
        giorni=giorni_valutati,
        trades=trades,
        minuti_spread_negativo=minuti_spread_negativo,
        conteggio_motivi=conteggio_motivi,
        metriche=calcola_metriche(trades),
        benchmark_compro=calcola_metriche(bench_buy_trades),
        benchmark_vendo=calcola_metriche(bench_sell_trades),
        trades_compro=bench_buy_trades,
        trades_vendo=bench_sell_trades,
    )
