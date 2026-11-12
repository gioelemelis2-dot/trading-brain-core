"""
Suite di Test per la Pipeline di Ingestione e Validazione Dati Reali.
Verifica Zero-Trust:
1. Rifiuto tassativo di timestamp senza fuso orario UTC esplicito.
2. Rifiuto di float.
3. Rifiuto di prezzi incoerenti (Low > High, Open/Close fuori range).
4. Blocco inversioni temporali e buchi anomali.
5. Sigillo OOS allineato a journal.sigilla (SHA256(nonce + canonico)).
"""

import json
import os
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

    def test_09_template_riconciliazione_da25_valido_per_scheda_g0(self):
        """Verifica che TEMPLATE_RICONCILIAZIONE_DA25.toml sia elaborato da g0.scheda.scheda() senza errori."""
        from brain.guardian.g0 import _toml
        from brain.guardian.g0.scheda import scheda

        template_path = repo_root / "brain" / "dati" / "reali" / "TEMPLATE_RICONCILIAZIONE_DA25.toml"
        self.assertTrue(template_path.exists(), f"Manca il template {template_path}")

        if _toml.MOTORE != "minimale":
            with open(template_path, "rb") as f:
                dati = _toml.load(f)
        else:
            # Con -s su Python 3.9 tomli e' disabilitato; normalizza la chiave quotata "USD/EUR" per test_09
            text = template_path.read_text(encoding="utf-8")
            dati = _toml.loads(text.replace('"USD/EUR"', "USD__EUR"))
            if "cambi" in dati and "USD__EUR" in dati["cambi"]:
                dati["cambi"]["USD/EUR"] = dati["cambi"].pop("USD__EUR")

        righe = scheda(dati)
        testo = "\n".join(righe)
        self.assertIn("G0 · CONSULTIVO · NON RICONCILIATO", testo)
        self.assertIn("LIMITI DETERMINISTICI", testo)
        self.assertIn("TRADE PREVISTO", testo)
        self.assertIn("SCENARIO DI STRESS", testo)
        self.assertIn("nessuna obiezione dalle regole verificate", testo)

    def test_10_split_no_candle_dropped_on_boundary_and_empty_branch_raises(self):
        """RED TEAM CRITICO-3 + MEDIO-9: nessuna candela persa al confine split_time, e ramo vuoto solleva ValueError."""
        candles = []
        for i in range(5):
            t_open = self.t0 + timedelta(hours=i)
            t_close = t_open + timedelta(hours=1)
            candles.append(
                Candle(
                    symbol="EURUSD",
                    timeframe="1H",
                    open_time=t_open,
                    close_time=t_close,
                    open=Decimal("1.08000"),
                    high=Decimal("1.08500"),
                    low=Decimal("1.07900"),
                    close=Decimal("1.08200"),
                    volume=Decimal("1000"),
                )
            )

        # split_time cade esattamente a meta' della candela indice 2 (02:30 UTC)
        split_time = self.t0 + timedelta(hours=2, minutes=30)
        partitioner = DatasetPartitioner(in_sample_ratio=0.7)
        _, _, comm_path = partitioner.split(candles, output_dir=self.temp_dir / "s1", split_time=split_time)

        with open(comm_path, "r", encoding="utf-8") as f:
            comm = json.load(f)
        self.assertEqual(comm["in_sample_count"] + comm["out_of_sample_count"], len(candles))
        self.assertEqual(comm["in_sample_count"], 2)
        self.assertEqual(comm["out_of_sample_count"], 3)

        # MEDIO-9: split_time fuori range che produce ramo vuoto deve sollevare ValueError
        with self.assertRaises(ValueError):
            partitioner.split(candles, output_dir=self.temp_dir / "s2", split_time=self.t0)
        with self.assertRaises(ValueError):
            partitioner.split(candles, output_dir=self.temp_dir / "s3", split_time=self.t0 + timedelta(hours=10))

    def test_11_verify_commitment_malformed_json_returns_false(self):
        """RED TEAM MEDIO-8: commitment.json malformato deve restituire valid=False con reason, non KeyError."""
        candles = [
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=i),
                close_time=self.t0 + timedelta(hours=i + 1),
                open=Decimal("1.08"),
                high=Decimal("1.09"),
                low=Decimal("1.07"),
                close=Decimal("1.085"),
                volume=Decimal("100"),
            )
            for i in range(4)
        ]
        partitioner = DatasetPartitioner(in_sample_ratio=0.5)
        _, oos_path, comm_path = partitioner.split(candles, output_dir=self.temp_dir / "m1")
        nonce_path = self.temp_dir / "m1" / "sealed_nonce.secret"

        # 1. Chiavi mancanti
        comm_path.write_text(json.dumps({"status": "CORRUPTED"}), encoding="utf-8")
        res1 = DatasetPartitioner.verify_commitment(oos_path, comm_path, nonce_path)
        self.assertFalse(res1["valid"])
        self.assertIn("reason", res1)

        # 2. JSON non dizionario (lista)
        comm_path.write_text("[1, 2, 3]", encoding="utf-8")
        res2 = DatasetPartitioner.verify_commitment(oos_path, comm_path, nonce_path)
        self.assertFalse(res2["valid"])
        self.assertIn("reason", res2)

    def test_12_split_custom_nonce_dir_and_env(self):
        """RED TEAM Nota Sicurezza: il nonce puo' essere salvato in directory separata o via TRADING_OOS_NONCE_DIR."""
        candles = [
            Candle(
                symbol="EURUSD",
                timeframe="1H",
                open_time=self.t0 + timedelta(hours=i),
                close_time=self.t0 + timedelta(hours=i + 1),
                open=Decimal("1.08"),
                high=Decimal("1.09"),
                low=Decimal("1.07"),
                close=Decimal("1.085"),
                volume=Decimal("100"),
            )
            for i in range(4)
        ]
        out_dir = self.temp_dir / "out"
        nonce_dir = self.temp_dir / "isolated_vault"
        partitioner = DatasetPartitioner(in_sample_ratio=0.5)
        _, oos_path, comm_path = partitioner.split(candles, output_dir=out_dir, nonce_dir=nonce_dir)

        self.assertFalse((out_dir / "sealed_nonce.secret").exists())
        self.assertTrue((nonce_dir / "sealed_nonce.secret").exists())
        res = DatasetPartitioner.verify_commitment(oos_path, comm_path, nonce_dir / "sealed_nonce.secret")
        self.assertTrue(res["valid"])

        # Verifica variabile d'ambiente TRADING_OOS_NONCE_DIR
        out_dir2 = self.temp_dir / "out2"
        env_nonce_dir = self.temp_dir / "env_vault"
        old_env = os.environ.get("TRADING_OOS_NONCE_DIR")
        os.environ["TRADING_OOS_NONCE_DIR"] = str(env_nonce_dir)
        try:
            partitioner.split(candles, output_dir=out_dir2)
            self.assertFalse((out_dir2 / "sealed_nonce.secret").exists())
            self.assertTrue((env_nonce_dir / "sealed_nonce.secret").exists())
        finally:
            if old_env is None:
                os.environ.pop("TRADING_OOS_NONCE_DIR", None)
            else:
                os.environ["TRADING_OOS_NONCE_DIR"] = old_env

    def test_13_iso_utc_z_fractional_seconds_and_non_finite_decimal(self):
        """RED TEAM CRITICO-4 + BASSO-2: parsing ISO Z / frazioni compatibile 3.9+ e rifiuto Decimal NaN/Infinity."""
        # Test parsing Z e frazioni diverse da 3 o 6 cifre
        for s in (
            "2026-01-01T00:00:00Z",
            "2026-01-01T00:00:00.5Z",
            "2026-01-01T00:00:00.1234Z",
            "2026-01-01T00:00:00.123456789Z",
        ):
            dt = DataIngestionPipeline._parse_iso_utc(s)
            self.assertEqual(dt.utcoffset(), timedelta(0))

        c_dict = {
            "symbol": "EURUSD",
            "timeframe": "1H",
            "open_time": "2026-01-01T00:00:00Z",
            "close_time": "2026-01-01T01:00:00.5Z",
            "open": "1.08",
            "high": "1.09",
            "low": "1.07",
            "close": "1.085",
            "volume": "100",
        }
        c = Candle.from_dict(c_dict)
        self.assertEqual(c.open_time, self.t0)

        # Rifiuto NaN e Infinity su qualsiasi campo numerico
        for bad_val in (Decimal("NaN"), Decimal("Infinity"), Decimal("-Infinity")):
            with self.assertRaises(DataValidationError):
                Candle("EURUSD", "1H", self.t0, self.t0 + timedelta(hours=1), bad_val, Decimal("1.09"), Decimal("1.07"), Decimal("1.08"), Decimal("100"))
            with self.assertRaises(DataValidationError):
                Candle("EURUSD", "1H", self.t0, self.t0 + timedelta(hours=1), Decimal("1.08"), Decimal("1.09"), Decimal("1.07"), Decimal("1.08"), bad_val)


if __name__ == "__main__":
    unittest.main()
