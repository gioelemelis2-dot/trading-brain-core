"""
Eventi e Strutture Dati per il Backtester Event-Driven.
Tutti i valori monetari, quantita' e prezzi sono gestiti in Decimal.
Include flag per ambiguità intrabarra e tracciamento delle condizioni epistemiche.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Dict, Any, FrozenSet


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
    reduce_only: bool = False
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
    reduce_only: bool = False


@dataclass(frozen=True)
class FillEvent:
    timestamp: datetime
    symbol: str
    direction: Direction
    quantity: Decimal
    fill_price: Decimal
    commission: Decimal
    spread_cost: Decimal
    slippage: Decimal
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

    def unrealized_pnl(self, current_price: Decimal, calc_pnl_func) -> Decimal:
        return calc_pnl_func(self.position_type, self.entry_price, current_price, self.quantity)


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
    is_ambiguous_intrabar: bool = False
    fill_timing: str = "standard"
    condizioni: FrozenSet[str] = field(default_factory=frozenset)
