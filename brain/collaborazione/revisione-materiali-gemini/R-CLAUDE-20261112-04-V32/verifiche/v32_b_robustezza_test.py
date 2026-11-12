"""[CLAUDE · VERIFICA V3.2] I test stocastici della suite V3.2 passano per merito o per il seme?
(1) Valori effettivi con il seme 42 della suite (z dichiarati: Gruppo A |z| <= 1,46; test R:R 1 z = 0,13).
(2) Stessi controlli, motore ORIGINALE, con 40 semi alternativi: quante volte fallirebbero (falsi allarmi)?
(3) Mutante V10 (MAE troncato a 0,5R) con 40 semi: quante volte il Gruppo A lo intercetterebbe?
Uso: python3 -s v32_b_robustezza_test.py <cartella con prop_risk_engine_v3_2.py> <cartella mutante V10>"""
import sys, math, random, importlib.util

def carica(cartella, nome):
    spec = importlib.util.spec_from_file_location(nome, cartella + "/prop_risk_engine_v3_2.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

E = carica(sys.argv[1], "orig"); M10 = carica(sys.argv[2], "v10")
ESATTI = [("Senza limite 0,50%", "b", 0.0050, 2, None, 0.9108), ("Senza limite 1,00%", "b", 0.0100, 2, None, 0.7034),
          ("Swing 60 g 1,00%", "b", 0.0100, 2, 60, 0.6686), ("Markov swing 1%", "m", 0.0100, 2, 60, 0.4406),
          ("Intraday 1% MAE", "a", 0.0100, 6, 25, 0.3884)]

def gruppo_a(eng, seme, n=3000):
    sc = {"b": eng.PropSimulationScenarioV3_2("b", 0.40, 2.0, cost_r=0.05),
          "m": eng.PropSimulationScenarioV3_2("m", 0.40, 2.0, cost_r=0.05, p_loss_given_loss=0.80),
          "a": eng.PropSimulationScenarioV3_2("a", 0.40, 2.0, cost_r=0.05, use_brownian_mae=True)}
    out = []
    for nome, k, r, t, d, p in ESATTI:
        x = eng.run_full_challenge_v3_2(seme, sc[k], r, t, d, n)["pass"]["rate"]
        out.append((nome, x, (x - p) / math.sqrt(p * (1 - p) / n)))
    return out

def test_rr1(eng, s1, s2, s3, n=10000):
    sc = eng.PropSimulationScenarioV3_2("x", 0.50, 1.0, cost_r=0.0, use_brownian_mae=True)
    a, b, c = random.Random(s1), random.Random(s2), random.Random(s3)
    k = sum(eng.simulate_phase_v3_2(a, b, c, sc, 0.10, 1, 1, 0.50)[0] == "daily_loss" for _ in range(n))
    p = 1 / 6; return k / n, (k / n - p) / math.sqrt(p * (1 - p) / n)

def test_fase2(eng, s1, s2, s3, n=3000):
    sc = eng.PropSimulationScenarioV3_2("x", 0.40, 2.0, cost_r=0.05)
    def tasso(t):
        a, b, c = random.Random(s1), random.Random(s2), random.Random(s3)
        return sum(eng.simulate_phase_v3_2(a, b, c, sc, 0.01, 2, 60, target_pct=t)[0] == "pass" for _ in range(n)) / n
    return tasso(0.10), tasso(0.05)

print("(1) Seme della suite (42)")
for nome, x, zz in gruppo_a(E, 42): print(f"  Gruppo A {nome:20s} tasso {x:.4f}  z {zz:+.2f}")
x, zz = test_rr1(E, 42, 1042, 2042); print(f"  Test R:R 1 (1/6): tasso {x:.4f}  z {zz:+.2f}")
p1, p2 = test_fase2(E, 42, 142, 242)
print(f"  Test fase 2: P1 {p1:.4f}  P2 {p2:.4f} (esatti 0,7800 / 0,8572; il test confronta P2 con 0,8596 ± 0,025)")

print("\n(2) Motore originale, 40 semi alternativi (1001-1040)")
fa, zmax = 0, 0.0
for s in range(1001, 1041):
    zs = [abs(zz) for _, _, zz in gruppo_a(E, s)]; zmax = max(zmax, max(zs)); fa += any(v >= 4 for v in zs)
print(f"  Gruppo A: semi con almeno un |z| >= 4: {fa}/40; |z| massimo osservato {zmax:.2f}")
fr = sum(abs(test_rr1(E, s, s + 1000, s + 2000)[1]) >= 3 for s in range(1001, 1041))
print(f"  Test R:R 1 (soglia |z| < 3): fallimenti {fr}/40")
ff = 0
for s in range(1001, 1041):
    p1, p2 = test_fase2(E, s, s + 100, s + 200); ff += not (p2 > p1 + 0.05 and abs(p2 - 0.8596) <= 0.025)
print(f"  Test fase 2: fallimenti {ff}/40")

print("\n(3) Mutante V10 con 40 semi: intercettato dal Gruppo A (|z| >= 4) o dal test R:R 1 (|z| >= 3)?")
ka = sum(any(abs(zz) >= 4 for _, _, zz in gruppo_a(M10, s)) for s in range(1001, 1041))
kr = sum(abs(test_rr1(M10, s, s + 1000, s + 2000)[1]) >= 3 for s in range(1001, 1041))
print(f"  Gruppo A: {ka}/40 semi; test R:R 1: {kr}/40 semi (atteso ~0: in quel test V10 e' indistinguibile per costruzione)")
