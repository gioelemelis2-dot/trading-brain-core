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


class TestRichiestaHttpR12bis(unittest.TestCase):
    """Rilievi R12-bis di Gemini (#52, #54) e difetto #58."""

    def test_retry_after_in_forma_di_data_non_fa_cadere(self):
        attese, n = [], []

        def apri(r, timeout):
            n.append(1)
            if len(n) == 1:
                raise urllib.error.HTTPError(r.full_url, 429, "Too Many", {"Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"}, None)
            if len(n) == 2:
                raise urllib.error.HTTPError(r.full_url, 503, "Busy", {"Retry-After": "boh"}, None)
            return _Risposta(b"ok")
        self.assertEqual(DK.richiesta_http("http://x", attesa=attese.append, apri=apri), (200, b"ok", 3))
        self.assertEqual(attese, [5.0, 10.0])            # data passata e valore illeggibile: attesa crescente normale

    def test_retry_after_data_futura(self):
        from email.utils import format_datetime
        from datetime import datetime, timedelta, timezone
        futuro = format_datetime(datetime.now(timezone.utc) + timedelta(seconds=120), usegmt=True)
        attese, n = [], []

        def apri(r, timeout):
            n.append(1)
            if len(n) == 1:
                raise urllib.error.HTTPError(r.full_url, 429, "Too Many", {"Retry-After": futuro}, None)
            return _Risposta(b"ok")
        DK.richiesta_http("http://x", attesa=attese.append, apri=apri)
        self.assertTrue(100 <= attese[0] <= 121, attese)

    def test_codice_vero_della_risposta(self):
        r = _Risposta(b"")
        r.status = 204
        self.assertEqual(DK.richiesta_http("http://x", apri=lambda q, timeout: r), (204, b"", 1))

    def test_impostazioni_risolte_alla_chiamata(self):
        """#58: sostituire urlopen e sleep del modulo deve bastare (prima restavano quelli fissati alla definizione)."""
        from unittest import mock
        chiamate = []

        def urlopen(r, timeout):
            chiamate.append(r.full_url)
            if len(chiamate) == 1:
                raise urllib.error.HTTPError(r.full_url, 500, "x", {}, None)
            return _Risposta(b"z")
        with mock.patch.object(DK.urllib.request, "urlopen", urlopen), mock.patch.object(DK.time, "sleep", lambda s: chiamate.append(s)):
            self.assertEqual(DK.richiesta_http("http://y"), (200, b"z", 2))
        self.assertEqual(chiamate, ["http://y", 5.0, "http://y"])


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
                if isinstance(r, tuple):
                    return r
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
        self.assertEqual(conta, {"in_cache": 1, "dati": 1, "404": 1, "vuoto-200": 0, "http": 0, "rovinati": 0,
                                 "registrati_dopo": 1})
        r = self.righe()                                                   # il 6/8 era in cache senza riga: registrato (#53)
        self.assertEqual([x["giorno"] for x in r], ["2009-06-08", "2009-06-09", "2009-06-10"])
        self.assertEqual([x["esito"] for x in r], ["in-cache-non-registrato", "dati", "404"])
        self.assertEqual(r[0]["sha256"], hashlib.sha256(bi5()).hexdigest())
        r = r[1:]
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

    def test_continua_su_errore_http_se_richiesto(self):
        """Con continua_su_http un errore HTTP sconosciuto si registra, il giorno resta SENZA file (quindi «mancante»
        per il controllo della cache) e si va avanti; ci si ferma dopo troppi errori di fila (blocco vero)."""
        errore = urllib.error.HTTPError("u", 403, "Forbidden", {}, None)
        finta = Finta({date(2009, 6, 8): errore, date(2009, 6, 9): bi5(), date(2009, 6, 10): errore})
        conta = SC.scarica_periodo("XAUUSD", "ASK", date(2009, 6, 8), date(2009, 6, 10), self.cache, self.registro,
                                   richiesta=finta, pausa=lambda: None, stampa=lambda *a, **k: None,
                                   continua_su_http=True)
        self.assertEqual(conta["http"], 2)
        self.assertFalse((self.cache / "2009-06-08.bi5").exists())
        self.assertTrue((self.cache / "2009-06-09.bi5").exists())
        self.assertEqual([x["esito"] for x in self.righe()], ["http-403", "dati", "http-403"])
        tutti = Finta({date(2009, 7, 1) + __import__("datetime").timedelta(days=k): errore for k in range(30)})
        with self.assertRaises(SC.Fermo) as e:
            SC.scarica_periodo("XAUUSD", "ASK", date(2009, 7, 1), date(2009, 7, 30), self.cache, self.registro,
                               richiesta=tutti, pausa=lambda: None, stampa=lambda *a, **k: None,
                               continua_su_http=True)
        self.assertIn("20 errori HTTP di fila", str(e.exception))
        self.assertEqual(len(tutti.chiamate), 20)

    def test_uscita_della_riga_di_comando_con_errori_http(self):
        """Finito ma con giorni in errore: codice 5, così lo script non lo scambia per un successo pieno."""
        from unittest import mock
        errore = urllib.error.HTTPError("u", 403, "Forbidden", {}, None)
        finta = Finta({date(2009, 6, 8): errore})
        with mock.patch.object(SC.DK, "richiesta_http", finta), mock.patch.object(SC.time, "sleep", lambda s: None):
            rc = SC.main(["--lato", "ASK", "--inizio", "2009-06-08", "--fine", "2009-06-09", "--cache", str(self.radice),
                          "--continua-su-http"])
        self.assertEqual(rc, 5)
        self.assertEqual(len(finta.chiamate), 2)          # la risposta finta è stata usata: nessuna richiesta vera in rete

    def test_un_giorno_buono_azzera_gli_errori_di_fila(self):
        """19 errori, un giorno buono, altri 19 errori: nessun blocco vero, si arriva in fondo."""
        from datetime import timedelta
        errore = urllib.error.HTTPError("u", 403, "Forbidden", {}, None)
        d0 = date(2009, 7, 1)
        risposte = {d0 + timedelta(days=k): (bi5() if k == 19 else errore) for k in range(39)}
        conta = SC.scarica_periodo("XAUUSD", "ASK", d0, d0 + timedelta(days=38), self.cache, self.registro,
                                   richiesta=Finta(risposte), pausa=lambda: None, stampa=lambda *a, **k: None,
                                   continua_su_http=True)
        self.assertEqual((conta["http"], conta["dati"]), (38, 1))

    def test_scrittura_forzata_su_disco_anche_della_cartella(self):
        """Difetto #47: su macOS fsync non basta (serve F_FULLFSYNC) e senza forzare la cartella lo spostamento può
        sparire a uno spegnimento improvviso: il 16/11 sono andati persi 20 giorni già scaricati."""
        from unittest import mock
        forzati = []
        with mock.patch.object(SC, "_forza", lambda fd: forzati.append(SC.os.fstat(fd).st_mode)):
            self.cache.mkdir(parents=True)
            SC._scrivi_atomico(self.cache / "2009-06-08.bi5", b"x")
            SC._registra(self.registro, {k: "" for k in SC.CAMPI})
        import stat
        self.assertEqual([stat.S_ISDIR(m) for m in forzati], [False, True, False])   # file, cartella, registro

    def test_forza_usa_fullfsync_se_c_e_altrimenti_fsync(self):
        from unittest import mock
        chiamate = []
        finto = type("F", (), {"F_FULLFSYNC": 51, "fcntl": staticmethod(lambda fd, op: chiamate.append(("full", op)))})
        with mock.patch.object(SC, "fcntl", finto), mock.patch.object(SC.os, "fsync", lambda fd: chiamate.append(("fsync",))):
            SC._forza(3)
        self.assertEqual(chiamate, [("full", 51)])
        chiamate.clear()

        def rifiuta(fd, op):
            raise OSError("non supportato")
        finto2 = type("F", (), {"F_FULLFSYNC": 51, "fcntl": staticmethod(rifiuta)})
        with mock.patch.object(SC, "fcntl", finto2), mock.patch.object(SC.os, "fsync", lambda fd: chiamate.append(("fsync",))):
            SC._forza(3)
        self.assertEqual(chiamate, [("fsync",)])
        chiamate.clear()
        with mock.patch.object(SC, "fcntl", type("F", (), {})), mock.patch.object(SC.os, "fsync", lambda fd: chiamate.append(("fsync",))):
            SC._forza(3)                                                  # Linux: niente F_FULLFSYNC
        self.assertEqual(chiamate, [("fsync",)])

    def test_ripresa_dopo_interruzione_registra_e_controlla_i_file_in_cache(self):
        """#53 (R12bis-B-02): file in cache senza riga di registro; file rovinato in cache (spegnimento del 16/11)."""
        self.cache.mkdir(parents=True)
        (self.cache / "2009-06-08.bi5").write_bytes(bi5())                      # buono, mai registrato
        (self.cache / "2009-06-09.bi5").write_bytes(b"rovinato")                # rovinato
        self.scarica(Finta({}), fine=date(2009, 6, 8))                          # prima registrazione
        conta = self.scarica(Finta({date(2009, 6, 9): bi5(4)}), fine=date(2009, 6, 9))
        self.assertEqual((conta["registrati_dopo"], conta["rovinati"], conta["dati"]), (0, 1, 1))   # 6/8 già registrato
        self.assertEqual((self.cache / "2009-06-09.bi5").read_bytes(), bi5(4))                    # riscaricato
        self.assertEqual((self.cache / ".2009-06-09.rovinato").read_bytes(), b"rovinato")         # conservato, non cancellato
        self.assertEqual([(x["giorno"], x["esito"]) for x in self.righe()],
                         [("2009-06-08", "in-cache-non-registrato"), ("2009-06-09", "rovinato-in-cache"), ("2009-06-09", "dati")])

    def test_codici_diversi_registrati_come_sono(self):
        """#54: 204 non diventa «vuoto-200»; un 2xx diverso con contenuto non entra in cache."""
        conta = self.scarica(Finta({date(2009, 6, 8): (204, b"", 1)}), fine=date(2009, 6, 8))
        self.assertEqual(self.righe()[0]["esito"], "vuoto-204")
        self.assertEqual(conta["vuoto-204"], 1)
        with self.assertRaises(SC.Fermo):
            self.scarica(Finta({date(2009, 6, 9): (206, bi5(), 1)}), inizio=date(2009, 6, 9), fine=date(2009, 6, 9))
        self.assertFalse((self.cache / "2009-06-09.bi5").exists())

    def test_pausa_negativa_codice_2(self):
        self.assertEqual(SC.main(["--inizio", "2009-06-08", "--fine", "2009-06-08", "--cache", str(self.radice),
                                  "--pausa", "-1"]), 2)
        self.assertFalse(self.registro.exists())

    def test_riprova_i_giorni_feriali_vuoti_solo_se_richiesto(self):
        """#55: un 404 temporaneo lasciava il giorno vuoto per sempre."""
        self.cache.mkdir(parents=True)
        for g in ("2009-06-06", "2009-06-08"):                                   # sabato e lunedì, vuoti
            (self.cache / f"{g}.bi5").write_bytes(b"")
        finta = Finta({date(2009, 6, 8): bi5()})
        self.scarica(finta, inizio=date(2009, 6, 6), fine=date(2009, 6, 8))
        self.assertEqual(finta.chiamate, [DK.url_giorno("XAUUSD", date(2009, 6, 7))])   # senza opzione: solo il mancante
        finta = Finta({date(2009, 6, 8): bi5()})
        SC.scarica_periodo("XAUUSD", "BID", date(2009, 6, 6), date(2009, 6, 8), self.cache, self.registro,
                           richiesta=finta, pausa=lambda: None, stampa=lambda *a, **k: None, riprova_vuoti=True)
        self.assertEqual(finta.chiamate, [DK.url_giorno("XAUUSD", date(2009, 6, 8))])   # il sabato no, il lunedì sì
        self.assertEqual((self.cache / "2009-06-08.bi5").read_bytes(), bi5())

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
