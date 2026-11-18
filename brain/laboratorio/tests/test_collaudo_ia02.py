"""Test del pilota di collaudo del test IA-02 sul limite inferiore (studi/collaudo_ia02.py), scritti PRIMA del codice
(17/11/2026; risposta 7 al DGS, §4). Solo numeri inventati. Il pilota vero (migliaia di repliche) NON si esegue
senza il via del titolare: qui si controllano i pezzi con poche repliche e con i riferimenti analitici del DGS.
Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_collaudo_ia02
"""
import io
import math
import random
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.laboratorio.studi import collaudo_ia02 as C                 # noqa: E402


class TestRiferimentiAnalitici(unittest.TestCase):
    def test_fattore_ar1_del_dgs(self):
        """Addendum del DGS §2: F a n = 450 per rho 0; 0,25; 0,50."""
        self.assertAlmostEqual(C.fattore_ar1(450, 0.0), 1.0, places=12)
        self.assertAlmostEqual(C.fattore_ar1(450, 0.25), 1.664691, places=6)
        self.assertAlmostEqual(C.fattore_ar1(450, 0.50), 2.991111, places=6)

    def test_falsa_promozione_del_test_ingenuo(self):
        self.assertAlmostEqual(C.falsa_promozione_ingenua(450, 0.25, 0.025), 0.064371, places=5)
        self.assertAlmostEqual(C.falsa_promozione_ingenua(450, 0.50, 0.025), 0.128551, places=5)
        self.assertAlmostEqual(C.falsa_promozione_ingenua(450, 0.0, 0.025), 0.025, places=9)

    def test_clopper_pearson(self):
        lo, hi = C.clopper_pearson(0, 100, 0.95)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 1 - 0.025 ** (1 / 100), places=6)
        lo, hi = C.clopper_pearson(5, 100, 0.95)                        # valori di riferimento noti
        self.assertAlmostEqual(lo, 0.016432, places=4)
        self.assertAlmostEqual(hi, 0.112835, places=4)
        lo, hi = C.clopper_pearson(100, 100, 0.95)
        self.assertEqual(hi, 1.0)


class TestGeneratoreEMetodi(unittest.TestCase):
    def test_serie_ar1_stazionaria(self):
        rnd = random.Random(7)
        x = C.serie_ar1(200_000, 0.15, 1.25, 0.25, rnd)
        media = sum(x) / len(x)
        var = sum((v - media) ** 2 for v in x) / (len(x) - 1)
        r1 = sum((x[i] - media) * (x[i + 1] - media) for i in range(len(x) - 1)) / (len(x) - 1) / var
        self.assertAlmostEqual(media, 0.15, delta=0.02)
        self.assertAlmostEqual(var, 1.25 ** 2, delta=0.05)
        self.assertAlmostEqual(r1, 0.25, delta=0.02)
        self.assertEqual(C.serie_ar1(5, 0.15, 1.25, 0.25, random.Random(3)),
                         C.serie_ar1(5, 0.15, 1.25, 0.25, random.Random(3)))       # riproducibile

    def test_limite_ingenuo_e_hac(self):
        x = [0.5, -1.0, 1.5, 0.2, -0.3, 0.9, -1.1, 0.4]
        n = len(x)
        m = sum(x) / n
        s = math.sqrt(sum((v - m) ** 2 for v in x) / (n - 1))
        z = C.Z(0.025)
        self.assertAlmostEqual(C.limite_ingenuo(x, 0.025), m - z * s / math.sqrt(n), places=12)
        g0 = sum((v - m) ** 2 for v in x) / n
        self.assertAlmostEqual(C.limite_hac(x, 0.025, ritardi=0), m - z * math.sqrt(g0 / n), places=12)
        g1 = sum((x[i] - m) * (x[i + 1] - m) for i in range(n - 1)) / n
        atteso = m - z * math.sqrt((g0 + 2 * (1 - 1 / 2) * g1) / n)                    # Bartlett, L = 1
        self.assertAlmostEqual(C.limite_hac(x, 0.025, ritardi=1), atteso, places=12)
        self.assertEqual(C.ritardi_newey_west(1000), math.floor(4 * (1000 / 100) ** (2 / 9)))

    def test_bootstrap_a_blocchi(self):
        rnd = random.Random(11)
        x = C.serie_ar1(300, 0.15, 1.25, 0.25, rnd)
        a = C.limite_bootstrap(x, 0.025, 199, random.Random(5))
        b = C.limite_bootstrap(x, 0.025, 199, random.Random(5))
        self.assertEqual(a, b)                                                      # riproducibile
        self.assertLess(a, sum(x) / len(x))                                         # un limite inferiore
        self.assertEqual(C.blocco_predefinito(1000), 10)

    def test_cella_conta_le_promozioni(self):
        """Poche repliche: solo il funzionamento, non il tasso vero."""
        r = C.cella(n=200, mu=0.15, rho=0.0, metodo="ingenuo", repliche=200, seme=1)
        self.assertEqual(r["repliche"], 200)
        self.assertTrue(0 <= r["promosse"] <= 200)
        self.assertLess(r["promosse"] / 200, 0.10)
        forte = C.cella(n=1000, mu=0.60, rho=0.0, metodo="hac", repliche=50, seme=2)
        self.assertEqual(forte["promosse"], 50)                                     # vantaggio molto forte


class TestCoperturaDopoIMutanti(unittest.TestCase):
    """Scritti DOPO la corsa dei mutanti (CO02, CO07, CO08, CO10 vivi al primo giro): dichiarato."""

    def test_primo_valore_gia_stazionario(self):
        rnd = random.Random(21)
        primi = [C.serie_ar1(1, 0.15, 1.25, 0.25, rnd)[0] for _ in range(20_000)]
        m = sum(primi) / len(primi)
        var = sum((v - m) ** 2 for v in primi) / (len(primi) - 1)
        self.assertAlmostEqual(var, 1.25 ** 2, delta=0.06)

    def test_blocchi_allargano_l_intervallo_con_dipendenza(self):
        x = C.serie_ar1(1000, 0.15, 1.25, 0.8, random.Random(4))
        a_blocchi = C.limite_bootstrap(x, 0.025, 299, random.Random(9))
        a_singoli = C.limite_bootstrap(x, 0.025, 299, random.Random(9), blocco=1)
        self.assertLess(a_blocchi, a_singoli - 0.05)

    def test_quantile_del_bootstrap(self):
        """Il limite è il k-esimo valore ordinato delle medie, k = ⌈a·R⌉ (calcolo indipendente)."""
        x = C.serie_ar1(100, 0.15, 1.25, 0.0, random.Random(8))
        R, a = 199, 0.025
        rnd = random.Random(3)
        b = C.blocco_predefinito(len(x))
        blocchi = math.ceil(len(x) / b)
        medie = sorted(sum(sum(x[i:i + b]) for i in [rnd.randint(0, len(x) - b) for _ in range(blocchi)])
                       / (blocchi * b) for _ in range(R))
        self.assertAlmostEqual(C.limite_bootstrap(x, a, R, random.Random(3)), medie[math.ceil(a * R) - 1], places=9)

    def test_quantile_del_bootstrap_con_blocco_che_non_divide_n(self):
        """Aggiunto dopo R16 (mutante M-R16-03 di Gemini sopravvissuto, dichiarato): con b che non divide n la media si
        fa su blocchi·b osservazioni, non su n."""
        x = C.serie_ar1(100, 0.15, 1.25, 0.0, random.Random(8))
        R, a, b = 199, 0.025, 7
        rnd = random.Random(3)
        blocchi = math.ceil(len(x) / b)
        medie = sorted(sum(sum(x[i:i + b]) for i in [rnd.randint(0, len(x) - b) for _ in range(blocchi)])
                       / (blocchi * b) for _ in range(R))
        self.assertAlmostEqual(C.limite_bootstrap(x, a, R, random.Random(3), blocco=b), medie[math.ceil(a * R) - 1],
                               places=9)

    def test_test_ingenuo_al_confine_con_dati_indipendenti(self):
        """Con trade indipendenti il test ingenuo al confine promuove circa il 2,5% (teoria del DGS)."""
        r = C.cella(n=1000, mu=0.15, rho=0.0, metodo="ingenuo", repliche=2000, seme=17)
        self.assertTrue(0.015 <= r["promosse"] / 2000 <= 0.04, r)


class TestRigaDiComando(unittest.TestCase):
    def test_pilota_ridotto(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = C.main(["--repliche", "10", "--bootstrap", "19", "--n", "120"])
        self.assertEqual(rc, 0)
        testo = buf.getvalue()
        for parola in ("ingenuo", "hac", "bootstrap", "rho", "Clopper"):
            self.assertIn(parola, testo)
        self.assertIn("NON è il pilota", testo)                                     # con poche repliche lo dice


if __name__ == "__main__":
    unittest.main()
