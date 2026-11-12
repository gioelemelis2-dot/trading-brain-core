"""[CLAUDE · VERIFICA V3.1] Tabella di Kelly (P-09) della risposta V3.1, §4.
f* = 2 m D / (s2 ln(1/alpha)), D = 0,10, alpha = 0,05 (approssimazione di diffusione, orizzonte infinito)."""
import math
L = math.log(20); D = 0.10
fs = lambda m, s2: 2*m*D/(s2*L)
# Slippage Lomax alpha 1,8, scala 0,05, tetto 3R: momenti per integrazione numerica
A, SC, CAP = 1.8, 0.05, 3.0
sf = lambda s: (1 + s/SC) ** (-A)
n = 200000; h = CAP / n
ES = sum(sf((i+0.5)*h) for i in range(n)) * h                    # E[min(S,CAP)] = ∫ P(S>s) ds
ES2 = sum(2*((i+0.5)*h)*sf((i+0.5)*h) for i in range(n)) * h     # E[min(S,CAP)^2] = ∫ 2s P(S>s) ds
VS = ES2 - ES**2
p = 0.40; w = 1.95; lmean = -1.05 - ES
m = p*w + (1-p)*lmean
EX2 = p*w*w + (1-p)*((1.05+ES)**2 + VS)
s2 = EX2 - m*m
print(f"Slippage con tetto: E[S] = {ES:.4f}R, Var[S] = {VS:.4f}  ->  E[R] = {m:.4f}, Var[R] = {s2:.4f}, f* = {100*fs(m, s2):.4f}%   (V3.1: 0,114 / 2,19 / 0,3472%)")
for mm in (0.15, 0.10, 0.05):
    print(f"E[R] = {mm:.3f}, Var 2,16: f* = {100*fs(mm, 2.16):.4f}%")
N = 300; se_wr = math.sqrt(0.4*0.6/N); se_e = 3*se_wr   # E[R] = 3*WR - 1,05 con R:R 2 e costo 0,05
for nome, k in (("±1 errore standard (≈ 68%)", 1.0), ("IC 95% (±1,96 errori standard)", 1.959964)):
    lo, hi = 0.15 - k*se_e, 0.15 + k*se_e
    flo = f"{100*fs(lo, 2.16):.2f}%" if lo > 0 else "nessuna size (edge non distinguibile da zero)"
    print(f"300 trade, {nome}: E[R] in [{lo:+.3f}, {hi:+.3f}]  ->  f* da {flo} a {100*fs(hi, 2.16):.2f}%")
print("V3.1 dichiara: 'Stima da 300 trade reali (IC 95%)' [+0,068R, +0,232R] -> [0,21%, 0,71%]")
