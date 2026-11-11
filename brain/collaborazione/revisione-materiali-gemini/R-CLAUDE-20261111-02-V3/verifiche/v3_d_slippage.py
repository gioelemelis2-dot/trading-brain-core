"""[CLAUDE · VERIFICA V3] (D) Effetto dello slippage Lomax (alpha 1,8, scala 0,05R, tetto 3R) con un simulatore
indipendente di Claude e accoppiamento esatto per sfida. [SIMULATO], parametri come nel run V3 (illustrativi)."""
import random, math
A, SC, CAP = 1.8, 0.05, 3.0
def fase(re, rs, slip, risk, tpd, md, target):
    eq = 0.0
    for _ in range(md):
        fl = eq - 0.05
        for _ in range(tpd):
            win = re.random() < 0.40; u = rs.random()
            s = min(CAP, SC * ((1 - u) ** (-1 / A) - 1)) if (slip and not win) else 0.0
            eq += (1.95 if win else -(1.05 + s)) * risk
            if eq <= -0.10: return "max_loss"
            if eq <= fl: return "daily_loss"
            if eq >= target: return "pass"
    return "timeout"
def lotto(slip, risk, tpd, md, n, seed=5):
    c = {"pass": 0, "max_loss": 0, "daily_loss": 0, "timeout": 0}
    for i in range(n):
        re, rs = random.Random(seed * 10**7 + i), random.Random(seed * 10**7 + i + 5 * 10**6)
        a = fase(re, rs, slip, risk, tpd, md, 0.10)
        c[a if a != "pass" else fase(re, rs, slip, risk, tpd, md, 0.05)] += 1
    return {k: v / n for k, v in c.items()}
N = 20000
for (r, tpd, md, nome) in ((0.01, 2, 60, "swing 1%, 60 giorni"), (0.01, 2, 6000, "swing 1%, senza limite")):
    a, b = lotto(False, r, tpd, md, N), lotto(True, r, tpd, md, N)
    print(f"{nome:24s} senza slippage pass {a['pass']:.4f} ML {a['max_loss']:.4f} TO {a['timeout']:.4f} | con slippage pass {b['pass']:.4f} ML {b['max_loss']:.4f} TO {b['timeout']:.4f} | effetto {100*(b['pass']-a['pass']):+.2f} punti")
m = SC / (A - 1); tail = SC * ((1 + CAP / SC) ** (1 - A)) / (A - 1)   # E[S] - E[(S-CAP)+] per Lomax
print(f"Slippage medio per perdita: {m:.4f}R senza tetto, {m - tail:.4f}R con tetto 3R; E[R] netto: 0,150 -> {0.15 - 0.6*(m-tail):.4f}R")
