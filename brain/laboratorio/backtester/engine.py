"""
Motore di Backtest Strictly Event-Driven.
Regole Ferree:
1. Un segnale generato al Close(t) puo' essere eseguito SOLO all'Open(t+1).
   Divieto assoluto di same-bar fill sui segnali.
2. Gestione Gap: Se Open(t+1) apre oltre il livello di Stop Loss, l'esecuzione
   avviene all'Open(t+1) (slippage da gap reale), non al prezzo dello stop.
3. Costi espliciti parametrizzati (spread, commissioni, slippage).
"""

from decimal import Decimal
from datetime import datetime
from typing import List, Dict, Optional, Callable, Any

from brain.dati.pipeline.models import Candle
from .events import (
    SignalEvent,
    OrderEvent,
    FillEvent,
    OrderType,
    Direction,
    PositionType,
    LookAheadViolationError,
)
from .portfolio import Portfolio


class EventDrivenBacktester:
    def __init__(
        self,
        symbol: str,
        initial_capital: Decimal = Decimal("100000.00"),
        spread_pips: Decimal = Decimal("0.00010"),  # Es: 1 pip EURUSD
        fixed_commission_per_order: Decimal = Decimal("2.00"),  # $2 per operazione
        slippage_fixed: Decimal = Decimal("0.00000"),  # slippage base oltre ai gap
    ):
        self.symbol = symbol
        self.portfolio = Portfolio(initial_cash=initial_capital)
        self.spread = spread_pips
        self.fixed_commission = fixed_commission_per_order
        self.slippage_fixed = slippage_fixed

        # Coda di ordini pendenti: eseguibili SOLO alla prossima barra (Open t+1)
        self.pending_orders: List[OrderEvent] = []
        self.current_bar_index: int = -1
        self.last_bar: Optional[Candle] = None
        self.is_running: bool = False

    def run(self, data_feed: List[Candle], strategy_func: Callable[[Candle, Portfolio, "EventDrivenBacktester"], Optional[SignalEvent]]) -> Portfolio:
        """
        Ciclo principale a eventi.
        Elabora le candele in modo rigorosamente sequenziale bar-by-bar.
        """
        self.is_running = True
        self.pending_orders.clear()

        for idx, bar in enumerate(data_feed):
            self.current_bar_index = idx
            self.last_bar = bar

            # FASE 1: Inizio barra t. Apertura ad Open(t).
            # 1.A: Verifica Gap e Stop Loss / Take Profit su posizioni aperte
            self._process_intrabar_stops_and_gaps(bar)

            # 1.B: Esecuzione ordini pendenti generati al Close(t-1)
            # Questi ordini possono essere eseguiti ESCLUSIVAMENTE all'Open(t)
            self._execute_pending_orders_at_open(bar)

            # FASE 2: Aggiornamento equity all'Open/Close della barra corrente
            self.portfolio.update_equity(bar.close_time, {self.symbol: bar.close})

            # FASE 3: Chiamata alla strategia al Close(t)
            # La strategia vede la barra t e decide se emettere un segnale
            signal = strategy_func(bar, self.portfolio, self)

            if signal is not None:
                # Validazione rigorosa anti-lookahead:
                # Il segnale deve essere marcato al close_time della barra corrente
                if signal.timestamp != bar.close_time:
                    raise LookAheadViolationError(
                        f"Violazione Anti-Lookahead: Segnale generato con timestamp {signal.timestamp.isoformat()} "
                        f"mentre la barra corrente chiude a {bar.close_time.isoformat()}."
                    )

                # Trasformazione in OrderEvent pendente per Open(t+1)
                order = OrderEvent(
                    timestamp=bar.close_time,
                    symbol=signal.symbol,
                    order_type=OrderType.MARKET,
                    direction=signal.direction,
                    quantity=signal.quantity,
                    target_bar_open_time=bar.close_time,  # Esecuzione obbligata alla barra successiva
                    stop_loss=signal.stop_loss,
                    take_profit=signal.take_profit,
                )
                self.pending_orders.append(order)

        self.is_running = False
        return self.portfolio

    def _process_intrabar_stops_and_gaps(self, bar: Candle):
        """
        Verifica se una posizione attiva ha colpito lo Stop Loss o il Take Profit.
        Se Open(t) apre oltre lo stop (GAP), l'uscita avviene forzatamente ad Open(t).
        """
        pos = self.portfolio.positions.get(bar.symbol)
        if pos is None:
            return

        exit_price: Optional[Decimal] = None
        exit_reason: str = ""
        is_gap: bool = False

        if pos.position_type == PositionType.LONG:
            # Controllo STOP LOSS su posizione LONG
            if pos.stop_loss is not None:
                if bar.open <= pos.stop_loss:
                    # GAP DOWN: L'apertura e' gia' sotto il livello dello stop!
                    # Esecuzione obbligata ad Open(t), assorbendo l'intero gap negativo
                    exit_price = bar.open
                    exit_reason = "GAP_STOP_LOSS"
                    is_gap = True
                elif bar.low <= pos.stop_loss:
                    # Lo stop e' stato toccato durante la barra
                    exit_price = pos.stop_loss
                    exit_reason = "INTRABAR_STOP_LOSS"

            # Controllo TAKE PROFIT su posizione LONG (se stop non attivato)
            if exit_price is None and pos.take_profit is not None:
                if bar.open >= pos.take_profit:
                    # GAP UP favorevole
                    exit_price = bar.open
                    exit_reason = "GAP_TAKE_PROFIT"
                    is_gap = True
                elif bar.high >= pos.take_profit:
                    exit_price = pos.take_profit
                    exit_reason = "INTRABAR_TAKE_PROFIT"

            if exit_price is not None:
                half_spread_cost = (self.spread / Decimal("2")) * pos.quantity
                fill = FillEvent(
                    timestamp=bar.open_time if is_gap else bar.close_time,
                    symbol=pos.symbol,
                    direction=Direction.SELL,
                    quantity=pos.quantity,
                    fill_price=exit_price,
                    commission=self.fixed_commission,
                    slippage=self.slippage_fixed,
                    spread_cost=half_spread_cost,
                    is_gap_slippage=is_gap,
                    metadata={"exit_reason": exit_reason},
                )
                self.portfolio.on_fill(fill)

        elif pos.position_type == PositionType.SHORT:
            # Controllo STOP LOSS su posizione SHORT
            if pos.stop_loss is not None:
                if bar.open >= pos.stop_loss:
                    # GAP UP: L'apertura e' sopra il livello di stop short
                    exit_price = bar.open
                    exit_reason = "GAP_STOP_LOSS"
                    is_gap = True
                elif bar.high >= pos.stop_loss:
                    exit_price = pos.stop_loss
                    exit_reason = "INTRABAR_STOP_LOSS"

            # Controllo TAKE PROFIT su posizione SHORT
            if exit_price is None and pos.take_profit is not None:
                if bar.open <= pos.take_profit:
                    exit_price = bar.open
                    exit_reason = "GAP_TAKE_PROFIT"
                    is_gap = True
                elif bar.low <= pos.take_profit:
                    exit_price = pos.take_profit
                    exit_reason = "INTRABAR_TAKE_PROFIT"

            if exit_price is not None:
                half_spread_cost = (self.spread / Decimal("2")) * pos.quantity
                fill = FillEvent(
                    timestamp=bar.open_time if is_gap else bar.close_time,
                    symbol=pos.symbol,
                    direction=Direction.BUY,
                    quantity=pos.quantity,
                    fill_price=exit_price,
                    commission=self.fixed_commission,
                    slippage=self.slippage_fixed,
                    spread_cost=half_spread_cost,
                    is_gap_slippage=is_gap,
                    metadata={"exit_reason": exit_reason},
                )
                self.portfolio.on_fill(fill)

    def _execute_pending_orders_at_open(self, bar: Candle):
        """
        Esegue gli ordini generati al Close(t-1) rigorosamente all'Open(t).
        """
        if not self.pending_orders:
            return

        orders_to_execute = list(self.pending_orders)
        self.pending_orders.clear()

        for order in orders_to_execute:
            half_spread_cost = (self.spread / Decimal("2")) * order.quantity
            fill = FillEvent(
                timestamp=bar.open_time,
                symbol=order.symbol,
                direction=order.direction,
                quantity=order.quantity,
                fill_price=bar.open,
                commission=self.fixed_commission,
                slippage=self.slippage_fixed,
                spread_cost=half_spread_cost,
                metadata={
                    "stop_loss": order.stop_loss,
                    "take_profit": order.take_profit,
                    "entry_commission": self.fixed_commission,
                    "entry_spread": half_spread_cost,
                    "entry_slippage": self.slippage_fixed,
                },
            )
            self.portfolio.on_fill(fill)
