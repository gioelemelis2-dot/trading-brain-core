"""Test minimi per replica.py (calcoli a mano) e genera_dati.py (copertura scenari)."""
from __future__ import annotations

import unittest
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from typing import List
from zoneinfo import ZoneInfo

from .genera_dati import genera_serie_anno
from .replica import MinutoMercato, esegui_replica, is_giorno_escluso

LONDRA = ZoneInfo("Europe/London")
UTC = timezone.utc


def _giorno_normale(
    d: date,
    ra_low: float = 2495.0,
    ra_high: float = 2505.0,
    spread: float = 0.20,
    break_dir: str = "NONE",
    entry_ask: float = 2506.0,
    entry_bid: float = 2505.8,
    post_minutes: list = None,
) -> List[MinutoMercato]:
    t0 = datetime.combine(d, time(8, 0), tzinfo=LONDRA)
    bars: List[MinutoMercato] = []
    # RA 30 minuti: minuto 0 fissa ra_high/ra_low, altri minuti dentro
    for m in range(30):
        tl = t0 + timedelta(minutes=m)
        lo = ra_low if m == 0 else (ra_low + 1.0)
        hi = ra_high if m == 0 else (ra_high - 1.0)
        mid = (ra_low + ra_high) / 2.0
        bars.append(
            MinutoMercato(
                tl.astimezone(UTC),
                Decimal(str(mid)), Decimal(str(hi)), Decimal(str(lo)), Decimal(str(mid)),
                Decimal(str(mid + spread)), Decimal(str(hi + spread)),
                Decimal(str(lo + spread)), Decimal(str(mid + spread)),
            )
        )
    # 08:30..08:44 candela segnale 15m
    sig_close = (
        ra_high + 1.0 if break_dir == "BUY" else (ra_low - 1.0 if break_dir == "SELL" else (ra_low + ra_high) / 2.0)
    )
    for m in range(30, 45):
        tl = t0 + timedelta(minutes=m)
        c = sig_close if m == 44 else (ra_low + ra_high) / 2.0
        o = (ra_low + ra_high) / 2.0
        hi = max(o, c)
        lo = min(o, c)
        bars.append(
            MinutoMercato(
                tl.astimezone(UTC),
                Decimal(str(o)), Decimal(str(hi)), Decimal(str(lo)), Decimal(str(c)),
                Decimal(str(o + spread)), Decimal(str(hi + spread)),
                Decimal(str(lo + spread)), Decimal(str(c + spread)),
            )
        )
    if post_minutes is not None:
        bars.extend(post_minutes)
    else:
        # 08:45..16:35 neutri
        for m in range(45, 515):
            tl = t0 + timedelta(minutes=m)
            o = entry_bid if m == 45 else (ra_low + ra_high) / 2.0
            a_o = entry_ask if m == 45 else (o + spread)
            bars.append(
                MinutoMercato(
                    tl.astimezone(UTC),
                    Decimal(str(o)), Decimal(str(o + 0.1)), Decimal(str(o - 0.1)), Decimal(str(o)),
                    Decimal(str(a_o)), Decimal(str(a_o + 0.1)), Decimal(str(a_o - 0.1)), Decimal(str(a_o)),
                )
            )
    return bars


class TestReplicaCalcoliAMano(unittest.TestCase):
    def _warmup_20_giorni(self) -> List[MinutoMercato]:
        # 20 giorni validi prima del 2024-03-04 (febbraio 2024 ha solo giorni feriali senza festivi UK)
        bars: List[MinutoMercato] = []
        d = date(2024, 2, 1)
        count = 0
        while count < 20:
            if not is_giorno_escluso(d):
                bars.extend(_giorno_normale(d, ra_low=2495.0, ra_high=2505.0, spread=0.20))
                count += 1
            d += timedelta(days=1)
        return bars

    def test_calcolo_a_mano_buy_target_vt(self):
        bars = self._warmup_20_giorni()
        # Giorno test: 2024-03-04 (lunedi' valido). RA=[2495, 2505], A=10.
        # Spread medio storico = 0.20 -> costo_rif = 0.20 + 0.07 + 0.10 + 0.20 = 0.57 -> min A = 3.42 <= 10.
        d_test = date(2024, 3, 4)
        t0 = datetime.combine(d_test, time(8, 0), tzinfo=LONDRA)
        # Ingresso 08:45: bid_open = 2505.80, ask_open = 2506.00 -> entry_exec = 2506.10.
        # Rischio = 2506.10 - 2495.00 = 11.10 (>= 2.50).
        # Target = 2506.10 + 1.5 * 11.10 = 2522.75.
        # Perdita allo stop per oncia = (2506.10 - (2495.00 - 0.20)) = 11.30; + comm 0.07 = 11.37.
        # Once = floor(500 / 11.37) = 43.
        # Al minuto 46 (08:46): bid_high = 2523.00 -> scatta target a 2522.75 esatto!
        # R = 43 * ((2522.75 - 2506.10) - 0.07) / 500 = 43 * 16.58 / 500 = 1.42588.
        post = [
            MinutoMercato(
                (t0 + timedelta(minutes=45)).astimezone(UTC),
                Decimal("2505.80"), Decimal("2525.00"), Decimal("2505.50"), Decimal("2506.00"),
                Decimal("2506.00"), Decimal("2525.20"), Decimal("2505.70"), Decimal("2506.20"),
                # Nota: al minuto d'ingresso tocca anche il target 2525 > 2522.75 -> NON deve chiudere!
            ),
            MinutoMercato(
                (t0 + timedelta(minutes=46)).astimezone(UTC),
                Decimal("2506.00"), Decimal("2523.00"), Decimal("2505.90"), Decimal("2522.90"),
                Decimal("2506.20"), Decimal("2523.20"), Decimal("2506.10"), Decimal("2523.10"),
            ),
        ]
        bars.extend(_giorno_normale(d_test, break_dir="BUY", post_minutes=post))
        res = esegui_replica(bars, variante="V-T")
        self.assertEqual(len(res.trades), 1)
        tr = res.trades[0]
        self.assertEqual(tr.lato, "BUY")
        self.assertEqual(tr.prezzo_ingresso, Decimal("2506.10"))
        self.assertEqual(tr.prezzo_uscita, Decimal("2522.75"))
        self.assertEqual(tr.motivo_uscita, "TARGET")
        self.assertEqual(tr.once, 43)
        self.assertEqual(tr.r_netto, Decimal("1.42588"))
        self.assertEqual(tr.minuto_uscita_utc, (t0 + timedelta(minutes=46)).astimezone(UTC))

    def test_sell_stop_scatta_su_ask_e_salto_gap(self):
        bars = self._warmup_20_giorni()
        d_test = date(2024, 3, 4)
        t0 = datetime.combine(d_test, time(8, 0), tzinfo=LONDRA)
        # SELL: ra_high = 2505.00, ra_low = 2495.00.
        # Ingresso 08:45: bid_open = 2494.00, ask_open = 2494.20 -> entry_exec = 2493.90.
        # Rischio = 2505.00 - 2493.90 = 11.10; once = floor(500 / (11.10 + 0.20 + 0.07)) = 43.
        # Minuto 46: bid_high resta a 2504.90 (< 2505!), MA ask_open = 2506.00 (salto oltre stop!)
        # Deve uscire a max(2505.00, 2506.00) + 0.20 = 2506.20!
        post = [
            MinutoMercato(
                (t0 + timedelta(minutes=45)).astimezone(UTC),
                Decimal("2494.00"), Decimal("2494.10"), Decimal("2493.90"), Decimal("2494.00"),
                Decimal("2494.20"), Decimal("2494.30"), Decimal("2494.10"), Decimal("2494.20"),
            ),
            MinutoMercato(
                (t0 + timedelta(minutes=46)).astimezone(UTC),
                Decimal("2504.50"), Decimal("2504.90"), Decimal("2504.40"), Decimal("2504.80"),
                Decimal("2506.00"), Decimal("2506.10"), Decimal("2505.90"), Decimal("2506.00"),
            ),
        ]
        bars.extend(_giorno_normale(d_test, break_dir="SELL", post_minutes=post))
        res = esegui_replica(bars, variante="V-S")
        self.assertEqual(len(res.trades), 1)
        tr = res.trades[0]
        self.assertEqual(tr.lato, "SELL")
        self.assertEqual(tr.prezzo_ingresso, Decimal("2493.90"))
        self.assertEqual(tr.prezzo_uscita, Decimal("2506.20"))
        self.assertEqual(tr.motivo_uscita, "STOP")
        self.assertEqual(tr.once, 43)

    def test_fallback_chiusura_senza_minuti_1630_1645(self):
        bars = self._warmup_20_giorni()
        d_test = date(2024, 3, 4)
        t0 = datetime.combine(d_test, time(8, 0), tzinfo=LONDRA)
        # Ingresso 08:45, ultimo minuto eseguibile <16:30 e' 16:28 (close BID 2510.00), poi salto alle 16:45
        post = [
            MinutoMercato(
                (t0 + timedelta(minutes=45)).astimezone(UTC),
                Decimal("2505.80"), Decimal("2506.00"), Decimal("2505.70"), Decimal("2505.90"),
                Decimal("2506.00"), Decimal("2506.20"), Decimal("2505.90"), Decimal("2506.10"),
            ),
            MinutoMercato(
                (t0 + timedelta(minutes=508)).astimezone(UTC),  # 16:28 Londra
                Decimal("2509.50"), Decimal("2510.10"), Decimal("2509.40"), Decimal("2510.00"),
                Decimal("2509.70"), Decimal("2510.30"), Decimal("2509.60"), Decimal("2510.20"),
            ),
            MinutoMercato(
                (t0 + timedelta(minutes=525)).astimezone(UTC),  # 16:45 Londra (>= 16:45 -> escluso!)
                Decimal("2520.00"), Decimal("2520.50"), Decimal("2519.50"), Decimal("2520.00"),
                Decimal("2520.20"), Decimal("2520.70"), Decimal("2519.70"), Decimal("2520.20"),
            ),
        ]
        bars.extend(_giorno_normale(d_test, break_dir="BUY", post_minutes=post))
        res = esegui_replica(bars, variante="V-S")
        self.assertEqual(len(res.trades), 1)
        tr = res.trades[0]
        self.assertEqual(tr.motivo_uscita, "FINE_SESSIONE")
        # close BID 2510.00 - 0.20 = 2509.80
        self.assertEqual(tr.prezzo_uscita, Decimal("2509.80"))

    def test_generatore_copre_tutti_i_casi_su_tre_semi(self):
        for seme in (101, 202, 303):
            dati = genera_serie_anno(seme)
            res_vt = esegui_replica(dati, variante="V-T")
            res_vs = esegui_replica(dati, variante="V-S")
            res_stress = esegui_replica(dati, variante="V-T", stress=True)
            res_ra20 = esegui_replica(dati, variante="V-T", ra_minuti=20)
            self.assertGreater(len(res_vt.giorni), 200, f"seme {seme}")
            self.assertGreater(len(res_vt.trades), 20, f"seme {seme}")
            self.assertGreater(len(res_vs.trades), 20, f"seme {seme}")
            self.assertGreater(res_vt.minuti_spread_negativo, 0, f"seme {seme}")
            for motivo in (
                "fine_settimana_o_festivo",
                "minuti_range_insufficienti",
                "storico_insufficiente",
                "tetto_ampiezza",
                "minimo_ampiezza",
                "spread_storici_insufficienti",
            ):
                self.assertIn(motivo, res_vt.conteggio_motivi, f"manca {motivo} su seme {seme}")
            self.assertNotEqual(res_vt.metriche["r_somma"], res_stress.metriche["r_somma"])
            self.assertGreater(len(res_ra20.trades), 10)


if __name__ == "__main__":
    unittest.main()
