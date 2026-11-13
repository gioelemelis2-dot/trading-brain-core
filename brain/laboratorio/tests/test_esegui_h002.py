"""Prove complete dell'esecutore di H-002 su mercati INVENTATI a seme fisso (mandato notturno del 14/11/2026).
- mercato casuale: il programma NON deve promuovere nessuna variante;
- mercato con un vantaggio noto della rottura: lo DEVE trovare;
- mercato con sola tendenza al rialzo: NON deve promuovere (criterio delle vendite);
- casi limite e riga di comando (sigillo, periodi, verifica una volta sola).
Scritti PRIMA dell'esecutore. Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_esegui_h002
"""
import contextlib
import io
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.laboratorio.esecuzione import criteri as K               # noqa: E402
from brain.laboratorio.esecuzione import esegui_h002 as E           # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S               # noqa: E402
from brain.laboratorio.esecuzione import sintetico as SN            # noqa: E402

INIZIO = date(2024, 1, 1)
GIORNI = 800                                                        # circa 430 trade per variante
ORA = "2026-11-15T03:00:00Z"


def mercato(**kw):
    return SN.mercato(INIZIO, GIORNI, seme=3, sd=0.7, **kw)


class TestMercatiInventati(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ris = {}
        for nome, kw in (("casuale", {}), ("vantaggio", {"spinta": 0.01}), ("tendenza", {"deriva": 0.01})):
            bid, ask = mercato(**kw)
            cls.ris[nome] = E.esegui_sviluppo(bid, ask)

    def test_mercato_casuale_non_promuove(self):
        for v in ("V-T", "V-S"):
            x = self.ris["casuale"]["varianti"][v]
            self.assertGreaterEqual(x["metriche"]["n"], 300, v)
            self.assertFalse(x["screening"]["promossa"], v)
            self.assertLess(x["metriche"]["r_medio"], 0.05, v)
            self.assertFalse(x["casuale"]["sopra"], v)

    def test_vantaggio_noto_trovato(self):
        for v in ("V-T", "V-S"):
            x = self.ris["vantaggio"]["varianti"][v]
            self.assertTrue(x["screening"]["promossa"], (v, [c for c in x["screening"]["criteri"] if not c["passa"]]))
            self.assertFalse(x["veto"])

    def test_sola_tendenza_non_promuove(self):
        for v in ("V-T", "V-S"):
            x = self.ris["tendenza"]["varianti"][v]
            self.assertFalse(x["screening"]["promossa"], v)
            vendite = [c for c in x["screening"]["criteri"] if c["nome"] == "R medio delle vendite"][0]
            self.assertFalse(vendite["passa"], v)

    def test_robustezza_sempre_eseguita(self):
        x = self.ris["casuale"]["varianti"]
        self.assertEqual(sorted(x["V-T"]["robustezza"]),
                         sorted(["range 20'", "range 45'", "target 1,2", "target 2,0", "tetto 1,6", "tetto 2,5"]))
        self.assertEqual(sorted(x["V-S"]["robustezza"]), sorted(["range 20'", "range 45'", "tetto 1,6", "tetto 2,5"]))
        for v in ("V-T", "V-S"):
            self.assertTrue(all(r is not None for r in x[v]["robustezza"].values()))

    def test_stress_peggiora_e_confronti_sui_giorni_della_strategia(self):
        for nome in self.ris:
            for v, x in self.ris[nome]["varianti"].items():
                self.assertLess(x["r_stress"], x["metriche"]["r_medio"], (nome, v))
                n = x["metriche"]["n"]
                self.assertGreaterEqual(x["casuale"]["n_giorni"], 0.95 * n, (nome, v))
                self.assertLessEqual(x["casuale"]["n_giorni"], n, (nome, v))
                self.assertGreaterEqual(x["benchmark"]["n_comuni"], 0.95 * n, (nome, v))
                self.assertEqual(x["casuale"]["ripetizioni"], 1000)

    def test_vantaggio_batte_benchmark_e_casuale(self):
        x = self.ris["vantaggio"]["varianti"]["V-T"]
        self.assertTrue(x["benchmark"]["batte_entrambi"])
        self.assertTrue(x["casuale"]["sopra"])
        self.assertLess(abs(x["casuale"]["media_casuale"]), 0.15)       # direzione a caso: vicino a zero meno i costi

    def test_resoconto_e_rapporto(self):
        r = self.ris["casuale"]
        self.assertGreater(r["resoconto"]["giorni_per_motivo"]["valido"], 300)
        testo = E.rapporto(r, "H-002 su dati inventati", {"modalita": "sviluppo", "fonte": "mercato inventato"})
        for parola in ("H-002 su dati inventati", "V-T", "V-S", "BOCCIATA", "robustezza", "stress", "valido",
                       "mercato inventato", "confronto casuale"):
            self.assertIn(parola, testo)
        self.assertIn("PROMOSSA", E.rapporto(self.ris["vantaggio"], "x", {}))


class TestCasiLimite(unittest.TestCase):
    def test_nessun_dato(self):
        r = E.esegui_sviluppo({}, {})
        for v in ("V-T", "V-S"):
            self.assertEqual(r["varianti"][v]["metriche"]["n"], 0)
            self.assertFalse(r["varianti"][v]["screening"]["promossa"])
            self.assertIsNone(r["varianti"][v]["casuale"])
        E.rapporto(r, "vuoto", {})

    def test_pochi_giorni_e_senza_ask(self):
        bid, ask = SN.mercato(INIZIO, 20, seme=1, sd=0.7)
        r = E.esegui_sviluppo(bid, ask)
        self.assertEqual(r["varianti"]["V-T"]["metriche"]["n"], 0)            # meno di 20 sessioni precedenti
        bid, _ = SN.mercato(INIZIO, 60, seme=1, sd=0.7)
        r = E.esegui_sviluppo(bid, {})
        self.assertEqual(r["varianti"]["V-T"]["metriche"]["n"], 0)            # nessun minuto eseguibile

    def test_riproducibile(self):
        bid, ask = SN.mercato(INIZIO, 90, seme=5, sd=0.7)
        a, b = E.esegui_sviluppo(bid, ask), E.esegui_sviluppo(bid, ask)
        self.assertEqual(a["varianti"]["V-T"]["casuale"], b["varianti"]["V-T"]["casuale"])
        self.assertEqual(a["varianti"]["V-S"]["metriche"], b["varianti"]["V-S"]["metriche"])

    def test_verifica(self):
        bid, ask = SN.mercato(date(2008, 1, 1), 800, seme=4, sd=0.7, spinta=0.01)
        r = E.esegui_verifica(bid, ask, ["V-T"], n_prove=2)
        self.assertTrue(r["varianti"]["V-T"]["verifica"]["promossa"], r["varianti"]["V-T"]["verifica"])
        self.assertNotIn("V-S", r["varianti"])
        self.assertEqual(list(r["sharpe_prove"]), ["V-T"])                  # solo le promosse girano in verifica
        bid, ask = SN.mercato(date(2008, 1, 1), 800, seme=4, sd=0.7)
        self.assertFalse(E.esegui_verifica(bid, ask, ["V-T", "V-S"], n_prove=2)["varianti"]["V-S"]["verifica"]["promossa"])
        with self.assertRaises(ValueError):
            E.esegui_verifica(bid, ask, ["V-X"], n_prove=2)


class TestVarianzaDelleProve(unittest.TestCase):
    def test_sharpe_dispersi_alzano_la_soglia(self):
        import random
        rng = random.Random(9)
        tr = [{"data": date(2005 + k // 100, 1, 1), "lato": "acquisto", "r": rng.gauss(0.1, 1.0)} for k in range(1500)]
        base = K.verifica(tr, n_prove=2)["dsr"]
        self.assertEqual(K.verifica(tr, n_prove=2, sharpe_prove=[0.1])["dsr"], base)      # V = max(nulla, empirica)
        self.assertLess(K.verifica(tr, n_prove=2, sharpe_prove=[-0.5, 0.6])["dsr"], base)


class TestRigaDiComando(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.cache = self.dir / "cache"
        self.scheda = self.dir / "H-002.md"
        self.scheda.write_text("# H-002 di prova\n", encoding="utf-8")
        self.registro = self.dir / "registro.json"
        self.uscita = self.dir / "rapporto.md"

    def tearDown(self):
        self._tmp.cleanup()

    def cache_di(self, inizio, giorni):
        bid, ask = SN.mercato(inizio, giorni, seme=2, sd=0.7, spinta=0.01)
        SN.scrivi_cache(bid, self.cache / "XAUUSD")
        SN.scrivi_cache(ask, self.cache / "XAUUSD_ASK")

    def lancia(self, *argomenti):
        base = ["--registro", str(self.registro), "--scheda", str(self.scheda), "--cache", str(self.cache),
                "--rapporto", str(self.uscita), "--ora", ORA, "--ripetizioni", "100"]
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return E.main(base + list(argomenti))

    def test_sviluppo_richiede_il_sigillo(self):
        self.cache_di(date(2024, 1, 1), 60)
        self.assertEqual(self.lancia("--modalita", "sviluppo", "--inizio", "2024-01-01", "--fine", "2024-02-29"), 2)
        self.assertFalse(self.uscita.exists())
        self.assertFalse(self.registro.exists())

    def test_sviluppo_registra_le_esecuzioni(self):
        self.cache_di(date(2024, 1, 1), 60)
        S.sigilla(self.registro, "H-002", self.scheda, ["V-T", "V-S"], ORA)
        self.assertEqual(self.lancia("--modalita", "sviluppo", "--inizio", "2024-01-01", "--fine", "2024-02-29"), 0)
        testo = self.uscita.read_text(encoding="utf-8")
        self.assertIn("H-002", testo)
        self.assertIn(S.impronta(self.scheda), testo)
        dati = S.leggi(self.registro)
        ruoli = [e["ruolo"] for e in dati["esecuzioni"]]
        self.assertEqual(ruoli.count("sviluppo"), 2)
        self.assertEqual(ruoli.count("robustezza"), 10)
        self.assertEqual(S.n_prove(dati), 2)

    def test_periodi_e_scheda_modificata(self):
        self.cache_di(date(2024, 1, 1), 60)
        S.sigilla(self.registro, "H-002", self.scheda, ["V-T", "V-S"], ORA)
        self.assertEqual(self.lancia("--modalita", "sviluppo", "--inizio", "2023-11-01", "--fine", "2024-02-29"), 2)
        self.assertEqual(self.lancia("--modalita", "verifica", "--varianti", "V-T",
                                     "--inizio", "2024-01-01", "--fine", "2024-02-29"), 2)
        self.scheda.write_text("# H-002 cambiata\n", encoding="utf-8")
        self.assertEqual(self.lancia("--modalita", "sviluppo", "--inizio", "2024-01-01", "--fine", "2024-02-29"), 2)
        self.assertEqual(S.leggi(self.registro)["esecuzioni"], [])

    def test_verifica_una_volta_sola(self):
        self.cache_di(date(2010, 1, 1), 60)
        S.sigilla(self.registro, "H-002", self.scheda, ["V-T", "V-S"], ORA)
        argomenti = ("--modalita", "verifica", "--varianti", "V-T", "--inizio", "2010-01-01", "--fine", "2010-02-28")
        self.assertEqual(self.lancia(*argomenti), 0)
        self.assertIn("verifica", self.uscita.read_text(encoding="utf-8"))
        self.assertEqual(self.lancia(*argomenti), 2)
        self.assertEqual(self.lancia("--modalita", "verifica", "--inizio", "2010-01-01", "--fine", "2010-02-28"), 2)


if __name__ == "__main__":
    unittest.main()
