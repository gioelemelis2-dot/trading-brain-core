"""
Motore di Backtest Strictly Event-Driven.
Architettura Rigorosa:
1. Sequenza Esecutiva Corretta a 3 Fasi per barra t:
   (1) Controllo Gap di apertura (bar.open) sulle posizioni attive dal passato (t-1).
   (2) Esecuzione ordini pendenti all'Open(t) con verifica bar.open_time == target_bar_open_time.
   (3) Controllo escursioni intrabarra (bar.low e bar.high) su TUTTE le posizioni attive (incluse le nuove entrate ad Open(t)).
2. Regola Pessimistica di Ambiguità Intrabarra (SL vs TP):
   Se sia Stop Loss sia Take Profit risultano toccati nella stessa barra, viene eseguito lo Stop Loss,
   impostando is_ambiguous_intrabar = True e condizione {H_intrabar_worst_case}.
3. Chiusura forzata a fine dati:
   Se a fine feed restano posizioni aperte, vengono liquidate forzatamente al Close dell'ultima barra (exit_reason="END_OF_DATA").
4. Integrazione con Strumento e Valore per calcolo dei costi di slippage e spread.
"""

from decimal import Decimal
from datetime import datetime
from typing import List, Dict, Optional, Callable, Any

from brain.dati.pipeline.models import Candle
from brain.guardian.g0.strumenti import Strumento
from brain.guardian.g0.valori import Valore, misura
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
        strumento: Strumento,
        valuta_conto: str = "USD",
        initial_capital: Decimal = Decimal("100000.00"),
        spread_points: Decimal = Decimal("0.00010"),
        fixed_commission_per_order: Decimal = Decimal("2.00"),
        slippage_points: Decimal = Decimal("0.00005"),
        cambio_valuta: Optional[Decimal] = None,
    ):
        self.strumento = strumento
        self.valuta_conto = valuta_conto
        self.spread_points = spread_points
        self.fixed_commission = fixed_commission_per_order
        self.slippage_points = slippage_points
        self.cambio_valuta = cambio_valuta

        self.portfolio = Portfolio(
            strumento=strumento,
            valuta_conto=valuta_conto,
            initial_cash=initial_capital,
            cambio_valuta=cambio_valuta,
        )

        self.pending_orders: List[OrderEvent] = []
        self.current_bar_index: int = -1
        self.last_bar: Optional[Candle] = None
        self.is_running: bool = False

    def run(
        self,
        data_feed: List[Candle],
        strategy_func: Callable[[Candle, Portfolio, "EventDrivenBacktester"], Optional[SignalEvent]],
    ) -> Portfolio:
        """
        Ciclo principale di esecuzione bar-by-bar strettamente sequenziale.
        """
        if not data_feed:
            raise ValueError("Data feed vuoto.")

        self.is_running = True
        self.pending_orders.clear()

        for idx, bar in enumerate(data_feed):
            self.current_bar_index = idx
            self.last_bar = bar

            # =========================================================================
            # FASE 1: APERTURA BARRA t
            # =========================================================================
            # 1.A: Controlla GAP di apertura sulle posizioni preesistenti da t-1
            self._process_open_gaps_on_existing_positions(bar)

            # 1.B: Esegui gli ordini pendenti all'Open(t)
            self._execute_pending_orders_at_open(bar)

            # =========================================================================
            # FASE 2: INTRABARRA t (dopo le aperture a mercato)
            # =========================================================================
            # 2.A: Controlla Stop Loss e Take Profit intrabarra su TUTTE le posizioni aperte
            # (comprese quelle appena aperte all'Open(t))
            self._process_intrabar_stops_and_takes(bar)

            # 2.B: Aggiorna Equity al Close e Worst-Case Intrabar
            costo_uscita_stimato = Decimal("0.00")
            if self.portfolio.positions.get(self.strumento.simbolo):
                pos = self.portfolio.positions[self.strumento.simbolo]
                costo_uscita_stimato = (
                    self.fixed_commission
                    + self.portfolio.calcola_costo_punti(self.spread_points / Decimal("2"), pos.quantity, bar.close)
                    + self.portfolio.calcola_costo_punti(self.slippage_points, pos.quantity, bar.close)
                )

            self.portfolio.update_equity_bar(
                current_time=bar.close_time,
                bar_close=bar.close,
                bar_high=bar.high,
                bar_low=bar.low,
                costo_uscita_latente=costo_uscita_stimato,
            )

            # =========================================================================
            # FASE 3: CHIUSURA BARRA t
            # =========================================================================
            # La strategia elabora il segnale basandosi sulla barra chiusa
            signal = strategy_func(bar, self.portfolio, self)

            if signal is not None:
                # Anti-Lookahead Guard: Il segnale deve avere esattamente timestamp = bar.close_time
                if signal.timestamp != bar.close_time:
                    raise LookAheadViolationError(
                        f"Violazione Anti-Lookahead: Segnale emesso con timestamp {signal.timestamp.isoformat()} "
                        f"invece del Close della barra corrente {bar.close_time.isoformat()}."
                    )

                # Calcola il target open time della barra t+1
                # In assenza della barra successiva, target e' close_time della barra corrente (inizio barra successiva)
                order = OrderEvent(
                    timestamp=bar.close_time,
                    symbol=signal.symbol,
                    order_type=OrderType.MARKET,
                    direction=signal.direction,
                    quantity=signal.quantity,
                    target_bar_open_time=bar.close_time,  # Deve coincidere con open_time di t+1
                    stop_loss=signal.stop_loss,
                    take_profit=signal.take_profit,
                    reduce_only=signal.reduce_only,
                )
                self.pending_orders.append(order)

        # =============================================================================
        # FASE 4: CHIUSURA FORZATA A FINE DATI (Nessuna posizione lasciata fluttuante)
        # =============================================================================
        self._force_close_at_end_of_data(data_feed[-1])

        if self.pending_orders:
            self.portfolio.discarded_end_of_data_orders.extend(self.pending_orders)
            self.pending_orders.clear()

        self.is_running = False
        return self.portfolio

    def _process_open_gaps_on_existing_positions(self, bar: Candle):
        """
        1.A: Rileva se il salto di apertura ad Open(t) ha superato lo Stop o il Take
        di una posizione già aperta nelle barre precedenti.
        """
        pos = self.portfolio.positions.get(bar.symbol)
        if pos is None:
            return

        exit_price: Optional[Decimal] = None
        exit_reason: str = ""
        is_gap: bool = False

        if pos.position_type == PositionType.LONG:
            if pos.stop_loss is not None and bar.open <= pos.stop_loss:
                # GAP DOWN oltre lo stop: esecuzione forzata ad Open(t)
                exit_price = bar.open
                exit_reason = "GAP_STOP_LOSS"
                is_gap = True
            elif pos.take_profit is not None and bar.open >= pos.take_profit:
                exit_price = bar.open
                exit_reason = "GAP_TAKE_PROFIT"
                is_gap = True
        elif pos.position_type == PositionType.SHORT:
            if pos.stop_loss is not None and bar.open >= pos.stop_loss:
                # GAP UP oltre lo stop: esecuzione forzata ad Open(t)
                exit_price = bar.open
                exit_reason = "GAP_STOP_LOSS"
                is_gap = True
            elif pos.take_profit is not None and bar.open <= pos.take_profit:
                exit_price = bar.open
                exit_reason = "GAP_TAKE_PROFIT"
                is_gap = True

        if exit_price is not None:
            spread_cost = self.portfolio.calcola_costo_punti(
                self.spread_points / Decimal("2"), pos.quantity, exit_price
            )
            slippage_cost = self.portfolio.calcola_costo_punti(
                self.slippage_points, pos.quantity, exit_price
            )
            fill = FillEvent(
                timestamp=bar.open_time,
                symbol=pos.symbol,
                direction=Direction.SELL if pos.position_type == PositionType.LONG else Direction.BUY,
                quantity=pos.quantity,
                fill_price=exit_price,
                commission=self.fixed_commission,
                spread_cost=spread_cost,
                slippage=slippage_cost,
                is_gap_slippage=is_gap,
                metadata={"exit_reason": exit_reason},
            )
            self.portfolio.on_fill(fill)

    def _execute_pending_orders_at_open(self, bar: Candle):
        """
        1.B: Esegue gli ordini generati al Close(t-1) rigorosamente all'Open(t).
        Verifica anche la coerenza temporale target_bar_open_time == bar.open_time.
        """
        if not self.pending_orders:
            return

        orders_to_execute = list(self.pending_orders)
        self.pending_orders.clear()

        for order in orders_to_execute:
            # Controllo anti-lookahead su gap di sessione / weekend (CRITICO-2)
            if bar.open_time < order.target_bar_open_time:
                raise LookAheadViolationError(
                    f"Violazione Esecutiva: L'ordine pendente richiedeva esecuzione a {order.target_bar_open_time.isoformat()} "
                    f"ma la barra corrente apre prima ({bar.open_time.isoformat()})."
                )

            is_session_gap = bar.open_time > order.target_bar_open_time
            session_gap_delay = (
                int((bar.open_time - order.target_bar_open_time).total_seconds())
                if is_session_gap
                else 0
            )

            # Regola reduce_only: se l'ordine ha reduce_only=True e la posizione è già stata chiusa
            # (es. in Fase 1.A per GAP_STOP_LOSS o GAP_TAKE_PROFIT) oppure non è nella direzione da ridurre,
            # scartalo invece di aprire una posizione inversa scoperta.
            if order.reduce_only:
                pos = self.portfolio.positions.get(order.symbol)
                if pos is None:
                    continue
                if (pos.position_type == PositionType.LONG and order.direction != Direction.SELL) or \
                   (pos.position_type == PositionType.SHORT and order.direction != Direction.BUY):
                    continue
            else:
                # ALTO-7: Validazione coerenza SL/TP rispetto al vero bar.open dopo eventuale gap
                if order.direction == Direction.BUY:
                    if (order.stop_loss is not None and order.stop_loss >= bar.open) or (
                        order.take_profit is not None and order.take_profit <= bar.open
                    ):
                        self.portfolio.rejected_orders.append(
                            (order, "BUY invalidato post-gap: stop_loss >= bar.open o take_profit <= bar.open")
                        )
                        continue
                elif order.direction == Direction.SELL:
                    if (order.stop_loss is not None and order.stop_loss <= bar.open) or (
                        order.take_profit is not None and order.take_profit >= bar.open
                    ):
                        self.portfolio.rejected_orders.append(
                            (order, "SELL invalidato post-gap: stop_loss <= bar.open o take_profit >= bar.open")
                        )
                        continue

            spread_cost = self.portfolio.calcola_costo_punti(
                self.spread_points / Decimal("2"), order.quantity, bar.open
            )
            slippage_cost = self.portfolio.calcola_costo_punti(
                self.slippage_points, order.quantity, bar.open
            )

            fill_meta = {
                "stop_loss": order.stop_loss,
                "take_profit": order.take_profit,
                "reduce_only": order.reduce_only,
                "is_session_gap": is_session_gap,
            }
            if is_session_gap:
                fill_meta["session_gap_delay_seconds"] = session_gap_delay

            fill = FillEvent(
                timestamp=bar.open_time,
                symbol=order.symbol,
                direction=order.direction,
                quantity=order.quantity,
                fill_price=bar.open,
                commission=self.fixed_commission,
                spread_cost=spread_cost,
                slippage=slippage_cost,
                metadata=fill_meta,
            )
            self.portfolio.on_fill(fill)

    def _process_intrabar_stops_and_takes(self, bar: Candle):
        """
        2.A: Verifica escursioni intrabarra (High e Low) su TUTTE le posizioni aperte.
        Applica la regola di peggior scenario in caso di ambiguità (SL toccato contemporaneamente a TP).
        """
        pos = self.portfolio.positions.get(bar.symbol)
        if pos is None:
            return

        exit_price: Optional[Decimal] = None
        exit_reason: str = ""
        is_ambiguous: bool = False

        if pos.position_type == PositionType.LONG:
            sl_hit = (pos.stop_loss is not None) and (bar.low <= pos.stop_loss)
            tp_hit = (pos.take_profit is not None) and (bar.high >= pos.take_profit)

            if sl_hit and tp_hit:
                # AMBIGUITÀ INTRABARRA: Regola pessimistica obbligatoria -> STOP LOSS
                exit_price = pos.stop_loss
                exit_reason = "AMBIGUOUS_INTRABAR_STOP_LOSS"
                is_ambiguous = True
            elif sl_hit:
                exit_price = pos.stop_loss
                exit_reason = "INTRABAR_STOP_LOSS"
            elif tp_hit:
                exit_price = pos.take_profit
                exit_reason = "INTRABAR_TAKE_PROFIT"

        elif pos.position_type == PositionType.SHORT:
            sl_hit = (pos.stop_loss is not None) and (bar.high >= pos.stop_loss)
            tp_hit = (pos.take_profit is not None) and (bar.low <= pos.take_profit)

            if sl_hit and tp_hit:
                # AMBIGUITÀ INTRABARRA: Regola pessimistica obbligatoria -> STOP LOSS
                exit_price = pos.stop_loss
                exit_reason = "AMBIGUOUS_INTRABAR_STOP_LOSS"
                is_ambiguous = True
            elif sl_hit:
                exit_price = pos.stop_loss
                exit_reason = "INTRABAR_STOP_LOSS"
            elif tp_hit:
                exit_price = pos.take_profit
                exit_reason = "INTRABAR_TAKE_PROFIT"

        if exit_price is not None:
            spread_cost = self.portfolio.calcola_costo_punti(
                self.spread_points / Decimal("2"), pos.quantity, exit_price
            )
            slippage_cost = self.portfolio.calcola_costo_punti(
                self.slippage_points, pos.quantity, exit_price
            )
            fill = FillEvent(
                timestamp=bar.close_time,
                symbol=pos.symbol,
                direction=Direction.SELL if pos.position_type == PositionType.LONG else Direction.BUY,
                quantity=pos.quantity,
                fill_price=exit_price,
                commission=self.fixed_commission,
                spread_cost=spread_cost,
                slippage=slippage_cost,
                is_gap_slippage=False,
                metadata={
                    "exit_reason": exit_reason,
                    "is_ambiguous_intrabar": is_ambiguous,
                    "fill_timing": "intrabar_close_assumed",
                    "condizioni": ["{H_intrabar_worst_case}"] if is_ambiguous else [],
                },
            )
            self.portfolio.on_fill(fill)

    def _force_close_at_end_of_data(self, last_bar: Candle):
        """
        4: Chiusura forzata al Close dell'ultima barra per qualsiasi posizione ancora aperta.
        """
        pos = self.portfolio.positions.get(last_bar.symbol)
        if pos is None:
            return

        spread_cost = self.portfolio.calcola_costo_punti(
            self.spread_points / Decimal("2"), pos.quantity, last_bar.close
        )
        slippage_cost = self.portfolio.calcola_costo_punti(
            self.slippage_points, pos.quantity, last_bar.close
        )

        fill = FillEvent(
            timestamp=last_bar.close_time,
            symbol=pos.symbol,
            direction=Direction.SELL if pos.position_type == PositionType.LONG else Direction.BUY,
            quantity=pos.quantity,
            fill_price=last_bar.close,
            commission=self.fixed_commission,
            spread_cost=spread_cost,
            slippage=slippage_cost,
            is_gap_slippage=False,
            metadata={"exit_reason": "END_OF_DATA"},
        )
        self.portfolio.on_fill(fill)
