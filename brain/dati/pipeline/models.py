"""
Modello dati epistemico per candele storiche OHLCV.
Governance Epistemica: Ogni candela e' una MISURA aggregata priva di interpretazione.
Tutti i valori monetari e di prezzo utilizzano esclusivamente Decimal per prevenire errori di floating point.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Any, Dict


class EpistemicType(str, Enum):
    MISURA = "MISURA"
    DERIVATO = "DERIVATO"
    STIMA = "STIMA"
    IPOTESI = "IPOTESI"
    REGOLA = "REGOLA"


class DataValidationError(ValueError):
    """Sollevata quando una candela viola vincoli fisici o temporali."""
    pass


class MonotonicityError(DataValidationError):
    """Sollevata quando la sequenza temporale delle candele non e' strettamente crescente."""
    pass


class LookAheadDataError(DataValidationError):
    """Sollevata quando una candela include dati futuri rispetto al cutoff consentito."""
    pass


class AnomalyGapError(DataValidationError):
    """Sollevata quando si riscontra un buco anomalo non giustificato nel feed."""
    pass


@dataclass(frozen=True)
class Candle:
    symbol: str
    timeframe: str
    open_time: datetime
    close_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    epistemic_type: EpistemicType = field(default=EpistemicType.MISURA)
    condition_h: str = field(default="{H_feed_integro}")

    def __post_init__(self):
        # 1. Validazione Tipi e Timestamp UTC
        if not isinstance(self.open_time, datetime) or not isinstance(self.close_time, datetime):
            raise DataValidationError("open_time e close_time devono essere oggetti datetime.")
        
        if self.open_time.tzinfo is None or self.open_time.tzinfo != timezone.utc:
            raise DataValidationError(f"open_time deve avere timezone UTC esplicito. Trovato: {self.open_time.tzinfo}")
        if self.close_time.tzinfo is None or self.close_time.tzinfo != timezone.utc:
            raise DataValidationError(f"close_time deve avere timezone UTC esplicito. Trovato: {self.close_time.tzinfo}")

        if self.open_time >= self.close_time:
            raise DataValidationError(
                f"open_time ({self.open_time.isoformat()}) deve essere strettamente precedente a close_time ({self.close_time.isoformat()})."
            )

        # 2. Controllo Divieto Float e Conversione Rigorosa Decimal
        for field_name in ["open", "high", "low", "close", "volume"]:
            val = getattr(self, field_name)
            if isinstance(val, float):
                raise TypeError(
                    f"Violazione Governance Epistemica: Il campo '{field_name}' e' di tipo float ({val}). "
                    f"E' tassativo l'uso esclusivo di Decimal per evitare approssimazioni binarie."
                )
            if not isinstance(val, Decimal):
                try:
                    object.__setattr__(self, field_name, Decimal(str(val)))
                except (InvalidOperation, TypeError):
                    raise DataValidationError(f"Impossibile convertire '{field_name}' in Decimal: {val}")

        # 3. Validazione Coerenza Prezzi
        if self.low > self.high:
            raise DataValidationError(f"Incoerenza prezzi: Low ({self.low}) > High ({self.high}).")
        if self.open > self.high or self.open < self.low:
            raise DataValidationError(f"Incoerenza prezzi: Open ({self.open}) fuori dal range [{self.low}, {self.high}].")
        if self.close > self.high or self.close < self.low:
            raise DataValidationError(f"Incoerenza prezzi: Close ({self.close}) fuori dal range [{self.low}, {self.high}].")
        if self.volume < Decimal("0"):
            raise DataValidationError(f"Volume negativo non consentito: {self.volume}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "open_time": self.open_time.isoformat(),
            "close_time": self.close_time.isoformat(),
            "open": str(self.open),
            "high": str(self.high),
            "low": str(self.low),
            "close": str(self.close),
            "volume": str(self.volume),
            "epistemic_type": self.epistemic_type.value,
            "condition_h": self.condition_h,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Candle":
        open_time = datetime.fromisoformat(data["open_time"])
        if open_time.tzinfo is None:
            open_time = open_time.replace(tzinfo=timezone.utc)
        close_time = datetime.fromisoformat(data["close_time"])
        if close_time.tzinfo is None:
            close_time = close_time.replace(tzinfo=timezone.utc)

        return cls(
            symbol=data["symbol"],
            timeframe=data["timeframe"],
            open_time=open_time,
            close_time=close_time,
            open=Decimal(str(data["open"])),
            high=Decimal(str(data["high"])),
            low=Decimal(str(data["low"])),
            close=Decimal(str(data["close"])),
            volume=Decimal(str(data["volume"])),
            epistemic_type=EpistemicType(data.get("epistemic_type", "MISURA")),
            condition_h=data.get("condition_h", "{H_feed_integro}"),
        )
