"""[CLAUDE · VERIFICA] "Kelly a barriera finita".
Derivazione (approssimazione di diffusione): con rischio fisso f per trade (frazione del capitale iniziale),
l'equity dopo n trade ha incrementi di media f*m e varianza f^2*s^2 (m = E[R], s^2 = Var[R]).
Per un moto browniano con deriva mu = f*m e varianza sigma^2 = f^2*s^2, la probabilità di toccare MAI -D è
  psi = exp(-2 mu D / sigma^2) = exp(-2 m D / (f s^2)).
Imporre psi <= alpha  =>  f <= 2 m D / (s^2 ln(1/alpha)).
Con anche un target +T (ci si ferma al target): psi_T = (1 - e^{-theta T}) / (e^{theta D} - e^{-theta T}),
theta = 2 mu / sigma^2.
Verifica numerica: rovina ESATTA del cammino discreto (reticolo, nessun campionamento)."""
import math, sys; sys.path.insert(0, sys.argv[1])
from collections import defaultdict
from fractions import Fraction as F
from c1_esatto_challenge import reticolo

def ms(p, rr, cost):
    w, l = rr - cost, -(1 + cost); m = p * w + (1 - p) * l
    return m, p * w * w + (1 - p) * l * l - m * m

def f_star(m, s2, D=0.10, alpha=0.05): return 2 * m * D / (s2 * math.log(1 / alpha))

def rovina_esatta(p, f, rr, cost, D=0.10, top=1.0, tol=1e-12, max_iter=200000, ferma_al_target=None):
    """Probabilità di toccare -D prima di 'top' (top grande ~ orizzonte infinito) o prima del target."""
    unit, w, l = reticolo(f, rr, cost)
    lo = math.floor(-F(str(D)) / unit); hi = math.ceil(F(str(ferma_al_target if ferma_al_target else top)) / unit)
    dist = {0: 1.0}; rov = 0.0; it = 0
    while dist and it < max_iter:
        it += 1; nd = defaultdict(float)
        for e, pr in dist.items():
            for d, q in ((w, p), (l, 1 - p)):
                e2 = e + d
                if e2 <= lo: rov += pr * q
                elif e2 >= hi: pass
                else: nd[e2] += pr * q
        dist = {k: v for k, v in nd.items() if v > 1e-18}
        if sum(dist.values()) < tol: break
    return rov, it

p, rr = 0.40, 2.0
for nome, cost in (("lordo (senza costi)", 0.0), ("netto (costo 0,05R, come nel motore)", 0.05)):
    m, s2 = ms(p, rr, cost); f = f_star(m, s2)
    print(f"{nome}: E[R]={m:.3f}, Var[R]={s2:.3f} -> f* = {100*f:.3f}% del capitale (alpha=5%, D=10%)")
m_g, s2_g = ms(p, rr, 0.0); m_n, s2_n = ms(p, rr, 0.05)
print()
print("Rischio di rovina (-10%) al variare di f: diffusione vs cammino discreto ESATTO (esiti netti, costo 0,05R)")
print(f"{'f':>7s} {'diff. infinita':>15s} {'esatto infinito':>16s} {'diff. con T=+10%':>17s} {'esatto con T=+10%':>18s}")
for f in (0.00464, 0.00618, 0.0075, 0.01):
    theta = 2 * (f * m_n) / (f * f * s2_n)
    inf_bm = math.exp(-theta * 0.10)
    tgt_bm = (1 - math.exp(-theta * 0.10)) / (math.exp(theta * 0.10) - math.exp(-theta * 0.10))
    ex_inf, _ = rovina_esatta(p, f, rr, 0.05, top=1.0)
    ex_tgt, _ = rovina_esatta(p, f, rr, 0.05, ferma_al_target=0.10)
    print(f"{100*f:6.3f}% {inf_bm:15.4f} {ex_inf:16.4f} {tgt_bm:17.4f} {ex_tgt:18.4f}")
print()
print("Stesso calcolo con esiti LORDI (costo 0), cioè le ipotesi con cui risulta 0,618%:")
for f in (0.00618,):
    theta = 2 * m_g / (f * s2_g)
    print(f"  f=0.618%: diffusione infinita {math.exp(-theta*0.10):.4f}, con target {(1-math.exp(-theta*0.10))/(math.exp(theta*0.10)-math.exp(-theta*0.10)):.4f}; "
          f"esatto infinito {rovina_esatta(p, f, rr, 0.0, top=1.0)[0]:.4f}, esatto con target {rovina_esatta(p, f, rr, 0.0, ferma_al_target=0.10)[0]:.4f}")
print()
print("Sensibilità all'incertezza su E[R]: win rate stimato da N trade (±1 errore standard)")
for N in (100, 300, 1000):
    se = math.sqrt(0.4 * 0.6 / N)
    for pp in (0.40 - se, 0.40, 0.40 + se):
        mm, ss = ms(pp, rr, 0.05)
        print(f"  N={N:4d} WR={pp:.3f}: E[R]={mm:+.3f}  f*={'%.3f%%' % (100*f_star(mm, ss)) if mm > 0 else 'nessuna size sicura (E[R]<=0)'}")
