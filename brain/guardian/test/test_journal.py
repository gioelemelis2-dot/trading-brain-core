"""Test del journal: catena di hash, validazione, Brier score, impegni sigillati, indicatore R1.
Uso (dalla cartella guardian/): python3 -s -B -m unittest discover -s test -v
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from journal import journal as J              # noqa: E402
from journal.indicatori import pattern_r1, trade_da_journal  # noqa: E402

T1 = {"simbolo": "EURUSD", "direzione": "long", "aperto_utc": "2026-11-12T09:00:00Z", "ingresso": "1.08500",
      "stop": "1.08300", "quantita": "1", "fonte": "[ESEMPIO]", "chiuso_utc": "2026-11-12T09:30:00Z",
      "uscita": "1.08300", "pnl_conto": "-200"}
T2 = dict(T1, aperto_utc="2026-11-12T09:33:00Z", chiuso_utc="2026-11-12T10:00:00Z", quantita="2", pnl_conto="150")
T3 = dict(T1, aperto_utc="2026-11-12T11:00:00Z", chiuso_utc="2026-11-12T11:30:00Z", quantita="1", pnl_conto="100")


class TestJournal(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_catena_integra_e_manomissione_scoperta(self):
        for t in (T1, T2, T3):
            J.aggiungi("trade", t, self.dir)
        self.assertEqual(J.verifica(self.dir), [])
        p = self.dir / "trade.jsonl"
        righe = p.read_text(encoding="utf-8").splitlines()
        righe[0] = righe[0].replace('"-200"', '"-20"')          # modifica retroattiva
        p.write_text("\n".join(righe) + "\n", encoding="utf-8")
        self.assertTrue(any("catena interrotta" in x for x in J.verifica(self.dir)))

    def test_cancellazione_scoperta(self):
        for t in (T1, T2, T3):
            J.aggiungi("trade", t, self.dir)
        p = self.dir / "trade.jsonl"
        righe = p.read_text(encoding="utf-8").splitlines()
        p.write_text("\n".join(righe[:1] + righe[2:]) + "\n", encoding="utf-8")
        self.assertTrue(J.verifica(self.dir))

    def test_validazione(self):
        with self.assertRaises(ValueError):
            J.aggiungi("decisione", {"raccomandazione": "non entrare", "decisione": "entro", "deroga": True,
                                     "fonte": "utente"}, self.dir)                      # deroga senza motivo
        with self.assertRaises(ValueError):
            J.aggiungi("previsione", {"autore": "claude", "evento": "x", "scadenza_utc": "2026-12-01T00:00:00Z",
                                      "probabilita": 1.2, "fonte": "test"}, self.dir)
        with self.assertRaises(ValueError):
            J.aggiungi("trade", dict(T1, campo_inventato=1), self.dir)

    def test_brier(self):
        a = J.aggiungi("previsione", {"autore": "claude", "evento": "A", "scadenza_utc": "2026-12-01T00:00:00Z",
                                      "probabilita": 0.8, "fonte": "test"}, self.dir)
        b = J.aggiungi("previsione", {"autore": "claude", "evento": "B", "scadenza_utc": "2026-12-01T00:00:00Z",
                                      "probabilita": 0.3, "fonte": "test"}, self.dir)
        for rec, esito in ((a, 1), (b, 1)):
            J.aggiungi("previsione", {"autore": "utente", "fonte": "test", "chiude": rec["id"], "esito": esito},
                       self.dir)
        r = J.brier(self.dir)
        self.assertEqual(r["claude"]["n"], 2)
        self.assertAlmostEqual(r["claude"]["brier"], ((0.8 - 1) ** 2 + (0.3 - 1) ** 2) / 2)

    def test_sigillo(self):
        s = J.sigilla({"stima": 0.62})
        self.assertEqual(len(s["nonce"]), 64)                                   # 256 bit
        self.assertTrue(J.verifica_sigillo(s["impegno"], s["nonce"], {"stima": 0.62}))
        self.assertFalse(J.verifica_sigillo(s["impegno"], s["nonce"], {"stima": 0.63}))
        self.assertNotEqual(J.sigilla({"stima": 0.62})["impegno"], s["impegno"])   # nonce diverso ogni volta


class TestIndicatori(unittest.TestCase):
    def test_r1_spento_senza_parametri_e_attivo_con_parametri(self):
        with tempfile.TemporaryDirectory() as d:
            for t in (T1, T2, T3):
                J.aggiungi("trade", t, Path(d))
            trades = trade_da_journal(Path(d) / "trade.jsonl")
        self.assertEqual(pattern_r1(trades, None, None)["stato"], "spento")
        r = pattern_r1(trades, minuti_max=10, rapporto_min=1.5)
        self.assertEqual(len(r["casi"]), 1)                    # T2: 3 minuti dopo la perdita, size ×2
        self.assertEqual(r["casi"][0]["tipo"], "IPOTESI")
        self.assertEqual(r["casi"][0]["minuti_dopo_perdita"], 3.0)


if __name__ == "__main__":
    unittest.main()
