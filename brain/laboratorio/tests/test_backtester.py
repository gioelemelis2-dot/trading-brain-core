"""
Suite di Test per il Backtester Strictly Event-Driven e Deflated Sharpe Ratio.
Verifiche Zero-Trust e Regola Zero-Parametri-Nulli:
1. Strategia 1 (FX EUR/USD): spread>0, comm>0, slippage>0 -> Cash esatto al centesimo ($100,565.00).
2. Strategia 2 (Future ES con Cambio USD/EUR): spread>0, comm>0, slippage>0, cambio>0, Gap Down -> Cash esatto al centesimo (97,350.00 EUR).
3. Esecuzione corretta ordine: Verifica Stop Intrabarra anche sulla barra di ingresso.
4. Risoluzione ambiguità intrabarra SL vs TP con regola pessimistica {H_intrabar_worst_case}.
5. Max Drawdown Intrabar vs Close.
6. DSR restituisce Valore con incertezza NON STIMABILE se < 30 trades.
"""

import json
import multiprocessing
import sys
import unittest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta
from decimal import Decimal

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.dati.pipeline.models import Candle
from brain.guardian.g0.strumenti import Strumento
from brain.guardian.g0.valori import Valore, NON_STIMABILE
from brain.laboratorio.backtester import (
    EventDrivenBacktester,
    Portfolio,
    SignalEvent,
    FillEvent,
    Direction,
    LookAheadViolationError,
    DSRCalculator,
)


def _worker_register_trial(reg_path_str: str, worker_id: int) -> int:
    calc = DSRCalculator(registry_path=Path(reg_path_str))
    return calc.register_trial(
        strategy_name=f"Concurrent_{worker_id}",
        parameters={"w": worker_id},
        metrics={"total_trades": 30},
    )


class TestEventDrivenBacktesterZeroTrust(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_bt_zt_"))
        self.t0 = datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)
        self.registry_file = self.temp_dir / "trial_registry.json"

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_toy_strategy_fx_all_friction_gt_zero(self):
        """
        STRATEGIA 1: FX EUR/USD su Conto in USD.
        TUTTI I PARAMETRI > 0:
        - spread_points = 0.00020 (2 pips) > 0 -> Half spread = 0.00010 ($10 per lotto)
        - slippage_points = 0.00005 (0.5 pips) > 0 -> Slippage = $5 per lotto
        - fixed_commission = $2.50 > 0
        - quantita = 1.00 lotto (100,000 unita')
        Friction per leg: $10 (spread) + $5 (slip) + $2.50 (comm) = $17.50
        Round-trip friction: $35.00

        Calcolo Analitico:
        - Bar 0 (t0): Close=1.08000 -> Segnale BUY 1 lotto
        - Bar 1 (t1): Open=1.08100 -> Entry Fill @ 1.08100. Costi: $17.50
                      Close=1.08600 -> Segnale SELL 1 lotto (chiusura)
        - Bar 2 (t2): Open=1.08700 -> Exit Fill @ 1.08700. Costi: $17.50
        - Gross PnL: (1.08700 - 1.08100) * 100,000 * 1.0 = +$600.00
        - Net PnL: $600.00 - $35.00 = +$565.00
        - Ending Cash: $100,000.00 + $565.00 = $100,565.00 ESATTO AL CENTESIMO.
        """
        s_fx = Strumento(
            simbolo="EURUSD",
            classe="fx",
            valuta_base="EUR",
            valuta_profitto="USD",
            dimensione_contratto=Decimal("100000"),
            fonte="Broker FX Test",
        )

        bars = [
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0,
                close_time=self.t0 + timedelta(hours=1),
                open=Decimal("1.07900"),
                high=Decimal("1.08100"),
                low=Decimal("1.07800"),
                close=Decimal("1.08000"),
                volume=Decimal("1000"),
            ),
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=1),
                close_time=self.t0 + timedelta(hours=2),
                open=Decimal("1.08100"),
                high=Decimal("1.08650"),
                low=Decimal("1.08050"),
                close=Decimal("1.08600"),
                volume=Decimal("1000"),
            ),
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=2),
                close_time=self.t0 + timedelta(hours=3),
                open=Decimal("1.08700"),
                high=Decimal("1.08800"),
                low=Decimal("1.08500"),
                close=Decimal("1.08750"),
                volume=Decimal("1000"),
            ),
        ]

        def strategy(bar: Candle, portfolio: Portfolio, engine: EventDrivenBacktester):
            if engine.current_bar_index == 0:
                return SignalEvent(
                    timestamp=bar.close_time,
                    symbol="EURUSD",
                    direction=Direction.BUY,
                    quantity=Decimal("1.00"),
                )
            elif engine.current_bar_index == 1:
                return SignalEvent(
                    timestamp=bar.close_time,
                    symbol="EURUSD",
                    direction=Direction.SELL,
                    quantity=Decimal("1.00"),
                )
            return None

        engine = EventDrivenBacktester(
            strumento=s_fx,
            valuta_conto="USD",
            initial_capital=Decimal("100000.00"),
            spread_points=Decimal("0.00020"),
            fixed_commission_per_order=Decimal("2.50"),
            slippage_points=Decimal("0.00005"),
        )

        portfolio = engine.run(bars, strategy)

        self.assertEqual(len(portfolio.trade_history), 1)
        t = portfolio.trade_history[0]
        self.assertEqual(t.entry_price, Decimal("1.08100"))
        self.assertEqual(t.exit_price, Decimal("1.08700"))
        self.assertEqual(t.gross_pnl, Decimal("600.00"))
        self.assertEqual(t.total_commission, Decimal("5.00"))
        self.assertEqual(t.total_spread_cost, Decimal("20.00"))
        self.assertEqual(t.total_slippage, Decimal("10.00"))
        self.assertEqual(t.net_pnl, Decimal("565.00"))
        self.assertEqual(portfolio.cash, Decimal("100565.00"))

    def test_02_toy_strategy_future_es_currency_conversion_gap_down(self):
        """
        STRATEGIA 2: Future CME E-mini S&P 500 (ES) su Conto in EUR.
        TUTTI I PARAMETRI > 0:
        - s.passo_tick = 0.25, s.valore_tick = 12.50 USD
        - cambio_valuta = 1.25 USD per 1 EUR (tasso di conversione) > 0
        - quantita = 2 contratti
        - spread_points = 0.50 (2 ticks) -> Half spread = 0.25 (1 tick)
          Costo spread leg: (0.25 / 0.25) * $12.50 * 2 = $25 USD / 1.25 = 20.00 EUR > 0
        - slippage_points = 0.25 (1 tick)
          Costo slippage leg: (0.25 / 0.25) * $12.50 * 2 = $25 USD / 1.25 = 20.00 EUR > 0
        - fixed_commission = 5.00 EUR > 0
        Friction per leg: 20 + 20 + 5 = 45.00 EUR. Round-trip: 90.00 EUR.

        Calcolo Analitico Gap Down:
        - Bar 0 (t0): Close=5800.00 -> BUY 2 contratti, Stop Loss = 5780.00
        - Bar 1 (t1): Open=5802.00 -> Entry Fill @ 5802.00. Costo ingresso: 45.00 EUR
        - Bar 2 (t2): GAP DOWN! Open=5770.00 (< Stop Loss 5780.00!)
                      Regola Ferrea: Fill forzato ad Open = 5770.00 (slippage da gap reale)
                      Costo uscita: 45.00 EUR
        - Distanza: 5770.00 - 5802.00 = -32.00 punti (-128 ticks)
        - PnL lordo USD: -128 * $12.50 * 2 = -$3,200.00 USD
        - PnL lordo EUR: -$3,200.00 / 1.25 = -2,560.00 EUR
        - Costi totali: 90.00 EUR
        - Net PnL EUR: -2,560.00 - 90.00 = -2,650.00 EUR
        - Ending Cash: 100,000.00 - 2,650.00 = 97,350.00 EUR ESATTO AL CENTESIMO.
        """
        s_es = Strumento(
            simbolo="ES",
            classe="future",
            valuta_profitto="USD",
            dimensione_contratto=Decimal("1"),
            passo_tick=Decimal("0.25"),
            valore_tick=Decimal("12.50"),
            fonte="CME ES Spec",
        )

        bars = [
            Candle(
                symbol="ES",
                timeframe="1H",
                open_time=self.t0,
                close_time=self.t0 + timedelta(hours=1),
                open=Decimal("5795.00"),
                high=Decimal("5805.00"),
                low=Decimal("5790.00"),
                close=Decimal("5800.00"),
                volume=Decimal("5000"),
            ),
            Candle(
                symbol="ES",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=1),
                close_time=self.t0 + timedelta(hours=2),
                open=Decimal("5802.00"),
                high=Decimal("5810.00"),
                low=Decimal("5795.00"),
                close=Decimal("5805.00"),
                volume=Decimal("5000"),
            ),
            Candle(
                symbol="ES",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=2),
                close_time=self.t0 + timedelta(hours=3),
                open=Decimal("5770.00"),  # GAP DOWN SOTTO SL (5780.00)
                high=Decimal("5775.00"),
                low=Decimal("5765.00"),
                close=Decimal("5772.00"),
                volume=Decimal("5000"),
            ),
        ]

        def strategy(bar: Candle, portfolio: Portfolio, engine: EventDrivenBacktester):
            if engine.current_bar_index == 0:
                return SignalEvent(
                    timestamp=bar.close_time,
                    symbol="ES",
                    direction=Direction.BUY,
                    quantity=Decimal("2.00"),
                    stop_loss=Decimal("5780.00"),
                )
            return None

        engine = EventDrivenBacktester(
            strumento=s_es,
            valuta_conto="EUR",
            initial_capital=Decimal("100000.00"),
            cambio_valuta=Decimal("1.25000"),
            spread_points=Decimal("0.50"),
            fixed_commission_per_order=Decimal("5.00"),
            slippage_points=Decimal("0.25"),
        )

        portfolio = engine.run(bars, strategy)

        self.assertEqual(len(portfolio.trade_history), 1)
        t = portfolio.trade_history[0]
        self.assertTrue(t.is_gap_slippage)
        self.assertEqual(t.exit_reason, "GAP_STOP_LOSS")
        self.assertEqual(t.entry_price, Decimal("5802.00"))
        self.assertEqual(t.exit_price, Decimal("5770.00"))
        self.assertEqual(t.gross_pnl, Decimal("-2560.00"))
        self.assertEqual(t.total_commission, Decimal("10.00"))
        self.assertEqual(t.total_spread_cost, Decimal("40.00"))
        self.assertEqual(t.total_slippage, Decimal("40.00"))
        self.assertEqual(t.net_pnl, Decimal("-2650.00"))
        self.assertEqual(portfolio.cash, Decimal("97350.00"))

    def test_03_intrabar_stop_loss_on_entry_bar(self):
        """
        DIMOSTRAZIONE RISOLUZIONE BUG 5:
        Un ordine entra all'Open(t1)=1.08000 con SL=1.07700.
        Durante la barra t1, il prezzo tocca Low=1.07600.
        Il motore DEVE eseguire lo stop intrabarra a 1.07700 nella stessa barra t1!
        """
        s_fx = Strumento(
            simbolo="EURUSD",
            classe="fx",
            valuta_base="EUR",
            valuta_profitto="USD",
            dimensione_contratto=Decimal("100000"),
            fonte="Broker FX Test",
        )

        bars = [
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0,
                close_time=self.t0 + timedelta(hours=1),
                open=Decimal("1.07900"),
                high=Decimal("1.08100"),
                low=Decimal("1.07800"),
                close=Decimal("1.08000"),
                volume=Decimal("1000"),
            ),
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=1),
                close_time=self.t0 + timedelta(hours=2),
                open=Decimal("1.08000"),  # Ingresso Buy qui
                high=Decimal("1.08050"),
                low=Decimal("1.07600"),   # Tocca SL a 1.07700!
                close=Decimal("1.07800"),
                volume=Decimal("1000"),
            ),
        ]

        def strategy(bar: Candle, portfolio: Portfolio, engine: EventDrivenBacktester):
            if engine.current_bar_index == 0:
                return SignalEvent(
                    timestamp=bar.close_time,
                    symbol="EURUSD",
                    direction=Direction.BUY,
                    quantity=Decimal("1.00"),
                    stop_loss=Decimal("1.07700"),
                )
            return None

        engine = EventDrivenBacktester(
            strumento=s_fx,
            valuta_conto="USD",
            initial_capital=Decimal("100000.00"),
            spread_points=Decimal("0.00010"),
            fixed_commission_per_order=Decimal("2.00"),
            slippage_points=Decimal("0.00005"),
        )

        portfolio = engine.run(bars, strategy)

        # La posizione deve essere stata chiusa a 1.07700 nella barra t1!
        self.assertEqual(len(portfolio.trade_history), 1)
        t = portfolio.trade_history[0]
        self.assertEqual(t.exit_reason, "INTRABAR_STOP_LOSS")
        self.assertEqual(t.exit_price, Decimal("1.07700"))
        self.assertEqual(len(portfolio.positions), 0)

    def test_04_intrabar_ambiguity_pessimistic_rule(self):
        """
        DIMOSTRAZIONE RISOLUZIONE BUG 6:
        Durante la barra, sia lo Stop Loss (Low <= SL) sia il Take Profit (High >= TP) vengono toccati.
        Regola pessimistica ferrea: eseguire Stop Loss, impostare is_ambiguous_intrabar = True
        e aggiungere condizione {H_intrabar_worst_case}.
        """
        s_fx = Strumento(
            simbolo="EURUSD",
            classe="fx",
            valuta_base="EUR",
            valuta_profitto="USD",
            dimensione_contratto=Decimal("100000"),
            fonte="Broker FX Test",
        )

        bars = [
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0,
                close_time=self.t0 + timedelta(hours=1),
                open=Decimal("1.08000"),
                high=Decimal("1.08200"),
                low=Decimal("1.07900"),
                close=Decimal("1.08100"),
                volume=Decimal("1000"),
            ),
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=1),
                close_time=self.t0 + timedelta(hours=2),
                open=Decimal("1.08100"),
                high=Decimal("1.09500"),  # Tocca TP a 1.09000!
                low=Decimal("1.07000"),   # Tocca SL a 1.07500!
                close=Decimal("1.08200"),
                volume=Decimal("1000"),
            ),
        ]

        def strategy(bar: Candle, portfolio: Portfolio, engine: EventDrivenBacktester):
            if engine.current_bar_index == 0:
                return SignalEvent(
                    timestamp=bar.close_time,
                    symbol="EURUSD",
                    direction=Direction.BUY,
                    quantity=Decimal("1.00"),
                    stop_loss=Decimal("1.07500"),
                    take_profit=Decimal("1.09000"),
                )
            return None

        engine = EventDrivenBacktester(
            strumento=s_fx,
            valuta_conto="USD",
            initial_capital=Decimal("100000.00"),
            spread_points=Decimal("0.00010"),
            fixed_commission_per_order=Decimal("2.00"),
            slippage_points=Decimal("0.00005"),
        )

        portfolio = engine.run(bars, strategy)

        self.assertEqual(len(portfolio.trade_history), 1)
        t = portfolio.trade_history[0]
        # Esecuzione pessimistica confermata
        self.assertEqual(t.exit_reason, "AMBIGUOUS_INTRABAR_STOP_LOSS")
        self.assertEqual(t.exit_price, Decimal("1.07500"))  # Eseguito a SL, NON a TP!
        self.assertTrue(t.is_ambiguous_intrabar)
        self.assertIn("{H_intrabar_worst_case}", t.condizioni)

    def test_05_max_drawdown_intrabar_vs_close(self):
        """
        DIMOSTRAZIONE RISOLUZIONE BUG 7:
        Verifica che max_drawdown_intrabar catturi le escursioni sfavorevoli intrabarra
        anche se la barra chiude a prezzi superiori.
        """
        s_fx = Strumento(
            simbolo="EURUSD",
            classe="fx",
            valuta_base="EUR",
            valuta_profitto="USD",
            dimensione_contratto=Decimal("100000"),
            fonte="Broker FX Test",
        )

        bars = [
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0,
                close_time=self.t0 + timedelta(hours=1),
                open=Decimal("1.08000"),
                high=Decimal("1.08200"),
                low=Decimal("1.07900"),
                close=Decimal("1.08100"),
                volume=Decimal("1000"),
            ),
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=1),
                close_time=self.t0 + timedelta(hours=2),
                open=Decimal("1.08100"),
                high=Decimal("1.08200"),
                low=Decimal("1.07000"),   # Escursione avversa di 110 pips!
                close=Decimal("1.08150"),  # Chiusura positiva (+5 pips)
                volume=Decimal("1000"),
            ),
        ]

        def strategy(bar: Candle, portfolio: Portfolio, engine: EventDrivenBacktester):
            if engine.current_bar_index == 0:
                return SignalEvent(
                    timestamp=bar.close_time,
                    symbol="EURUSD",
                    direction=Direction.BUY,
                    quantity=Decimal("1.00"),
                )
            return None

        engine = EventDrivenBacktester(
            strumento=s_fx,
            valuta_conto="USD",
            initial_capital=Decimal("100000.00"),
            spread_points=Decimal("0.00010"),
            fixed_commission_per_order=Decimal("2.00"),
            slippage_points=Decimal("0.00005"),
        )

        portfolio = engine.run(bars, strategy)

        # Max drawdown intrabarra deve essere marcatamente superiore al drawdown al close
        self.assertGreater(portfolio.max_drawdown_intrabar, portfolio.max_drawdown_close)
        # Low a 1.07000 vs Open a 1.08100 = 110 pips * 100k = $1100 + friction > $1100
        self.assertGreater(portfolio.max_drawdown_intrabar, Decimal("1100.00"))

    def test_06_dsr_returns_valore_non_stimabile_when_insufficient_trades(self):
        """
        DIMOSTRAZIONE RISOLUZIONE BUG 3 & 10:
        Se total_trades < 30, sharpe_ratio e deflated_sharpe_ratio devono essere
        oggetti Valore con incertezza NON_STIMABILE e valore = None (MAI 0.0!).
        """
        s_fx = Strumento(
            simbolo="EURUSD",
            classe="fx",
            valuta_base="EUR",
            valuta_profitto="USD",
            dimensione_contratto=Decimal("100000"),
            fonte="Broker FX Test",
        )
        portfolio = Portfolio(strumento=s_fx, initial_cash=Decimal("100000.00"))
        # Portafoglio vuoto o con soli 2 trade
        metrics = DSRCalculator.evaluate_portfolio(
            portfolio,
            registry_path=self.registry_file,
            dry_run=True,
        )

        sr = metrics["sharpe_ratio"]
        dsr = metrics["deflated_sharpe_ratio"]

        self.assertIsInstance(sr, Valore)
        self.assertIsInstance(dsr, Valore)
        self.assertIsNone(sr.valore)
        self.assertIsNone(dsr.valore)
        self.assertEqual(sr.incertezza, NON_STIMABILE)
        self.assertEqual(dsr.incertezza, NON_STIMABILE)

    def test_07_reduce_only_discards_order_when_position_already_closed_by_gap_stop(self):
        """
        DIMOSTRAZIONE BUG REDUCE_ONLY:
        Se un ordine pendente di chiusura (reduce_only=True) arriva in Fase 1.B
        ma la posizione è già stata chiusa in Fase 1.A per GAP_STOP_LOSS,
        l'ordine deve essere scartato senza aprire una posizione inversa scoperta.
        """
        s_fx = Strumento(
            simbolo="EURUSD",
            classe="fx",
            valuta_base="EUR",
            valuta_profitto="USD",
            dimensione_contratto=Decimal("100000"),
            fonte="Broker FX Test",
        )
        bars = [
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0,
                close_time=self.t0 + timedelta(hours=1),
                open=Decimal("1.08000"),
                high=Decimal("1.08200"),
                low=Decimal("1.07900"),
                close=Decimal("1.08000"),
                volume=Decimal("1000"),
            ),
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=1),
                close_time=self.t0 + timedelta(hours=2),
                open=Decimal("1.08100"),
                high=Decimal("1.08300"),
                low=Decimal("1.07800"),
                close=Decimal("1.07850"),
                volume=Decimal("1000"),
            ),
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=2),
                close_time=self.t0 + timedelta(hours=3),
                open=Decimal("1.07000"),  # GAP DOWN violento sotto SL (1.07500)
                high=Decimal("1.07200"),
                low=Decimal("1.06900"),
                close=Decimal("1.07100"),
                volume=Decimal("1000"),
            ),
        ]

        def strategy(bar: Candle, portfolio: Portfolio, engine: EventDrivenBacktester):
            if engine.current_bar_index == 0:
                # Barra 0: entra LONG con SL a 1.07500
                return SignalEvent(
                    timestamp=bar.close_time,
                    symbol="EURUSD",
                    direction=Direction.BUY,
                    quantity=Decimal("1.00"),
                    stop_loss=Decimal("1.07500"),
                )
            elif engine.current_bar_index == 1:
                # Barra 1: la strategia decide di chiudere a mercato con reduce_only=True
                return SignalEvent(
                    timestamp=bar.close_time,
                    symbol="EURUSD",
                    direction=Direction.SELL,
                    quantity=Decimal("1.00"),
                    reduce_only=True,
                )
            return None

        engine = EventDrivenBacktester(
            strumento=s_fx,
            valuta_conto="USD",
            initial_capital=Decimal("100000.00"),
            spread_points=Decimal("0.00010"),
            fixed_commission_per_order=Decimal("2.00"),
            slippage_points=Decimal("0.00005"),
        )

        portfolio = engine.run(bars, strategy)

        # 1. Nessuna posizione inversa (SHORT) deve essere rimasta aperta!
        self.assertEqual(len(portfolio.positions), 0, "Non devono esserci posizioni aperte residue.")

        # 2. Ci deve essere ESATTAMENTE 1 trade (quello chiuso per GAP_STOP_LOSS in 1.A)
        self.assertEqual(len(portfolio.trade_history), 1, "Deve esserci solo il trade di GAP_STOP_LOSS.")
        t = portfolio.trade_history[0]
        self.assertEqual(t.exit_reason, "GAP_STOP_LOSS")
        self.assertEqual(t.exit_price, Decimal("1.07000"))

    def test_08_intrabar_peak_equity_tracks_bar_high_low_not_close(self):
        """RED TEAM CRITICO-1: peak_equity_intrabar deve tracciare eq_best_intrabar (High per LONG) e non solo eq_close."""
        s_fx = Strumento(
            simbolo="EURUSD", classe="fx", valuta_base="EUR", valuta_profitto="USD",
            dimensione_contratto=Decimal("100000"), fonte="test",
        )
        bars = [
            Candle("EURUSD", "1H", self.t0, self.t0 + timedelta(hours=1),
                   Decimal("1.08000"), Decimal("1.08100"), Decimal("1.07900"), Decimal("1.08000"), Decimal("100")),
            # Bar 1: Entra a 1.08000. Sale fino a 1.09000 (+1000 USD picco!) poi scende a 1.07500 (-500 USD), chiude a 1.08000 (0 PnL al close).
            Candle("EURUSD", "1H", self.t0 + timedelta(hours=1), self.t0 + timedelta(hours=2),
                   Decimal("1.08000"), Decimal("1.09000"), Decimal("1.07500"), Decimal("1.08000"), Decimal("100")),
        ]
        def strat(bar, p, eng):
            if eng.current_bar_index == 0:
                return SignalEvent(bar.close_time, "EURUSD", Direction.BUY, Decimal("1.00"))
            return None

        eng = EventDrivenBacktester(s_fx, "USD", Decimal("100000.00"), Decimal("0.00010"), Decimal("2.50"), Decimal("0.00005"))
        p = eng.run(bars, strat)

        # Entry friction = 5.00 + 5.00 + 2.50 = 12.50 -> cash = 99987.50
        # Best intrabar (High 1.09000) = 99987.50 + 1000.00 = 100987.50 (senza costi uscita latenti)
        # Worst intrabar (Low 1.07500) = 99987.50 - 500.00 - 12.50 = 99475.00
        # Vero DD intrabarra = 100987.50 - 99475.00 = 1512.50
        self.assertGreaterEqual(p.peak_equity_intrabar, Decimal("100987.50"))
        self.assertEqual(p.max_drawdown_intrabar, Decimal("1512.50"))

    def test_09_weekend_session_gap_executes_order_with_metadata(self):
        """RED TEAM CRITICO-2: un gap di sessione/weekend esegue l'ordine ad Open(t) con metadata is_session_gap=True."""
        s_fx = Strumento(
            simbolo="EURUSD", classe="fx", valuta_base="EUR", valuta_profitto="USD",
            dimensione_contratto=Decimal("100000"), fonte="test",
        )
        t_fri = datetime(2026, 1, 2, 21, 0, tzinfo=timezone.utc)
        t_mon = datetime(2026, 1, 5, 22, 0, tzinfo=timezone.utc)  # Gap weekend > 48h
        bars = [
            Candle("EURUSD", "1H", t_fri, t_fri + timedelta(hours=1),
                   Decimal("1.08000"), Decimal("1.08100"), Decimal("1.07900"), Decimal("1.08050"), Decimal("100")),
            Candle("EURUSD", "1H", t_mon, t_mon + timedelta(hours=1),
                   Decimal("1.08500"), Decimal("1.08600"), Decimal("1.08400"), Decimal("1.08550"), Decimal("100")),
        ]
        def strat(bar, p, eng):
            if eng.current_bar_index == 0:
                return SignalEvent(bar.close_time, "EURUSD", Direction.BUY, Decimal("1.00"))
            return None

        eng = EventDrivenBacktester(s_fx, "USD", Decimal("100000.00"), Decimal("0.00010"), Decimal("2.50"), Decimal("0.00005"))
        p = eng.run(bars, strat)

        self.assertEqual(len(p.trade_history), 1)
        self.assertEqual(p.trade_history[0].entry_price, Decimal("1.08500"))
        # Verifica metadati is_session_gap sul FillEvent eseguito
        session_gap_fills = [f for f in p.fill_history if f.metadata.get("is_session_gap")]
        self.assertEqual(len(session_gap_fills), 1)
        self.assertGreater(session_gap_fills[0].metadata.get("session_gap_delay_seconds", 0), 0)

        # Verifica che bar.open_time < target_bar_open_time continui a sollevare LookAheadViolationError
        bars_backward = [
            Candle("EURUSD", "1H", t_mon, t_mon + timedelta(hours=1),
                   Decimal("1.080"), Decimal("1.081"), Decimal("1.079"), Decimal("1.080"), Decimal("100")),
            Candle("EURUSD", "1H", t_fri, t_fri + timedelta(hours=1),
                   Decimal("1.081"), Decimal("1.082"), Decimal("1.080"), Decimal("1.081"), Decimal("100")),
        ]
        with self.assertRaises(LookAheadViolationError):
            EventDrivenBacktester(s_fx, "USD", Decimal("100000.00")).run(bars_backward, strat)

    def test_10_pyramiding_error_does_not_corrupt_cash(self):
        """RED TEAM ALTO-2: piramidazione rifiutata PRIMA di toccare self.cash."""
        s_fx = Strumento(
            simbolo="EURUSD", classe="fx", valuta_base="EUR", valuta_profitto="USD",
            dimensione_contratto=Decimal("100000"), fonte="test",
        )
        p = Portfolio(s_fx, initial_cash=Decimal("100000.00"))
        f1 = FillEvent(self.t0, "EURUSD", Direction.BUY, Decimal("1.00"), Decimal("1.08000"),
                       Decimal("2.50"), Decimal("5.00"), Decimal("5.00"))
        p.on_fill(f1)
        cash_after_f1 = p.cash
        self.assertEqual(cash_after_f1, Decimal("99987.50"))

        f2 = FillEvent(self.t0 + timedelta(hours=1), "EURUSD", Direction.BUY, Decimal("1.00"), Decimal("1.08100"),
                       Decimal("2.50"), Decimal("5.00"), Decimal("5.00"))
        with self.assertRaises(NotImplementedError):
            p.on_fill(f2)
        self.assertEqual(p.cash, cash_after_f1, "La cassa non deve essere corrotta dopo NotImplementedError.")

    def test_11_dsr_dry_run_readonly_and_counts_simulated_trial(self):
        """RED TEAM ALTO-3 + ALTO-4: dry_run=True e' readonly (non crea trial_registry.json) e usa N = total_trials + 1."""
        s_fx = Strumento(
            simbolo="EURUSD", classe="fx", valuta_base="EUR", valuta_profitto="USD",
            dimensione_contratto=Decimal("100000"), fonte="test",
        )
        p = Portfolio(s_fx, initial_cash=Decimal("100000.00"))
        from brain.laboratorio.backtester.events import TradeRecord
        for i in range(35):
            pnl = Decimal("100.00") if i % 2 == 0 else Decimal("-50.00")
            p.trade_history.append(TradeRecord(
                symbol="EURUSD", direction=Direction.BUY, quantity=Decimal("1"),
                entry_time=self.t0 + timedelta(hours=i), entry_price=Decimal("1.08"),
                exit_time=self.t0 + timedelta(hours=i + 1), exit_price=Decimal("1.081"),
                gross_pnl=pnl, net_pnl=pnl,
                total_commission=Decimal("0"), total_spread_cost=Decimal("0"),
                total_slippage=Decimal("0"), exit_reason="TEST",
            ))

        reg_path = self.temp_dir / "non_existent_registry.json"
        self.assertFalse(reg_path.exists())
        metrics = DSRCalculator.evaluate_portfolio(p, registry_path=reg_path, dry_run=True)
        self.assertFalse(reg_path.exists(), "dry_run=True NON deve creare o scrivere trial_registry.json su disco.")
        self.assertIn("N=1 trials", metrics["deflated_sharpe_ratio"].nota)

    def test_12_dsr_concurrent_locking_atomicity(self):
        """RED TEAM ALTO-3: registrazioni concorrenti su trial_registry.json devono essere atomiche senza perdite."""
        reg_path = self.temp_dir / "concurrent_registry.json"
        ctx = multiprocessing.get_context("spawn")
        num_workers = 8
        with ctx.Pool(processes=4) as pool:
            ids = pool.starmap(_worker_register_trial, [(str(reg_path), i) for i in range(num_workers)])

        self.assertEqual(sorted(ids), list(range(1, num_workers + 1)))
        data = json.loads(reg_path.read_text(encoding="utf-8"))
        self.assertEqual(data["total_trials"], num_workers)
        self.assertEqual(len(data["trials"]), num_workers)

    def test_13_dsr_pathological_variance_term_returns_non_stimabile(self):
        """RED TEAM BASSO-4: se variance_term <= 0, non mascherare con 1e-6 ma restituire NON_STIMABILE."""
        res_dsr, res_std = DSRCalculator.calculate_dsr_analytical(
            sharpe_estimated=2.0,
            num_trials=5,
            track_record_length=50,
            skewness=5.0,
            kurtosis=1.0,  # variance_term = 1 - 10 + 0 = -9 <= 0
        )
        self.assertIsNone(res_dsr)
        self.assertIsNone(res_std)

        # Verifica anche via evaluate_portfolio con distribuzione patologicamente asimmetrica
        s_fx = Strumento(
            simbolo="EURUSD", classe="fx", valuta_base="EUR", valuta_profitto="USD",
            dimensione_contratto=Decimal("100000"), fonte="test",
        )
        p = Portfolio(s_fx, initial_cash=Decimal("100000.00"))
        from brain.laboratorio.backtester.events import TradeRecord
        # Costruiamo >=30 trade dove skewness e' estremamente alta e sharpe alto ma kurtosis non compensa -> controlliamo che NON venga mascherato se patologico
        # Nota: per la disuguaglianza di Pearson (kurt >= skew^2 + 1), con campioni reali (kurt >= skew^2 + 1) variance_term = 1 - s*sr + ((k-1)/4)*sr^2 >= (1 - s*sr/2)^2 >= 0!
        # L'unico modo per avere variance_term <= 0 in campioni reali e' kurt = skew^2 + 1 e s*sr/2 == 1 -> variance_term == 0!
        # Simuliamo esplicitamente una distribuzione di esattamente 2 valori: 29 volte -1 e 1 volta +9 -> skew positivo e k - 1 = skew^2 -> verifichiamo se almeno la path patologica in evaluate_portfolio gestisce (None, None).
        from unittest.mock import patch
        for i in range(30):
            pnl = Decimal("100") if i % 2 == 0 else Decimal("-10")
            p.trade_history.append(TradeRecord(
                symbol="EURUSD", direction=Direction.BUY, quantity=Decimal("1"),
                entry_time=self.t0 + timedelta(hours=i), entry_price=Decimal("1.08"),
                exit_time=self.t0 + timedelta(hours=i + 1), exit_price=Decimal("1.081"),
                gross_pnl=pnl, net_pnl=pnl,
                total_commission=Decimal("0"), total_spread_cost=Decimal("0"),
                total_slippage=Decimal("0"), exit_reason="TEST",
            ))
        with patch.object(DSRCalculator, "calculate_dsr_analytical", return_value=(None, None)):
            metrics = DSRCalculator.evaluate_portfolio(p, registry_path=self.registry_file, dry_run=True)
            self.assertEqual(metrics["deflated_sharpe_ratio"].incertezza, NON_STIMABILE)
            self.assertIsNone(metrics["deflated_sharpe_ratio"].valore)

    def test_14_intrabar_fill_timing_and_discarded_end_of_data_orders(self):
        """RED TEAM MEDIO-1 + MEDIO-2: fill_timing='intrabar_close_assumed' e tracciamento discarded_end_of_data_orders."""
        s_fx = Strumento(
            simbolo="EURUSD", classe="fx", valuta_base="EUR", valuta_profitto="USD",
            dimensione_contratto=Decimal("100000"), fonte="test",
        )
        bars = [
            Candle("EURUSD", "1H", self.t0, self.t0 + timedelta(hours=1),
                   Decimal("1.08000"), Decimal("1.08100"), Decimal("1.07900"), Decimal("1.08000"), Decimal("100")),
            # Bar 1: Entra Long a 1.08000, SL a 1.07500 colpito intrabarra!
            Candle("EURUSD", "1H", self.t0 + timedelta(hours=1), self.t0 + timedelta(hours=2),
                   Decimal("1.08000"), Decimal("1.08200"), Decimal("1.07400"), Decimal("1.07800"), Decimal("100")),
            # Bar 2: Ultima barra emette segnale per t+1 (che non esiste) -> deve finire in discarded_end_of_data_orders
            Candle("EURUSD", "1H", self.t0 + timedelta(hours=2), self.t0 + timedelta(hours=3),
                   Decimal("1.07800"), Decimal("1.07900"), Decimal("1.07700"), Decimal("1.07850"), Decimal("100")),
        ]
        def strat(bar, p, eng):
            if eng.current_bar_index == 0:
                return SignalEvent(bar.close_time, "EURUSD", Direction.BUY, Decimal("1.00"), stop_loss=Decimal("1.07500"))
            if eng.current_bar_index == 2:
                return SignalEvent(bar.close_time, "EURUSD", Direction.BUY, Decimal("1.00"))
            return None

        eng = EventDrivenBacktester(s_fx, "USD", Decimal("100000.00"), Decimal("0.00010"), Decimal("2.50"), Decimal("0.00005"))
        p = eng.run(bars, strat)

        self.assertEqual(len(p.trade_history), 1)
        self.assertEqual(p.trade_history[0].fill_timing, "intrabar_close_assumed")
        self.assertEqual(len(p.discarded_end_of_data_orders), 1)
        self.assertEqual(len(eng.pending_orders), 0)

    def test_15_portfolio_on_fill_atomic_when_calcola_pnl_raises(self):
        """ALTO-2 residuo: se calcola_pnl_monetario() solleva ValueError in chiusura, cash e fill_history restano intatti."""
        s_es = Strumento(
            simbolo="ES",
            classe="future",
            valuta_base="USD",
            valuta_profitto="USD",
            dimensione_contratto=None,
            passo_tick=Decimal("0.25"),
            valore_tick=Decimal("12.50"),
            fonte="CME",
        )
        p = Portfolio(s_es, valuta_conto="EUR", initial_cash=Decimal("100000.00"), cambio_valuta=None)
        # Apertura posizione (non invoca calcola_pnl_monetario)
        p.on_fill(FillEvent(
            timestamp=self.t0,
            symbol="ES",
            direction=Direction.BUY,
            quantity=Decimal("1"),
            fill_price=Decimal("5800.00"),
            commission=Decimal("5.00"),
            spread_cost=Decimal("10.00"),
            slippage=Decimal("10.00"),
        ))
        cash_before = p.cash
        fills_before = len(p.fill_history)

        with self.assertRaises(ValueError):
            p.on_fill(FillEvent(
                timestamp=self.t0 + timedelta(hours=1),
                symbol="ES",
                direction=Direction.SELL,
                quantity=Decimal("1"),
                fill_price=Decimal("5810.00"),
                commission=Decimal("5.00"),
                spread_cost=Decimal("10.00"),
                slippage=Decimal("10.00"),
            ))

        self.assertEqual(p.cash, cash_before, "cash non deve essere mutato se calcola_pnl_monetario fallisce.")
        self.assertEqual(len(p.fill_history), fills_before, "fill_history non deve contenere il fill fallito.")
        self.assertIn("ES", p.positions)

    def test_16_rejected_orders_invalid_sl_tp_post_gap(self):
        """ALTO-7: ordini di apertura con SL/TP resi invalidi da un gap ad Open(t) vengono scartati in rejected_orders."""
        s_fx = Strumento(
            simbolo="EURUSD", classe="fx", valuta_base="EUR", valuta_profitto="USD",
            dimensione_contratto=Decimal("100000"), fonte="test",
        )
        # Caso A (BUY invalidato da gap down sotto stop_loss e gap up oltre take_profit)
        bars_buy = [
            Candle("EURUSD", "1H", self.t0, self.t0 + timedelta(hours=1),
                   Decimal("1.08000"), Decimal("1.08100"), Decimal("1.07900"), Decimal("1.08000"), Decimal("100")),
            # Gap down ad Open=1.07400 (stop_loss=1.07500 >= Open -> invalido!)
            Candle("EURUSD", "1H", self.t0 + timedelta(hours=1), self.t0 + timedelta(hours=2),
                   Decimal("1.07400"), Decimal("1.07600"), Decimal("1.07300"), Decimal("1.07500"), Decimal("100")),
        ]
        def strat_buy_bad_sl(bar, p, eng):
            if eng.current_bar_index == 0:
                return SignalEvent(bar.close_time, "EURUSD", Direction.BUY, Decimal("1.00"),
                                   stop_loss=Decimal("1.07500"), take_profit=Decimal("1.09000"))
            return None

        eng1 = EventDrivenBacktester(s_fx, "USD", Decimal("100000.00"), Decimal("0.00010"), Decimal("2.50"), Decimal("0.00005"))
        p1 = eng1.run(bars_buy, strat_buy_bad_sl)
        self.assertEqual(len(p1.positions), 0)
        self.assertEqual(len(p1.fill_history), 0)
        self.assertEqual(len(p1.rejected_orders), 1)
        self.assertEqual(p1.cash, Decimal("100000.00"))

        # Caso B (SELL invalidato da gap up oltre stop_loss / gap down sotto take_profit)
        bars_sell = [
            Candle("EURUSD", "1H", self.t0, self.t0 + timedelta(hours=1),
                   Decimal("1.08000"), Decimal("1.08100"), Decimal("1.07900"), Decimal("1.08000"), Decimal("100")),
            # Gap down ad Open=1.06900 (take_profit=1.07000 >= Open per SELL -> invalido!)
            Candle("EURUSD", "1H", self.t0 + timedelta(hours=1), self.t0 + timedelta(hours=2),
                   Decimal("1.06900"), Decimal("1.07200"), Decimal("1.06800"), Decimal("1.07100"), Decimal("100")),
        ]
        def strat_sell_bad_tp(bar, p, eng):
            if eng.current_bar_index == 0:
                return SignalEvent(bar.close_time, "EURUSD", Direction.SELL, Decimal("1.00"),
                                   stop_loss=Decimal("1.08500"), take_profit=Decimal("1.07000"))
            return None

        eng2 = EventDrivenBacktester(s_fx, "USD", Decimal("100000.00"), Decimal("0.00010"), Decimal("2.50"), Decimal("0.00005"))
        p2 = eng2.run(bars_sell, strat_sell_bad_tp)
        self.assertEqual(len(p2.positions), 0)
        self.assertEqual(len(p2.fill_history), 0)
        self.assertEqual(len(p2.rejected_orders), 1)
        self.assertEqual(p2.cash, Decimal("100000.00"))


if __name__ == "__main__":
    unittest.main()
