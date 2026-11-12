"""
Suite di Test per la Pipeline di Ingestione e Validazione Dati Reali.
Verifica Zero-Trust:
1. Rifiuto tassativo di timestamp senza fuso orario UTC esplicito.
2. Rifiuto di float.
3. Rifiuto di prezzi incoerenti (Low > High, Open/Close fuori range).
4. Blocco inversioni temporali e buchi anomali.
5. Sigillo OOS allineato a journal.sigilla (SHA256(nonce + canonico)).
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


class TestDataPipelineZeroTrust(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_pipeline_zt_"))
        self.t0 = datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_valid_candle_creation(self):
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
        self.assertEqual(c.open_valore.tipo, "MISURA")

    def test_02_reject_untimezoned_timestamps(self):
        """Verifica che timestamp privi di fuso orario sollevino DataValidationError."""
        naive_dt = datetime(2026, 1, 1, 0, 0)  # naive: senza tzinfo
        with self.assertRaises(DataValidationError):
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=naive_dt,
                close_time=self.t0 + timedelta(hours=1),
                open=Decimal("1.08500"),
                high=Decimal("1.08900"),
                low=Decimal("1.08450"),
                close=Decimal("1.08800"),
                volume=Decimal("100"),
            )

        # Verifica rifiuto in from_dict()
        with self.assertRaises(DataValidationError):
            Candle.from_dict({
                "symbol": "EURUSD",
                "timeframe": "1H",
                "open_time": "2026-01-01T00:00:00",  # privo di 'Z' o offset!
                "close_time": "2026-01-01T01:00:00Z",
                "open": "1.08500",
                "high": "1.08900",
                "low": "1.08450",
                "close": "1.08800",
                "volume": "100",
            })

    def test_03_reject_float_strictly(self):
        with self.assertRaises(TypeError):
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0,
                close_time=self.t0 + timedelta(hours=1),
                open=1.08500,  # float vietato
                high=Decimal("1.08900"),
                low=Decimal("1.08450"),
                close=Decimal("1.08800"),
                volume=Decimal("100"),
            )

    def test_04_reject_corrupted_prices(self):
        with self.assertRaises(DataValidationError):
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0,
                close_time=self.t0 + timedelta(hours=1),
                open=Decimal("1.08500"),
                high=Decimal("1.08000"),  # Low > High
                low=Decimal("1.08900"),
                close=Decimal("1.08500"),
                volume=Decimal("100"),
            )

    def test_05_reject_non_monotonic_sequence(self):
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
            open_time=self.t0 + timedelta(minutes=30),  # Overlap con c1!
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
        cutoff = self.t0 + timedelta(hours=1)
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
            close_time=self.t0 + timedelta(hours=2),  # oltre cutoff
            open=Decimal("1.08800"),
            high=Decimal("1.08950"),
            low=Decimal("1.08750"),
            close=Decimal("1.08900"),
            volume=Decimal("100"),
        )
        with self.assertRaises(LookAheadDataError):
            pipeline.validate_sequence([c1, c2])

    def test_07_reject_anomaly_data_gaps(self):
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
        c2 = Candle(
            symbol="EURUSD",
            timeframe="1H",
            open_time=self.t0 + timedelta(hours=5),  # Gap di 4 ore non autorizzato
            close_time=self.t0 + timedelta(hours=6),
            open=Decimal("1.08800"),
            high=Decimal("1.08950"),
            low=Decimal("1.08750"),
            close=Decimal("1.08900"),
            volume=Decimal("100"),
        )
        with self.assertRaises(AnomalyGapError):
            pipeline.validate_sequence([c1, c2])

    def test_08_partitioning_and_sealed_commitment_aligned_to_journal(self):
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
        nonce_path = self.temp_dir / "sealed_nonce.secret"

        res = DatasetPartitioner.verify_commitment(oos_path, comm_path, nonce_path)
        self.assertTrue(res["valid"])
        self.assertTrue(res["oos_match"])
        self.assertTrue(res["commitment_match"])

        # Manomissione
        with open(oos_path, "r", encoding="utf-8") as f:
            content = f.read()
        tampered_content = content.replace("1.08700", "1.08701")
        with open(oos_path, "w", encoding="utf-8") as f:
            f.write(tampered_content)

        res_tampered = DatasetPartitioner.verify_commitment(oos_path, comm_path, nonce_path)
        self.assertFalse(res_tampered["valid"])
        self.assertFalse(res_tampered["oos_match"])
        self.assertFalse(res_tampered["commitment_match"])


if __name__ == "__main__":
    unittest.main()
