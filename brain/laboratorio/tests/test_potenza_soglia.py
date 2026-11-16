"""Test del calcolo di potenza per la soglia IA-02 (laboratorio/studi/potenza_soglia.py), scritti PRIMA del codice.
Nessun dato vero: formule e simulazioni su esiti inventati.
Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_potenza_soglia
"""
import sys
import unittest
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.laboratorio.studi import potenza_soglia as P            # noqa: E402


class TestPotenza(unittest.TestCase):
    def test_esiti_binari(self):
        # target 1,5 R, stop 1 R, media 0,15 R: p = 1,15 / 2,5 = 0,46; sigma = 2,5 * sqrt(0,46 * 0,54)
        self.assertAlmostEqual(P.sigma_esiti(0.15, 1.5), 2.5 * (0.46 * 0.54) ** 0.5, places=12)
        self.assertAlmostEqual(P.sigma_esiti(0.0, 1.0), 1.0, places=12)

    def test_regola_sulla_stima_passa_meta_delle_volte_al_limite(self):
        for n in (100, 1000, 5000):
            self.assertAlmostEqual(P.prob_promozione(0.15, 1.2, n, 0.15, "stima"), 0.5, places=12)

    def test_regola_sul_limite_inferiore_piu_severa(self):
        for mu in (0.10, 0.20, 0.30):
            self.assertLess(P.prob_promozione(mu, 1.2, 500, 0.15, "limite"), P.prob_promozione(mu, 1.2, 500, 0.15, "stima"))
        self.assertAlmostEqual(P.prob_promozione(0.15, 1.2, 500, 0.15, "limite"), 0.025, places=3)
        with self.assertRaises(ValueError):
            P.prob_promozione(0.2, 1.2, 500, 0.15, "altro")

    def test_numerosita_per_la_potenza(self):
        for regola in ("stima", "limite"):
            n = P.n_per_potenza(0.30, 1.2, 0.15, 0.8, regola)
            self.assertGreaterEqual(P.prob_promozione(0.30, 1.2, n, 0.15, regola), 0.8)
            self.assertLess(P.prob_promozione(0.30, 1.2, n - 1, 0.15, regola), 0.8)
        self.assertIsNone(P.n_per_potenza(0.15, 1.2, 0.15, 0.8, "limite"))      # vantaggio vero = soglia: impossibile

    def test_simulazione_coerente_con_la_formula(self):
        for mu, regola in ((0.25, "limite"), (0.10, "stima"), (0.20, "stima")):
            sim = P.simula(mu, 1.5, 400, 0.15, regola, prove=4000, seme=7)
            teo = P.prob_promozione(mu, P.sigma_esiti(mu, 1.5), 400, 0.15, regola)
            self.assertAlmostEqual(sim, teo, delta=0.03, msg=(mu, regola))


if __name__ == "__main__":
    unittest.main()


class TestDominioR13(unittest.TestCase):
    """#70 (R13-C2-01)."""

    def test_valori_fuori_dominio_rifiutati(self):
        for mu in (-1.0, -1.5, 1.5, 2.0):
            with self.assertRaises(ValueError, msg=mu):
                P.sigma_esiti(mu, 1.5)
        with self.assertRaises(ValueError):
            P.prob_promozione(0.2, 0.0, 100, 0.15, "stima")
        with self.assertRaises(ValueError):
            P.prob_promozione(0.2, 1.2, 0, 0.15, "stima")
        for potenza in (0.0, 1.0, 1.5):
            with self.assertRaisesRegex(ValueError, "potenza", msg=potenza):     # mutante P12: il NOSTRO messaggio,
                P.n_per_potenza(0.3, 1.2, 0.15, potenza, "stima")                 # non uno StatisticsError di passaggio
        with self.assertRaises(ValueError):
            P.simula(0.2, 1.5, 1, 0.15, "stima", prove=10)

    def test_varianza_campionaria_con_n_meno_uno(self):
        # 2 vinte (+1,5) e 2 perse (−1) su 4: media 0,25, scarti quadrati 4 × 1,5625 = 6,25, varianza 6,25 / 3
        self.assertAlmostEqual(P._varianza_campionaria(2, 4, 1.5), 6.25 / 3, places=12)
