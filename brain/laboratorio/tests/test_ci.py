"""Test dello script dei test automatici (.github/scripts/esegui_test.py), #135 (Gemini R18-11, 21/11/2026).

Una suite che non esegue nessun test, o che li salta tutti, non è verde; una suite attesa che sparisce (file rinominato
o cancellato) ferma la corsa; una suite nuova non elencata è segnalata. Solo dati inventati, niente rete.
Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_ci
"""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
SCRIPT = repo_root / ".github" / "scripts" / "esegui_test.py"
_spec = importlib.util.spec_from_file_location("esegui_test", SCRIPT)
ET = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ET)


def uscita(ran, esito="OK", extra=""):
    return f"....\n----------------------------------------------------------------------\nRan {ran} tests in 0.1s\n\n{esito}{extra}\n"


class TestEsitoSuite(unittest.TestCase):
    def test_verde_solo_con_test_eseguiti(self):
        self.assertEqual(ET.esito_suite(0, uscita(12)), (True, "12 test"))
        self.assertEqual(ET.esito_suite(0, uscita(10, extra=" (skipped=1)")), (True, "10 test, 1 saltati"))

    def test_nessun_test_non_e_verde(self):
        ok, motivo = ET.esito_suite(0, uscita(0))
        self.assertFalse(ok)
        self.assertIn("nessun test", motivo)
        ok, motivo = ET.esito_suite(5, "\n----\nRan 0 tests in 0.000s\n\nNO TESTS RAN\n")      # Python 3.12+
        self.assertFalse(ok)
        self.assertIn("nessun test", motivo)

    def test_tutti_saltati_non_e_verde(self):
        ok, motivo = ET.esito_suite(0, uscita(3, extra=" (skipped=3)"))
        self.assertFalse(ok)
        self.assertIn("tutti saltati", motivo)

    def test_uscita_illeggibile_o_codice_diverso_da_zero(self):
        self.assertFalse(ET.esito_suite(0, "niente di riconoscibile")[0])
        self.assertFalse(ET.esito_suite(1, uscita(5, esito="FAILED", extra=" (failures=1)"))[0])
        self.assertFalse(ET.esito_suite(0, uscita(5, esito="FAILED", extra=" (failures=1)"))[0])


class TestElencoAtteso(unittest.TestCase):
    def test_mancanti_e_nuove(self):
        mancanti, nuove = ET.confronta_elenco(["a", "b", "d"], ["a", "b", "c"])
        self.assertEqual((mancanti, nuove), (["c"], ["d"]))
        self.assertEqual(ET.confronta_elenco(["a"], ["a"]), ([], []))

    def test_lettura_dell_elenco(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "suite_attese.txt"
            f.write_text("# commento\n\nbrain.x.test_a\n  brain.y.test_b  \n", encoding="utf-8")
            self.assertEqual(ET.leggi_elenco(f), ["brain.x.test_a", "brain.y.test_b"])

    def test_elenco_del_progetto_coincide_con_le_suite_trovate(self):
        trovate = [nome for nome, _c, _d in ET.suite()]
        self.assertEqual(ET.confronta_elenco(trovate, ET.leggi_elenco(ET.ELENCO)), ([], []))
        self.assertIn("brain.laboratorio.tests.test_ci", trovate)


if __name__ == "__main__":
    unittest.main()
