"""Test del rendiconto del protocollo DGS-07 (adottato dal titolare, D-25), scritti PRIMA del codice (17/11/2026).
Solo numeri inventati: nessun risultato del pilota è usato qui. I valori di riferimento numerici sono quelli
ricalcolati in modo indipendente dal DGS in DGS-07 (§2a.5, §2a.6, §2a.7, §2b).
Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_protocollo_ia02
"""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.laboratorio.studi import pilota_ia02 as P            # noqa: E402
from brain.laboratorio.studi import protocollo_ia02 as R        # noqa: E402

PRO, BOC, ATT = [0.3, 0.4], [0.0, 0.05], [0.1, 0.2]          # promossa, bocciata, attraversa a ogni margine


def lista(pro=0, boc=0, err=0, att=0, extra=()):
    return [PRO] * pro + [BOC] * boc + [None] * err + [ATT] * att + [list(x) for x in extra]


def dati_finti(M, per_metodo, fase=1, metodi=("hac", "bootstrap")):
    """per_metodo[metodo][cella] = lista di intervalli; le celle non indicate sono tutte «attraversa» tranne le
    celle di potenza, che hanno una promozione."""
    celle = {}
    for c in range(1, 13):
        celle[str(c)] = {}
        for m in metodi:
            v = per_metodo.get(m, {}).get(c)
            if v is None:
                v = lista(pro=1, att=M - 1) if c in R.CELLE_POTENZA else lista(att=M)
            celle[str(c)][m] = v
    return {"versione": "prova", "fase": fase, "repliche": M, "ricampionamenti": 3999, "master": P.MASTER,
            "celle": celle}


class TestClopperPearsonUnilaterale(unittest.TestCase):
    def test_valori_del_dgs(self):
        self.assertAlmostEqual(R.ucp(60, 3000, 0.05), 0.0247368843, places=9)
        self.assertAlmostEqual(R.ucp(61, 3000, 0.05), 0.0251039129, places=9)
        self.assertAlmostEqual(R.ucp(248, 12000, 0.001), 0.0249969661, places=9)
        self.assertAlmostEqual(R.ucp(249, 12000, 0.001), 0.0250881441, places=9)

    def test_estremi(self):
        self.assertAlmostEqual(R.ucp(0, 3000, 0.05), 1 - 0.05 ** (1 / 3000), places=12)
        self.assertEqual(R.ucp(50, 50, 0.05), 1.0)

    def test_soglie_intere(self):
        self.assertEqual(R.k_massimo(3000, 0.05), 60)
        self.assertEqual(R.k_massimo(12000, 0.001), 248)
        self.assertEqual(R.k_massimo(10, 0.05), -1)                       # nemmeno k = 0 basta

    def test_probabilita_di_passare_del_dgs(self):
        self.assertAlmostEqual(R.prob_passare(0.02, 12000, 248), 0.712758, places=6)
        self.assertAlmostEqual(R.prob_passare(1 / 60, 12000, 248), 0.999588, places=6)
        self.assertAlmostEqual(R.prob_passare(0.025, 12000, 248), 0.000993062, places=9)


class TestConteggi(unittest.TestCase):
    def test_margini_e_uguaglianze(self):
        v = [None, [0.16, 0.3], [0.1600001, 0.3], [0.0, 0.14], [0.0, 0.1399999], [0.0, 0.15], [0.1500001, 0.2]]
        self.assertEqual(R.conta(v, 0.0), {"E": 1, "P": 3, "B": 2, "I": 1})
        self.assertEqual(R.conta(v, 0.01), {"E": 1, "P": 1, "B": 1, "I": 4})
        self.assertEqual(R.conta(v, 0.05), {"E": 1, "P": 0, "B": 0, "I": 6})
        self.assertEqual(R.MARGINI, (0.0, 0.01, 0.025, 0.05))

    def test_esempi_del_dgs(self):
        """P = 59 ed E = 2 danno k = 61 e non passano la fase 1; P = 247 ed E = 1 passano un controllo della fase 2;
        P = 248 ed E = 1 no."""
        v1 = R.valuta(dati_finti(3000, {"hac": {2: lista(pro=59, err=2, att=2939)}}), 1)
        c = v1[("hac", 0.0)]
        self.assertEqual(c["celle"][2], {"M": 3000, "E": 2, "P": 59, "B": 0, "I": 2939, "kp": 61, "km": 2})
        self.assertFalse(c["ammissibile"])
        self.assertIn(("falsa promozione", 2, 61, False), [(x[0], x[1], x[2], x[4]) for x in c["controlli"]])
        for p, atteso in ((247, True), (248, False)):
            v2 = R.valuta(dati_finti(12000, {"bootstrap": {6: lista(pro=p, err=1, att=11999 - p)}},
                                     fase=2, metodi=("bootstrap",)), 2)
            ctl = [x for x in v2[("bootstrap", 0.0)]["controlli"] if x[0] == "falsa promozione" and x[1] == 6][0]
            self.assertEqual((ctl[2], ctl[4]), (p + 1, atteso))

    def test_dieci_controlli(self):
        c = R.valuta(dati_finti(100, {}), 1)[("hac", 0.0)]
        nomi = sorted((x[0], x[1]) for x in c["controlli"])
        attesi = sorted([("falsa promozione", k) for k in (1, 2, 5, 6, 9, 11)] +
                        [("falsa bocciatura", k) for k in (2, 6, 9, 11)])
        self.assertEqual(nomi, attesi)

    def test_bocciature_contano_al_confine_ma_non_sotto_soglia(self):
        v = R.valuta(dati_finti(3000, {"hac": {1: lista(boc=500, att=2500), 9: lista(boc=61, att=2939)}}), 1)
        c = v[("hac", 0.0)]
        self.assertFalse(c["ammissibile"])
        falliti = [(x[0], x[1]) for x in c["controlli"] if not x[4]]
        self.assertEqual(falliti, [("falsa bocciatura", 9)])


class TestSelezione(unittest.TestCase):
    def test_tutto_pulito_vince_hac_a_margine_zero(self):
        self.assertEqual(R.seleziona(R.valuta(dati_finti(3000, {}), 1)), ("hac", 0.0))

    def test_minimo_poi_somma_poi_margine_poi_hac(self):
        pot = lambda a, b, c, d: {3: lista(pro=a, att=3000 - a), 7: lista(pro=b, att=3000 - b),   # noqa: E731
                                  10: lista(pro=c, att=3000 - c), 12: lista(pro=d, att=3000 - d)}
        # bootstrap ha minimo maggiore: vince anche se la somma è minore
        v = R.valuta(dati_finti(3000, {"hac": pot(5, 900, 900, 900), "bootstrap": pot(6, 6, 6, 6)}), 1)
        self.assertEqual(R.seleziona(v), ("bootstrap", 0.0))
        # stesso minimo: vince la somma maggiore
        v = R.valuta(dati_finti(3000, {"hac": pot(5, 5, 5, 6), "bootstrap": pot(5, 5, 5, 9)}), 1)
        self.assertEqual(R.seleziona(v), ("bootstrap", 0.0))
        # parità completa: HAC
        v = R.valuta(dati_finti(3000, {"hac": pot(5, 5, 5, 9), "bootstrap": pot(5, 5, 5, 9)}), 1)
        self.assertEqual(R.seleziona(v), ("hac", 0.0))

    def test_margine_piu_piccolo_a_parita(self):
        """Le promozioni [0,3; 0,4] restano tali a ogni margine: a parità vince il margine più piccolo; se a margine 0
        la cella 2 fallisce (promozioni basse, 0,16) e a 0,01 no, vince 0,01."""
        quasi = lista(att=2900, extra=[[0.16, 0.3]] * 100)                 # promosse solo a margine 0
        v = R.valuta(dati_finti(3000, {"hac": {2: quasi}, "bootstrap": {2: quasi}}), 1)
        self.assertFalse(v[("hac", 0.0)]["ammissibile"])
        self.assertTrue(v[("hac", 0.01)]["ammissibile"])
        self.assertEqual(R.seleziona(v), ("hac", 0.01))

    def test_veto_della_cella_11_e_stop(self):
        v = R.valuta(dati_finti(3000, {"hac": {11: lista(pro=61, att=2939)}, "bootstrap": {11: lista(pro=61, att=2939)}}),
                     1)
        self.assertFalse(v[("hac", 0.0)]["ammissibile"])
        self.assertEqual(R.seleziona(v), None)

    def test_nessuna_promozione_in_una_cella_di_potenza(self):
        v = R.valuta(dati_finti(3000, {"hac": {12: lista(att=3000)}}), 1)
        self.assertFalse(v[("hac", 0.0)]["ammissibile"])
        self.assertEqual(R.seleziona(v), ("bootstrap", 0.0))
        self.assertEqual(v[("hac", 0.0)]["potenze"][12], 0)

    def test_corsa_incompleta_non_valutabile(self):
        d = dati_finti(3000, {})
        d["celle"]["4"]["hac"] = d["celle"]["4"]["hac"][:-1]                # una replica mancante
        del d["celle"]["8"]["bootstrap"]                                     # un metodo mancante in una cella
        v = R.valuta(d, 1)
        self.assertFalse(v[("hac", 0.0)]["completa"])
        self.assertFalse(v[("bootstrap", 0.025)]["completa"])
        self.assertEqual(R.seleziona(v), None)
        d = dati_finti(3000, {})
        del d["celle"]["12"]
        self.assertFalse(R.valuta(d, 1)[("hac", 0.0)]["completa"])

    def test_intervallo_non_valido_nel_file_rende_incompleta(self):
        for cattivo in ([0.2, 0.2], [0.3, 0.2], [0.1], "x", [float("nan"), 0.2]):
            d = dati_finti(3000, {})
            d["celle"]["5"]["hac"][7] = cattivo
            self.assertFalse(R.valuta(d, 1)[("hac", 0.0)]["completa"], cattivo)


class TestFase2(unittest.TestCase):
    def test_verdetto(self):
        v = R.valuta(dati_finti(12000, {}, fase=2, metodi=("bootstrap",)), 2)
        self.assertEqual(R.verdetto_fase2(v, ("bootstrap", 0.0), diagnostica_ok=True)[0],
                         "CONFERMATO NEL DOMINIO DEL PILOTA")
        esito, cause = R.verdetto_fase2(v, ("bootstrap", 0.0), diagnostica_ok=False)
        self.assertEqual(esito, "NON CONFERMATO")
        self.assertTrue(any("flussi" in c for c in cause))
        v = R.valuta(dati_finti(12000, {"bootstrap": {11: lista(boc=249, att=11751)}}, fase=2, metodi=("bootstrap",)), 2)
        esito, cause = R.verdetto_fase2(v, ("bootstrap", 0.0), diagnostica_ok=True)
        self.assertEqual(esito, "NON CONFERMATO")
        self.assertTrue(any("11" in c for c in cause))

    def test_fase2_con_meno_repliche_non_valutabile(self):
        v = R.valuta(dati_finti(3000, {}, fase=2, metodi=("hac",)), 2)
        esito, cause = R.verdetto_fase2(v, ("hac", 0.0), diagnostica_ok=True)
        self.assertEqual(esito, "NON CONFERMATO")
        self.assertTrue(any("12.000" in c or "12000" in c for c in cause))

    def test_candidato_assente(self):
        v = R.valuta(dati_finti(12000, {}, fase=2, metodi=("hac",)), 2)
        self.assertEqual(R.verdetto_fase2(v, ("bootstrap", 0.0), diagnostica_ok=True)[0], "NON CONFERMATO")


class TestFlussi(unittest.TestCase):
    def test_banda_dalla_formula(self):
        self.assertEqual(R.banda(10000, 0.01 / 216), (4796, 5204))
        self.assertEqual(R.BANDA, (4796, 5204))
        self.assertLessEqual(R.p_bilaterale(4795, 10000), 0.01 / 216)
        self.assertGreater(R.p_bilaterale(4796, 10000), 0.01 / 216)
        self.assertAlmostEqual(R.p_bilaterale(5000, 10000), 1.0, places=12)

    def test_216_confronti_e_un_caso_a_mano(self):
        conf = R.diagnostica_flussi()
        self.assertEqual(len(conf), 216)
        self.assertEqual(sorted({x["gruppo"] for x in conf}), ["A", "B", "C"])
        self.assertEqual([sum(1 for x in conf if x["gruppo"] == g) for g in "ABC"], [36, 72, 108])
        self.assertEqual(len({(x["cella"], x["primo"], x["secondo"], x["h"]) for x in conf}), 216)
        bit = lambda chiave: [1 if u >= 0.5 else 0 for u in (lambda r: [r.random() for _ in range(10002)])(  # noqa
            P.flusso(*chiave))]
        a, b = bit((1, 7, 1, 0)), bit((1, 7, 1, 2))
        for h in (-1, 0, 1):
            atteso = sum(1 for t in range(1, 10001) if a[t] == b[t + h])
            x = [c for c in conf if c["cella"] == 7 and c["primo"] == (1, 1, 0) and c["secondo"] == (1, 1, 2)
                 and c["h"] == h][0]
            self.assertEqual(x["X"], atteso)
            self.assertEqual(x["segnala"], not 4796 <= atteso <= 5204)
        a, b = bit((2, 3, 1, 0)), bit((2, 3, 2, 0))
        x = [c for c in conf if c["cella"] == 3 and c["primo"] == (2, 1, 0) and c["secondo"] == (2, 2, 0)
             and c["h"] == 1][0]
        self.assertEqual(x["X"], sum(1 for t in range(1, 10001) if a[t] == b[t + 1]))

    def test_inventario_dei_semi(self):
        inv = R.inventario_semi({1: 5, 2: 7})
        self.assertEqual(inv, {"chiavi": 12 * 12 * 4, "semi_distinti": 12 * 12 * 4})


class TestRigaDiComando(unittest.TestCase):
    def esegui(self, d, *altri):
        with tempfile.TemporaryDirectory() as t:
            f = os.path.join(t, "l.json")
            with open(f, "w", encoding="utf-8") as fh:
                json.dump(d, fh)
            buf = io.StringIO()
            with redirect_stdout(buf):
                codice = R.main(["--limiti", f, *altri])
        return codice, buf.getvalue()

    def test_fase1(self):
        codice, testo = self.esegui(dati_finti(3000, {}), "--fase", "1")
        self.assertEqual(codice, 0)
        self.assertIn("Candidato scelto: hac, margine 0", testo)
        self.assertIn("k ≤ 60", testo)
        _, testo = self.esegui(dati_finti(3000, {"hac": {11: lista(pro=61, att=2939)},
                                                 "bootstrap": {11: lista(pro=61, att=2939)}}), "--fase", "1")
        self.assertIn("STOP", testo)

    def test_fase2_esegue_da_sola_la_diagnostica(self):
        """La fase 2 non si fida di un'attestazione a mano: esegue inventario dei semi e 216 confronti."""
        orig = R.diagnostica_flussi
        try:
            codice, testo = self.esegui(dati_finti(12000, {}, fase=2, metodi=("hac",)), "--fase", "2",
                                        "--candidato", "hac:0.0")
            self.assertEqual(codice, 0)
            self.assertIn("Esito: CONFERMATO NEL DOMINIO DEL PILOTA", testo)
            self.assertIn("216 confronti", testo)
            R.diagnostica_flussi = lambda: [dict(c, X=4000, segnala=True) for c in orig()]
            _, testo = self.esegui(dati_finti(12000, {}, fase=2, metodi=("hac",)), "--fase", "2",
                                   "--candidato", "hac:0.0")
            self.assertIn("Esito: NON CONFERMATO", testo)
        finally:
            R.diagnostica_flussi = orig
        orig_inv = R.inventario_semi
        try:
            R.inventario_semi = lambda fasi: {"chiavi": 10, "semi_distinti": 9}
            _, testo = self.esegui(dati_finti(12000, {}, fase=2, metodi=("hac",)), "--fase", "2",
                                   "--candidato", "hac:0.0")
            self.assertIn("Esito: NON CONFERMATO", testo)
        finally:
            R.inventario_semi = orig_inv

    def test_fase_dichiarata_diversa_dal_file(self):
        codice, _ = self.esegui(dati_finti(3000, {}, fase=1), "--fase", "2", "--candidato", "hac:0.0")
        self.assertEqual(codice, 2)
        codice, _ = self.esegui(dati_finti(12000, {}, fase=2), "--fase", "1")
        self.assertEqual(codice, 2)


if __name__ == "__main__":
    unittest.main()
