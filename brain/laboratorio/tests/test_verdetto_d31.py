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
import hashlib
import json
import random
import sys
import tempfile
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

    def test_ampiezza_minima_119(self):
        """#119 (D-44): un intervallo più stretto di 1e-9 R è degenere (arrotondamento su dati quasi costanti)."""
        self.assertEqual(V.AMPIEZZA_MINIMA, 1e-9)
        self.assertEqual(V.segnale((0.3, 0.3 + 5e-10)), "invalido")
        self.assertEqual(V.segnale((0.3, 0.3 + 1e-13)), "invalido")
        self.assertEqual(V.segnale((0.3, 0.3 + 2e-9)), "favorevole")
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.25, 0.25 + 1e-13)):
            v = V.verdetto(SU, 5)
        self.assertEqual((v["esito"], v["causa"]), ("non decidibile", "intervallo invalido"))
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.30, 0.30 + 1e-13)):
            s = V.screening(costanti(0.6, 780), 9, 0.9)
        self.assertIn("intervallo invalido", s["cause"])

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
        self.assertEqual(len(V.minimi_mancanti(pochi)), 1)                  # 299 trade (299 sedute attive bastano)
        self.assertTrue(V.minimi_mancanti(pochi)[0].startswith("trade"))     # errore di Claude nel test rosso: «2»
        self.assertEqual(len(V.minimi_mancanti([(0.5, 1)] * 199 + [(0.0, 0)] * 801)), 2)
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
        v = V.verdetto(SU, 5, contesto=CTX)                                   # #133: si promuove solo con N
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
        self.assertEqual(V.verdetto(SU, 5, r, contesto=CTX)["esito"], "promossa")

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
            v = V.verdetto(SU, 5, contesto=CTX)
        self.assertEqual((v["esito"], v["vicini_soglia"]), ("promossa", ["L"]))


    def test_media_per_trade_non_per_seduta(self):
        coppie = [(1.2, 2)] * 400 + [(0.0, 0)] * 600                       # 800 trade in 1.000 sedute: 0,6 a trade
        # (errore di Claude: con 500 sedute da 2 trade il test non distingueva trade e sedute; VD26 sopravviveva)
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.3, 0.9)):
            v = V.verdetto(coppie, 5)
        self.assertAlmostEqual(v["media"], 0.6, places=12)
        self.assertEqual((v["trade"], v["sedute_attive"]), (800, 400))


class TestScreening(unittest.TestCase):
    def test_limite_zero_non_passa_e_media_per_trade(self):
        coppie = [(1.2, 2)] * 300 + [(0.0, 0)] * 480                       # 600 trade in 780 sedute (VD35, stesso errore)
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.0, 0.9)):
            s = V.screening(coppie, 9, 0.9)
        self.assertAlmostEqual(s["media"], 0.6, places=12)
        self.assertEqual(s["cause"], ["limite inferiore non > 0"])

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


class TestRuoliESegnale(unittest.TestCase):
    """DGS-12 §3 e §4 (21/11/2026): ruoli dei requisiti tipizzati (veto, vincolante per promuovere, descrittivo) e
    segnale del solo metro riportato a parte, anche quando l'esito è deciso da un veto."""

    def test_descrittivo_non_cambia_l_esito(self):
        for esito in ("superato", "fallito", "non valutabile"):
            r = [{"id": "dd", "veto": False, "descrittivo": True, "esito": esito}]
            self.assertEqual(V.verdetto(SU, 5, r, contesto=CTX)["esito"], "promossa", esito)
            self.assertEqual(V.verdetto(GIU, 5, r)["esito"], "bocciata", esito)

    def test_ruoli_registrati(self):
        r = [{"id": "a", "veto": True, "esito": "superato"}, {"id": "b", "veto": False, "esito": "superato"},
             {"id": "c", "veto": False, "descrittivo": True, "esito": "fallito"},
             {"id": "d", "veto": False, "descrittivo": False, "esito": "superato"}]
        v = V.verdetto(SU, 5, r, contesto=CTX)
        self.assertEqual(v["requisiti"], [{"id": "a", "ruolo": "veto", "esito": "superato"},
                                          {"id": "b", "ruolo": "promozione", "esito": "superato"},
                                          {"id": "c", "ruolo": "descrittivo", "esito": "fallito"},
                                          {"id": "d", "ruolo": "promozione", "esito": "superato"}])
        self.assertEqual(v["esito"], "promossa")
        self.assertEqual(V.verdetto(SU, 5)["requisiti"], [])

    def test_ruoli_malformati(self):
        for r in ([{"id": "a", "veto": True, "descrittivo": True, "esito": "fallito"}],
                  [{"id": "a", "veto": False, "descrittivo": 1, "esito": "fallito"}],
                  [{"id": "a", "veto": False, "descrittivo": None, "esito": "fallito"}]):
            with self.assertRaises(ValueError, msg=r):
                V.verdetto(SU, 5, r)

    def test_segnale_riportato(self):
        self.assertEqual(V.verdetto(SU, 5)["segnale"], "favorevole")
        self.assertEqual(V.verdetto(GIU, 5)["segnale"], "sfavorevole")
        self.assertEqual(V.verdetto(INC, 5)["segnale"], "inconclusivo")
        self.assertEqual(V.verdetto([(0.5, 1)] * 1000, 5)["segnale"], "invalido")
        self.assertIsNone(V.verdetto(SU[:999], 5)["segnale"])
        self.assertIsNone(V.verdetto([(0.5, 0)] * 1000, 5)["segnale"])

    def test_veto_con_segnale_e_media(self):
        veto = [{"id": "blocchi", "veto": True, "esito": "fallito"}]
        v = V.verdetto(SU, 5, veto)
        self.assertEqual((v["esito"], v["causa"], v["segnale"]), ("bocciata", "veto: blocchi", "favorevole"))
        self.assertAlmostEqual(v["media"], 0.6, places=12)
        self.assertEqual((v["L"], v["U"]), P.intervallo_bootstrap(SU, random.Random(5), 3999, 10))
        self.assertEqual((v["trade"], v["sedute_attive"]), (1000, 1000))
        v = V.verdetto(SU[:999], 5, veto)
        self.assertEqual((v["esito"], v["segnale"], v["trade"]), ("bocciata", None, 999))
        v = V.verdetto([(0.5, 0)] * 1000, 5, veto)
        self.assertEqual((v["esito"], v["segnale"], v["trade"], v["media"]), ("bocciata", None, None, None))

    def test_rapporto_segnale_e_requisiti(self):
        r = [{"id": "blocchi", "veto": True, "esito": "fallito"},
             {"id": "dd", "veto": False, "descrittivo": True, "esito": "fallito"}]
        testo = V.rapporto(V.verdetto(SU, 5, r))
        self.assertIn("segnale del solo metro: favorevole", testo)
        self.assertIn("requisito blocchi [veto]: fallito", testo)
        self.assertIn("requisito dd [descrittivo, non cambia l'esito]: fallito", testo)
        self.assertIn("segnale del solo metro: non calcolato", V.rapporto(V.verdetto(SU[:999], 5)))

    def test_blocchi_con_esiti_ignoti(self):
        base = [(0.3, 1)] * 1000
        ignota = list(base)
        ignota[600] = (None, 1)
        r = V.veto_blocchi(ignota, -0.25, 50)
        self.assertEqual((r["esito"], r["medie"][2]), ("non valutabile", None))
        self.assertEqual(round(r["medie"][0], 12), 0.3)    # (errore di Claude: senza arrotondamento falliva su 3.9, #124)
        ignota[0:250] = [(-0.5, 1)] * 250                                     # un blocco completo e negativo
        self.assertEqual(V.veto_blocchi(ignota, -0.25, 50)["esito"], "fallito")
        negativo_ignoto = [(-0.5, 1)] * 249 + [(None, 1)] + base[250:]           # l'ignota è nel blocco decisivo
        self.assertEqual(V.veto_blocchi(negativo_ignoto, -0.25, 50)["esito"], "non valutabile")
        for cattiva in ((None, 0), (None, 1.5), (float("nan"), 1), (0.5, 0)):
            c = list(base)
            c[3] = cattiva
            with self.assertRaises(ValueError, msg=cattiva):
                V.veto_blocchi(c, -0.25, 50)
        with self.assertRaises(ValueError):
            V.controlla_coppie(base[:999] + [(None, 1)])               # il verdetto resta severo sui dati


CTX = {"registro": "registro_prove.json", "n_prove": 3, "impronta": "ab" * 32}   # N valido per le promozioni


class TestRevisioneR18(unittest.TestCase):
    """Primo giro di revisione del modulo (Gemini R18, D-34): #131, #132, #133, #134."""

    def test_131_intervallo_invalido_non_e_una_stima(self):
        for iv in ((0.25, 0.25 + 1e-13), (0.2 + 5e-10, 0.2 + 9e-10)):
            with mock.patch.object(P, "intervallo_bootstrap", return_value=iv):
                v = V.verdetto(SU, 5, contesto=CTX)
            self.assertEqual((v["esito"], v["causa"], v["segnale"]), ("non decidibile", "intervallo invalido",
                                                                     "invalido"))
            self.assertEqual((v["L"], v["U"], v["vicini_soglia"]), (None, None, []))
            self.assertEqual(v["intervallo_scartato"], iv)
            testo = V.rapporto(v)
            self.assertIn("NON STIMABILE", testo)
            self.assertNotIn("valido nel dominio", testo)
            self.assertIn("intervallo scartato", testo)
        self.assertIsNone(V.verdetto(SU, 5, contesto=CTX)["intervallo_scartato"])

    def test_132_seme_intero_obbligatorio(self):
        for seme in (None, 1.0, True, "5"):
            with self.assertRaises(ValueError, msg=seme):
                V.verdetto(SU, seme)
            with self.assertRaises(ValueError, msg=seme):
                V.screening(SU, seme, 0.6)
            with self.assertRaises(ValueError, msg=seme):
                V.intervallo(SU, seme)

    def test_132_seme_controllato_anche_senza_bootstrap(self):        # per i mutanti VD96 e VD97
        with self.assertRaises(ValueError):
            V.verdetto(SU[:999], None)                                           # minimi mancanti: niente bootstrap
        with self.assertRaises(ValueError):
            V.screening([(0.0, 0)] * 1000, None, 0.6)                            # nessun trade: niente bootstrap

    def test_134_sedute_non_misurabili_dette_tali(self):                  # per il mutante VD112
        testo = V.rapporto(V.verdetto((x for x in SU), 5))
        self.assertIn("- sedute: — sedute [MISURA] · incertezza: NON DISPONIBILE", testo)

    def test_133_contesto_controllato(self):
        for cattivo in ({"registro": "r.json", "n_prove": -5, "impronta": "ab" * 32},
                        {"registro": "r.json", "n_prove": True, "impronta": "ab" * 32},
                        {"registro": "r.json", "n_prove": 3, "impronta": "0"},
                        {"registro": "r.json", "n_prove": 3, "impronta": "AB" * 32},
                        {"registro": "", "n_prove": 3, "impronta": "ab" * 32},
                        {"registro": "r.json", "n_prove": 3},
                        dict(CTX, altro=1), "N=3", ["r", 3, "ab" * 32]):
            with self.assertRaises(ValueError, msg=cattivo):
                V.verdetto(SU, 5, contesto=cattivo)

    def test_133_promossa_solo_con_n(self):
        v = V.verdetto(SU, 5)
        self.assertEqual(v["segnale"], "favorevole")
        self.assertEqual(v["esito"], "non decidibile")
        self.assertIn("N non fornito", v["causa"])
        self.assertEqual(V.verdetto(SU, 5, contesto=CTX)["esito"], "promossa")
        self.assertEqual(V.verdetto(GIU, 5)["esito"], "bocciata")                    # bocciare non richiede N

    def test_133_registro_collegato_rifiutato(self):
        with tempfile.TemporaryDirectory() as d:
            vero = Path(d) / "vero.json"
            vero.write_text("{}", encoding="utf-8")
            link = Path(d) / "registro_prove.json"
            link.symlink_to(vero)
            with self.assertRaises(ValueError) as e:
                V.contesto_prove(link)
            self.assertIn("collegamento simbolico", str(e.exception))
            ereditato = Path(d) / "trial_registry.json"
            ereditato.write_text("{}", encoding="utf-8")
            alias = Path(d) / "alias.json"
            alias.symlink_to(ereditato)
            with self.assertRaises(ValueError):
                V.contesto_prove(alias)

    def test_134_tipi_rifiutati(self):
        with self.assertRaises(ValueError):
            V.controlla_coppie([(True, 1)] + SU[1:])
        with self.assertRaises(ValueError):
            V.screening(SU, 5, True)
        b = [(0.3, 1)] * 1000
        for args in ((b, True, 50), (b, -0.25, 50, True)):
            with self.assertRaises(ValueError, msg=args[1:]):
                V.veto_blocchi(*args)
        with self.assertRaises(ValueError):
            V.verdetto(SU, 5, [{"id": 5, "veto": False, "esito": "superato"}])

    def test_soglia_infinita_rifiutata_anche_con_blocchi_sottili(self):   # mutante VD44 (dopo le frazioni)
        for soglia in (float("inf"), float("-inf"), float("nan")):
            for minimo in (1, 10_000):                                      # blocchi valutati o tutti sottili
                with self.assertRaises(ValueError, msg=(soglia, minimo)):
                    V.veto_blocchi(costanti(0.6, 250), soglia, minimo)

    def test_134_errore_indica_la_seduta(self):                           # per il mutante VD10
        for cattivo in (float("nan"), float("inf")):
            c = list(SU)
            c[7] = (cattivo, 1)
            with self.assertRaises(ValueError) as e:
                V.controlla_coppie(c)
            self.assertIn("seduta 7", str(e.exception))

    def test_134_coppie_non_in_lista_e_somme_enormi(self):
        with self.assertRaises(ValueError):
            V.controlla_coppie(x for x in SU)
        v = V.verdetto((x for x in SU), 5)
        self.assertEqual(v["esito"], "non decidibile")
        self.assertTrue(v["causa"].startswith("dati inidonei"))
        v = V.verdetto([(1e308, 1)] * 1000, 5)
        self.assertEqual((v["esito"], v["media"]), ("non decidibile", None))
        self.assertTrue(v["causa"].startswith("dati inidonei"))

    def test_134_banda_dei_vicini_con_tipo(self):
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.2 + 5e-10, 0.6)):
            testo = V.rapporto(V.verdetto(SU, 5, contesto=CTX))
        self.assertIn("estremi a meno di 1e-9 R [REGOLA] dalla soglia", testo)


class TestContestoProve(unittest.TestCase):
    """D-34 punto 2 (registro unico di N) e DGS-11 §6: N deve venire dal registro canonico e restare nel rapporto.
    Scritti PRIMA del codice (20/11/2026)."""

    def registro(self, nome="registro_prove.json", prove=None, schema="registro-prove/1"):
        d = Path(tempfile.mkdtemp())
        f = d / nome
        prove = prove if prove is not None else [{"ruolo": "selezionabile"}] * 3 + [{"ruolo": "esplorazione"}]
        f.write_text(json.dumps({"schema": schema, "prove": prove, "sigilli": [], "esecuzioni": []}))
        return f

    def test_legge_n_e_impronta(self):
        f = self.registro()
        c = V.contesto_prove(f)
        self.assertEqual(c, {"registro": "registro_prove.json", "n_prove": 3,
                             "impronta": hashlib.sha256(f.read_bytes()).hexdigest()})

    def test_registri_ereditati_rifiutati(self):
        self.assertEqual(V.REGISTRI_EREDITATI, ("trial_registry.json", "trial_registry_xauusd.json"))
        for nome in V.REGISTRI_EREDITATI:
            with self.assertRaises(ValueError, msg=nome):
                V.contesto_prove(self.registro(nome))

    def test_registro_assente_o_malformato(self):
        with self.assertRaises(ValueError):
            V.contesto_prove(Path(tempfile.mkdtemp()) / "registro_prove.json")
        with self.assertRaises(ValueError):
            V.contesto_prove(self.registro(schema="altro/9"))

    def test_registro_cambiato_durante_la_lettura(self):
        f = self.registro()
        originale = V.S.leggi

        def leggi_e_cambia(x):
            dati = originale(x)
            f.write_text(f.read_text() + " ")
            return dati
        with mock.patch.object(V.S, "leggi", side_effect=leggi_e_cambia):
            with self.assertRaises(ValueError):
                V.contesto_prove(f)

    def test_contesto_e_quota_nel_verdetto(self):
        c = V.contesto_prove(self.registro())
        v = V.verdetto(SU, 5, contesto=c)
        self.assertEqual((v["contesto_prove"], v["quota"]), (c, 0.025))
        self.assertIsNone(V.verdetto(SU, 5)["contesto_prove"])
        self.assertEqual(V.verdetto([(0.5, 0)] * 1000, 5, contesto=c)["contesto_prove"], c)  # anche se non decidibile

    def test_quota_fuori_collaudo_rifiutata(self):
        self.assertEqual(V.QUOTA, 0.025)
        class Q(float):
            pass
        for q in (0.0125, 0.008333, 0.05, 0, "0.025", None, Q(0.025)):   # Q: aggiunto per il mutante VD55
            with self.assertRaises(ValueError, msg=q):
                V.verdetto(SU, 5, quota=q)

    def test_nessun_uso_dei_registri_ereditati(self):
        """Statico: il verdetto e il perimetro di esecuzione non leggono i registri di Binario B
        e non istanziano il calcolatore del DSR (che li userebbe)."""
        cartelle = [repo_root / "brain/laboratorio/verdetto", repo_root / "brain/laboratorio/esecuzione"]
        for c in cartelle:
            for f in sorted(c.glob("*.py")):
                testo = f.read_text(encoding="utf-8")
                if f.name != "verdetto_d31.py":
                    self.assertNotIn("trial_registry", testo, f.name)
                self.assertNotIn("DSRCalculator(", testo, f.name)


class TestRapportoTipizzato(unittest.TestCase):
    """D-34 punto 4 (audit I2, MODELLO-EPISTEMICO §3-§4): ogni numero del rapporto ha tipo, incertezza e fonte;
    misure, derivati e regole prima delle stime; la decisione resta del titolare. Scritti PRIMA del codice (20/11/2026)."""

    def setUp(self):
        self.c = {"registro": "registro_prove.json", "n_prove": 7, "impronta": "ab" * 32}
        self.v = V.verdetto(SU, 5, contesto=self.c)

    def voce(self, voci, etichetta):
        trovate = [x for x in voci if x["etichetta"] == etichetta]
        self.assertEqual(len(trovate), 1, etichetta)
        return trovate[0]

    def test_campi_obbligatori_e_tipi(self):
        self.assertEqual(V.TIPI, ("MISURA", "DERIVATO", "STIMA", "IPOTESI", "REGOLA"))
        voci = V.voci_rapporto(self.v)
        self.assertGreaterEqual(len(voci), 8)
        for x in voci:
            self.assertEqual(set(x), {"etichetta", "valore", "unita", "tipo", "incertezza", "fonte"}, x)
            self.assertIn(x["tipo"], V.TIPI)
            self.assertTrue(x["incertezza"] and x["fonte"], x)

    def test_misure_derivati_e_stima(self):
        voci = V.voci_rapporto(self.v)
        for e in ("sedute", "trade", "sedute con trade"):
            self.assertEqual(self.voce(voci, e)["tipo"], "MISURA")
        m = self.voce(voci, "media del campione")
        self.assertEqual((m["tipo"], m["unita"]), ("DERIVATO", "R a trade"))
        self.assertAlmostEqual(m["valore"], 0.6, places=12)
        st = self.voce(voci, "vantaggio della strategia")
        self.assertEqual(st["tipo"], "STIMA")
        self.assertEqual(st["valore"], (self.v["L"], self.v["U"]))
        for pezzo in ("bootstrap", "basic", "B = 3999", "blocchi da 10", "seme 5", "2,5%"):
            self.assertIn(pezzo, st["incertezza"])

    def test_regole_e_registro(self):
        voci = V.voci_rapporto(self.v)
        r = self.voce(voci, "soglie del metro")
        self.assertEqual((r["tipo"], r["valore"]), ("REGOLA", (0.20, 0.10)))
        self.assertIn("D-31", r["fonte"])
        q = self.voce(voci, "quota")
        self.assertEqual((q["tipo"], q["valore"]), ("REGOLA", 0.025))
        n = self.voce(voci, "prove nel registro (N)")
        self.assertEqual((n["tipo"], n["valore"]), ("MISURA", 7))
        self.assertIn("abababab", n["fonte"])

    def test_ordine_misure_prima_delle_stime(self):
        voci = V.voci_rapporto(self.v)
        tipi = [x["tipo"] for x in voci]
        primo_stima = tipi.index("STIMA")
        self.assertTrue(all(t != "STIMA" for t in tipi[:primo_stima]))
        self.assertTrue(all(t == "STIMA" for t in tipi[primo_stima:]))

    def test_non_stimabile_e_n_mancante(self):
        v = V.verdetto(SU[:999], 5)
        voci = V.voci_rapporto(v)
        st = self.voce(voci, "vantaggio della strategia")
        self.assertEqual((st["valore"], st["incertezza"]), (None, "NON STIMABILE"))
        n = self.voce(voci, "prove nel registro (N)")
        self.assertEqual((n["valore"], n["incertezza"]), (None, "NON FORNITO"))
        testo = V.rapporto(v)
        self.assertIn("NON STIMABILE", testo)
        self.assertIn("NON FORNITO", testo)

    def test_testo(self):
        testo = V.rapporto(self.v)
        righe = testo.splitlines()
        self.assertIn("promossa", righe[0])
        self.assertIn(self.v["causa"], righe[0])
        self.assertIn("decisione resta del titolare", righe[-1])
        for x in V.voci_rapporto(self.v):
            self.assertIn(f"[{x['tipo']}]", testo)
        self.assertIn("0.6000", testo)
        self.assertNotIn("1e-9", testo)

    def test_vicini_nel_testo(self):          # aggiunto per il mutante VD68 (dichiarato)
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.2 + 5e-10, 0.6)):
            v = V.verdetto(SU, 5)
        self.assertIn("1e-9 R [REGOLA] dalla soglia: L", V.rapporto(v))


class TestRapportoScreening(unittest.TestCase):
    """D-34 punto 4 per lo screening (D-36). Scritti PRIMA del codice (20/11/2026)."""

    def setUp(self):
        self.s = V.screening(costanti(0.6, 780), 9, 0.62)

    def voce(self, voci, etichetta):
        trovate = [x for x in voci if x["etichetta"] == etichetta]
        self.assertEqual(len(trovate), 1, etichetta)
        return trovate[0]

    def test_potenza_riportata(self):
        self.assertEqual(self.s["potenza"], 0.62)

    def test_voci(self):
        voci = V.voci_screening(self.s)
        for x in voci:
            self.assertIn(x["tipo"], V.TIPI)
            self.assertTrue(x["incertezza"] and x["fonte"])
        m = self.voce(voci, "media sullo sviluppo")
        self.assertEqual(m["tipo"], "DERIVATO")
        self.assertIn("selezione", m["incertezza"])
        r = self.voce(voci, "soglie dello screening")
        self.assertEqual((r["tipo"], r["valore"]), ("REGOLA", (0.25, 0.0, 0.50)))
        self.assertIn("D-36", r["fonte"])
        p = self.voce(voci, "potenza stimata della verifica")
        self.assertEqual((p["tipo"], p["valore"]), ("STIMA", 0.62))
        st = self.voce(voci, "intervallo sullo sviluppo")
        self.assertEqual((st["tipo"], st["valore"]), ("STIMA", (self.s["L"], self.s["U"])))
        tipi = [x["tipo"] for x in voci]
        i = tipi.index("STIMA")
        self.assertTrue(all(t == "STIMA" for t in tipi[i:]))
        self.assertTrue(all(t != "STIMA" for t in tipi[:i]))

    def test_non_stimabile(self):
        s = V.screening([(0.5, 1)] * 780, 9, 0.9)
        st = self.voce(V.voci_screening(s), "intervallo sullo sviluppo")
        self.assertEqual((st["valore"], st["incertezza"]), (None, "NON STIMABILE"))
        s = V.screening([(0.0, 0)] * 780, 9, 0.9)
        m = self.voce(V.voci_screening(s), "media sullo sviluppo")
        self.assertEqual((m["valore"], m["incertezza"]), (None, "NON DISPONIBILE"))

    def test_testo(self):
        testo = V.rapporto_screening(self.s)
        righe = testo.splitlines()
        self.assertIn("SCREENING D-36", righe[0])
        self.assertIn("ammessa", righe[0])
        no = V.rapporto_screening(V.screening(costanti(0.6, 780), 9, 0.3))
        self.assertIn("NON ammessa", no.splitlines()[0])
        self.assertIn("potenza", no.splitlines()[0])
        self.assertIn("non è una prova", righe[-1])
        for x in V.voci_screening(self.s):
            self.assertIn(f"[{x['tipo']}]", testo)


# Valori inventati per cui la somma compensata di Python ≥ 3.12 NON è la somma esatta arrotondata (math.fsum)
DISCORDI = [-6.91055939135834e+18, 2.9029347063393805e-20, -2.3626325107814694e+17, 9.102538185465903e+18]


def media_esatta(valori, k):
    """Riferimento indipendente: somma esatta in frazioni, arrotondata una volta, poi divisa per k (IEEE)."""
    from fractions import Fraction
    return float(sum(Fraction(x) for x in valori)) / k


class TestSommeEsatte124(unittest.TestCase):
    """#124 (Gemini, notte del 22/11, N22-A1): con sum() la decisione a filo di soglia dipendeva dalla versione di
    Python (su 3.9 falsa ammissione allo screening e falso veto). Le medie del modulo usano la somma esatta."""

    def test_screening_media_esattamente_025_non_passa(self):          # S1
        coppie = [(0.3, 1)] * 125 + [(0.2, 1)] * 125
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.1, 0.4)):
            s = V.screening(coppie, 9, 0.9)
        self.assertEqual(s["media"], 0.25)
        self.assertIn("media 0.2500 non > +0,25 R", s["cause"])

    def test_veto_media_uguale_alla_soglia_non_scatta(self):           # B1, B3
        self.assertEqual(V.veto_blocchi([(0.3, 1)] * 250, 0.3, 1)["esito"], "superato")
        self.assertEqual(V.veto_blocchi([(0.3, 1)] * 250, 0.3, 1)["medie"], [0.3])
        b3 = [(-0.3, 1)] * 125 + [(-0.2, 1)] * 125
        self.assertEqual(V.veto_blocchi(b3, -0.25, 1), {"id": "blocchi", "veto": True, "esito": "superato",
                                                         "medie": [-0.25]})

    def test_medie_uguali_al_riferimento_esatto_su_ogni_versione(self):
        coppie = [(x, 1) for x in DISCORDI]
        atteso = media_esatta(DISCORDI, 4)
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.1, 0.4)):
            self.assertEqual(V.screening(coppie, 9, 0.9)["media"], atteso)
        self.assertEqual(V.veto_blocchi(coppie, 0.0, 1, ampiezza=4)["medie"], [atteso])
        self.assertEqual(V.verdetto(coppie, 5)["media"], atteso)

    def test_limite_inferiore_vicino_a_zero_segnalato(self):           # N22-A2, proposta 3: V3
        coppie = costanti(0.6, 780)
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(4e-16, 0.9)):
            s = V.screening(coppie, 9, 0.9)
        self.assertTrue(s["ammessa"])                                    # non cambia l'esito
        self.assertTrue(s["L_vicino_a_zero"])
        self.assertIn("limite inferiore a meno di 1e-9 R [REGOLA] da 0", V.rapporto_screening(s))
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(-4e-16, 0.9)):
            self.assertTrue(V.screening(coppie, 9, 0.9)["L_vicino_a_zero"])
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(2e-9, 0.9)):
            s = V.screening(coppie, 9, 0.9)
        self.assertFalse(s["L_vicino_a_zero"])
        self.assertNotIn("a meno di 1e-9 R [REGOLA] da 0", V.rapporto_screening(s))
        self.assertFalse(V.screening(costanti(0.6, 780), 9, 0.9)["L_vicino_a_zero"])


class TestConfrontiEsatti124(unittest.TestCase):
    """#124, seconda parte (Gemini, verifica del 22/11, V124-01..06 e M-124-01..04): anche con la somma esatta, il
    quoziente arrotondato può invertire una decisione a filo. Le decisioni si prendono in frazioni esatte; le medie
    riportate sono il quoziente esatto arrotondato una volta sola."""

    def test_d1_screening_media_appena_sopra_la_soglia(self):
        v = [0.25] * 299 + [0.25 + 2 ** -48]                            # media esatta 0,25 + 2^-48/300
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.1, 0.4)):
            s = V.screening([(x, 1) for x in v], 9, 0.9)
        self.assertNotIn("media 0.2500 non > +0,25 R", s["cause"])
        self.assertTrue(s["ammessa"])

    def test_d2_veto_media_appena_sotto_la_soglia(self):
        w = [-0.25] * 249 + [-0.25 - 2 ** -49]
        self.assertEqual(V.veto_blocchi([(x, 1) for x in w], -0.25, 1)["esito"], "fallito")

    def test_d3_serie_costante_uguale_alla_soglia(self):
        for x, k in ((-0.4, 3), (-0.3, 7), (0.1, 3)):
            self.assertEqual(V.veto_blocchi([(x, 1)] * k, x, 1, ampiezza=k)["esito"], "superato", (x, k))

    def test_d4_media_riportata_arrotondata_una_volta(self):
        from fractions import Fraction
        v = [0.25] * 999 + [0.25 + 2 ** -46]
        atteso = float(sum(Fraction(x) for x in v) / 1000)
        self.assertEqual(V.verdetto([(x, 1) for x in v], 5)["media"], atteso)
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.1, 0.4)):
            self.assertEqual(V.screening([(x, 1) for x in v], 9, 0.9)["media"], atteso)
        self.assertEqual(V.veto_blocchi([(x, 1) for x in v], 0.0, 1, ampiezza=1000)["medie"], [atteso])

    def test_d6_finitezza_indipendente_dall_ordine(self):
        # il pilota congelato somma in qualunque ordine (ricampionamenti): conta la somma dei valori assoluti
        for ordine in ([1.5e308, 1.5e308, -1.5e308], [1.5e308, -1.5e308, 1.5e308], [-1.5e308, 1.5e308, 1.5e308]):
            with self.assertRaisesRegex(ValueError, "non è un numero finito"):
                V.controlla_coppie([(x, 1) for x in ordine])
        V.controlla_coppie([(1e307, 1)] * 3)                             # 3e307: finito in ogni ordine

    def test_banda_di_vicinanza_a_zero_dello_screening(self):           # M-124-01, M-124-02
        coppie = costanti(0.6, 780)
        for L, atteso in ((5e-10, True), (-5e-10, True), (1e-9, False), (-1e-9, False), (2e-9, False)):
            with mock.patch.object(P, "intervallo_bootstrap", return_value=(L, 0.9)):
                self.assertEqual(V.screening(coppie, 9, 0.9)["L_vicino_a_zero"], atteso, L)

    def test_vicinanza_falsa_senza_trade_o_con_intervallo_invalido(self):   # M-124-03
        self.assertFalse(V.screening([(0.0, 0)] * 10, 9, 0.9)["L_vicino_a_zero"])
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.0, 0.0)):
            self.assertFalse(V.screening(costanti(0.6, 780), 9, 0.9)["L_vicino_a_zero"])

    def test_riga_del_rapporto_completa(self):                         # M-124-04
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(4e-16, 0.9)):
            s = V.screening(costanti(0.6, 780), 9, 0.9)
        self.assertIn("- limite inferiore a meno di 1e-9 R [REGOLA] da 0 (non cambia l'esito; arrotondamento "
                      "possibile, #124)", V.rapporto_screening(s))


if __name__ == "__main__":
    unittest.main()
