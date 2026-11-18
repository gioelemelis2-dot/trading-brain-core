"""Test del rendiconto dell'intersezione BID/ASK e dei buchi (studi/intersezione_bid_ask.py), scritti PRIMA del
codice (17/11/2026, richiesta del DGS in DGS-05 P5: «i due strumenti non bastano a dimostrare l'intersezione al
minuto»). Strumento di contorno, fuori dal candidato sigillato. SOLO conteggi e date, mai prezzi. Dati inventati.
Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_intersezione_bid_ask
"""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date, time as ora_t, timedelta
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.laboratorio.esecuzione import sintetico as SN               # noqa: E402
from brain.laboratorio.simulatori.orb_londra import _utc               # noqa: E402
from brain.laboratorio.studi import intersezione_bid_ask as X          # noqa: E402

PREZZO = 2345.678                                                     # non deve mai comparire nell'uscita


def _minuti(giorno, quanti, dalle=ora_t(8, 0), prezzo=PREZZO):
    t0 = _utc(giorno, dalle)
    return {t0 + timedelta(minutes=k): (prezzo, prezzo + 0.5, prezzo - 0.5, prezzo) for k in range(quanti)}


class Base(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.cache = Path(self._t.name)
        self.bid, self.ask = {}, {}

    def tearDown(self):
        self._t.cleanup()

    def giorno(self, g, bid=525, ask=525, **k):
        self.bid.update(_minuti(g, bid, **k))
        self.ask.update({t: tuple(v + 0.3 for v in q) for t, q in _minuti(g, ask, **k).items()})

    def scrivi(self, inizio, fine):
        SN.scrivi_cache(self.bid, self.cache / "XAUUSD", inizio=inizio, fine=fine)
        SN.scrivi_cache(self.ask, self.cache / "XAUUSD_ASK", inizio=inizio, fine=fine)

    def seduta(self, e, g):
        return [s for s in e["sedute"] + e["vigilie"] if s["giorno"] == g.isoformat()][0]


class TestSeduta(Base):
    def test_seduta_piena(self):
        g = date(2024, 1, 8)
        self.giorno(g)
        self.scrivi(g, g)
        s = self.seduta(X.esamina(self.cache, g, g), g)
        self.assertEqual((s["griglia"], s["comuni_validi"], s["solo_bid"], s["solo_ask"], s["comuni_non_validi"],
                          s["mancanti"], s["buco_max"]), (525, 525, 0, 0, 0, 0, 0))
        self.assertEqual(s["terzi"], [175, 175, 175])
        self.assertEqual(s["stati"], ["ok", "ok"])

    def test_buco_da_un_lato_solo(self):
        g = date(2024, 1, 9)
        self.giorno(g)
        for k in range(10):                                             # 10 minuti ASK mancanti dalle 09:00
            del self.ask[_utc(g, ora_t(9, 0)) + timedelta(minutes=k)]
        self.scrivi(g, g)
        s = self.seduta(X.esamina(self.cache, g, g), g)
        self.assertEqual((s["comuni_validi"], s["solo_bid"], s["solo_ask"], s["buco_max"]), (515, 10, 0, 10))
        self.assertEqual(s["terzi"], [165, 175, 175])

    def test_ask_sotto_bid_non_valido(self):
        g = date(2024, 1, 10)
        self.giorno(g)
        for k in (100, 101, 300):
            t = _utc(g, ora_t(8, 0)) + timedelta(minutes=k)
            self.ask[t] = tuple(v - 1.0 for v in self.bid[t])
        t = _utc(g, ora_t(8, 0)) + timedelta(minutes=400)                # solo l'apertura sotto il BID
        o, h, l, c = self.bid[t]
        self.ask[t] = (o - 1.0, h + 1.0, l - 1.0, c + 0.3)
        self.scrivi(g, g)
        s = self.seduta(X.esamina(self.cache, g, g), g)
        self.assertEqual((s["comuni_validi"], s["comuni_non_validi"], s["buco_max"]), (521, 4, 2))

    def test_estremi_incrociati_contati_a_parte(self):
        """#108 (R15-03): un minimo ASK sotto il minimo BID (o un massimo ASK sotto il massimo BID) indica quotazioni
        incrociate dentro il minuto. Il minuto resta valido come per il simulatore (apertura e chiusura), ma si conta
        a parte: sui dati veri dirà quanto conta il rilievo."""
        g = date(2024, 1, 12)
        self.giorno(g)
        t = _utc(g, ora_t(8, 0)) + timedelta(minutes=50)
        o, h, l, c = self.ask[t]
        self.ask[t] = (o, h, l - 2.0, c)                                 # minimo ASK sotto il minimo BID
        t2 = _utc(g, ora_t(8, 0)) + timedelta(minutes=60)
        o, h, l, c = self.ask[t2]
        self.ask[t2] = (o, self.bid[t2][1] - 0.1, min(l, o, c) - 0.0, c)  # massimo ASK sotto il massimo BID
        self.scrivi(g, g)
        e = X.esamina(self.cache, g, g)
        s = self.seduta(e, g)
        self.assertEqual((s["comuni_validi"], s["estremi_incrociati"]), (525, 2))
        self.assertEqual(e["anni"]["2024"]["estremi_incrociati"], 2)
        self.assertIn("incrociat", X.tabella(e))

    def test_buchi_ai_bordi_contano(self):
        g = date(2024, 1, 11)
        self.giorno(g, bid=518, ask=518, dalle=ora_t(8, 4))             # mancano i primi 4 e gli ultimi 3 minuti
        self.scrivi(g, g)
        s = self.seduta(X.esamina(self.cache, g, g), g)
        self.assertEqual((s["comuni_validi"], s["mancanti"], s["buco_max"]), (518, 7, 4))

    def test_file_mancante_vuoto_o_illeggibile(self):
        g1, g2, g3 = date(2024, 1, 15), date(2024, 1, 16), date(2024, 1, 17)
        for g in (g1, g2, g3):
            self.giorno(g)
        self.scrivi(g1, g3)
        (self.cache / "XAUUSD_ASK" / f"{g1.isoformat()}.bi5").unlink()
        (self.cache / "XAUUSD" / f"{g2.isoformat()}.bi5").write_bytes(b"")
        (self.cache / "XAUUSD" / f"{g3.isoformat()}.bi5").write_bytes(b"rotto")
        e = X.esamina(self.cache, g1, g3)
        a = e["anni"]["2024"]
        self.assertEqual((a["mancanti_ask"], a["vuoti_bid"], a["illeggibili_bid"], a["con_entrambi_i_file"]), (1, 1, 1, 0))
        self.assertEqual(self.seduta(e, g1)["stati"], ["ok", "mancante"])
        self.assertEqual(self.seduta(e, g2)["stati"], ["vuoto", "ok"])
        self.assertEqual(self.seduta(e, g3)["stati"], ["illeggibile", "ok"])
        for g in (g1, g2, g3):
            self.assertEqual((self.seduta(e, g)["comuni_validi"], self.seduta(e, g)["buco_max"]), (0, 525))

    def test_vigilia_solo_primo_terzo_e_chiusure_escluse(self):
        g = date(2024, 12, 24)
        self.giorno(g, bid=175, ask=175)
        self.giorno(date(2024, 12, 25), bid=100, ask=100)               # Natale: chiusura nota
        self.giorno(date(2024, 12, 28), bid=100, ask=100)               # sabato
        self.scrivi(g, date(2024, 12, 28))
        e = X.esamina(self.cache, g, date(2024, 12, 28))
        v = [s for s in e["vigilie"] if s["giorno"] == g.isoformat()][0]
        self.assertEqual((v["griglia"], v["comuni_validi"], v["buco_max"]), (175, 175, 0))
        giorni = {s["giorno"] for s in e["sedute"] + e["vigilie"]}
        self.assertNotIn("2024-12-25", giorni)
        self.assertNotIn("2024-12-28", giorni)
        self.assertIn("2024-12-27", giorni)                             # venerdì aperto, senza file: va contato


class TestPercentiliSoloSedute(Base):
    def test_le_vigilie_non_entrano_nei_percentili_annuali(self):
        """Aggiunto dopo R16 (mutante M-R16-01 di Gemini sopravvissuto, dichiarato): i percentili dell'anno usano solo
        le sedute piene; una vigilia completa (175/175) non deve alzarli."""
        self.giorno(date(2024, 12, 23), bid=300, ask=300)               # lunedì: 300 su 525
        self.giorno(date(2024, 12, 24), bid=175, ask=175)               # vigilia completa
        self.scrivi(date(2024, 12, 23), date(2024, 12, 24))
        a = X.esamina(self.cache, date(2024, 12, 23), date(2024, 12, 24))["anni"]["2024"]
        self.assertEqual((a["sedute"], a["vigilie"]), (1, 1))
        self.assertEqual(a["quota_comuni"], X.percentili([round(300 / 525, 4)]))
        self.assertEqual(a["buco_max"], X.percentili([225]))


class TestAnniEDiagnostica(Base):
    def setUp(self):
        super().setUp()
        self.giorno(date(2024, 1, 8))                                   # piena
        self.giorno(date(2024, 1, 9))
        for k in range(8):                                              # 98,5% (terzo 95,4%) ma buco di 8 minuti
            del self.ask[_utc(date(2024, 1, 9), ora_t(9, 0)) + timedelta(minutes=k)]
        self.giorno(date(2024, 1, 10), bid=300, ask=300)                # 57%, terzo 3 vuoto
        self.scrivi(date(2024, 1, 8), date(2024, 1, 10))
        self.e = X.esamina(self.cache, date(2024, 1, 8), date(2024, 1, 10))

    def test_conteggi_per_anno(self):
        a = self.e["anni"]["2024"]
        self.assertEqual((a["sedute"], a["con_entrambi_i_file"]), (3, 3))
        self.assertEqual(a["mancanti_bid"] + a["mancanti_ask"] + a["vuoti_bid"] + a["vuoti_ask"], 0)

    def test_griglia_diagnostica(self):
        """Quante sedute sarebbero ammissibili con una soglia: SOLO diagnostica, le soglie le decide il titolare."""
        self.assertEqual(X.ammissibili(self.e, 0.98, 0.95, 5), ["2024-01-08"])
        self.assertEqual(X.ammissibili(self.e, 0.98, 0.95, 10), ["2024-01-08", "2024-01-09"])
        self.assertEqual(X.ammissibili(self.e, 0.5, 0.25, 525), ["2024-01-08", "2024-01-09"])
        self.assertEqual(X.ammissibili(self.e, 0.5, 0.0, 525), ["2024-01-08", "2024-01-09", "2024-01-10"])
        self.assertEqual(X.ammissibili(self.e, 0.9, 0.0, 525), ["2024-01-08", "2024-01-09"])   # solo la quota

    def test_uscita_senza_prezzi(self):
        testo = X.tabella(self.e)
        for p in ("2345", "2346", "2344"):
            self.assertNotIn(p, testo)
        self.assertIn("diagnostica", testo.lower())
        self.assertIn("2024", testo)


class TestRigaDiComando(Base):
    def test_main_e_json(self):
        g = date(2024, 1, 8)
        self.giorno(g)
        self.scrivi(g, g)
        uscita = self.cache / "r.json"
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = X.main(["--cache", str(self.cache), "--inizio", "2024-01-08", "--fine", "2024-01-08",
                         "--json", str(uscita)])
        self.assertEqual(rc, 0)
        self.assertNotIn("2345", buf.getvalue())
        dati = json.loads(uscita.read_text())
        self.assertEqual(dati["anni"]["2024"]["sedute"], 1)
        self.assertNotIn("2345", uscita.read_text())

    def test_argomenti_non_validi(self):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(X.main(["--cache", str(self.cache), "--inizio", "2024-01-09", "--fine", "2024-01-08"]), 2)
            self.assertEqual(X.main(["--cache", str(self.cache / "nessuna"), "--inizio", "2024-01-08",
                                     "--fine", "2024-01-08"]), 2)
            (self.cache / "XAUUSD").mkdir()                                   # c'è il BID ma non l'ASK
            self.assertEqual(X.main(["--cache", str(self.cache), "--inizio", "2024-01-08", "--fine", "2024-01-08"]), 2)


if __name__ == "__main__":
    unittest.main()
