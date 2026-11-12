"""
Gestione Portafoglio ed Equity per il Backtester Event-Driven.
Accounting Istituzionale Rigoroso integrato con Strumento e Valore:
- Supporto FX, Futures (passo_tick e valore_tick), CFD.
- Conversione valutaria rigorosa (valuta_profitto -> valuta_conto).
- Calcolo friction reale (spread, commissioni, slippage moltiplicati per lotti/contratti).
- Tracciamento Max Drawdown al Close e Intrabar (Worst Intrabar Equity).
Tutti i valori monetari sono rigorosamente in Decimal.
"""

from decimal import Decimal
from datetime import datetime
from typing import Dict, List, Tuple, Optional

from brain.guardian.g0.valori import Valore, misura, combina, NON_STIMABILE, ESATTO
from brain.guardian.g0.strumenti import Strumento
from .events import Position, PositionType, Direction, FillEvent, TradeRecord


class Portfolio:
    def __init__(
        self,
        strumento: Strumento,
        valuta_conto: str = "USD",
        initial_cash: Decimal = Decimal("100000.00"),
        cambio_valuta: Optional[Decimal] = None,  # unita: valuta_profitto / valuta_conto
    ):
        self.strumento: Strumento = strumento
        self.valuta_conto: str = valuta_conto
        self.initial_cash: Decimal = initial_cash
        self.cash: Decimal = initial_cash
        self.equity: Decimal = initial_cash
        self.cambio_valuta: Optional[Decimal] = cambio_valuta

        self.positions: Dict[str, Position] = {}
        self.trade_history: List[TradeRecord] = []
        self.equity_curve_close: List[Tuple[datetime, Decimal]] = []
        self.equity_curve_intrabar: List[Tuple[datetime, Decimal]] = []

        self.peak_equity_close: Decimal = initial_cash
        self.peak_equity_intrabar: Decimal = initial_cash
        self.max_drawdown_close: Decimal = Decimal("0.00")
        self.max_drawdown_intrabar: Decimal = Decimal("0.00")

    def calcola_pnl_monetario(
        self,
        pos_type: PositionType,
        prezzo_ingresso: Decimal,
        prezzo_uscita: Decimal,
        quantita: Decimal,
    ) -> Decimal:
        """
        Calcola il PnL lordo convertito nella valuta del conto usando le specifiche di Strumento.
        """
        s = self.strumento
        if pos_type == PositionType.LONG:
            distanza = prezzo_uscita - prezzo_ingresso
        else:
            distanza = prezzo_ingresso - prezzo_uscita

        if s.classe == "future":
            if s.passo_tick is None or s.valore_tick is None:
                raise ValueError("Per un future servono passo e valore del tick.")
            ticks = distanza / s.passo_tick
            pnl_prof = ticks * s.valore_tick * quantita
        else:
            pnl_prof = distanza * s.dimensione_contratto * quantita

        # Conversione valuta del conto
        if s.valuta_profitto == self.valuta_conto:
            return pnl_prof
        elif s.classe == "fx" and s.valuta_base == self.valuta_conto:
            # Caso EUR/USD su conto EUR: si converte al prezzo di uscita (quotata -> base)
            return pnl_prof / prezzo_uscita
        else:
            if self.cambio_valuta is None:
                raise ValueError(
                    f"Serve il tasso di cambio per convertire {s.valuta_profitto} in {self.valuta_conto}"
                )
            return pnl_prof / self.cambio_valuta

    def calcola_costo_punti(self, punti: Decimal, quantita: Decimal, prezzo_rif: Decimal) -> Decimal:
        """
        Converte uno spread o slippage espresso in punti prezzo nel costo totale in valuta conto.
        """
        s = self.strumento
        if punti == Decimal("0"):
            return Decimal("0.00")

        if s.classe == "future":
            if s.passo_tick is None or s.valore_tick is None:
                raise ValueError("Future privo di tick specifications.")
            ticks = punti / s.passo_tick
            costo_prof = ticks * s.valore_tick * quantita
        else:
            costo_prof = punti * s.dimensione_contratto * quantita

        if s.valuta_profitto == self.valuta_conto:
            return costo_prof
        elif s.classe == "fx" and s.valuta_base == self.valuta_conto:
            return costo_prof / prezzo_rif
        else:
            if self.cambio_valuta is None:
                raise ValueError("Cambio non definito per conversione costi.")
            return costo_prof / self.cambio_valuta

    def update_equity_bar(
        self,
        current_time: datetime,
        bar_close: Decimal,
        bar_high: Decimal,
        bar_low: Decimal,
        costo_uscita_latente: Decimal = Decimal("0.00"),
    ):
        """
        Aggiorna l'equity sia al Close sia nel worst-case Intrabarra.
        """
        pos = self.positions.get(self.strumento.simbolo)
        if pos is None:
            eq_close = self.cash
            eq_worst_intrabar = self.cash
        else:
            # Equity al close
            unrealized_close = self.calcola_pnl_monetario(
                pos.position_type, pos.entry_price, bar_close, pos.quantity
            )
            eq_close = self.cash + unrealized_close

            # Worst-case intrabarra: Low per Long, High per Short, sottraendo i costi stimati di uscita
            if pos.position_type == PositionType.LONG:
                worst_price = bar_low
            else:
                worst_price = bar_high

            unrealized_worst = self.calcola_pnl_monetario(
                pos.position_type, pos.entry_price, worst_price, pos.quantity
            )
            eq_worst_intrabar = self.cash + unrealized_worst - costo_uscita_latente

        self.equity = eq_close
        self.equity_curve_close.append((current_time, eq_close))
        self.equity_curve_intrabar.append((current_time, eq_worst_intrabar))

        # Max Drawdown Close
        if eq_close > self.peak_equity_close:
            self.peak_equity_close = eq_close
        dd_close = self.peak_equity_close - eq_close
        if dd_close > self.max_drawdown_close:
            self.max_drawdown_close = dd_close

        # Max Drawdown Intrabar
        if eq_close > self.peak_equity_intrabar:
            self.peak_equity_intrabar = eq_close
        dd_intrabar = self.peak_equity_intrabar - eq_worst_intrabar
        if dd_intrabar > self.max_drawdown_intrabar:
            self.max_drawdown_intrabar = dd_intrabar

    def on_fill(self, fill: FillEvent) -> Optional[TradeRecord]:
        """
        Aggiorna cassa e posizioni all'arrivo di un FillEvent.
        """
        # Deduce costi della leg corrente
        leg_friction = fill.commission + fill.spread_cost + fill.slippage
        self.cash -= leg_friction

        existing = self.positions.get(fill.symbol)
        trade_record: Optional[TradeRecord] = None

        if existing is None:
            # Apertura nuova posizione
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
            # Chiusura posizione esistente
            if (existing.position_type == PositionType.LONG and fill.direction == Direction.SELL) or \
               (existing.position_type == PositionType.SHORT and fill.direction == Direction.BUY):
                
                gross_pnl = self.calcola_pnl_monetario(
                    existing.position_type, existing.entry_price, fill.fill_price, existing.quantity
                )

                total_comm = existing.entry_commission + fill.commission
                total_spread = existing.entry_spread + fill.spread_cost
                total_slip = existing.entry_slippage + fill.slippage
                net_pnl = gross_pnl - total_comm - total_spread - total_slip

                self.cash += gross_pnl

                condizioni = set(fill.metadata.get("condizioni", []))
                if fill.metadata.get("is_ambiguous_intrabar", False):
                    condizioni.add("{H_intrabar_worst_case}")

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
                    is_ambiguous_intrabar=fill.metadata.get("is_ambiguous_intrabar", False),
                    condizioni=frozenset(condizioni),
                )
                self.trade_history.append(trade_record)
                del self.positions[fill.symbol]
            else:
                raise NotImplementedError("Piramidazione posizioni non supportata.")

        return trade_record
