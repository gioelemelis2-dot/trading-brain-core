"""Errata V3.3 (D-17, D-22): test aggiuntivi sul motore V3.3 CONGELATO, senza modificarlo.

Il motore si importa da PYTHONPATH (cartella che contiene prop_risk_engine_v3_3.py, SHA-256 b20608ca…1a12).
Ogni valore di riferimento è calcolato qui in modo INDIPENDENTE dal motore (formule chiuse, libreria standard).

- T-01 / V22: campionatore MAE deterministico con deriva piccola ma non nulla (mu = 0,05).
- T-04 / V16: una configurazione irraggiungibile deve sollevare ValueError.
- T-04 / V24: deriva negativa: la deriva risolta deve riprodurre il win rate.
- R-16 (revisione esterna): wilson_confidence_interval(0, 0) restituisce (0, 0). È un difetto noto del codice congelato,
  marcato expectedFailure: il test documenta il comportamento corretto, da adottare nel codice nuovo.

Uso: PYTHONPATH=<cartella del motore V3.3> python3 -s -B test_errata_v3_3.py
"""
import math
import unittest

import prop_risk_engine_v3_3 as E


class Fisso:
    def __init__(self, v):
        self.v = v

    def random(self):
        return self.v


def p_win(mu, rr):
    """P(+rr prima di -1) per moto browniano con deriva mu e sigma 1 (formula chiusa indipendente)."""
    if mu == 0:
        return 1.0 / (1.0 + rr)
    return -math.expm1(2 * mu) / (math.exp(-2 * mu * rr) - math.exp(2 * mu))


def F(d, b, mu):
    """P(MAE <= -d | vincita), 0 < d < 1, barriere -1 e +b (funzione di scala s(x) = 1 - exp(-2 mu x))."""
    s = (lambda x: x) if mu == 0 else (lambda x: -math.expm1(-2 * mu * x))
    P = lambda x, up, lo: (s(x) - s(lo)) / (s(up) - s(lo))
    return (1 - P(0, b, -d)) * P(-d, b, -1) / P(0, b, -1)


class TestErrataV33(unittest.TestCase):

    def test_t01_v22_campionatore_deriva_piccola(self):
        """Con mu = 0,05 il campionatore deve usare la formula con deriva: F(m(u)) = u entro 1e-12.
        Con la soglia mu~0 portata a 0,1 (mutante V22) userebbe la formula a deriva nulla e sbaglierebbe di ~1e-3."""
        for b in (1.0, 2.0, 3.0):
            for u in (0.1, 0.3, 0.5, 0.7, 0.9):
                m = -E.sample_brownian_mae_given_win(Fisso(u), b, 0.05)
                self.assertAlmostEqual(F(m, b, 0.05), u, places=12, msg=f"b={b} u={u}")

    def test_t04_v16_configurazione_irraggiungibile(self):
        """WR 0,40 con R:R 0,001 richiede una deriva fuori dall'intervallo di ricerca: errore esplicito, non un valore al bordo."""
        with self.assertRaises(ValueError):
            E.PropSimulationScenarioV3_3("irraggiungibile", 0.40, 0.001, use_brownian_mae=True)

    def test_t04_v24_deriva_negativa(self):
        """WR sotto il valore equo (deriva negativa): la deriva risolta riproduce il win rate entro 1e-12."""
        for wr, rr in ((0.05, 0.1), (0.90, 0.02), (0.20, 3.0)):
            mu = E.PropSimulationScenarioV3_3("x", wr, rr, use_brownian_mae=True).brownian_mu
            self.assertLess(mu, 0.0)
            self.assertAlmostEqual(p_win(mu, rr), wr, places=12, msg=f"WR={wr} R:R={rr}")

    @unittest.expectedFailure
    def test_r16_wilson_zero_osservazioni(self):
        """R-16: con n = 0 la proporzione non è stimabile. Comportamento corretto: ValueError (o stato NON STIMABILE).
        V3.3 restituisce (0, 0): difetto noto, il codice congelato non si corregge (D-17)."""
        with self.assertRaises(ValueError):
            E.wilson_confidence_interval(0, 0)


if __name__ == "__main__":
    unittest.main()
