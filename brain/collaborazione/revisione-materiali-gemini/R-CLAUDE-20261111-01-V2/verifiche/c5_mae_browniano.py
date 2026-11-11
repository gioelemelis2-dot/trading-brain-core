"""[CLAUDE · VERIFICA] MAE dei trade VINCENTI per un moto browniano con deriva mu (sigma=1),
stop a -1R e target a +2R, con mu tarato perché P(target prima dello stop) = 0.40.
Formula chiusa (funzione di scala s(x) = 1 - exp(-2 mu x)):
  P_x(a prima di b) = (s(x)-s(b)) / (s(a)-s(b))
  P(MAE <= -m, vincita) = P_0(-m prima di +2) * P_{-m}(+2 prima di -1)
Poi: confronto con una simulazione DISCRETIZZATA (per mostrare il bias della discretizzazione)
e con la distribuzione normale usata nel motore (media -0.205, dev.std 0.1025, tagliata a -0.95)."""
import math, random, statistics

def s(x, mu): return x if abs(mu) < 1e-12 else 1 - math.exp(-2 * mu * x)
def P(x, a, b, mu): return (s(x, mu) - s(b, mu)) / (s(a, mu) - s(b, mu))
def pwin(mu): return P(0, 2, -1, mu)

lo, hi = 0.0, 2.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if pwin(mid) < 0.40 else (lo, mid)
mu = (lo + hi) / 2
_ = (f"Deriva che dà P(vincita)=0.40: mu = {mu:.5f} (sigma=1)   [a deriva nulla P(vincita) = {pwin(0):.4f}]")

def cdf_mae(m, mu):  # P(MAE <= -m | vincita), 0<m<1
    return (1 - P(0, 2, -m, mu)) * P(-m, 2, -1, mu) / pwin(mu)
if __name__ == "__main__":
    print(f"Deriva che dà P(vincita)=0.40: mu = {mu:.5f} (sigma=1)   [a deriva nulla P(vincita) = {pwin(0):.4f}]")
    for m in (0.1, 0.25, 0.5, 0.75, 0.9):
        print(f"   P(MAE <= -{m:.2f}R | vincita) = {cdf_mae(m, mu):.4f}   (deriva nulla: {cdf_mae(m, 0):.4f})")
    # media: E[MAE] = -∫_0^1 P(MAE <= -m) dm
    n = 20000; media = -sum(cdf_mae((i + 0.5) / n, mu) for i in range(n)) / n
    media0 = -sum(cdf_mae((i + 0.5) / n, 0) for i in range(n)) / n
    print(f"   MAE medio dei vincitori = {media:.4f}R (deriva nulla: {media0:.4f}R)")
    print(f"   Gemini dichiara: P(MAE <= -0.5R | vincita) = 0.107, MAE medio = -0.205R")
    
    print("\n[SIMULATO] Sentieri browniani DISCRETIZZATI (passo dt), stessa deriva: il minimo si sottostima")
    rng = random.Random(11)
    for steps_per_unit in (4, 25, 400):
        dt = 1.0 / steps_per_unit; sd = math.sqrt(dt); vincenti = 0; sotto = 0; somma = 0.0; prove = 0
        while vincenti < 8000:
            x = 0.0; mn = 0.0; prove += 1
            while -1 < x < 2:
                x += mu * dt + sd * rng.gauss(0, 1); mn = min(mn, x)
            if x >= 2:
                vincenti += 1; mn = max(mn, -1); somma += mn; sotto += mn <= -0.5
        print(f"   passi per unità di tempo {steps_per_unit:4d}: P(vincita) {vincenti/prove:.3f}, P(MAE<=-0.5|vinc.) {sotto/vincenti:.3f}, MAE medio {somma/vincenti:.3f}")
    
    print("\nDistribuzione usata nel motore V2: Normale(-0.205, 0.1025) tagliata in [-0.95, 0]")
    z = (-0.5 + 0.205) / 0.1025
    print(f"   P(MAE <= -0.5R) implicita = {0.5 * math.erfc(-z / math.sqrt(2)):.5f}  (contro 0.107 dichiarato da Gemini e {cdf_mae(0.5, mu):.3f} browniano esatto)")
