"""
Eventi e Strutture Dati per il Backtester Event-Driven.
Tutti i valori monetari, quantita' e prezzi sono gestiti in Decimal.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Dict, Any


class OrderType(str, Enum):
    MARKET = "MARKET"
    STOP_LOSS = "STOP_LOSS"
    TAKE_PROFIT = "TAKE_PROFIT"


class Direction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class PositionType(str, Enum):
    FLAT = "FLAT"
    LONG = "LONG"
    SHORT = "SHORT"


class LookAheadViolationError(RuntimeError):
    """Sollevata quando si tenta un'esecuzione anticipata o l'accesso a dati futuri."""
    pass


@dataclass(frozen=True)
class SignalEvent:
    timestamp: datetime
    symbol: str
    direction: Direction
    quantity: Decimal
    stop_loss: Optional[Decimal] = None
    take_profit: Optional[Decimal] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.quantity, Decimal) or self.quantity <= Decimal("0"):
            raise ValueError(f"Quantity deve essere Decimal > 0. Ricevuto: {self.quantity}")


@dataclass(frozen=True)
class OrderEvent:
    timestamp: datetime
    symbol: str
    order_type: OrderType
    direction: Direction
    quantity: Decimal
    target_bar_open_time: datetime
    stop_loss: Optional[Decimal] = None
    take_profit: Optional[Decimal] = None


@dataclass(frozen=True)
class FillEvent:
    timestamp: datetime
    symbol: str
    direction: Direction
    quantity: Decimal
    fill_price: Decimal
    commission: Decimal
    slippage: Decimal
    spread_cost: Decimal
    is_gap_slippage: bool = False
    pnl_realized: Decimal = Decimal("0.00")
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Position:
    symbol: str
    position_type: PositionType
    quantity: Decimal
    entry_price: Decimal
    entry_time: datetime
    entry_commission: Decimal = Decimal("0.00")
    entry_spread: Decimal = Decimal("0.00")
    entry_slippage: Decimal = Decimal("0.00")
    stop_loss: Optional[Decimal] = None
    take_profit: Optional[Decimal] = None

    def unrealized_pnl(self, current_price: Decimal) -> Decimal:
        if self.position_type == PositionType.LONG:
            return (current_price - self.entry_price) * self.quantity
        elif self.position_type == PositionType.SHORT:
            return (self.entry_price - current_price) * self.quantity
        return Decimal("0.00")


@dataclass(frozen=True)
class TradeRecord:
    symbol: str
    direction: Direction
    quantity: Decimal
    entry_time: datetime
    entry_price: Decimal
    exit_time: datetime
    exit_price: Decimal
    gross_pnl: Decimal
    net_pnl: Decimal
    total_commission: Decimal
    total_spread_cost: Decimal
    total_slippage: Decimal
    exit_reason: str
    is_gap_slippage: bool = False
