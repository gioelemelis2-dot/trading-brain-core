"""[CLAUDE · VERIFICA] Controlli aritmetici sulle affermazioni STR-002 (nessun dato di mercato disponibile).
Solo conseguenze delle cifre dichiarate da Gemini; tutte [IPOTESI] finché non ci sono dati e backtest."""
import math
# (1) Win rate di pareggio con R:R = b e costo c (in R): p* = (1 + c) / (1 + b)
for b in (0.43, 0.70, 1.2):
    for c in (0.0, 0.04, 0.05):
        print(f"R:R 1:{b:.2f}  costo {c:.2f}R  -> pareggio {100*(1+c)/(1+b):.1f}%")
c = 0.612 * 1.7 - 1
print(f"Il 61,2% dichiarato per R:R 0,70 implica un costo di circa {c:.4f}R per trade")
# (2) 94.518 aperture "S&P 500"
print(f"94.518 aperture / 252 sedute l'anno = {94518/252:.0f} anni: non è un campione storico 2016-2026, è sintetico")
# (3) Numero di trade e potenza su 10 anni (~2.515 sedute), assumendo WR = 70% (= gap fill dichiarato, IPOTESI)
for nome, quota, pareggio in (("filtro 0,70 + gap min (Gemini)", 0.384, 0.612), ("filtro R:R >= 1,2 (Claude)", 0.137, (1.05) / 2.2)):
    n = round(2515 * quota); wr = 0.70
    z = (wr - pareggio) / math.sqrt(wr * (1 - wr) / n)
    print(f"{nome:32s}: ~{n} trade in 10 anni; pareggio {100*pareggio:.1f}%; se WR=70% -> z = {z:.1f}")
