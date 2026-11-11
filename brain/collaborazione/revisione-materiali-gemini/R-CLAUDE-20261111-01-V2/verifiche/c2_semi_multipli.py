"""[CLAUDE · VERIFICA] Esegue il motore ORIGINALE di Gemini (importato, non modificato) con semi diversi
e confronta media e dispersione con il valore esatto di c1_esatto_challenge.py."""
import sys, statistics, math, time
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, sys.argv[2])
from prop_risk_engine_v2 import PropSimulationScenarioV2, run_full_challenge_v2
from c1_esatto_challenge import challenge
scen = PropSimulationScenarioV2("B", win_rate=0.40, reward_to_risk=2.0, cost_r=0.05)
for (r, tpd, md) in [(0.005, 2, 60), (0.01, 6, 25)]:
    ex = challenge(0.40, r, 2.0, 0.05, tpd, md)["pass"]
    t = time.time(); vals = []
    for seed in range(1, 31):
        vals.append(run_full_challenge_v2(seed, scen, r, tpd, md, 10000)["pass"]["rate"])
    m, s = statistics.fmean(vals), statistics.stdev(vals)
    se_atteso = math.sqrt(ex * (1 - ex) / 10000)
    print(f"rischio {r:.3f} tpd {tpd}: esatto {ex:.4f} | 30 semi: media {m:.4f}, dev.std {s:.4f} "
          f"(attesa binomiale {se_atteso:.4f}) | z della media {(m-ex)/(se_atteso/math.sqrt(30)):.2f} | {time.time()-t:.0f}s")
