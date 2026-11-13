"""Test di laboratorio/studi/studio_range.py con dati inventati (nessun dato reale).
La prova più importante è la CALIBRAZIONE: su prezzi puramente casuali lo studio deve ritrovare le probabilità
teoriche (33,3%, 20%, 50%). Al primo giro, con le ombre, dava 40,5%: un errore di selezione (si escludevano i trade
contro il range eseguiti nel minuto che poi rompeva), trovato da questa prova e corretto.
Uso (dalla radice del repository): python3 -s -B -W error -m unittest brain.laboratorio.tests.test_studio_range
"""
import random
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.laboratorio.studi import studio_range as R      # noqa: E402

UTC = timezone.utc


def casuali(n_minuti, passi=100, seme=7):
    rng, p, out = random.Random(seme), 2000.0, []
    t0 = datetime(2026, 1, 5, tzinfo=UTC)
    sd = 0.95 / passi ** 0.5
    for k in range(n_minuti):
        o = p
        hi = lo = p
        for _ in range(passi):
            p += rng.gauss(0, sd)
            hi, lo = max(hi, p), min(lo, p)
        out.append((t0 + timedelta(minutes=k), o, hi, lo, p, 1.0))
    return out


def quota(diz, filtro):
    s = n = 0
    for k, v in diz.items():
        if filtro(k):
            s += v.get("target", 0)
            n += v.get("target", 0) + v.get("stop", 0)
    return s / n, n


class TestCalibrazione(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ms = casuali(40000)
        cls.r = {m: R.analizza(ms, m, riferimento=lambda g: 8.0) for m in ("ombre", "chiusure")}

    def test_chiusure_ritrovano_la_teoria(self):
        r = self.r["chiusure"]
        for chiave, teoria in (("circa metà", 1 / 3), ("circa bordo", 0.2)):
            q, n = quota(r["contro"], lambda k: k[1].startswith(chiave))
            self.assertGreater(n, 1000)
            self.assertAlmostEqual(q, teoria, delta=0.035, msg=chiave)
        q, n = quota(r["rottura"], lambda k: True)
        self.assertAlmostEqual(q, 0.5, delta=0.035)

    def test_ombre_mai_sopra_la_teoria(self):
        """Con le ombre la regola prudente dentro il minuto può solo abbassare le vittorie, mai alzarle."""
        r = self.r["ombre"]
        for chiave, teoria in (("circa metà", 1 / 3), ("circa bordo", 0.2)):
            q, _ = quota(r["contro"], lambda k: k[1].startswith(chiave))
            self.assertLess(q, teoria + 0.01, chiave)
            self.assertGreater(q, teoria - 0.06, chiave)
        q, _ = quota(r["rottura"], lambda k: True)
        self.assertLess(q, 0.51)


class TestScenarioCostruito(unittest.TestCase):
    """Range 2000–2002 (A = 2) formato in 10 minuti; tre tocchi dell'alto (massimo 2001,9, chiusura 2001 = metà, che
    riarma); al minuto 13 il massimo 2002,5 rompe (oltre 2002,2). Con le ombre: 3 tocchi, poi rottura verso l'alto,
    più un quarto ordine limite eseguito nel minuto della rottura (stop). Vendite a 2001,8 con stop a 2002,3: tutte
    stoppate. Rottura: ingresso 2002,2, target 2003,2, stop 2001,2 (il minuto della rottura ha minimo 2001,5: la regola
    prudente non scatta): il prezzo sale a 2003,5, quindi target."""

    def minuti(self):
        t0 = datetime(2026, 1, 7, 10, 0, tzinfo=UTC)
        barre = [(2001.0, 2002.0, 2000.0, 2001.0)] * 10
        barre += [(2001.0, 2001.9, 2000.9, 2001.0)] * 3
        barre += [(2001.0, 2002.5, 2001.5, 2002.4)]      # minimo sopra lo stop della rottura (2001,2)
        barre += [(2002.4, 2003.5, 2002.3, 2003.4)] * 5
        return [(t0 + timedelta(minutes=k), o, h, lo, c, 1.0) for k, (o, h, lo, c) in enumerate(barre)]

    def test_tocchi_rottura_ed_esiti(self):
        r = R.analizza(self.minuti(), "ombre", riferimento=lambda g: 100.0)
        self.assertEqual(r["range"], 1)
        self.assertEqual(r["rotture_con_tocchi"], {3: 1})
        self.assertEqual(r["raggiunti"], {0: 1, 1: 1, 2: 1, 3: 1})
        self.assertEqual(r["lato_ultimo_tocco"], {"stesso": 1, "opposto": 0})
        for n in (1, 2, 3, 4):
            for nome in ("circa metà (0,5 A)", "circa bordo opposto (1 A)"):
                self.assertEqual(r["contro"][(n, nome)], {"stop": 1}, (n, nome))
        self.assertEqual(r["rottura"], {"2-3 tocchi": {"target": 1}})
        # se il minuto della rottura tocca anche lo stop, con le ombre conta lo stop (non si sa cosa è venuto prima)
        ms = self.minuti()
        ms[13] = (ms[13][0], 2001.0, 2002.5, 2001.1, 2002.4, 1.0)
        self.assertEqual(R.analizza(ms, "ombre", riferimento=lambda g: 100.0)["rottura"], {"2-3 tocchi": {"stop": 1}})

    def test_range_troppo_largo_o_stretto_ignorato(self):
        self.assertEqual(R.analizza(self.minuti(), "ombre", riferimento=lambda g: 3.0)["range"], 0)   # 2 > 0,5 × 3
        piatto = [(m[0], 2000.0, 2000.2, 1999.9, 2000.0, 1.0) for m in self.minuti()]                 # A < 1 USD
        self.assertEqual(R.analizza(piatto, "ombre", riferimento=lambda g: 100.0)["range"], 0)


class TestStrumenti(unittest.TestCase):
    def test_wilson(self):
        lo, hi = R.wilson(5, 10)
        self.assertAlmostEqual(lo, 0.2366, places=3)
        self.assertAlmostEqual(hi, 0.7634, places=3)
        self.assertEqual(R.wilson(0, 0), (None, None))

    def test_rifiuta_il_periodo_sigillato(self):
        self.assertEqual(R.main(["--inizio", "2020-01-01", "--fine", "2020-02-01", "--cache", "/inesistente"]), 2)

    def test_modo_non_valido(self):
        with self.assertRaises(ValueError):
            R.analizza([], "medie")


if __name__ == "__main__":
    unittest.main()
