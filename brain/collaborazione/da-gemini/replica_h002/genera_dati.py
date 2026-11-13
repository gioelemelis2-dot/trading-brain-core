"""Generatore di minuti 1m BID/ASK sintetici per verificare H-002 v3.1 (Fase 1).

Genera circa 1 anno per ciascuno di almeno 3 semi fissi (solo stdlib Python 3.9),
includendo cambi ora legale UK (marzo e ottobre), bank holiday inglesi inclusi
sostitutivi e straordinari (2022, 2023, 2024), buchi, spread negativi, gap oltre
lo stop, assenza di minuti [16:30, 16:45), rotture all'ultima candela 15:15 e
fuori finestra 15:30, range sopra il tetto e sotto il minimo, e sessioni senza spread.
"""
from __future__ import annotations

import random
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

from .replica import MinutoMercato, is_giorno_escluso

LONDRA = ZoneInfo("Europe/London")
UTC = timezone.utc


def _q(val: float) -> Decimal:
    return Decimal(str(round(val, 2))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _minuto_normale(
    t_lon: datetime,
    base_price: float,
    delta_close: float,
    wick: float,
    spread: float,
    ask_missing: bool = False,
    neg_open_spread: bool = False,
    neg_close_spread: bool = False,
) -> MinutoMercato:
    o = base_price
    c = base_price + delta_close
    hi = max(o, c) + wick
    lo = min(o, c) - wick
    if ask_missing:
        return MinutoMercato(
            open_time_utc=t_lon.astimezone(UTC),
            bid_open=_q(o),
            bid_high=_q(hi),
            bid_low=_q(lo),
            bid_close=_q(c),
        )
    ao = (o - 0.15) if neg_open_spread else (o + spread)
    ac = (c - 0.15) if neg_close_spread else (c + spread)
    ahi = max(ao, ac, hi + spread) + 0.02
    alo = min(ao, ac, lo + spread) - 0.02
    return MinutoMercato(
        open_time_utc=t_lon.astimezone(UTC),
        bid_open=_q(o),
        bid_high=_q(hi),
        bid_low=_q(lo),
        bid_close=_q(c),
        ask_open=_q(ao),
        ask_high=_q(ahi),
        ask_low=_q(alo),
        ask_close=_q(ac),
    )


def _build_base_day(
    rng: random.Random,
    giorno: date,
    start_price: float,
    spread_base: float,
    ra_target_half: float = 4.0,
) -> Tuple[List[MinutoMercato], float]:
    """Costruisce un giorno standard da 08:00 a 16:49 Londra."""
    out: List[MinutoMercato] = []
    px = start_price
    t0 = datetime.combine(giorno, time(8, 0), tzinfo=LONDRA)
    # 08:00..08:29 (RA): mantiene oscillazione controllata attorno a start_price
    for m in range(530):  # 08:00 -> 16:49 (530 minuti)
        t_lon = t0 + timedelta(minutes=m)
        if m < 30:
            # Oscilla entro +- ra_target_half intorno a start_price
            target = start_price + (ra_target_half * 0.7 if m % 6 < 3 else -ra_target_half * 0.7)
            step = (target - px) * 0.6 + rng.uniform(-0.4, 0.4)
            wick = rng.uniform(0.15, 0.45)
        else:
            step = rng.gauss(0.0, 0.75)
            wick = rng.uniform(0.20, 0.90)
        sp = max(0.10, spread_base + rng.uniform(-0.04, 0.08))
        bar = _minuto_normale(t_lon, px, step, wick, sp)
        out.append(bar)
        px = float(bar.bid_close)
    return out, px


def genera_serie_anno(seme: int) -> List[MinutoMercato]:
    """Genera ~1 anno di candele 1m BID/ASK con scenari patologici deterministici."""
    rng = random.Random(seme)
    periodi: Dict[int, Tuple[date, date]] = {
        101: (date(2022, 1, 1), date(2022, 12, 31)),  # Giubileo 2022, funerali Regina, sostitutivi
        202: (date(2023, 1, 1), date(2023, 12, 31)),  # Incoronazione 2023-05-08 + DST marzo/ottobre
        303: (date(2024, 1, 1), date(2025, 1, 31)),  # Bisestile 2024 + Capodanno 2025 + DST
    }
    if seme in periodi:
        d_inizio, d_fine = periodi[seme]
    else:
        anno = 2022 + (seme % 3)
        d_inizio = date(anno, 1, 1)
        d_fine = date(anno, 12, 31)

    tutti_giorni: List[date] = []
    cur = d_inizio
    while cur <= d_fine:
        tutti_giorni.append(cur)
        cur += timedelta(days=1)

    # Identifica giorni feriali NON esclusi dopo il warm-up per iniettare scenari specifici
    giorni_lavorativi = [d for d in tutti_giorni if not is_giorno_escluso(d)]
    # Indici dopo i primi 25 giorni lavorativi
    scenari: Dict[date, str] = {}
    nomi_scenari = [
        "buco_range_23",             # 23/30 min nel range -> escluso
        "buco_range_24",             # 24/30 min nel range -> valido (bordo)
        "buco_post_segnale_fuori",   # segnale 08:45 poi buco 08:45..09:02 (>15m -> no entry)
        "buco_post_segnale_ritardo", # segnale 08:45 poi buco 08:45..08:50 -> entra 08:51
        "spread_neg_in_ra_e_entry",  # ask<bid in RA + all'ingresso 08:45 -> entra 08:46
        "salto_oltre_stop_buy",      # BUY entra, poi gap down oltre stop -> esce a open
        "salto_oltre_stop_sell",     # SELL entra, poi gap up oltre stop -> esce a open
        "gap_gia_oltre_stop_entry",  # prezzo d'ingresso gia' oltre stop -> scartato
        "mancanti_1630_1645",        # zero minuti in [16:30, 16:45) -> chiude su ultimo < 16:30
        "mancante_1630_entra_1636",  # 16:30..16:35 mancanti -> esce a open 16:36
        "rottura_ultima_1515",       # rompe solo nella candela 15:15-15:30 -> entra 15:30
        "rottura_fuori_1530",        # rompe solo alle 15:30-15:45 -> nessun trade
        "range_sopra_tetto",         # A > 2 * mediana -> escluso
        "range_sotto_minimo",        # A < 6 * costo -> escluso
        "ingresso_stop_e_target",    # nel minuto d'ingresso tocca target E stop -> solo stop
        "ingresso_solo_target",      # nel minuto d'ingresso tocca target ma NON stop -> resta aperto
        "ambigua_intrabar_dopo",     # minuto successivo tocca stop E target -> vince stop
        "senza_spread_0",
        "senza_spread_1",
        "senza_spread_2",
        "senza_spread_3",
        "senza_spread_4",
        "senza_spread_5",
        "senza_spread_6",            # 7 sessioni base senza spread -> fa scattare <15/20
    ]
    base_idx = 28
    for i, nome in enumerate(nomi_scenari):
        pos = base_idx + i * 2
        if pos < len(giorni_lavorativi):
            scenari[giorni_lavorativi[pos]] = nome

    # Includiamo anche un giorno festivo con dati dentro il feed per verificare priorita' esclusione!
    festivi_nel_periodo = [d for d in tutti_giorni if d.weekday() < 5 and is_giorno_escluso(d)]

    minuti_finali: List[MinutoMercato] = []
    px = 2350.0 + (seme % 50) * 3.0
    spread_base = 0.16 + (seme % 4) * 0.02

    for d in tutti_giorni:
        if d.weekday() >= 5:
            continue
        if is_giorno_escluso(d):
            # Includiamo dati solo su alcuni festivi (incluso un eventuale straordinario)
            if d in festivi_nel_periodo[:4] or d.month in (5, 6, 9, 12):
                bars, px = _build_base_day(rng, d, px, spread_base)
                minuti_finali.extend(bars)
            continue

        sc = scenari.get(d)
        t0 = datetime.combine(d, time(8, 0), tzinfo=LONDRA)

        if sc is None:
            bars, px = _build_base_day(rng, d, px, spread_base, ra_target_half=4.2)
            minuti_finali.extend(bars)
            continue

        # Giorni con scenari patologici costruiti con precisione deterministica
        bars, px = _build_base_day(rng, d, px, spread_base, ra_target_half=4.0)
        # Normalizza un RA pulito [p0 - 4.0, p0 + 4.0] nei primi 30 minuti (ampiezza ~ 8.5 USD)
        p0 = float(bars[0].bid_open)
        ra_hi = p0 + 4.0
        ra_lo = p0 - 4.0

        def _crea_range_pulito(min_count: int = 30, ampiezza_half: float = 4.0) -> List[MinutoMercato]:
            ra_list: List[MinutoMercato] = []
            for m in range(30):
                if m >= min_count:
                    continue
                tl = t0 + timedelta(minutes=m)
                if m == 0:
                    b = _minuto_normale(tl, p0, 0.2, 0.2, spread_base)
                    b = MinutoMercato(
                        b.open_time_utc,
                        _q(p0), _q(p0 + ampiezza_half), _q(p0 - ampiezza_half), _q(p0 + 0.1),
                        _q(p0 + spread_base), _q(p0 + ampiezza_half + spread_base),
                        _q(p0 - ampiezza_half + spread_base), _q(p0 + 0.1 + spread_base),
                    )
                else:
                    b = _minuto_normale(tl, p0, 0.0, 0.4, spread_base)
                ra_list.append(b)
            return ra_list

        if sc == "buco_range_23":
            ra_bars = _crea_range_pulito(23, 4.0)
            minuti_finali.extend(ra_bars + bars[30:])
        elif sc == "buco_range_24":
            ra_bars = _crea_range_pulito(24, 4.0)
            minuti_finali.extend(ra_bars + bars[30:])
        elif sc == "buco_post_segnale_fuori":
            custom = _crea_range_pulito(30, 4.0)
            # Candela 08:30-08:44 chiude sopra ra_hi (BUY)
            for m in range(30, 45):
                c_px = ra_hi + 2.0 if m == 44 else p0 + 1.0
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), p0 + 1.0, c_px - (p0 + 1.0), 0.2, spread_base))
            # Buco 08:45..09:04 (20 minuti -> fuori finestra 15m!)
            for m in range(65, 530):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), ra_hi + 2.0, 0.05, 0.2, spread_base))
            minuti_finali.extend(custom)
        elif sc == "buco_post_segnale_ritardo":
            custom = _crea_range_pulito(30, 4.0)
            for m in range(30, 45):
                c_px = ra_hi + 2.0 if m == 44 else p0 + 1.0
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), p0 + 1.0, c_px - (p0 + 1.0), 0.2, spread_base))
            # Mancano 08:45..08:49; entra a 08:50
            for m in range(50, 530):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), ra_hi + 2.2, 0.01, 0.2, spread_base))
            minuti_finali.extend(custom)
        elif sc == "spread_neg_in_ra_e_entry":
            custom = _crea_range_pulito(30, 4.0)
            # Minuto 10 (08:10) con ask_close < bid_close; minuto 45 (08:45) con ask_open < bid_open
            custom[10] = _minuto_normale(t0 + timedelta(minutes=10), p0, 0.0, 0.3, spread_base, neg_close_spread=True)
            for m in range(30, 45):
                c_px = ra_hi + 2.5 if m == 44 else p0 + 1.0
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), p0 + 1.0, c_px - (p0 + 1.0), 0.2, spread_base))
            custom.append(_minuto_normale(t0 + timedelta(minutes=45), ra_hi + 2.5, 0.1, 0.2, spread_base, neg_open_spread=True))
            for m in range(46, 530):
                neg = (m == 60)
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), ra_hi + 2.6, 0.02, 0.2, spread_base, neg_close_spread=neg))
            minuti_finali.extend(custom)
        elif sc == "salto_oltre_stop_buy":
            custom = _crea_range_pulito(30, 4.0)
            for m in range(30, 45):
                c_px = ra_hi + 2.0 if m == 44 else p0 + 1.0
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), p0 + 1.0, c_px - (p0 + 1.0), 0.2, spread_base))
            custom.append(_minuto_normale(t0 + timedelta(minutes=45), ra_hi + 2.0, -0.5, 0.2, spread_base))
            # Al minuto 46 salta giu' di 10 USD sotto ra_lo!
            gap_px = ra_lo - 4.0
            custom.append(_minuto_normale(t0 + timedelta(minutes=46), gap_px, -0.5, 0.2, spread_base))
            for m in range(47, 530):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), gap_px, 0.0, 0.2, spread_base))
            minuti_finali.extend(custom)
        elif sc == "salto_oltre_stop_sell":
            custom = _crea_range_pulito(30, 4.0)
            for m in range(30, 45):
                c_px = ra_lo - 2.0 if m == 44 else p0 - 1.0
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), p0 - 1.0, c_px - (p0 - 1.0), 0.2, spread_base))
            custom.append(_minuto_normale(t0 + timedelta(minutes=45), ra_lo - 2.0, 0.2, 0.2, spread_base))
            gap_px = ra_hi + 5.0
            custom.append(_minuto_normale(t0 + timedelta(minutes=46), gap_px, 0.2, 0.2, spread_base))
            for m in range(47, 530):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), gap_px, 0.0, 0.2, spread_base))
            minuti_finali.extend(custom)
        elif sc == "gap_gia_oltre_stop_entry":
            custom = _crea_range_pulito(30, 4.0)
            for m in range(30, 45):
                c_px = ra_hi + 2.0 if m == 44 else p0 + 1.0
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), p0 + 1.0, c_px - (p0 + 1.0), 0.2, spread_base))
            # A 08:45 apre gia' sotto ra_lo -> niente trade
            custom.append(_minuto_normale(t0 + timedelta(minutes=45), ra_lo - 1.0, 0.0, 0.2, spread_base))
            for m in range(46, 530):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), ra_lo - 1.0, 0.0, 0.2, spread_base))
            minuti_finali.extend(custom)
        elif sc == "mancanti_1630_1645":
            custom = _crea_range_pulito(30, 4.0)
            for m in range(30, 45):
                c_px = ra_hi + 2.0 if m == 44 else p0 + 1.0
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), p0 + 1.0, c_px - (p0 + 1.0), 0.2, spread_base))
            # Prezzo resta fermo sopra p0 fino a 16:28 (m=508), poi buco fino a 16:48 (m=528)
            for m in range(45, 509):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), ra_hi + 2.5, 0.01, 0.1, spread_base))
            for m in range(528, 532):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), ra_hi + 3.0, 0.0, 0.1, spread_base))
            minuti_finali.extend(custom)
        elif sc == "mancante_1630_entra_1636":
            custom = _crea_range_pulito(30, 4.0)
            for m in range(30, 45):
                c_px = ra_hi + 2.0 if m == 44 else p0 + 1.0
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), p0 + 1.0, c_px - (p0 + 1.0), 0.2, spread_base))
            for m in range(45, 510):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), ra_hi + 2.5, 0.0, 0.1, spread_base))
            # Mancano 16:30..16:35 (m=510..515), riprende a 16:36 (m=516)
            for m in range(516, 530):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), ra_hi + 2.8, 0.0, 0.1, spread_base))
            minuti_finali.extend(custom)
        elif sc == "rottura_ultima_1515":
            custom = _crea_range_pulito(30, 4.0)
            # Sta dentro [ra_lo, ra_hi] fino a m=449 (15:29, candela 15:15-15:30), poi chiude sopra!
            for m in range(30, 450):
                c_px = ra_hi + 2.0 if m == 449 else p0
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), p0, c_px - p0, 0.2, spread_base))
            for m in range(450, 530):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), ra_hi + 2.0, 0.02, 0.2, spread_base))
            minuti_finali.extend(custom)
        elif sc == "rottura_fuori_1530":
            custom = _crea_range_pulito(30, 4.0)
            # Sta dentro fino a 15:30 (m=450), rompe solo alle 15:44 (candela 15:30) -> nessun trade
            for m in range(30, 465):
                c_px = ra_hi + 3.0 if m == 464 else p0
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), p0, c_px - p0, 0.2, spread_base))
            for m in range(465, 530):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), ra_hi + 3.0, 0.0, 0.2, spread_base))
            minuti_finali.extend(custom)
        elif sc == "range_sopra_tetto":
            custom = _crea_range_pulito(30, 18.0)  # A = 36 USD > 2 * mediana (~8.5)
            minuti_finali.extend(custom + bars[30:])
        elif sc == "range_sotto_minimo":
            custom = _crea_range_pulito(30, 0.40)  # A = 0.80 USD < 6 * costo (~3.30)
            minuti_finali.extend(custom + bars[30:])
        elif sc == "ingresso_stop_e_target":
            custom = _crea_range_pulito(30, 4.0)
            for m in range(30, 45):
                c_px = ra_hi + 2.0 if m == 44 else p0 + 1.0
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), p0 + 1.0, c_px - (p0 + 1.0), 0.2, spread_base))
            # Al minuto d'ingresso 08:45 apre sopra ra_lo ma ha wick enorme (25 USD) che tocca sia stop che target!
            custom.append(_minuto_normale(t0 + timedelta(minutes=45), ra_hi + 2.0, 0.5, 25.0, spread_base))
            for m in range(46, 530):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), ra_hi + 2.5, 0.0, 0.2, spread_base))
            minuti_finali.extend(custom)
        elif sc == "ingresso_solo_target":
            custom = _crea_range_pulito(30, 4.0)
            for m in range(30, 45):
                c_px = ra_hi + 2.0 if m == 44 else p0 + 1.0
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), p0 + 1.0, c_px - (p0 + 1.0), 0.2, spread_base))
            # Al minuto d'ingresso tocca SOLO target in alto (low > ra_lo, high > ra_hi + 25), non deve uscire!
            o45 = ra_hi + 2.0
            custom.append(
                MinutoMercato(
                    (t0 + timedelta(minutes=45)).astimezone(UTC),
                    _q(o45), _q(o45 + 30.0), _q(ra_lo + 1.0), _q(o45 + 0.5),
                    _q(o45 + spread_base), _q(o45 + 30.0 + spread_base), _q(ra_lo + 1.0 + spread_base), _q(o45 + 0.5 + spread_base),
                )
            )
            for m in range(46, 530):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), o45 + 0.5, 0.0, 0.2, spread_base))
            minuti_finali.extend(custom)
        elif sc == "ambigua_intrabar_dopo":
            custom = _crea_range_pulito(30, 4.0)
            for m in range(30, 45):
                c_px = ra_hi + 2.0 if m == 44 else p0 + 1.0
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), p0 + 1.0, c_px - (p0 + 1.0), 0.2, spread_base))
            custom.append(_minuto_normale(t0 + timedelta(minutes=45), ra_hi + 2.0, 0.2, 0.2, spread_base))
            # Al minuto 46 wick da 25 USD tocca sia stop che target -> conta stop!
            custom.append(_minuto_normale(t0 + timedelta(minutes=46), ra_hi + 2.2, 0.0, 25.0, spread_base))
            for m in range(47, 530):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), ra_hi + 2.2, 0.0, 0.2, spread_base))
            minuti_finali.extend(custom)
        elif sc.startswith("senza_spread_"):
            custom = _crea_range_pulito(30, 4.0)
            # Da 08:30 in poi nessuna candela ASK disponibile -> sessione di base senza spread!
            for m in range(30, 530):
                custom.append(_minuto_normale(t0 + timedelta(minutes=m), p0, 0.0, 0.3, spread_base, ask_missing=True))
            minuti_finali.extend(custom)

    return minuti_finali
