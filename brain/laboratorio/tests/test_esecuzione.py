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

    def sigillo(self):
        """Sigillo di prova (una volta sola): anche lo sviluppo legge i dati solo con un sigillo valido."""
        if not S.leggi(self.registro)["sigilli"]:
            S.sigilla(self.registro, "H-999", self.scheda, ["V-T"], ORA)
        return self.registro, "H-999", self.scheda


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
            S.registra_esecuzione(self.registro, "H-999", {"ruolo": "altro", "variante": "V-T"}, ORA)   # variante valida
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


class TestMinoriR15(unittest.TestCase):
    """R15 di Gemini, minori nel perimetro (#107, #110), corretti il 17/11 su delega del titolare."""

    def test_copertura_zero_senza_confronto_casuale(self):
        """#107: con il confronto casuale assente la copertura registrata valeva 1,0 (100%)."""
        e = K.screening(metriche_buone(), {}, {"batte_entrambi": True, "r_compro": 0.01, "r_vendo": -0.02}, False,
                        0.03)
        self.assertEqual(e["criteri"][3]["valore"][1], 0.0)
        self.assertFalse(e["criteri"][3]["passa"])

    def test_valori_non_ammessi_rifiutati_con_un_messaggio(self):
        """#110: anni vuoti, Sharpe mancanti e percentili fuori da (0, 1] davano errori generici o valori sbagliati."""
        tr = [trade(2005, 1, 1.0), trade(2005, 2, -1.0)]
        with self.assertRaises(ValueError):
            K.verifica(tr, n_prove=2, anni=[])
        tr = [trade(2005 + k // 12, 1 + k % 12, 1.5 if k % 2 else -1.0) for k in range(60)]
        with self.assertRaises(ValueError):
            K.verifica(tr, n_prove=2, sharpe_prove=[None])
        for q in (-0.5, 0.0, 1.5):
            with self.assertRaises(ValueError, msg=q):
                K.percentile([1.0, 2.0, 3.0], q)
        self.assertEqual(K.percentile([1.0, 2.0, 3.0], 1.0), 3.0)


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
        bid, ask, info = C.carica(b, a, date(2026, 1, 5), date(2026, 1, 7), "sviluppo", *self.sigillo())
        t = datetime(2026, 1, 5, 8, 0, tzinfo=UTC)
        self.assertEqual(bid[t], (2650.0, 2650.02, 2649.99, 2650.01))      # open, high, low, close
        self.assertEqual(ask[t], (2650.3, 2650.32, 2650.29, 2650.31))
        self.assertEqual((info["giorni_bid_mancanti"], info["giorni_ask_mancanti"]), (1, 2))
        self.assertEqual((info["minuti_bid"], info["minuti_ask"]), (2, 1))

    def test_sviluppo_rifiuta_il_periodo_sigillato(self):
        with self.assertRaises(ValueError):
            C.carica(self.dir, self.dir, date(2023, 11, 14), date(2023, 12, 1), "sviluppo", *self.sigillo())

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


class TestRevisioneR7GeminiCriteri(Cartella):
    """Rilievi P4, P7, P8 e mutanti MG03, MG04, MG06, MG07 della revisione R7 di Gemini, scritti PRIMA delle
    correzioni."""

    def test_p4_ultimi_cinque_anni_della_verifica_non_dell_ultimo_trade(self):
        t = [trade(a, 1, 1.0 if a <= 2010 else -0.2) for a in range(2005, 2015)]
        e = K.verifica(t, n_prove=1, anni=range(2005, 2024))
        q = [c for c in e["criteri"] if c["nome"].startswith("quota")][0]
        u = [c for c in e["criteri"] if c["nome"].startswith("ultimi 5")][0]
        self.assertAlmostEqual(q["valore"], 6 / 19)
        self.assertEqual((u["valore"], u["passa"]), (0.0, False))             # 2019–2023 senza trade

    def criterio(self, t, inizio):
        return [c for c in K.verifica(t, n_prove=1)["criteri"] if c["nome"].startswith(inizio)][0]

    def test_mg03_r_medio_zero_non_passa(self):
        self.assertFalse(self.criterio([trade(2005 + k % 10, 1, 1.0 if k % 2 else -1.0) for k in range(100)],
                                       "R medio")["passa"])

    def test_mg04_drawdown_di_15_esatti_non_passa(self):
        t = [trade(2005, 1, 1.0)] + [trade(2005, 2, -1.0)] * 15 + [trade(2006, 1, 2.0)] * 20
        c = self.criterio(t, "drawdown")
        self.assertEqual((c["valore"], c["passa"]), (15.0, False))

    def test_mg07_ultimi_cinque_anni_a_zero_non_passano(self):
        t = [trade(a, 1, 3.0) for a in range(2005, 2019)] + [trade(a, m, 1.0 if m == 1 else -1.0)
                                                            for a in range(2019, 2024) for m in (1, 2)]
        c = self.criterio(t, "ultimi 5")
        self.assertEqual((c["valore"], c["passa"]), (0.0, False))

    def test_mg06_dsr_con_la_varianza_nulla_1_su_t_meno_1(self):
        """Valore atteso ricalcolato a parte: Sharpe campionario, momenti di popolazione, V = 1/(T − 1)."""
        from statistics import mean, stdev
        from brain.laboratorio.backtester.dsr import DSRCalculator
        rs = [0.9, -1.0, 1.5, -1.0, 0.4, 1.5, -1.0, 2.0, -0.3, 0.8] * 4                 # 40 trade (DSR da 30)
        t = [trade(2005 + k // 12, 1 + k % 12, r) for k, r in enumerate(rs)]
        mu, n = mean(rs), len(rs)
        m2 = sum((x - mu) ** 2 for x in rs) / n
        asim = (sum((x - mu) ** 3 for x in rs) / n) / m2 ** 1.5
        curt = (sum((x - mu) ** 4 for x in rs) / n) / m2 ** 2
        atteso, _ = DSRCalculator.calculate_dsr_analytical(mu / stdev(rs), 2, n, asim, curt,
                                                          varianza_sr_prove=1.0 / (n - 1))
        self.assertAlmostEqual(K.verifica(t, n_prove=2)["dsr"], atteso, places=12)

    def test_p7_embargo_chiuso_in_verifica(self):
        S.sigilla(self.registro, "H-999", self.scheda, ["V-T"], ORA)
        with self.assertRaises(ValueError):
            C.carica(self.dir, self.dir, date(2023, 10, 1), date(2023, 11, 1), "verifica", self.registro, "H-999",
                     self.scheda)
        C.carica(self.dir, self.dir, date(2023, 10, 1), date(2023, 10, 31), "verifica", self.registro, "H-999",
                 self.scheda)

    def test_p8_scritture_concorrenti_non_si_perdono(self):
        import threading
        S.sigilla(self.registro, "H-999", self.scheda, ["V-T"], ORA)
        errori = []

        def scrivi(k):
            try:
                for j in range(15):
                    S.registra_esecuzione(self.registro, "H-999", {"ruolo": "robustezza", "variante": f"V-T {k}-{j}"},
                                          ORA)
            except Exception as e:                                       # noqa: BLE001
                errori.append(e)
        fili = [threading.Thread(target=scrivi, args=(k,)) for k in range(4)]
        for f in fili:
            f.start()
        for f in fili:
            f.join()
        self.assertEqual(errori, [])
        self.assertEqual(len(S.leggi(self.registro)["esecuzioni"]), 60)


class TestBloccoDelloSviluppo(Cartella):
    """Incidente del 14/11 (difetto #41): script esterni hanno letto i dati veri dello sviluppo senza sigillo, perché il
    caricatore lo controllava solo in verifica. Ora lo controlla in entrambe le modalità. Scritto PRIMA del codice."""

    def test_sviluppo_senza_sigillo_rifiutato(self):
        d = self.dir / "c"
        d.mkdir()
        with self.assertRaises(S.NonSigillata):
            C.carica(d, d, date(2026, 1, 5), date(2026, 1, 5), "sviluppo")
        with self.assertRaises(S.NonSigillata):
            C.carica(d, d, date(2026, 1, 5), date(2026, 1, 5), "sviluppo", self.registro, "H-999", self.scheda)
        C.carica(d, d, date(2026, 1, 5), date(2026, 1, 5), "sviluppo", *self.sigillo())
        self.scheda.write_text("# H-999 cambiata\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            C.carica(d, d, date(2026, 1, 5), date(2026, 1, 5), "sviluppo", self.registro, "H-999", self.scheda)


class TestRevisioneR11GeminiCriteri(Cartella):
    """R11-S1 (DSR con pochi trade), R11-S2 (giorni feriali vuoti), R11-S6 (impronta dei dati), R11-S7 (varianti
    fuori dal sigillo), MR06 (DSR al confine), impronta del codice nel sigillo. Scritti PRIMA delle correzioni."""

    def test_s1_niente_dsr_sotto_30_trade(self):
        e = K.verifica([trade(2005, 1, 1.0), trade(2006, 1, 2.0)], n_prove=1)
        self.assertIsNone(e["dsr"])
        self.assertFalse(e["promossa"])
        rs = [1.0, -0.5] * 15
        self.assertIsNotNone(K.verifica([trade(2005 + k // 12, 1 + k % 12, r) for k, r in enumerate(rs)], 1)["dsr"])

    def test_mr06_dsr_uguale_alla_soglia_passa(self):
        rs = [1.0, -0.6, 0.4, -0.2, 0.9] * 10
        t = [trade(2005 + k // 12, 1 + k % 12, r) for k, r in enumerate(rs)]
        d = K.verifica(t, n_prove=2)["dsr"]
        c = [c for c in K.verifica(t, n_prove=2, dsr_min=d)["criteri"] if c["nome"].startswith("DSR")][0]
        self.assertTrue(c["passa"])

    def test_s7_varianti_fuori_dal_sigillo(self):
        S.sigilla(self.registro, "H-999", self.scheda, ["V-T"], ORA)
        with self.assertRaises(ValueError):
            S.registra_esecuzione(self.registro, "H-999", {"ruolo": "sviluppo", "variante": "INVENTATA"}, ORA)
        with self.assertRaises(ValueError):
            S.registra_esecuzione(self.registro, "H-999", {"ruolo": "sviluppo"}, ORA)
        S.registra_esecuzione(self.registro, "H-999", {"ruolo": "robustezza", "variante": "V-T range 20'"}, ORA)
        S.registra_esecuzione(self.registro, "H-999", {"ruolo": "verifica", "variante": "V-T"}, ORA)   # #90
        S.registra_esecuzione(self.registro, "H-999", {"ruolo": "esito", "variante": "V-T", "promossa": False}, ORA)

    def test_codice_nel_sigillo(self):
        S.sigilla(self.registro, "H-999", self.scheda, ["V-T"], ORA, codice={"a.py": "1" * 64})
        self.assertEqual(S.controlla_sigillo(self.registro, "H-999", self.scheda, codice={"a.py": "1" * 64})["codice"],
                         {"a.py": "1" * 64})
        with self.assertRaises(ValueError):
            S.controlla_sigillo(self.registro, "H-999", self.scheda, codice={"a.py": "2" * 64})

    def test_s2_giorni_feriali_vuoti_e_chiusure_note(self):
        for nome in ("bid", "ask"):
            d = self.dir / nome
            d.mkdir()
            for g in (date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 3), date(2026, 4, 3)):   # gio, ven, sab, Ven. Santo
                (d / f"{g.isoformat()}.bi5").write_bytes(b"")
            (d / "2026-01-05.bi5").write_bytes(bi5([(480 * 60, 2650000, 2650010, 2649990, 2650020, 1.0)]))
        _, _, info = C.carica(self.dir / "bid", self.dir / "ask", date(2026, 1, 1), date(2026, 1, 5), "sviluppo", *self.sigillo())
        self.assertEqual(info["feriali_vuoti_bid"], ["2026-01-02"])               # il 1/1 è chiusura nota
        self.assertEqual(info["feriali_vuoti_ask"], ["2026-01-02"])
        _, _, info = C.carica(self.dir / "bid", self.dir / "ask", date(2026, 4, 3), date(2026, 4, 3), "sviluppo", *self.sigillo())
        self.assertEqual(info["feriali_vuoti_bid"], [])                           # Venerdì Santo

    def test_s6_impronta_dei_dati_letti(self):
        for nome in ("bid", "ask"):
            d = self.dir / nome
            d.mkdir()
            (d / "2026-01-05.bi5").write_bytes(bi5([(480 * 60, 2650000, 2650010, 2649990, 2650020, 1.0)]))
        a = C.carica(self.dir / "bid", self.dir / "ask", date(2026, 1, 5), date(2026, 1, 5), "sviluppo", *self.sigillo())[2]
        self.assertEqual(len(a["dati_sha256"]), 64)
        self.assertEqual(a["dati_sha256"],
                         C.carica(self.dir / "bid", self.dir / "ask", date(2026, 1, 5), date(2026, 1, 5), "sviluppo", *self.sigillo())[2]["dati_sha256"])
        (self.dir / "ask" / "2026-01-05.bi5").write_bytes(bi5([(480 * 60, 2650300, 2650310, 2650290, 2650320, 1.0)]))
        b = C.carica(self.dir / "bid", self.dir / "ask", date(2026, 1, 5), date(2026, 1, 5), "sviluppo", *self.sigillo())[2]
        self.assertNotEqual(a["dati_sha256"], b["dati_sha256"])


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
            C.carica(self.dir, self.dir, date(2024, 2, 1), date(2024, 1, 1), "sviluppo", *self.sigillo())


# ---------------------------------------------------------------------------------------------------------------
# R12-bis di Gemini (16/11/2026): #49 completezza dei giorni, #50 festività spostate, #51 registro
# ---------------------------------------------------------------------------------------------------------------
from datetime import time as _ora, timedelta as _td          # noqa: E402
import subprocess as _sp                                    # noqa: E402
from brain.laboratorio.esecuzione import sintetico as _SN   # noqa: E402


def _minuti(giorno, quanti, dalle=_ora(8, 0)):
    """`quanti` minuti di fila dall'ora di Londra `dalle`, prezzi piatti."""
    from brain.laboratorio.simulatori.orb_londra import _utc
    t0 = _utc(giorno, dalle)
    return {t0 + _td(minutes=k): (2000.0, 2000.5, 1999.5, 2000.0) for k in range(quanti)}


class TestCompletezzaDeiGiorni(Cartella):
    """#49 (R12bis-A3-02): un giorno feriale con un solo minuto non è un giorno con i dati."""

    def carica(self, minuti, inizio, fine):
        for lato in ("XAUUSD", "XAUUSD_ASK"):
            _SN.scrivi_cache(minuti, self.dir / lato, inizio=inizio, fine=fine)
        return C.carica(self.dir / "XAUUSD", self.dir / "XAUUSD_ASK", inizio, fine, "sviluppo", *self.sigillo())

    def test_un_minuto_a_mezzanotte_non_basta(self):
        g1, g2, g3 = date(2024, 1, 8), date(2024, 1, 9), date(2024, 1, 10)            # lunedì, martedì, mercoledì
        m = {}
        m.update(_minuti(g1, 525))                                                   # sessione piena
        m[datetime(2024, 1, 9, 0, 0, tzinfo=timezone.utc)] = (2000.0, 2000.0, 2000.0, 2000.0)   # un minuto fittizio
        m.update(_minuti(g3, 262))                                                   # sotto la metà della sessione
        g4 = date(2024, 1, 11)
        m.update(_minuti(g4, 400, dalle=_ora(17, 0)))                                # tanti minuti, ma fuori sessione
        _, _, info = self.carica(m, g1, g4)
        self.assertEqual(info["feriali_vuoti_bid"], [])
        self.assertEqual(info["feriali_incompleti_bid"], ["2024-01-09", "2024-01-10", "2024-01-11"])
        self.assertEqual(info["feriali_incompleti_ask"], ["2024-01-09", "2024-01-10", "2024-01-11"])

    def test_meta_sessione_basta_e_i_giorni_corti_noti_sono_tollerati(self):
        g = date(2024, 1, 11)
        m = _minuti(g, 88)                                                           # metà sessione, su tutti i terzi
        m.update(_minuti(g, 88, dalle=_ora(10, 55)))
        m.update(_minuti(g, 87, dalle=_ora(13, 50)))
        m.update(_minuti(date(2024, 12, 24), 60))                                    # vigilia: giornata corta nota
        _, _, info = self.carica(m, g, g)
        self.assertEqual(info["feriali_incompleti_bid"], [])
        _, _, info = self.carica(m, date(2024, 12, 24), date(2024, 12, 24))
        self.assertEqual(info["feriali_incompleti_bid"], [])

    def test_impronta_della_cache_uguale_a_quella_del_caricatore(self):
        g1, g2 = date(2024, 1, 8), date(2024, 1, 9)
        m = _minuti(g1, 525)
        m.update(_minuti(g2, 525))
        _, _, info = self.carica(m, g1, g2)
        self.assertEqual(C.impronta_cache(self.dir / "XAUUSD", self.dir / "XAUUSD_ASK", g1, g2), info["dati_sha256"])
        self.assertNotEqual(C.impronta_cache(self.dir / "XAUUSD", self.dir / "XAUUSD_ASK", g1, g1), info["dati_sha256"])


class TestCompletezzaPerTerzi(TestCompletezzaDeiGiorni):
    """#63 (R13-B-03): il totale non basta; ogni terzo della sessione deve avere minuti; le vigilie il mattino."""

    def test_tutto_nel_pomeriggio_non_basta(self):
        g = date(2024, 1, 15)
        m = _minuti(g, 263, dalle=_ora(12, 22))
        _, _, info = self.carica(m, g, g)
        self.assertEqual(info["feriali_incompleti_bid"], ["2024-01-15"])

    def test_vigilia_con_un_solo_minuto_non_basta(self):
        g = date(2024, 12, 24)
        m = {datetime(2024, 12, 24, 0, 0, tzinfo=timezone.utc): (2000.0, 2000.0, 2000.0, 2000.0)}
        _, _, info = self.carica(m, g, g)
        self.assertEqual(info["feriali_incompleti_bid"], ["2024-12-24"])

    def test_minuti_fuori_sessione_non_contano(self):
        """Mutante N15: i minuti dopo le 16:45 (o prima delle 08:00) non riempiono i terzi della sessione."""
        g = date(2024, 1, 17)
        m = _minuti(g, 132)                                                          # terzo 1 pieno
        m.update(_minuti(g, 131, dalle=_ora(10, 55)))                                # terzo 2 pieno (totale 263)
        m.update(_minuti(g, 60, dalle=_ora(17, 0)))                                  # dopo la sessione: non contano
        _, _, info = self.carica(m, g, g)
        self.assertEqual(info["feriali_incompleti_bid"], ["2024-01-17"])             # terzo 3 vuoto

    def test_un_terzo_quasi_vuoto_non_basta(self):
        g = date(2024, 1, 16)
        m = _minuti(g, 175)
        m.update(_minuti(g, 175, dalle=_ora(10, 55)))
        m.update(_minuti(g, 43, dalle=_ora(13, 50)))                                 # 43 < 44 (25% di 175)
        _, _, info = self.carica(m, g, g)
        self.assertEqual(info["feriali_incompleti_bid"], ["2024-01-16"])
        m.update(_minuti(g, 44, dalle=_ora(13, 50)))
        _, _, info = self.carica(m, g, g)
        self.assertEqual(info["feriali_incompleti_bid"], [])


class TestMinutiDistinti(unittest.TestCase):
    def test_record_ripetuti_non_fanno_completezza(self):
        """#85 (revisore del laboratorio, notte del 17/11): la completezza contava i record, non i minuti distinti; un
        file con lo stesso minuto ripetuto 600 volte passava per un giorno completo."""
        g = date(2024, 1, 15)
        t = [datetime(2024, 1, 15, h, m, tzinfo=timezone.utc) for h, m in ((8, 30), (11, 0), (14, 0))]
        self.assertFalse(C._completo([x for x in t for _ in range(200)], g, False))
        self.assertTrue(C._completo(list(_minuti(g, 525)), g, False))


class TestFestivitaSpostate(unittest.TestCase):
    """#50 (R12bis-A3-03): 26/12, i giorni spostati di 1/1 e 25/12, il Lunedì dell'Angelo."""

    def test_chiusure_note_comprese_le_spostate(self):
        attese = ["2005-12-26", "2005-12-27", "2006-01-02", "2010-12-24", "2010-12-27", "2010-12-28", "2010-12-31",
                  "2011-12-26", "2011-12-27", "2012-01-02", "2016-12-26", "2016-12-27", "2017-01-02", "2021-12-24",
                  "2021-12-27", "2021-12-28", "2022-12-26", "2022-12-27", "2023-01-02", "2010-04-05"]
        for g in attese:
            d = date.fromisoformat(g)
            self.assertIn(d, C.chiusure_note(d.year), g)
        from brain.dati.pipeline import controlla_cache as CC
        self.assertIs(CC.chiusure_note, C.chiusure_note)          # una sola fonte: niente copie che divergono
        for g in ("2005-03-15", "2010-12-29", "2023-01-03", "2016-12-28"):
            d = date.fromisoformat(g)
            self.assertNotIn(d, C.chiusure_note(d.year), g)


class TestRegistroR12bis(Cartella):
    """#51 (R12bis-A3-04)."""

    def test_varianti_con_nomi_esatti_e_robustezza_ben_formata(self):
        S.sigilla(self.registro, "H-999", self.scheda, ["V-T", "V-S"], ORA)
        with self.assertRaises(ValueError):
            S.registra_esecuzione(self.registro, "H-999", {"ruolo": "sviluppo", "variante": "V-T taroccata_extra"}, ORA)
        with self.assertRaises(ValueError):
            S.registra_esecuzione(self.registro, "H-999", {"ruolo": "robustezza", "variante": "V-T"}, ORA)
        with self.assertRaises(ValueError):
            S.registra_esecuzione(self.registro, "H-999", {"ruolo": "robustezza", "variante": "V-X range 20'"}, ORA)
        S.registra_esecuzione(self.registro, "H-999", {"ruolo": "robustezza", "variante": "V-T range 20'"}, ORA)
        S.registra_esecuzione(self.registro, "H-999", {"ruolo": "sviluppo", "variante": "V-S"}, ORA)

    def test_prove_di_robustezza_dichiarate_al_sigillo(self):
        """#69 (R13-B-06): con l'elenco al sigillo, una prova di robustezza non dichiarata è rifiutata."""
        S.sigilla(self.registro, "H-999", self.scheda, ["V-T"], ORA, robustezza=["range 20'", "tetto 1,6"])
        S.registra_esecuzione(self.registro, "H-999", {"ruolo": "robustezza", "variante": "V-T range 20'"}, ORA)
        with self.assertRaises(ValueError):
            S.registra_esecuzione(self.registro, "H-999", {"ruolo": "robustezza", "variante": "V-T range 45'"}, ORA)
        self.assertEqual(S.controlla_sigillo(self.registro, "H-999", self.scheda)["robustezza"],
                         ["range 20'", "tetto 1,6"])

    def test_codice_sigillato_controllato_anche_senza_passarlo(self):
        radice = self.dir / "radice"
        (radice / "pkg").mkdir(parents=True)
        f = radice / "pkg" / "a.py"
        f.write_text("x = 1\n")
        import hashlib
        S.sigilla(self.registro, "H-999", self.scheda, ["V-T"], ORA,
                  codice={"pkg/a.py": hashlib.sha256(f.read_bytes()).hexdigest()})
        S.controlla_sigillo(self.registro, "H-999", self.scheda, radice=radice)
        f.write_text("x = 2\n")
        with self.assertRaises(ValueError):
            S.controlla_sigillo(self.registro, "H-999", self.scheda, radice=radice)
        f.unlink()
        with self.assertRaises(ValueError):
            S.controlla_sigillo(self.registro, "H-999", self.scheda, radice=radice)

    def _repo_con_remoto(self):
        remoto, repo = self.dir / "remoto.git", self.dir / "repo"
        _sp.run(["git", "init", "-q", "--bare", str(remoto)], check=True)
        _sp.run(["git", "clone", "-q", str(remoto), str(repo)], check=True, capture_output=True)
        g = ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@invalid"]
        _sp.run(g + ["checkout", "-q", "-b", "principale"], check=True)
        reg = repo / "registro_prove.json"
        S.sigilla(reg, "H-999", self.scheda, ["V-T"], ORA)
        _sp.run(g + ["add", "registro_prove.json"], check=True)
        _sp.run(g + ["commit", "-q", "-m", "sigillo"], check=True)
        _sp.run(g + ["push", "-q", "-u", "origin", "principale"], check=True, capture_output=True)
        return repo, reg, g

    def test_ancora_ogni_controllo_scatta_da_solo(self):
        """Mutanti N06, N07, N24, N26: ogni controllo deve fermare da solo, con il SUO messaggio (un altro
        controllo che scatta per caso nello stesso scenario non vale)."""
        repo, reg, g = self._repo_con_remoto()
        reg2 = repo / "secondo.json"                                                 # N07: file mai committato
        S.sigilla(reg2, "H-998", self.scheda, ["V-T"], ORA)
        with self.assertRaisesRegex(ValueError, "non è versionato"):
            S.controlla_ancora(reg2, repo)
        import os as _os                                                             # N26: storia riscritta,
        _sp.run(g + ["commit", "-q", "--amend", "--no-edit"], check=True,             # registro IDENTICO (ora
               env=dict(_os.environ, GIT_COMMITTER_DATE="2030-01-01T00:00:00 +0000"))  # diversa: hash diverso)
        with self.assertRaisesRegex(ValueError, "non contiene"):
            S.controlla_ancora(reg, repo)
        _sp.run(g + ["reset", "-q", "--hard", "origin/principale"], check=True)
        dati = json.loads(reg.read_text())                                           # N06: voce già su GitHub
        dati["sigilli"][0]["scheda_sha256"] = "0" * 64                               # cambiata, con un commit
        reg.write_text(json.dumps(dati))                                             # NORMALE (storia intatta)
        _sp.run(g + ["commit", "-q", "-am", "voce cambiata"], check=True)
        with self.assertRaisesRegex(ValueError, "voci cambiate o tolte"):
            S.controlla_ancora(reg, repo)
        _sp.run(g + ["reset", "-q", "--hard", "origin/principale"], check=True)
        _sp.run(g + ["checkout", "-q", "--detach"], check=True)                      # N24: HEAD staccata,
        with self.assertRaisesRegex(ValueError, "staccata"):                         # col suo messaggio
            S.controlla_ancora(reg, repo)

    def test_registro_ancorato_alla_versione_su_github(self):
        """#62 (R13-B-02): registro identico alla HEAD, HEAD su un ramo che contiene la versione remota, registro
        della HEAD che continua quello remoto, nessun collegamento simbolico."""
        repo, reg, g = self._repo_con_remoto()
        S.controlla_ancora(reg, repo)                                             # pulito e uguale a GitHub
        S.registra_esecuzione(reg, "H-999", {"ruolo": "sviluppo", "variante": "V-T", "promossa": False}, ORA)
        with self.assertRaises(ValueError):                                       # aggiunta non committata: no
            S.controlla_ancora(reg, repo)
        _sp.run(g + ["commit", "-q", "-am", "sviluppo"], check=True)
        S.controlla_ancora(reg, repo)                                             # committata, non ancora spinta: sì
        _sp.run(g + ["push", "-q"], check=True, capture_output=True)
        dati = json.loads(reg.read_text())
        dati["esecuzioni"][0]["promossa"] = True                                  # manomissione di una voce spinta
        reg.write_text(json.dumps(dati))
        _sp.run(g + ["commit", "-q", "-a", "--amend", "-m", "riscritto"], check=True)
        with self.assertRaises(ValueError):                                       # --amend: non discende da GitHub
            S.controlla_ancora(reg, repo)
        _sp.run(g + ["reset", "-q", "--hard", "origin/principale"], check=True)
        S.controlla_ancora(reg, repo)
        _sp.run(g + ["checkout", "-q", "--detach", "HEAD~1"], check=True)
        with self.assertRaises(ValueError):                                       # HEAD staccata
            S.controlla_ancora(reg, repo)
        _sp.run(g + ["checkout", "-q", "-b", "senza_verifica"], check=True)
        with self.assertRaises(ValueError):                                       # ramo senza versione remota
            S.controlla_ancora(reg, repo)
        _sp.run(g + ["checkout", "-q", "principale"], check=True)
        collegamento = repo / "altro.json"
        collegamento.symlink_to(reg)
        with self.assertRaises(ValueError):                                       # collegamento simbolico
            S.controlla_ancora(collegamento, repo)
        with self.assertRaises(ValueError):                                       # registro fuori dal repository
            S.controlla_ancora(self.registro, repo)
