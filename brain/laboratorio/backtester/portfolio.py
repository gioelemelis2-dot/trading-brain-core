"""
Gestione Portafoglio ed Equity per il Backtester Event-Driven.
Accounting Istituzionale Rigoroso:
- Prezzi di fill registrati al prezzo di mercato base (Open o Stop).
- Costi di transazione espliciti: Commissioni, Metà Spread per leg, Slippage.
- Gross PnL = Delta prezzo * Quantità.
- Net PnL = Gross PnL - Costi Totali Round-Trip.
Tutti i valori monetari sono rigorosamente in Decimal.
"""

from decimal import Decimal
from datetime import datetime
from typing import Dict, List, Tuple, Optional

from .events import Position, PositionType, Direction, FillEvent, TradeRecord


class Portfolio:
    def __init__(self, initial_cash: Decimal = Decimal("100000.00")):
        self.initial_cash: Decimal = initial_cash
        self.cash: Decimal = initial_cash
        self.equity: Decimal = initial_cash
        self.positions: Dict[str, Position] = {}
        self.trade_history: List[TradeRecord] = []
        self.equity_curve: List[Tuple[datetime, Decimal]] = []

    def update_equity(self, current_time: datetime, current_prices: Dict[str, Decimal]):
        unrealized = Decimal("0.00")
        for sym, pos in self.positions.items():
            if sym in current_prices:
                unrealized += pos.unrealized_pnl(current_prices[sym])
        self.equity = self.cash + unrealized
        self.equity_curve.append((current_time, self.equity))

    def on_fill(self, fill: FillEvent) -> Optional[TradeRecord]:
        """
        Aggiorna la cassa e le posizioni a seguito di un FillEvent.
        Deduce i costi di transazione della leg (commissione + spread leg + slippage).
        Se chiude una posizione esistente, accredita il gross PnL e genera il TradeRecord.
        """
        # Costi della leg corrente dedotti istantaneamente dalla cassa
        leg_friction = fill.commission + fill.spread_cost + fill.slippage
        self.cash -= leg_friction

        existing = self.positions.get(fill.symbol)
        trade_record: Optional[TradeRecord] = None

        if existing is None:
            # Apertura nuova posizione: memorizza i costi di ingresso nella posizione
            pos_type = PositionType.LONG if fill.direction == Direction.BUY else PositionType.SHORT
            self.positions[fill.symbol] = Position(
                symbol=fill.symbol,
                position_type=pos_type,
                quantity=fill.quantity,
                entry_price=fill.fill_price,
                entry_time=fill.timestamp,
                entry_commission=fill.commission,
                entry_spread=fill.spread_cost,
                entry_slippage=fill.slippage,
                stop_loss=fill.metadata.get("stop_loss"),
                take_profit=fill.metadata.get("take_profit"),
            )
        else:
            # Chiusura posizione esistente (segnale opposto o stop/take)
            if (existing.position_type == PositionType.LONG and fill.direction == Direction.SELL) or \
               (existing.position_type == PositionType.SHORT and fill.direction == Direction.BUY):
                
                if existing.position_type == PositionType.LONG:
                    gross_pnl = (fill.fill_price - existing.entry_price) * existing.quantity
                else:
                    gross_pnl = (existing.entry_price - fill.fill_price) * existing.quantity

                total_comm = existing.entry_commission + fill.commission
                total_spread = existing.entry_spread + fill.spread_cost
                total_slip = existing.entry_slippage + fill.slippage

                net_pnl = gross_pnl - total_comm - total_spread - total_slip
                
                # Il gross_pnl viene accreditato/addebitato alla cassa
                self.cash += gross_pnl

                trade_record = TradeRecord(
                    symbol=fill.symbol,
                    direction=Direction.BUY if existing.position_type == PositionType.LONG else Direction.SELL,
                    quantity=existing.quantity,
                    entry_time=existing.entry_time,
                    entry_price=existing.entry_price,
                    exit_time=fill.timestamp,
                    exit_price=fill.fill_price,
                    gross_pnl=gross_pnl,
                    net_pnl=net_pnl,
                    total_commission=total_comm,
                    total_spread_cost=total_spread,
                    total_slippage=total_slip,
                    exit_reason=fill.metadata.get("exit_reason", "SIGNAL"),
                    is_gap_slippage=fill.is_gap_slippage,
                )
                self.trade_history.append(trade_record)
                del self.positions[fill.symbol]
            else:
                raise NotImplementedError("Piramidazione posizioni non abilitata.")

        return trade_record
