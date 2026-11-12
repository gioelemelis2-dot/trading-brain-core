"""[CLAUDE · AUDIT ARCHITETTURA V2] Numero di trade necessario per distinguere l'edge di riferimento da zero.
[DERIVATO condizionato alle ipotesi]: WR 0,40, R:R 2, costo fisso 0,05R, trade i.i.d., edge vero = edge di riferimento.
Serve a valutare la durata di paper trading "3-6 mesi" (Fase 9) e i criteri della Fase 6. Libreria standard."""
from statistics import NormalDist as N
import math
p, b, c = 0.40, 2.0, 0.05
m = p * b - (1 - p) - c; s = (b + 1) * math.sqrt(p * (1 - p))
z = lambda q: N().inv_cdf(q)
casi = [("IC 95% con limite inferiore > 0 se si osserva esattamente l'edge", z(.975)),
        ("test unilaterale alfa 5%, potenza 80%", z(.95) + z(.80)),
        ("test bilaterale alfa 5%, potenza 80%", z(.975) + z(.80)),
        ("soglia t > 3 (Harvey, Liu e Zhu 2016), potenza 80%", 3 + z(.80))]
print(f"E[R] = {m:.4f}R, sigma = {s:.4f}R")
for nome, k in casi:
    n = math.ceil((k * s / m) ** 2)
    print(f"{nome}: N = {n} trade; {n / 42:.1f} mesi a 2 trade/giorno; {n / 126:.1f} mesi a 6 trade/giorno (21 giorni/mese)")
