"""Adattatori per tipo di strumento e perdita allo stop (revisione esterna §6.2: niente formula unica).

La perdita allo stop è un DERIVATO condizionato a H_esec: «lo stop viene eseguito al prezzo indicato».
Gap, slippage, lato bid/ask del trigger e mancata esecuzione non sono inclusi: vanno in una riserva separata
(IPOTESI o STIMA), dichiarata a parte.

Conversione nella valuta del conto:
- valuta del profitto uguale alla valuta del conto: nessuna conversione;
- coppia FX con valuta BASE uguale alla valuta del conto (per esempio EUR/USD su conto in EUR): la perdita in
  valuta quotata si converte al cambio dell'uscita, cioè al prezzo dello stop stesso (DERIVATO | H_esec);
- altrimenti serve un cambio MISURATO: unità di valuta del profitto per 1 unità di valuta del conto
  (per esempio EURJPY = 162,00 per un conto in EUR che opera USD/JPY); perdita_conto = perdita / cambio.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from .valori import Valore, combina

H_ESEC = "H_esec: stop eseguito esattamente al prezzo indicato (nessun gap, slippage o mancata esecuzione)"


@dataclass(frozen=True)
class Strumento:
    simbolo: str
    classe: str                        # "fx" | "future" | "cfd"
    valuta_profitto: str               # FX: valuta quotata; future/CFD: valuta del contratto
    dimensione_contratto: Decimal      # FX/CFD: unità per lotto; future: non usato (vedi tick)
    fonte: str                         # specifica del broker o dell'exchange, con data
    stato_verifica: str = "C"          # V solo se la specifica è stata letta sulla fonte del broker
    valuta_base: Optional[str] = None  # solo FX
    passo_tick: Optional[Decimal] = None
    valore_tick: Optional[Decimal] = None

    def __post_init__(self):
        if self.classe not in ("fx", "future", "cfd"):
            raise ValueError(f"classe di strumento non gestita: {self.classe}")
        if self.classe == "fx" and not self.valuta_base:
            raise ValueError("per una coppia FX serve la valuta base")
        if self.classe == "future" and (self.passo_tick is None or self.valore_tick is None):
            raise ValueError("per un future servono passo e valore del tick")


def perdita_allo_stop(s: Strumento, ingresso: Valore, stop: Valore, quantita: Valore, valuta_conto: str,
                      cambio: Optional[Valore] = None, commissioni: Optional[Valore] = None) -> Valore:
    """Perdita nella valuta del conto se lo stop viene eseguito al suo prezzo (DERIVATO | H_esec).
    `quantita`: lotti (FX/CFD) o contratti (future). `commissioni`: costo totale previsto in valuta del conto."""
    spec = Valore(s.dimensione_contratto, "unità", "REGOLA", "norma", s.fonte, stato_verifica=s.stato_verifica)
    distanza = abs(ingresso.valore - stop.valore)
    if s.classe == "future":
        tick = distanza / s.passo_tick
        if tick != tick.to_integral_value():
            raise ValueError(f"la distanza {distanza} non è multipla del tick {s.passo_tick}")
        perdita_prof = tick * s.valore_tick * quantita.valore
    else:
        perdita_prof = distanza * s.dimensione_contratto * quantita.valore
    ins = [ingresso, stop, quantita, spec]

    if s.valuta_profitto == valuta_conto:
        perdita = perdita_prof
    elif s.classe == "fx" and s.valuta_base == valuta_conto:
        perdita = perdita_prof / stop.valore          # cambio all'uscita = prezzo dello stop
    else:
        if cambio is None:
            raise ValueError(f"serve il cambio {valuta_conto}{s.valuta_profitto} (MISURA con ora e fonte)")
        if cambio.unita != f"{s.valuta_profitto}/{valuta_conto}":
            raise ValueError(f"cambio con unità {cambio.unita!r}; attesa {s.valuta_profitto}/{valuta_conto}")
        perdita = perdita_prof / cambio.valore
        ins.append(cambio)
    if commissioni is not None:
        if commissioni.unita != valuta_conto:
            raise ValueError("commissioni in una valuta diversa da quella del conto")
        perdita += commissioni.valore
        ins.append(commissioni)
    return combina(ins, perdita, valuta_conto, "calcolo deterministico",
                   fonte=f"perdita_allo_stop({s.simbolo})", condizioni_aggiunte=[H_ESEC],
                   nota="non include gap, slippage né lato bid/ask del trigger: vedi riserva separata")
