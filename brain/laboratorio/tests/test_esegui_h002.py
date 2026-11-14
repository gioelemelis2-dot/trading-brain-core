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
from datetime import date, timedelta
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

    def test_robustezza_con_i_parametri_giusti_e_stress_di_020(self):
        from brain.laboratorio.simulatori import orb_londra as O
        bid, ask = mercato()
        x = self.ris["casuale"]["varianti"]["V-T"]
        for nome in ("range 20'", "range 45'", "tetto 1,6", "tetto 2,5", "target 1,2", "target 2,0"):
            self.assertNotAlmostEqual(x["robustezza"][nome], x["metriche"]["r_medio"], places=6, msg=nome)
        p = O.Parametri(stress=0.20)
        self.assertAlmostEqual(x["r_stress"], O.metriche(O.trade(O.prepara(bid, ask, p), p))["r_medio"])

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


class BaseRiga(unittest.TestCase):
    """Strumenti comuni dei test della riga di comando (nessun test qui)."""

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

    def cache_di(self, inizio, giorni, da=None):
        """Cache completa come quella vera: un file per ogni giorno di calendario, vuoto nei giorni senza dati.
        `da`: primo giorno della cache, se prima del mercato (giorni vuoti in testa)."""
        bid, ask = SN.mercato(inizio, giorni, seme=2, sd=0.7, spinta=0.01)
        fine = inizio + timedelta(days=giorni - 1)
        SN.scrivi_cache(bid, self.cache / "XAUUSD", inizio=da or inizio, fine=fine)
        SN.scrivi_cache(ask, self.cache / "XAUUSD_ASK", inizio=da or inizio, fine=fine)

    def sviluppo_finto(self, **promosse):
        """Esiti dello screening scritti nel registro come li scriverebbe main (per provare la verifica)."""
        for v, esito in promosse.items():
            S.registra_esecuzione(self.registro, "H-002", {"ruolo": "sviluppo", "variante": v.replace("_", "-"),
                                                          "promossa": esito}, ORA)

    def lancia(self, *argomenti):
        base = ["--registro", str(self.registro), "--scheda", str(self.scheda), "--cache", str(self.cache),
                "--rapporto", str(self.uscita), "--ora", ORA, "--ripetizioni", "100"]
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return E.main(base + list(argomenti))


class TestRigaDiComando(BaseRiga):
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
        self.cache_di(date(2010, 1, 1), 59)
        S.sigilla(self.registro, "H-002", self.scheda, ["V-T", "V-S"], ORA)
        self.sviluppo_finto(V_T=True, V_S=False)
        argomenti = ("--modalita", "verifica", "--varianti", "V-T", "--inizio", "2010-01-01", "--fine", "2010-02-28")
        self.assertEqual(self.lancia(*argomenti), 0)
        self.assertIn("verifica", self.uscita.read_text(encoding="utf-8"))
        self.assertEqual(self.lancia(*argomenti), 2)
        self.assertEqual(self.lancia("--modalita", "verifica", "--inizio", "2010-01-01", "--fine", "2010-02-28"), 2)

    def test_verifica_senza_varianti_fermata_prima_dei_dati(self):
        """Senza --varianti la verifica si ferma PRIMA di leggere i dati sigillati (mutante E12)."""
        S.sigilla(self.registro, "H-002", self.scheda, ["V-T", "V-S"], ORA)
        errore = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(errore):
            rc = E.main(["--registro", str(self.registro), "--scheda", str(self.scheda), "--cache", str(self.cache),
                         "--rapporto", str(self.uscita), "--ora", ORA, "--modalita", "verifica",
                         "--inizio", "2010-01-01", "--fine", "2010-02-28"])
        self.assertEqual(rc, 2)
        self.assertIn("--varianti", errore.getvalue())


class SimFinto:
    """Simulatore finto con i trade già decisi per variante (V-T ha il target, V-S no): serve a provare
    l'esecutore su casi costruiti a mano, senza mercati."""

    def __init__(self, strategia, compro=None, vendo=None):
        self.strategia, self.compro, self.vendo = strategia, compro or {}, vendo or {}

    @staticmethod
    def nome(par):
        return "V-T" if par.target_r is not None else "V-S"

    def prepara(self, bid, ask, par):
        return []

    def resoconto(self, bid, ask, par):
        return {"giorni_per_motivo": {}, "minuti_spread_negativo": 0}

    def trade(self, giorni, par):
        return self.strategia[self.nome(par)]

    def specchio(self, giorni, par, lato_fisso=None, lati=None):
        return (self.compro if lato_fisso == "acquisto" else self.vendo).get(self.nome(par), [])

    @staticmethod
    def metriche(tr):
        from brain.laboratorio.simulatori import orb_londra as O
        return O.metriche(tr)


def tr(d, r, lato="acquisto"):
    return {"data": d, "lato": lato, "r": r}


class TestRevisioneR7Gemini(BaseRiga):
    """Rilievi P1–P7 della revisione R7 di Gemini (G-20261115-R7, ramo rev/gemini-esecutore-h002), scritti come
    test PRIMA delle correzioni."""

    def verifica(self, varianti="V-T", inizio="2010-01-01", fine="2010-02-28"):
        a = ["--modalita", "verifica", "--inizio", inizio, "--fine", fine]
        return self.lancia(*(a + (["--varianti", varianti] if varianti else [])))

    def verifiche(self):
        return [e for e in S.leggi(self.registro)["esecuzioni"] if e["ruolo"] == "verifica"]

    def test_p1_verifica_solo_delle_varianti_promosse_in_sviluppo(self):
        self.cache_di(date(2010, 1, 1), 59)
        S.sigilla(self.registro, "H-002", self.scheda, ["V-T", "V-S"], ORA)
        self.assertEqual(self.verifica("V-T"), 2)                       # nessuno screening registrato
        self.sviluppo_finto(V_T=False, V_S=False)
        self.assertEqual(self.verifica("V-T"), 2)                       # bocciata in sviluppo
        self.assertEqual(self.verifiche(), [])

    def test_p1_basta_una_bocciatura(self):
        """Uno screening ripetuto non cancella una bocciatura (niente «riprova finché passa»)."""
        self.cache_di(date(2010, 1, 1), 59)
        S.sigilla(self.registro, "H-002", self.scheda, ["V-T", "V-S"], ORA)
        self.sviluppo_finto(V_T=False)
        self.sviluppo_finto(V_T=True, V_S=True)
        self.assertEqual(self.verifica("V-T"), 2)
        self.assertEqual(self.verifica("V-S"), 0)

    def test_p2_tutte_e_sole_le_promosse_in_una_chiamata(self):
        self.cache_di(date(2010, 1, 1), 59)
        S.sigilla(self.registro, "H-002", self.scheda, ["V-T", "V-S"], ORA)
        self.sviluppo_finto(V_T=True, V_S=True)
        self.assertEqual(self.verifica("V-T"), 2)                       # chiamate separate: V del DSR aggirata
        self.assertEqual(self.verifica("V-S"), 2)
        self.assertEqual(self.verifiche(), [])
        self.assertEqual(self.verifica("V-T,V-S"), 0)
        self.assertEqual(sorted(e["variante"] for e in self.verifiche()), ["V-S", "V-T"])

    def test_p3_sigillo_con_varianti_diverse_da_quelle_dell_esecutore(self):
        self.cache_di(date(2024, 1, 1), 60)
        S.sigilla(self.registro, "H-002", self.scheda, ["V-T"], ORA)                 # N = 1 invece di 2
        self.assertEqual(self.lancia("--modalita", "sviluppo", "--inizio", "2024-01-01", "--fine", "2024-02-29"), 2)
        self.assertEqual(S.leggi(self.registro)["esecuzioni"], [])

    def test_p4_anni_del_periodo_nella_riga_di_comando(self):
        """Mercato solo nel 2010, verifica dal 2008: il 2008 e il 2009 contano come anni non positivi."""
        self.cache_di(date(2010, 1, 1), 59, da=date(2008, 1, 1))
        S.sigilla(self.registro, "H-002", self.scheda, ["V-T", "V-S"], ORA)
        self.sviluppo_finto(V_T=True, V_S=False)
        self.assertEqual(self.verifica("V-T", inizio="2008-01-01"), 0)
        riga = [r for r in self.uscita.read_text(encoding="utf-8").splitlines() if "quota di anni solari" in r][0]
        self.assertIn(riga.split("|")[3].strip(), ("0.0000", "0.3333"))

    def test_p6_dati_mancanti_non_bruciano_la_verifica(self):
        S.sigilla(self.registro, "H-002", self.scheda, ["V-T", "V-S"], ORA)
        self.sviluppo_finto(V_T=True, V_S=False)
        self.assertEqual(self.verifica("V-T"), 2)                       # cache inesistente
        self.cache_di(date(2010, 1, 1), 30)                             # cache fino al 30/1, periodo fino al 28/2
        self.assertEqual(self.verifica("V-T"), 2)
        self.assertEqual(self.verifiche(), [])
        self.assertEqual(self.lancia("--modalita", "sviluppo", "--inizio", "2010-01-01", "--fine", "2010-02-28"), 2)

    def test_p5_confronto_casuale_sugli_stessi_giorni(self):
        """Caso di Gemini: 100 giorni comuni (strategia +0,02, compro +0,50, vendo −0,30) e 50 giorni solo della
        strategia a +0,50. Sui 150 giorni R = 0,18 batterebbe il casuale; sui 100 comuni R = 0,02 no."""
        d = [date(2025, 1, 1) + timedelta(days=k) for k in range(150)]
        sim = SimFinto({"V-T": [tr(x, 0.02) for x in d[:100]] + [tr(x, 0.50) for x in d[100:]]},
                       {"V-T": [tr(x, 0.50) for x in d[:100]]}, {"V-T": [tr(x, -0.30, "vendita") for x in d[:100]]})
        from brain.laboratorio.simulatori import orb_londra as O
        x = E.valuta_variante(sim, E._Giorni(sim, {}, {}), O.V_T, {}, 0.2, 1000, 42)
        self.assertAlmostEqual(x["casuale"]["r_strategia"], 0.02)
        self.assertAlmostEqual(x["casuale"]["copertura"], 100 / 150)
        self.assertFalse(x["casuale"]["sopra"])

    def test_mg01_la_verifica_usa_gli_sharpe_delle_altre_promosse(self):
        import random
        rng = random.Random(5)
        d = [date(2005, 1, 3) + timedelta(days=k) for k in range(1000)]
        sim = SimFinto({"V-T": [tr(x, rng.gauss(0.2, 1.0)) for x in d], "V-S": [tr(x, rng.gauss(-0.3, 1.0)) for x in d]})
        r = E.esegui_verifica({}, {}, ["V-T", "V-S"], 2, sim=sim, anni=range(2005, 2008))
        vs = sim.metriche(sim.strategia["V-S"])["sharpe"]
        atteso = K.verifica(sim.strategia["V-T"], 2, anni=range(2005, 2008), sharpe_prove=[vs])["dsr"]
        self.assertEqual(r["varianti"]["V-T"]["verifica"]["dsr"], atteso)
        self.assertNotEqual(atteso, K.verifica(sim.strategia["V-T"], 2, anni=range(2005, 2008))["dsr"])


if __name__ == "__main__":
    unittest.main()
