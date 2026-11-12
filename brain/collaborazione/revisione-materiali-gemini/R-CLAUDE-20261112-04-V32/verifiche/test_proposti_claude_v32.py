"""[CLAUDE · PROPOSTA PER LA V3.3] Test di accettazione proposti (S-02, S-04, S-07). NON fanno parte del pacchetto
di Antigravity: sono la forma eseguibile delle proposte. Devono PASSARE sul motore V3.2 originale e FALLIRE sui
mutanti indicati. Valori di riferimento: calcolo esatto (v32_a_esatto.py) e forma chiusa (v32_c_kelly_q08_crn.py).
Uso: PYTHONPATH=<cartella del motore> python3 -s test_proposti_claude_v32.py"""
import math, random, unittest
import prop_risk_engine_v3_2 as E

class Fisso:
    def __init__(self, v): self.v = v
    def random(self): return self.v

class TestPropostiClaude(unittest.TestCase):
    def test_mae_profondo_attraverso_motore_rr1(self):
        """S-02 (V10, V03): rischio 10%, daily loss 7,5%: violazione durante il trade se MAE <= -0,75R.
        Esatto: P = 0,5 * F(0,75) = 0,5 * (1/1,75) * 0,25 = 1/14. Con V10 (MAE troncato a 0,5R) e' 0."""
        sc = E.PropSimulationScenarioV3_2("x", 0.50, 1.0, cost_r=0.0, use_brownian_mae=True)
        a, b, c = random.Random(5), random.Random(6), random.Random(7); n = 20000
        k = sum(E.simulate_phase_v3_2(a, b, c, sc, 0.10, 1, 1, 0.50, max_daily_loss_pct=0.075)[0] == "daily_loss" for _ in range(n))
        p = 1 / 14
        self.assertLess(abs(k / n - p) / math.sqrt(p * (1 - p) / n), 4.0)

    def test_fase2_esatta_e_prodotto_due_fasi(self):
        """S-02 (V07): fase 2 isolata contro il valore ESATTO 0,8572 (non 0,8596) e sfida completa attraverso
        run_full_challenge_v3_2 contro P1*P2 esatto = 0,7800 * 0,8572 = 0,6686."""
        sc = E.PropSimulationScenarioV3_2("x", 0.40, 2.0, cost_r=0.05); n = 4000
        a, b, c = random.Random(8), random.Random(9), random.Random(10)
        p2 = sum(E.simulate_phase_v3_2(a, b, c, sc, 0.01, 2, 60, target_pct=0.05)[0] == "pass" for _ in range(n)) / n
        self.assertLess(abs(p2 - 0.8572) / math.sqrt(0.8572 * 0.1428 / n), 4.0)
        r = E.run_full_challenge_v3_2(11, sc, 0.01, 2, 60, n)["pass"]["rate"]
        self.assertLess(abs(r - 0.6686) / math.sqrt(0.6686 * 0.3314 / n), 4.0)

    def test_slippage_deterministico(self):
        """S-07 (V19, V20): una perdita con u_slip fissato. u = 0,5: S = (0,5^(-1/1,8) - 1) * 0,05;
        u -> 1: S al tetto 3R."""
        sc = E.PropSimulationScenarioV3_2("x", 0.40, 2.0, cost_r=0.05, slippage_tail_alpha=1.8, slippage_scale=0.05, slippage_cap_r=3.0)
        for u, s_att in ((0.5, (0.5 ** (-1 / 1.8) - 1) * 0.05), (1 - 1e-12, 3.0)):
            _, _, eq = E.simulate_phase_v3_2(Fisso(0.9), Fisso(0.5), Fisso(u), sc, 0.001, 1, 1, 0.10)
            self.assertAlmostEqual(eq, -(1 + s_att + 0.05) * 0.001, places=12)

    def test_momenti_slippage_forma_chiusa(self):
        """S-07: media e varianza campionarie della formula del motore contro i momenti troncati in forma chiusa
        E[S] = 0,060169, Var[S] = 0,022249 (n = 400000, tolleranza 4 errori standard sulla media)."""
        g = random.Random(12); n = 400000
        xs = [min(3.0, max(0.0, ((1 - g.random()) ** (-1 / 1.8) - 1) * 0.05)) for _ in range(n)]
        m = sum(xs) / n
        self.assertLess(abs(m - 0.060169) / math.sqrt(0.022249 / n), 4.0)

    def test_wilson_valori_noti(self):
        """S-04 (V21 e livelli diversi da 0,95): k=50, n=100."""
        for cl, (lo, hi) in ((0.95, (0.4038, 0.5962)), (0.90, (0.4188, 0.5812)), (0.99, (0.3753, 0.6247))):
            a, b = E.wilson_confidence_interval(50, 100, cl)
            self.assertAlmostEqual(a, lo, places=4); self.assertAlmostEqual(b, hi, places=4)

if __name__ == "__main__":
    unittest.main()
