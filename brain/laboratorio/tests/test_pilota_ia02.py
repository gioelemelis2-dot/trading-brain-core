"""Test del pilota del collaudo IA-02 nel disegno del DGS (DGS-06 §2c), scritti PRIMA del codice (17/11/2026, su
delega del titolare). Solo numeri inventati; nessuna certificazione.
Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_pilota_ia02
"""
import io
import math
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.laboratorio.studi import pilota_ia02 as P                    # noqa: E402


class TestSemi(unittest.TestCase):
    def test_flussi_deterministici_e_distinti(self):
        a = P.flusso(1, 3, 7, 0).random()
        self.assertEqual(a, P.flusso(1, 3, 7, 0).random())
        altri = {P.flusso(1, 3, 7, c).random() for c in (1, 2, 3)} | {P.flusso(1, 3, 8, 0).random(),
                                                                      P.flusso(2, 3, 7, 0).random(),
                                                                      P.flusso(1, 4, 7, 0).random()}
        self.assertNotIn(a, altri)
        self.assertEqual(len(altri), 6)


class TestGeneratori(unittest.TestCase):
    def momenti(self, cella, repliche=40):
        S = K = 0
        tutti = []
        for r in range(1, repliche + 1):
            coppie = P.genera(cella, 1, r)
            self.assertEqual(len(coppie), P.D)
            for s, k in coppie:
                S += s
                K += k
                if k == 1:
                    tutti.append(s)
        return S / K, tutti

    def test_celle_gaussiane(self):
        for cella, mu in ((1, 0.10), (4, 0.30), (5, 0.10), (8, 0.30)):
            media, x = self.momenti(cella)
            self.assertAlmostEqual(media, mu, delta=0.03, msg=cella)
            m = sum(x) / len(x)
            var = sum((v - m) ** 2 for v in x) / (len(x) - 1)
            self.assertAlmostEqual(var, 1.25 ** 2, delta=0.08, msg=cella)

    def test_ar1_stazionario_e_correlato(self):
        primi, r1 = [], []
        for r in range(1, 2001):
            coppie = P.genera(6, 1, r)
            primi.append(coppie[0][0])
        m = sum(primi) / len(primi)
        self.assertAlmostEqual(sum((v - m) ** 2 for v in primi) / (len(primi) - 1), 1.25 ** 2, delta=0.12)
        serie = [s for s, _ in P.genera(6, 1, 3)]
        mm = sum(serie) / len(serie)
        cov = sum((serie[i] - mm) * (serie[i + 1] - mm) for i in range(len(serie) - 1)) / (len(serie) - 1)
        var = sum((v - mm) ** 2 for v in serie) / (len(serie) - 1)
        self.assertAlmostEqual(cov / var, 0.25, delta=0.1)

    def test_conteggi_casuali(self):
        conte = {0: 0, 1: 0, 3: 0}
        S = K = 0
        for r in range(1, 41):
            for s, k in P.genera(9, 1, r):
                conte[k] += 1
                S += s
                K += k
                if k == 0:
                    self.assertEqual(s, 0.0)
        tot = sum(conte.values())
        self.assertAlmostEqual(conte[0] / tot, 0.25, delta=0.02)
        self.assertAlmostEqual(conte[1] / tot, 0.50, delta=0.02)
        self.assertAlmostEqual(conte[3] / tot, 0.25, delta=0.02)
        self.assertAlmostEqual(S / K, 0.15, delta=0.03)

    def test_conteggi_con_componente_comune(self):
        """Aggiunto dopo i mutanti (PI05 sopravvissuto, dichiarato). Nei giorni con K = 3,
        Var(S) = 1,25² · (9 · 0,5 + 3 · 0,5) = 9,375; senza la componente comune sarebbe 4,6875."""
        tre = [s for r in range(1, 41) for s, k in P.genera(9, 1, r) if k == 3]
        m = sum(tre) / len(tre)
        self.assertAlmostEqual(sum((v - m) ** 2 for v in tre) / (len(tre) - 1), 9.375, delta=0.8)

    def test_perdite_rare(self):
        q = 0.01
        alto = 0.15 + 1.25 * q / math.sqrt(q * (1 - q))
        basso = 0.15 + 1.25 * (q - 1) / math.sqrt(q * (1 - q))
        valori = [s for r in range(1, 21) for s, _ in P.genera(11, 1, r)]
        self.assertEqual({round(v, 9) for v in valori} <= {round(alto, 9), round(basso, 9)}, True)
        quota_perdite = sum(1 for v in valori if v < 0) / len(valori)
        self.assertAlmostEqual(quota_perdite, q, delta=0.004)


class TestMetodi(unittest.TestCase):
    def test_hac_a_mano(self):
        coppie = [(1.0, 1), (0.0, 0), (2.0, 2), (-1.0, 1), (0.5, 1)]
        mu = 2.5 / 5
        e = [s - mu * k for s, k in coppie]
        D = len(coppie)
        g = [sum(e[d] * e[d - h] for d in range(h, D)) / D for h in range(3)]
        V = g[0] + 2 * (1 - 1 / 3) * g[1] + 2 * (1 - 2 / 3) * g[2]
        se = math.sqrt(V / (D * (5 / D) ** 2))
        z = P.Z
        lo, hi = P.intervallo_hac(coppie, ritardi=2)
        self.assertAlmostEqual(lo, mu - z * se, places=12)
        self.assertAlmostEqual(hi, mu + z * se, places=12)
        self.assertEqual(P.ritardi_predefiniti(1000), 6)

    def test_hac_con_k_medio_diverso_da_uno(self):
        """Aggiunto dopo i mutanti (PI09 e PI20 sopravvissuti, dichiarato): nel caso a mano K medio vale 1, quindi
        K̄² = K̄ non veniva provato; e Z era confrontato con sé stesso."""
        self.assertAlmostEqual(P.Z, 1.959963984540054, places=12)
        coppie = [(1.0, 1), (0.0, 0), (2.0, 2), (-1.0, 1), (0.5, 1), (4.0, 3)]
        D, sk = len(coppie), 8
        mu = 6.5 / sk
        e = [s - mu * k for s, k in coppie]
        g = [sum(e[d] * e[d - h] for d in range(h, D)) / D for h in range(2)]
        V = g[0] + 2 * (1 - 1 / 2) * g[1]
        se = math.sqrt(V / (D * (sk / D) ** 2))
        lo, hi = P.intervallo_hac(coppie, ritardi=1)
        self.assertAlmostEqual(lo, mu - 1.959963984540054 * se, places=12)
        self.assertAlmostEqual(hi, mu + 1.959963984540054 * se, places=12)

    def test_hac_non_stimabile(self):
        self.assertIsNone(P.intervallo_hac([(0.0, 0)] * 10))
        self.assertIsNone(P.intervallo_hac([(1.0, 1)] * 10))                    # varianza nulla

    def test_bootstrap_basic_circolare(self):
        coppie = [(float(i % 7) - 3.0, 1) for i in range(100)]
        a = P.intervallo_bootstrap(coppie, P.flusso(9, 0, 1, 3), ricampionamenti=199, blocco=10)
        b = P.intervallo_bootstrap(coppie, P.flusso(9, 0, 1, 3), ricampionamenti=199, blocco=10)
        self.assertEqual(a, b)
        mu = sum(s for s, _ in coppie) / 100
        lo, hi = a
        self.assertLess(lo, mu)
        self.assertGreater(hi, mu)

    def test_bootstrap_formula_basic_e_ranghi(self):
        """Intervallo basic: [2μ − Q(1−a), 2μ − Q(a)], quantile di rango ⌈p·B⌉ senza interpolazione."""
        coppie = [(float(i % 5), 1) for i in range(50)]
        rnd = P.flusso(9, 0, 2, 3)
        medie = P.medie_bootstrap(coppie, rnd, 99, 10)
        mu = sum(s for s, _ in coppie) / 50
        ordinate = sorted(medie)
        atteso = (2 * mu - ordinate[math.ceil(0.975 * 99) - 1], 2 * mu - ordinate[math.ceil(0.025 * 99) - 1])
        self.assertEqual(P.intervallo_bootstrap(coppie, P.flusso(9, 0, 2, 3), 99, 10), atteso)

    def test_bootstrap_ranghi_su_medie_diverse(self):
        """Aggiunto dopo il primo codice (dichiarato): il caso sopra ha blocchi tutti uguali (periodo 5, blocco 10),
        quindi tutte le medie bootstrap coincidono e i ranghi non vengono provati davvero. Errore mio nel test."""
        coppie = [(float((i * i) % 7) - 2.0, 1 + (i % 3 == 0)) for i in range(53)]
        medie = P.medie_bootstrap(coppie, P.flusso(9, 0, 4, 3), 99, 10)
        self.assertGreater(len(set(medie)), 50)
        o = sorted(medie)
        mu = sum(s for s, _ in coppie) / sum(k for _, k in coppie)
        atteso = (2 * mu - o[96], 2 * mu - o[2])        # rango ⌈0,975·99⌉ = 97 → indice 96; ⌈0,025·99⌉ = 3 → indice 2
        self.assertEqual(P.intervallo_bootstrap(coppie, P.flusso(9, 0, 4, 3), 99, 10), atteso)
        self.assertEqual(len(medie), 99)
        # medie a mano: blocchi circolari di 10 su 53, 5 blocchi
        r = P.flusso(9, 0, 4, 3)
        estese = coppie + coppie[:9]
        for m in medie[:3]:
            ss = kk = 0
            for _ in range(5):
                i = r.randrange(53)
                ss += sum(s for s, _ in estese[i:i + 10])
                kk += sum(k for _, k in estese[i:i + 10])
            self.assertAlmostEqual(m, ss / kk, places=12)

    def test_bootstrap_con_denominatore_nullo_fallisce(self):
        coppie = [(0.0, 0)] * 95 + [(1.0, 1)] * 5
        self.assertIsNone(P.intervallo_bootstrap(coppie, P.flusso(9, 0, 3, 3), 199, 10))


class TestCellaERigaDiComando(unittest.TestCase):
    def test_cella_conteggi_coerenti(self):
        r = P.esegui_cella(1, fase=0, repliche=6, ricampionamenti=99)
        for metodo in ("hac", "bootstrap"):
            m = r[metodo]
            self.assertEqual(m["promosse"] + m["bocciate"] + m["attraversamenti"] + m["errori"], 6)
            self.assertTrue(0 <= m["coperture"] <= 6)
        self.assertEqual(r["cella"], 1)

    def test_cella_uguale_al_calcolo_a_mano(self):
        """Aggiunto dopo il codice (dichiarato): i conteggi della cella devono coincidere con il calcolo a mano sulle
        stesse repliche e sugli stessi flussi (bootstrap sul componente 3). I casi scelti contengono promozioni,
        bocciature, attraversamenti e limiti tra 0,10 e 0,15, e intervalli che mancano μ da sopra e da sotto."""
        visti = {"pro": 0, "boc": 0, "fra": 0, "sopra": 0, "sotto": 0}
        for cella in (1, 7):
            mu = P.CELLE[cella][1]
            r = P.esegui_cella(cella, fase=0, repliche=40, ricampionamenti=99)
            for metodo in ("hac", "bootstrap"):
                atteso = {"promosse": 0, "bocciate": 0, "attraversamenti": 0, "errori": 0, "coperture": 0}
                for k in range(1, 41):
                    g = P.genera(cella, 0, k)
                    iv = P.intervallo_hac(g) if metodo == "hac" else \
                        P.intervallo_bootstrap(g, P.flusso(0, cella, k, 3), 99)
                    lo, hi = iv
                    if lo > 0.15:
                        atteso["promosse"] += 1
                    elif hi < 0.15:
                        atteso["bocciate"] += 1
                    else:
                        atteso["attraversamenti"] += 1
                    atteso["coperture"] += lo <= mu <= hi
                    visti["pro"] += lo > 0.15
                    visti["boc"] += hi < 0.15
                    visti["fra"] += 0.10 <= lo <= 0.15
                    visti["sopra"] += lo > mu
                    visti["sotto"] += hi < mu
                self.assertEqual({c: r[metodo][c] for c in atteso}, atteso, msg=(cella, metodo))
        self.assertTrue(all(v > 0 for v in visti.values()), visti)

    def test_riga_di_comando_ridotta(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(P.main(["--fase", "0", "--repliche", "3", "--ricampionamenti", "99", "--celle", "1,11",
                                     "--processi", "1"]), 0)
        testo = buf.getvalue()
        self.assertIn("NON è il pilota", testo)
        self.assertIn("Clopper", testo)
        self.assertIn("hac", testo)
        self.assertIn("bootstrap", testo)


if __name__ == "__main__":
    unittest.main()
