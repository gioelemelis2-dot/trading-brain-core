"""[CLAUDE · TEST AGGIUNTIVI] per prop_risk_engine_v2.py (Gemini). Non modificano il motore.
Gruppo A: devono PASSARE se il motore è corretto rispetto al modello dichiarato.
Gruppo B: documentano DIFETTI noti; falliscono sul motore V2 consegnato (attesi come fallimenti).
Il motore si importa dalla cartella in cui si trova questo file (collegamento simbolico) o dalla variabile
MOTORE_DIR; i valori di riferimento esatti vengono da c1_esatto_challenge.py / c4b_markov_esatto.py."""
import math, os, random, sys, unittest
QUI = os.path.abspath(os.path.dirname(__file__)); VER = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, VER); sys.path.insert(0, os.environ.get("MOTORE_DIR", QUI))
from prop_risk_engine_v2 import PropSimulationScenarioV2, simulate_phase_v2, run_full_challenge_v2
from c1_esatto_challenge import challenge
from c4b_markov_esatto import due_fasi

B = PropSimulationScenarioV2("B", win_rate=0.40, reward_to_risk=2.0, cost_r=0.05)

class RngFinto:
    """Generatore controllato: random() e gauss() restituiscono valori prestabiliti."""
    def __init__(self, unif, gauss=()): self.u, self.g = list(unif), list(gauss)
    def random(self): return self.u.pop(0)
    def gauss(self, mu, sd): return self.g.pop(0)

def z(stima, esatto, n): return (stima - esatto) / math.sqrt(max(esatto * (1 - esatto), 1e-9) / n)

class A_Concordanza(unittest.TestCase):
    N = 20000
    def test_A1_swing_1pct_concorda_con_esatto(self):
        res = run_full_challenge_v2(7, B, 0.01, 2, 60, self.N); ex = challenge(0.40, 0.01, 2.0, 0.05, 2, 60)
        for k in ("pass", "max_loss", "timeout"):
            self.assertLess(abs(z(res[k]["rate"], ex[k], self.N)), 4, k)
    def test_A2_intraday_1pct_concorda_con_esatto(self):
        res = run_full_challenge_v2(7, B, 0.01, 6, 25, self.N); ex = challenge(0.40, 0.01, 2.0, 0.05, 6, 25)
        for k in ("pass", "max_loss", "daily_loss"):
            self.assertLess(abs(z(res[k]["rate"], ex[k], self.N)), 4, k)
    def test_A3_markov_concorda_con_esatto_stesso_stato_iniziale(self):
        s = PropSimulationScenarioV2("M", 0.40, 2.0, 0.05, p_loss_given_loss=0.80)
        res = run_full_challenge_v2(7, s, 0.01, 2, 60, self.N)
        ex_pass = due_fasi(p=0.40, pll=0.80, risk=0.01, tpd=2, max_days=60, init="W")[0]
        self.assertLess(abs(z(res["pass"]["rate"], ex_pass, self.N)), 4)

class A_Deterministici(unittest.TestCase):
    def test_A4_mae_puo_violare_il_daily_loss_durante_un_trade_vincente(self):
        # 4 perdite da -1,05% (equity -4,2%), poi una vincita con MAE -0,9R: fluttuante -5,1% <= -5%
        s = PropSimulationScenarioV2("MAE", 0.40, 2.0, 0.05, mae_mean_winner=-0.205)
        rng = RngFinto([0.9, 0.9, 0.9, 0.9, 0.1], gauss=[-0.90])
        esito, giorno, _ = simulate_phase_v2(rng, s, 0.01, 6, 1, 0.10)
        self.assertEqual((esito, giorno), ("daily_loss", 1))
    def test_A5_costi_applicati(self):
        rng = RngFinto([0.9])   # una perdita
        s = PropSimulationScenarioV2("C", 0.40, 2.0, 0.05)
        esito, _, eq = simulate_phase_v2(rng, s, 0.01, 1, 1, 0.10)
        self.assertAlmostEqual(eq, -0.0105, places=10)
    def test_A6_target_raggiunto_dopo_min_days_chiude_quel_giorno(self):
        s = PropSimulationScenarioV2("W", 1.0, 2.0, 0.0)
        esito, giorno, eq = simulate_phase_v2(random.Random(1), s, 0.01, 1, 30, 0.10)  # +2% al giorno
        self.assertEqual((esito, giorno), ("pass", 5)); self.assertAlmostEqual(eq, 0.10, places=9)

class B_DifettiDocumentati(unittest.TestCase):
    """Falliscono sul motore consegnato: servono a tracciare i difetti, non a 'passare'."""
    def test_B1_markov_parte_dalla_distribuzione_stazionaria(self):
        s = PropSimulationScenarioV2("M", 0.40, 2.0, 0.05, p_loss_given_loss=0.80)
        vinte = 0; n = 20000
        for i in range(n):
            esito, _, eq = simulate_phase_v2(random.Random(i), s, 0.01, 1, 1, 0.10)
            vinte += eq > 0
        self.assertLess(abs(z(vinte / n, 0.40, n)), 4, f"primo trade vinto nel {vinte/n:.3f} dei casi")
    def test_B2_markov_rifiuta_parametri_non_ammissibili(self):
        s = PropSimulationScenarioV2("M", 0.40, 2.0, 0.05, p_loss_given_loss=0.20)  # richiede P(L|W)=1,2
        with self.assertRaises(ValueError):
            simulate_phase_v2(random.Random(0), s, 0.01, 2, 5, 0.10)
    def test_B3_parametro_slippage_dichiarato_ha_effetto(self):
        a = PropSimulationScenarioV2("S0", 0.40, 2.0, 0.05)
        b = PropSimulationScenarioV2("S1", 0.40, 2.0, 0.05, slippage_tail_alpha=1.8)
        ra = run_full_challenge_v2(3, a, 0.01, 6, 25, 3000); rb = run_full_challenge_v2(3, b, 0.01, 6, 25, 3000)
        self.assertNotEqual(ra["pass"]["count"], rb["pass"]["count"], "slippage_tail_alpha non è usato dal motore")

if __name__ == "__main__":
    unittest.main(verbosity=1)
