"""Test dell'esecutore ordinario di verifica (laboratorio/esecuzione/esegui_verifica.py): #127, DGS-14, DGS-15 punti 2–4.
Scritti PRIMA del codice, 22/11/2026. Solo dati e registri SINTETICI (mercato_sintetico), nessuna rete.

Le regole di H-002 sono l'oggetto sintetico dentro una scheda di test conforme al modello H-003 (contratto JSON),
sigillata e presentata all'ingresso ordinario. Il percorso: controllo della scheda e del sigillo, prenotazione,
controllo della quota PRIMA di ogni lettura, screening sullo sviluppo, manifesto dei dati, autorizzazione con
l'impegno, lettura con i byte verificati, coppie, verdetto D-31, registrazione con il record, rapporto tipizzato.
Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_esegui_verifica
"""
import json
import shutil
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest import mock

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.laboratorio.esecuzione import caricatore as C            # noqa: E402
from brain.laboratorio.esecuzione import esegui_verifica as EV      # noqa: E402
from brain.laboratorio.esecuzione import manifesto as MF            # noqa: E402
from brain.laboratorio.esecuzione import riserva as RV              # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S               # noqa: E402
from brain.laboratorio.tests import mercato_sintetico as M           # noqa: E402
from brain.laboratorio.verdetto import verdetto_d31 as V            # noqa: E402

ORA = "2026-11-22T12:00:00Z"
LETTURA = date(2010, 1, 4)                     # inizio della lettura (date accessorie comprese)
ACCESSORIE = 35                                 # giorni di storia per le mediane di H-002 (20 sedute)
INIZIO = LETTURA + timedelta(days=ACCESSORIE)
FINE = M.fine_per_sedute(INIZIO, 1000)
B_INIZIO = date(2015, 1, 5)                                      # seconda richiesta (concorrenza): anche 1.000 sedute
B_FINE = M.fine_per_sedute(B_INIZIO + timedelta(days=ACCESSORIE), 1000)
SVILUPPO = (date(2024, 1, 1), date(2024, 12, 31))


def contratto(ipotesi, **k):
    c = {"modello": "H-003", "ipotesi": ipotesi, "destinazione": "test", "simulatore": "orb_londra",
         "variante": "V-T", "m": 1, "mercato": "XAUUSD", "metro": "D-31", "seme": 20261122, "screening_seme": 9,
         "potenza_stimata": 0.6, "date_accessorie": ACCESSORIE, "sedute": 1000,
         "veto_blocchi": {"soglia": -0.25, "minimo_trade": 50},
         "sviluppo": [SVILUPPO[0].isoformat(), SVILUPPO[1].isoformat()]}
    c.update(k)
    return c


def testo_scheda(c):
    return (f"# {c['ipotesi']} — scheda di TEST (oggetto sintetico: regole di H-002)\n\n"
            "Destinazione: prova sintetica del percorso ordinario (#127). Nessun dato vero.\n\n"
            f"```json contratto-h003\n{json.dumps(c, indent=2, ensure_ascii=False)}\n```\n")


class Percorso(unittest.TestCase):
    """Cache sintetiche scritte una volta; registri nuovi per ogni prova."""

    @classmethod
    def setUpClass(cls):
        cls._t = tempfile.TemporaryDirectory()
        base = Path(cls._t.name)
        cls.cache, cls.cache_sv = base / "cache", base / "cache_sviluppo"
        cls.vere = M.scrivi(cls.cache, LETTURA, FINE, 0.6, 11)
        M.scrivi(cls.cache, B_INIZIO, B_FINE, 0.6, 12)
        M.scrivi(cls.cache_sv, *SVILUPPO, 0.6, 13)

    @classmethod
    def tearDownClass(cls):
        cls._t.cleanup()

    def setUp(self):
        self._d = tempfile.TemporaryDirectory()
        self.d = Path(self._d.name)
        self.registro = self.d / "registro_prove.json"
        self.riserva = self.d / "riserva.json"
        RV.crea(self.riserva, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        self.chiamate = []
        vero = C.carica

        def conta(*a, **k):
            self.chiamate.append(a[4])                                   # modalità: sviluppo o verifica
            return vero(*a, **k)
        p = mock.patch.object(C, "carica", side_effect=conta)
        p.start()
        self.addCleanup(p.stop)

    def tearDown(self):
        self._d.cleanup()

    def prepara(self, ipotesi="H-T127", inizio=LETTURA, fine=FINE, id_="P1", sigilla=True, **k):
        scheda = self.d / f"{ipotesi}.md"
        scheda.write_text(testo_scheda(contratto(ipotesi, **k)), encoding="utf-8")
        if sigilla:
            S.sigilla(self.registro, ipotesi, scheda, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(self.riserva, id_, ipotesi, inizio, fine, S.impronta(scheda), ORA)
        return scheda

    def esegui(self, scheda, id_="P1", rapporto=None):
        return EV.esegui(scheda, self.registro, self.riserva, id_, self.cache, self.cache_sv,
                         rapporto or (self.d / f"rapporto_{id_}.txt"), ORA)


class TestCorsaCompleta(Percorso):
    def test_percorso_ordinario_promossa(self):
        scheda = self.prepara()
        n_prima = V.contesto_prove(self.registro)["n_prove"]
        r = self.esegui(scheda)
        self.assertEqual((r["esito_tecnico"], r["esito"]), ("completata", "promossa"))
        self.assertEqual(self.chiamate, ["sviluppo", "verifica"])
        self.assertEqual(r["chiamate_caricatore"], {"sviluppo": 1, "verifica": 1})
        # registro della riserva: una apertura, j = 1, quota 2,5%, date consumate = tutta la prenotazione
        s = RV.stato(self.riserva)
        self.assertEqual([(a["id"], a["j"], a["alfa_j"], a["esito"]) for a in s["aperture"]], [("P1", 1, 0.025, "promossa")])
        self.assertEqual(s["giorni"]["consumato"], (FINE - LETTURA).days + 1)
        self.assertEqual(s["aperture"][0]["n_globale"], n_prima)
        # impegno: scheda, codice, metro, finestra, registri, elenco con impronte, N, quota, variante, seme
        imp = RV._ricostruisci(RV._leggi(self.riserva)).prenotazioni["P1"]["autorizzazione"]["impegno"]
        self.assertEqual(imp["scheda_sha256"], S.impronta(scheda))
        self.assertEqual(imp["codice"], EV.impronte_codice())
        self.assertEqual(imp["metro"], {"modulo": "D-31", "pilota": V.IMPRONTA_PILOTA, "quota": 0.025})
        self.assertEqual(imp["finestra"], {"lettura": [LETTURA.isoformat(), FINE.isoformat()],
                                           "verifica": [INIZIO.isoformat(), FINE.isoformat()]})
        self.assertEqual((imp["variante"], imp["seme"], imp["n_globale"], imp["quota"], imp["j"]),
                         ("V-T", 20261122, n_prima, 0.025, 1))
        self.assertEqual(len(imp["registri"]), 2)
        self.assertEqual(len(imp["elenco"]), 2 * ((FINE - LETTURA).days + 1))
        self.assertEqual(imp["impronta_elenco"], MF.impronta_elenco(imp["elenco"]))
        # coppie: 1000 sedute, una operazione per seduta, media uguale al «vero» del mercato sintetico
        rec = RV.record_esito(self.riserva, "P1")
        v = rec["verdetto"]
        self.assertEqual((v["sedute"], v["trade"], v["sedute_attive"]), (1000, 1000, 1000))
        vinte = sum(1 for g, x in self.vere.items() if INIZIO <= g <= FINE and x)
        self.assertAlmostEqual(v["media"], (vinte * M.R_VINTA + (1000 - vinte) * M.R_PERSA) / 1000, places=6)
        self.assertEqual(rec["impronta_impegno"], RV.impronta_impegno(imp))
        self.assertTrue(rec["screening"]["ammessa"])
        # registro delle prove: screening, verifica ed esito, una volta sola
        ruoli = [e["ruolo"] for e in S.leggi(self.registro)["esecuzioni"]]
        self.assertEqual(ruoli, ["sviluppo", "verifica", "esito"])
        # rapporto tipizzato, rigenerabile dal record
        testo = Path(r["rapporto"]).read_text(encoding="utf-8")
        self.assertEqual(testo, EV.rapporto_da_record(rec))
        for frammento in ("VERDETTO D-31 · promossa", "[MISURA]", "[STIMA]", "[REGOLA]", "impronta dell'impegno",
                          "chiamate al caricatore", "criteri di H-002 (solo descrizione", "j = 1", "quota 0.025"):
            self.assertIn(frammento, testo)

    def test_ripresa_dopo_il_verdetto_senza_rileggere(self):
        scheda = self.prepara()
        rapporto = self.d / "rapporto.txt"
        vero = EV._scrivi_rapporto
        with mock.patch.object(EV, "_scrivi_rapporto", side_effect=RuntimeError("caduta prima del rapporto")):
            with self.assertRaisesRegex(RuntimeError, "caduta"):
                self.esegui(scheda, rapporto=rapporto)
        self.assertFalse(rapporto.exists())
        rec = RV.record_esito(self.riserva, "P1")
        self.assertEqual(rec["esito"], "promossa")                     # il verdetto era già registrato
        self.chiamate.clear()
        prima = self.riserva.read_bytes()
        with mock.patch.object(EV, "_scrivi_rapporto", side_effect=vero):
            r = self.esegui(scheda, rapporto=rapporto)
        self.assertEqual((r["esito_tecnico"], r["esito"]), ("rapporto rigenerato", "promossa"))
        self.assertEqual(self.chiamate, [])                             # nessuna lettura, né sviluppo né finestra
        self.assertEqual(self.riserva.read_bytes(), prima)              # nessun nuovo evento
        self.assertEqual(rapporto.read_text(encoding="utf-8"), EV.rapporto_da_record(rec))
        with mock.patch.object(EV, "impronte_codice", return_value={"x.py": "0" * 64}):
            with self.assertRaisesRegex(ValueError, "ripresa non identica"):
                self.esegui(scheda, rapporto=rapporto)


class TestRifiutiPrimaDellaLettura(Percorso):
    def test_vecchia_scheda_h002_rifiutata(self):
        vecchia = self.d / "H-002-ORB-v3.md"
        shutil.copy(repo_root / "brain" / "laboratorio" / "ipotesi" / "H-002-ORB-v3.md", vecchia)
        RV.prenota(self.riserva, "P1", "H-002", LETTURA, FINE, S.impronta(vecchia), ORA)
        prima = self.riserva.read_bytes()
        with self.assertRaisesRegex(EV.SchedaNonConforme, "H-003"):
            self.esegui(vecchia)
        self.assertEqual((self.chiamate, self.riserva.read_bytes()), ([], prima))

    def test_contratto_incompleto_o_non_di_test(self):
        for difetto in ({"metro": "HAC"}, {"m": True}, {"sedute": 999}, {"variante": "V-X"}, {"modello": "H-002"}):
            with self.subTest(difetto=difetto):
                scheda = self.d / "x.md"
                scheda.write_text(testo_scheda(contratto("H-X", **difetto)), encoding="utf-8")
                with self.assertRaises(EV.SchedaNonConforme):
                    EV.leggi_contratto(scheda)

    def test_prenotazione_di_un_altra_scheda_o_non_sigillata(self):
        scheda = self.prepara()
        scheda.write_text(scheda.read_text(encoding="utf-8") + "\nmodifica dopo il sigillo\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.esegui(scheda)
        self.assertEqual(self.chiamate, [])
        altra = self.prepara("H-T128", B_INIZIO, B_FINE, "P2", sigilla=False)
        with self.assertRaises(S.NonSigillata):
            self.esegui(altra, "P2")
        self.assertEqual(self.chiamate, [])

    def test_quota_non_collaudata_rifiuto_durevole_e_zero_letture(self):
        scheda = self.prepara(m=2)
        n_prima = V.contesto_prove(self.registro)["n_prove"]
        r = self.esegui(scheda)
        self.assertEqual((r["esito_tecnico"], r["esito"]), ("rifiutata per quota", None))
        self.assertEqual((self.chiamate, r["chiamate_caricatore"]), ([], {"sviluppo": 0, "verifica": 0}))
        s = RV.stato(self.riserva)                                     # riletto dal file: durevole
        self.assertEqual((s["aperture"], s["alfa_speso"], s["giorni"]["consumato"], s["giorni"]["prenotato"]),
                         ([], 0, 0, 0))
        self.assertEqual([(x["id"], x["j_previsto"], x["m"], x["quota_calcolata"], x["impronta_scheda"])
                          for x in s["rifiuti"]], [("P1", 1, 2, 0.0125, S.impronta(scheda))])
        self.assertEqual(RV.quota_prevista(self.riserva, 1), (1, 0.025))   # l'indice delle aperture non avanza
        self.assertEqual(V.contesto_prove(self.registro)["n_prove"], n_prima)
        self.assertEqual(S.leggi(self.registro)["esecuzioni"], [])
        with self.assertRaisesRegex(ValueError, "rifiutat"):           # la stessa richiesta resta chiusa
            self.esegui(scheda)
        self.assertEqual(self.chiamate, [])


class TestConcorrenzaEFileDifforme(Percorso):
    def test_due_richieste_una_sola_apertura_alla_quota(self):
        scheda_a = self.prepara("H-TA", LETTURA, FINE, "A")
        scheda_b = self.prepara("H-TB", B_INIZIO, B_FINE, "B")
        vero_manifesto, vero_carica = MF.manifesto, C.carica.side_effect
        stato = {"a_fatta": False}

        def carica_che_cade(*a, **k):
            if a[4] == "verifica":
                raise RuntimeError("caduta di A durante la lettura")
            return vero_carica(*a, **k)

        def manifesto(*a, **k):
            if not stato["a_fatta"] and a[2] == B_INIZIO:               # B ha già controllato la quota: arriva A
                stato["a_fatta"] = True
                with mock.patch.object(C, "carica", side_effect=carica_che_cade):
                    with self.assertRaisesRegex(RuntimeError, "caduta di A"):
                        self.esegui(scheda_a, "A")
            return vero_manifesto(*a, **k)
        with mock.patch.object(MF, "manifesto", side_effect=manifesto):
            r = self.esegui(scheda_b, "B")
        self.assertEqual((r["esito_tecnico"], r["esito"]), ("rifiutata per quota", None))
        self.assertEqual(r["chiamate_caricatore"]["verifica"], 0)
        s = RV.stato(self.riserva)
        self.assertEqual([(x["id"], x["j"], x["alfa_j"]) for x in s["aperture"]], [("A", 1, 0.025)])
        self.assertEqual([(x["id"], x["j_previsto"], x["fase"]) for x in s["rifiuti"]],
                         [("B", 2, "ricontrollo all'autorizzazione")])
        self.assertEqual(s["giorni"]["consumato"], (FINE - LETTURA).days + 1)   # solo le date di A

    def test_file_difforme_dopo_l_autorizzazione(self):
        scheda = self.prepara()
        bersaglio = self.cache / "XAUUSD_ASK" / f"{(INIZIO + timedelta(days=10)).isoformat()}.bi5"
        originale = bersaglio.read_bytes()
        vero = C.carica.side_effect

        def sostituisce_poi_carica(*a, **k):
            if a[4] == "verifica":
                bersaglio.write_bytes(originale + b"\x00")
            return vero(*a, **k)
        try:
            with mock.patch.object(C, "carica", side_effect=sostituisce_poi_carica):
                r = self.esegui(scheda)
        finally:
            bersaglio.write_bytes(originale)
        self.assertEqual((r["esito_tecnico"], r["esito"]), ("file difforme", "non decidibile"))
        s = RV.stato(self.riserva)
        self.assertEqual([(a["id"], a["esito"]) for a in s["aperture"]], [("P1", "non decidibile")])
        self.assertEqual(s["giorni"]["consumato"], (FINE - LETTURA).days + 1)  # il consumo resta
        rec = RV.record_esito(self.riserva, "P1")
        self.assertIn("byte diversi dal manifesto", rec["causa"])
        self.assertIn("file difforme", Path(r["rapporto"]).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
