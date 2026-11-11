"""[CLAUDE · VERIFICA] Impatto del MAE sulla challenge con NUMERI CASUALI COMUNI (CRN):
stessi esiti dei trade per tutti i modelli; il MAE usa un generatore separato.
Modelli: (0) nessun MAE; (G) Normale(-0.205, 0.1025) tagliata come nel motore V2; (B) MAE browniano esatto
(c5). Il simulatore è indipendente da quello di Gemini; il caso (0) è validato contro il calcolo esatto (c1)."""
import sys, math, random, bisect; sys.path.insert(0, sys.argv[1])
from c1_esatto_challenge import challenge
from c5_mae_browniano import cdf_mae, mu

# tabella per campionare il MAE browniano per inversione
GRID = [i / 2000 for i in range(1, 2000)]
CDFB = [cdf_mae(m, mu) for m in GRID]           # P(MAE <= -m), decrescente in m
def mae_browniano(u):                            # restituisce MAE <= 0
    # cerca m con P(MAE <= -m) = u  (CDFB decrescente)
    lo, hi = 0, len(GRID) - 1
    if u >= CDFB[0]: return -GRID[0] * (1 - u) / (1 - CDFB[0]) if CDFB[0] < 1 else 0.0
    if u <= CDFB[-1]: return -GRID[-1]
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if CDFB[mid] >= u: lo = mid
        else: hi = mid
    return -GRID[lo]
def mae_gemini(rng):
    x = rng.gauss(-0.205, 0.1025); return min(0.0, max(-0.95, x))

def fase(rng_e, rng_m, modello, risk, tpd, max_days, target, p=0.40, rr=2.0, cost=0.05):
    eq = 0.0
    for day in range(max_days):
        floor = eq - 0.05
        for _ in range(tpd):
            win = rng_e.random() < p
            u = rng_m.random()                     # estratto sempre, per mantenere i flussi allineati
            if win and modello != "0":
                m = mae_browniano(u) if modello == "B" else mae_gemini(random.Random(u))
                fl = eq + m * risk
                if fl <= -0.10: return "max_loss"
                if fl <= floor: return "daily_loss"
            eq += ((rr - cost) if win else -(1 + cost)) * risk
            if eq <= -0.10: return "max_loss"
            if eq <= floor: return "daily_loss"
            if eq >= target: return "pass"
    return "timeout"

def sfida(seed, modello, risk, tpd, md, n):
    c = {"pass": 0, "max_loss": 0, "daily_loss": 0, "timeout": 0}
    for i in range(n):
        # un seme per sfida: accoppiamento esatto tra modelli (CRN), nessuno sfasamento tra sfide
        re, rm = random.Random(seed * 10**7 + i), random.Random(seed * 10**7 + i + 5 * 10**6)
        a = fase(re, rm, modello, risk, tpd, md, 0.10)
        if a != "pass": c[a] += 1; continue
        b = fase(re, rm, modello, risk, tpd, md, 0.05); c[b] += 1
    return {k: v / n for k, v in c.items()}

N = int(sys.argv[2]) if len(sys.argv) > 2 else 40000
for r, tpd, md in [(0.005, 6, 25), (0.01, 6, 25), (0.01, 2, 60)]:
    ex = challenge(0.40, r, 2.0, 0.05, tpd, md)
    res = {m: sfida(123, m, r, tpd, md, N) for m in ("0", "G", "B")}
    se = math.sqrt(ex["pass"] * (1 - ex["pass"]) / N)
    print(f"r={r:.3f} tpd={tpd}  N={N}  validazione caso 0: pass {res['0']['pass']:.4f} vs esatto {ex['pass']:.4f} (z {(res['0']['pass']-ex['pass'])/se:.2f})")
    for m, nome in (("G", "MAE Normale del motore"), ("B", "MAE browniano esatto")):
        d = {k: res[m][k] - res["0"][k] for k in res[m]}
        print(f"   {nome:24s}: pass {res[m]['pass']:.4f} ({d['pass']:+.4f})  DL {res[m]['daily_loss']:.4f} ({d['daily_loss']:+.4f})  ML {res[m]['max_loss']:.4f} ({d['max_loss']:+.4f})")
