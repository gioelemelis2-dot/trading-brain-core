"""Test dello strumento dei costi del broker (dati/pipeline/costi_tick.py), scritti PRIMA del codice (18/11/2026).
Legge l'esportazione dei tick di MetaTrader 5 (desktop: Simboli → Tick → Esporta) e calcola lo spread per ora UTC e il
costo in R per varie distanze dello stop. Solo numeri inventati. Mai prezzi nell'uscita; mai tick della riserva.
Uso: python3 -s -B -W error -m unittest brain.dati.tests.test_costi_tick
"""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.dati.pipeline import costi_tick as C                       # noqa: E402

TESTA = "<DATE>\t<TIME>\t<BID>\t<ASK>\t<LAST>\t<VOLUME>\t<FLAGS>\n"


def riga(data, ora, bid="", ask="", flags="6"):
    return f"{data}\t{ora}\t{bid}\t{ask}\t\t\t{flags}\n"


def utc(*a):
    return datetime(*a, tzinfo=timezone.utc)


class Base(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.dir = Path(self._t.name)

    def tearDown(self):
        self._t.cleanup()

    def file(self, righe, testa=TESTA, nome="tick.csv"):
        p = self.dir / nome
        p.write_text(testa + "".join(righe), encoding="utf-8")
        return p


class TestLettura(Base):
    def test_formato_mt5_fuso_e_lato_mancante(self):
        """Ora del server +2 → UTC; un tick con un solo lato aggiornato riusa l'ultimo valore dell'altro."""
        p = self.file([riga("2026.11.18", "10:00:00.100", "3767.49", "3767.89"),
                       riga("2026.11.18", "10:00:01.250", "3767.59", "", flags="2"),
                       riga("2026.11.18", "10:00:02.000", "", "3768.09", flags="4")])
        t = list(C.leggi(p, fuso_server=2))
        self.assertEqual([x[0] for x in t], [utc(2026, 11, 18, 8, 0, 0, 100000), utc(2026, 11, 18, 8, 0, 1, 250000),
                                             utc(2026, 11, 18, 8, 0, 2)])
        self.assertEqual([(x[1], x[2]) for x in t], [(3767.49, 3767.89), (3767.59, 3767.89), (3767.59, 3768.09)])

    def test_tick_senza_entrambi_i_lati_saltati_finche_non_noti(self):
        p = self.file([riga("2026.11.18", "10:00:00", "", "3767.89", flags="4"),
                       riga("2026.11.18", "10:00:01", "3767.49", "", flags="2")])
        self.assertEqual([(x[1], x[2]) for x in C.leggi(p, fuso_server=0)], [(3767.49, 3767.89)])

    def test_riserva_rifiutata_dopo_la_conversione_in_utc(self):
        """15/11/2023 01:00 sul server a +2 è il 14/11 alle 23:00 UTC: periodo sigillato, si rifiuta tutto il file."""
        p = self.file([riga("2026.11.18", "10:00:00", "1.0", "1.1"), riga("2023.11.15", "01:00:00", "1.0", "1.1")])
        with self.assertRaisesRegex(ValueError, "15/11/2023"):
            list(C.leggi(p, fuso_server=2))
        p = self.file([riga("2023.11.15", "02:00:00", "1.0", "1.1")], nome="ok.csv")
        self.assertEqual(len(list(C.leggi(p, fuso_server=2))), 1)                 # 00:00 UTC del 15/11: ammesso

    def test_intestazione_sconosciuta_rifiutata(self):
        p = self.file([riga("2026.11.18", "10:00:00", "1.0", "1.1")], testa="data,ora,bid,ask\n")
        with self.assertRaisesRegex(ValueError, "intestazione"):
            list(C.leggi(p, fuso_server=0))


class TestStatistiche(unittest.TestCase):
    def tick(self, ora, spread, minuto=0):
        return (utc(2026, 11, 18, ora, minuto), 100.0, 100.0 + spread)

    def test_spread_per_ora(self):
        t = [self.tick(8, s) for s in (0.30, 0.40, 0.50, 0.20, 0.60, 0.40, 0.30, 0.40, 0.50, 1.00)] + \
            [self.tick(9, 0.25), self.tick(9, -0.05)]
        r = C.spread_per_ora(t)
        o8 = r["ore"][8]
        self.assertEqual(o8["n"], 10)
        self.assertAlmostEqual(o8["mediana"], 0.40)
        self.assertAlmostEqual(o8["media"], 0.46)
        self.assertAlmostEqual(o8["p90"], 0.60)                    # rango ⌈0,9·10⌉ = 9 → 0,60
        self.assertAlmostEqual(o8["max"], 1.00)
        self.assertEqual(r["ore"][9]["n"], 1)
        self.assertEqual(r["anomali"], 1)                          # ASK < BID: escluso e contato
        self.assertNotIn(10, r["ore"])

    def test_sessione_di_londra(self):
        t = [self.tick(7, 9.0, 59), self.tick(8, 0.3), self.tick(16, 0.5, 44), self.tick(16, 9.0, 45)]
        r = C.spread_per_ora(t)
        self.assertEqual(r["londra"]["n"], 2)                      # 08:00 ≤ t < 16:45 UTC
        self.assertAlmostEqual(r["londra"]["max"], 0.5)

    def test_costo_in_r(self):
        self.assertAlmostEqual(C.costo_in_r(0.40, 6.0, 100, 5.0), 0.092)
        self.assertAlmostEqual(C.costo_in_r(0.40, 6.0, 100, 15.0), 0.46 / 15)
        with self.assertRaises(ValueError):
            C.costo_in_r(0.40, 6.0, 100, 0.0)


class TestRigaDiComando(Base):
    def test_uscita_senza_prezzi(self):
        righe = [riga("2026.11.18", f"{h:02d}:{m:02d}:00", "3767.49", "3767.89") for h in (9, 10, 12) for m in (0, 30)]
        p = self.file(righe)
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(C.main(["--tick", str(p), "--fuso-server", "2", "--commissione", "6",
                                     "--stop", "5,15"]), 0)
        testo = buf.getvalue()
        self.assertNotIn("3767", testo)
        self.assertIn("UTC", testo)
        self.assertIn("0,40", testo)                               # spread mediano in USD
        self.assertIn("0,092", testo)                              # costo in R con stop 5

    def test_errori(self):
        err = io.StringIO()
        with redirect_stderr(err):
            self.assertEqual(C.main(["--tick", str(self.dir / "manca.csv"), "--fuso-server", "2"]), 2)
            p = self.file([riga("2023.01.05", "10:00:00", "1.0", "1.1")])
            self.assertEqual(C.main(["--tick", str(p), "--fuso-server", "2"]), 2)
        self.assertIn("15/11/2023", err.getvalue())


if __name__ == "__main__":
    unittest.main()
