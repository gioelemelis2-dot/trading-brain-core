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


CACHE = {}


def setUpModule():
    """Le cache sintetiche si scrivono UNA volta per tutto il modulo (sono solo lette dalle prove)."""
    CACHE["tmp"] = tempfile.TemporaryDirectory()
    base = Path(CACHE["tmp"].name)
    CACHE["cache"], CACHE["sviluppo"] = base / "cache", base / "cache_sviluppo"
    CACHE["vere"] = M.scrivi(CACHE["cache"], LETTURA, FINE, 0.6, 11)
    M.scrivi(CACHE["cache"], B_INIZIO, B_FINE, 0.6, 12)
    M.scrivi(CACHE["sviluppo"], *SVILUPPO, 0.6, 13)


def tearDownModule():
    CACHE["tmp"].cleanup()


class Percorso(unittest.TestCase):
    """Cache sintetiche comuni; registri nuovi per ogni prova."""

    @classmethod
    def setUpClass(cls):
        cls.cache, cls.cache_sv, cls.vere = CACHE["cache"], CACHE["sviluppo"], CACHE["vere"]

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
        for nome in ("ANCORA_GIT", "CONTROLLO_AMBIENTE"):                  # registri temporanei, stesso processo
            q = mock.patch.object(EV, nome, False)
            q.start()
            self.addCleanup(q.stop)

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
        # DGS-16: l'elenco delle sedute è fissato nell'impegno PRIMA dell'autorizzazione (calendario di H-002: feriali
        # senza le chiusure inglesi), e le coppie del record sono proprio quelle sedute, in ordine, comprese le
        # sedute senza operazioni
        attese = [g.isoformat() for g in M.sedute(INIZIO, FINE)]
        self.assertEqual(imp["sedute"], attese)
        sv = MF.manifesto(self.cache_sv, "XAUUSD", *SVILUPPO)                # PIANO-D51 §3.2
        self.assertEqual(imp["sviluppo"], {"finestra": [SVILUPPO[0].isoformat(), SVILUPPO[1].isoformat()],
                                           "registri": sv["registri"], "impronta_elenco": sv["impronta_elenco"]})
        self.assertEqual(S.leggi(self.registro)["esecuzioni"][0]["impronta_sviluppo"], sv["impronta_elenco"])
        self.assertEqual(len(attese), 1000)
        self.assertEqual([x[0] for x in rec["coppie"]], attese)
        self.assertEqual(sum(x[2] for x in rec["coppie"]), 1000)
        esclusi = [g.isoformat() for g in (INIZIO + timedelta(days=i) for i in range((FINE - INIZIO).days + 1))
                   if g.weekday() < 5 and g.isoformat() not in attese]
        self.assertEqual(len(esclusi), 40)                              # le chiusure del calendario (DGS-16)
        self.assertEqual(rec["feriali_esclusi"], esclusi)
        self.assertTrue(rec["screening"]["ammessa"])
        self.assertEqual(rec["descrizione_h002"]["n"], 1000)          # le date accessorie sono solo storia
        # registro delle prove: screening, verifica ed esito, una volta sola
        ruoli = [e["ruolo"] for e in S.leggi(self.registro)["esecuzioni"]]
        self.assertEqual(ruoli, ["sviluppo", "verifica", "esito"])
        # rapporto tipizzato, rigenerabile dal record
        testo = Path(r["rapporto"]).read_text(encoding="utf-8")
        self.assertEqual(testo, EV.rapporto_da_record(rec))
        for frammento in ("VERDETTO D-31 · promossa", "[MISURA]", "[STIMA]", "[REGOLA]", "impronta dell'impegno",
                          "chiamate al caricatore", "criteri di H-002 (solo descrizione", "j = 1", "quota 0.025",
                          "requisito blocchi [veto]: superato"):
            self.assertIn(frammento, testo)
        riga = [x for x in testo.splitlines() if x.startswith("- criteri di H-002")][0]
        self.assertTrue(riga.endswith("[DERIVATO]"), riga[-40:])          # #141 (b): Sharpe, media, drawdown
        self.assertNotIn("procedura congelata", testo)                     # #141 (a)

    def test_seconda_verifica_della_stessa_variante_rifiutata_prima_di_consumare(self):
        # PIANO-D51 §3.4: una verifica per ipotesi e variante (come nella vecchia verifica). Una seconda prenotazione
        # della stessa ipotesi si ferma PRIMA di ogni lettura e senza consumare la riserva
        scheda = self.prepara()
        self.assertEqual(self.esegui(scheda)["esito"], "promossa")
        RV.prenota(self.riserva, "P2", "H-T127", B_INIZIO, B_FINE, S.impronta(scheda), ORA)
        self.chiamate.clear()
        prima = self.riserva.read_bytes()
        with self.assertRaisesRegex(ValueError, "verifica di H-T127 V-T già eseguita"):
            self.esegui(scheda, "P2")
        self.assertEqual((self.chiamate, self.riserva.read_bytes()), ([], prima))
        self.assertEqual(RV.prenotazione(self.riserva, "P2")["stato"], "prenotato")
        voci = [e for e in S.leggi(self.registro)["esecuzioni"] if e["ruolo"] == "verifica"]
        self.assertEqual([e["prenotazione"] for e in voci], ["P1"])

    def test_caduta_dopo_l_esito_nella_riserva_prima_del_registro_delle_prove(self):
        # #140 (DGS-17 Q8): la ripresa riconcilia i due registri: l'esito entra UNA volta nel registro delle prove
        scheda = self.prepara()
        vero = EV._registra_una_volta

        def cade_sull_esito(registro, ipotesi, voce, ora):
            if voce["ruolo"] == "esito":
                raise RuntimeError("caduta fra i due registri")
            return vero(registro, ipotesi, voce, ora)
        with mock.patch.object(EV, "_registra_una_volta", side_effect=cade_sull_esito):
            with self.assertRaisesRegex(RuntimeError, "fra i due registri"):
                self.esegui(scheda)
        self.assertEqual(RV.record_esito(self.riserva, "P1")["esito"], "promossa")
        self.assertEqual([e["ruolo"] for e in S.leggi(self.registro)["esecuzioni"]], ["sviluppo", "verifica"])
        self.chiamate.clear()
        r = self.esegui(scheda)
        self.assertEqual((r["esito_tecnico"], self.chiamate), ("rapporto rigenerato", []))
        esiti = [e for e in S.leggi(self.registro)["esecuzioni"] if e["ruolo"] == "esito"]
        self.assertEqual([(e["esito"], e["impronta_impegno"]) for e in esiti],
                         [("promossa", RV.record_esito(self.riserva, "P1")["impronta_impegno"])])
        self.esegui(scheda)                                              # una seconda ripresa non duplica
        self.assertEqual(len([e for e in S.leggi(self.registro)["esecuzioni"] if e["ruolo"] == "esito"]), 1)

    def test_caduta_durante_la_lettura_ripresa_tecnica_identica(self):
        # DGS-17 Q8, revisione critica del 23/11: dopo l'autorizzazione e la voce «verifica», la lettura cade. La
        # ripresa con la stessa scheda è una RIPETIZIONE TECNICA: stessa autorizzazione (stessi j, quota e impegno),
        # nessuna seconda apertura, una sola voce «verifica», un solo esito
        scheda = self.prepara()
        vero = C.carica.side_effect

        def cade(*a, **k):
            if a[4] == "verifica":
                raise RuntimeError("caduta durante la lettura")
            return vero(*a, **k)
        with mock.patch.object(C, "carica", side_effect=cade):
            with self.assertRaisesRegex(RuntimeError, "durante la lettura"):
                self.esegui(scheda)
        prima = RV.prenotazione(self.riserva, "P1")
        self.assertEqual((prima["stato"], prima["esito"]), ("autorizzato", None))
        eventi = len(json.loads(self.riserva.read_text(encoding="utf-8"))["eventi"])
        r = self.esegui(scheda)
        self.assertEqual((r["esito_tecnico"], r["esito"]), ("completata", "promossa"))
        dopo = RV.prenotazione(self.riserva, "P1")
        self.assertEqual(dopo["autorizzazione"], prima["autorizzazione"])
        self.assertEqual(len(json.loads(self.riserva.read_text(encoding="utf-8"))["eventi"]), eventi + 1)  # solo l'esito
        self.assertEqual([(x["id"], x["j"]) for x in RV.stato(self.riserva)["aperture"]], [("P1", 1)])
        ruoli = [e["ruolo"] for e in S.leggi(self.registro)["esecuzioni"]]
        self.assertEqual(ruoli, ["sviluppo", "verifica", "esito"])

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

    def test_variante_non_dichiarata_nel_sigillo_prima_dell_autorizzazione(self):
        # #137 (seconda revisione di Claude): il rifiuto arrivava solo alla registrazione dello screening, dopo una
        # lettura dello sviluppo; ora arriva subito dopo il sigillo, prima di ogni lettura
        scheda = self.prepara(variante="V-S")                          # sigillo con le sole ["V-T"]
        prima = self.riserva.read_bytes()
        with self.assertRaisesRegex(ValueError, "non dichiarata nel sigillo"):
            self.esegui(scheda)
        self.assertEqual((self.chiamate, self.riserva.read_bytes()), ([], prima))

    def test_prenotazione_con_l_impronta_di_un_altra_scheda(self):
        scheda = self.prepara()                                         # sigillata e prenotata come P1
        RV.prenota(self.riserva, "P9", "H-T127", B_INIZIO, B_FINE, "0" * 64, ORA)   # stessa ipotesi, altra domanda
        with self.assertRaisesRegex(ValueError, "un'altra scheda"):
            self.esegui(scheda, "P9")
        self.assertEqual(self.chiamate, [])

    def test_giorno_omesso_nel_registro_dello_scaricamento(self):
        scheda = self.prepara()
        reg = self.cache / "registro_scaricamento_XAUUSD_ASK.csv"
        originale = reg.read_bytes()
        righe = originale.decode("utf-8").splitlines(keepends=True)
        reg.write_text("".join(x for x in righe if not x.split(",")[1:2] == [INIZIO.isoformat()]), encoding="utf-8")
        prima = self.riserva.read_bytes()
        try:
            with self.assertRaisesRegex(ValueError, f"manifesto con anomalie: omesso: XAUUSD ASK {INIZIO.isoformat()}"):
                self.esegui(scheda)
        finally:
            reg.write_bytes(originale)
        self.assertEqual((self.chiamate, self.riserva.read_bytes()), (["sviluppo"], prima))   # nessuna autorizzazione

    def test_dopo_l_anomalia_corretta_la_stessa_prenotazione_riprende(self):
        # DGS-16 Q3: G lascia la prenotazione aperta (nessuna autorizzazione); corretto il registro dello scaricamento,
        # la STESSA richiesta, con scheda e identità invariate, si esegue
        scheda = self.prepara()
        reg = self.cache / "registro_scaricamento_XAUUSD_ASK.csv"
        originale = reg.read_bytes()
        righe = originale.decode("utf-8").splitlines(keepends=True)
        reg.write_text("".join(x for x in righe if not x.split(",")[1:2] == [INIZIO.isoformat()]), encoding="utf-8")
        try:
            with self.assertRaisesRegex(ValueError, "manifesto con anomalie"):
                self.esegui(scheda)
        finally:
            reg.write_bytes(originale)
        self.assertEqual(RV.prenotazione(self.riserva, "P1")["stato"], "prenotato")
        r = self.esegui(scheda)
        self.assertEqual((r["esito_tecnico"], r["esito"]), ("completata", "promossa"))

    def test_prenotazione_abbandonata_si_rilascia(self):
        # DGS-16 Q3, transizione di B: una prenotazione che non si può eseguire (scheda non conforme) si libera
        # con un rilascio registrato, prima di qualunque autorizzazione; le date tornano disponibili
        vecchia = self.d / "H-002-ORB-v3.md"
        shutil.copy(repo_root / "brain" / "laboratorio" / "ipotesi" / "H-002-ORB-v3.md", vecchia)
        RV.prenota(self.riserva, "P1", "H-002", LETTURA, FINE, S.impronta(vecchia), ORA)
        with self.assertRaises(EV.SchedaNonConforme):
            self.esegui(vecchia)
        self.assertEqual(RV.prenotazione(self.riserva, "P1")["stato"], "prenotato")   # DGS-17: il rifiuto NON rilascia
        RV.rilascia(self.riserva, "P1", ORA)                                         # il rilascio è un atto esplicito
        s = RV.stato(self.riserva)
        self.assertEqual((s["giorni"]["prenotato"], s["prenotazioni_attive"]), (0, []))
        self.assertEqual(RV.prenotazione(self.riserva, "P1")["stato"], "rilasciato")

    def test_dati_di_sviluppo_diversi_dal_registro_dello_scaricamento(self):
        # PIANO-D51 §3.2 (protezione R11-S6 e #51 della vecchia verifica): lo screening legge lo sviluppo con i byte
        # verificati contro il registro dello scaricamento; un file cambiato ferma tutto PRIMA dell'autorizzazione
        scheda = self.prepara()
        f = self.cache_sv / "XAUUSD" / "2024-03-05.bi5"
        originale = f.read_bytes()
        prima = self.riserva.read_bytes()
        try:
            f.write_bytes(originale + b"\x00")
            with self.assertRaisesRegex(ValueError, "BID 2024-03-05: byte diversi"):
                self.esegui(scheda)
        finally:
            f.write_bytes(originale)
        self.assertEqual((self.chiamate, self.riserva.read_bytes()), (["sviluppo"], prima))
        self.assertEqual(S.leggi(self.registro)["esecuzioni"], [])

    def test_screening_gia_registrato_con_altri_dati_di_sviluppo(self):
        # PIANO-D51 §3.2: uno screening registrato con un'altra impronta dello sviluppo non si sostituisce in silenzio
        scheda = self.prepara()
        S.registra_esecuzioni(self.registro, "H-T127", [{"ruolo": "sviluppo", "variante": "V-T",
                                                         "impronta_sviluppo": "0" * 64}], ORA)
        prima = self.riserva.read_bytes()
        with self.assertRaisesRegex(ValueError, "già registrata con un altro sviluppo"):
            self.esegui(scheda)
        self.assertEqual(self.riserva.read_bytes(), prima)

    def test_registro_dello_scaricamento_dello_sviluppo_con_anomalie(self):
        scheda = self.prepara()
        reg = self.cache_sv / "registro_scaricamento_XAUUSD_BID.csv"
        originale = reg.read_bytes()
        righe = originale.decode("utf-8").splitlines(keepends=True)
        prima = self.riserva.read_bytes()
        try:
            reg.write_text("".join(x for x in righe if not x.split(",")[1:2] == ["2024-03-05"]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "manifesto dello sviluppo con anomalie: omesso: XAUUSD BID 2024-03-05"):
                self.esegui(scheda)
        finally:
            reg.write_bytes(originale)
        self.assertEqual((self.chiamate, self.riserva.read_bytes()), ([], prima))

    def test_finestra_diversa_da_1000_sedute(self):
        scheda = self.prepara(fine=FINE - timedelta(days=1))
        prima = self.riserva.read_bytes()
        with self.assertRaisesRegex(ValueError, "999 sedute"):
            self.esegui(scheda)
        self.assertEqual((self.chiamate, self.riserva.read_bytes()), ([], prima))

    def test_screening_non_superato_ferma_prima_del_manifesto(self):
        scheda = self.prepara(potenza_stimata=0.4)
        prima = self.riserva.read_bytes()
        with mock.patch.object(MF, "manifesto", wraps=MF.manifesto) as man:
            with self.assertRaisesRegex(ValueError, "screening non superato"):
                self.esegui(scheda)
        self.assertEqual([c.args[2] for c in man.call_args_list], [SVILUPPO[0]])   # solo il manifesto dello sviluppo
        self.assertEqual((self.chiamate, self.riserva.read_bytes()), (["sviluppo"], prima))

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


class TestCostanti(unittest.TestCase):
    def test_ancora_accesa_nel_codice(self):                           # mutante EV23: solo i test la spengono
        self.assertIs(EV.ANCORA_GIT, True)
        self.assertIs(EV.CONTROLLO_AMBIENTE, True)                      # PIANO-D51 §3.3
        self.assertEqual((EV.REL_REGISTRO_PROVE, EV.REL_RISERVA),
                         ("brain/laboratorio/registro_prove.json", "brain/laboratorio/registro_riserva.json"))


class TestAncoraEStoria(Percorso):
    """PIANO-D51 §3.1 (protezioni #86, #125, R14-03 della vecchia verifica, portate nel percorso ordinario): registri
    canonici, ancorati alla versione su GitHub, con la storia completa; una prenotazione consumata in un'altra
    versione del registro della riserva non si riusa; N non scende. Repository git temporaneo con un remoto finto."""

    def setUp(self):
        import subprocess
        super().setUp()
        self.sp = subprocess
        remoto, self.repo = self.d / "remoto.git", self.d / "repo"
        subprocess.run(["git", "init", "-q", "--bare", str(remoto)], check=True)
        subprocess.run(["git", "clone", "-q", str(remoto), str(self.repo)], check=True, capture_output=True)
        self.g = ["git", "-C", str(self.repo), "-c", "user.name=t", "-c", "user.email=t@invalid"]
        subprocess.run(self.g + ["checkout", "-q", "-b", "principale"], check=True)
        base = self.repo / "brain" / "laboratorio"
        base.mkdir(parents=True)
        self.registro = base / "registro_prove.json"
        self.riserva = base / "registro_riserva.json"
        RV.crea(self.riserva, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        for nome, valore in (("RADICE", self.repo), ("ANCORA_GIT", True)):
            c = mock.patch.object(EV, nome, valore)
            c.start()
            self.addCleanup(c.stop)
        self.d_schede = self.repo

    def spingi(self, messaggio, ramo="principale"):
        self.sp.run(self.g + ["add", "-A"], check=True)
        self.sp.run(self.g + ["commit", "-q", "-m", messaggio], check=True)
        self.sp.run(self.g + ["push", "-q", "-u", "origin", ramo], check=True, capture_output=True)
        return self.sp.run(self.g + ["rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

    def scheda_nel_repo(self, ipotesi="H-T127", id_="P1", inizio=LETTURA, fine=FINE):
        scheda = self.repo / f"{ipotesi}.md"
        scheda.write_text(testo_scheda(contratto(ipotesi)), encoding="utf-8")
        S.sigilla(self.registro, ipotesi, scheda, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(self.riserva, id_, ipotesi, inizio, fine, S.impronta(scheda), ORA)
        return scheda

    def test_registro_della_riserva_non_canonico(self):
        scheda = self.scheda_nel_repo()
        self.spingi("sigillo e prenotazione")
        altro = self.repo / "riserva_bis.json"
        altro.write_bytes(self.riserva.read_bytes())
        with self.assertRaisesRegex(ValueError, "canonico"):
            EV.esegui(scheda, self.registro, altro, "P1", self.cache, self.cache_sv, self.d / "r.txt", ORA)
        self.assertEqual(self.chiamate, [])

    def test_riserva_non_committata(self):
        scheda = self.scheda_nel_repo()
        self.spingi("sigillo e prenotazione")
        RV.quarantena(self.riserva, date(2005, 1, 3), date(2005, 1, 3), "prova", ORA)   # modifica locale
        with self.assertRaisesRegex(ValueError, "committ"):
            self.esegui(scheda)
        self.assertEqual(self.chiamate, [])

    def test_prenotazione_consumata_in_un_altra_versione(self):
        scheda = self.scheda_nel_repo()
        prima = self.spingi("sigillo e prenotazione")
        RV.autorizza(self.riserva, "P1", 1, "h" * 64, ORA)                # consumata su principale
        self.spingi("autorizzata")
        self.sp.run(self.g + ["checkout", "-q", "-b", "rifaccio", prima], check=True)
        self.sp.run(self.g + ["push", "-q", "-u", "origin", "rifaccio"], check=True, capture_output=True)
        self.assertEqual(RV.prenotazione(self.riserva, "P1")["stato"], "prenotato")   # qui sembra libera
        with self.assertRaisesRegex(ValueError, "'P1' è già consumata in un'altra versione"):   # mutante EV26
            self.esegui(scheda)
        self.assertEqual(self.chiamate, [])

    def test_aperture_perse_rispetto_a_un_altra_versione(self):
        # un'ALTRA prenotazione consumata altrove: su questo ramo j è più basso, quindi la quota sarebbe sbagliata
        scheda = self.scheda_nel_repo()
        RV.prenota(self.riserva, "P2", "H-ALTRA", date(2015, 1, 5), date(2015, 3, 31), "d" * 64, ORA)
        prima = self.spingi("due prenotazioni")
        RV.autorizza(self.riserva, "P2", 1, "h" * 64, ORA)
        self.spingi("P2 autorizzata")
        self.sp.run(self.g + ["checkout", "-q", "-b", "rifaccio", prima], check=True)
        self.sp.run(self.g + ["push", "-q", "-u", "origin", "rifaccio"], check=True, capture_output=True)
        with self.assertRaisesRegex(ValueError, "j non scende"):
            self.esegui(scheda)
        self.assertEqual(self.chiamate, [])

    def test_n_non_scende(self):
        scheda = self.scheda_nel_repo()
        prima = self.spingi("sigillo e prenotazione")                     # N = 1
        S.sigilla(self.registro, "H-ALTRA", scheda, [f"X{k}" for k in range(8)], ORA)
        self.spingi("altre 8 prove")                                       # N = 9
        self.sp.run(self.g + ["checkout", "-q", "-b", "vecchio", prima], check=True)
        self.sp.run(self.g + ["push", "-q", "-u", "origin", "vecchio"], check=True, capture_output=True)
        self.assertEqual(V.contesto_prove(self.registro)["n_prove"], 1)
        self.assertEqual(EV.n_globale(self.registro, EV.RADICE)["n_prove"], 9)


class TestLanciatore(Percorso):
    """PIANO-D51 §3.3 (#61, #95 della vecchia verifica, portati nel percorso ordinario): il solo ingresso è il
    lanciatore `avvio.py verifica`, che controlla l'ambiente e il codice sigillato PRIMA di importare il progetto;
    l'esecutore, chiamato direttamente, si ferma; e ricontrolla l'ambiente prima di leggere i dati."""

    def test_senza_lanciatore_si_ferma(self):
        scheda = self.prepara()
        prima = self.riserva.read_bytes()
        argomenti = ["--scheda", str(scheda), "--registro", str(self.registro), "--riserva", str(self.riserva),
                     "--prenotazione", "P1", "--cache", str(self.cache), "--cache-sviluppo", str(self.cache_sv),
                     "--rapporto", str(self.d / "r.txt"), "--ora", ORA]
        import contextlib
        import io
        errore = io.StringIO()
        with mock.patch.object(EV, "CONTROLLO_AMBIENTE", True), contextlib.redirect_stderr(errore), \
                contextlib.redirect_stdout(io.StringIO()):
            rc = EV.main(argomenti)
        self.assertEqual(rc, 2)
        self.assertIn("avvio.py verifica", errore.getvalue())
        self.assertEqual((self.chiamate, self.riserva.read_bytes()), ([], prima))

    def test_ambiente_ricontrollato_prima_di_leggere(self):
        scheda = self.prepara()
        visti = []

        def ambiente(codice):
            visti.append(codice)
            raise ValueError("ambiente non pulito (simulato)")
        with mock.patch.object(EV, "CONTROLLO_AMBIENTE", True), mock.patch.object(EV, "controlla_ambiente", ambiente):
            with self.assertRaisesRegex(ValueError, "ambiente non pulito"):
                self.esegui(scheda)
        self.assertEqual(visti, [EV.impronte_codice()])                  # con il codice sigillato
        self.assertEqual(self.chiamate, [])


class TestAvvioVerifica(unittest.TestCase):
    """Il lanciatore in una COPIA di `brain`, in un processo separato (come TestAvvioControllato di esegui_h002)."""

    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.dir = Path(self._t.name)
        shutil.copytree(repo_root / "brain", self.dir / "brain", ignore=shutil.ignore_patterns("__pycache__"))
        self.scheda = self.dir / "H-T127.md"
        self.scheda.write_text(testo_scheda(contratto("H-T127")), encoding="utf-8")

    def tearDown(self):
        self._t.cleanup()

    def sigilla(self, ipotesi="H-T127", codice=None):
        reg = self.dir / "brain/laboratorio/registro_prove.json"
        reg.write_text(json.dumps({"schema": S.SCHEMA, "prove": [], "esecuzioni": [], "sigilli": [
            {"ipotesi": ipotesi, "codice": EV.impronte_codice(self.dir) if codice is None else codice}]}),
            encoding="utf-8")

    def avvia(self, *argomenti):
        import os
        import subprocess
        return subprocess.run([sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py", "verifica",
                               *argomenti], cwd=str(self.dir), capture_output=True, text=True,
                              env=dict(os.environ, HTTPS_PROXY="http://127.0.0.1:9", HTTP_PROXY="http://127.0.0.1:9"))

    def test_scheda_senza_contratto_ferma_prima_degli_import(self):
        self.sigilla()
        vecchia = self.dir / "vecchia.md"
        vecchia.write_text("# H-002\nnessun contratto\n", encoding="utf-8")
        r = self.avvia("--scheda", str(vecchia))
        self.assertEqual(r.returncode, 2)
        self.assertIn("FERMO prima di importare", r.stderr)
        self.assertIn("contratto", r.stderr)

    def test_codice_non_sigillato_per_quell_ipotesi(self):
        self.sigilla(ipotesi="H-ALTRA")
        r = self.avvia("--scheda", str(self.scheda))
        self.assertEqual(r.returncode, 2)
        self.assertIn("FERMO prima di importare", r.stderr)
        self.assertIn("H-T127", r.stderr)

    def test_codice_cambiato_dopo_il_sigillo(self):
        codice = EV.impronte_codice(self.dir)
        primo = sorted(codice)[0]
        self.sigilla(codice=dict(codice, **{primo: "0" * 64}))
        r = self.avvia("--scheda", str(self.scheda))
        self.assertEqual(r.returncode, 2)
        self.assertIn("diverso da quello sigillato", r.stderr)

    def test_il_lanciatore_e_nel_codice_sigillato(self):
        # #142 (prova positiva dal lanciatore, 23/11; protezione #95 non portata nel percorso nuovo): il lanciatore
        # è caricato in ogni verifica, quindi sta nel codice sigillato e si controlla prima degli import
        self.assertIn("brain/laboratorio/esecuzione/avvio.py", EV.impronte_codice(self.dir))

    def test_positivo_completo_dal_lanciatore(self):
        # #142, DGS-18 Q4: la corsa ORDINARIA intera, dal lanciatore isolato ai due registri canonici e al rapporto,
        # in un repository git con un remoto finto, con ancora e controllo dell'ambiente accesi come nel codice
        import os
        import subprocess
        remoto = Path(self._t.name + "-remoto.git")
        self.addCleanup(shutil.rmtree, remoto, True)
        g = ["git", "-C", str(self.dir), "-c", "user.name=t", "-c", "user.email=t@invalid"]
        subprocess.run(["git", "init", "-q", "--bare", str(remoto)], check=True)
        subprocess.run(["git", "init", "-q", str(self.dir)], check=True)
        subprocess.run(g + ["checkout", "-q", "-b", "principale"], check=True)
        subprocess.run(g + ["remote", "add", "origin", str(remoto)], check=True)
        registro, riserva = self.dir / EV.REL_REGISTRO_PROVE, self.dir / EV.REL_RISERVA
        S.sigilla(registro, "H-T127", self.scheda, ["V-T"], ORA, codice=EV.impronte_codice(self.dir))
        RV.crea(riserva, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        RV.prenota(riserva, "P1", "H-T127", LETTURA, FINE, S.impronta(self.scheda), ORA)
        subprocess.run(g + ["add", "-A"], check=True)
        subprocess.run(g + ["commit", "-q", "-m", "sigillo e prenotazione"], check=True)
        subprocess.run(g + ["push", "-q", "-u", "origin", "principale"], check=True, capture_output=True)
        rapporto = Path(self._t.name + "-rapporto.txt")
        self.addCleanup(lambda: rapporto.unlink() if rapporto.exists() else None)
        argomenti = ["--scheda", str(self.scheda), "--registro", EV.REL_REGISTRO_PROVE, "--riserva", EV.REL_RISERVA,
                     "--prenotazione", "P1", "--cache", str(CACHE["cache"]), "--cache-sviluppo", str(CACHE["sviluppo"]),
                     "--rapporto", str(rapporto), "--ora", ORA]
        r = self.avvia(*argomenti)
        self.assertEqual(r.returncode, 0, r.stderr[-600:])
        uscita = json.loads(r.stdout)
        self.assertEqual((uscita["esito_tecnico"], uscita["esito"]), ("completata", "promossa"))
        rec = RV.record_esito(riserva, "P1")
        self.assertEqual(rec["impronta_impegno"], uscita["impronta_impegno"])
        self.assertEqual(rapporto.read_bytes(), EV.rapporto_da_record(rec).encode("utf-8"))
        self.assertEqual([e["ruolo"] for e in S.leggi(registro)["esecuzioni"]], ["sviluppo", "verifica", "esito"])
        subprocess.run(g + ["add", "-A"], check=True)                      # il titolare pubblica i registri
        subprocess.run(g + ["commit", "-q", "-m", "esito P1"], check=True)
        subprocess.run(g + ["push", "-q"], check=True, capture_output=True)
        prima = riserva.read_bytes()
        r2 = self.avvia(*argomenti)                                       # ripresa identica: nessuna lettura
        self.assertEqual(r2.returncode, 0, r2.stderr[-600:])
        self.assertEqual(json.loads(r2.stdout)["esito_tecnico"], "rapporto rigenerato")
        self.assertEqual(riserva.read_bytes(), prima)

    def test_con_i_controlli_superati_passa_all_esecutore(self):
        self.sigilla()
        r = self.avvia("--scheda", str(self.scheda), "--registro", "x", "--riserva", "x", "--prenotazione", "P1",
                       "--cache", "x", "--cache-sviluppo", "x", "--rapporto", str(self.dir / "r.txt"), "--ora", ORA)
        self.assertNotIn("FERMO prima di importare", r.stderr)
        self.assertNotIn("avvio.py verifica", r.stderr)                 # l'esecutore riconosce il lanciatore
        self.assertIn("RIFIUTATA", r.stderr)                            # poi si ferma sui registri finti


class TestSeduteSenzaOperazioni(Percorso):
    """DGS-17: una seduta con i dati completi ma senza operazioni è una coppia (0, 0) nel record, distinta da una seduta
    con dati mancanti (che il manifesto ferma prima dell'autorizzazione). Il 25% delle giornate è neutro (nessun
    segnale). Si ricontrolla anche la media come somma degli S diviso somma dei K, dal solo record."""

    @classmethod
    def setUpClass(cls):
        cls._t = tempfile.TemporaryDirectory()
        base = Path(cls._t.name)
        cls.cache, cls.cache_sv = base / "cache", CACHE["sviluppo"]
        cls.vere = M.scrivi(cls.cache, LETTURA, FINE, 0.6, 21, p_neutra=0.25)

    @classmethod
    def tearDownClass(cls):
        cls._t.cleanup()

    def test_coppie_zero_e_riconciliazione_dal_record(self):
        from fractions import Fraction
        scheda = self.prepara()
        r = self.esegui(scheda)
        rec = RV.record_esito(self.riserva, "P1")
        coppie = rec["coppie"]
        neutre = sorted(g.isoformat() for g, x in self.vere.items() if x is None and INIZIO <= g <= FINE)
        self.assertGreater(len(neutre), 150)
        self.assertEqual([c[0] for c in coppie if c[2] == 0], neutre)          # K = 0 proprio nelle neutre
        self.assertTrue(all(c[1] == 0 for c in coppie if c[2] == 0))
        self.assertEqual(len({c[0] for c in coppie}), 1000)                    # date uniche
        v = rec["verdetto"]
        self.assertEqual((v["sedute"], v["sedute_attive"], v["trade"]), (1000, 1000 - len(neutre), 1000 - len(neutre)))
        esatta = sum(Fraction(c[1]) for c in coppie) / sum(c[2] for c in coppie)
        self.assertEqual(v["media"], float(esatta))                           # somma degli S / somma dei K
        self.assertEqual(r["esito"], v["esito"])


if __name__ == "__main__":
    unittest.main()
