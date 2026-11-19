"""Test del modulo del verdetto D-31 (D-34 … D-37), scritti PRIMA del codice (19/11/2026). Solo numeri inventati.

Che cosa deve fare `brain/laboratorio/verdetto/verdetto_d31.py`:
- `segnale(iv)`: «favorevole» se L > +0,20 R; «sfavorevole» se U < +0,10 R; «inconclusivo» altrimenti; «invalido» per un
  intervallo mancante, non finito, invertito o di ampiezza nulla (contratto di DGS-06, `pilota_ia02.intervallo_valido`).
  L'uguaglianza non attraversa la soglia (DGS-10 testo I).
- `vicini(L, U)`: gli estremi a meno di 1e-9 R dalla loro soglia, riportati a parte; non cambiano il segnale.
- `controlla_coppie(coppie)`: coppie giornaliere (S_d, K_d) con S finito, K intero ≥ 0 (non bool), S = 0 se K = 0.
- `minimi_mancanti(coppie)`: D = 1.000 sedute esatte, almeno 300 trade, almeno 200 sedute con trade (D-37).
- `intervallo(coppie, seme)`: l'implementazione di riferimento collaudata (`pilota_ia02.intervallo_bootstrap`, B = 3.999,
  blocchi da 10, quota 2,5%) con `random.Random(seme)`; si rifiuta se l'impronta del pilota non è quella congelata.
- `verdetto(coppie, seme, requisiti)`: tre esiti con la tabella delle priorità di DGS-10 §4 opzione 2 (D-35).
- `screening(coppie, seme, potenza_stimata)`: D-36: media > +0,25 R, L > 0, potenza stimata ≥ 50%.
- `veto_blocchi(coppie, soglia, minimo_trade_blocco, ampiezza=250)`: veto per blocchi di D-37; soglia e minimo li fissa
  la scheda (nessun valore predefinito).
Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_verdetto_d31
"""
import random
import sys
import unittest
from pathlib import Path
from unittest import mock

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.laboratorio.studi import pilota_ia02 as P                    # noqa: E402
from brain.laboratorio.verdetto import verdetto_d31 as V               # noqa: E402


def costanti(media, n=1000, delta=0.1):
    """n sedute con un trade: media ± delta alternati in ordine casuale fisso (varianza piccola, media esatta)."""
    s = [media + delta] * (n // 2) + [media - delta] * (n - n // 2)
    random.Random(7).shuffle(s)
    return [(x, 1) for x in s]


def gaussiane(media, sd, n=1000, seme=3):
    r = random.Random(seme)
    return [(r.gauss(media, sd), 1) for _ in range(n)]


SU = costanti(0.6)          # chiaramente favorevole
GIU = costanti(-0.3)        # chiaramente sfavorevole
INC = gaussiane(0.15, 1.25)  # intervallo largo attorno a +0,15


class TestCostanti(unittest.TestCase):
    def test_valori_decisi(self):
        self.assertEqual((V.SOGLIA_PROMOZIONE, V.SOGLIA_BOCCIATURA), (0.20, 0.10))
        self.assertEqual((V.D_COLLAUDATO, V.MIN_TRADE, V.MIN_SEDUTE_ATTIVE), (1000, 300, 200))
        self.assertEqual((V.SCREENING_MEDIA, V.SCREENING_POTENZA), (0.25, 0.50))
        self.assertEqual((V.B, V.BLOCCO), (3999, 10))
        self.assertEqual(V.ESITI, ("promossa", "bocciata", "non decidibile"))
        self.assertEqual(V.IMPRONTA_PILOTA, "717e55996b23a4954d69c97722458e30c2499000b5055fdcca4cba29f864b0ee")


class TestSegnale(unittest.TestCase):
    def test_soglie_strette(self):
        self.assertEqual(V.segnale((0.2000001, 0.5)), "favorevole")
        self.assertEqual(V.segnale((0.20, 0.5)), "inconclusivo")
        self.assertEqual(V.segnale((-0.1, 0.0999999)), "sfavorevole")
        self.assertEqual(V.segnale((-0.1, 0.10)), "inconclusivo")
        self.assertEqual(V.segnale((0.16, 0.19)), "inconclusivo")          # tutto sopra 0,15 ma senza attraversare

    def test_invalidi(self):
        for iv in (None, (0.3, 0.3), (0.5, 0.4), (float("nan"), 1.0), (0.0, float("inf")), (float("-inf"), 0.0)):
            self.assertEqual(V.segnale(iv), "invalido", iv)

    def test_vicini(self):
        self.assertEqual(V.vicini(0.2 + 5e-10, 0.5), ["L"])
        self.assertEqual(V.vicini(0.2 - 5e-10, 0.1 + 5e-10), ["L", "U"])
        self.assertEqual(V.vicini(0.2 + 2e-9, 0.1 - 2e-9), [])
        self.assertEqual(V.vicini(0.0, 0.1 - 5e-10), ["U"])


class TestCoppie(unittest.TestCase):
    def test_coppie_valide(self):
        V.controlla_coppie([(0.0, 0), (1.5, 2), (-1, 1)])

    def test_coppie_non_valide(self):
        for c in ([(0.5, 0)], [(float("nan"), 1)], [(float("inf"), 1)], [(1.0, -1)], [(1.0, 1.0)], [(1.0, True)],
                  [("1", 1)], [(1.0,)], []):
            with self.assertRaises(ValueError, msg=c):
                V.controlla_coppie(c)

    def test_minimi(self):
        self.assertEqual(V.minimi_mancanti(SU), [])
        self.assertTrue(V.minimi_mancanti(SU[:999])[0].startswith("sedute"))
        pochi = [(0.5, 1)] * 299 + [(0.0, 0)] * 701
        self.assertEqual(len(V.minimi_mancanti(pochi)), 2)                  # 299 trade e 299 sedute attive
        self.assertTrue(any(m.startswith("trade") for m in V.minimi_mancanti(pochi)))
        concentrati = [(1.0, 2)] * 199 + [(0.0, 0)] * 801                     # 398 trade in 199 sedute
        self.assertEqual(len(V.minimi_mancanti(concentrati)), 1)
        self.assertTrue(V.minimi_mancanti(concentrati)[0].startswith("sedute con trade"))
        giusti = [(1.0, 2)] * 100 + [(0.5, 1)] * 100 + [(0.0, 0)] * 800     # 300 trade, 200 sedute attive
        self.assertEqual(V.minimi_mancanti(giusti), [])


class TestIntervallo(unittest.TestCase):
    def test_usa_il_riferimento_con_il_seme(self):
        self.assertEqual(V.intervallo(INC, 11), P.intervallo_bootstrap(INC, random.Random(11), 3999, 10))
        self.assertNotEqual(V.intervallo(INC, 11), V.intervallo(INC, 12))

    def test_impronta_diversa_rifiutata(self):
        with mock.patch.object(P, "impronta_modulo", return_value="0" * 64):
            with self.assertRaises(RuntimeError):
                V.intervallo(INC, 11)


class TestVerdetto(unittest.TestCase):
    def test_promossa(self):
        v = V.verdetto(SU, 5)
        self.assertEqual(v["esito"], "promossa")
        self.assertEqual((v["L"], v["U"]), P.intervallo_bootstrap(SU, random.Random(5), 3999, 10))
        self.assertAlmostEqual(v["media"], 0.6, places=12)
        self.assertEqual((v["sedute"], v["trade"], v["sedute_attive"], v["seme"]), (1000, 1000, 1000, 5))
        self.assertEqual(v["impronta_pilota"], V.IMPRONTA_PILOTA)
        self.assertEqual(v["vicini_soglia"], [])

    def test_bocciata_statistica(self):
        v = V.verdetto(GIU, 5)
        self.assertEqual((v["esito"], v["causa"][:10]), ("bocciata", "statistica"))
        nv = [{"id": "costi", "veto": False, "esito": "non valutabile"}]
        self.assertEqual(V.verdetto(GIU, 5, nv)["esito"], "bocciata")

    def test_inconclusivo(self):
        v = V.verdetto(INC, 5)
        self.assertEqual(V.segnale((v["L"], v["U"])), "inconclusivo")
        self.assertEqual(v["esito"], "non decidibile")
        self.assertIn("inconclusiv", v["causa"])

    def test_veto_ha_la_precedenza(self):
        veto = [{"id": "ok", "veto": False, "esito": "superato"}, {"id": "blocchi", "veto": True, "esito": "fallito"}]
        self.assertEqual((V.verdetto(SU, 5, veto)["esito"], V.verdetto(SU, 5, veto)["causa"]), ("bocciata", "veto: blocchi"))
        self.assertEqual(V.verdetto(SU[:999], 5, veto)["esito"], "bocciata")       # anche senza i minimi generali
        self.assertEqual(V.verdetto([(0.5, 0)] * 1000, 5, veto)["esito"], "bocciata")  # e con dati inidonei

    def test_veto_non_accertato_non_boccia(self):
        nv = [{"id": "blocchi", "veto": True, "esito": "non valutabile"}]
        v = V.verdetto(SU, 5, nv)
        self.assertEqual(v["esito"], "non decidibile")
        self.assertIn("blocchi", v["causa"])

    def test_requisito_fallito_senza_veto_non_boccia(self):
        r = [{"id": "drawdown", "veto": False, "esito": "fallito"}]
        v = V.verdetto(SU, 5, r)
        self.assertEqual(v["esito"], "non decidibile")
        self.assertIn("drawdown", v["causa"])

    def test_requisiti_superati(self):
        r = [{"id": "a", "veto": False, "esito": "superato"}, {"id": "b", "veto": True, "esito": "superato"}]
        self.assertEqual(V.verdetto(SU, 5, r)["esito"], "promossa")

    def test_minimi_e_dati(self):
        v = V.verdetto(SU[:999], 5)
        self.assertEqual(v["esito"], "non decidibile")
        self.assertTrue(v["causa"].startswith("minimi"))
        self.assertIsNone(v["L"])
        v = V.verdetto([(0.5, 0)] * 1000, 5)
        self.assertEqual(v["esito"], "non decidibile")
        self.assertTrue(v["causa"].startswith("dati inidonei"))

    def test_intervallo_invalido(self):
        v = V.verdetto([(0.5, 1)] * 1000, 5)                                  # tutte uguali: ampiezza nulla
        self.assertEqual((v["esito"], v["causa"]), ("non decidibile", "intervallo invalido"))

    def test_requisiti_malformati(self):
        for r in ([{"id": "a", "veto": False, "esito": "boh"}], [{"id": "a", "esito": "superato"}],
                  [{"veto": True, "esito": "fallito"}], [{"id": "a", "veto": 1, "esito": "fallito"}]):
            with self.assertRaises(ValueError, msg=r):
                V.verdetto(SU, 5, r)

    def test_vicini_riportati(self):
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.2 + 5e-10, 0.6)):
            v = V.verdetto(SU, 5)
        self.assertEqual((v["esito"], v["vicini_soglia"]), ("promossa", ["L"]))


class TestScreening(unittest.TestCase):
    def test_ammessa(self):
        s = V.screening(costanti(0.6, 780), 9, 0.50)                       # potenza 50% inclusa
        self.assertTrue(s["ammessa"])
        self.assertEqual(s["cause"], [])
        self.assertEqual((s["L"], s["U"]), P.intervallo_bootstrap(costanti(0.6, 780), random.Random(9), 3999, 10))

    def test_potenza_insufficiente(self):
        s = V.screening(costanti(0.6, 780), 9, 0.4999)
        self.assertFalse(s["ammessa"])
        self.assertEqual(len(s["cause"]), 1)
        self.assertIn("potenza", s["cause"][0])

    def test_media_uguale_alla_soglia_non_passa(self):
        s = V.screening(costanti(0.25, 780, 0.25), 9, 0.9)                  # media esattamente 0,25
        self.assertEqual(s["media"], 0.25)
        self.assertFalse(s["ammessa"])
        self.assertTrue(any("media" in c for c in s["cause"]))

    def test_limite_non_positivo(self):
        s = V.screening(costanti(0.30, 780, 6.0), 9, 0.9)                   # media alta ma dispersione enorme
        self.assertLessEqual(s["L"], 0)
        self.assertEqual(s["cause"], [s["cause"][0]])
        self.assertIn("limite", s["cause"][0])

    def test_casi_degeneri(self):
        self.assertFalse(V.screening([(0.0, 0)] * 780, 9, 0.9)["ammessa"])
        self.assertFalse(V.screening([(0.5, 1)] * 780, 9, 0.9)["ammessa"])  # intervallo invalido
        for p in (-0.1, 1.1, float("nan"), "0.5", None):
            with self.assertRaises(ValueError, msg=p):
                V.screening(costanti(0.6, 780), 9, p)
        with self.assertRaises(ValueError):
            V.screening([(0.5, 0)] * 780, 9, 0.9)


class TestVetoBlocchi(unittest.TestCase):
    def blocchi(self, medie, trade=(1, 1, 1, 1)):
        coppie = []
        for m, k in zip(medie, trade):
            coppie += [(m * k, k)] * 250
        return coppie

    def test_esiti(self):
        r = V.veto_blocchi(self.blocchi((0.3, 0.2, -0.3, 0.4)), -0.25, 50)
        self.assertEqual((r["id"], r["veto"], r["esito"]), ("blocchi", True, "fallito"))
        self.assertEqual([round(x, 12) for x in r["medie"]], [0.3, 0.2, -0.3, 0.4])
        self.assertEqual(V.veto_blocchi(self.blocchi((0.3, 0.2, -0.2, 0.4)), -0.25, 50)["esito"], "superato")
        self.assertEqual(V.veto_blocchi(self.blocchi((0.3, 0.2, -0.25, 0.4)), -0.25, 50)["esito"], "superato")

    def test_blocchi_con_pochi_trade(self):
        sottile = self.blocchi((0.3, 0.2, 0.1, 0.4))
        sottile[500:750] = [(0.1, 1)] * 40 + [(0.0, 0)] * 210
        r = V.veto_blocchi(sottile, -0.25, 50)
        self.assertEqual(r["esito"], "non valutabile")
        self.assertIsNone(r["medie"][2] if sum(k for _, k in sottile[500:750]) == 0 else None)
        sottile[0:250] = [(-0.5, 1)] * 250                                    # un blocco valido molto negativo
        self.assertEqual(V.veto_blocchi(sottile, -0.25, 50)["esito"], "fallito")
        vuoto = self.blocchi((0.3, 0.2, 0.1, 0.4))
        vuoto[250:500] = [(0.0, 0)] * 250
        r = V.veto_blocchi(vuoto, -0.25, 50)
        self.assertEqual((r["esito"], r["medie"][1]), ("non valutabile", None))
        self.assertEqual(V.veto_blocchi(self.blocchi((0.3, 0.2, 0.1, 0.4)), -0.25, 250)["esito"], "superato")
        self.assertEqual(V.veto_blocchi(self.blocchi((0.3, 0.2, 0.1, 0.4)), -0.25, 251)["esito"], "non valutabile")

    def test_parametri(self):
        b = self.blocchi((0.3, 0.2, 0.1, 0.4))
        for args in ((b[:999], -0.25, 50), (b, float("nan"), 50), (b, -0.25, 0), (b, -0.25, 1.5), (b, "x", 50)):
            with self.assertRaises(ValueError, msg=args[1:]):
                V.veto_blocchi(*args)
        self.assertEqual(len(V.veto_blocchi(b[:500], -0.25, 50, ampiezza=100)["medie"]), 5)


if __name__ == "__main__":
    unittest.main()
