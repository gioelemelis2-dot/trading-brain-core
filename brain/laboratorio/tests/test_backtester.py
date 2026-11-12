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
    Direction,
    LookAheadViolationError,
    DSRCalculator,
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


if __name__ == "__main__":
    unittest.main()
