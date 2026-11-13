"""Test offline di brain/dati/pipeline/dukascopy.py (Gate 2): nessuna rete, file .bi5 costruiti nel formato atteso.
Uso (dalla radice del repository): python3 -s -B -W error -m unittest brain.dati.tests.test_dukascopy
"""
import hashlib
import io
import json
import lzma
import os
import struct
import sys
import tempfile
import unittest
import urllib.error
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal as D
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.dati.pipeline import dukascopy as DK                      # noqa: E402

UTC = timezone.utc


def bi5(minuti):
    """minuti: (secondi dall'inizio del giorno, open, close, low, high, volume), prezzi in millesimi di USD."""
    return lzma.compress(b"".join(DK.RECORD.pack(*m) for m in minuti), format=lzma.FORMAT_ALONE)


GIORNO_DI_MERCATO = list(range(0, 21 * 60)) + list(range(22 * 60, 24 * 60))   # pausa 21:00-22:00 UTC


def giornata(base=2650000, minuti=GIORNO_DI_MERCATO, salto=()):
    """Minuti di scambio (predefinito: tutto il giorno tranne la pausa giornaliera 21:00-22:00 UTC), con prezzi
    plausibili per l'oro. `salto`: minuti senza scambi (volume 0) per creare buchi."""
    out = []
    for m in minuti:
        p = base + m
        vol = 0.0 if m in salto else 1.25
        out.append((m * 60, p, p + 2, p - 3, p + 5, vol))
    return out


class TestDecodificaEAggregazione(unittest.TestCase):
    def test_decodifica_scala_e_minuti_senza_scambi(self):
        g = date(2026, 1, 5)
        m = DK.decodifica(bi5([(0, 2650123, 2650456, 2650000, 2650500, 1.5), (60, 2650456, 2650456, 2650456,
                                                                                2650456, 0.0)]), g, 3)
        self.assertEqual(len(m), 1)                                   # il minuto a volume 0 è scartato
        t, o, h, lo, c, v = m[0]
        self.assertEqual((t, o, h, lo, c, v), (datetime(2026, 1, 5, tzinfo=UTC), D("2650.123"), D("2650.500"),
                                                D("2650.000"), D("2650.456"), D("1.5")))

    def test_record_non_validi_fermano(self):
        """Rilievo di Gemini G3-06: secondi fuori dal giorno, prezzi non positivi o volume non finito sono errori di
        dati (ErroreDati), non eccezioni generiche né minuti accettati."""
        p = 2650000
        for rec in ((86400, p, p, p - 3, p + 5, 1.0), (-60, p, p, p - 3, p + 5, 1.0), (60, 0, 0, 0, 0, 1.0),
                    (60, p, p, p - 3, p + 5, float("nan")), (60, p, p, p - 3, p + 5, float("inf"))):
            with self.assertRaises(DK.ErroreDati, msg=repr(rec)):
                DK.decodifica(bi5([rec]), date(2026, 1, 5), 3)

    def test_campi_in_ordine_diverso_o_file_troncato_fermano(self):
        g = date(2026, 1, 5)
        with self.assertRaises(DK.ErroreDati):                        # low sopra high: ordine dei campi sbagliato
            DK.decodifica(bi5([(0, 2650000, 2650100, 2650500, 2649000, 1.0)]), g, 3)
        with self.assertRaises(DK.ErroreDati):
            DK.decodifica(lzma.compress(b"\x00" * 23, format=lzma.FORMAT_ALONE), g, 3)

    def test_aggregazione_15_minuti(self):
        g = date(2026, 1, 5)
        m = DK.decodifica(bi5(giornata(minuti=range(30))), g, 3)
        c = DK.aggrega(m)
        self.assertEqual(len(c), 2)
        a = c[0]
        self.assertEqual(a["open_time"], datetime(2026, 1, 5, 0, 0, tzinfo=UTC))
        self.assertEqual(a["close_time"], datetime(2026, 1, 5, 0, 15, tzinfo=UTC))
        self.assertEqual(a["open"], D("2650.000"))                    # open del primo minuto
        self.assertEqual(a["close"], D("2650.016"))                   # close dell'ultimo (minuto 14: 2650014 + 2)
        self.assertEqual(a["high"], D("2650.019"))                    # massimo degli high (minuto 14: + 5)
        self.assertEqual(a["low"], D("2649.997"))                     # minimo dei low (minuto 0: - 3)
        self.assertEqual(a["volume"], D("18.75"))                     # 15 × 1,25


class TestControlli(unittest.TestCase):
    def candela(self, t, prezzo=D("2650")):
        return {"open_time": t, "close_time": t + DK.QUINDICI, "open": prezzo, "high": prezzo + 1,
                "low": prezzo - 1, "close": prezzo, "volume": D(1)}

    def test_scala_sbagliata_ferma(self):
        """Una scala ×10 o ÷10 esce dalla banda plausibile dell'anno: 2026 (265 / 26.500 USD) e 2004 (40 / 4.000)."""
        for t, prezzi in ((datetime(2026, 1, 5, tzinfo=UTC), (D("265"), D("26500"))),
                          (datetime(2004, 3, 10, tzinfo=UTC), (D("40"), D("4000")))):
            for p in prezzi:
                with self.assertRaises(DK.ErroreDati, msg=f"{t.year} {p}"):
                    DK.controlla([self.candela(t, p)])

    def test_bande_per_periodo(self):
        """Rilievo di Gemini G-20261113-01: con il limite fisso 1.000 USD gli anni prima del 2010 erano esclusi.
        L'oro a 400 USD nel 2004 e a 1.300 nel 2017 è plausibile; un anno senza banda ferma (va aggiunta, a mano)."""
        DK.controlla([self.candela(datetime(2004, 3, 10, tzinfo=UTC), D("400"))])
        DK.controlla([self.candela(datetime(2017, 6, 1, tzinfo=UTC), D("1300"))])
        with self.assertRaises(DK.ErroreDati) as e:
            DK.controlla([self.candela(datetime(1999, 6, 1, tzinfo=UTC), D("280"))])
        self.assertIn("nessuna banda", str(e.exception))
        with self.assertRaises(DK.ErroreDati):
            DK.controlla([self.candela(datetime(2026, 1, 5, tzinfo=UTC))], simbolo="EURUSD")

    def test_salto_di_scala_fra_candele_ferma(self):
        """Un giorno decodificato con la scala sbagliata può restare nella banda: lo scopre il salto fra due candele
        consecutive (oltre il 25%). Un movimento forte ma reale (5%) passa."""
        t = datetime(2026, 1, 5, 10, tzinfo=UTC)
        DK.controlla([self.candela(t, D("2650")), self.candela(t + DK.QUINDICI, D("2782.5"))])
        for p in (D("3400"), D("2000")):
            with self.assertRaises(DK.ErroreDati, msg=str(p)) as e:
                DK.controlla([self.candela(t, D("2650")), self.candela(t + DK.QUINDICI, p)])
            self.assertIn("salto", str(e.exception))

    def test_buchi_classificati(self):
        ven = datetime(2026, 1, 9, 20, 45, tzinfo=UTC)                 # venerdì, ultima candela
        dom = datetime(2026, 1, 11, 23, 0, tzinfo=UTC)                 # domenica sera: riapertura
        candele = [self.candela(ven)] + [self.candela(dom + i * DK.QUINDICI) for i in range(88)]   # fino a lun 21:00
        lun_22 = datetime(2026, 1, 12, 22, 0, tzinfo=UTC)               # pausa giornaliera 21:00-22:00
        candele += [self.candela(lun_22), self.candela(lun_22 + DK.QUINDICI)]
        candele += [self.candela(datetime(2026, 1, 13, 2, 0, tzinfo=UTC))]   # 22:30 -> 02:00: chiusura lunga
        r = DK.controlla(candele)
        self.assertEqual(r["buchi_per_tipo"], {"fine settimana": 1, "pausa giornaliera": 1,
                                               "festività o chiusura lunga (da verificare)": 1})
        self.assertEqual(r["anomali"], 0)
        self.assertEqual(len(r["buchi_da_verificare"]), 1)
        # Domenica 23:15 -> martedì 20:45: copre il lunedì, NON è un fine settimana
        self.assertNotEqual(DK.classifica_buco(datetime(2026, 1, 11, 23, 15, tzinfo=UTC),
                                               datetime(2026, 1, 13, 20, 45, tzinfo=UTC)), "fine settimana")
        buco = [self.candela(datetime(2026, 1, 14, 10, 0, tzinfo=UTC)),
                self.candela(datetime(2026, 1, 14, 10, 45, tzinfo=UTC))]                    # 30 minuti alle 10:15
        self.assertEqual(DK.controlla(buco)["anomali"], 1)

    def test_buco_lungo_di_giorno_e_anomalo(self):
        """Rilievo di Gemini G3-03: un buco di 2 ore e 15 minuti alle 10:00 UTC di mercoledì non è una festività.
        Le chiusure lunghe accettate cominciano la sera (dalle 17:00 UTC: chiusure anticipate dei festivi USA, Natale,
        Capodanno), come le 22 trovate nei dati reali del 2023–2026."""
        mer = datetime(2026, 1, 7, 10, 0, tzinfo=UTC)
        self.assertTrue(DK.classifica_buco(mer, mer + timedelta(hours=2, minutes=15)).startswith("ANOMALO"))
        for da, a in ((datetime(2025, 11, 27, 19, 30, tzinfo=UTC), datetime(2025, 11, 27, 23, 0, tzinfo=UTC)),
                      (datetime(2025, 12, 24, 18, 45, tzinfo=UTC), datetime(2025, 12, 25, 23, 0, tzinfo=UTC)),
                      (datetime(2025, 12, 31, 22, 0, tzinfo=UTC), datetime(2026, 1, 1, 23, 0, tzinfo=UTC)),
                      (datetime(2024, 5, 27, 18, 30, tzinfo=UTC), datetime(2024, 5, 27, 22, 0, tzinfo=UTC))):
            self.assertEqual(DK.classifica_buco(da, a), "festività o chiusura lunga (da verificare)", da)
        self.assertTrue(DK.classifica_buco(datetime(2026, 1, 7, 16, 45, tzinfo=UTC),
                                           datetime(2026, 1, 7, 19, 0, tzinfo=UTC)).startswith("ANOMALO"))

    def test_ampiezza_dentro_la_candela_ferma(self):
        """Rilievo di Gemini G3-03: un picco dentro la candela (massimo 9.999 con apertura e chiusura a 2.650) resta
        nella banda dell'anno ma è un errore di dati. Oltre il 25% fra massimo e minimo ci si ferma."""
        t = datetime(2026, 1, 5, 10, tzinfo=UTC)
        c = dict(self.candela(t), high=D("9999"))
        with self.assertRaises(DK.ErroreDati) as e:
            DK.controlla([c])
        self.assertIn("ampiezza", str(e.exception))
        DK.controlla([dict(self.candela(t), high=D("2700"), low=D("2600"))])

    def test_ordine_non_crescente_ferma(self):
        t = datetime(2026, 1, 5, 10, tzinfo=UTC)
        with self.assertRaises(DK.ErroreDati):
            DK.controlla([self.candela(t), self.candela(t - DK.QUINDICI)])


class _Risposta(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()


class TestScaricamentoEPipeline(unittest.TestCase):
    def test_url_mese_da_zero_e_nuovo_tentativo_su_429(self):
        self.assertEqual(DK.url_giorno("XAUUSD", date(2026, 1, 5)),
                         "https://datafeed.dukascopy.com/datafeed/XAUUSD/2026/00/05/BID_candles_min_1.bi5")
        chiamate, attese = [], []

        def apri(richiesta, timeout):
            chiamate.append(richiesta.get_header("User-agent"))
            if len(chiamate) == 1:
                raise urllib.error.HTTPError(richiesta.full_url, 429, "Too Many Requests", {"Retry-After": "30"}, None)
            return _Risposta(b"dati")

        self.assertEqual(DK.scarica_http("http://x", attesa=attese.append, apri=apri), b"dati")
        self.assertEqual(attese, [30.0])                                 # Retry-After rispettato

        def apri_sempre_429(richiesta, timeout):
            raise urllib.error.HTTPError(richiesta.full_url, 429, "Too Many Requests", {}, None)
        attese.clear()
        with self.assertRaises(ConnectionError):
            DK.scarica_http("http://x", attesa=attese.append, apri=apri_sempre_429)
        self.assertEqual(attese, [5.0, 10.0, 20.0, 40.0, 80.0, 160.0, 300.0, 300.0, 300.0, 300.0])   # ~25 minuti

        def scarica_rotto(url):
            raise ConnectionError(url)
        with self.assertRaisesRegex(ConnectionError, r"giorno 2026-09-20 .*2026/08/20"):       # data vera e URL
            DK.scarica_giorno("XAUUSD", date(2026, 9, 20), None, scarica_rotto)
        self.assertEqual(chiamate[0], "trading-brain-dati/1.0")        # nessun dato personale nell'User-Agent

        # Timeout di lettura e risposte troncate: su Python 3.9 socket.timeout NON è un TimeoutError (lo è dalla 3.10),
        # e http.client.IncompleteRead non è un errore di urllib. Devono essere nuovi tentativi, non un crash.
        import http.client
        import socket
        for errore in (socket.timeout("The read operation timed out"), http.client.IncompleteRead(b"x"),
                       ConnectionResetError("reset")):
            chiamate.clear()
            attese.clear()

            def apri_lento(richiesta, timeout, errore=errore):
                chiamate.append(1)
                if len(chiamate) == 1:
                    raise errore
                return _Risposta(b"ok")
            self.assertEqual(DK.scarica_http("http://x", attesa=attese.append, apri=apri_lento), b"ok", repr(errore))
            self.assertEqual(attese, [5.0])

        def apri_404(richiesta, timeout):
            raise urllib.error.HTTPError(richiesta.full_url, 404, "Not Found", {}, None)
        self.assertIsNone(DK.scarica_http("http://x", attesa=attese.append, apri=apri_404))

    def scarica_finta(self, richieste):
        giorni = {date(2026, 1, 5) + timedelta(days=i): bi5(giornata()) for i in range(5)}

        def scarica(url):
            richieste.append(url)
            for g, dati in giorni.items():
                if url == DK.url_giorno("XAUUSD", g):
                    return dati
            return None
        return scarica

    def test_pipeline_senza_partizione_non_sigilla(self):
        """Senza partizione decisa (DA-26) si scaricano e controllano i dati, ma non si sigilla nulla: niente più 70/30
        per numero di candele. La cache è usata al secondo giro."""
        richieste = []
        scarica = self.scarica_finta(richieste)
        with tempfile.TemporaryDirectory() as tmp:
            reali, nonce, cache = Path(tmp) / "reali", Path(tmp) / "fuori" / "nonce", Path(tmp) / "cache"
            meta = DK.esegui("XAUUSD", date(2026, 1, 5), date(2026, 1, 11), reali, nonce, scarica, cache,
                             pausa=lambda: None, stampa=lambda *a: None)
            self.assertEqual(meta["candele_15m"], 5 * 23 * 4)            # 23 ore di mercato al giorno
            self.assertEqual(meta["giorni_senza_dati"], 2)              # sabato e domenica
            self.assertEqual(meta["controlli"], {"buchi_per_tipo": {"pausa giornaliera": 5},
                                                 "buchi_da_verificare": [], "anomali": 0})
            self.assertIn("non decisa", meta["partizione"])
            self.assertNotIn("in_sample", meta)
            self.assertFalse((reali / "partizioni").exists())
            self.assertFalse(nonce.exists())
            self.assertTrue((reali / "XAUUSD_15m.meta.json").exists())
            n = len(richieste)
            DK.esegui("XAUUSD", date(2026, 1, 5), date(2026, 1, 11), reali, nonce, scarica, cache,
                      pausa=lambda: None, stampa=lambda *a: None)
            self.assertEqual(len(richieste), n)                          # tutto dalla cache

    def test_pipeline_con_partizione_per_date(self):
        """Sviluppo 5–6 gennaio, embargo il 7, verifica 8–9: 184 + 184 candele, 92 escluse; sigillo verificabile,
        nonce fuori dalla cartella dei dati."""
        from brain.dati.pipeline import partizione_date as PD
        part = {"schema": PD.SCHEMA, "simbolo": "XAUUSD", "embargo_giorni": 1, "blocco": [
            {"nome": "sviluppo", "ruolo": "sviluppo", "inizio": "2026-01-05", "fine": "2026-01-07"},
            {"nome": "verifica", "ruolo": "verifica", "inizio": "2026-01-08", "fine": "2026-01-10"}]}
        with tempfile.TemporaryDirectory() as tmp:
            reali, nonce = Path(tmp) / "reali", Path(tmp) / "fuori" / "nonce"
            meta = DK.esegui("XAUUSD", date(2026, 1, 5), date(2026, 1, 9), reali, nonce, self.scarica_finta([]), None,
                             pausa=lambda: None, stampa=lambda *a: None, partizione=part, partizione_sha256="cd" * 32)
            self.assertEqual({b["nome"]: b["candele"] for b in meta["partizione"]["blocchi"]},
                             {"sviluppo": 184, "verifica": 184})
            self.assertEqual(meta["partizione"]["candele_escluse"], 92)
            cartella = reali / "partizioni" / "XAUUSD_15m_date"
            self.assertEqual(meta["partizione"]["commitment_json_sha256"],
                             hashlib.sha256((cartella / "commitment.json").read_bytes()).hexdigest())
            self.assertTrue(PD.verifica(cartella, nonce / "sealed_nonce.secret", part, "cd" * 32)["valido"])
            self.assertFalse((cartella / "sealed_nonce.secret").exists())

    def test_nonce_esistente_ferma_prima_di_scrivere(self):
        """Rilievo di Gemini G3-04: con un nonce già presente ci si ferma PRIMA di scaricare e di scrivere il CSV,
        non dopo averlo sovrascritto."""
        from brain.dati.pipeline import partizione_date as PD
        part = {"schema": PD.SCHEMA, "simbolo": "XAUUSD", "embargo_giorni": 1, "blocco": [
            {"nome": "sviluppo", "ruolo": "sviluppo", "inizio": "2026-01-05", "fine": "2026-01-07"},
            {"nome": "verifica", "ruolo": "verifica", "inizio": "2026-01-08", "fine": "2026-01-10"}]}
        richieste = []
        with tempfile.TemporaryDirectory() as tmp:
            reali, nonce = Path(tmp) / "reali", Path(tmp) / "fuori" / "nonce"
            nonce.mkdir(parents=True)
            (nonce / PD.NONCE).write_text("vecchio\n", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                DK.esegui("XAUUSD", date(2026, 1, 5), date(2026, 1, 9), reali, nonce, self.scarica_finta(richieste),
                          None, pausa=lambda: None, stampa=lambda *a: None, partizione=part, partizione_sha256="cd" * 32)
            self.assertEqual(richieste, [])
            self.assertFalse((reali / "XAUUSD_15m.csv").exists())
            self.assertEqual((nonce / PD.NONCE).read_text(encoding="utf-8"), "vecchio\n")

    def test_periodo_dalla_partizione(self):
        from brain.dati.pipeline import partizione_date as PD
        part = {"schema": PD.SCHEMA, "simbolo": "XAUUSD", "embargo_giorni": 14, "blocco": [
            {"nome": "vecchia", "ruolo": "verifica", "inizio": "2010-01-01", "fine": "2013-01-01"},
            {"nome": "sviluppo", "ruolo": "sviluppo", "inizio": "2013-01-15", "fine": "2024-01-01"}]}
        self.assertEqual(DK.periodo_da_partizione(part), (date(2010, 1, 1), date(2023, 12, 31)))

    def test_buco_anomalo_ferma_salvo_accetta_buchi(self):
        dati = bi5(giornata(salto=range(600, 630)))                     # 10:00-10:30 senza scambi
        with tempfile.TemporaryDirectory() as tmp:
            reali, nonce = Path(tmp) / "reali", Path(tmp) / "nonce"
            args = ("XAUUSD", date(2026, 1, 5), date(2026, 1, 5), reali, nonce, lambda url: dati, None)
            with self.assertRaises(DK.ErroreDati):
                DK.esegui(*args, pausa=lambda: None, stampa=lambda *a: None)
            self.assertFalse((reali / "XAUUSD_15m.csv").exists())        # nessun file scritto se ci si ferma
            meta = DK.esegui(*args, accetta_buchi=True, pausa=lambda: None, stampa=lambda *a: None)
            self.assertEqual(meta["controlli"]["anomali"], 1)


if __name__ == "__main__":
    unittest.main()
