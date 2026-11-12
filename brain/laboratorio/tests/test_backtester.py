"""
Suite di Test per il Backtester Strictly Event-Driven e Deflated Sharpe Ratio.
Verifiche:
1. Strategia Giocattolo 1: Ciclo deterministico 2-trade verificato al centesimo ($100,028.00).
2. Strategia Giocattolo 2: Gap Down oltre lo Stop Loss con slippage reale al centesimo ($99,887.00).
3. Test Avversariali Anti-Lookahead: Rifiuto segnali con timestamp incoerenti e divieto same-bar execution.
4. Funzionamento del contatore globale N in trial_registry.json e calcolo del DSR (Bailey & Lopez de Prado).
"""

import sys
import unittest
import tempfile
import shutil
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from decimal import Decimal

# Assicuriamo import relativo al repository
repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.dati.pipeline.models import Candle
from brain.laboratorio.backtester import (
    EventDrivenBacktester,
    Portfolio,
    SignalEvent,
    Direction,
    LookAheadViolationError,
    DSRCalculator,
)


class TestEventDrivenBacktester(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_backtester_"))
        self.t0 = datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)
        self.registry_file = self.temp_dir / "trial_registry.json"

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_toy_strategy_1_reversal_exact_to_the_cent(self):
        """
        STRATEGIA GIOCATTOLO 1: Verifica al centesimo di PnL, commissioni e spread.
        Capitale Iniziale: $100,000.00
        Spread: 0.00010 (1 pip) -> Half-spread leg: $0.50 per 10k unita'
        Commissione Fissa: $2.00 per fill
        Quantita': 10,000 unita'

        Calcolo Analitico a Mano:
        - Bar 0 (t0): Close=1.08100 -> Segnale BUY 10k
        - Bar 1 (t1): Open=1.08120 -> FILL BUY a 1.08120. Costo ingresso: $2 comm + $0.50 spread = $2.50
                      Close=1.08400 -> Segnale SELL 10k (uscita)
        - Bar 2 (t2): Open=1.08450 -> FILL SELL a 1.08450. Costo uscita: $2 comm + $0.50 spread = $2.50
        - Gross PnL: (1.08450 - 1.08120) * 10,000 = 0.00330 * 10,000 = +$33.00
        - Costi Totali Round-Trip: $2.50 + $2.50 = $5.00
        - Net PnL: $33.00 - $5.00 = +$28.00
        - Ending Cash Atteso: $100,000.00 + $28.00 = $100,028.00 ESATTO AL CENTESIMO.
        """
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
                open=Decimal("1.08120"),
                high=Decimal("1.08500"),
                low=Decimal("1.08080"),
                close=Decimal("1.08400"),
                volume=Decimal("1000"),
            ),
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=2),
                close_time=self.t0 + timedelta(hours=3),
                open=Decimal("1.08450"),
                high=Decimal("1.08600"),
                low=Decimal("1.08300"),
                close=Decimal("1.08550"),
                volume=Decimal("1000"),
            ),
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=3),
                close_time=self.t0 + timedelta(hours=4),
                open=Decimal("1.08550"),
                high=Decimal("1.08700"),
                low=Decimal("1.08400"),
                close=Decimal("1.08600"),
                volume=Decimal("1000"),
            ),
        ]

        def toy_strategy(bar: Candle, portfolio: Portfolio, engine: EventDrivenBacktester):
            if engine.current_bar_index == 0:
                # Emette BUY al close di Bar 0
                return SignalEvent(
                    timestamp=bar.close_time,
                    symbol="EURUSD",
                    direction=Direction.BUY,
                    quantity=Decimal("10000"),
                )
            elif engine.current_bar_index == 1:
                # Emette SELL al close di Bar 1
                return SignalEvent(
                    timestamp=bar.close_time,
                    symbol="EURUSD",
                    direction=Direction.SELL,
                    quantity=Decimal("10000"),
                )
            return None

        engine = EventDrivenBacktester(
            symbol="EURUSD",
            initial_capital=Decimal("100000.00"),
            spread_pips=Decimal("0.00010"),
            fixed_commission_per_order=Decimal("2.00"),
            slippage_fixed=Decimal("0.00000"),
        )

        portfolio = engine.run(bars, toy_strategy)

        self.assertEqual(len(portfolio.trade_history), 1)
        trade = portfolio.trade_history[0]

        # Verifiche analitiche al centesimo
        self.assertEqual(trade.entry_price, Decimal("1.08120"))
        self.assertEqual(trade.exit_price, Decimal("1.08450"))
        self.assertEqual(trade.gross_pnl, Decimal("33.00"))
        self.assertEqual(trade.total_commission, Decimal("4.00"))
        self.assertEqual(trade.total_spread_cost, Decimal("1.00"))
        self.assertEqual(trade.net_pnl, Decimal("28.00"))
        self.assertEqual(portfolio.cash, Decimal("100028.00"))
        self.assertEqual(portfolio.equity, Decimal("100028.00"))

    def test_02_toy_strategy_2_gap_down_stop_loss_exact_to_the_cent(self):
        """
        STRATEGIA GIOCATTOLO 2: Gestione Gap e Slippage reale dello Stop Loss al centesimo.
        Capitale Iniziale: $100,000.00
        Spread: 0.00020 (2 pips) -> Half-spread leg: $1.00 per 10k unita'
        Commissione Fissa: $3.00 per fill
        Quantita': 10,000 unita'

        Scenario:
        - Bar 0 (t0): Close=1.10200 -> Segnale BUY 10k con Stop Loss = 1.09500
        - Bar 1 (t1): Open=1.10250 -> FILL BUY a 1.10250. Costo ingresso: $3 comm + $1 spread = $4.00
                      Close=1.10300. Posizione aperta LONG 10k @ 1.10250, SL=1.09500
        - Bar 2 (t2): GAP DOWN! Open=1.09200 (ben oltre lo stop di 1.09500 di 30 pips!)
                      Regola Ferrea: Il backtester deve eseguire a 1.09200 (Open), NON al prezzo nominale di SL 1.09500!
                      Costo uscita: $3 comm + $1 spread = $4.00
        - Gross PnL: (1.09200 - 1.10250) * 10,000 = -0.01050 * 10,000 = -$105.00
        - Costi Totali Round-Trip: $4.00 + $4.00 = $8.00
        - Net PnL: -$105.00 - $8.00 = -$113.00
        - Ending Cash Atteso: $100,000.00 - $113.00 = $99,887.00 ESATTO AL CENTESIMO.
        """
        bars = [
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0,
                close_time=self.t0 + timedelta(hours=1),
                open=Decimal("1.10000"),
                high=Decimal("1.10300"),
                low=Decimal("1.09900"),
                close=Decimal("1.10200"),
                volume=Decimal("1000"),
            ),
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=1),
                close_time=self.t0 + timedelta(hours=2),
                open=Decimal("1.10250"),
                high=Decimal("1.10500"),
                low=Decimal("1.10100"),
                close=Decimal("1.10300"),
                volume=Decimal("1000"),
            ),
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=2),
                close_time=self.t0 + timedelta(hours=3),
                open=Decimal("1.09200"),  # GAP DOWN SOTTO STOP LOSS (1.09500)
                high=Decimal("1.09400"),
                low=Decimal("1.09000"),
                close=Decimal("1.09100"),
                volume=Decimal("1000"),
            ),
        ]

        def gap_strategy(bar: Candle, portfolio: Portfolio, engine: EventDrivenBacktester):
            if engine.current_bar_index == 0:
                return SignalEvent(
                    timestamp=bar.close_time,
                    symbol="EURUSD",
                    direction=Direction.BUY,
                    quantity=Decimal("10000"),
                    stop_loss=Decimal("1.09500"),
                )
            return None

        engine = EventDrivenBacktester(
            symbol="EURUSD",
            initial_capital=Decimal("100000.00"),
            spread_pips=Decimal("0.00020"),
            fixed_commission_per_order=Decimal("3.00"),
            slippage_fixed=Decimal("0.00000"),
        )

        portfolio = engine.run(bars, gap_strategy)

        self.assertEqual(len(portfolio.trade_history), 1)
        trade = portfolio.trade_history[0]

        # Verifica slippage da gap reale
        self.assertTrue(trade.is_gap_slippage)
        self.assertEqual(trade.exit_reason, "GAP_STOP_LOSS")
        self.assertEqual(trade.entry_price, Decimal("1.10250"))
        # Verifica che NON sia stato eseguito a 1.09500 ma a 1.09200
        self.assertEqual(trade.exit_price, Decimal("1.09200"))
        self.assertEqual(trade.gross_pnl, Decimal("-105.00"))
        self.assertEqual(trade.total_commission, Decimal("6.00"))
        self.assertEqual(trade.total_spread_cost, Decimal("2.00"))
        self.assertEqual(trade.net_pnl, Decimal("-113.00"))
        self.assertEqual(portfolio.cash, Decimal("99887.00"))
        self.assertEqual(portfolio.equity, Decimal("99887.00"))

    def test_03_adversarial_lookahead_detection(self):
        """
        STRESS-TEST AVVERSARIALE: Tentativo di iniezione di look-ahead bias.
        Una strategia cerca di emettere un segnale con timestamp futuro o passato.
        Il motore deve bloccare l'esecuzione sollevando LookAheadViolationError.
        """
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
                open=Decimal("1.08120"),
                high=Decimal("1.08500"),
                low=Decimal("1.08080"),
                close=Decimal("1.08400"),
                volume=Decimal("1000"),
            ),
        ]

        def malicious_strategy(bar: Candle, portfolio: Portfolio, engine: EventDrivenBacktester):
            # La strategia mente sul timestamp del segnale (es. anticipa all'open)
            return SignalEvent(
                timestamp=bar.open_time,  # INCOERENTE con bar.close_time!
                symbol="EURUSD",
                direction=Direction.BUY,
                quantity=Decimal("10000"),
            )

        engine = EventDrivenBacktester(symbol="EURUSD")
        with self.assertRaises(LookAheadViolationError):
            engine.run(bars, malicious_strategy)

    def test_04_trial_registry_and_deflated_sharpe_ratio(self):
        """
        Verifica integrazione del contatore globale N e del Deflated Sharpe Ratio (DSR).
        Dimostra che all'aumentare di N (trial registry), il DSR defla a parita' di Sharpe stimato.
        """
        calc = DSRCalculator(registry_path=self.registry_file)
        self.assertEqual(calc.get_total_trials(), 0)

        # Registrazione di 3 prove fittizie
        calc.register_trial("Strat_A", {"param": 1}, {"sharpe_ratio": 1.5, "total_trades": 100})
        calc.register_trial("Strat_B", {"param": 2}, {"sharpe_ratio": 1.8, "total_trades": 100})
        n3 = calc.register_trial("Strat_C", {"param": 3}, {"sharpe_ratio": 2.0, "total_trades": 100})

        self.assertEqual(n3, 3)
        self.assertEqual(calc.get_total_trials(), 3)

        # Calcolo DSR con N=1 vs N=100
        # Per lo stesso Sharpe stimato (es. 1.8) e T=100, DSR diminuisce con l'aumento di N
        dsr_n1 = DSRCalculator.calculate_dsr(sharpe_estimated=1.8, num_trials=1, track_record_length=100)
        dsr_n50 = DSRCalculator.calculate_dsr(sharpe_estimated=1.8, num_trials=50, track_record_length=100)

        # Dimostrazione analitica: il DSR con 50 trial DEVE essere inferiore a quello con 1 solo trial
        self.assertGreater(dsr_n1, dsr_n50)
        self.assertGreaterEqual(dsr_n50, 0.0)
        self.assertLessEqual(dsr_n50, 1.0)


if __name__ == "__main__":
    unittest.main()
