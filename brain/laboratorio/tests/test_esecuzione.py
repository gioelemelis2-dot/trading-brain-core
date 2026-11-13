"""Test del pacchetto laboratorio/esecuzione: sigillo e registro delle prove, criteri generici (§6–§8 delle schede),
caricatore dei dati. Scritti PRIMA del codice (mandato notturno del 14/11/2026). Dati inventati.
Uso (dalla radice del repository): python3 -s -B -W error -m unittest brain.laboratorio.tests.test_esecuzione
"""
import json
import lzma
import math
import sys
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.dati.pipeline import dukascopy as DK                    # noqa: E402
from brain.laboratorio.esecuzione import caricatore as C            # noqa: E402
from brain.laboratorio.esecuzione import criteri as K               # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S               # noqa: E402

UTC = timezone.utc
ORA = "2026-11-15T03:00:00Z"


class Cartella(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.scheda = self.dir / "H-999.md"
        self.scheda.write_text("# H-999\nregole\n", encoding="utf-8")
        self.registro = self.dir / "registro_prove.json"

    def tearDown(self):
        self._tmp.cleanup()


class TestSigillo(Cartella):
    def test_sigillo_registra_le_prove_dichiarate(self):
        s = S.sigilla(self.registro, "H-999", self.scheda, ["V-T", "V-S"], ORA)
        self.assertEqual(s["scheda_sha256"], S.impronta(self.scheda))
        dati = S.leggi(self.registro)
        self.assertEqual(dati["schema"], S.SCHEMA)
        self.assertEqual([p["id"] for p in dati["prove"]], ["H-999/V-T", "H-999/V-S"])
        self.assertTrue(all(p["ruolo"] == "selezionabile" for p in dati["prove"]))
        self.assertEqual(S.n_prove(dati), 2)

    def test_niente_doppio_sigillo_e_varianti_valide(self):
        S.sigilla(self.registro, "H-999", self.scheda, ["V-T"], ORA)
        with self.assertRaises(ValueError):
            S.sigilla(self.registro, "H-999", self.scheda, ["V-S"], ORA)
        for varianti in ([], ["A", "A"]):
            with self.assertRaises(ValueError):
                S.sigilla(self.registro, "H-998", self.scheda, varianti, ORA)

    def test_controllo_del_sigillo(self):
        with self.assertRaises(S.NonSigillata):
            S.controlla_sigillo(self.registro, "H-999", self.scheda)
        S.sigilla(self.registro, "H-999", self.scheda, ["V-T"], ORA)
        self.assertEqual(S.controlla_sigillo(self.registro, "H-999", self.scheda)["ipotesi"], "H-999")
        self.scheda.write_text("# H-999\nregole cambiate dopo il sigillo\n", encoding="utf-8")
        with self.assertRaises(ValueError) as e:
            S.controlla_sigillo(self.registro, "H-999", self.scheda)
        self.assertIn("modificata dopo il sigillo", str(e.exception))

    def test_esecuzioni_registrate_e_verifica_una_volta_sola(self):
        with self.assertRaises(S.NonSigillata):
            S.registra_esecuzione(self.registro, "H-999", {"ruolo": "sviluppo"}, ORA)
        S.sigilla(self.registro, "H-999", self.scheda, ["V-T"], ORA)
        S.registra_esecuzione(self.registro, "H-999", {"ruolo": "sviluppo", "variante": "V-T"}, ORA)
        S.registra_esecuzione(self.registro, "H-999", {"ruolo": "robustezza", "variante": "V-T or20"}, ORA)
        S.registra_esecuzione(self.registro, "H-999", {"ruolo": "verifica", "variante": "V-T"}, ORA)
        with self.assertRaises(ValueError):
            S.registra_esecuzione(self.registro, "H-999", {"ruolo": "verifica", "variante": "V-T"}, ORA)
        with self.assertRaises(ValueError):
            S.registra_esecuzione(self.registro, "H-999", {"ruolo": "altro"}, ORA)
        dati = S.leggi(self.registro)
        self.assertEqual(len(dati["esecuzioni"]), 3)
        self.assertEqual(S.n_prove(dati), 1)                         # la robustezza non entra in N

    def test_registro_assente_e_vuoto(self):
        self.assertEqual(S.leggi(self.registro), {"schema": S.SCHEMA, "prove": [], "sigilli": [], "esecuzioni": []})
        self.assertFalse(self.registro.exists())


class TestConfrontoCasuale(unittest.TestCase):
    def test_percentile_e_riproducibilita(self):
        esiti = [(1.0, -1.0)] * 50 + [(-1.0, 1.0)] * 50
        a = K.confronto_casuale(esiti, 0.5, ripetizioni=200, seme=7)
        b = K.confronto_casuale(esiti, 0.5, ripetizioni=200, seme=7)
        self.assertEqual(a, b)
        self.assertEqual(a["n_giorni"], 100)
        self.assertEqual(a["ripetizioni"], 200)
        # media casuale di ±1 su 100 giorni: deviazione 0,1, quindi il 95° percentile sta intorno a 0,16
        self.assertGreater(a["percentile_95"], 0.08)
        self.assertLess(a["percentile_95"], 0.26)
        self.assertTrue(a["sopra"])
        self.assertFalse(K.confronto_casuale(esiti, 0.0, ripetizioni=200, seme=7)["sopra"])

    def test_percentile_a_rango(self):
        """Rango più vicino: con le medie ordinate m_1 ≤ … ≤ m_n il 95° percentile è m_ceil(0,95 n)."""
        self.assertEqual(K.percentile([5.0, 1.0, 3.0, 2.0, 4.0], 0.95), 5.0)
        self.assertEqual(K.percentile([float(i) for i in range(1, 101)], 0.95), 95.0)
        with self.assertRaises(ValueError):
            K.percentile([], 0.95)

    def test_niente_giorni(self):
        with self.assertRaises(ValueError):
            K.confronto_casuale([], 0.1, ripetizioni=10, seme=1)


class TestBenchmarkEVeto(unittest.TestCase):
    def test_benchmark_sui_giorni_comuni(self):
        d = [date(2025, 1, k) for k in range(2, 7)]
        strategia = {d[0]: 1.0, d[1]: -1.0, d[2]: 2.0, d[3]: 0.5}
        compro = {d[0]: 1.0, d[1]: 1.0, d[2]: -1.0, d[4]: 3.0}
        vendo = {d[0]: -1.0, d[1]: -1.0, d[2]: 1.0, d[3]: 0.0}
        b = K.confronto_benchmark(strategia, compro, vendo)
        self.assertEqual(b["n_comuni"], 3)                           # d0, d1, d2
        self.assertAlmostEqual(b["r_strategia"], 2.0 / 3)
        self.assertAlmostEqual(b["r_compro"], 1.0 / 3)
        self.assertAlmostEqual(b["r_vendo"], -1.0 / 3)
        self.assertTrue(b["batte_entrambi"])

    def test_veto(self):
        self.assertEqual(K.veto_robustezza(0.10, {"a": 0.08, "b": 0.06}), (False, []))
        veto, motivi = K.veto_robustezza(0.10, {"a": 0.04, "b": 0.0})
        self.assertTrue(veto)
        self.assertEqual(len(motivi), 2)
        self.assertTrue(K.veto_robustezza(0.0, {"a": 0.5})[0])         # base non positiva: niente da proteggere
        self.assertTrue(K.veto_robustezza(0.10, {"a": 0.0499})[0])
        self.assertFalse(K.veto_robustezza(0.10, {"a": 0.05})[0])       # esattamente metà: non scende OLTRE il 50%


def metriche_buone(**diverse):
    m = {"n": 400, "r_medio": 0.10, "sharpe": 0.09, "dd_max": 8.0, "r_vendite": 0.02, "n_vendite": 150}
    m.update(diverse)
    return m


class TestScreening(unittest.TestCase):
    def esito(self, m=None, casuale_sopra=True, batte=True, veto=False, stress=0.03):
        return K.screening(m or metriche_buone(), {"sopra": casuale_sopra, "percentile_95": 0.04},
                           {"batte_entrambi": batte, "r_compro": 0.01, "r_vendo": -0.02}, veto, stress)

    def test_tutti_i_criteri_passano(self):
        e = self.esito()
        self.assertTrue(e["promossa"])
        self.assertEqual(len(e["criteri"]), 9)
        self.assertTrue(all(c["passa"] for c in e["criteri"]))

    def test_ogni_criterio_boccia_da_solo(self):
        casi = [dict(m=metriche_buone(r_medio=0.049)), dict(m=metriche_buone(sharpe=0.059)),
                dict(m=metriche_buone(n=299)), dict(casuale_sopra=False), dict(batte=False),
                dict(m=metriche_buone(r_vendite=-0.051)), dict(m=metriche_buone(dd_max=12.0)), dict(veto=True),
                dict(stress=0.0)]
        for k, caso in enumerate(casi):
            e = self.esito(**caso)
            self.assertFalse(e["promossa"], caso)
            self.assertEqual([c["passa"] for c in e["criteri"]].count(False), 1, caso)
            self.assertFalse(e["criteri"][k]["passa"], caso)

    def test_valori_al_limite(self):
        self.assertTrue(self.esito(m=metriche_buone(r_medio=0.05, sharpe=0.06, n=300, r_vendite=-0.05))["promossa"])

    def test_nessuna_vendita_o_sharpe_mancante_bocciano(self):
        self.assertFalse(self.esito(m=metriche_buone(r_vendite=None, n_vendite=0))["promossa"])
        self.assertFalse(self.esito(m=metriche_buone(sharpe=None))["promossa"])
        self.assertFalse(self.esito(m={"n": 0})["promossa"])


def trade(anno, mese, r):
    return {"data": date(anno, mese, 1), "lato": "acquisto", "r": r}


class TestVerifica(unittest.TestCase):
    def test_criteri_di_verifica(self):
        tr = []
        for anno in range(2005, 2024):
            for mese in range(1, 13):
                tr.append(trade(anno, mese, 1.5 if mese % 2 else -1.0))     # +0,25R in media, ogni anno positivo
        e = K.verifica(tr, n_prove=2)
        self.assertTrue(e["promossa"], e)
        self.assertEqual(len(e["criteri"]), 5)
        self.assertGreater(e["dsr"], 0.95)

    def test_dsr_con_il_numero_di_prove(self):
        """Stesso campione: con più prove il DSR scende (la soglia sale)."""
        import random
        rng = random.Random(3)
        tr = [trade(2005 + k // 120, 1 + (k % 12), rng.gauss(0.05, 1.0)) for k in range(2400)]
        self.assertGreater(K.verifica(tr, n_prove=1)["dsr"], K.verifica(tr, n_prove=40)["dsr"])

    def test_ogni_criterio_di_verifica_boccia(self):
        base = [trade(a, m, 1.5 if m % 2 else -1.0) for a in range(2005, 2024) for m in range(1, 13)]
        perdente = [trade(a, m, -1.0) for a in range(2005, 2024) for m in range(1, 13)]
        self.assertFalse(K.verifica(perdente, n_prove=2)["promossa"])
        # ultimi 5 anni negativi (2019–2023) con il resto molto positivo
        tr = [trade(a, m, (3.0 if m % 2 else -1.0) if a < 2019 else -1.0) for a in range(2005, 2024) for m in range(1, 13)]
        e = K.verifica(tr, n_prove=2)
        self.assertFalse([c for c in e["criteri"] if c["nome"].startswith("ultimi 5")][0]["passa"])
        # drawdown oltre 15R: 16 perdite di fila all'inizio, poi molto positivo
        tr = [trade(2005, 1, -1.0)] * 16 + base
        e = K.verifica(tr, n_prove=2)
        self.assertFalse([c for c in e["criteri"] if c["nome"].startswith("drawdown")][0]["passa"])

    def test_anni_positivi(self):
        tr = [trade(2005, 1, 1.0), trade(2006, 1, -1.0), trade(2007, 1, 1.0), trade(2008, 1, 1.0), trade(2009, 1, -1.0)]
        self.assertAlmostEqual(K.quota_anni_positivi(tr), 0.6)
        self.assertEqual(K.quota_anni_positivi([]), 0.0)


class TestRapporto(unittest.TestCase):
    def test_rapporto_contiene_verdetto_e_criteri(self):
        e = K.screening(metriche_buone(), {"sopra": True, "percentile_95": 0.04},
                        {"batte_entrambi": True, "r_compro": 0.01, "r_vendo": -0.02}, False, 0.03)
        testo = K.rapporto_screening("H-999 V-T", e)
        self.assertIn("PROMOSSA", testo)
        self.assertEqual(testo.count("| ✅ |"), 9)


def bi5(minuti):
    return lzma.compress(b"".join(DK.RECORD.pack(*m) for m in minuti), format=lzma.FORMAT_ALONE)


class TestCaricatore(Cartella):
    def cache(self, nome, giorni, base):
        d = self.dir / nome
        d.mkdir()
        for g in giorni:
            (d / f"{g.isoformat()}.bi5").write_bytes(bi5([(480 * 60, base, base + 10, base - 10, base + 20, 1.0)]))
        return d

    def test_sviluppo(self):
        giorni = [date(2026, 1, 5), date(2026, 1, 6)]
        b = self.cache("bid", giorni, 2650000)
        a = self.cache("ask", giorni[:1], 2650300)
        bid, ask, info = C.carica(b, a, date(2026, 1, 5), date(2026, 1, 7), "sviluppo")
        t = datetime(2026, 1, 5, 8, 0, tzinfo=UTC)
        self.assertEqual(bid[t], (2650.0, 2650.02, 2649.99, 2650.01))      # open, high, low, close
        self.assertEqual(ask[t], (2650.3, 2650.32, 2650.29, 2650.31))
        self.assertEqual((info["giorni_bid_mancanti"], info["giorni_ask_mancanti"]), (1, 2))
        self.assertEqual((info["minuti_bid"], info["minuti_ask"]), (2, 1))

    def test_sviluppo_rifiuta_il_periodo_sigillato(self):
        with self.assertRaises(ValueError):
            C.carica(self.dir, self.dir, date(2023, 11, 14), date(2023, 12, 1), "sviluppo")

    def test_verifica_richiede_il_sigillo_e_il_periodo_vecchio(self):
        b = self.cache("bid", [date(2010, 3, 1)], 1100000)
        a = self.cache("ask", [date(2010, 3, 1)], 1100500)
        with self.assertRaises(S.NonSigillata):
            C.carica(b, a, date(2010, 3, 1), date(2010, 3, 1), "verifica", self.registro, "H-999", self.scheda)
        S.sigilla(self.registro, "H-999", self.scheda, ["V-T"], ORA)
        bid, ask, info = C.carica(b, a, date(2010, 3, 1), date(2010, 3, 1), "verifica", self.registro, "H-999",
                                  self.scheda)
        self.assertEqual(len(bid), 1)
        with self.assertRaises(ValueError):                          # la verifica non tocca lo sviluppo
            C.carica(b, a, date(2023, 11, 1), date(2023, 11, 20), "verifica", self.registro, "H-999", self.scheda)
        with self.assertRaises(ValueError):
            C.carica(b, a, date(2010, 3, 1), date(2010, 3, 1), "boh")


if __name__ == "__main__":
    unittest.main()


class TestCasiAlLimite(Cartella):
    """Aggiunti dopo l'analisi dei mutanti (mutazioni_esecuzione.py): soglie esatte e controlli difensivi."""

    def test_registro_manomesso(self):
        self.registro.write_text(json.dumps({"schema": "altro/9", "prove": [], "sigilli": [], "esecuzioni": []}))
        with self.assertRaises(ValueError):
            S.leggi(self.registro)
        self.registro.write_text(json.dumps({"schema": S.SCHEMA, "prove": [], "sigilli": [],
                                             "esecuzioni": [{"ipotesi": "H-999", "ruolo": "sviluppo"}]}))
        with self.assertRaises(ValueError):                           # esecuzioni prima del sigillo: niente sigillo
            S.sigilla(self.registro, "H-999", self.scheda, ["V-T"], ORA)

    def test_casuale_uguale_al_percentile_non_basta(self):
        self.assertFalse(K.confronto_casuale([(1.0, 1.0)] * 10, 1.0, ripetizioni=50, seme=1)["sopra"])

    def test_percentile_95_della_distribuzione(self):
        """100 giorni a ±1: media con deviazione 0,1; il 95° percentile teorico è 0,1645 (passi di 0,02)."""
        p = K.confronto_casuale([(1.0, -1.0)] * 100, 0.0, ripetizioni=20000, seme=3)["percentile_95"]
        self.assertGreater(p, 0.15)
        self.assertLess(p, 0.19)

    def test_benchmark_battuto_solo_da_uno(self):
        d = [date(2025, 1, 2), date(2025, 1, 3)]
        self.assertFalse(K.confronto_benchmark({d[0]: 0.1, d[1]: 0.1}, {d[0]: 0.3, d[1]: 0.3},
                                               {d[0]: -0.3, d[1]: -0.3})["batte_entrambi"])
        self.assertEqual(K.confronto_benchmark({d[0]: 1.0}, {d[1]: 1.0}, {d[0]: 1.0})["n_comuni"], 0)

    def test_anni_senza_trade_e_quota_esatta(self):
        tr = [trade(2005, 1, 1.0), trade(2006, 1, -1.0), trade(2007, 1, 1.0), trade(2008, 1, 1.0), trade(2009, 1, -1.0)]
        self.assertAlmostEqual(K.quota_anni_positivi(tr, anni=range(2005, 2011)), 0.5)
        e = K.verifica([trade(a, m, 1.0 if a in (2005, 2007, 2008) else -0.5) for a in range(2005, 2010)
                        for m in range(1, 13)], n_prove=1)
        self.assertTrue([c for c in e["criteri"] if c["nome"].startswith("quota")][0]["passa"])     # 60% esatto

    def test_ultimi_cinque_anni_esatti(self):
        tr = [trade(a, m, 1.0 if a < 2019 else -0.1) for a in range(2005, 2024) for m in range(1, 13)]
        e = K.verifica(tr, n_prove=2)
        c = [c for c in e["criteri"] if c["nome"].startswith("ultimi 5")][0]
        self.assertAlmostEqual(c["valore"], -6.0)
        self.assertFalse(c["passa"])

    def test_media_negativa_e_drawdown_in_ordine_di_data(self):
        e = K.verifica([trade(2005, 1, -1.0), trade(2005, 2, -1.2)], n_prove=1)
        self.assertFalse([c for c in e["criteri"] if c["nome"] == "R medio netto"][0]["passa"])
        tr = [trade(2005, 1, -1.0)] * 8 + [trade(2007, 1, -1.0)] * 8 + [trade(2006, 1, 1.0)] * 8   # fuori ordine
        dd = [c for c in K.verifica(tr, n_prove=1)["criteri"] if c["nome"].startswith("drawdown")][0]
        self.assertAlmostEqual(dd["valore"], 8.0)

    def test_momenti(self):
        asim, curt = K._momenti([0.0, 0.0, 0.0, 4.0])
        self.assertAlmostEqual(asim, 6 / 3 ** 1.5)
        self.assertAlmostEqual(curt, 21 / 9)

    def test_periodi_del_caricatore(self):
        S.sigilla(self.registro, "H-999", self.scheda, ["V-T"], ORA)
        with self.assertRaises(ValueError):
            C.carica(self.dir, self.dir, date(2023, 11, 1), date(2023, 11, 15), "verifica", self.registro, "H-999",
                     self.scheda)
        with self.assertRaises(ValueError):
            C.carica(self.dir, self.dir, date(2024, 2, 1), date(2024, 1, 1), "sviluppo")
