"""
Pipeline di ingestione e validazione per dati storici OHLCV.
Verifica:
1. Formato temporale UTC nativo con offset esplicito (vietato mascheramento di timezone tramite replace).
2. Distinzione rigorosa tra open_time e close_time (anti look-ahead bias).
3. Monotonia stretta della sequenza cronologica.
4. Assenza di sovrapposizioni temporali (overlap) o inversioni.
5. Controllo buchi anomali non dichiarati.
6. Blocco dati futuri rispetto al timestamp di cutoff della ricerca.
"""

import csv
import json
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import List, Optional, Union, Dict, Any
from pathlib import Path

from .models import (
    Candle,
    DataValidationError,
    MonotonicityError,
    LookAheadDataError,
    AnomalyGapError,
    EpistemicType,
)


class DataIngestionPipeline:
    def __init__(
        self,
        symbol: str,
        timeframe: str,
        max_allowed_utc: Optional[datetime] = None,
        max_gap_seconds: Optional[int] = None,
    ):
        self.symbol = symbol
        self.timeframe = timeframe
        if max_allowed_utc is not None:
            if max_allowed_utc.tzinfo is None or max_allowed_utc.utcoffset() != timedelta(0):
                raise DataValidationError("max_allowed_utc deve avere timezone UTC esplicito.")
        self.max_allowed_utc = max_allowed_utc
        self.max_gap_seconds = max_gap_seconds

    def parse_csv_stream(self, file_path: Union[str, Path]) -> List[Candle]:
        candles: List[Candle] = []
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File dati non trovato: {path}")

        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_idx, row in enumerate(reader, start=1):
                try:
                    open_time = self._parse_iso_utc(row["open_time"])
                    if "close_time" in row and row["close_time"]:
                        close_time = self._parse_iso_utc(row["close_time"])
                    else:
                        close_time = open_time + self._timeframe_to_timedelta(self.timeframe)

                    candle = Candle(
                        symbol=self.symbol,
                        timeframe=self.timeframe,
                        open_time=open_time,
                        close_time=close_time,
                        open=Decimal(str(row["open"])),
                        high=Decimal(str(row["high"])),
                        low=Decimal(str(row["low"])),
                        close=Decimal(str(row["close"])),
                        volume=Decimal(str(row["volume"])),
                    )
                    candles.append(candle)
                except Exception as e:
                    raise DataValidationError(f"Errore riga {row_idx} in {path.name}: {e}") from e

        return self.validate_sequence(candles)

    def parse_jsonl(self, file_path: Union[str, Path]) -> List[Candle]:
        candles: List[Candle] = []
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File dati non trovato: {path}")

        with open(path, mode="r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    candles.append(Candle.from_dict(data))
                except Exception as e:
                    raise DataValidationError(f"Errore JSON riga {line_idx} in {path.name}: {e}") from e

        return self.validate_sequence(candles)

    def validate_sequence(self, candles: List[Candle]) -> List[Candle]:
        if not candles:
            return []

        prev_candle: Optional[Candle] = None

        for idx, candle in enumerate(candles):
            # 1. Verifica cutoff dati futuri (Anti-Lookahead)
            if self.max_allowed_utc and candle.close_time > self.max_allowed_utc:
                raise LookAheadDataError(
                    f"Violazione temporale alla candela {idx} ({candle.symbol}): "
                    f"close_time ({candle.close_time.isoformat()}) supera il cutoff autorizzato ({self.max_allowed_utc.isoformat()})."
                )

            # 2. Verifica sequenzialita' e monotonia
            if prev_candle is not None:
                if candle.open_time < prev_candle.close_time:
                    raise MonotonicityError(
                        f"Inversione/Sovrapposizione cronologica alla candela {idx}: "
                        f"open_time attuale ({candle.open_time.isoformat()}) < close_time precedente ({prev_candle.close_time.isoformat()})."
                    )

                if candle.open_time < prev_candle.open_time:
                    raise MonotonicityError(
                        f"Inversione temporale alla candela {idx}: "
                        f"open_time ({candle.open_time.isoformat()}) < open_time precedente ({prev_candle.open_time.isoformat()})."
                    )

                # 3. Controllo buchi temporali non dichiarati
                if self.max_gap_seconds is not None:
                    gap_seconds = (candle.open_time - prev_candle.close_time).total_seconds()
                    if gap_seconds > self.max_gap_seconds:
                        raise AnomalyGapError(
                            f"Buco temporale anomalo alla candela {idx}: "
                            f"distacco di {gap_seconds} secondi (massimo consentito: {self.max_gap_seconds}s) "
                            f"tra {prev_candle.close_time.isoformat()} e {candle.open_time.isoformat()}."
                        )

            prev_candle = candle

        return candles

    @staticmethod
    def _parse_iso_utc(val: str) -> datetime:
        dt = datetime.fromisoformat(val)
        if dt.tzinfo is None:
            raise DataValidationError(
                f"Timestamp privo di fuso orario UTC esplicito: '{val}'. Richiesto suffisso UTC (+00:00 o Z)."
            )
        if dt.utcoffset() != timedelta(0):
            dt = dt.astimezone(timezone.utc)
        return dt

    @staticmethod
    def _timeframe_to_timedelta(tf: str) -> timedelta:
        tf = tf.upper()
        if tf == "1M":
            return timedelta(minutes=1)
        if tf == "5M":
            return timedelta(minutes=5)
        if tf == "15M":
            return timedelta(minutes=15)
        if tf == "1H":
            return timedelta(hours=1)
        if tf == "4H":
            return timedelta(hours=4)
        if tf == "1D":
            return timedelta(days=1)
        raise ValueError(f"Timeframe non supportato per calcolo automatico: {tf}")
