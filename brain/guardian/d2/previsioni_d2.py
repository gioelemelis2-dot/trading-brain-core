"""Previsioni della prova D2 (D-57), calcolate con la funzione del Guardian PRIMA delle operazioni (27/11/2026).
Uso (da brain/guardian): python3 -s -B d2/previsioni_d2.py
La perdita lorda allo stop è quella di g0.strumenti.perdita_allo_stop SENZA commissioni (si confronta con il profitto
lordo del broker, che le esclude). Commissione e margine NON sono calcoli del Guardian: sono ipotesi del profilo demo,
dichiarate qui prima di operare."""
import sys
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from g0.strumenti import Strumento, perdita_allo_stop          # noqa: E402
from g0.valori import Valore                                    # noqa: E402

CONTRATTO = D("100")          # once per lotto: specifica MT5 del 18/11, DA CONFERMARE sulla specifica MT4 della demo
LOTTI = D("0.01")
STRUMENTO = Strumento("XAUUSD", "cfd", "USD", CONTRATTO,
                      "FP Markets, specifica MT5 del 18/11 (da confermare su MT4 demo)", stato_verifica="C")
ORDINI = [("O1", "acquisto", D("2.00")), ("O2", "vendita", D("3.00")), ("O3", "acquisto", D("5.00"))]
PREZZO_RIF = D("3770.00")     # solo per il margine illustrativo; la perdita allo stop non dipende dal livello del prezzo


def v(x, u):
    return Valore(D(x), u, "MISURA", "osservazione", "piano D2")


for nome, lato, dist in ORDINI:
    stop = PREZZO_RIF - dist if lato == "acquisto" else PREZZO_RIF + dist
    p = perdita_allo_stop(STRUMENTO, v(PREZZO_RIF, "USD/oz"), v(stop, "USD/oz"), v(LOTTI, "lotti"), "USD")
    print(f"{nome} {lato} {LOTTI} lotti, stop a {dist} USD: perdita lorda allo stop (Guardian) = {p.valore} {p.unita}"
          f" [{p.tipo}]")
print("Formula congelata per il confronto al prezzo eseguito: |apertura - chiusura| x", CONTRATTO, "x", LOTTI,
      "con il segno dato dal lato (il segno lo applica Claude, non il Guardian)")
