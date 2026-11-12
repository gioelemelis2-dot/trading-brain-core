"""Test dei 5 difetti del G0 e del journal (mandato «Binario A», 12/11/2026), scritti PRIMA delle correzioni (TDD).
Uso (dalla cartella guardian/): python3 -s -B -m unittest discover -s test -v
"""
import copy
import json
import sys
import tempfile
import tomllib
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from g0 import scheda as SCH                      # noqa: E402
from g0.strumenti import Strumento, perdita_allo_stop  # noqa: E402
from g0.valori import misura                       # noqa: E402
from journal import journal as J                   # noqa: E402
from journal.indicatori import metriche_dopo_perdita, pattern_r1  # noqa: E402

ESEMPIO = Path(__file__).resolve().parent.parent / "esempi" / "situazione_esempio.toml"


def esempio():
    with open(ESEMPIO, "rb") as f:
        return tomllib.load(f)


class TestFix1StressMargineTotale(unittest.TestCase):
    def test_avviso_se_lo_stress_viola_il_limite_totale(self):
        """Conto 2-Step a 91.500: limite giornaliero 86.500 (margine 5.000), limite totale 90.000 (margine 1.500).
        Posizione aperta EURUSD 1,5 lotti dal prezzo attuale 1,08400 allo stop 1,08300 = 150 USD + 10,50 → ma con 15
        lotti = 1.510,50 USD: il giornaliero regge, il totale no. Serve l'avviso sul limite totale."""
        d = esempio()
        d["conto"].update(saldo_mezzanotte="91500", equity="91500")
        d["posizione"][0]["quantita"] = "15"
        d.pop("trade_previsto")
        testo = "\n".join(SCH.scheda(d))
        self.assertIn("margine totale dopo lo scenario", testo)
        self.assertIn("Nello scenario di stress il limite totale viene violato.", testo)
        self.assertNotIn("Nello scenario di stress il limite giornaliero viene violato.", testo)


class TestFix2MetadatiFutures(unittest.TestCase):
    def test_future_senza_dimensione_contratto_fittizia(self):
        """Un future si descrive con passo e valore del tick: nessuna dimensione del contratto «1» inventata."""
        es = Strumento("ES", "future", "USD", None, "specifica CME (test)", "V",
                       passo_tick=D("0.25"), valore_tick=D("12.50"))
        p = perdita_allo_stop(es, misura("5000.00", "prezzo", "t"), misura("4990.00", "prezzo", "t"),
                              misura("2", "contratti", "t"), "USD")
        self.assertEqual(p.valore, D(1000))
        dati = {"strumento": [{"simbolo": "ES", "classe": "future", "valuta_profitto": "USD", "passo_tick": "0.25",
                               "valore_tick": "12.50", "fonte": "t", "stato_verifica": "C"}]}
        self.assertIsNone(SCH._strumenti(dati)["ES"].dimensione_contratto)
        with self.assertRaises(ValueError):                    # FX senza dimensione del contratto: errore esplicito
            Strumento("EURUSD", "fx", "USD", None, "t", valuta_base="EUR")


class TestFix3RegolePersonali(unittest.TestCase):
    def test_regola_confermata_applicata_e_non_confermate_dichiarate(self):
        """Con P-01 confermata a 0,5% del capitale, il trade previsto dell'esempio (682 USD su 100.000 = 0,682%)
        deve produrre un avviso P-01. Senza conferme la scheda lo dichiara, senza stringhe fisse."""
        with open(SCH.FILE_REGOLE_PERSONALI, "rb") as f:
            regole = tomllib.load(f)
        nessuna = "\n".join(SCH.scheda(esempio(), regole_personali=regole))
        self.assertIn("0 regole personali confermate su 15", nessuna)
        conf = copy.deepcopy(regole)
        p01 = next(r for r in conf["regola"] if r["id"] == "P-01")
        p01.update(confermata=True, valore="0.005")
        testo = "\n".join(SCH.scheda(esempio(), regole_personali=conf))
        self.assertIn("1 regole personali confermate su 15", testo)
        self.assertIn("P-01", testo.split("AVVISI")[1])


class TestFix4AncoraEsterna(unittest.TestCase):
    def test_ancora_rileva_ultima_riga_troncamento_e_riscrittura(self):
        T = {"simbolo": "EURUSD", "direzione": "long", "aperto_utc": "2026-11-12T09:00:00Z", "ingresso": "1.085",
             "stop": "1.083", "quantita": "1", "fonte": "t"}

        def nuovo():
            d = Path(tempfile.mkdtemp())
            for q in ("1", "2", "3"):
                J.aggiungi("trade", dict(T, quantita=q), d)
            return d, d / "trade.jsonl"

        d, f = nuovo()
        self.assertTrue((d / "ancora_integrita.json").exists())
        self.assertEqual(J.verifica(d), [])
        r = f.read_text().splitlines()
        r[2] = r[2].replace('"quantita":"3"', '"quantita":"9"')            # ultima riga modificata
        f.write_text("\n".join(r) + "\n")
        self.assertTrue(J.verifica(d))

        d, f = nuovo()
        f.write_text("\n".join(f.read_text().splitlines()[:2]) + "\n")      # coda troncata
        self.assertTrue(J.verifica(d))

        d, f = nuovo()
        recs = [json.loads(x) for x in f.read_text().splitlines()]
        recs[0]["dati"]["quantita"] = "9"
        prec, out = J.GENESI, []
        for rec in recs:                                                    # riscrittura coerente della catena
            rec["prec_hash"] = prec
            s = J._canonico(rec)
            out.append(s)
            prec = J._sha(s)
        f.write_text("\n".join(out) + "\n")
        self.assertTrue(J.verifica(d))


class TestFix5IndicatoriDecimal(unittest.TestCase):
    def test_decimal_e_frazioni_di_secondo(self):
        base = {"simbolo": "EURUSD", "direzione": "long", "ingresso": "1.085", "stop": "1.083", "fonte": "t"}
        t1 = dict(base, aperto_utc="2026-11-12T09:00:00Z", chiuso_utc="2026-11-12T09:30:00Z", quantita="0.1",
                  pnl_conto="-20.10")
        t2 = dict(base, aperto_utc="2026-11-12T09:33:00.120Z", chiuso_utc="2026-11-12T10:00:00.5Z", quantita="0.3",
                  pnl_conto="15")
        m = metriche_dopo_perdita([t1, t2])
        self.assertIsInstance(m[0]["minuti_dopo_perdita"], D)
        self.assertEqual(m[0]["minuti_dopo_perdita"], D("3.002"))          # 180,12 s
        self.assertEqual(m[0]["rapporto_size"], D("3"))                    # 0,3 / 0,1 (in float: 2,9999…)
        r = pattern_r1([t1, t2], minuti_max=D("5"), rapporto_min=D("2"))
        self.assertEqual(len(r["casi"]), 1)


if __name__ == "__main__":
    unittest.main()
