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
        r = E.esegui_verifica(bid, ask, ["V-T"], n_prove=2, anni=range(2008, 2011))
        self.assertTrue(r["varianti"]["V-T"]["verifica"]["promossa"], r["varianti"]["V-T"]["verifica"])
        self.assertNotIn("V-S", r["varianti"])
        self.assertEqual(list(r["sharpe_prove"]), ["V-T"])                  # solo le promosse girano in verifica
        bid, ask = SN.mercato(date(2008, 1, 1), 800, seme=4, sd=0.7)
        self.assertFalse(E.esegui_verifica(bid, ask, ["V-T", "V-S"], n_prove=2, anni=range(2008, 2011))["varianti"]["V-S"]["verifica"]["promossa"])
        with self.assertRaises(ValueError):
            E.esegui_verifica(bid, ask, ["V-X"], n_prove=2, anni=range(2008, 2011))


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
        self.periodi(sviluppo=(date(2024, 1, 1), date(2024, 2, 29)), verifica=(date(2010, 1, 1), date(2010, 2, 28)))

    def tearDown(self):
        self._tmp.cleanup()

    def periodi(self, sviluppo=None, verifica=None):
        """I periodi sono costanti del codice (R11-S1): i test li sostituiscono con periodi brevi."""
        from unittest import mock
        for nome, valore in (("PERIODO_SVILUPPO", sviluppo), ("PERIODO_VERIFICA", verifica)):
            if valore is not None:
                cerotto = mock.patch.object(E, nome, valore)
                cerotto.start()
                self.addCleanup(cerotto.stop)

    def sigilla(self, varianti=("V-T", "V-S"), codice=None, ipotesi="H-002", scheda=None):
        S.sigilla(self.registro, ipotesi, scheda or self.scheda, list(varianti), ORA,
                  codice=E.impronte_codice() if codice is None else codice)

    def cache_di(self, inizio, giorni, da=None, spinta=0.01):
        """Cache completa come quella vera: un file per ogni giorno di calendario, vuoto nei giorni senza dati.
        `da`: primo giorno della cache, se prima del mercato (giorni vuoti in testa)."""
        bid, ask = SN.mercato(inizio, giorni, seme=2, sd=0.7, spinta=spinta)
        fine = inizio + timedelta(days=giorni - 1)
        SN.scrivi_cache(bid, self.cache / "XAUUSD", inizio=da or inizio, fine=fine)
        SN.scrivi_cache(ask, self.cache / "XAUUSD_ASK", inizio=da or inizio, fine=fine)

    def sviluppo_finto(self, ipotesi="H-002", cache=None, **promosse):
        """Esiti dello screening scritti nel registro come li scriverebbe main (per provare la verifica)."""
        for v, esito in promosse.items():
            S.registra_esecuzione(self.registro, ipotesi, {"ruolo": "sviluppo", "variante": v.replace("_", "-"),
                                                          "promossa": esito,
                                                          "cache": str(Path(cache or self.cache).resolve())}, ORA)

    def lancia(self, *argomenti):
        base = ["--registro", str(self.registro), "--scheda", str(self.scheda), "--cache", str(self.cache),
                "--rapporto", str(self.uscita), "--ora", ORA]
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return E.main(base + list(argomenti))


class TestRigaDiComando(BaseRiga):
    def test_sviluppo_richiede_il_sigillo(self):
        self.cache_di(date(2024, 1, 1), 60)
        self.assertEqual(self.lancia("--modalita", "sviluppo"), 2)
        self.assertFalse(self.uscita.exists())
        self.assertFalse(self.registro.exists())

    def test_sviluppo_registra_le_esecuzioni(self):
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla(["V-T", "V-S"])
        self.assertEqual(self.lancia("--modalita", "sviluppo"), 0)
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
        self.sigilla(["V-T", "V-S"])
        self.periodi(sviluppo=(date(2023, 11, 1), date(2024, 2, 29)), verifica=(date(2024, 1, 1), date(2024, 2, 29)))
        self.assertEqual(self.lancia("--modalita", "sviluppo"), 2)                  # sviluppo nel periodo sigillato
        self.sviluppo_finto(V_T=True, V_S=False)
        self.assertEqual(self.lancia("--modalita", "verifica", "--varianti", "V-T"), 2)   # verifica nello sviluppo
        self.periodi(sviluppo=(date(2024, 1, 1), date(2024, 2, 29)))
        self.scheda.write_text("# H-002 cambiata\n", encoding="utf-8")
        self.assertEqual(self.lancia("--modalita", "sviluppo"), 2)
        self.assertEqual([e for e in S.leggi(self.registro)["esecuzioni"] if "periodo" in e], [])

    def test_verifica_una_volta_sola(self):
        self.cache_di(date(2010, 1, 1), 59)
        self.sigilla(["V-T", "V-S"])
        self.sviluppo_finto(V_T=True, V_S=False)
        argomenti = ("--modalita", "verifica", "--varianti", "V-T")
        self.assertEqual(self.lancia(*argomenti), 0)
        self.assertIn("verifica", self.uscita.read_text(encoding="utf-8"))
        self.assertEqual(self.lancia(*argomenti), 2)
        self.assertEqual(self.lancia("--modalita", "verifica"), 2)

    def test_verifica_senza_varianti_fermata_prima_dei_dati(self):
        """Senza --varianti la verifica si ferma PRIMA di leggere i dati sigillati (mutante E12)."""
        self.sigilla(["V-T", "V-S"])
        errore = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(errore):
            rc = E.main(["--registro", str(self.registro), "--scheda", str(self.scheda), "--cache", str(self.cache),
                         "--rapporto", str(self.uscita), "--ora", ORA, "--modalita", "verifica"])
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

    def verifica(self, varianti="V-T"):
        a = ["--modalita", "verifica"]
        return self.lancia(*(a + (["--varianti", varianti] if varianti else [])))

    def verifiche(self):
        return [e for e in S.leggi(self.registro)["esecuzioni"] if e["ruolo"] == "verifica"]

    def test_p1_verifica_solo_delle_varianti_promosse_in_sviluppo(self):
        self.cache_di(date(2010, 1, 1), 59)
        self.sigilla(["V-T", "V-S"])
        self.assertEqual(self.verifica("V-T"), 2)                       # nessuno screening registrato
        self.sviluppo_finto(V_T=False, V_S=False)
        self.assertEqual(self.verifica("V-T"), 2)                       # bocciata in sviluppo
        self.assertEqual(self.verifiche(), [])

    def test_p1_basta_una_bocciatura(self):
        """Uno screening ripetuto non cancella una bocciatura (niente «riprova finché passa»)."""
        self.cache_di(date(2010, 1, 1), 59)
        self.sigilla(["V-T", "V-S"])
        self.sviluppo_finto(V_T=False)
        self.sviluppo_finto(V_T=True, V_S=True)
        self.assertEqual(self.verifica("V-T"), 2)
        self.assertEqual(self.verifica("V-S"), 0)

    def test_p2_tutte_e_sole_le_promosse_in_una_chiamata(self):
        self.cache_di(date(2010, 1, 1), 59)
        self.sigilla(["V-T", "V-S"])
        self.sviluppo_finto(V_T=True, V_S=True)
        self.assertEqual(self.verifica("V-T"), 2)                       # chiamate separate: V del DSR aggirata
        self.assertEqual(self.verifica("V-S"), 2)
        self.assertEqual(self.verifiche(), [])
        self.assertEqual(self.verifica("V-T,V-S"), 0)
        self.assertEqual(sorted(e["variante"] for e in self.verifiche()), ["V-S", "V-T"])

    def test_p3_sigillo_con_varianti_diverse_da_quelle_dell_esecutore(self):
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla(["V-T"])                 # N = 1 invece di 2
        self.assertEqual(self.lancia("--modalita", "sviluppo"), 2)
        self.assertEqual(S.leggi(self.registro)["esecuzioni"], [])

    def test_p4_anni_del_periodo_nella_riga_di_comando(self):
        """Verifica dal 2008: nel 2008 e nel 2009 ci sono i dati ma nessun trade (mercato piatto, range sotto il minimo
        dei costi); nel 2010 25 trade con R medio +0,27 (anno positivo). Il 2008 e il 2009 contano come anni non
        positivi: quota 1/3, non 1 (mutante E16). Prima stesura: 2010 negativo, non distingueva i casi. Seconda: 2008–2009
        senza dati, che dopo R11-S2 sono un buco dei dati, non «anni senza trade»."""
        piatto_b, piatto_a = SN.mercato(date(2008, 1, 1), 731, seme=2, sd=0.001)
        bid, ask = SN.mercato(date(2010, 1, 1), 59, seme=2, sd=0.7, spinta=0.03)
        piatto_b.update(bid)
        piatto_a.update(ask)
        SN.scrivi_cache(piatto_b, self.cache / "XAUUSD", inizio=date(2008, 1, 1), fine=date(2010, 2, 28))
        SN.scrivi_cache(piatto_a, self.cache / "XAUUSD_ASK", inizio=date(2008, 1, 1), fine=date(2010, 2, 28))
        self.sigilla(["V-T", "V-S"])
        self.sviluppo_finto(V_T=True, V_S=False)
        self.periodi(verifica=(date(2008, 1, 1), date(2010, 2, 28)))
        self.assertEqual(self.verifica("V-T"), 0)
        riga = [r for r in self.uscita.read_text(encoding="utf-8").splitlines() if "quota di anni solari" in r][0]
        self.assertEqual(riga.split("|")[3].strip(), "0.3333")

    def test_p6_dati_mancanti_non_bruciano_la_verifica(self):
        self.sigilla(["V-T", "V-S"])
        self.sviluppo_finto(V_T=True, V_S=False)
        self.assertEqual(self.verifica("V-T"), 2)                       # cache inesistente
        self.cache_di(date(2010, 1, 1), 30)                             # cache fino al 30/1, periodo fino al 28/2
        self.assertEqual(self.verifica("V-T"), 2)
        self.assertEqual(self.verifiche(), [])
        self.cache_di(date(2024, 1, 1), 30)                             # anche lo sviluppo con dati incompleti
        self.assertEqual(self.lancia("--modalita", "sviluppo"), 2)
        self.assertEqual([e for e in S.leggi(self.registro)["esecuzioni"] if e["ruolo"] != "sviluppo" or
                          "periodo" in e], [])

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


class TestRevisioneR11Gemini(BaseRiga):
    """Rilievi R11-S1…S7 e mutanti MR01–MR07 del secondo attacco di Gemini (G-20261115-R11, ramo rev/gemini-r11),
    scritti come test PRIMA delle correzioni. Principio: la riga di comando non lascia scelte libere."""

    def lancia_errore(self, *argomenti):
        base = ["--registro", str(self.registro), "--scheda", str(self.scheda), "--cache", str(self.cache),
                "--rapporto", str(self.uscita), "--ora", ORA]
        errore = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(errore):
            rc = E.main(base + list(argomenti))
        return rc, errore.getvalue()

    def esecuzioni(self, ruolo):
        return [e for e in S.leggi(self.registro)["esecuzioni"] if e["ruolo"] == ruolo]

    def test_s1_s3_nessuna_scelta_libera_dalla_riga_di_comando(self):
        """Periodi, ripetizioni e seme non si scelgono: un'opzione in più è un errore di argparse."""
        for extra in (["--inizio", "2022-08-01"], ["--fine", "2023-10-31"], ["--ripetizioni", "1"], ["--seme", "1"]):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                E.main(["--modalita", "sviluppo", "--rapporto", str(self.uscita)] + extra)

    def test_s1_periodo_di_verifica_fisso_nel_codice(self):
        self.assertEqual(E.PERIODO_VERIFICA[1], date(2010, 2, 28))                 # sostituito dal test
        from unittest import mock
        with mock.patch.object(E, "PERIODO_VERIFICA", E.PERIODO_VERIFICA):
            pass
        import importlib
        modulo = importlib.reload(E)                                               # valori veri del codice
        try:
            self.assertEqual(modulo.PERIODO_VERIFICA, (date(2005, 1, 1), date(2023, 10, 31)))
            self.assertEqual(modulo.PERIODO_SVILUPPO, (date(2023, 11, 15), date(2026, 11, 12)))
        finally:
            self.periodi(sviluppo=(date(2024, 1, 1), date(2024, 2, 29)), verifica=(date(2010, 1, 1), date(2010, 2, 28)))

    def test_s3_e_mr07_lo_sviluppo_registra_esito_ripetizioni_seme_e_dati(self):
        """Mercato casuale di 60 giorni: lo screening boccia (meno di 300 trade) e il registro lo dice."""
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla()
        self.assertEqual(self.lancia("--modalita", "sviluppo"), 0)
        sv = self.esecuzioni("sviluppo")
        self.assertEqual(len(sv), 2)
        for e in sv:
            self.assertIs(e["promossa"], False)                                    # MR07
            self.assertEqual((e["ripetizioni"], e["seme"]), (K.RIPETIZIONI, K.SEME))
            self.assertEqual(e["cache"], str(self.cache.resolve()))
            self.assertEqual(len(e["dati_sha256"]), 64)

    def test_s2_giorni_feriali_vuoti_fermano_tutto(self):
        """File presenti ma vuoti in un giorno feriale = dati mancanti; tollerate solo le chiusure note dell'oro
        (1° gennaio, 25 dicembre, Venerdì Santo)."""
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla()
        for lato in ("XAUUSD", "XAUUSD_ASK"):
            (self.cache / lato / "2024-01-01.bi5").write_bytes(b"")              # Capodanno: chiusura nota
        self.assertEqual(self.lancia("--modalita", "sviluppo"), 0)
        self.registro.unlink()
        self.sigilla()
        (self.cache / "XAUUSD_ASK" / "2024-01-03.bi5").write_bytes(b"")          # mercoledì qualunque, solo ASK
        rc, err = self.lancia_errore("--modalita", "sviluppo")
        self.assertEqual(rc, 2)
        self.assertIn("2024-01-03", err)
        self.assertEqual(self.esecuzioni("sviluppo"), [])

    def test_mr01_mr02_dati_ask_incompleti(self):
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla()
        (self.cache / "XAUUSD_ASK" / "2024-02-12.bi5").unlink()                  # un giorno ASK mancante
        self.assertEqual(self.lancia("--modalita", "sviluppo"), 2)
        for f in (self.cache / "XAUUSD_ASK").glob("*.bi5"):                     # tutti gli ASK vuoti
            f.write_bytes(b"")
        self.assertEqual(self.lancia("--modalita", "sviluppo"), 2)
        self.assertEqual(self.esecuzioni("sviluppo"), [])

    def test_s4_rapporto_non_scrivibile_non_brucia_la_verifica(self):
        self.cache_di(date(2010, 1, 1), 59)
        self.sigilla()
        self.sviluppo_finto(V_T=True, V_S=False)
        self.uscita.mkdir()                                                      # il rapporto è una cartella
        self.assertEqual(self.lancia("--modalita", "verifica", "--varianti", "V-T"), 2)
        self.assertEqual(self.esecuzioni("verifica"), [])

    def test_s4_la_verifica_registra_l_esito(self):
        self.cache_di(date(2010, 1, 1), 59)
        self.sigilla()
        self.sviluppo_finto(V_T=True, V_S=False)
        self.assertEqual(self.lancia("--modalita", "verifica", "--varianti", "V-T"), 0)
        esito = self.esecuzioni("esito")
        self.assertEqual(len(esito), 1)
        for chiave in ("variante", "promossa", "dsr", "r_medio", "quota_anni", "rapporto_sha256"):
            self.assertIn(chiave, esito[0])
        import hashlib
        self.assertEqual(esito[0]["rapporto_sha256"], hashlib.sha256(self.uscita.read_bytes()).hexdigest())
        self.assertEqual(self.esecuzioni("verifica")[0]["cache"], str(self.cache.resolve()))

    def test_s5_copertura_minima_dei_confronti(self):
        """350 giorni della strategia, benchmark e casuale solo su 20 (5,7%): criteri 4 e 5 non passano."""
        d = [date(2025, 1, 1) + timedelta(days=k) for k in range(350)]
        sim = SimFinto({"V-T": [tr(x, 0.30 if k % 2 else -0.10) for k, x in enumerate(d)]},
                       {"V-T": [tr(x, -0.50) for x in d[:20]]}, {"V-T": [tr(x, -0.50, "vendita") for x in d[:20]]})
        from brain.laboratorio.simulatori import orb_londra as O
        x = E.valuta_variante(sim, E._Giorni(sim, {}, {}), O.V_T, {}, 0.0, 1000, 42)
        nomi = {c["nome"]: c["passa"] for c in x["screening"]["criteri"]}
        self.assertFalse(nomi["sopra il 95° percentile del confronto casuale"])
        self.assertFalse(nomi["batte «compro sempre» e «vendo sempre»"])
        self.assertFalse(x["screening"]["promossa"])

    def test_s6_stessa_cache_dello_sviluppo(self):
        self.cache_di(date(2010, 1, 1), 59)
        self.sigilla()
        self.sviluppo_finto(V_T=True, V_S=False, cache=self.dir / "altra_cache")
        self.assertEqual(self.lancia("--modalita", "verifica", "--varianti", "V-T"), 2)
        self.assertEqual(self.esecuzioni("verifica"), [])

    def test_s6_anni_obbligatori_nella_funzione(self):
        with self.assertRaises(TypeError):
            E.esegui_verifica({}, {}, ["V-T"], 2)

    def test_mr03_mr04_ipotesi_diverse_nello_stesso_registro(self):
        self.cache_di(date(2010, 1, 1), 59)
        altra = self.dir / "H-999.md"
        altra.write_text("# H-999\n", encoding="utf-8")
        self.sigilla()
        self.sigilla(ipotesi="H-999", scheda=altra)
        self.sviluppo_finto(ipotesi="H-999", V_T=True)                           # promossa in UN'ALTRA ipotesi
        self.assertEqual(self.lancia("--modalita", "verifica", "--varianti", "V-T"), 2)     # MR03
        S.registra_esecuzione(self.registro, "H-999", {"ruolo": "verifica", "variante": "V-T"}, ORA)
        self.sviluppo_finto(V_T=True, V_S=False)
        self.assertEqual(self.lancia("--modalita", "verifica", "--varianti", "V-T"), 0)     # MR04

    def test_codice_sigillato(self):
        """Il sigillo registra l'impronta del codice che esegue la scheda: se il codice cambia, niente esecuzioni."""
        self.cache_di(date(2024, 1, 1), 60)
        altro = dict(E.impronte_codice())
        primo = sorted(altro)[0]
        altro[primo] = "0" * 64
        self.sigilla(codice=altro)
        rc, err = self.lancia_errore("--modalita", "sviluppo")
        self.assertEqual(rc, 2)
        self.assertIn("codice", err)
        self.registro.unlink()
        S.sigilla(self.registro, "H-002", self.scheda, ["V-T", "V-S"], ORA)        # sigillo senza codice
        self.assertEqual(self.lancia("--modalita", "sviluppo"), 2)
        self.assertEqual(self.esecuzioni("sviluppo"), [])


if __name__ == "__main__":
    unittest.main()
