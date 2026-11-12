"""Test aggiunti dopo il primo giro di mutation testing (mutazioni_g0_journal.py, 12/11/2026): con i 41 test
precedenti sopravvivevano 14 mutanti su 44 non equivalenti. Ogni test indica i mutanti che uccide.
I valori attesi vengono dalle regole (FTMO: violazione = equity SOTTO il limite; regole personali come scritte nel
file), non dal codice.
Uso (dalla cartella guardian/): python3 -s -B -m unittest discover -s test -v
"""
import sys
import tempfile
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from g0 import _toml as tomllib                     # noqa: E402  (portabile: Python 3.9+)

from g0 import limiti as L                                      # noqa: E402
from g0 import scheda as SCH                                     # noqa: E402
from g0.strumenti import Strumento, perdita_allo_stop            # noqa: E402
from g0.valori import NON_STIMABILE, ipotesi, misura             # noqa: E402
from journal import journal as J                                 # noqa: E402
from journal.indicatori import metriche_dopo_perdita, pattern_r1, trade_da_journal  # noqa: E402

ESEMPIO = Path(__file__).resolve().parent.parent / "esempi" / "situazione_esempio.toml"
EURUSD_200 = {"simbolo": "EURUSD", "ingresso": "1.08500", "stop": "1.08300", "quantita": "1"}   # 200 USD esatti
T = {"simbolo": "EURUSD", "direzione": "long", "aperto_utc": "2026-11-12T09:00:00Z", "ingresso": "1.085",
     "stop": "1.083", "quantita": "1", "fonte": "t"}


def esempio(**conto):
    with open(ESEMPIO, "rb") as f:
        d = tomllib.load(f)
    d["conto"].update(conto)
    return d


def regole_con(**conferme):
    with open(SCH.FILE_REGOLE_PERSONALI, "rb") as f:
        regole = tomllib.load(f)
    for r in regole["regola"]:
        if r["id"].replace("-", "_") in conferme:
            r.update(confermata=True, valore=conferme[r["id"].replace("-", "_")])
    return regole


def avvisi(d, **conferme):
    testo = "\n".join(SCH.scheda(d, regole_personali=regole_con(**conferme)))
    return testo.split("\nAVVISI\n")[1].split("\nREGOLE PERSONALI\n")[0]


class TestValoriNonFiniti(unittest.TestCase):
    def test_prezzi_quantita_e_cambi_infiniti_rifiutati(self):
        """V09. Infinity > 0 è vero: senza is_finite() la perdita allo stop diventerebbe infinita senza errore."""
        fx = Strumento("EURUSD", "fx", "USD", D(100000), "t", valuta_base="EUR")
        jp = Strumento("USDJPY", "fx", "JPY", D(100000), "t", valuta_base="USD")
        m = lambda x, u="prezzo": misura(x, u, "t")
        for caso in (lambda: perdita_allo_stop(fx, m("Infinity"), m("1.083"), m("1", "lotti"), "USD"),
                     lambda: perdita_allo_stop(fx, m("1.085"), m("1.083"), m("Infinity", "lotti"), "USD"),
                     lambda: perdita_allo_stop(jp, m("150"), m("149.5"), m("1", "lotti"), "EUR",
                                               cambio=misura("Infinity", "JPY/EUR", "t"))):
            with self.assertRaises(ValueError):
                caso()


class TestStressConRiserve(unittest.TestCase):
    def test_le_riserve_entrano_nello_scenario(self):
        """V17. Scenario = perdite allo stop + riserve dichiarate; una riserva NON STIMABILE rende lo scenario tale."""
        st = L.scenario_di_stress([misura("200", "USD", "t")], [ipotesi("50", "USD", "t", "H_gap")])
        self.assertEqual(st.valore, D("250"))
        self.assertIn("H_gap", st.condizioni)
        st = L.scenario_di_stress([misura("200", "USD", "t")], [ipotesi(None, "USD", "t", "H_gap")])
        self.assertEqual(st.incertezza, NON_STIMABILE)


class TestSoglieAlLimite(unittest.TestCase):
    def test_p05_uguale_al_limite_della_prop_non_e_piu_stretto(self):
        """V18. P-05 = 5% sul 2-Step (limite FTMO 5%): non è PIÙ stretto, va segnalato; 4,99% invece sì."""
        self.assertIn("non è più stretto del limite della prop firm", avvisi(esempio(), P_05="0.05"))
        self.assertNotIn("non è più stretto", avvisi(esempio(), P_05="0.0499"))

    def test_p01_rischio_uguale_alla_soglia_non_la_supera(self):
        """V19. Trade EURUSD 1 lotto, 200 USD esatti su 100.000 = 0,2%: con soglia 0,2% nessun avviso; 0,19% sì."""
        d = esempio()
        d["trade_previsto"] = dict(EURUSD_200)
        self.assertNotIn("P-01: il trade previsto rischia", avvisi(d, P_01="0.002"))
        self.assertIn("P-01: il trade previsto rischia", avvisi(d, P_01="0.0019"))

    def test_p11_e_p14_valore_uguale_alla_soglia_rispetta_la_regola(self):
        """V20. «Meno di 6 ore di sonno»: 6 ore rispettano la regola, 5,9 no. Pausa di 15 minuti: 15 la rispettano."""
        for rid, chiave, soglia, ok, ko in (("P_14", "ore_sonno", "6", "6", "5.9"),
                                           ("P_11", "minuti_da_ultima_perdita", "15", "15", "14")):
            for x, violata in ((ok, False), (ko, True)):
                d = esempio()
                d["sessione"] = {chiave: x}
                presente = f"{rid.replace('_', '-')}:" in avvisi(d, **{rid: soglia})
                self.assertEqual(presente, violata, f"{chiave}={x}")

    def test_p15_raggiunto_il_massimo_di_perdite_consecutive(self):
        """V21. «Massimo numero di perdite consecutive prima dello stop» = 3: alla terza perdita la regola scatta."""
        for x, violata in (("3", True), ("2", False)):
            d = esempio()
            d["sessione"] = {"perdite_consecutive_oggi": x}
            self.assertEqual("P-15:" in avvisi(d, P_15="3"), violata, x)

    def test_equity_esattamente_al_limite_non_e_violazione(self):
        """V23, V27. FTMO: violazione = equity SOTTO il limite. Limite giornaliero 100.400 − 5.000 = 95.400.
        Trade previsto 200 USD: con equity 95.600 lo stop porta l'equity AL limite (nessun avviso); 95.599,99 sotto.
        Scenario di stress = 160,50 (posizione aperta) + 200 = 360,50: equity 95.760,50 → al limite; 95.760,49 sotto."""
        msg_t = "Se lo stop del trade previsto viene colpito, il limite giornaliero viene violato."
        msg_s = "Nello scenario di stress il limite giornaliero viene violato."
        for eq, trade, stress in (("95600", False, True), ("95599.99", True, True),
                                  ("95760.50", False, False), ("95760.49", False, True)):
            d = esempio(equity=eq)
            d["trade_previsto"] = dict(EURUSD_200)
            a = avvisi(d)
            self.assertEqual(msg_t in a, trade, f"trade, equity {eq}")
            self.assertEqual(msg_s in a, stress, f"stress, equity {eq}")


class TestCorrezioniACatena(unittest.TestCase):
    def test_brier_e_indicatori_con_correzione_di_una_correzione(self):
        """V29. a → a2 (corregge a) → a3 (corregge a2): vale a3 (0,6). Esito 1: Brier (0,6 − 1)² = 0,16 su n = 1.
        Lo stesso per i trade: una sola operazione, nell'ultima versione."""
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            base = {"autore": "claude", "evento": "A", "scadenza_utc": "2026-12-01T00:00:00Z", "fonte": "t"}
            a = J.aggiungi("previsione", dict(base, probabilita=0.8), d)["id"]
            a2 = J.aggiungi("previsione", dict(base, probabilita=0.7, corregge=a), d)["id"]
            J.aggiungi("previsione", dict(base, probabilita=0.6, corregge=a2), d)
            J.aggiungi("previsione", {"autore": "utente", "fonte": "t", "chiude": a, "esito": 1}, d)
            self.assertEqual(J.brier(d)["claude"]["n"], 1)
            self.assertAlmostEqual(J.brier(d)["claude"]["brier"], (0.6 - 1) ** 2)
            chiuso = dict(T, chiuso_utc="2026-11-12T09:30:00Z", pnl_conto="-100")
            t1 = J.aggiungi("trade", chiuso, d)["id"]
            t2 = J.aggiungi("trade", dict(chiuso, pnl_conto="-150", corregge=t1), d)["id"]
            J.aggiungi("trade", dict(chiuso, pnl_conto="-200", corregge=t2), d)
            trades = trade_da_journal(d / "trade.jsonl")
            self.assertEqual([t["pnl_conto"] for t in trades], ["-200"])


class TestOrariUTC(unittest.TestCase):
    def test_journal_rifiuta_fusi_diversi_da_utc_e_ammette_apertura_uguale_a_chiusura(self):
        """V36, V37. +01:00 non è UTC (anche se è un orario ISO valido); +00:00 sì. Un trade aperto e chiuso nello
        stesso istante (per esempio uno stop immediato) non è un errore: «chiuso_utc non precede aperto_utc»."""
        with self.assertRaises(ValueError):
            J.valida("trade", dict(T, aperto_utc="2026-11-12T10:00:00+01:00"))
        J.valida("trade", dict(T, aperto_utc="2026-11-12T09:00:00+00:00"))
        J.valida("trade", dict(T, chiuso_utc=T["aperto_utc"]))

    def test_indicatori_rifiutano_fusi_diversi_da_utc(self):
        """V42."""
        t1 = dict(T, chiuso_utc="2026-11-12T09:30:00Z", pnl_conto="-100")
        t2 = dict(T, aperto_utc="2026-11-12T10:33:00+01:00")
        with self.assertRaises(ValueError):
            metriche_dopo_perdita([t1, t2])


class TestIndicatoriAlLimite(unittest.TestCase):
    def test_r1_rientro_esattamente_al_limite_e_pareggio(self):
        """V43: R1 = ingresso ENTRO `minuti_max` (≤): 3 minuti con minuti_max = 3 è un caso.
        V44: un pareggio (P/L = 0) non è una perdita: nessuna metrica «dopo una perdita»."""
        t1 = dict(T, chiuso_utc="2026-11-12T09:30:00Z", pnl_conto="-200")
        t2 = dict(T, aperto_utc="2026-11-12T09:33:00Z", quantita="2")
        self.assertEqual(len(pattern_r1([t1, t2], minuti_max=3, rapporto_min=2)["casi"]), 1)
        self.assertEqual(metriche_dopo_perdita([dict(t1, pnl_conto="0"), t2]), [])


if __name__ == "__main__":
    unittest.main()
