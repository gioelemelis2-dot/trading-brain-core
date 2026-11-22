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
from brain.laboratorio.esecuzione import caricatore as _C           # noqa: E402

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
        from unittest import mock
        for nome in ("ANCORA_GIT", "CONTROLLO_AMBIENTE"):                # registri temporanei, fuori da git (#51);
            cerotto = mock.patch.object(E, nome, False)                   # test nello stesso processo (#61)
            cerotto.start()
            self.addCleanup(cerotto.stop)

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
                  codice=E.impronte_codice() if codice is None else codice, robustezza=E.nomi_robustezza())

    def cache_di(self, inizio, giorni, da=None, spinta=0.01):
        """Cache completa come quella vera: un file per ogni giorno di calendario, vuoto nei giorni senza dati.
        `da`: primo giorno della cache, se prima del mercato (giorni vuoti in testa)."""
        bid, ask = SN.mercato(inizio, giorni, seme=2, sd=0.7, spinta=spinta)
        fine = inizio + timedelta(days=giorni - 1)
        SN.scrivi_cache(bid, self.cache / "XAUUSD", inizio=da or inizio, fine=fine)
        SN.scrivi_cache(ask, self.cache / "XAUUSD_ASK", inizio=da or inizio, fine=fine)

    def sviluppo_finto(self, ipotesi="H-002", cache=None, **promosse):
        """Esiti dello screening scritti nel registro come li scriverebbe main (per provare la verifica)."""
        c = Path(cache or self.cache).resolve()
        impronta = _C.impronta_cache(c / "XAUUSD", c / "XAUUSD_ASK", *E.PERIODO_SVILUPPO)    # come la scrive main
        for v, esito in promosse.items():
            S.registra_esecuzione(self.registro, ipotesi, {"ruolo": "sviluppo", "variante": v.replace("_", "-"),
                                                          "promossa": esito, "cache": str(c),
                                                          "dati_sha256": impronta}, ORA)

    def lancia(self, *argomenti):
        base = ["--registro", str(self.registro), "--scheda", str(self.scheda), "--cache", str(self.cache),
                "--rapporto", str(self.uscita), "--ora", ORA]
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return E.main(base + list(argomenti))

    def lancia_errore(self, *argomenti):
        base = ["--registro", str(self.registro), "--scheda", str(self.scheda), "--cache", str(self.cache),
                "--rapporto", str(self.uscita), "--ora", ORA]
        errore = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(errore):
            rc = E.main(base + list(argomenti))
        return rc, errore.getvalue()

    def esecuzioni(self, ruolo):
        return [e for e in S.leggi(self.registro)["esecuzioni"] if e["ruolo"] == ruolo]


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

    def test_p3_sigillo_con_varianti_diverse_da_quelle_dell_esecutore(self):
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla(["V-T"])                 # N = 1 invece di 2
        self.assertEqual(self.lancia("--modalita", "sviluppo"), 2)
        self.assertEqual(S.leggi(self.registro)["esecuzioni"], [])

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

class TestRevisioneR11Gemini(BaseRiga):
    """Rilievi R11-S1…S7 e mutanti MR01–MR07 del secondo attacco di Gemini (G-20261115-R11, ramo rev/gemini-r11),
    scritti come test PRIMA delle correzioni. Principio: la riga di comando non lascia scelte libere."""

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

    def test_mr02_ask_senza_minuti_anche_senza_giorni_feriali(self):
        """Periodo di soli giorni non feriali (sabato e domenica): BID con un minuto, ASK vuoto. Nessun giorno feriale
        vuoto da segnalare, ma zero minuti ASK: fermo (mutante MR02, coperto altrimenti dal controllo dei feriali)."""
        from datetime import datetime, timezone
        self.periodi(sviluppo=(date(2024, 1, 6), date(2024, 1, 7)))
        t = datetime(2024, 1, 6, 10, 0, tzinfo=timezone.utc)
        SN.scrivi_cache({t: (2000.0, 2000.5, 1999.5, 2000.2)}, self.cache / "XAUUSD", inizio=date(2024, 1, 6),
                        fine=date(2024, 1, 7))
        SN.scrivi_cache({}, self.cache / "XAUUSD_ASK", inizio=date(2024, 1, 6), fine=date(2024, 1, 7))
        self.sigilla()
        rc, err = self.lancia_errore("--modalita", "sviluppo")
        self.assertEqual(rc, 2)
        self.assertIn("minuti 1/0", err)
        self.assertEqual(self.esecuzioni("sviluppo"), [])

    def test_s4_rapporto_non_scrivibile_non_brucia_la_verifica(self):
        self.cache_di(date(2010, 1, 1), 59)
        self.sigilla()
        self.sviluppo_finto(V_T=True, V_S=False)
        self.uscita.mkdir()                                                      # il rapporto è una cartella
        self.assertEqual(self.lancia("--modalita", "verifica", "--varianti", "V-T"), 2)
        self.assertEqual(self.esecuzioni("verifica"), [])

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


class TestD51VerificaDisattivata(BaseRiga):
    """D-51 (DA-38 a, 22/11/2026): la verifica del vecchio esecutore è disattivata; passa solo dal percorso ordinario
    D-31 (esegui_verifica). Il rifiuto è IMMEDIATO: nessuna lettura, nessuna scrittura, nessun rapporto. Il caso di
    partenza è valido (cache completa, sigillo, screening promosso), cambia solo la modalità (DGS-16 Q7)."""

    def test_rifiuto_immediato_senza_letture_ne_scritture(self):
        from unittest import mock
        self.cache_di(date(2010, 1, 1), 59)
        self.sigilla(["V-T", "V-S"])
        self.sviluppo_finto(V_T=True, V_S=False)
        prima = self.registro.read_bytes()
        with mock.patch.object(_C, "carica", side_effect=AssertionError("lettura durante una verifica disattivata")) \
                as carica, mock.patch.object(S, "controlla_sigillo", side_effect=AssertionError("sigillo letto")):
            rc, err = self.lancia_errore("--modalita", "verifica", "--varianti", "V-T")
        self.assertEqual(rc, 2)
        self.assertIn("D-51", err)
        self.assertIn("esegui_verifica", err)
        carica.assert_not_called()
        self.assertEqual(self.registro.read_bytes(), prima)
        self.assertFalse(self.uscita.exists())

    def test_lo_sviluppo_resta(self):
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla(["V-T", "V-S"])
        self.assertEqual(self.lancia("--modalita", "sviluppo"), 0)


if __name__ == "__main__":
    unittest.main()


# ---------------------------------------------------------------------------------------------------------------
# R12-bis di Gemini (16/11/2026): #48 codice sigillato completo, #49 completezza, #51 registro e --ora
# ---------------------------------------------------------------------------------------------------------------
import subprocess as _sp                                                    # noqa: E402
import shutil as _sh                                                        # noqa: E402
from brain.laboratorio.esecuzione import caricatore as _C                   # noqa: E402


class TestCodiceSigillatoCompleto(unittest.TestCase):
    """#48 (R12bis-A3-01, mutante MC05): le impronte coprono TUTTO il codice brain che l'esecutore può eseguire."""

    def test_ogni_modulo_brain_caricato_e_nelle_impronte(self):
        prog = ("import sys, json\n"
                "from pathlib import Path\n"
                "import brain.laboratorio.esecuzione.esegui_h002 as E\n"
                "r = E.RADICE.resolve()\n"
                "caricati = sorted(str(Path(m.__file__).resolve().relative_to(r)) for m in list(sys.modules.values())\n"
                "                  if getattr(m, '__file__', None) and Path(m.__file__).resolve().is_relative_to(r / 'brain'))\n"
                "print(json.dumps([c for c in caricati if c not in E.impronte_codice()]))\n")
        if sys.version_info < (3, 9):
            self.skipTest("is_relative_to richiede Python 3.9")
        out = _sp.run([sys.executable, "-s", "-B", "-c", prog], cwd=str(E.RADICE), capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout.strip(), "[]")
        chiavi = E.impronte_codice()
        for f in ("brain/laboratorio/esecuzione/__init__.py", "brain/laboratorio/esecuzione/criteri.py",
                  "brain/dati/pipeline/__init__.py", "brain/laboratorio/backtester/__init__.py",
                  "brain/dati/pipeline/partizione_date.py"):                # importato solo dentro una funzione
            self.assertIn(f, chiavi, f)

    def test_un_init_cambiato_cambia_le_impronte(self):
        with tempfile.TemporaryDirectory() as d:
            copia = Path(d)
            _sh.copytree(E.RADICE / "brain", copia / "brain",
                         ignore=_sh.ignore_patterns("__pycache__", "cache_dukascopy", "*.csv", "partizioni"))
            prima = E.impronte_codice(copia)
            self.assertEqual(prima, {k: v for k, v in E.impronte_codice().items()})
            f = copia / "brain" / "laboratorio" / "esecuzione" / "__init__.py"
            f.write_text(f.read_text() + "\nimport os  # codice nuovo\n")
            dopo = E.impronte_codice(copia)
            self.assertNotEqual(prima["brain/laboratorio/esecuzione/__init__.py"],
                                dopo["brain/laboratorio/esecuzione/__init__.py"])


class TestRigaDiComandoR12bis(BaseRiga):
    def test_un_minuto_per_giorno_non_basta(self):
        """#49: un tick a mezzanotte in ogni giorno non deve far passare lo sviluppo con 0 trade."""
        from datetime import datetime as _dt, timezone as _tz
        minuti = {}
        g = date(2024, 1, 1)
        while g <= date(2024, 2, 29):
            if g.weekday() < 5:
                minuti[_dt(g.year, g.month, g.day, 0, 0, tzinfo=_tz.utc)] = (2000.0, 2000.0, 2000.0, 2000.0)
            g += timedelta(days=1)
        ask = {t: (2000.3, 2000.3, 2000.3, 2000.3) for t in minuti}          # #126: ASK diverso dal BID
        for lato, m in (("XAUUSD", minuti), ("XAUUSD_ASK", ask)):
            SN.scrivi_cache(m, self.cache / lato, inizio=date(2024, 1, 1), fine=date(2024, 2, 29))
        self.sigilla()
        rc, err = self.lancia_errore("--modalita", "sviluppo")
        self.assertEqual(rc, 2)
        self.assertIn("incomplet", err)
        self.assertEqual(self.esecuzioni("sviluppo"), [])

    def test_ora_non_iso_rifiutata(self):
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = E.main(["--registro", str(self.registro), "--scheda", str(self.scheda), "--cache", str(self.cache),
                         "--rapporto", str(self.uscita), "--ora", "ieri sera", "--modalita", "sviluppo"])
        self.assertEqual(rc, 2)
        self.assertEqual(self.esecuzioni("sviluppo"), [])

    def test_ancora_git_attiva_rifiuta_un_registro_fuori_dal_repository(self):
        from unittest import mock
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla()
        with mock.patch.object(E, "ANCORA_GIT", True):
            rc, err = self.lancia_errore("--modalita", "sviluppo")
        self.assertEqual(rc, 2)
        self.assertIn("repository", err)


# ---------------------------------------------------------------------------------------------------------------
# R13 di Gemini (16/11/2026): #61 ambiente, #69 prove di robustezza nel sigillo
# ---------------------------------------------------------------------------------------------------------------
class TestAmbiente(unittest.TestCase):
    """#61 (R13-B-01): codice non sigillato dall'ambiente (PYTHONPATH che ombra la libreria standard, moduli brain
    diversi da quelli sigillati). Prove in processi separati, come il programma vero."""

    def lancia(self, opzioni, prog, env_extra=None):
        import os
        env = dict(os.environ, **(env_extra or {}))
        return _sp.run([sys.executable, *opzioni, "-c", prog], cwd=str(E.RADICE), capture_output=True, text=True,
                       env=env)

    PROG = ("import sys; sys.path.insert(0, '.')\n"
            "import brain.laboratorio.esecuzione.esegui_h002 as E\n"
            "try:\n    E.controlla_ambiente(E.impronte_codice(){extra})\n    print('AMBIENTE OK')\n"
            "except ValueError as e:\n    print('FERMO', e)\n")

    def test_isolato_e_pulito_passa(self):
        out = self.lancia(["-I", "-S", "-B"], self.PROG.format(extra=""))
        self.assertIn("AMBIENTE OK", out.stdout, out.stderr)

    def test_senza_modalita_isolata_si_ferma(self):
        out = self.lancia(["-s", "-B"], self.PROG.format(extra=""))
        self.assertIn("FERMO", out.stdout, out.stderr)
        self.assertIn("-I", out.stdout)

    def test_libreria_standard_ombrata_si_ferma(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "statistics.py").write_text(                       # copia funzionante della vera, ma altrove
                "import importlib.util, os, sysconfig\n"
                "_s = importlib.util.spec_from_file_location('_vera', os.path.join(sysconfig.get_paths()['stdlib'], "
                "'statistics.py'))\n_m = importlib.util.module_from_spec(_s)\n_s.loader.exec_module(_m)\n"
                "globals().update({k: getattr(_m, k) for k in dir(_m) if not k.startswith('__')})\n")
            out = self.lancia(["-s", "-B"], self.PROG.format(extra=", isolato_richiesto=False"),
                              {"PYTHONPATH": d})
        self.assertIn("FERMO", out.stdout, out.stderr)
        self.assertIn("statistics", out.stdout)

    def test_modulo_brain_diverso_dal_sigillato_si_ferma(self):
        prog = ("import sys; sys.path.insert(0, '.')\n"
                "import brain.laboratorio.esecuzione.esegui_h002 as E\n"
                "s = E.impronte_codice(); s['brain/laboratorio/esecuzione/criteri.py'] = '0' * 64\n"
                "try:\n    E.controlla_ambiente(s)\n    print('AMBIENTE OK')\n"
                "except ValueError as e:\n    print('FERMO', e)\n")
        out = self.lancia(["-I", "-S", "-B"], prog)
        self.assertIn("FERMO", out.stdout, out.stderr)
        self.assertIn("criteri.py", out.stdout)


class TestAmbienteInUnaCopia(unittest.TestCase):
    """#87, #88 (revisore del laboratorio, 17/11): attacchi che richiedono file nella cartella del progetto. Si fanno
    in una COPIA di `brain` in una cartella temporanea, mai nel repository vero."""

    PROG = ("import sys; sys.path.insert(0, '.')\n"
            "import brain.laboratorio.esecuzione.esegui_h002 as E\n"
            "import brain.laboratorio.esecuzione.criteri as C\n"
            "try:\n    E.controlla_ambiente(E.impronte_codice())\n    print('AMBIENTE OK', getattr(C, 'ATTACCO', 0))\n"
            "except ValueError as e:\n    print('FERMO', e)\n")

    def setUp(self):
        import shutil
        self._t = tempfile.TemporaryDirectory()
        self.dir = Path(self._t.name)
        shutil.copytree(E.RADICE / "brain", self.dir / "brain", ignore=shutil.ignore_patterns("__pycache__"))

    def tearDown(self):
        self._t.cleanup()

    def lancia(self):
        return _sp.run([sys.executable, "-I", "-S", "-B", "-c", self.PROG], cwd=str(self.dir), capture_output=True,
                       text=True)

    def sysconfig_falso(self):
        """Copia funzionante del sysconfig vero, con get_paths che dice «la libreria standard è /»."""
        import sysconfig
        (self.dir / "sysconfig.py").write_text(
            Path(sysconfig.__file__).read_text(encoding="utf-8") + "\n\ndef get_paths(*a, **k):\n"
            "    return {'stdlib': '/', 'platstdlib': '/', 'purelib': '/nessuno', 'platlib': '/nessuno'}\n",
            encoding="utf-8")

    def test_copia_pulita_passa(self):
        out = self.lancia()
        self.assertIn("AMBIENTE OK 0", out.stdout, out.stderr)

    def test_bytecode_preparato_si_ferma(self):
        """#87: -B non impedisce di LEGGERE i .pyc; un .pyc con data e dimensione del sorgente vero viene eseguito."""
        import importlib.util, marshal, struct
        src = self.dir / "brain/laboratorio/esecuzione/criteri.py"
        codice = compile(src.read_text(encoding="utf-8") + "\nATTACCO = 1\n", str(src), "exec")
        st = src.stat()
        pyc = src.parent / "__pycache__" / f"{src.stem}.{sys.implementation.cache_tag}.pyc"   # R14-02
        pyc.parent.mkdir(parents=True, exist_ok=True)
        pyc.write_bytes(importlib.util.MAGIC_NUMBER + struct.pack("<III", 0, int(st.st_mtime) & 0xFFFFFFFF,
                                                                  st.st_size & 0xFFFFFFFF) + marshal.dumps(codice))
        out = self.lancia()
        self.assertNotIn("AMBIENTE OK", out.stdout, out.stdout + out.stderr)
        self.assertIn("FERMO", out.stdout, out.stderr)
        self.assertIn("criteri", out.stdout)

    def test_sysconfig_falso_non_definisce_la_libreria_standard(self):
        """#88: un sysconfig.py nella cartella di lancio diceva che la libreria standard è «/», e un statistics.py
        avvelenato passava."""
        self.sysconfig_falso()
        import statistics                                                       # copia funzionante, avvelenata
        (self.dir / "statistics.py").write_text(Path(statistics.__file__).read_text(encoding="utf-8")
                                                + "\nAVVELENATO = 1\n", encoding="utf-8")
        out = self.lancia()
        self.assertNotIn("AMBIENTE OK", out.stdout, out.stdout + out.stderr)
        self.assertIn("FERMO", out.stdout, out.stderr)

    def test_cartella_esterna_del_bytecode_si_ferma(self):
        """#87 (copertura, scritto dopo il codice): -X pycache_prefix farebbe leggere bytecode da un'altra cartella."""
        out = _sp.run([sys.executable, "-I", "-S", "-B", "-X", f"pycache_prefix={self.dir / 'pyc'}", "-c", self.PROG],
                      cwd=str(self.dir), capture_output=True, text=True)
        self.assertIn("FERMO", out.stdout, out.stderr)
        self.assertIn("pycache_prefix", out.stdout)

    def test_pacchetti_installati_fuori_dalla_libreria_standard(self):
        """#88 (copertura, scritto dopo il codice): site-packages sta DENTRO la cartella della libreria standard."""
        std = Path("/x/lib/python3.13")
        self.assertTrue(E._fuori_standard(std / "site-packages" / "numpy" / "__init__.py", std))
        self.assertTrue(E._fuori_standard(Path("/usr/lib/python3/dist-packages/a.py"), Path("/usr/lib/python3")))
        self.assertTrue(E._fuori_standard(Path("/altrove/statistics.py"), std))
        self.assertFalse(E._fuori_standard(std / "statistics.py", std))

    def test_sysconfig_falso_da_solo_si_ferma(self):
        """#88: anche se nessun altro modulo è ombrato, un sysconfig fuori dalla libreria standard è un problema."""
        self.sysconfig_falso()
        out = self.lancia()
        self.assertIn("FERMO", out.stdout, out.stdout + out.stderr)


class TestVerificaUnaVoltaNellaStoria(BaseRiga):
    """#86 (revisore del laboratorio, 17/11): la verifica si rifaceva con un secondo registro (--registro libero) o
    con un ramo nuovo da un commit precedente; e N scendeva. Repository git temporaneo con un remoto «GitHub» finto."""

    def setUp(self):
        super().setUp()
        from unittest import mock
        remoto, self.repo = self.dir / "remoto.git", self.dir / "repo"
        _sp.run(["git", "init", "-q", "--bare", str(remoto)], check=True)
        _sp.run(["git", "clone", "-q", str(remoto), str(self.repo)], check=True, capture_output=True)
        self.g = ["git", "-C", str(self.repo), "-c", "user.name=t", "-c", "user.email=t@invalid"]
        _sp.run(self.g + ["checkout", "-q", "-b", "principale"], check=True)
        self.registro = self.repo / "brain" / "laboratorio" / "registro_prove.json"
        self.registro.parent.mkdir(parents=True)
        self.scheda = self.repo / "H-002.md"
        self.scheda.write_text("# H-002 di prova\n", encoding="utf-8")
        for nome, valore in (("RADICE", self.repo), ("ANCORA_GIT", True)):
            cerotto = mock.patch.object(E, nome, valore)
            cerotto.start()
            self.addCleanup(cerotto.stop)
        self.cache_di(date(2024, 1, 1), 60)
        self.cache_di(date(2010, 1, 1), 59)

    def spingi(self, messaggio, ramo="principale"):
        _sp.run(self.g + ["add", "-A"], check=True)
        _sp.run(self.g + ["commit", "-q", "-m", messaggio], check=True)
        _sp.run(self.g + ["push", "-q", "-u", "origin", ramo], check=True, capture_output=True)
        return _sp.run(self.g + ["rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

    def ramo_nuovo(self, nome, commit):
        _sp.run(self.g + ["checkout", "-q", "-b", nome, commit], check=True)
        _sp.run(self.g + ["push", "-q", "-u", "origin", nome], check=True, capture_output=True)

    def prepara(self):
        self.sigilla()
        self.sviluppo_finto(V_T=True, V_S=True)
        return self.spingi("sigillo e sviluppo")

    def test_registro_diverso_da_quello_canonico_rifiutato(self):
        self.prepara()
        bis = self.repo / "registro_bis.json"
        canonico, self.registro = self.registro, bis
        self.prepara()
        rc, err = self.lancia_errore("--modalita", "sviluppo")                 # D-51: protezione comune, sullo sviluppo
        self.assertEqual(rc, 2, err)
        self.assertIn("canonico", err)

    def test_registro_canonico_non_committato_rifiutato(self):
        """Copertura (N09, staccato da #86): con il registro canonico, l'ancora deve ancora pretendere che sia
        identico a quello committato e spinto."""
        self.prepara()
        S.sigilla(self.registro, "H-001", self.scheda, ["X0"], ORA)             # modifica non committata
        rc, err = self.lancia_errore("--modalita", "sviluppo")                 # D-51: protezione comune
        self.assertEqual(rc, 2, err)
        self.assertIn("committ", err)

    def test_storia_parziale_rifiutata(self):
        """R14-03 (Gemini): in un clone parziale (--depth 1) la storia non c'è e la verifica si rifaceva."""
        self.prepara()
        S.sigilla(self.registro, "H-001", self.scheda, ["X0"], ORA)             # D-51: seconda versione del registro
        self.spingi("seconda versione")
        parziale = self.dir / "parziale"
        _sp.run(["git", "clone", "-q", "--depth", "1", "--branch", "principale", f"file://{self.dir / 'remoto.git'}",
                 str(parziale)],
                check=True, capture_output=True)
        with self.assertRaises(ValueError) as e:
            S.versioni_nella_storia(parziale, E.REL_REGISTRO)
        self.assertIn("parziale", str(e.exception))

    def copia_senza_blob(self):
        """Copia parziale (`git clone --filter=blob:none`) con il remoto poi irraggiungibile (rete assente)."""
        remoto = self.dir / "remoto.git"
        _sp.run(["git", "-C", str(remoto), "config", "uploadpack.allowFilter", "true"], check=True)
        copia = self.dir / "senza_blob"
        _sp.run(["git", "clone", "-q", "--filter=blob:none", "--no-checkout", "--branch", "principale",
                 f"file://{remoto}", str(copia)], check=True, capture_output=True)
        _sp.run(["git", "-C", str(copia), "remote", "set-url", "origin", f"file://{self.dir / 'non_esiste.git'}"],
                check=True)
        return copia

    def test_copia_senza_blob_rifiutata(self):
        """#125 (Gemini R18-01): con `--filter=blob:none` e la rete assente `git show` falliva e il commit veniva
        saltato in silenzio: 0 versioni lette, verifica già fatta non vista."""
        self.prepara()
        S.sigilla(self.registro, "H-001", self.scheda, ["X0"], ORA)             # D-51: seconda versione del registro
        self.spingi("seconda versione")
        copia = self.copia_senza_blob()
        with self.assertRaises(ValueError) as e:
            S.versioni_nella_storia(copia, E.REL_REGISTRO)
        self.assertIn("parziale", str(e.exception))

    def test_versione_illeggibile_rifiutata(self):
        """#125: anche senza la configurazione della copia parziale, un file presente in un commit ma illeggibile
        (oggetto mancante) ferma la lettura invece di essere saltato."""
        self.prepara()
        S.sigilla(self.registro, "H-001", self.scheda, ["X0"], ORA)             # seconda versione del registro
        self.spingi("seconda")
        copia = self.copia_senza_blob()
        for chiave in ("remote.origin.promisor", "remote.origin.partialclonefilter"):
            _sp.run(["git", "-C", str(copia), "config", "--unset", chiave], capture_output=True)
        _sp.run(["git", "-C", str(copia), "config", "--unset", "extensions.partialclone"], capture_output=True)
        with self.assertRaises(ValueError) as e:
            S.versioni_nella_storia(copia, E.REL_REGISTRO)
        self.assertIn("illeggibile", str(e.exception))

    def test_commit_che_cancella_il_registro_non_e_un_errore(self):
        """#125: un commit in cui il file non c'è (cancellato) si salta, come prima: non è una versione illeggibile."""
        self.prepara()
        contenuto = self.registro.read_bytes()
        self.registro.unlink()
        self.spingi("tolto")
        self.registro.write_bytes(contenuto)
        self.spingi("rimesso")
        versioni = S.versioni_nella_storia(self.repo, E.REL_REGISTRO)
        self.assertEqual(len(versioni), 2)

class TestEsitoDopoIlControlloFinale(BaseRiga):
    """#91: l'esito (verifica) e gli esiti dello screening (sviluppo) si scrivono DOPO il secondo controllo
    dell'ambiente: se quel controllo ferma, nel registro non resta un risultato contaminato."""

    def ambiente_che_cade_alla_fine(self):
        from unittest import mock
        chiamate = []

        def finto(s):
            chiamate.append(1)
            if len(chiamate) == 2:
                raise ValueError("ambiente non pulito (simulato)")
        for nome, valore in (("CONTROLLO_AMBIENTE", True), ("controlla_ambiente", finto)):
            cerotto = mock.patch.object(E, nome, valore)
            cerotto.start()
            self.addCleanup(cerotto.stop)
        cerotto = mock.patch.object(sys, "_tb_avvio_controllato", True, create=True)       # #95: come dal lanciatore
        cerotto.start()
        self.addCleanup(cerotto.stop)

    def test_sviluppo_senza_esiti(self):
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla()
        self.ambiente_che_cade_alla_fine()
        self.assertEqual(self.lancia("--modalita", "sviluppo"), 2)
        self.assertEqual(self.esecuzioni("sviluppo"), [])
        self.assertEqual(self.esecuzioni("robustezza"), [])


class TestEsitiUnici(BaseRiga):
    def test_un_solo_esito_per_variante_e_solo_dopo_la_verifica(self):
        """#90 (revisore del laboratorio): il registro accettava esiti senza verifica e più esiti, anche
        contraddittori, per la stessa variante."""
        self.sigilla()
        with self.assertRaises(ValueError) as e:
            S.registra_esecuzione(self.registro, "H-002", {"ruolo": "esito", "variante": "V-T", "promossa": True}, ORA)
        self.assertIn("senza verifica", str(e.exception))
        S.registra_esecuzione(self.registro, "H-002", {"ruolo": "verifica", "variante": "V-T", "n_prove": 2}, ORA)
        S.registra_esecuzione(self.registro, "H-002", {"ruolo": "esito", "variante": "V-T", "promossa": False}, ORA)
        with self.assertRaises(ValueError) as e:
            S.registra_esecuzione(self.registro, "H-002", {"ruolo": "esito", "variante": "V-T", "promossa": True}, ORA)
        self.assertIn("già registrato", str(e.exception))
        self.assertEqual([x["promossa"] for x in self.esecuzioni("esito")], [False])


class TestVerificheInsieme(BaseRiga):
    def test_tutte_o_nessuna(self):
        """#94 (c): due lanci con le varianti in ordine diverso registravano una verifica ciascuno e poi si fermavano:
        verifica bruciata senza esito. Ora le verifiche si registrano tutte insieme o nessuna."""
        self.sigilla()
        S.registra_esecuzione(self.registro, "H-002", {"ruolo": "verifica", "variante": "V-S"}, ORA)
        with self.assertRaises(ValueError):
            S.registra_esecuzioni(self.registro, "H-002", [{"ruolo": "verifica", "variante": "V-T"},
                                                           {"ruolo": "verifica", "variante": "V-S"}], ORA)
        self.assertEqual([e["variante"] for e in self.esecuzioni("verifica")], ["V-S"])     # V-T non scritta


class TestFusoOrario(BaseRiga):
    """#94 (d) (revisore del laboratorio): i dati del fuso orario non sono sigillati; un tzdata diverso sposterebbe la
    sessione di Londra con lo stesso codice e la stessa cache. Si controllano contro la regola europea."""

    def test_fuso_vero_passa(self):
        E.controlla_fuso()

    def test_fuso_diverso_ferma_prima_di_ogni_esecuzione(self):
        from unittest import mock
        from zoneinfo import ZoneInfo
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla()
        for zona in ("America/New_York", "UTC", "Europe/Paris"):              # Dublino ha gli stessi orari: non è un errore
            with mock.patch.object(E.O, "LONDRA", ZoneInfo(zona)):
                rc, err = self.lancia_errore("--modalita", "sviluppo")
            self.assertEqual(rc, 2, zona)
            self.assertIn("fuso", err)
        self.assertEqual(self.esecuzioni("sviluppo"), [])


class TestAvvioControllato(unittest.TestCase):
    """#95 (17/11, dagli output di BANCO-02 di Gemini, riprodotto da Claude): i controlli dell'ambiente giravano DOPO
    gli import, quando il codice estraneo era già stato eseguito e poteva manometterli (un .pyc che sostituisce
    importlib.util.cache_from_source dava «AMBIENTE OK»). Il lanciatore controlla tutto PRIMA di importare il progetto.
    Prove in una COPIA di `brain`; il codice estraneo scrive un file-spia quando viene eseguito: non deve esistere."""

    AVVIO = "brain/laboratorio/esecuzione/avvio.py"

    def setUp(self):
        import shutil
        self._t = tempfile.TemporaryDirectory()
        self.dir = Path(self._t.name)
        shutil.copytree(E.RADICE / "brain", self.dir / "brain", ignore=shutil.ignore_patterns("__pycache__"))
        self.spia = self.dir / "SPIA"
        self.sigilla()

    def tearDown(self):
        self._t.cleanup()

    def sigilla(self):
        import json as _json
        reg = self.dir / "brain/laboratorio/registro_prove.json"
        reg.write_text(_json.dumps({"prove": [], "sigilli": [{"ipotesi": "H-002", "codice": E.impronte_codice(self.dir)}],
                                    "esecuzioni": []}), encoding="utf-8")

    def avvia(self, *argomenti, opzioni=("-I", "-S", "-B")):
        return _sp.run([sys.executable, *opzioni, self.AVVIO, *argomenti], cwd=str(self.dir), capture_output=True,
                       text=True)

    def veleno(self):
        return f"\nimport pathlib as _p\n_p.Path({str(self.spia)!r}).write_text('eseguito')\n"

    def test_copia_pulita_arriva_alla_riga_di_comando(self):
        out = self.avvia("--help")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("--modalita", out.stdout)

    def test_bytecode_rifiutato_prima_di_eseguirlo(self):
        import importlib.util, marshal, struct
        src = self.dir / "brain/laboratorio/esecuzione/criteri.py"
        st = src.stat()
        pyc = src.parent / "__pycache__" / f"{src.stem}.{sys.implementation.cache_tag}.pyc"   # R14-02
        pyc.parent.mkdir(parents=True, exist_ok=True)
        pyc.write_bytes(importlib.util.MAGIC_NUMBER + struct.pack("<III", 0, int(st.st_mtime) & 0xFFFFFFFF,
                                                                  st.st_size & 0xFFFFFFFF)
                        + marshal.dumps(compile(src.read_text(encoding="utf-8") + self.veleno(), str(src), "exec")))
        out = self.avvia("--help")
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertIn("__pycache__", out.stderr)
        self.assertFalse(self.spia.exists())

    def test_modulo_nella_cartella_di_lancio_rifiutato_prima_di_eseguirlo(self):
        for nome in ("sysconfig.py", "statistics.py"):
            (self.dir / nome).write_text(self.veleno(), encoding="utf-8")
            out = self.avvia("--help")
            self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
            self.assertIn(nome, out.stderr)
            self.assertFalse(self.spia.exists())
            (self.dir / nome).unlink()

    def test_file_sigillato_modificato_rifiutato_prima_di_eseguirlo(self):
        f = self.dir / "brain/laboratorio/esecuzione/criteri.py"
        f.write_text(f.read_text(encoding="utf-8") + self.veleno(), encoding="utf-8")
        out = self.avvia("--help")
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertIn("criteri.py", out.stderr)
        self.assertFalse(self.spia.exists())

    def test_senza_sigillo_o_senza_modalita_isolata_si_ferma(self):
        (self.dir / "brain/laboratorio/registro_prove.json").unlink()
        out = self.avvia("--help")
        self.assertEqual(out.returncode, 2)
        self.assertIn("sigillo", out.stderr)
        self.sigilla()
        out = self.avvia("--help", opzioni=("-s", "-B"))
        self.assertEqual(out.returncode, 2)
        self.assertIn("-I", out.stderr)

    def test_il_lanciatore_e_sigillato(self):
        self.assertIn(self.AVVIO, E.impronte_codice())


class TestAvvioR14(TestAvvioControllato):
    """R14-01 (Gemini, riprodotto da Claude): una cartella `statistics/` con il solo `__init__.pyc` nella radice
    veniva importata al posto della libreria standard. R14-08, R14-09: coperture mancanti e -B non richiesto."""

    def test_pacchetto_compilato_nella_radice_rifiutato(self):
        import marshal, importlib.util
        d = self.dir / "statistics"
        d.mkdir()
        (d / "__init__.pyc").write_bytes(importlib.util.MAGIC_NUMBER + b"\0" * 12
                                         + marshal.dumps(compile(self.veleno(), "statistics", "exec")))
        out = self.avvia("--help")
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertIn("statistics", out.stderr)
        self.assertFalse(self.spia.exists())

    def test_cartelle_non_importabili_ammesse(self):
        for nome in (".vscode", "dati-utente"):
            (self.dir / nome).mkdir()
        out = self.avvia("--help")
        self.assertEqual(out.returncode, 0, out.stderr)

    def test_archivi_nella_radice_rifiutati(self):
        for nome in ("pacchetto.zip", "ruota.whl", "uovo.egg"):
            (self.dir / nome).write_bytes(b"x")
            out = self.avvia("--help")
            self.assertEqual(out.returncode, 2, nome)
            self.assertIn(nome, out.stderr)
            (self.dir / nome).unlink()

    def test_senza_meno_i_si_ferma(self):
        """Copertura (N61): con -S -B ma senza -I il lanciatore si ferma prima degli import."""
        out = self.avvia("--help", opzioni=("-S", "-B"))
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertIn("-I", out.stderr)
        self.assertFalse(self.spia.exists())

    def test_senza_meno_b_si_ferma(self):
        """#106 (R15-01 di Gemini): sul Python 3.9 di Apple -I implica già -B, quindi lì il caso non esiste: il test
        lo dichiara e si salta, invece di fallire."""
        implicito = _sp.run([sys.executable, "-I", "-S", "-c", "import sys; print(sys.flags.dont_write_bytecode)"],
                            capture_output=True, text=True).stdout.strip()
        if implicito == "1":
            self.skipTest("su questo interprete -I implica già -B (Python di Apple): caso impossibile")
        out = self.avvia("--help", opzioni=("-I", "-S"))
        self.assertEqual(out.returncode, 2)
        self.assertIn("-B", out.stderr)

    def test_cartella_esterna_del_bytecode_si_ferma(self):
        out = self.avvia("--help", opzioni=("-I", "-S", "-B", "-X", f"pycache_prefix={self.dir / 'pyc'}"))
        self.assertEqual(out.returncode, 2)
        self.assertIn("pycache_prefix", out.stderr)


class TestPortabilitaPythonApple(unittest.TestCase):
    def test_test_dell_ambiente_con_cartella_esterna_del_bytecode(self):
        """R14-02 (Gemini, riprodotto da Claude): il Python 3.9 di Apple imposta una cartella esterna per il bytecode
        (~/Library/Caches/com.apple.python) fuori dalla modalità isolata; tre test fallivano. Simulata con
        PYTHONPYCACHEPREFIX."""
        import os
        with tempfile.TemporaryDirectory() as d:
            nomi = ["brain.laboratorio.tests.test_esegui_h002." + t for t in (
                "TestAmbiente.test_libreria_standard_ombrata_si_ferma",
                "TestAmbienteInUnaCopia.test_bytecode_preparato_si_ferma",
                "TestAvvioControllato.test_bytecode_rifiutato_prima_di_eseguirlo")]
            out = _sp.run([sys.executable, "-s", "-B", "-m", "unittest", *nomi], cwd=str(E.RADICE),
                          capture_output=True, text=True, env=dict(os.environ, PYTHONPYCACHEPREFIX=d))
        self.assertEqual(out.returncode, 0, out.stderr[-1500:])


class TestRapportoPrimaDegliEsiti(BaseRiga):
    def test_rapporto_non_scrivibile_niente_esito_dello_sviluppo(self):
        """R14-09 (Gemini), portato sullo sviluppo con D-51: se il rapporto non si scrive, nel registro non resta
        nessun esito senza rapporto."""
        from unittest import mock
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla()
        originale = Path.write_text

        def scrivi(percorso, *a, **k):
            if Path(percorso) == self.uscita:
                raise OSError("disco pieno (simulato)")
            return originale(percorso, *a, **k)
        with mock.patch.object(Path, "write_text", scrivi):
            self.assertEqual(self.lancia("--modalita", "sviluppo"), 2)
        self.assertEqual(self.esecuzioni("sviluppo"), [])
        self.assertEqual(self.esecuzioni("robustezza"), [])


class TestSoloDalLanciatore(BaseRiga):
    def test_con_il_controllo_attivo_serve_il_lanciatore(self):
        """#95: chiamato direttamente, main si ferma (il lanciatore è il solo ingresso con i controlli prima
        degli import). Limite dichiarato: chi lancia il codice a mano può sempre aggirare il lanciatore."""
        from unittest import mock
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla()
        with mock.patch.object(E, "CONTROLLO_AMBIENTE", True), mock.patch.object(E, "controlla_ambiente", lambda s: None):
            rc, err = self.lancia_errore("--modalita", "sviluppo")
        self.assertEqual(rc, 2)
        self.assertIn("avvio.py", err)
        self.assertEqual(self.esecuzioni("sviluppo"), [])


class TestComandoIsolato(unittest.TestCase):
    def test_la_forma_documentata_e_il_lanciatore(self):
        """#95: il comando documentato passa dal lanciatore (controlli prima degli import), non da python3 -c."""
        self.assertIn("python3 -I -S -B brain/laboratorio/esecuzione/avvio.py", E.__doc__)
        self.assertNotIn("python3 -I -S -B -c", E.__doc__)


class TestRigaDiComandoR13(BaseRiga):
    def test_controllo_dell_ambiente_attivo_nello_stesso_processo_si_ferma(self):
        from unittest import mock
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla()
        with mock.patch.object(E, "CONTROLLO_AMBIENTE", True):
            rc, err = self.lancia_errore("--modalita", "sviluppo")
        self.assertEqual(rc, 2)
        self.assertIn("-I", err)
        self.assertEqual(self.esecuzioni("sviluppo"), [])

    def test_ambiente_controllato_all_avvio_e_alla_fine(self):
        from unittest import mock
        self.cache_di(date(2024, 1, 1), 60)
        self.sigilla()
        chiamate = []
        with mock.patch.object(E, "CONTROLLO_AMBIENTE", True), \
                mock.patch.object(sys, "_tb_avvio_controllato", True, create=True), \
                mock.patch.object(E, "controlla_ambiente", lambda s: chiamate.append(sorted(s) == sorted(E.impronte_codice()))):
            self.assertEqual(self.lancia("--modalita", "sviluppo"), 0)
        self.assertEqual(chiamate, [True, True])

    def test_sigillo_senza_le_prove_di_robustezza_dell_esecutore_si_ferma(self):
        self.cache_di(date(2024, 1, 1), 60)
        S.sigilla(self.registro, "H-002", self.scheda, ["V-T", "V-S"], ORA, codice=E.impronte_codice(),
                  robustezza=["range 20'"])
        rc, err = self.lancia_errore("--modalita", "sviluppo")
        self.assertEqual(rc, 2)
        self.assertIn("robustezza", err)

