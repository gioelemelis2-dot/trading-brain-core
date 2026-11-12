"""
Suite di Test per la Pipeline di Ingestione e Validazione Dati Reali.
Verifica:
1. Rifiuto sistematico di dati corrotti (prezzi incoerenti, float, timestamp invertiti).
2. Blocco di look-ahead bias e dati futuri.
3. Rilevamento di buchi temporali anomali.
4. Partizionamento deterministico In-Sample / Out-of-Sample.
5. Sigillo crittografico a 256-bit e rilevamento manomissioni su OOS.
"""

import sys
import unittest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta
from decimal import Decimal

# Assicuriamo import relativo al repository
repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.dati.pipeline import (
    Candle,
    EpistemicType,
    DataValidationError,
    MonotonicityError,
    LookAheadDataError,
    AnomalyGapError,
    DataIngestionPipeline,
    DatasetPartitioner,
)


class TestDataPipeline(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_pipeline_"))
        self.t0 = datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_valid_candle_creation(self):
        """Verifica creazione corretta di una candela conforme alla governance epistemica."""
        c = Candle(
            symbol="EURUSD",
            timeframe="1H",
            open_time=self.t0,
            close_time=self.t0 + timedelta(hours=1),
            open=Decimal("1.08500"),
            high=Decimal("1.08900"),
            low=Decimal("1.08450"),
            close=Decimal("1.08800"),
            volume=Decimal("15200.5"),
        )
        self.assertEqual(c.epistemic_type, EpistemicType.MISURA)
        self.assertEqual(c.condition_h, "{H_feed_integro}")
        self.assertIsInstance(c.open, Decimal)
        self.assertIsInstance(c.close, Decimal)

    def test_02_reject_float_strictly(self):
        """Verifica divieto assoluto di tipi float nei campi monetari."""
        with self.assertRaises(TypeError):
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0,
                close_time=self.t0 + timedelta(hours=1),
                open=1.08500,  # FLOAT: vietato
                high=Decimal("1.08900"),
                low=Decimal("1.08450"),
                close=Decimal("1.08800"),
                volume=Decimal("100"),
            )

    def test_03_reject_inverted_bar_timestamps(self):
        """Verifica rifiuto candela con open_time >= close_time."""
        with self.assertRaises(DataValidationError):
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0,
                close_time=self.t0,  # Invalido: durata zero
                open=Decimal("1.08500"),
                high=Decimal("1.08900"),
                low=Decimal("1.08450"),
                close=Decimal("1.08800"),
                volume=Decimal("100"),
            )

        with self.assertRaises(DataValidationError):
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=1),
                close_time=self.t0,  # Invalido: open futuro rispetto a close
                open=Decimal("1.08500"),
                high=Decimal("1.08900"),
                low=Decimal("1.08450"),
                close=Decimal("1.08800"),
                volume=Decimal("100"),
            )

    def test_04_reject_corrupted_prices(self):
        """Verifica rifiuto prezzi incoerenti (Low > High, Open fuori range)."""
        # Low > High
        with self.assertRaises(DataValidationError):
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0,
                close_time=self.t0 + timedelta(hours=1),
                open=Decimal("1.08500"),
                high=Decimal("1.08000"),  # Errato
                low=Decimal("1.08900"),
                close=Decimal("1.08500"),
                volume=Decimal("100"),
            )

        # Close fuori range
        with self.assertRaises(DataValidationError):
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0,
                close_time=self.t0 + timedelta(hours=1),
                open=Decimal("1.08500"),
                high=Decimal("1.08900"),
                low=Decimal("1.08450"),
                close=Decimal("1.09000"),  # > High
                volume=Decimal("100"),
            )

    def test_05_reject_non_monotonic_sequence(self):
        """Verifica blocco sequenza con candele cronologicamente invertite o sovrapposte."""
        c1 = Candle(
            symbol="EURUSD",
            timeframe="1H",
            open_time=self.t0,
            close_time=self.t0 + timedelta(hours=1),
            open=Decimal("1.08500"),
            high=Decimal("1.08900"),
            low=Decimal("1.08450"),
            close=Decimal("1.08800"),
            volume=Decimal("100"),
        )
        # c2 apre prima che c1 sia chiusa (sovrapposizione temporale)
        c2 = Candle(
            symbol="EURUSD",
            timeframe="1H",
            open_time=self.t0 + timedelta(minutes=30),
            close_time=self.t0 + timedelta(minutes=90),
            open=Decimal("1.08800"),
            high=Decimal("1.08950"),
            low=Decimal("1.08750"),
            close=Decimal("1.08900"),
            volume=Decimal("100"),
        )

        pipeline = DataIngestionPipeline(symbol="EURUSD", timeframe="1H")
        with self.assertRaises(MonotonicityError):
            pipeline.validate_sequence([c1, c2])

    def test_06_reject_lookahead_future_candles(self):
        """Verifica blocco candele che superano il cutoff temporale massimo (anti-lookahead)."""
        cutoff = self.t0 + timedelta(hours=2)
        pipeline = DataIngestionPipeline(symbol="EURUSD", timeframe="1H", max_allowed_utc=cutoff)

        c1 = Candle(
            symbol="EURUSD",
            timeframe="1H",
            open_time=self.t0,
            close_time=self.t0 + timedelta(hours=1),
            open=Decimal("1.08500"),
            high=Decimal("1.08900"),
            low=Decimal("1.08450"),
            close=Decimal("1.08800"),
            volume=Decimal("100"),
        )
        c2 = Candle(
            symbol="EURUSD",
            timeframe="1H",
            open_time=self.t0 + timedelta(hours=1),
            close_time=self.t0 + timedelta(hours=2),
            open=Decimal("1.08800"),
            high=Decimal("1.08950"),
            low=Decimal("1.08750"),
            close=Decimal("1.08900"),
            volume=Decimal("100"),
        )
        # c3 chiude alle ore 3 (oltre il cutoff delle ore 2)
        c3 = Candle(
            symbol="EURUSD",
            timeframe="1H",
            open_time=self.t0 + timedelta(hours=2),
            close_time=self.t0 + timedelta(hours=3),
            open=Decimal("1.08900"),
            high=Decimal("1.09100"),
            low=Decimal("1.08850"),
            close=Decimal("1.09050"),
            volume=Decimal("100"),
        )

        with self.assertRaises(LookAheadDataError):
            pipeline.validate_sequence([c1, c2, c3])

    def test_07_reject_anomaly_data_gaps(self):
        """Verifica rilevamento di buchi temporali superiori al massimo consentito."""
        pipeline = DataIngestionPipeline(symbol="EURUSD", timeframe="1H", max_gap_seconds=3600)

        c1 = Candle(
            symbol="EURUSD",
            timeframe="1H",
            open_time=self.t0,
            close_time=self.t0 + timedelta(hours=1),
            open=Decimal("1.08500"),
            high=Decimal("1.08900"),
            low=Decimal("1.08450"),
            close=Decimal("1.08800"),
            volume=Decimal("100"),
        )
        # c2 apre dopo 5 ore di buco non dichiarato
        c2 = Candle(
            symbol="EURUSD",
            timeframe="1H",
            open_time=self.t0 + timedelta(hours=6),
            close_time=self.t0 + timedelta(hours=7),
            open=Decimal("1.08800"),
            high=Decimal("1.08950"),
            low=Decimal("1.08750"),
            close=Decimal("1.08900"),
            volume=Decimal("100"),
        )

        with self.assertRaises(AnomalyGapError):
            pipeline.validate_sequence([c1, c2])

    def test_08_partitioning_and_sealed_commitment(self):
        """Verifica partizionamento In-Sample / Out-Of-Sample e sigillo crittografico SHA-256."""
        candles = []
        for i in range(10):
            t_open = self.t0 + timedelta(hours=i)
            t_close = t_open + timedelta(hours=1)
            candles.append(
                Candle(
                    symbol="EURUSD",
                    timeframe="1H",
                    open_time=t_open,
                    close_time=t_close,
                    open=Decimal("1.08000") + Decimal(str(i * 0.001)),
                    high=Decimal("1.08500") + Decimal(str(i * 0.001)),
                    low=Decimal("1.07900") + Decimal(str(i * 0.001)),
                    close=Decimal("1.08200") + Decimal(str(i * 0.001)),
                    volume=Decimal("1000"),
                )
            )

        partitioner = DatasetPartitioner(in_sample_ratio=0.7)
        is_path, oos_path, comm_path = partitioner.split(candles, output_dir=self.temp_dir)

        self.assertTrue(is_path.exists())
        self.assertTrue(oos_path.exists())
        self.assertTrue(comm_path.exists())
        nonce_path = self.temp_dir / "sealed_nonce.secret"
        self.assertTrue(nonce_path.exists())

        # Verifica crittografica formale dell'OOS intatto
        res = DatasetPartitioner.verify_commitment(oos_path, comm_path, nonce_path)
        self.assertTrue(res["valid"])
        self.assertTrue(res["oos_match"])
        self.assertTrue(res["nonce_match"])
        self.assertTrue(res["commitment_match"])

        # Simulazione manomissione: modifichiamo 1 singolo carattere nel file OOS
        with open(oos_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        lines[0] = lines[0].replace("1.08700", "1.08701")  # manomissione di 1 decimale
        with open(oos_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        # La verifica DEVE fallire evidenziando la manomissione
        res_tampered = DatasetPartitioner.verify_commitment(oos_path, comm_path, nonce_path)
        self.assertFalse(res_tampered["valid"])
        self.assertFalse(res_tampered["oos_match"])
        self.assertFalse(res_tampered["commitment_match"])


if __name__ == "__main__":
    unittest.main()
