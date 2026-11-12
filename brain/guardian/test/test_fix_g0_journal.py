"""Test dei 5 difetti del G0 e del journal (mandato «Binario A», 12/11/2026), scritti PRIMA delle correzioni (TDD).
Uso (dalla cartella guardian/): python3 -s -B -m unittest discover -s test -v
"""
import copy
import json
import sys
import tempfile
import tomllib
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from g0 import scheda as SCH                      # noqa: E402
from g0.strumenti import Strumento, perdita_allo_stop  # noqa: E402
from g0.valori import misura                       # noqa: E402
from journal import journal as J                   # noqa: E402
from journal.indicatori import metriche_dopo_perdita, pattern_r1  # noqa: E402

ESEMPIO = Path(__file__).resolve().parent.parent / "esempi" / "situazione_esempio.toml"


def esempio():
    with open(ESEMPIO, "rb") as f:
        return tomllib.load(f)


class TestFix1StressMargineTotale(unittest.TestCase):
    def test_avviso_se_lo_stress_viola_il_limite_totale(self):
        """Conto 2-Step a 91.500: limite giornaliero 86.500 (margine 5.000), limite totale 90.000 (margine 1.500).
        Posizione aperta EURUSD 1,5 lotti dal prezzo attuale 1,08400 allo stop 1,08300 = 150 USD + 10,50 → ma con 15
        lotti = 1.510,50 USD: il giornaliero regge, il totale no. Serve l'avviso sul limite totale."""
        d = esempio()
        d["conto"].update(saldo_mezzanotte="91500", equity="91500")
        d["posizione"][0]["quantita"] = "15"
        d.pop("trade_previsto")
        testo = "\n".join(SCH.scheda(d))
        self.assertIn("margine totale dopo lo scenario", testo)
        self.assertIn("Nello scenario di stress il limite totale viene violato.", testo)
        self.assertNotIn("Nello scenario di stress il limite giornaliero viene violato.", testo)


class TestFix2MetadatiFutures(unittest.TestCase):
    def test_future_senza_dimensione_contratto_fittizia(self):
        """Un future si descrive con passo e valore del tick: nessuna dimensione del contratto «1» inventata."""
        es = Strumento("ES", "future", "USD", None, "specifica CME (test)", "V",
                       passo_tick=D("0.25"), valore_tick=D("12.50"))
        p = perdita_allo_stop(es, misura("5000.00", "prezzo", "t"), misura("4990.00", "prezzo", "t"),
                              misura("2", "contratti", "t"), "USD")
        self.assertEqual(p.valore, D(1000))
        dati = {"strumento": [{"simbolo": "ES", "classe": "future", "valuta_profitto": "USD", "passo_tick": "0.25",
                               "valore_tick": "12.50", "fonte": "t", "stato_verifica": "C"}]}
        self.assertIsNone(SCH._strumenti(dati)["ES"].dimensione_contratto)
        with self.assertRaises(ValueError):                    # FX senza dimensione del contratto: errore esplicito
            Strumento("EURUSD", "fx", "USD", None, "t", valuta_base="EUR")


class TestFix3RegolePersonali(unittest.TestCase):
    def test_regola_confermata_applicata_e_non_confermate_dichiarate(self):
        """Con P-01 confermata a 0,5% del capitale, il trade previsto dell'esempio (682 USD su 100.000 = 0,682%)
        deve produrre un avviso P-01. Senza conferme la scheda lo dichiara, senza stringhe fisse."""
        with open(SCH.FILE_REGOLE_PERSONALI, "rb") as f:
            regole = tomllib.load(f)
        nessuna = "\n".join(SCH.scheda(esempio(), regole_personali=regole))
        self.assertIn("0 regole personali confermate su 15", nessuna)
        conf = copy.deepcopy(regole)
        p01 = next(r for r in conf["regola"] if r["id"] == "P-01")
        p01.update(confermata=True, valore="0.005")
        testo = "\n".join(SCH.scheda(esempio(), regole_personali=conf))
        self.assertIn("1 regole personali confermate su 15", testo)
        self.assertIn("P-01", testo.split("AVVISI")[1])


class TestFix4AncoraEsterna(unittest.TestCase):
    def test_ancora_rileva_ultima_riga_troncamento_e_riscrittura(self):
        T = {"simbolo": "EURUSD", "direzione": "long", "aperto_utc": "2026-11-12T09:00:00Z", "ingresso": "1.085",
             "stop": "1.083", "quantita": "1", "fonte": "t"}

        def nuovo():
            d = Path(tempfile.mkdtemp())
            for q in ("1", "2", "3"):
                J.aggiungi("trade", dict(T, quantita=q), d)
            return d, d / "trade.jsonl"

        d, f = nuovo()
        self.assertTrue((d / "ancora_integrita.json").exists())
        self.assertEqual(J.verifica(d), [])
        r = f.read_text().splitlines()
        r[2] = r[2].replace('"quantita":"3"', '"quantita":"9"')            # ultima riga modificata
        f.write_text("\n".join(r) + "\n")
        self.assertTrue(J.verifica(d))

        d, f = nuovo()
        f.write_text("\n".join(f.read_text().splitlines()[:2]) + "\n")      # coda troncata
        self.assertTrue(J.verifica(d))

        d, f = nuovo()
        recs = [json.loads(x) for x in f.read_text().splitlines()]
        recs[0]["dati"]["quantita"] = "9"
        prec, out = J.GENESI, []
        for rec in recs:                                                    # riscrittura coerente della catena
            rec["prec_hash"] = prec
            s = J._canonico(rec)
            out.append(s)
            prec = J._sha(s)
        f.write_text("\n".join(out) + "\n")
        self.assertTrue(J.verifica(d))


class TestFix5IndicatoriDecimal(unittest.TestCase):
    def test_decimal_e_frazioni_di_secondo(self):
        base = {"simbolo": "EURUSD", "direzione": "long", "ingresso": "1.085", "stop": "1.083", "fonte": "t"}
        t1 = dict(base, aperto_utc="2026-11-12T09:00:00Z", chiuso_utc="2026-11-12T09:30:00Z", quantita="0.1",
                  pnl_conto="-20.10")
        t2 = dict(base, aperto_utc="2026-11-12T09:33:00.120Z", chiuso_utc="2026-11-12T10:00:00.5Z", quantita="0.3",
                  pnl_conto="15")
        m = metriche_dopo_perdita([t1, t2])
        self.assertIsInstance(m[0]["minuti_dopo_perdita"], D)
        self.assertEqual(m[0]["minuti_dopo_perdita"], D("3.002"))          # 180,12 s
        self.assertEqual(m[0]["rapporto_size"], D("3"))                    # 0,3 / 0,1 (in float: 2,9999…)
        r = pattern_r1([t1, t2], minuti_max=D("5"), rapporto_min=D("2"))
        self.assertEqual(len(r["casi"]), 1)



# ---------------------------------------------------------------------------------------------------------------
# Contro-audit del 12/11/2026: 7 rilievi bloccanti prima del merge (test scritti PRIMA delle correzioni)
# ---------------------------------------------------------------------------------------------------------------

def regole_con(**conferme):
    """Regole personali del file con alcune regole confermate: conferme = {"P-05": "0.004", ...}."""
    with open(SCH.FILE_REGOLE_PERSONALI, "rb") as f:
        regole = tomllib.load(f)
    for r in regole["regola"]:
        if r["id"].replace("-", "_") in conferme:
            r.update(confermata=True, valore=conferme[r["id"].replace("-", "_")])
    return regole


class TestAudit1P05RegolaAurea(unittest.TestCase):
    def test_p05_non_piu_stretto_della_prop_e_avvisi_non_soppressi(self):
        d = esempio()
        d["conto"]["prodotto"] = "ftmo_1step"                                  # limite giornaliero della prop: 3%
        testo = "\n".join(SCH.scheda(d, regole_personali=regole_con(P_05="0.04")))
        self.assertIn("non è più stretto del limite della prop firm", testo)
        # P-05 a 0,4%: limite personale = 100.400 − 400 = 100.000; margine = 150. Trade 682 e stress 842,50 lo superano:
        # devono comparire ENTRAMBI gli avvisi.
        testo = "\n".join(SCH.scheda(esempio(), regole_personali=regole_con(P_05="0.004")))
        self.assertIn("P-05: se lo stop del trade previsto viene colpito", testo)
        self.assertIn("P-05: nello scenario di stress", testo)


class TestAudit2P01SecondaParte(unittest.TestCase):
    def test_p01_size_maggiore_dopo_perdita(self):
        d = esempio()                                                          # trade previsto: 2 lotti
        testo = "\n".join(SCH.scheda(d, regole_personali=regole_con(P_01="0.01")))
        self.assertIn("P-01 (seconda parte) non verificata", testo)
        d["sessione"] = {"ultima_operazione_in_perdita": True, "size_precedente": "1"}
        testo = "\n".join(SCH.scheda(d, regole_personali=regole_con(P_01="0.01")))
        self.assertIn("P-01: size maggiore della precedente dopo una perdita", testo.split("AVVISI")[1])


class TestAudit3ValidazioneJournal(unittest.TestCase):
    def test_numeri_e_orari_validati_all_ingresso(self):
        T = {"simbolo": "EURUSD", "direzione": "long", "aperto_utc": "2026-11-12T09:00:00Z", "ingresso": "1.085",
             "stop": "1.083", "quantita": "1", "fonte": "t"}
        J.valida("trade", T)                                                   # record valido: nessun errore
        for campo, valore in (("aperto_utc", "ieri"), ("aperto_utc", "2026-11-12T09:00:00"), ("quantita", "0"),
                              ("quantita", "abc"), ("ingresso", "-1"), ("stop", "NaN"), ("pnl_conto", "Infinity"),
                              ("chiuso_utc", "2026-11-12T08:59:59Z")):
            with self.assertRaises(ValueError, msg=f"{campo}={valore}"):
                J.valida("trade", dict(T, **{campo: valore}))
        with self.assertRaises(ValueError):
            J.valida("previsione", {"autore": "claude", "evento": "x", "scadenza_utc": "domani",
                                    "probabilita": 0.5, "fonte": "t"})


class TestAudit4BrierCorrezioni(unittest.TestCase):
    def test_brier_applica_le_correzioni(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            base = {"autore": "claude", "evento": "A", "scadenza_utc": "2026-12-01T00:00:00Z", "fonte": "t"}
            a = J.aggiungi("previsione", dict(base, probabilita=0.8), d)
            J.aggiungi("previsione", dict(base, probabilita=0.6, corregge=a["id"]), d)       # previsione corretta
            e = J.aggiungi("previsione", {"autore": "utente", "fonte": "t", "chiude": a["id"], "esito": 1}, d)
            self.assertAlmostEqual(J.brier(d)["claude"]["brier"], (0.6 - 1) ** 2)
            self.assertEqual(J.brier(d)["claude"]["n"], 1)
            J.aggiungi("previsione", {"autore": "utente", "fonte": "t", "chiude": a["id"], "esito": 0,
                                      "corregge": e["id"]}, d)                                # esito corretto
            self.assertAlmostEqual(J.brier(d)["claude"]["brier"], (0.6 - 0) ** 2)
            self.assertEqual(J.brier(d)["claude"]["n"], 1)


class TestAudit5ImprontaEsterna(unittest.TestCase):
    def test_verifica_con_impronta_rileva_cancellazione_totale(self):
        T = {"simbolo": "EURUSD", "direzione": "long", "aperto_utc": "2026-11-12T09:00:00Z", "ingresso": "1.085",
             "stop": "1.083", "quantita": "1", "fonte": "t"}
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            J.aggiungi("trade", T, d)
            imp = J.impronta_ancora(d)
            self.assertEqual(J.verifica(d, impronta_attesa=imp), [])
            self.assertTrue(J.verifica(d, impronta_attesa="0" * 64))                         # impronta diversa
            for f in d.iterdir():
                f.unlink()                                                                   # dati e ancora cancellati
            self.assertEqual(J.verifica(d), [])                                              # senza impronta: invisibile
            self.assertTrue(J.verifica(d, impronta_attesa=imp))                              # con impronta: rilevato


class TestAudit6Positivita(unittest.TestCase):
    def test_valori_non_positivi_rifiutati(self):
        from g0 import limiti as L
        t = "t"
        fx = Strumento("EURUSD", "fx", "USD", D(100000), t, valuta_base="EUR")
        jp = Strumento("USDJPY", "fx", "JPY", D(100000), t, valuta_base="USD")
        m = lambda x, u="prezzo": misura(x, u, t)
        casi = [
            lambda: L.limite_giornaliero("ftmo_2step", m("0", "USD"), m("0", "USD")),
            lambda: perdita_allo_stop(fx, m("1.085"), m("1.083"), m("0", "lotti"), "USD"),
            lambda: perdita_allo_stop(fx, m("1.085"), m("1.085"), m("1", "lotti"), "USD"),
            lambda: perdita_allo_stop(fx, m("-1.085"), m("1.083"), m("1", "lotti"), "USD"),
            lambda: perdita_allo_stop(fx, m("1.085"), m("0"), m("1", "lotti"), "USD"),
            lambda: perdita_allo_stop(jp, m("150"), m("149.5"), m("1", "lotti"), "EUR", cambio=misura("0", "JPY/EUR", t)),
            lambda: Strumento("ES", "future", "USD", None, t, passo_tick=D("0"), valore_tick=D("12.5")),
            lambda: Strumento("ES", "future", "USD", None, t, passo_tick=D("0.25"), valore_tick=D("-12.5")),
            lambda: Strumento("EURUSD", "fx", "USD", D(0), t, valuta_base="EUR"),
        ]
        for i, caso in enumerate(casi):
            with self.assertRaises(ValueError, msg=f"caso {i}"):
                caso()


class TestAudit7Continuita(unittest.TestCase):
    def test_documenti_di_continuita_allineati(self):
        brain = Path(__file__).resolve().parent.parent.parent
        self.assertIn("trading-brain-core", (brain / "CONTINUITA.md").read_text(encoding="utf-8"))
        self.assertIn("feat/fix-g0-journal", (brain / "governance" / "REGISTRO-MODIFICHE.md").read_text(encoding="utf-8"))
        aperte = (brain / "governance" / "DECISIONI-APERTE.md").read_text(encoding="utf-8")
        self.assertIn("trading-brain-core", aperte.split("### DA-01")[1].split("### DA-02")[0])


if __name__ == "__main__":
    unittest.main()


# ---------------------------------------------------------------------------------------------------------------
# Mandato notturno del 12/11/2026: 4 difetti residui in 357e48d, più 1 trovato in auto-audit (test scritti PRIMA)
# ---------------------------------------------------------------------------------------------------------------

def _avvisi(testo):
    return testo.split("\nAVVISI\n")[1].split("\nREGOLE PERSONALI\n")[0]


class TestNotte1Commissioni(unittest.TestCase):
    def test_commissioni_negative_o_non_finite_rifiutate(self):
        """Commissioni negative (segno invertito in un export) o non finite RIDURREBBERO la perdita allo stop."""
        fx = Strumento("EURUSD", "fx", "USD", D(100000), "t", valuta_base="EUR")
        m = lambda x, u="prezzo": misura(x, u, "t")
        base = perdita_allo_stop(fx, m("1.085"), m("1.083"), m("1", "lotti"), "USD")
        self.assertEqual(base.valore, D("200"))
        self.assertEqual(perdita_allo_stop(fx, m("1.085"), m("1.083"), m("1", "lotti"), "USD",
                                           commissioni=m("0", "USD")).valore, D("200"))     # spread-only: ammesso
        self.assertEqual(perdita_allo_stop(fx, m("1.085"), m("1.083"), m("1", "lotti"), "USD",
                                           commissioni=m("7", "USD")).valore, D("207"))
        for c in ("-200", "-0.01", "NaN", "Infinity", "-Infinity"):
            with self.assertRaises(ValueError, msg=f"commissioni={c}"):
                perdita_allo_stop(fx, m("1.085"), m("1.083"), m("1", "lotti"), "USD", commissioni=m(c, "USD"))


class TestNotte2P05MarginePersonaleNegativo(unittest.TestCase):
    def test_avvisi_trade_e_stress_anche_a_limite_personale_superato(self):
        """P-05 a 0,4%: limite personale = 100.400 − 400 = 100.000. Equity 99.900 → margine personale −100 (limite
        personale superato, FTMO no: limite 95.400). Trade 682 e stress 842,50 vanno segnalati comunque."""
        d = esempio()
        d["conto"]["equity"] = "99900"
        avvisi = _avvisi("\n".join(SCH.scheda(d, regole_personali=regole_con(P_05="0.004"))))
        self.assertIn("P-05: limite personale giornaliero già superato", avvisi)
        self.assertIn("P-05: se lo stop del trade previsto viene colpito", avvisi)
        self.assertIn("P-05: nello scenario di stress", avvisi)


class TestNotte3SemanticaJournal(unittest.TestCase):
    def test_corregge_e_chiude_coerenti_e_nessuna_doppia_chiusura(self):
        base = {"autore": "claude", "evento": "A", "scadenza_utc": "2026-12-01T00:00:00Z", "fonte": "t"}
        esito = lambda pid, x, **k: dict({"autore": "utente", "fonte": "t", "chiude": pid, "esito": x}, **k)
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            a = J.aggiungi("previsione", dict(base, probabilita=0.8), d)["id"]
            a2 = J.aggiungi("previsione", dict(base, probabilita=0.7, corregge=a), d)["id"]   # correzione valida
            b = J.aggiungi("previsione", dict(base, evento="B", probabilita=0.3), d)["id"]
            e = J.aggiungi("previsione", esito(a, 1), d)["id"]
            casi = {
                "(a) esito che corregge una previsione": esito(b, 1, corregge=a),
                "(a) previsione che corregge un esito": dict(base, probabilita=0.5, corregge=e),
                "(b) chiude punta a un esito": esito(e, 1),
                "(b) chiude punta a una correzione, non alla radice": esito(a2, 0),
                "(c) secondo esito senza corregge sulla stessa previsione": esito(a, 0),
                "(c) correzione di esito che sposta la chiusura su un'altra previsione": esito(b, 0, corregge=e),
            }
            for nome, dati in casi.items():
                with self.assertRaises(ValueError, msg=nome):
                    J.aggiungi("previsione", dati, d)
            J.aggiungi("previsione", esito(a, 0, corregge=e), d)                              # correzione valida
            J.aggiungi("previsione", esito(b, 1), d)                                          # chiusura valida
            self.assertEqual(J.verifica(d), [])
            # Un file scritto a mano (catena di hash ricostruita) con una doppia chiusura: verifica() la segnala.
            path = d / "previsione.jsonl"
            righe = J._righe(path)
            rec = {"schema": J.SCHEMA, "registro": "previsione", "id": f"PRE-{len(righe) + 1:05d}",
                   "registrato_utc": "2026-11-12T22:00:00Z", "prec_hash": J._sha(righe[-1]), "dati": esito(a, 1)}
            with open(path, "a", encoding="utf-8") as f:
                f.write(J._canonico(rec) + "\n")
            self.assertTrue(any("già chiusa" in p for p in J.verifica(d)), J.verifica(d))


class TestNotte4DatiSessione(unittest.TestCase):
    def test_dati_di_sessione_e_soglie_non_validi(self):
        """Booleani, negativi, NaN, infiniti e ore di sonno oltre 24: dato non valido, mai «regola rispettata» o crash."""
        casi = [("P_14", "6", "ore_sonno", True), ("P_14", "6", "ore_sonno", "25"), ("P_14", "6", "ore_sonno", "-1"),
                ("P_11", "15", "minuti_da_ultima_perdita", "-5"), ("P_11", "15", "minuti_da_ultima_perdita", "NaN"),
                ("P_15", "3", "perdite_consecutive_oggi", "-1"), ("P_15", "3", "perdite_consecutive_oggi", "1.5"),
                ("P_15", "3", "perdite_consecutive_oggi", "Infinity")]
        for rid, soglia, chiave, x in casi:
            d = esempio()
            d["sessione"] = {chiave: x}
            avvisi = _avvisi("\n".join(SCH.scheda(d, regole_personali=regole_con(**{rid: soglia}))))
            self.assertIn(f"{rid.replace('_', '-')}: dato «sessione.{chiave}» non valido", avvisi, f"{chiave}={x!r}")
        for rid, soglia in (("P_14", "NaN"), ("P_11", "-15"), ("P_15", "Infinity"), ("P_01", "NaN"), ("P_05", "0")):
            d = esempio()
            d["sessione"] = {"ore_sonno": "8", "minuti_da_ultima_perdita": "30", "perdite_consecutive_oggi": "0"}
            avvisi = _avvisi("\n".join(SCH.scheda(d, regole_personali=regole_con(**{rid: soglia}))))
            self.assertIn(f"{rid.replace('_', '-')}: regola confermata senza valore numerico valido", avvisi, soglia)


class TestNotte5BooleaniJournal(unittest.TestCase):
    def test_booleani_rifiutati_come_numeri(self):
        """In Python True == 1: senza controllo, `probabilita: true`, `esito: true` e `aderenza: true` passerebbero."""
        P = {"autore": "claude", "evento": "x", "scadenza_utc": "2026-12-01T00:00:00Z", "fonte": "t"}
        T = {"simbolo": "EURUSD", "direzione": "long", "aperto_utc": "2026-11-12T09:00:00Z", "ingresso": "1.085",
             "stop": "1.083", "quantita": "1", "fonte": "t"}
        for registro, dati in (("previsione", dict(P, probabilita=True)), ("previsione", dict(P, probabilita=False)),
                               ("previsione", {"autore": "u", "fonte": "t", "chiude": "PRE-00001", "esito": True}),
                               ("trade", dict(T, aderenza=True)), ("trade", dict(T, quantita=True))):
            with self.assertRaises(ValueError, msg=str(dati)):
                J.valida(registro, dati)
        J.valida("previsione", dict(P, probabilita=1))                          # interi 0 e 1 restano ammessi
        J.valida("previsione", {"autore": "u", "fonte": "t", "chiude": "PRE-00001", "esito": 0})
