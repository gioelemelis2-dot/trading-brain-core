"""[CLAUDE · VERIFICA V3.3, adattato da v32_c_kelly_q08_crn.py] Q-01 (IC dell'edge), Q-03 (momenti troncati del Lomax in forma chiusa, indipendente dalla
integrazione numerica della V3.1), Q-08 (casi estremi del MAE, soglia mu~0, input non validi), semi CRN.
Uso: python3 -s v32_c_kelly_q08_crn.py <cartella con prop_risk_engine_v3_3.py>"""
import sys, math, random
from statistics import NormalDist
sys.path.insert(0, sys.argv[1])
import prop_risk_engine_v3_3 as E

print("Q-01 · Intervallo dell'edge, N=300, WR 0,40, R:R 2, costo 0,05")
p, b, c, N = 0.40, 2.0, 0.05, 300
m = p * b - (1 - p) - c; se = (b + 1) * math.sqrt(p * (1 - p) / N)
var_r = (b + 1) ** 2 * p * (1 - p)
z95 = NormalDist().inv_cdf(0.975)
print(f"  E[R] {m:.6f}  SE {se:.6f}  (controllo: sqrt(Var[R]/N) = {math.sqrt(var_r / N):.6f}, Var[R] = {var_r:.4f})")
print(f"  ±1 SE: [{m - se:+.4f}, {m + se:+.4f}]   IC 95% (z {z95:.6f}): [{m - z95 * se:+.4f}, {m + z95 * se:+.4f}]")
kf = lambda mm, v: 2 * mm * 0.10 / (v * math.log(20))
print(f"  f* ai limiti di ±1 SE: [{100 * kf(m - se, var_r):.3f}%, {100 * kf(m + se, var_r):.3f}%]; al limite inferiore 95%: {100 * kf(m - z95 * se, var_r):+.3f}% (negativo)")
r = E.calculate_kelly_confidence_interval(300, 0.40, 2.0, 0.05, 0.95)
print(f"  Motore V3.3 (95%): E {r[0]:.6f} SE {r[1]:.6f} IC [{r[2]:+.6f}, {r[3]:+.6f}]")
print("  Quantile usato dal motore per altri livelli, contro il valore esatto:")
for cl in (0.6827, 0.675, 0.69, 0.80, 0.90, 0.99):
    zz = (E.calculate_kelly_confidence_interval(300, 0.40, 2.0, 0.05, cl)[1] and
          (E.calculate_kelly_confidence_interval(300, 0.40, 2.0, 0.05, cl)[3] - r[0]) / r[1])
    print(f"    livello {cl:.4f}: z motore {zz:.4f}  z esatto {NormalDist().inv_cdf(0.5 + cl / 2):.4f}")
print("  Wilson del motore a livelli diversi da 0,95 (k=50, n=100):")
for cl in (0.90, 0.95, 0.99):
    lo, hi = E.wilson_confidence_interval(50, 100, cl); zz = NormalDist().inv_cdf(0.5 + cl / 2)
    ph = 0.5; den = 1 + zz * zz / 100; cen = (ph + zz * zz / 200) / den
    hw = zz * math.sqrt(ph * (1 - ph) / 100 + zz * zz / 40000) / den
    print(f"    livello {cl}: motore [{lo:.4f}, {hi:.4f}]  corretto [{cen - hw:.4f}, {cen + hw:.4f}]")

print("\nQ-03 · Slippage Lomax (alpha 1,8, scala 0,05R, tetto 3R) applicato alle perdite: momenti in forma chiusa")
a, lam, cap = 1.8, 0.05, 3.0; T = 1 + cap / lam
ES = lam / (a - 1) * (1 - T ** (1 - a))
ES2 = 2 * lam ** 2 * ((T ** (2 - a) - 1) / (2 - a) - (T ** (1 - a) - 1) / (1 - a))
VS = ES2 - ES ** 2
EY = p * b - (1 - p) * (1 + ES); EY2 = p * b * b + (1 - p) * (1 + 2 * ES + ES2)
m_net = EY - c; V = EY2 - EY ** 2
print(f"  E[S] {ES:.6f}  E[S^2] {ES2:.6f}  Var[S] {VS:.6f}  P(S >= tetto) {T ** -a:.6f}")
print(f"  E[R netto] {m_net:.6f}  Var[R] {V:.6f}  f* {100 * kf(m_net, V):.4f}%   (dichiarati 0,0602 / 0,0222 / 0,1139 / 2,2609 / 0,3363%)")
rng = random.Random(3); n = 2_000_000; s1 = s2 = 0.0
for _ in range(n):
    u = rng.random(); x = min(cap, max(0.0, ((1 - u) ** (-1 / a) - 1) * lam)); s1 += x; s2 += x * x
print(f"  Controllo Monte Carlo della formula del motore (n=2e6): E[S] {s1 / n:.5f}  Var[S] {s2 / n - (s1 / n) ** 2:.5f}")

print("\nQ-08 · Casi estremi del MAE (costruttore; se accettato: errore di P_win e confronto del campionatore con F(d) esatto)")
def F(d, bb, mu):
    s = (lambda x: x) if mu == 0 else (lambda x: -math.expm1(-2 * mu * x))
    P = lambda x, up, lo: (s(x) - s(lo)) / (s(up) - s(lo))
    return (1 - P(0, bb, -d)) * P(-d, bb, -1) / P(0, bb, -1)
casi = [(0.40, 50.0), (0.99, 2.0), (0.99, 50.0), (0.999, 2.0), (0.40, 24.0), (0.40, 100.0), (0.40, 500.0), (0.99, 500.0),
        (0.9999995, 50.0), (0.05, 0.10), (0.40, 0.001), (0.90, 0.02), (1/3 + 1e-8, 2.0), (1/3 + 2e-7, 2.0), (1/3 - 3e-7, 2.0)]
for wr, rr in casi:
    try:
        sc = E.PropSimulationScenarioV3_3("x", wr, rr, cost_r=0.0, use_brownian_mae=True); mu = sc.brownian_mu
    except Exception as e:
        print(f"  WR {wr:<10.8g} R:R {rr:<6g}: {type(e).__name__}: {str(e)[:90]}"); continue
    pw = 1 / (1 + rr) if mu == 0 else -math.expm1(2 * mu) / (math.exp(-2 * mu * rr) - math.exp(2 * mu))
    g = random.Random(11); xs = sorted(-E.sample_brownian_mae_given_win(g, rr, mu) for _ in range(20000))
    dmax = 0.0
    for d in (0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.98):
        emp = sum(1 for x in xs if x >= d) / len(xs); dmax = max(dmax, abs(emp - F(d, rr, mu)) / math.sqrt(max(F(d, rr, mu) * (1 - F(d, rr, mu)), 1e-9) / 20000))
    print(f"  WR {wr:<10.8g} R:R {rr:<6g}: mu {mu:+.6g}  |P_win - WR| {abs(pw - wr):.1e}  campionatore vs F(d): max |z| {dmax:.2f}")
print("  Continuita' alla soglia mu~0 (R:R 2): F(0,5) con mu 0 e con mu 1,01e-7, 1e-6:",
      ", ".join(f"{F(0.5, 2.0, mm):.9f}" for mm in (0, 1.01e-7, 1e-6)))

print("\nInput non validati (rilevati, non intercettati)")
def prova(desc, fn):
    try: print(f"  {desc}: esito {fn()}")
    except Exception as e: print(f"  {desc}: {type(e).__name__}: {str(e)[:80]}")
prova("R:R = nan, 1 sfida, 30 giorni", lambda: E.run_full_challenge_v3_3(1, E.PropSimulationScenarioV3_3("x", 0.4, float('nan')), 0.01, 2, 30, 1)["_challenge_outcomes"])
prova("R:R = inf, 1 sfida", lambda: E.run_full_challenge_v3_3(1, E.PropSimulationScenarioV3_3("x", 0.4, float('inf')), 0.01, 2, 30, 1)["_challenge_outcomes"])
prova("costo = nan", lambda: E.run_full_challenge_v3_3(1, E.PropSimulationScenarioV3_3("x", 0.4, 2.0, cost_r=float('nan')), 0.01, 2, 30, 1)["_challenge_outcomes"])
prova("rischio = -1%", lambda: E.run_full_challenge_v3_3(1, E.PropSimulationScenarioV3_3("x", 0.4, 2.0), -0.01, 2, 30, 5)["_challenge_outcomes"])
prova("alpha slippage = 0", lambda: E.run_full_challenge_v3_3(1, E.PropSimulationScenarioV3_3("x", 0.4, 2.0, slippage_tail_alpha=0.0), 0.01, 2, 30, 1)["_challenge_outcomes"])
prova("max_days 3 < min_days 4, target istantaneo", lambda: E.simulate_phase_v3_3(random.Random(1), random.Random(2), random.Random(3), E.PropSimulationScenarioV3_3("x", 1 - 1e-9, 2.0, cost_r=0), 0.05, 1, 3, 0.10))

print("\nSemi CRN: collisioni tra flussi (sfida i, flusso k) per seme 42")
for n in (2500, 3000, 10000, 20000):
    seen = {}
    coll = 0
    for i in range(n):
        base = (42 * 1_000_003 + i * 1_007) & 0xFFFFFFFF
        for off in (0, 100_000, 200_000, 500_000, 600_000, 700_000):
            k = (base + off) & 0xFFFFFFFF; coll += k in seen; seen[k] = (i, off)
    print(f"  n {n}: collisioni {coll}")
inv = pow(1007, -1, 2 ** 32)
print("  Distanza minima tra sfide perche' due flussi coincidano (qualsiasi seme):",
      min(min((d * inv) % 2 ** 32, (-d * inv) % 2 ** 32) for d in (100_000, 200_000, 300_000, 400_000, 500_000, 600_000, 700_000)))
