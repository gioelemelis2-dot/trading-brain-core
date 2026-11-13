"""Test di laboratorio/studi/studio_sessioni.py con dati inventati (nessun dato reale).
Uso (dalla radice del repository): python3 -s -B -W error -m unittest brain.laboratorio.tests.test_studio_sessioni
"""
import lzma
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.dati.pipeline import dukascopy as DK                    # noqa: E402
from brain.laboratorio.studi import studio_sessioni as S            # noqa: E402

UTC = timezone.utc


def bi5(minuti):
    return lzma.compress(b"".join(DK.RECORD.pack(*m) for m in minuti), format=lzma.FORMAT_ALONE)


def minuto(t, prezzo, escursione=0.5):
    return (t, prezzo, prezzo + escursione, prezzo - escursione, prezzo, 1.0)


class TestPeriodoSigillato(unittest.TestCase):
    def test_rifiuta_date_prima_dello_sviluppo(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError) as e:
                S.carica_minuti(Path(tmp), date(2023, 11, 14), date(2023, 12, 1))
            self.assertIn("SIGILLATA", str(e.exception))
            self.assertEqual(S.main(["--inizio", "2020-01-01", "--fine", "2020-02-01", "--cache", tmp]), 2)

    def test_carica_e_conta_i_giorni_mancanti(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = 2650000
            (Path(tmp) / "2026-01-05.bi5").write_bytes(bi5([(600, p, p + 2, p - 3, p + 5, 1.0)]))
            (Path(tmp) / "2026-01-06.bi5").write_bytes(b"")                       # giorno vuoto in cache
            minuti, mancanti = S.carica_minuti(Path(tmp), date(2026, 1, 5), date(2026, 1, 7))
            self.assertEqual(mancanti, 1)
            self.assertEqual(len(minuti), 1)
            self.assertEqual(minuti[0][0], datetime(2026, 1, 5, 0, 10, tzinfo=UTC))
            self.assertAlmostEqual(minuti[0][4], 2650.002)


class TestSessioni(unittest.TestCase):
    def test_orari_con_ora_legale(self):
        """Londra apre alle 08:00 di Londra: 08:00 UTC d'inverno, 07:00 UTC d'estate. New York 09:30 di New York:
        14:30 UTC d'inverno, 13:30 UTC d'estate. Londra e New York si sovrappongono: conta New York."""
        self.assertTrue(S.in_sessione(datetime(2026, 1, 7, 8, 0, tzinfo=UTC), "Londra"))
        self.assertFalse(S.in_sessione(datetime(2026, 1, 7, 7, 59, tzinfo=UTC), "Londra"))
        self.assertTrue(S.in_sessione(datetime(2026, 7, 7, 7, 0, tzinfo=UTC), "Londra"))
        self.assertEqual(S.sessione_di(datetime(2026, 1, 7, 14, 30, tzinfo=UTC)), "New York")
        self.assertEqual(S.sessione_di(datetime(2026, 7, 7, 13, 30, tzinfo=UTC)), "New York")
        self.assertEqual(S.sessione_di(datetime(2026, 1, 7, 0, 0, tzinfo=UTC)), "Tokyo")
        self.assertIsNone(S.sessione_di(datetime(2026, 1, 7, 22, 0, tzinfo=UTC)))

    def test_statistiche_su_un_giorno_costruito(self):
        """Mercoledì 7/1/2026: prezzo fermo a 2000, poi dalle 17:00 alle 18:00 UTC (Londra già chiusa alle 16:30 UTC,
        New York aperta fino alle 21:00 UTC) sale di 1 USD al minuto fino a 2060. New York: netto +60, efficienza 1,
        rompe sopra il massimo di Londra dopo la sua chiusura; massimo del giorno alle 19 italiane, minimo alle 00."""
        ms = []
        t = datetime(2026, 1, 6, 23, 0, tzinfo=UTC)
        salita = datetime(2026, 1, 7, 17, 0, tzinfo=UTC)
        while t < datetime(2026, 1, 7, 22, 0, tzinfo=UTC):
            p = 2000.0 + min(60, max(0, (t - salita).total_seconds() // 60)) if t >= salita else 2000.0
            ms.append(minuto(t, p, 0.0))
            t += timedelta(minutes=1)
        giorni = S.per_giorno(ms)
        self.assertEqual(list(giorni), [date(2026, 1, 7)])
        studio = S.studio_sessioni(giorni)
        sess = {x["sessione"]: x for x in studio["righe"]}
        self.assertAlmostEqual(sess["New York"]["netto_con_segno"], 60.0)
        self.assertAlmostEqual(sess["New York"]["efficienza"], 1.0)
        self.assertAlmostEqual(sess["Londra"]["escursione"], 0.0)
        self.assertEqual(studio["new_york_dopo_la_chiusura_di_londra"]["sopra"], 1)
        ore = {x["ora"]: x for x in S.studio_ore(giorni)["righe"]}
        self.assertEqual(ore[19]["massimo_del_giorno_pct"], 100.0)
        self.assertEqual(ore[0]["minimo_del_giorno_pct"], 100.0)


class TestConfrontoCasuale(unittest.TestCase):
    def test_conserva_orari_e_ampiezze_e_cambia_solo_la_direzione(self):
        t0 = datetime(2026, 1, 7, 10, 0, tzinfo=UTC)
        ms = [(t0 + timedelta(minutes=i), 100.0 + i, 101.5 + i, 99.0 + i, 101.0 + i, 2.0) for i in range(200)]
        f = S.segni_casuali(ms)
        self.assertEqual([m[0] for m in f], [m[0] for m in ms])
        for vero, finto in zip(ms, f):
            self.assertAlmostEqual(abs(finto[4] - finto[1]), abs(vero[4] - vero[1]))
            self.assertAlmostEqual(finto[2] - max(finto[1], finto[4]), vero[2] - max(vero[1], vero[4]))
            self.assertAlmostEqual(min(finto[1], finto[4]) - finto[3], min(vero[1], vero[4]) - vero[3])
        for a, b in zip(f, f[1:]):
            self.assertAlmostEqual(b[1], a[4])                     # continuità: ogni minuto parte dalla chiusura
        su = sum(1 for m in f if m[4] > m[1])
        self.assertTrue(70 < su < 130, su)                      # direzioni casuali, non tutte in salita
        self.assertEqual(f, S.segni_casuali(ms))                # seme fisso: riproducibile


class TestCandeleECompressioni(unittest.TestCase):
    def test_candele_da_5_minuti(self):
        t0 = datetime(2026, 1, 7, 10, 0, tzinfo=UTC)
        ms = [(t0 + timedelta(minutes=i), 100.0 + i, 101.0 + i, 99.0 + i, 100.5 + i, 1.0) for i in range(10)]
        c = S.candele(ms, 5)
        self.assertEqual(len(c), 2)
        self.assertEqual(c[0][:5], (t0, 100.0, 105.0, 99.0, 104.5))
        self.assertEqual(c[1][5], 5.0)

    def test_compressione_e_rottura_verso_l_alto(self):
        """21 giorni di oscillazioni da 10 USD all'ora (riferimento), poi 1 ora con escursione 1 (compressione) e una
        rottura di 6 USD verso l'alto: deve risultare almeno una compressione con uscita sopra."""
        ms = []
        t = datetime(2026, 1, 5, 0, 0, tzinfo=UTC)
        for g in range(22):
            for i in range(24 * 60):
                tt = t + timedelta(days=g, minutes=i)
                if g < 21:
                    p = 2000.0 + 5.0 * ((i // 30) % 2)
                elif i < 600:
                    p = 2000.0 + 0.5 * ((i // 5) % 2)
                else:
                    p = 2006.0
                ms.append(minuto(tt, p, 0.0))
        comp = S.studio_compressioni(ms)
        totale_sopra = sum(v["sopra"] for v in comp["per_sessione"].values())
        self.assertGreaterEqual(totale_sopra, 1)
        self.assertEqual(sum(v["sotto"] for v in comp["per_sessione"].values()), 0)


if __name__ == "__main__":
    unittest.main()
