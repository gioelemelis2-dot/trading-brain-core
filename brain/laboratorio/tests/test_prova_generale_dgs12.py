"""Prova generale a vuoto (D-34 punto 5): i 15 casi a risposta esatta del DGS (DGS-12, allegato C, 21/11/2026).

I casi e gli attesi li ha scritti il DGS, che non ha scritto il codice; qui sono trascritti senza ritoccarli. Dati tutti
inventati; zero nuove prove selezionabili (N) e zero aperture della riserva.

Per ogni caso si controlla il componente indicato dal DGS:
- A, B: contabilità del simulatore (`simulatori/orb_londra.simula`), poi il verdetto sulle coppie;
- C, D, E, I, J, K, M, N: percorso dalle coppie al verdetto, con l'intervallo calcolato dal metro collaudato;
- F, G, H, L, O e la seconda parte di M: decisore con l'intervallo fornito a mano (prova la sola logica).
La prova tiene distinti esito contabile, segnale del metro, veto e verdetto finale (DGS-12 §4).

Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_prova_generale_dgs12
"""
import sys
import unittest
from dataclasses import replace
from datetime import date, datetime, timezone
from pathlib import Path
from unittest import mock

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.laboratorio.simulatori import orb_londra as O               # noqa: E402
from brain.laboratorio.verdetto import verdetto_d31 as V               # noqa: E402

SEME = 314159                    # il seme del riferimento indipendente del DGS per M e N
VUOTA = (0, 0)


def vuote(n):
    return [VUOTA] * n


def con_intervallo(lo, hi):
    """Fornisce al decisore un intervallo sintetico (non stimato dalle coppie)."""
    return mock.patch.object(V, "intervallo", lambda coppie, seme: (lo, hi))


def minuto(h, m):
    return datetime(2026, 1, 6, h, m, tzinfo=timezone.utc)


def q(x):
    return (x, x, x, x)


def veto_dgs(coppie):
    """La regola di veto dei casi H, I, J: blocchi da 250 sedute, media < −0,25 R, almeno 100 trade validi."""
    return V.veto_blocchi(coppie, -0.25, 100)


class TestContabilita(unittest.TestCase):
    def test_a_costo_contato_una_volta(self):
        """Long di un'unità: acquisto all'ASK 101, vendita al BID 106, commissione totale 1, budget di rischio 10.
        P/L netto = 106 − 101 − 1 = 4, cioè S = 0,40 R e K = 1; lo spread è già nei prezzi."""
        par = replace(O.V_T, target_r=None, slip_ingresso=0.0, slip_uscita=0.0, commissione=1.0, rischio_usd=10.0)
        g = O.Giorno(date(2026, 1, 6), 10.0, 110.0, 92.0, True, "", "acquisto",
                     [(minuto(9, 0), q(100.5), q(101.0)), (minuto(16, 30), q(106.0), q(106.5))])
        x = O.simula(g, "acquisto", par)
        self.assertEqual((x["entrata"], x["uscita"], x["once"]), (101.0, 106.0, 1))
        self.assertAlmostEqual(x["r"], 0.40, places=12)
        v = V.verdetto([(x["r"], 1)] + vuote(999), 1)
        self.assertEqual(v["esito"], "non decidibile")
        self.assertTrue(v["causa"].startswith("minimi"))

    def test_b_stop_scavalcato(self):
        """Long a 100, stop 99, prima vendita eseguibile a 97,50 dopo il salto, budget 1, costi nulli: S = −2,50 R.
        Un esecutore che stampa −1 R fallisce."""
        par = replace(O.V_T, target_r=None, slip_ingresso=0.0, slip_uscita=0.0, commissione=0.0, rischio_usd=1.0)
        g = O.Giorno(date(2026, 1, 6), 2.0, 101.0, 99.0, True, "", "acquisto",
                     [(minuto(9, 0), q(99.9), q(100.0)), (minuto(9, 1), q(97.5), q(97.6)),
                      (minuto(16, 30), q(98.0), q(98.1))])
        x = O.simula(g, "acquisto", par)
        self.assertEqual((x["motivo"], x["once"]), ("stop", 1))
        self.assertAlmostEqual(x["r"], -2.50, places=12)
        v = V.verdetto([(x["r"], 1)] + vuote(999), 1)
        self.assertEqual(v["esito"], "non decidibile")
        self.assertTrue(v["causa"].startswith("minimi"))


class TestDatiEMinimi(unittest.TestCase):
    def test_c_seduta_ignota(self):
        """999 coppie (0,40; 1) e una con K = 1 e S mancante: non decidibile per dati inidonei. Sostituirla con zero
        o eliminarla fallisce il caso."""
        coppie = [(0.40, 1)] * 999 + [(None, 1)]
        v = V.verdetto(coppie, 1)
        self.assertEqual(v["esito"], "non decidibile")
        self.assertTrue(v["causa"].startswith("dati inidonei"))
        self.assertEqual(v["sedute"], 1000)                              # la seduta ignota resta nel rendiconto
        self.assertIsNone(v["segnale"])

    def test_d_minimo_trade(self):
        v = V.verdetto([(0.25, 1)] * 299 + vuote(701), 1)
        self.assertEqual((v["sedute"], v["trade"], v["sedute_attive"]), (1000, 299, 299))
        self.assertEqual(v["esito"], "non decidibile")
        self.assertIn("trade: 299 < 300", v["causa"])
        self.assertIsNone(v["L"])                                         # prima di usare il bootstrap
        self.assertIsNone(v["segnale"])

    def test_e_minimo_sedute_attive(self):
        v = V.verdetto([(0.50, 2)] * 199 + vuote(801), 1)
        self.assertEqual((v["trade"], v["sedute_attive"]), (398, 199))
        self.assertEqual(v["esito"], "non decidibile")
        self.assertIn("sedute con trade: 199 < 200", v["causa"])
        self.assertNotIn("trade: 398", v["causa"])


class TestSoglie(unittest.TestCase):
    PIENE = [(0.40, 1)] * 1000                                            # dati idonei, minimi soddisfatti

    def test_f_uguaglianza_di_l(self):
        self.assertEqual(V.segnale((0.20, 0.32)), "inconclusivo")
        with con_intervallo(0.20, 0.32):
            v = V.verdetto(self.PIENE, 1)
        self.assertEqual((v["esito"], v["segnale"]), ("non decidibile", "inconclusivo"))

    def test_g_uguaglianza_di_u(self):
        self.assertEqual(V.segnale((0.01, 0.10)), "inconclusivo")
        with con_intervallo(0.01, 0.10):
            v = V.verdetto(self.PIENE, 1)
        self.assertEqual((v["esito"], v["segnale"]), ("non decidibile", "inconclusivo"))

    def test_l_confine_d44(self):
        eps = V.AMPIEZZA_MINIMA
        with con_intervallo(0.0, eps / 2):
            v = V.verdetto(self.PIENE, 1)
        self.assertEqual((v["esito"], v["causa"], v["segnale"]), ("non decidibile", "intervallo invalido", "invalido"))
        with con_intervallo(0.0, eps):
            v = V.verdetto(self.PIENE, 1)
        self.assertEqual((v["esito"], v["segnale"]), ("bocciata", "sfavorevole"))


class TestVeti(unittest.TestCase):
    def test_h_veto_con_l_favorevole(self):
        """Primo blocco 250 × (−0,50; 1), poi 750 × (1; 1). Media totale +0,625 R, segnale favorevole (estremi
        forniti al decisore), ma bocciata per veto. Il rapporto distingue segnale e veto."""
        coppie = [(-0.50, 1)] * 250 + [(1.0, 1)] * 750
        veto = veto_dgs(coppie)
        self.assertEqual(veto["esito"], "fallito")
        self.assertEqual(veto["medie"][0], -0.50)
        with con_intervallo(0.30, 0.65):
            v = V.verdetto(coppie, 1, [veto])
        self.assertEqual((v["esito"], v["causa"]), ("bocciata", "veto: blocchi"))
        self.assertAlmostEqual(v["media"], 0.625, places=12)
        self.assertEqual(v["segnale"], "favorevole")
        r = V.rapporto(v)
        self.assertIn("segnale del solo metro: favorevole", r)
        self.assertIn("veto: blocchi", r)

    def test_i_veto_valido_con_minimi_globali_mancanti(self):
        coppie = [(-0.50, 1)] * 100 + vuote(150) + vuote(750)
        veto = veto_dgs(coppie)
        self.assertEqual(veto["esito"], "fallito")
        v = V.verdetto(coppie, 1, [veto])
        self.assertEqual((v["esito"], v["causa"]), ("bocciata", "veto: blocchi"))
        self.assertEqual((v["trade"], v["sedute_attive"]), (100, 100))
        self.assertIsNone(v["segnale"])                                    # i minimi globali mancano: niente metro

    def test_j_veto_solo_apparente(self):
        """Come I, ma il risultato del centesimo trade è ignoto: 99 esiti noti, veto non accertato, non decidibile."""
        coppie = [(-0.50, 1)] * 99 + [(None, 1)] + vuote(150) + vuote(750)
        veto = veto_dgs(coppie)
        self.assertEqual(veto["esito"], "non valutabile")
        self.assertIsNone(veto["medie"][0])
        v = V.verdetto(coppie, 1, [veto])
        self.assertEqual(v["esito"], "non decidibile")
        self.assertTrue(v["causa"].startswith("dati inidonei"))

    def test_veto_accertato_con_un_dato_mancante_altrove(self):
        """DGS-12 §3: un blocco completo può bocciare anche se manca un'osservazione in un altro blocco."""
        coppie = [(-0.50, 1)] * 100 + vuote(150) + vuote(250) + [(None, 1)] + vuote(249) + vuote(250)
        veto = veto_dgs(coppie)
        self.assertEqual(veto["esito"], "fallito")
        self.assertIsNone(veto["medie"][2])
        v = V.verdetto(coppie, 1, [veto])
        self.assertEqual((v["esito"], v["causa"]), ("bocciata", "veto: blocchi"))


class TestPercorsiCompleti(unittest.TestCase):
    P = [(3 / 8, 1)] * 500 + [(5 / 8, 1)] * 500

    def test_k_intervallo_degenere(self):
        for seme in (1, 7, SEME):                                          # indipendente dal seme
            v = V.verdetto([(0.375, 1)] * 1000, seme)
            self.assertEqual((v["esito"], v["causa"], v["segnale"]), ("non decidibile", "intervallo invalido",
                                                                     "invalido"))

    def test_m_promozione_da_coppie(self):
        """Riferimento indipendente del DGS (CPython 3.12, random.Random(314159), 100 randrange(1000) per replica,
        3.999 repliche, ranghi 100 e 3.900): L = 0,47475 e U = 0,52450 R. Promossa; un indicatore descrittivo fallito
        resta visibile nel rapporto e non cambia l'esito."""
        descr = {"id": "drawdown descrittivo", "veto": False, "descrittivo": True, "esito": "fallito"}
        v = V.verdetto(self.P, SEME, [descr])
        self.assertEqual(v["media"], 0.5)
        self.assertEqual((v["L"], v["U"]), (0.47475, 0.5245))
        self.assertEqual((v["esito"], v["segnale"]), ("promossa", "favorevole"))
        r = V.rapporto(v)
        self.assertIn("drawdown descrittivo", r)
        self.assertIn("descrittivo", r)

    def test_m_requisito_vincolante_indeterminato(self):
        """Stesso intervallo, un requisito vincolante per promuovere indeterminato: non decidibile."""
        vinc = {"id": "costi", "veto": False, "esito": "non valutabile"}
        with con_intervallo(0.47475, 0.5245):
            v = V.verdetto(self.P, SEME, [vinc])
        self.assertEqual(v["esito"], "non decidibile")
        self.assertIn("costi", v["causa"])

    def test_n_bocciatura_da_coppie(self):
        n = [(s - 0.5, k) for s, k in self.P]
        v = V.verdetto(n, SEME)
        self.assertEqual(v["media"], 0.0)
        self.assertEqual((v["L"], v["U"]), (-0.02525, 0.0245))
        self.assertEqual((v["esito"], v["causa"]), ("bocciata", "statistica: U < +0,10 R"))


class TestScreening(unittest.TestCase):
    def test_o_confini(self):
        """Con l'operatore ≥ scritto nella formula di D-36 (lettura da far chiarire al titolare): ammessa, esclusa,
        esclusa, esclusa. L'ammissione non assegna il verdetto «promossa»."""
        attesi = {(0.26, 0.01, 0.50): True, (0.25, 0.01, 0.60): False, (0.26, 0.0, 0.60): False,
                  (0.26, 0.01, 0.4999): False}
        for (media, lo, potenza), atteso in attesi.items():
            with con_intervallo(lo, lo + 0.5):
                s = V.screening([(media, 1)] * 1000, 1, potenza)
            self.assertEqual(s["ammessa"], atteso, (media, lo, potenza))
            self.assertNotIn("esito", s)


if __name__ == "__main__":
    unittest.main()
