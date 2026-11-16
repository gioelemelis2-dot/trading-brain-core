"""Test della taratura della soglia «giorno completo» (studi/taratura_completezza.py), scritti PRIMA del codice.
Conta i minuti della cache per giorno e per terzo di sessione: SOLO conteggi e date, mai prezzi.
Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_taratura_completezza
"""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date, time as ora_t, timedelta
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.laboratorio.esecuzione import sintetico as SN               # noqa: E402
from brain.laboratorio.simulatori.orb_londra import _utc               # noqa: E402
from brain.laboratorio.studi import taratura_completezza as T          # noqa: E402


def _minuti(giorno, quanti, dalle=ora_t(8, 0)):
    t0 = _utc(giorno, dalle)
    return {t0 + timedelta(minutes=k): (2222.0, 2222.5, 2221.5, 2222.0) for k in range(quanti)}


class TestTaratura(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.cache = Path(self._t.name) / "XAUUSD"
        m = {}
        m.update(_minuti(date(2024, 1, 8), 525))                       # lunedì pieno
        m.update(_minuti(date(2024, 1, 9), 525))                       # martedì pieno
        m.update(_minuti(date(2024, 1, 10), 263, dalle=ora_t(12, 22)))  # solo pomeriggio
        m.update(_minuti(date(2024, 1, 11), 90))                       # quasi vuoto
        m.update(_minuti(date(2024, 12, 24), 100))                     # vigilia: solo mattino
        m.update(_minuti(date(2024, 1, 1), 0))                         # chiusura nota: file vuoto
        SN.scrivi_cache(m, self.cache, inizio=date(2024, 1, 1), fine=date(2024, 12, 24))
        # NB: scrivi_cache crea un file VUOTO per ogni giorno senza dati fra inizio e fine

    def tearDown(self):
        self._t.cleanup()

    def test_conteggi_per_giorno_e_per_terzo(self):
        e = T.esamina(self.cache, date(2024, 1, 8), date(2024, 1, 11))
        self.assertEqual(e["giorni_con_dati"], 4)
        per = {g["giorno"]: g for g in e["per_giorno"]}
        self.assertEqual(per["2024-01-08"]["sessione"], 525)
        self.assertEqual(per["2024-01-08"]["terzi"], [175, 175, 175])
        self.assertEqual(per["2024-01-10"]["sessione"], 263)
        self.assertEqual(per["2024-01-10"]["terzi"][0], 0)
        self.assertEqual(per["2024-01-11"]["terzi"], [90, 0, 0])
        self.assertNotIn("2024-01-06", per)                            # sabato: fuori
        self.assertNotIn("prezzo", str(e))

    def test_vigilie_contate_a_parte_e_chiusure_escluse(self):
        e = T.esamina(self.cache, date(2024, 1, 1), date(2024, 12, 24))
        self.assertEqual([g["giorno"] for g in e["vigilie"]], ["2024-12-24"])
        self.assertEqual(e["vigilie"][0]["terzi"][0], 100)
        self.assertNotIn("2024-01-01", [g["giorno"] for g in e["per_giorno"]])      # chiusura nota vuota: esclusa
        self.assertGreater(e["feriali_vuoti"], 200)                    # gli altri feriali sono file vuoti

    def test_quote_della_griglia_contano_i_giorni_sotto_soglia(self):
        e = T.esamina(self.cache, date(2024, 1, 8), date(2024, 1, 11))
        r = T.verifica_quote(e, quota_sessione=0.5, quota_terzo=0.25)   # soglie attuali del caricatore
        self.assertEqual(r["sotto"], ["2024-01-10", "2024-01-11"])     # il pomeridiano (terzo 1 vuoto) e il corto
        r2 = T.verifica_quote(e, quota_sessione=0.1, quota_terzo=0.1)
        self.assertEqual(r2["sotto"], ["2024-01-10", "2024-01-11"])    # terzi vuoti: cadono anche con soglie basse
        r3 = T.verifica_quote(e, quota_sessione=0.1, quota_terzo=0.0)
        self.assertEqual(r3["sotto"], [])                              # senza vincolo sui terzi passano tutti

    def test_rapporto_di_testo_senza_prezzi(self):
        e = T.esamina(self.cache, date(2024, 1, 8), date(2024, 1, 11))
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = T.main(["--cache", str(self.cache), "--inizio", "2024-01-08", "--fine", "2024-01-11"])
        testo = buf.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("525", testo)
        self.assertIn("2024-01-10", testo)                             # i giorni sotto la soglia attuale, elencati
        self.assertNotIn("2222", testo)                                # mai prezzi
        self.assertIn("percentil", testo)


if __name__ == "__main__":
    unittest.main()
