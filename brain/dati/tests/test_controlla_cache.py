"""Test del controllo d'integrità della cache Dukascopy (dati/pipeline/controlla_cache.py), scritti PRIMA del codice.
Il controllo conta e basta: non deve mai restituire prezzi (il periodo di verifica sigillato non si guarda, DA-26).
Uso (dalla radice del repository): python3 -s -B -W error -m unittest brain.dati.tests.test_controlla_cache
"""
import json
import lzma
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.dati.pipeline import controlla_cache as CC                 # noqa: E402
from brain.dati.pipeline import dukascopy as DK                       # noqa: E402

PREZZO = 2650123                                                      # millesimi: non deve comparire nell'esito


def bi5(n_minuti, base=PREZZO):
    rec = [DK.RECORD.pack(60 * k, base, base + 1, base - 1, base + 2, 1.0) for k in range(n_minuti)]
    return lzma.compress(b"".join(rec), format=lzma.FORMAT_ALONE)


class TestControllaCache(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name) / "XAUUSD"
        self.dir.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def scrivi(self, g, contenuto):
        (self.dir / f"{g.isoformat()}.bi5").write_bytes(contenuto)

    def mese_pulito(self, anno=2010, mese=3, minuti=1000):
        """Un mese con un file per ogni giorno: feriali con `minuti` minuti, fine settimana vuoti."""
        g = date(anno, mese, 1)
        while g.month == mese:
            self.scrivi(g, bi5(minuti) if g.weekday() < 5 else b"")
            g = date.fromordinal(g.toordinal() + 1)

    def test_mese_pulito(self):
        self.mese_pulito()
        e = CC.esamina(self.dir)
        a = e["anni"]["2010"]
        self.assertEqual((a["giorni"], a["file"], a["mancanti"], a["feriali_vuoti"], a["illeggibili"], a["corti"]),
                         (31, 31, 0, [], [], []))
        self.assertEqual((a["prima_data"], a["ultima_data"]), ("2010-03-01", "2010-03-31"))
        self.assertEqual(a["minuti"], 23 * 1000)                       # 23 feriali a marzo 2010
        self.assertEqual(e["tmp_residui"], [])
        self.assertTrue(e["pulito"])

    def test_problemi_contati_e_datati(self):
        self.mese_pulito()
        (self.dir / "2010-03-10.bi5").unlink()                         # mancante
        self.scrivi(date(2010, 3, 11), b"")                            # feriale vuoto
        self.scrivi(date(2010, 3, 12), bi5(1000)[:-40])                # troncato
        self.scrivi(date(2010, 3, 15), b"non e' un file lzma")         # danneggiato
        self.scrivi(date(2010, 3, 16), bi5(300))                       # corto (300 < metà di 1000)
        (self.dir / ".2010-03-17.tmp").write_bytes(b"x")               # temporaneo rimasto dallo spegnimento
        a = CC.esamina(self.dir)["anni"]["2010"]
        self.assertEqual(a["mancanti"], 1)
        self.assertEqual(a["feriali_vuoti"], ["2010-03-11"])
        self.assertEqual(a["illeggibili"], ["2010-03-12", "2010-03-15"])
        self.assertEqual(a["corti"], ["2010-03-16"])
        e = CC.esamina(self.dir)
        self.assertEqual(e["tmp_residui"], [".2010-03-17.tmp"])
        self.assertFalse(e["pulito"])

    def test_un_solo_problema_basta(self):
        """Ogni problema, da solo, rende la cache da sistemare (mutanti Q06, Q07)."""
        self.mese_pulito()
        (self.dir / ".2010-03-17.tmp").write_bytes(b"x")
        self.assertFalse(CC.esamina(self.dir)["pulito"])
        (self.dir / ".2010-03-17.tmp").unlink()
        self.assertTrue(CC.esamina(self.dir)["pulito"])
        self.scrivi(date(2010, 3, 11), b"")
        self.assertFalse(CC.esamina(self.dir)["pulito"])

    def test_chiusure_note_non_sono_problemi(self):
        for g in (date(2010, 1, 1), date(2010, 4, 2), date(2010, 12, 24), date(2010, 12, 27), date(2010, 12, 29),
                  date(2010, 12, 30)):
            self.scrivi(g, b"")
        a = CC.esamina(self.dir)["anni"]["2010"]
        # 25/12/2010 era sabato: 24 e 27 sono festività spostate (#50, R12bis-A3-03); 29 e 30 sono feriali normali
        self.assertEqual(a["feriali_vuoti"], ["2010-12-29", "2010-12-30"])
        self.assertEqual(a["chiusure_note_vuote"], ["2010-01-01", "2010-04-02", "2010-12-24", "2010-12-27"])
        self.scrivi(date(2009, 12, 24), b"")                  # 25/12/2009 era venerdì: il 24 è un feriale normale
        self.assertEqual(CC.esamina(self.dir)["anni"]["2009"]["feriali_vuoti"], ["2009-12-24"])

    def test_periodo_esplicito_conta_i_giorni_senza_file(self):
        self.mese_pulito()
        a = CC.esamina(self.dir, date(2010, 2, 25), date(2010, 3, 31))["anni"]["2010"]
        self.assertEqual((a["giorni"], a["mancanti"]), (35, 4))

    def test_anni_separati(self):
        self.mese_pulito(2009, 12)
        self.mese_pulito(2010, 1)
        e = CC.esamina(self.dir)
        self.assertEqual(sorted(e["anni"]), ["2009", "2010"])
        self.assertEqual(e["anni"]["2009"]["giorni"], 31)

    def test_mai_prezzi_nell_esito(self):
        self.mese_pulito()
        testo = json.dumps(CC.esamina(self.dir))
        for numero in ("2650", "2650.123", "2650123", "2650124", "2650122", "2650125"):
            self.assertNotIn(numero, testo)
        self.assertNotIn("2650", CC.testo(CC.esamina(self.dir)))

    def test_cartella_vuota_o_assente(self):
        self.assertFalse(CC.esamina(self.dir)["pulito"])
        with self.assertRaises(FileNotFoundError):
            CC.esamina(self.dir / "non_esiste")


if __name__ == "__main__":
    unittest.main()
