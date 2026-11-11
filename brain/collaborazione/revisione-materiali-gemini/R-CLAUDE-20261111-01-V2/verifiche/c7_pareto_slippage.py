"""[CLAUDE · VERIFICA] Slippage sugli stop con code pesanti. Tutti i parametri sono ILLUSTRATIVI [SIMULATO],
non stimati da dati reali.
(1) Fatti matematici sulla Pareto/Lomax (alpha=1.8).
(2) La stima Monte Carlo di una PROBABILITÀ (superamento, rovina) converge con errore binomiale anche se lo
    slippage ha varianza infinita: lo si misura su 20 semi.
(3) Effetto del troncamento a 3R rispetto a nessun troncamento e a una lognormale con la stessa mediana."""
import math, random, statistics, sys
A, SC = 1.8, 0.05            # Lomax: S = SC * ((1-U)^(-1/A) - 1); mediana = SC*(2^(1/A)-1)
med = SC * (2 ** (1 / A) - 1)
print("(1) Lomax alpha=1.8, scala 0.05R")
print(f"    mediana {med:.4f}R · media {SC/(A-1):.4f}R (finita perché alpha>1) · varianza infinita (alpha<=2)")
for x in (1, 2, 3, 5, 10):
    print(f"    P(S > {x:2d}R) = {(1 + x / SC) ** (-A):.2e}")

def slip(rng, modello):
    u = rng.random()
    if modello == "nessuno": return 0.0
    if modello.startswith("lomax"):
        s = SC * ((1 - u) ** (-1 / A) - 1)
        cap = {"lomax": None, "lomax_cap3": 3.0, "lomax_cap1": 1.0}[modello]
        return min(s, cap) if cap else s
    if modello == "lognormale":   # stessa mediana, sigma scelta = 1.2
        z = statistics.NormalDist().inv_cdf(min(max(u, 1e-12), 1 - 1e-12))
        return med * math.exp(1.2 * z)

def fase(re, rs, mod, risk, tpd, md, target, p=0.40):
    eq = 0.0
    for _ in range(md):
        floor = eq - 0.05
        for _ in range(tpd):
            win = re.random() < p; s = slip(rs, mod)
            eq += (1.95 if win else -(1.05 + s)) * risk
            if eq <= -0.10: return "max_loss"
            if eq <= floor: return "daily_loss"
            if eq >= target: return "pass"
    return "timeout"

def sfida(seed, mod, risk, tpd, md, n):
    c = dict(pass_=0, max_loss=0, daily_loss=0, timeout=0); pl = []
    for i in range(n):
        re, rs = random.Random(seed * 10**7 + i), random.Random(seed * 10**7 + i + 5 * 10**6)
        a = fase(re, rs, mod, risk, tpd, md, 0.10)
        if a == "pass": a = fase(re, rs, mod, risk, tpd, md, 0.05)
        c["pass_" if a == "pass" else a] += 1
    return {k: v / n for k, v in c.items()}

r, tpd, md = 0.01, 6, 25
print("\n(2) Convergenza della probabilità di superamento con slippage Lomax NON troncato (20 semi × 5.000)")
vals = [sfida(s, "lomax", r, tpd, md, 5000)["pass_"] for s in range(1, 21)]
m = statistics.fmean(vals)
print(f"    media {m:.4f} · dev.std tra semi {statistics.stdev(vals):.4f} · errore binomiale atteso {math.sqrt(m*(1-m)/5000):.4f}")

print("\n(3) Intraday 1%, 6 trade/giorno, 25 giorni, 30.000 sfide, numeri casuali comuni")
base = None
for mod in ("nessuno", "lognormale", "lomax_cap1", "lomax_cap3", "lomax"):
    res = sfida(99, mod, r, tpd, md, 30000)
    if base is None: base = res
    print(f"    {mod:11s} pass {res['pass_']:.4f} ({res['pass_']-base['pass_']:+.4f})  DL {res['daily_loss']:.4f}  ML {res['max_loss']:.4f}")
