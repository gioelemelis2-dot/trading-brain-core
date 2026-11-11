"""[CLAUDE · VERIFICA V3] (B) Accoppiamento CRN tra scenari; (C) campionatore del MAE; (E) test CRN di Gemini.
Importa il motore V3 ORIGINALE (non modificato). Uso: python3 -s v3_b_crn_mae.py <cartella v3-link> <verifiche V2 Claude>"""
import sys, random, math, statistics
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, sys.argv[2])
from prop_risk_engine_v3 import PropSimulationScenarioV3 as Sc, simulate_phase_v3, sample_brownian_mae_given_win
from c5_mae_browniano import cdf_mae

def sfide(scen, risk, tpd, md, n, seed, per_sfida):
    """Replica il ciclo di run_full_challenge_v3. per_sfida=False: generatori unici per il lotto (come Gemini);
    per_sfida=True: generatori riseminati per ogni sfida (accoppiamento esatto)."""
    out = []
    if not per_sfida:
        g = (random.Random(seed), random.Random(seed + 100_000), random.Random(seed + 200_000))
    for i in range(n):
        if per_sfida:
            g = (random.Random(seed * 10**6 + i), random.Random(seed * 10**6 + i + 10**12), random.Random(seed * 10**6 + i + 2 * 10**12))
        r1, _, _ = simulate_phase_v3(*g, scen, risk, tpd, md, 0.10)
        if r1 != "pass": out.append(r1); continue
        r2, _, _ = simulate_phase_v3(*g, scen, risk, tpd, md, 0.05); out.append(r2)
    return out

base = Sc("base", 0.40, 2.0, 0.05); mae = Sc("mae", 0.40, 2.0, 0.05, use_brownian_mae=True)
N = 10000
print("(B) Accoppiamento CRN: intraday 1%, 6 trade/giorno, 25 giorni, 10.000 sfide, seed 42")
for per_sfida, nome in ((False, "come V3 (generatori unici per il lotto)"), (True, "generatori riseminati per ogni sfida")):
    a = sfide(base, 0.01, 6, 25, N, 42, per_sfida); b = sfide(mae, 0.01, 6, 25, N, 42, per_sfida)
    impossibili = sum(1 for x, y in zip(a, b) if x != "pass" and y == "pass")   # col MAE si passa, senza no: impossibile se accoppiati
    diverse = sum(1 for x, y in zip(a, b) if x != y)
    prima = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), None)
    pa = a.count("pass") / N; pb = b.count("pass") / N
    print(f"  {nome:42s}: pass {pa:.4f} -> {pb:.4f} ({100*(pb-pa):+.2f} punti); sfide con esito diverso {diverse}; "
          f"casi IMPOSSIBILI (passa solo col MAE) {impossibili}; prima divergenza alla sfida {prima}")

print("\n(C1) Campionatore MAE di V3 contro la formula esatta (mu tarato per WR 0,40, R:R 2)")
rng = random.Random(7); n = 100000
xs = [sample_brownian_mae_given_win(rng) for _ in range(n)]
mu = 0.0974830
for m in (0.1, 0.25, 0.5, 0.75, 0.9):
    emp = sum(1 for x in xs if x <= -m) / n; ex = cdf_mae(m, mu)
    print(f"  P(MAE <= -{m:.2f}) campionata {emp:.4f}  esatta {ex:.4f}  z {(emp-ex)/math.sqrt(ex*(1-ex)/n):+.2f}")
print(f"  media campionata {statistics.fmean(xs):.4f}  (esatta -0.4315)")

print("\n(C2) Il campionatore ignora win_rate e reward_to_risk dello scenario (deriva 0,09754 e barriere +2/-1 fisse)")
def cdf_generale(m, a, b, mu):
    s = (lambda x: x) if abs(mu) < 1e-12 else (lambda x: 1 - math.exp(-2 * mu * x))
    P = lambda x, up, lo: (s(x) - s(lo)) / (s(up) - s(lo))
    return (1 - P(0, a, -m)) * P(-m, a, -b) / P(0, a, -b)
rng = random.Random(8); xs = [sample_brownian_mae_given_win(rng) for _ in range(50000)]
emp = sum(1 for x in xs if x <= -0.5) / 50000
print(f"  Scenario WR 0,50, R:R 1 (moto browniano SENZA deriva, barriere +1/-1): P(MAE <= -0,5R | vincita) corretta = {cdf_generale(0.5, 1, 1, 0):.4f}")
print(f"  Il motore V3 campiona comunque dalla distribuzione per WR 0,40 / R:R 2: {emp:.4f}")
s = Sc("x", 0.50, 1.0, 0.05, use_brownian_mae=True); print(f"  Lo scenario WR 0,50 R:R 1 con use_brownian_mae=True viene accettato senza avvisi: {s.name!r}")

print("\n(E) Il test test_crn_stream_isolation di Gemini esegue davvero l'asserzione?")
g1 = (random.Random(123), random.Random(456), random.Random(789)); g2 = (random.Random(123), random.Random(456), random.Random(789))
r1, _, _ = simulate_phase_v3(*g1, base, 0.005, 2, 10, 0.10); r2, _, _ = simulate_phase_v3(*g2, mae, 0.005, 2, 10, 0.10)
print(f"  esiti: senza MAE {r1!r}, con MAE {r2!r} -> asserzione eseguita: {r1 == 'timeout' and r2 == 'timeout'}")
