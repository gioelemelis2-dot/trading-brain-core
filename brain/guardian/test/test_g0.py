"""Test del Guardian G0. Valori attesi:
- limiti FTMO: esempi numerici pubblicati sulla pagina ufficiale (ftmo.com/en/trading-objectives, 12/11/2026);
- conversioni e perdite allo stop: calcolo a mano riportato accanto a ogni test.
Uso (dalla cartella guardian/): python3 -s -B -m unittest discover -s test -v
"""
import sys
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from g0 import _toml as tomllib                     # noqa: E402  (portabile: Python 3.9+)

from g0 import limiti as L                                    # noqa: E402
from g0.scheda import scheda                                  # noqa: E402
from g0.strumenti import H_ESEC, Strumento, perdita_allo_stop  # noqa: E402
from g0.valori import (NON_STIMABILE, Valore, combina, ipotesi,  # noqa: E402
                       misura, regola, restringi)

F = "test"


def m(x, u="USD"):
    return misura(x, u, F)


class TestLimitiFTMO(unittest.TestCase):
    """Esempi ufficiali FTMO: i valori attesi sono copiati dalla pagina, non calcolati dal codice."""

    def test_2step_giornaliero_esempio_ufficiale(self):
        for saldo, atteso in ((100000, 95000), (102000, 97000), (101000, 96000)):
            self.assertEqual(L.limite_giornaliero("ftmo_2step", m(100000), m(saldo)).valore, D(atteso))

    def test_2step_totale_statico(self):
        self.assertEqual(L.limite_totale("ftmo_2step", m(100000), [m(104000)]).valore, D(90000))

    def test_1step_giornaliero_e_trailing(self):
        for saldo, atteso in ((100000, 97000), (102000, 99000), (101000, 98000)):
            self.assertEqual(L.limite_giornaliero("ftmo_1step", m(100000), m(saldo)).valore, D(atteso))
        self.assertEqual(L.limite_totale("ftmo_1step", m(100000), []).valore, D(90000))
        self.assertEqual(L.limite_totale("ftmo_1step", m(100000), [m(104000)]).valore, D(94000))
        self.assertEqual(L.limite_totale("ftmo_1step", m(100000), [m(104000), m(103000)]).valore, D(94000))

    def test_instant_esempio_ufficiale(self):
        for saldo, atteso in ((50000, 48500), (51000, 49500), (50500, 49000)):
            self.assertEqual(L.limite_giornaliero("ftmo_instant", m(50000), m(saldo)).valore, D(atteso))
        self.assertEqual(L.limite_totale("ftmo_instant", m(50000), []).valore, D(45000))
        self.assertEqual(L.limite_totale("ftmo_instant", m(50000), [m(50600)]).valore, D(45600))
        self.assertEqual(L.limite_totale("ftmo_instant", m(50000), [m(50600), m(50300)]).valore, D(45600))

    def test_limite_e_derivato_dalla_regola_verificata(self):
        lg = L.limite_giornaliero("ftmo_2step", m(100000), m(100000))
        self.assertEqual(lg.tipo, "DERIVATO")
        self.assertEqual(lg.stato_verifica, "V")


class TestPerditaAlloStop(unittest.TestCase):
    EURUSD = Strumento("EURUSD", "fx", "USD", D(100000), F, valuta_base="EUR")
    USDJPY = Strumento("USDJPY", "fx", "JPY", D(100000), F, valuta_base="USD")
    ES = Strumento("ES", "future", "USD", D(50), F, passo_tick=D("0.25"), valore_tick=D("12.50"))

    def test_fx_conto_nella_valuta_quotata(self):
        # |1,08500 − 1,08300| × 100.000 × 1 = 200 USD
        p = perdita_allo_stop(self.EURUSD, m("1.08500", "prezzo"), m("1.08300", "prezzo"), m(1, "lotti"), "USD")
        self.assertEqual(p.valore, D(200))
        self.assertIn(H_ESEC, p.condizioni)
        self.assertEqual(p.tipo, "DERIVATO")

    def test_fx_conto_nella_valuta_base_converte_al_prezzo_dello_stop(self):
        # 200 USD / 1,08300 (cambio all'uscita = prezzo dello stop) = 184,6722… EUR
        p = perdita_allo_stop(self.EURUSD, m("1.08500", "prezzo"), m("1.08300", "prezzo"), m(1, "lotti"), "EUR")
        self.assertAlmostEqual(float(p.valore), 200 / 1.083, places=9)

    def test_fx_terza_valuta_richiede_cambio_misurato(self):
        with self.assertRaises(ValueError):
            perdita_allo_stop(self.USDJPY, m("150.00", "prezzo"), m("149.50", "prezzo"), m(1, "lotti"), "EUR")
        # 0,50 × 100.000 = 50.000 JPY; / 162 (EURJPY) = 308,6419… EUR
        p = perdita_allo_stop(self.USDJPY, m("150.00", "prezzo"), m("149.50", "prezzo"), m(1, "lotti"), "EUR",
                              cambio=misura("162.00", "JPY/EUR", "piattaforma 14:32 UTC"))
        self.assertAlmostEqual(float(p.valore), 50000 / 162, places=9)

    def test_future_tick(self):
        # 10 punti = 40 tick × 12,50 USD × 2 contratti = 1.000 USD
        p = perdita_allo_stop(self.ES, m("5000.00", "prezzo"), m("4990.00", "prezzo"), m(2, "contratti"), "USD")
        self.assertEqual(p.valore, D(1000))
        with self.assertRaises(ValueError):
            perdita_allo_stop(self.ES, m("5000.00", "prezzo"), m("4990.10", "prezzo"), m(1, "contratti"), "USD")

    def test_vendita_allo_scoperto_e_commissioni(self):
        p = perdita_allo_stop(self.EURUSD, m("1.08300", "prezzo"), m("1.08500", "prezzo"), m(1, "lotti"), "USD",
                              commissioni=m("7.00"))
        self.assertEqual(p.valore, D("207.00"))


class TestSchemaDeiValori(unittest.TestCase):

    def test_un_numero_senza_tipo_valido_e_rifiutato(self):
        with self.assertRaises(ValueError):
            Valore(D(1), "USD", "FATTO", "osservazione", F)
        with self.assertRaises(ValueError):
            Valore(D(1), "USD", "MISURA", "osservazione", "")
        with self.assertRaises(TypeError):
            Valore(1.0, "USD", "MISURA", "osservazione", F)
        with self.assertRaises(ValueError):
            Valore(D(1), "USD", "STIMA", "inferenza", F)  # stima senza incertezza

    def test_propagazione_del_tipo_piu_debole_e_delle_condizioni(self):
        a, r = m(100), regola("0.05", "frazione", F, stato="V-sec")
        d = combina([a, r], D(5), "USD", "calcolo deterministico", F)
        self.assertEqual((d.tipo, d.stato_verifica), ("DERIVATO", "V-sec"))
        h = ipotesi(50, "USD", F, "H_edge")
        x = combina([a, h], D(150), "USD", "calcolo deterministico", F)
        self.assertEqual(x.tipo, "IPOTESI")              # regola dell'utente: il tipo più debole
        self.assertEqual(x.operazione, "calcolo deterministico")
        self.assertIn("H_edge", x.condizioni)            # le condizioni non si perdono

    def test_non_stimabile_contagioso_e_incertezza_obbligatoria(self):
        n = ipotesi(None, "USD", F, "H_gap")
        self.assertEqual(combina([m(1), n], D(0), "USD", "calcolo deterministico", F).incertezza, NON_STIMABILE)
        s = Valore(D(10), "USD", "STIMA", "inferenza", F, incertezza="IC 90% [6; 14], n=42")
        with self.assertRaises(ValueError):
            combina([m(1), s], D(11), "USD", "calcolo deterministico", F)

    def test_una_stima_non_allarga_mai_un_limite(self):
        lim = combina([m(1000)], D(1000), "USD", "calcolo deterministico", F)
        stretta = Valore(D(800), "USD", "STIMA", "inferenza", F, incertezza="IC 90% [700; 900]")
        larga = Valore(D(1200), "USD", "STIMA", "inferenza", F, incertezza="IC 90% [1100; 1300]")
        self.assertEqual(restringi(lim, stretta).valore, D(800))
        self.assertEqual(restringi(lim, larga).valore, D(1000))
        self.assertEqual(restringi(lim, ipotesi(None, "USD", F, "H")).valore, D(1000))


class TestMarginiStress(unittest.TestCase):

    def test_stop_residui(self):
        p = combina([m(800)], D(800), "USD", "calcolo deterministico", F)
        for marg, atteso in ((2700, 3), (2400, 3), (799, 0), (-10, 0)):
            mg = combina([m(marg)], D(marg), "USD", "calcolo deterministico", F)
            self.assertEqual(L.stop_residui(mg, p).valore, D(atteso))

    def test_scenario_di_stress(self):
        st = L.scenario_di_stress([m(200), m(300)])
        self.assertEqual(st.valore, D(500))
        self.assertTrue(any("scenario di stress" in c for c in st.condizioni))


class TestScheda(unittest.TestCase):

    def test_esempio_end_to_end(self):
        with open(Path(__file__).resolve().parent.parent / "esempi" / "situazione_esempio.toml", "rb") as f:
            dati = tomllib.load(f)
        righe = scheda(dati)
        testo = "\n".join(righe)
        self.assertTrue(righe[0].startswith("G0 · CONSULTIVO · NON RICONCILIATO"))
        i = {k: testo.index(k) for k in ("LIMITI DETERMINISTICI", "TRADE PREVISTO", "SCENARIO DI STRESS",
                                          "RISERVE", "AVVISI", "DECISIONE")}
        self.assertEqual(sorted(i, key=i.get), list(i))   # ordine fisso: prima i limiti deterministici
        self.assertIn("riserva per gap e slippage: NON STIMABILE", testo)
        # posizione aperta EURUSD: dal prezzo attuale 1,08400 allo stop 1,08300 = 0,001 × 100.000 × 1,5 = 150 USD
        # + 10,50 commissioni residue = 160,50; trade previsto USDJPY su conto USD: 100.000 JPY / 149,70 + 14 = 682,00
        self.assertIn("perdita nello scenario: 842,50 USD", testo)

    def test_posizione_aperta_senza_prezzo_attuale_rifiutata(self):
        with open(Path(__file__).resolve().parent.parent / "esempi" / "situazione_esempio.toml", "rb") as f:
            dati = tomllib.load(f)
        del dati["posizione"][0]["prezzo_attuale"]
        with self.assertRaises(ValueError):
            scheda(dati)


if __name__ == "__main__":
    unittest.main()
