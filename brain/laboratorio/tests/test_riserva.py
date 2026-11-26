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
        RV.rilascia(self.reg, "A", ORA, "titolare", "scheda non conforme")
        self.assertEqual(RV.stato(self.reg)["giorni"]["prenotato"], 0)
        with self.assertRaises(ValueError):
            RV.autorizza(self.reg, "A", 12, "dati", ORA)              # rilasciata: niente autorizzazione
        self.prenota("B", D(2005, 1, 1), D(2005, 1, 31))               # le date tornano libere
        RV.autorizza(self.reg, "B", 12, "dati", ORA)
        with self.assertRaises(ValueError):
            RV.rilascia(self.reg, "B", ORA, "titolare", "x")
        with self.assertRaises(ValueError):
            RV.rilascia(self.reg, "ignota", ORA, "titolare", "x")

    def test_rilascio_attribuito_a_chi_lo_chiede(self):                # DGS-19, caso B
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        with self.assertRaises(TypeError):
            RV.rilascia(self.reg, "A", ORA)                            # senza autore né motivo non si rilascia
        for chi, motivo in (("", "m"), ("titolare", ""), ("  ", "m"), ("titolare", None)):
            with self.assertRaisesRegex(ValueError, "rilascio"):
                RV.rilascia(self.reg, "A", ORA, chi, motivo)
        self.assertEqual(RV.prenotazione(self.reg, "A")["stato"], "prenotato")
        RV.rilascia(self.reg, "A", ORA, "titolare", "scheda non conforme")
        p = RV.prenotazione(self.reg, "A")
        self.assertEqual((p["stato"], p["rilascio"]["chi"], p["rilascio"]["motivo"]),
                         ("rilasciato", "titolare", "scheda non conforme"))
        dati = json.loads(self.reg.read_text(encoding="utf-8"))
        self.prenota("B", D(2005, 3, 1), D(2005, 3, 31))
        dati = json.loads(self.reg.read_text(encoding="utf-8"))
        dati["eventi"].append({"tipo": "rilascio", "id": "B", "ora": ORA})          # scritto a mano, senza autore
        self.reg.write_text(json.dumps(dati), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "rilascio"):
            RV.stato(self.reg)


class TestIpotesiDellaPrenotazione(Base):
    """#150: la prenotazione esige un'ipotesi testo non vuoto, senza spazi ai bordi né caratteri di controllo (la stessa
    regola del contratto H-003, #146 e), alla scrittura e alla ricostruzione di un registro manomesso."""

    def test_ipotesi_vuota_o_non_testo_rifiutata_senza_scrivere(self):
        prima = self.reg.read_bytes()
        for ip in ("", " ", " H-X", "H-X ", "H-\nX", "H-\tX", 7, None, ["H-X"], True):
            with self.subTest(ipotesi=ip):
                with self.assertRaisesRegex(ValueError, "ipotesi"):
                    RV.prenota(self.reg, "A", ip, D(2005, 1, 1), D(2005, 1, 5), "domanda-A", ORA)
                self.assertEqual(self.reg.read_bytes(), prima)
        RV.prenota(self.reg, "A", "H-X", D(2005, 1, 1), D(2005, 1, 5), "domanda-A", ORA)    # caso valido
        self.assertEqual(RV.prenotazione(self.reg, "A")["evento"]["ipotesi"], "H-X")

    def test_registro_manomesso_con_ipotesi_vuota_rifiutato(self):
        dati = json.loads(self.reg.read_text())
        dati["eventi"].append({"tipo": "prenotazione", "id": "X", "ipotesi": "", "inizio": "2005-01-01",
                               "fine": "2005-01-05", "hash_domanda": "d", "usa_protetta": False, "ora": ORA})
        self.reg.write_text(json.dumps(dati))
        with self.assertRaisesRegex(ValueError, "ipotesi"):
            RV.stato(self.reg)


class TestQuotaEsatta(unittest.TestCase):
    def test_quota_calcolata_in_frazioni_esatte(self):
        # #149 (R19-09): 0,15/(2·3)/1 vale esattamente 1/40; in virgola mobile dava 0,024999999999999998
        self.assertEqual(RV.quota(0.15, 2, 1), 0.025)
        self.assertEqual(RV.quota(0.30, 2, 2), 0.025)
        self.assertEqual(RV.quota(0.05, 1, 1), 0.025)
        self.assertEqual(RV.quota(0.05, 2, 1), 1 / 120)


class TestTentativoRifiutato(Base):
    """DGS-18 Q3 e DGS-19 (caso G): un tentativo rifiutato prima dell'autorizzazione si registra SENZA consumo,
    collegato alla prenotazione e allo snapshot dei registri; un ritentativo identico non si duplica."""
    REGISTRI = [["registro_scaricamento_XAUUSD_ASK.csv", "ab" * 32], ["registro_scaricamento_XAUUSD_BID.csv", "cd" * 32]]

    def test_registrato_senza_consumo(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        prima = RV.stato(self.reg)
        RV.tentativo(self.reg, "A", "manifesto", "omesso: XAUUSD ASK 2005-01-03", self.REGISTRI, ORA)
        dopo = RV.stato(self.reg)
        self.assertEqual((dopo["giorni"], dopo["aperture"], dopo["prenotazioni_attive"]),
                         (prima["giorni"], prima["aperture"], prima["prenotazioni_attive"]))
        p = RV.prenotazione(self.reg, "A")
        self.assertEqual(p["stato"], "prenotato")
        self.assertEqual([(t["fase"], t["motivo"], t["registri"]) for t in p["tentativi"]],
                         [("manifesto", "omesso: XAUUSD ASK 2005-01-03", self.REGISTRI)])
        RV.autorizza(self.reg, "A", 1, "h", ORA)                       # la prenotazione resta correggibile

    def test_ritentativo_identico_non_si_duplica_uno_diverso_si(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        RV.tentativo(self.reg, "A", "manifesto", "omesso: X", self.REGISTRI, ORA)
        prima = self.reg.read_bytes()
        RV.tentativo(self.reg, "A", "manifesto", "omesso: X", self.REGISTRI, "2026-11-27T00:00:00Z")
        self.assertEqual(self.reg.read_bytes(), prima)
        altri = [["registro_scaricamento_XAUUSD_ASK.csv", "ef" * 32], self.REGISTRI[1]]
        RV.tentativo(self.reg, "A", "manifesto", "omesso: X", altri, ORA)
        self.assertEqual(len(RV.prenotazione(self.reg, "A")["tentativi"]), 2)

    def test_rifiuti_del_tentativo(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        with self.assertRaisesRegex(ValueError, "sconosciuta"):
            RV.tentativo(self.reg, "Z", "manifesto", "m", self.REGISTRI, ORA)
        for fase, motivo, registri in (("", "m", self.REGISTRI), ("manifesto", "", self.REGISTRI),
                                       ("manifesto", "m", []), ("manifesto", "m", [["x", "corta"]])):
            with self.assertRaisesRegex(ValueError, "tentativo"):
                RV.tentativo(self.reg, "A", fase, motivo, registri, ORA)
        RV.autorizza(self.reg, "A", 1, "h", ORA)
        with self.assertRaisesRegex(ValueError, "tentativo"):
            RV.tentativo(self.reg, "A", "manifesto", "m", self.REGISTRI, ORA)  # dopo l'autorizzazione no


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
        # #128 (Gemini R18-04): NaN passava il confronto con la quota (ogni confronto con NaN è falso); anche un
        # testo o un booleano convertibili in numero non sono una quota registrata.
        for campo, valore in (("j", 5), ("alfa_j", 0.05), ("alfa_j", float("nan")), ("alfa_j", float("inf")),
                              ("alfa_j", "0.025"), ("alfa_j", True)):
            dati = json.loads(self.reg.read_text())
            originale = dati["eventi"][-1][campo]
            dati["eventi"][-1][campo] = valore
            self.reg.write_text(json.dumps(dati))
            with self.assertRaises(ValueError, msg=campo):
                RV.stato(self.reg)
            dati["eventi"][-1][campo] = originale
            self.reg.write_text(json.dumps(dati))
        RV.stato(self.reg)


# --- Schema riserva/2 (D-50, DGS-14 Q1-Q2, DGS-15 punto 4), 22/11/2026: test scritti PRIMA del codice ---
SCHEDA = "ab" * 32


class TestRiserva2(Base):
    def test_schema_2_e_registri_vecchi_rifiutati(self):
        self.assertEqual(json.loads(self.reg.read_text(encoding="utf-8"))["schema"], "riserva/2")
        dati = json.loads(self.reg.read_text(encoding="utf-8"))
        dati["schema"] = "riserva/1"
        self.reg.write_text(json.dumps(dati), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "riserva/2"):
            RV.stato(self.reg)

    def test_quota_prevista_non_scrive(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        prima = self.reg.read_bytes()
        self.assertEqual(RV.quota_prevista(self.reg, 1), (1, 0.025))
        self.assertEqual(RV.quota_prevista(self.reg, 2), (1, 0.0125))
        self.assertEqual(self.reg.read_bytes(), prima)

    def test_rifiuto_per_quota_durevole_senza_consumo(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        e = RV.rifiuta(self.reg, "A", 2, 0.025, "quota 1,25% non collaudata (D-31)", "prima dell'autorizzazione",
                       SCHEDA, ORA)
        self.assertEqual((e["tipo"], e["j_previsto"], e["m"], e["quota_calcolata"], e["quota_collaudata"]),
                         ("rifiuto", 1, 2, 0.0125, 0.025))
        s = RV.stato(self.reg)                                          # riletto dal file: durevole
        self.assertEqual(s["giorni"]["prenotato"] + s["giorni"]["consumato"], 0)
        self.assertEqual((s["aperture"], s["alfa_speso"], s["prenotazioni_attive"]), ([], 0, []))
        self.assertEqual([(r["id"], r["j_previsto"], r["motivo"]) for r in s["rifiuti"]],
                         [("A", 1, "quota 1,25% non collaudata (D-31)")])
        with self.assertRaisesRegex(ValueError, "rifiutat"):            # (b): la prenotazione è chiusa
            RV.autorizza(self.reg, "A", 1, "h", ORA)
        with self.assertRaisesRegex(ValueError, "già usata"):
            self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        self.prenota("A2", D(2005, 1, 1), D(2005, 1, 31))              # le date sono di nuovo disponibili
        self.assertEqual(RV.autorizza(self.reg, "A2", 1, "h", ORA)["j"], 1)   # j non è avanzato

    def test_rifiuto_solo_su_prenotazione_aperta_e_completo(self):
        with self.assertRaises(ValueError):
            RV.rifiuta(self.reg, "X", 2, 0.025, "m", "f", SCHEDA, ORA)
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        for args in ((2, 0.025, "", "f", SCHEDA), (2, 0.025, "m", "", SCHEDA), (2, 0.025, "m", "f", ""),
                     (True, 0.025, "m", "f", SCHEDA), (0, 0.025, "m", "f", SCHEDA)):
            with self.assertRaises(ValueError):
                RV.rifiuta(self.reg, "A", *args, ORA)
        RV.autorizza(self.reg, "A", 1, "h", ORA)
        with self.assertRaises(ValueError):                             # dopo l'autorizzazione non si rifiuta
            RV.rifiuta(self.reg, "A", 2, 0.025, "m", "f", SCHEDA, ORA)

    def test_rifiuto_manomesso_rifiutato_alla_ricostruzione(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        RV.rifiuta(self.reg, "A", 2, 0.025, "m", "f", SCHEDA, ORA)
        buono = self.reg.read_text(encoding="utf-8")
        for campo, valore in (("j_previsto", 2), ("quota_calcolata", 0.025), ("motivo", ""), ("m", 1.0)):
            dati = json.loads(buono)
            dati["eventi"][-1][campo] = valore
            self.reg.write_text(json.dumps(dati), encoding="utf-8")
            with self.assertRaises(ValueError, msg=campo):
                RV.stato(self.reg)

    def test_autorizzazione_ricontrolla_la_quota_attesa(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        self.prenota("B", D(2005, 2, 1), D(2005, 2, 28))
        RV.autorizza(self.reg, "A", 1, "h", ORA, quota_attesa=0.025)
        prima = self.reg.read_bytes()
        with self.assertRaisesRegex(ValueError, "quota"):              # B aveva controllato 2,5% prima di A
            RV.autorizza(self.reg, "B", 1, "h", ORA, quota_attesa=0.025)
        self.assertEqual(self.reg.read_bytes(), prima)                  # niente scritto, j resta 1
        self.assertEqual(RV.stato(self.reg)["prenotazioni_attive"], ["B"])

    def test_impegno_legato_all_impronta(self):
        imp = {"scheda": SCHEDA, "codice": "c" * 64, "finestra": ["2005-01-01", "2005-01-31"],
               "elenco": [["XAUUSD", "ASK", "2005-01-03", "d" * 64], ["XAUUSD", "BID", "2005-01-03", "e" * 64]]}
        h = RV.impronta_impegno(imp)
        self.assertEqual(h, RV.impronta_impegno(json.loads(json.dumps(imp))))
        self.assertEqual(h, RV.impronta_impegno(dict(reversed(list(imp.items())))))   # l'ordine delle chiavi non conta
        self.assertNotEqual(h, RV.impronta_impegno(dict(imp, codice="f" * 64)))
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        with self.assertRaisesRegex(ValueError, "impegno"):
            RV.autorizza(self.reg, "A", 1, "0" * 64, ORA, impegno=imp)
        a = RV.autorizza(self.reg, "A", 1, h, ORA, impegno=imp)
        self.assertEqual(a["impegno"], imp)
        self.assertEqual(RV.autorizza(self.reg, "A", 1, h, ORA, impegno=imp), a)   # ripetizione tecnica
        with self.assertRaises(ValueError):                             # stessa impronta, impegno diverso: no
            RV.autorizza(self.reg, "A", 1, h, ORA, impegno=dict(imp, codice="f" * 64))
        altro = dict(imp, finestra=["2005-01-01", "2005-01-30"])
        with self.assertRaises(ValueError):
            RV.autorizza(self.reg, "A", 1, RV.impronta_impegno(altro), ORA, impegno=altro)
        dati = json.loads(self.reg.read_text(encoding="utf-8"))
        dati["eventi"][-1]["impegno"]["codice"] = "f" * 64              # impegno ritoccato dopo
        self.reg.write_text(json.dumps(dati), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "impegno"):
            RV.stato(self.reg)

    def test_date_dello_sviluppo_fuori_dalla_riserva(self):          # PIANO-D51 §3.5
        reg = Path(self._t.name) / "riserva_vera.json"
        RV.crea(reg, D(2005, 1, 1), D(2023, 10, 31), 0.05, ORA)        # i confini di D-29
        for a, b in ((D(2023, 11, 15), D(2023, 12, 31)), (D(2023, 10, 1), D(2023, 11, 15)), (D(2024, 1, 2), D(2024, 1, 2))):
            with self.assertRaisesRegex(ValueError, "fuori dalla riserva"):
                RV.prenota(reg, "S", "H-900", a, b, "x", ORA)

    def test_una_sola_autorizzazione_per_domanda(self):              # #139 (DGS-17 Q8)
        # due prenotazioni della STESSA domanda (stessa ipotesi, stessa scheda): una sola si consuma, sotto il blocco
        RV.prenota(self.reg, "A", "H-900", D(2005, 1, 1), D(2005, 1, 31), SCHEDA, ORA)
        RV.prenota(self.reg, "B", "H-900", D(2005, 2, 1), D(2005, 2, 28), SCHEDA, ORA)
        RV.autorizza(self.reg, "A", 1, "h", ORA)
        prima = self.reg.read_bytes()
        with self.assertRaisesRegex(ValueError, "domanda già autorizzata"):
            RV.autorizza(self.reg, "B", 1, "h", ORA)
        self.assertEqual(self.reg.read_bytes(), prima)
        RV.prenota(self.reg, "C", "H-900", D(2005, 3, 1), D(2005, 3, 31), "cd" * 32, ORA)   # altra scheda: ammessa
        RV.autorizza(self.reg, "C", 2, "h", ORA)
        self.prenota("D", D(2005, 4, 1), D(2005, 4, 30))                                    # altra ipotesi: ammessa
        RV.autorizza(self.reg, "D", 2, "h", ORA)

    def test_unicita_anche_dopo_l_esito_della_prima(self):            # #139, revisione critica del 23/11
        # la prima verifica è conclusa (esito scritto): la stessa domanda non si riapre con un'altra prenotazione
        RV.prenota(self.reg, "A", "H-900", D(2005, 1, 1), D(2005, 1, 31), SCHEDA, ORA)
        RV.autorizza(self.reg, "A", 1, "h", ORA)
        RV.rendiconta(self.reg, "A", "bocciata", ORA)
        RV.prenota(self.reg, "B", "H-900", D(2005, 2, 1), D(2005, 2, 28), SCHEDA, ORA)
        prima = self.reg.read_bytes()
        with self.assertRaisesRegex(ValueError, "domanda già autorizzata con la prenotazione 'A'"):
            RV.autorizza(self.reg, "B", 1, "h", ORA)
        self.assertEqual(self.reg.read_bytes(), prima)

    def test_doppia_autorizzazione_della_stessa_domanda_rifiutata_alla_ricostruzione(self):
        RV.prenota(self.reg, "A", "H-900", D(2005, 1, 1), D(2005, 1, 31), SCHEDA, ORA)
        RV.prenota(self.reg, "B", "H-900", D(2005, 2, 1), D(2005, 2, 28), SCHEDA, ORA)
        RV.autorizza(self.reg, "A", 1, "h", ORA)
        dati = json.loads(self.reg.read_text(encoding="utf-8"))
        dati["eventi"].append({"tipo": "autorizzazione", "id": "B", "j": 2, "n_globale": 1, "hash_dati": "h", "m": 1,
                               "alfa_j": RV.quota(0.05, 2, 1), "ora": ORA})            # scritta a mano
        self.reg.write_text(json.dumps(dati), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "domanda già autorizzata"):
            RV.stato(self.reg)

    def test_prenotazione_letta_senza_scrivere(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        prima = self.reg.read_bytes()
        p = RV.prenotazione(self.reg, "A")
        self.assertEqual((p["stato"], p["evento"]["inizio"], p["evento"]["hash_domanda"], p["esito"]),
                         ("prenotato", "2005-01-01", "domanda-A", None))
        self.assertEqual(self.reg.read_bytes(), prima)
        with self.assertRaises(ValueError):
            RV.prenotazione(self.reg, "Z")
        RV.rifiuta(self.reg, "A", 2, 0.025, "m", "f", SCHEDA, ORA)
        self.assertEqual(RV.prenotazione(self.reg, "A")["stato"], "rifiutato")

    def test_esito_con_il_record_del_verdetto(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        RV.autorizza(self.reg, "A", 1, "h", ORA)
        rec = {"esito": "bocciata", "L": -0.1, "U": 0.05}
        RV.rendiconta(self.reg, "A", "bocciata", ORA, record=rec)
        self.assertEqual(RV.record_esito(self.reg, "A"), rec)
        with self.assertRaises(ValueError):
            RV.record_esito(self.reg, "B")
        self.prenota("C", D(2005, 3, 1), D(2005, 3, 31))
        RV.autorizza(self.reg, "C", 2, "h", ORA)
        with self.assertRaisesRegex(ValueError, "esito"):
            RV.rendiconta(self.reg, "C", "promossa", ORA, record={"esito": "bocciata"})   # record incoerente
        self.assertIsNone(RV.record_esito(self.reg, "C"))               # autorizzata, esito non ancora scritto


if __name__ == "__main__":
    unittest.main()


# ---------------------------------------------------------------------------------------------------------------
# R13 di Gemini (16/11/2026): #64 ancora a GitHub, #65 controlli dei valori
# ---------------------------------------------------------------------------------------------------------------
import subprocess as _sp                                         # noqa: E402


class TestValoriR13(Base):
    def test_valori_rifiutati(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        for m in (True, 0, -1, 1.0):
            with self.assertRaises(ValueError, msg=repr(m)):
                RV.autorizza(self.reg, "A", 12, "dati-A", ORA, m=m)
        for n in (0, -5, True, 12.0):
            with self.assertRaises(ValueError, msg=repr(n)):
                RV.autorizza(self.reg, "A", n, "dati-A", ORA)
        with self.assertRaises(ValueError):
            RV.autorizza(self.reg, "A", 12, "", ORA)
        RV.autorizza(self.reg, "A", 12, "dati-A", ORA)
        self.prenota("B", D(2005, 2, 1), D(2005, 2, 5))
        with self.assertRaises(ValueError):                                      # N globale non può scendere
            RV.autorizza(self.reg, "B", 11, "dati-B", ORA)
        RV.autorizza(self.reg, "B", 12, "dati-B", ORA)

    def test_niente_ripetizione_tecnica_dopo_l_esito(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        RV.autorizza(self.reg, "A", 12, "dati-A", ORA)
        RV.rendiconta(self.reg, "A", "bocciata", ORA)
        with self.assertRaises(ValueError):
            RV.autorizza(self.reg, "A", 12, "dati-A", ORA)

    def test_quarantena_sulla_parte_protetta_solo_con_sblocco(self):
        with self.assertRaises(ValueError):
            RV.quarantena(self.reg, D(2005, 11, 10), D(2005, 11, 12), "buchi", ORA)
        e = RV.quarantena(self.reg, D(2005, 11, 10), D(2005, 11, 12), "buchi", ORA, usa_protetta=True)
        self.assertTrue(e["usa_protetta"])

    def test_file_con_valori_falsi_rifiutato(self):
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        RV.autorizza(self.reg, "A", 12, "dati-A", ORA)
        for campo, valore in (("n_globale", 0), ("hash_dati", ""), ("m", True)):
            dati = json.loads(self.reg.read_text())
            originale = dati["eventi"][-1][campo]
            dati["eventi"][-1][campo] = valore
            if campo == "m":
                dati["eventi"][-1]["alfa_j"] = 0.05 / 2                         # quota coerente con m = 1
            self.reg.write_text(json.dumps(dati))
            with self.assertRaises(ValueError, msg=campo):
                RV.stato(self.reg)
            dati["eventi"][-1][campo] = originale
            self.reg.write_text(json.dumps(dati))
        RV.stato(self.reg)


class TestTestaRicontrollata(Base):
    def test_testa_scritta_a_mano_rifiutata(self):
        """#93 (revisore del laboratorio): la ricostruzione non ricontrollava la testa: α totale 5,0 o una parte
        protetta fuori dalla riserva erano accettati da un file scritto a mano."""
        for campo, valore in (("alfa_tot", 5.0), ("alfa_tot", 0.0), ("alfa_tot", True), ("alfa_tot", "0.05"),
                              ("protetta", ["2010-01-01", "2010-12-31"]), ("protetta", ["2005-12-31", "2005-11-01"]),
                              ("fine", "2004-12-31")):
            dati = json.loads(self.reg.read_text())
            originale = dati["riserva"][campo]
            dati["riserva"][campo] = valore
            self.reg.write_text(json.dumps(dati))
            with self.assertRaises(ValueError, msg=f"{campo} = {valore!r}"):
                RV.stato(self.reg)
            dati["riserva"][campo] = originale
            self.reg.write_text(json.dumps(dati))
        RV.stato(self.reg)

    def test_contatore_j_intero(self):
        """#94 (a): j = True o 1.0 erano accettati (True == 1)."""
        self.prenota("A", D(2005, 1, 1), D(2005, 1, 31))
        RV.autorizza(self.reg, "A", 12, "dati-A", ORA)
        for valore in (True, 1.0):
            dati = json.loads(self.reg.read_text())
            dati["eventi"][-1]["j"] = valore
            self.reg.write_text(json.dumps(dati))
            with self.assertRaises(ValueError, msg=repr(valore)):
                RV.stato(self.reg)
            dati["eventi"][-1]["j"] = 1
            self.reg.write_text(json.dumps(dati))
        RV.stato(self.reg)


class TestAncoraR13(unittest.TestCase):
    """#64 (R13-C1-01): il file della riserva ancorato alla versione su GitHub, come il registro delle prove."""

    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.dir = Path(self._t.name)
        remoto, self.repo = self.dir / "remoto.git", self.dir / "repo"
        _sp.run(["git", "init", "-q", "--bare", str(remoto)], check=True)
        _sp.run(["git", "clone", "-q", str(remoto), str(self.repo)], check=True, capture_output=True)
        self.g = ["git", "-C", str(self.repo), "-c", "user.name=t", "-c", "user.email=t@invalid"]
        _sp.run(self.g + ["checkout", "-q", "-b", "principale"], check=True)
        self.reg = self.repo / "riserva.json"
        RV.crea(self.reg, D(2005, 1, 1), D(2005, 12, 31), 0.05, ORA, protetta=(D(2005, 11, 1), D(2005, 12, 31)))
        RV.prenota(self.reg, "A", "H-900", D(2005, 1, 1), D(2005, 1, 31), "d", ORA)
        RV.autorizza(self.reg, "A", 12, "dati-A", ORA)
        self.commit_e_push("apertura")

    def tearDown(self):
        self._t.cleanup()

    def commit_e_push(self, msg):
        _sp.run(self.g + ["add", "riserva.json"], check=True)
        _sp.run(self.g + ["commit", "-q", "-m", msg], check=True)
        _sp.run(self.g + ["push", "-q", "-u", "origin", "principale"], check=True, capture_output=True)

    def scrivi(self, f):
        dati = json.loads(self.reg.read_text())
        f(dati)
        self.reg.write_text(json.dumps(dati))
        _sp.run(self.g + ["commit", "-q", "-am", "manomesso"], check=True)

    def test_continua_la_versione_su_github(self):
        RV.controlla_ancora(self.reg, self.repo)
        RV.rendiconta(self.reg, "A", "bocciata", ORA)
        with self.assertRaises(ValueError):                                      # non committato
            RV.controlla_ancora(self.reg, self.repo)
        self.commit_e_push("esito")
        RV.controlla_ancora(self.reg, self.repo)

    def test_manomissioni_committate_rifiutate(self):
        for f in (lambda d: d["riserva"].__setitem__("protetta", None),         # testa
                  lambda d: d["riserva"].__setitem__("fine", "2006-12-31"),
                  lambda d: d["eventi"][-1].__setitem__("hash_dati", "altro"),  # voce già su GitHub
                  lambda d: d["eventi"].pop()):                                   # troncamento
            _sp.run(self.g + ["reset", "-q", "--hard", "origin/principale"], check=True)
            self.scrivi(f)
            with self.assertRaises(ValueError):
                RV.controlla_ancora(self.reg, self.repo)
