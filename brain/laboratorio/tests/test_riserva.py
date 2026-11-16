"""Test del registro della riserva di verifica (laboratorio/esecuzione/riserva.py), scritti PRIMA del codice.
Richiesta 3 a Claude di DGS-20261114-04: su dati inventati, due richieste simultanee o sovrapposte ricevono al massimo
un'autorizzazione per lo stesso perimetro; un'interruzione dopo l'apertura conserva j e quota; il rapporto distingue
prenotazione, consumo, quarantena e rendicontazione. Nessun dato di prezzo: il registro conosce solo date.
Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_riserva
"""
import json
import sys
import tempfile
import threading
import unittest
from datetime import date
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.laboratorio.esecuzione import riserva as RV            # noqa: E402

ORA = "2026-11-16T01:00:00Z"
D = date


class Base(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.reg = Path(self._t.name) / "riserva.json"
        RV.crea(self.reg, D(2005, 1, 1), D(2005, 12, 31), 0.05, ORA, protetta=(D(2005, 11, 1), D(2005, 12, 31)))

    def tearDown(self):
        self._t.cleanup()

    def prenota(self, id_, a, b, **k):
        return RV.prenota(self.reg, id_, "H-900", a, b, "domanda-" + id_, ORA, **k)


class TestCreazione(Base):
    def test_una_sola_volta_e_parametri_validi(self):
        with self.assertRaises(ValueError):
            RV.crea(self.reg, D(2005, 1, 1), D(2005, 12, 31), 0.05, ORA)
        altro = Path(self._t.name) / "altro.json"
        for args in ((D(2005, 1, 2), D(2005, 1, 1), 0.05), (D(2005, 1, 1), D(2005, 2, 1), 0.0),
                     (D(2005, 1, 1), D(2005, 2, 1), 1.0)):
            with self.assertRaises(ValueError):
                RV.crea(altro, *args, ORA)
        self.assertFalse(altro.exists())
        s = RV.stato(self.reg)
        self.assertEqual(s["giorni"], {"disponibile": 365, "prenotato": 0, "consumato": 0, "quarantena": 0})
        self.assertEqual(s["giorni_protetti"], 61)


class TestPrenotazione(Base):
    def test_perimetro_e_sovrapposizioni(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 3, 31))
        with self.assertRaises(ValueError):                            # sovrapposta (anche un «alias» con altro nome)
            RV.prenota(self.reg, "B", "H-901-alias", D(2005, 3, 31), D(2005, 4, 30), "x", ORA)
        with self.assertRaises(ValueError):                            # fuori dalla riserva, prima
            self.prenota("C", D(2004, 12, 31), D(2005, 1, 5))
        with self.assertRaises(ValueError):                            # fuori dalla riserva, dopo
            self.prenota("C2", D(2005, 10, 30), D(2006, 1, 2), usa_protetta=True)
        with self.assertRaises(ValueError):                            # identità già usata
            self.prenota("A", D(2005, 5, 1), D(2005, 5, 2))
        with self.assertRaises(ValueError):                            # intervallo rovesciato
            self.prenota("D", D(2005, 5, 2), D(2005, 5, 1))
        self.assertEqual(RV.stato(self.reg)["giorni"]["prenotato"], 90)

    def test_parte_protetta_solo_con_sblocco_esplicito(self):
        with self.assertRaises(ValueError):
            self.prenota("P", D(2005, 10, 25), D(2005, 11, 5))
        e = self.prenota("P", D(2005, 10, 25), D(2005, 11, 5), usa_protetta=True)
        self.assertTrue(e["usa_protetta"])

    def test_quarantena_blocca_e_si_mette_solo_su_giorni_liberi(self):
        RV.quarantena(self.reg, D(2005, 6, 1), D(2005, 6, 10), "buchi nei dati", ORA)
        with self.assertRaises(ValueError):
            self.prenota("Q", D(2005, 6, 5), D(2005, 6, 20))
        self.prenota("R", D(2005, 7, 1), D(2005, 7, 10))
        with self.assertRaises(ValueError):
            RV.quarantena(self.reg, D(2005, 7, 5), D(2005, 7, 6), "x", ORA)
        self.assertEqual(RV.stato(self.reg)["giorni"]["quarantena"], 10)

    def test_rilascio_solo_prima_dell_autorizzazione(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        RV.rilascia(self.reg, "A", ORA)
        self.assertEqual(RV.stato(self.reg)["giorni"]["prenotato"], 0)
        with self.assertRaises(ValueError):
            RV.autorizza(self.reg, "A", 12, "dati", ORA)              # rilasciata: niente autorizzazione
        self.prenota("B", D(2005, 1, 1), D(2005, 1, 31))               # le date tornano libere
        RV.autorizza(self.reg, "B", 12, "dati", ORA)
        with self.assertRaises(ValueError):
            RV.rilascia(self.reg, "B", ORA)
        with self.assertRaises(ValueError):
            RV.rilascia(self.reg, "ignota", ORA)


class TestAutorizzazione(Base):
    def test_contatore_e_quota(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        self.prenota("B", D(2005, 2, 1), D(2005, 2, 28))
        a = RV.autorizza(self.reg, "A", 12, "dati-A", ORA)
        b = RV.autorizza(self.reg, "B", 14, "dati-B", ORA, m=2)
        self.assertEqual((a["j"], b["j"]), (1, 2))
        self.assertAlmostEqual(a["alfa_j"], 0.05 / 2, places=15)
        self.assertAlmostEqual(b["alfa_j"], 0.05 / 6 / 2, places=15)  # α_tot / [j(j+1)] / m
        self.assertEqual((a["n_globale"], b["n_globale"]), (12, 14))
        s = RV.stato(self.reg)
        self.assertEqual(s["giorni"]["consumato"], 59)
        self.assertAlmostEqual(s["alfa_speso"], 0.05 / 2 + 0.05 / 6, places=15)   # quota della famiglia, non /m
        with self.assertRaises(ValueError):
            RV.autorizza(self.reg, "ignota", 1, "x", ORA)
        self.prenota("C", D(2005, 3, 1), D(2005, 3, 5))
        with self.assertRaises(ValueError):
            RV.autorizza(self.reg, "C", 12, "dati-C", ORA, m=0)

    def test_ripetizione_tecnica_stessa_identita_stessi_byte(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        a1 = RV.autorizza(self.reg, "A", 12, "dati-A", ORA)
        a2 = RV.autorizza(self.reg, "A", 12, "dati-A", ORA)            # stesso tentativo: nessun nuovo j
        self.assertEqual(a1, a2)
        self.assertEqual(len(RV.stato(self.reg)["aperture"]), 1)
        with self.assertRaises(ValueError):
            RV.autorizza(self.reg, "A", 12, "dati-DIVERSI", ORA)        # byte diversi: non è una ripetizione
        with self.assertRaises(ValueError):
            RV.autorizza(self.reg, "A", 13, "dati-A", ORA)              # N diverso: non è una ripetizione

    def test_interruzione_dopo_l_apertura_conserva_consumo_e_quota(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        RV.autorizza(self.reg, "A", 12, "dati-A", ORA)
        # «crash»: nessun esito registrato; si rilegge da disco
        s = RV.stato(self.reg)
        self.assertEqual(s["aperture"][0]["esito"], None)
        self.assertEqual(s["giorni"]["consumato"], 31)
        with self.assertRaises(ValueError):                            # le date non tornano disponibili
            self.prenota("A2", D(2005, 1, 15), D(2005, 1, 20))
        self.prenota("B", D(2005, 2, 1), D(2005, 2, 5))
        self.assertEqual(RV.autorizza(self.reg, "B", 12, "dati-B", ORA)["j"], 2)   # j continua

    def test_esito_negativo_o_non_decidibile_non_restituisce_nulla(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        RV.autorizza(self.reg, "A", 12, "dati-A", ORA)
        RV.rendiconta(self.reg, "A", "non decidibile", ORA)
        s = RV.stato(self.reg)
        self.assertEqual(s["aperture"][0]["esito"], "non decidibile")
        self.assertEqual(s["giorni"]["consumato"], 31)
        with self.assertRaises(ValueError):
            RV.rendiconta(self.reg, "A", "promossa", ORA)              # un solo esito
        self.prenota("B", D(2005, 2, 1), D(2005, 2, 5))
        with self.assertRaises(ValueError):
            RV.rendiconta(self.reg, "B", "bocciata", ORA)              # non autorizzata
        RV.autorizza(self.reg, "B", 12, "dati-B", ORA)
        with self.assertRaises(ValueError):
            RV.rendiconta(self.reg, "B", "forse", ORA)


class TestConcorrenza(Base):
    def test_richieste_simultanee_sullo_stesso_perimetro(self):
        esiti, barriera = [], threading.Barrier(8)

        def prova(k):
            barriera.wait()
            try:
                RV.prenota(self.reg, f"T{k}", f"H-9{k}", D(2005, 3, 1 + k), D(2005, 3, 20 + k), "d", ORA)
                RV.autorizza(self.reg, f"T{k}", 10, "dati", ORA)
                esiti.append(k)
            except ValueError:
                pass
        fili = [threading.Thread(target=prova, args=(k,)) for k in range(8)]
        for f in fili:
            f.start()
        for f in fili:
            f.join()
        self.assertEqual(len(esiti), 1)
        self.assertEqual(len(RV.stato(self.reg)["aperture"]), 1)


class TestNessunaScritturaPersa(Base):
    def test_prenotazioni_simultanee_su_date_diverse_tutte_registrate(self):
        barriera = threading.Barrier(16)

        def prova(k):
            barriera.wait()
            RV.prenota(self.reg, f"T{k}", "H-900", D(2005, 1, 1) + (D(2005, 1, 11) - D(2005, 1, 1)) * k,
                       D(2005, 1, 5) + (D(2005, 1, 11) - D(2005, 1, 1)) * k, "d", ORA)
        fili = [threading.Thread(target=prova, args=(k,)) for k in range(16)]
        for f in fili:
            f.start()
        for f in fili:
            f.join()
        self.assertEqual(len(RV.stato(self.reg)["prenotazioni_attive"]), 16)


class TestIntegrita(Base):
    def test_registro_manomesso_rifiutato(self):
        dati = json.loads(self.reg.read_text())
        dati["eventi"].append({"tipo": "regalo", "id": "X", "ora": ORA})
        self.reg.write_text(json.dumps(dati))
        with self.assertRaises(ValueError):
            RV.stato(self.reg)

    def test_evento_sconosciuto_anche_se_ha_l_aspetto_di_un_esito(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        RV.autorizza(self.reg, "A", 12, "dati-A", ORA)
        dati = json.loads(self.reg.read_text())
        dati["eventi"].append({"tipo": "regalo", "id": "A", "esito": "promossa", "ora": ORA})
        self.reg.write_text(json.dumps(dati))
        with self.assertRaises(ValueError):
            RV.stato(self.reg)

    def test_autorizzazione_senza_prenotazione_nel_file_rifiutata(self):
        dati = json.loads(self.reg.read_text())
        dati["eventi"].append({"tipo": "autorizzazione", "id": "X", "j": 1, "n_globale": 1, "hash_dati": "d",
                               "m": 1, "alfa_j": 0.025, "ora": ORA})
        self.reg.write_text(json.dumps(dati))
        with self.assertRaises(ValueError):
            RV.stato(self.reg)

    def test_j_o_quota_falsificati_rifiutati(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        RV.autorizza(self.reg, "A", 12, "dati-A", ORA)
        for campo, valore in (("j", 5), ("alfa_j", 0.05)):
            dati = json.loads(self.reg.read_text())
            originale = dati["eventi"][-1][campo]
            dati["eventi"][-1][campo] = valore
            self.reg.write_text(json.dumps(dati))
            with self.assertRaises(ValueError, msg=campo):
                RV.stato(self.reg)
            dati["eventi"][-1][campo] = originale
            self.reg.write_text(json.dumps(dati))
        RV.stato(self.reg)


if __name__ == "__main__":
    unittest.main()
