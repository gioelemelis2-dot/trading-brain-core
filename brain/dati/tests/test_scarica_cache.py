"""Test dello scaricatore «solo cache» (dati/pipeline/scarica_cache.py) e degli esiti HTTP distinti
(dukascopy.richiesta_http), scritti PRIMA del codice. Nessuna rete: le risposte sono finte.
Uso (dalla radice del repository): python3 -s -B -W error -m unittest brain.dati.tests.test_scarica_cache
"""
import csv
import hashlib
import lzma
import sys
import tempfile
import unittest
import urllib.error
from datetime import date
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.dati.pipeline import dukascopy as DK                       # noqa: E402
from brain.dati.pipeline import scarica_cache as SC                   # noqa: E402


def bi5(n=3):
    return lzma.compress(b"".join(DK.RECORD.pack(60 * k, 2000000, 2000001, 1999999, 2000002, 1.0) for k in range(n)),
                         format=lzma.FORMAT_ALONE)


class _Risposta:
    def __init__(self, dati):
        self.dati = dati

    def read(self):
        return self.dati

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class TestRichiestaHttp(unittest.TestCase):
    """DGS-04, richiesta 1 a Claude: 404, risposta 200 vuota e guasto devono essere distinguibili."""

    def test_tre_esiti_distinti(self):
        self.assertEqual(DK.richiesta_http("http://x", apri=lambda r, timeout: _Risposta(b"abc")), (200, b"abc", 1))
        self.assertEqual(DK.richiesta_http("http://x", apri=lambda r, timeout: _Risposta(b"")), (200, b"", 1))

        def apri_404(r, timeout):
            raise urllib.error.HTTPError(r.full_url, 404, "Not Found", {}, None)
        self.assertEqual(DK.richiesta_http("http://x", attesa=lambda s: None, apri=apri_404), (404, None, 1))

        def apri_500(r, timeout):
            raise urllib.error.HTTPError(r.full_url, 500, "Errore", {}, None)
        with self.assertRaises(ConnectionError):
            DK.richiesta_http("http://x", tentativi=3, attesa=lambda s: None, apri=apri_500)

        def apri_403(r, timeout):
            raise urllib.error.HTTPError(r.full_url, 403, "Forbidden", {}, None)
        with self.assertRaises(urllib.error.HTTPError):                        # subito, senza nuovi tentativi
            DK.richiesta_http("http://x", tentativi=3, attesa=lambda s: None, apri=apri_403)

    def test_tentativi_contati_e_vecchia_interfaccia_invariata(self):
        n = []

        def apri(r, timeout):
            n.append(1)
            if len(n) < 3:
                raise urllib.error.HTTPError(r.full_url, 429, "Too Many", {}, None)
            return _Risposta(b"ok")
        self.assertEqual(DK.richiesta_http("http://x", attesa=lambda s: None, apri=apri), (200, b"ok", 3))
        self.assertIsNone(DK.scarica_http("http://x", apri=lambda r, timeout: _Risposta(b"")))     # come prima


class Finta:
    """Risposte per giorno: bytes (200), None (404), b"" (200 vuoto), oppure un'eccezione da sollevare."""

    def __init__(self, risposte):
        self.risposte, self.chiamate = risposte, []

    def __call__(self, url):
        self.chiamate.append(url)
        for g, r in self.risposte.items():
            if url == DK.url_giorno("XAUUSD", g, "ASK") or url == DK.url_giorno("XAUUSD", g):
                if isinstance(r, Exception):
                    raise r
                return (404, None, 1) if r is None else (200, r, 2)
        return (404, None, 1)


class TestScaricaCache(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.radice = Path(self._tmp.name) / "cache_dukascopy"
        self.cache = self.radice / "XAUUSD"
        self.registro = self.radice / "registro.csv"
        self.pause = []

    def tearDown(self):
        self._tmp.cleanup()

    def scarica(self, finta, inizio=date(2009, 6, 8), fine=date(2009, 6, 10), lato="BID"):
        return SC.scarica_periodo("XAUUSD", lato, inizio, fine, self.cache, self.registro, richiesta=finta,
                                  pausa=lambda: self.pause.append(1), stampa=lambda *a, **k: None)

    def righe(self):
        with open(self.registro, encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def test_salta_la_cache_senza_attese_e_registra_gli_esiti(self):
        self.cache.mkdir(parents=True)
        (self.cache / "2009-06-08.bi5").write_bytes(bi5())                   # già in cache
        dati = bi5(5)
        finta = Finta({date(2009, 6, 9): dati, date(2009, 6, 10): None})
        conta = self.scarica(finta)
        self.assertEqual(len(finta.chiamate), 2)                              # il 6/8 non si richiede
        self.assertEqual(len(self.pause), 2)                                  # e non si aspetta
        self.assertEqual((self.cache / "2009-06-09.bi5").read_bytes(), dati)
        self.assertEqual((self.cache / "2009-06-10.bi5").read_bytes(), b"")
        self.assertEqual(conta, {"in_cache": 1, "dati": 1, "404": 1, "vuoto-200": 0})
        r = self.righe()
        self.assertEqual([x["giorno"] for x in r], ["2009-06-09", "2009-06-10"])
        self.assertEqual([x["esito"] for x in r], ["dati", "404"])
        self.assertEqual(r[0]["sha256"], hashlib.sha256(dati).hexdigest())
        self.assertEqual((r[0]["byte"], r[0]["tentativi"], r[0]["http"]), (str(len(dati)), "2", "200"))
        self.assertEqual(r[0]["lato"], "BID")
        self.assertEqual(list(self.cache.glob(".*.tmp")), [])

    def test_risposta_200_vuota_distinta_dal_404(self):
        self.scarica(Finta({date(2009, 6, 8): b""}), fine=date(2009, 6, 8))
        self.assertEqual(self.righe()[0]["esito"], "vuoto-200")
        self.assertEqual((self.cache / "2009-06-08.bi5").read_bytes(), b"")

    def test_errore_http_sconosciuto_ferma_senza_scrivere_il_giorno(self):
        errore = urllib.error.HTTPError("u", 403, "Forbidden", {}, None)
        finta = Finta({date(2009, 6, 8): bi5(), date(2009, 6, 9): errore})
        with self.assertRaises(SC.Fermo) as e:
            self.scarica(finta)
        self.assertIn("403", str(e.exception))
        self.assertIn("2009-06-09", str(e.exception))
        self.assertTrue((self.cache / "2009-06-08.bi5").exists())
        self.assertFalse((self.cache / "2009-06-09.bi5").exists())
        self.assertEqual([x["esito"] for x in self.righe()], ["dati", "http-403"])     # registro già scritto

    def test_file_danneggiato_dal_server_non_entra_in_cache(self):
        with self.assertRaises(SC.Fermo):
            self.scarica(Finta({date(2009, 6, 8): b"non lzma"}), fine=date(2009, 6, 8))
        self.assertFalse((self.cache / "2009-06-08.bi5").exists())
        self.assertEqual(self.righe()[0]["esito"], "danneggiato")

    def test_rete_assente_ferma_con_codice_di_ripresa(self):
        with self.assertRaises(ConnectionError):
            self.scarica(Finta({date(2009, 6, 8): ConnectionError("giù")}), fine=date(2009, 6, 8))
        self.assertEqual(self.righe()[0]["esito"], "nessuna-risposta")
        self.assertFalse((self.cache / "2009-06-08.bi5").exists())

    def test_lato_ask_e_registro_che_continua(self):
        self.cache = self.radice / "XAUUSD_ASK"
        self.scarica(Finta({date(2009, 6, 8): bi5()}), fine=date(2009, 6, 8), lato="ASK")
        self.scarica(Finta({date(2009, 6, 9): bi5()}), inizio=date(2009, 6, 9), fine=date(2009, 6, 9), lato="ASK")
        r = self.righe()
        self.assertEqual([(x["giorno"], x["lato"]) for x in r], [("2009-06-08", "ASK"), ("2009-06-09", "ASK")])
        self.assertTrue(r[0]["url"].endswith("ASK_candles_min_1.bi5"))

    def test_riga_di_comando(self):
        self.assertEqual(SC.main(["--inizio", "2009-06-10", "--fine", "2009-06-08", "--cache", str(self.radice)]), 2)
        self.assertFalse(self.registro.exists())


if __name__ == "__main__":
    unittest.main()
