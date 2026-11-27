"""Test del manifesto dei dati di una finestra (laboratorio/esecuzione/manifesto.py) e del controllo dei byte nel
caricatore. DGS-14 Q1 e DGS-15 punto 3, 22/11/2026. Scritti PRIMA del codice. Solo dati e registri inventati.

- L'insieme ATTESO (mercato, lato, giorno, comprese le date accessorie) si ricava dal calendario della finestra.
- Si confronta con il registro dello scaricamento: un giorno omesso, una voce doppia, un lato sbagliato emergono
  anche quando i file presenti hanno l'impronta giusta.
- I giorni in quarantena restano nell'elenco con il loro stato.
- Il caricatore verifica l'impronta dei byte che passa al decodificatore, file per file.
Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_manifesto
"""
import csv
import hashlib
import lzma
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.dati.pipeline import dukascopy as DK                    # noqa: E402
from brain.laboratorio.esecuzione import caricatore as C            # noqa: E402
from brain.laboratorio.esecuzione import manifesto as MF            # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S               # noqa: E402

CAMPI = ("ora_utc", "giorno", "lato", "url", "http", "esito", "byte", "sha256", "tentativi")
ORA = "2026-11-22T10:00:00Z"


def bi5(base):
    return lzma.compress(DK.RECORD.pack(480 * 60, base, base + 10, base - 10, base + 20, 1.0), format=lzma.FORMAT_ALONE)


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Cache(unittest.TestCase):
    """Una cache inventata di 7 giorni (02–08/01/2024, con il fine settimana vuoto) e i due registri coerenti."""
    GIORNI = [date(2024, 1, d) for d in range(2, 9)]

    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.cache = Path(self._t.name) / "cache"
        self.righe = {"BID": [], "ASK": []}
        for lato, cartella, base in (("BID", "XAUUSD", 2000000), ("ASK", "XAUUSD_ASK", 2000300)):
            d = self.cache / cartella
            d.mkdir(parents=True)
            for g in self.GIORNI:
                corpo = b"" if g.weekday() >= 5 else bi5(base + g.day)
                (d / f"{g.isoformat()}.bi5").write_bytes(corpo)
                self.righe[lato].append({"ora_utc": ORA, "giorno": g.isoformat(), "lato": lato,
                                         "url": DK.url_giorno("XAUUSD", g, lato), "http": 200,
                                         "esito": "vuoto-200" if not corpo else "dati", "byte": len(corpo),
                                         "sha256": sha(corpo), "tentativi": 1})
        self.scrivi_registri()

    def tearDown(self):
        self._t.cleanup()

    def rifai(self):
        self._t.cleanup()
        self.setUp()

    def scrivi_registri(self):
        for lato, righe in self.righe.items():
            with open(self.cache / f"registro_scaricamento_XAUUSD_{lato}.csv", "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=CAMPI)
                w.writeheader()
                w.writerows(righe)

    def manifesto(self, inizio=date(2024, 1, 2), fine=date(2024, 1, 8), **k):
        return MF.manifesto(self.cache, "XAUUSD", inizio, fine, **k)


class TestInsiemeAtteso(unittest.TestCase):
    def test_ogni_giorno_di_calendario_per_lato_e_date_accessorie(self):
        a = MF.insieme_atteso("XAUUSD", date(2024, 1, 5), date(2024, 1, 8))
        self.assertEqual(len(a), 8)                                     # 4 giorni × 2 lati, fine settimana compreso
        self.assertEqual(a[0], ("XAUUSD", "ASK", "2024-01-05"))
        self.assertEqual(a, sorted(a))
        b = MF.insieme_atteso("XAUUSD", date(2024, 1, 5), date(2024, 1, 8), accessorie=2)
        self.assertEqual(len(b), 12)
        self.assertIn(("XAUUSD", "BID", "2024-01-03"), b)
        with self.assertRaises(ValueError):
            MF.insieme_atteso("XAUUSD", date(2024, 1, 8), date(2024, 1, 5))
        with self.assertRaises(ValueError):
            MF.insieme_atteso("XAUUSD", date(2024, 1, 5), date(2024, 1, 8), accessorie=-1)


class TestConfronto(Cache):
    def test_registro_coerente(self):
        m = self.manifesto()
        self.assertEqual(m["anomalie"], [])
        self.assertEqual(len(m["elenco"]), 14)
        self.assertEqual(m["elenco"][0], ["XAUUSD", "ASK", "2024-01-02", "dati",
                                          sha((self.cache / "XAUUSD_ASK" / "2024-01-02.bi5").read_bytes())])
        sabato = [x for x in m["elenco"] if x[1] == "BID" and x[2] == "2024-01-06"][0]
        self.assertEqual(sabato[3:], ["nessun dato", sha(b"")])
        self.assertEqual(m["impronta_elenco"], MF.impronta_elenco(m["elenco"]))
        self.assertEqual(len(m["registri"]), 2)                       # istantanea dei due registri: nome e SHA-256
        self.assertEqual(MF.attese(m), {(x[1], x[2]): x[4] for x in m["elenco"]})

    def test_giorno_omesso_con_impronte_giuste(self):
        del self.righe["ASK"][3]                                       # 05/01 ASK: il file c'è, la riga no
        self.scrivi_registri()
        self.assertEqual(self.manifesto()["anomalie"], ["omesso: XAUUSD ASK 2024-01-05"])

    # D-59 (A1, DGS-18 Q2): le righe restano tutte; il manifesto unifica solo i doppioni IDENTICI (indirizzo, classe del
    # contenuto, byte, impronta) e li conta come anomalia di processo nella traccia «doppioni»; i discordanti bloccano.
    # Prima di D-59 ogni doppione bloccava (test sostituito: test_voce_doppia).
    def test_doppione_identico_unificato_con_traccia(self):
        pulito = self.manifesto()
        copia = dict(self.righe["BID"][1], ora_utc="2026-11-16T03:00:00Z", tentativi=2)   # differenze amministrative
        self.righe["BID"].append(copia)
        self.scrivi_registri()
        m = self.manifesto()
        self.assertEqual(m["anomalie"], [])
        self.assertEqual((m["elenco"], m["impronta_elenco"]), (pulito["elenco"], pulito["impronta_elenco"]))
        self.assertEqual(m["doppioni"], [{"lato": "BID", "giorno": "2024-01-03", "righe": 2,
                                          "sha256": self.righe["BID"][1]["sha256"], "esiti": ["dati"]}])
        self.assertEqual(pulito["doppioni"], [])

    def test_tre_righe_identiche_e_osservazione_dalla_cache(self):
        # «in-cache-non-registrato» dice COME è stato osservato il file, non che cosa contiene (DGS-18 Q2): stessa classe
        r = self.righe["ASK"][2]
        self.righe["ASK"] += [dict(r, esito="in-cache-non-registrato", http=""), dict(r, ora_utc="2026-11-16T04:00:00Z")]
        self.scrivi_registri()
        m = self.manifesto()
        self.assertEqual(m["anomalie"], [])
        self.assertEqual(m["doppioni"], [{"lato": "ASK", "giorno": "2024-01-04", "righe": 3, "sha256": r["sha256"],
                                          "esiti": ["dati", "in-cache-non-registrato"]}])
        self.assertEqual([x for x in m["elenco"] if x[1] == "ASK" and x[2] == "2024-01-04"][0][3], "dati")

    def test_voce_doppia_discordante_blocca(self):
        r = self.righe["BID"][1]
        altra = sha(b"altro")
        for nome, diversa in (("impronta", dict(r, sha256=altra)), ("byte", dict(r, byte=int(r["byte"]) + 1)),
                              ("impronta e byte", dict(r, sha256=altra, byte=5))):
            with self.subTest(diversa=nome):
                self.rifai()
                self.righe["BID"].append(diversa)
                self.scrivi_registri()
                m = self.manifesto()
                self.assertEqual(m["anomalie"], ["voce doppia: XAUUSD BID 2024-01-03 (2 righe valide, discordanti)"])
                self.assertEqual(m["doppioni"], [])
        self.rifai()
        sab = self.righe["BID"][4]                                       # sabato: «vuoto-200»; un 404 è un'altra classe
        self.righe["BID"].append(dict(sab, esito="404", http=404))
        self.scrivi_registri()
        self.assertEqual(self.manifesto()["anomalie"], ["voce doppia: XAUUSD BID 2024-01-06 (2 righe valide, discordanti)"])

    def test_passaggio_vuoto_dati_blocca_con_regola_di_revisione(self):
        # come dopo --riprova-vuoti: prima «vuoto-200», poi «dati» per lo stesso giorno: nuova osservazione discordante
        sab = self.righe["BID"][4]
        corpo = bi5(2000006)
        self.righe["BID"].append(dict(sab, esito="dati", byte=len(corpo), sha256=sha(corpo)))
        self.scrivi_registri()
        self.assertEqual(self.manifesto()["anomalie"],
                         ["voce doppia: XAUUSD BID 2024-01-06 (2 righe valide, passaggio vuoto → dati: serve una "
                          "regola di revisione esplicita)"])

    def test_lato_sbagliato_nel_registro_o_nell_indirizzo(self):
        self.righe["BID"][2]["url"] = DK.url_giorno("XAUUSD", date(2024, 1, 4), "ASK")
        self.scrivi_registri()
        self.assertEqual(self.manifesto()["anomalie"], ["lato sbagliato: XAUUSD BID 2024-01-04 (indirizzo ASK)",
                                                        "omesso: XAUUSD BID 2024-01-04"])   # la riga scartata lascia il giorno scoperto
        self.rifai()
        riga = dict(self.righe["ASK"][2], lato="ASK")
        self.righe["BID"][2] = riga                                    # riga ASK finita nel registro BID
        self.scrivi_registri()
        an = self.manifesto()["anomalie"]
        self.assertIn("lato sbagliato: riga ASK nel registro BID (2024-01-04)", an)
        self.assertIn("omesso: XAUUSD BID 2024-01-04", an)

    def test_altro_mercato_e_esiti_non_validi(self):
        self.righe["BID"][1]["url"] = DK.url_giorno("XAGUSD", date(2024, 1, 3), "BID")
        self.righe["ASK"][1]["esito"] = "http-403"
        self.scrivi_registri()
        an = self.manifesto()["anomalie"]
        self.assertIn("mercato sbagliato: XAUUSD BID 2024-01-03 (indirizzo di un altro mercato)", an)
        self.assertIn("omesso: XAUUSD ASK 2024-01-03", an)              # una riga http-403 non è un dato

    def test_indirizzo_di_un_altro_dominio_o_di_un_altra_data(self):
        # #147 (R19-07a): l'indirizzo deve essere ESATTAMENTE quello atteso per mercato, lato e giorno
        giusto = self.righe["BID"][2]["url"]
        self.righe["BID"][2]["url"] = "https://evil.invalid/" + giusto.split("/", 3)[3]
        self.scrivi_registri()
        self.assertEqual(self.manifesto()["anomalie"], ["indirizzo diverso da quello atteso: XAUUSD BID 2024-01-04",
                                                        "omesso: XAUUSD BID 2024-01-04"])
        self.rifai()
        self.righe["BID"][2]["url"] = DK.url_giorno("XAUUSD", date(2019, 5, 5), "BID")   # un altro giorno
        self.scrivi_registri()
        self.assertEqual(self.manifesto()["anomalie"], ["indirizzo diverso da quello atteso: XAUUSD BID 2024-01-04",
                                                        "omesso: XAUUSD BID 2024-01-04"])

    def test_impronta_non_valida(self):
        # #147 (R19-07b): una riga valida senza un'impronta di 64 cifre esadecimali non vale; prima l'autorizzazione
        # consumava la finestra e solo la lettura dava «file difforme»
        for cattiva in ("", "abc", "G" * 64, "A" * 64):
            self.rifai()
            self.righe["BID"][2]["sha256"] = cattiva
            self.scrivi_registri()
            self.assertEqual(self.manifesto()["anomalie"], ["impronta non valida: XAUUSD BID 2024-01-04",
                                                            "omesso: XAUUSD BID 2024-01-04"], cattiva)

    def test_righe_rovinate_e_riscaricate(self):
        r = dict(self.righe["BID"][1], esito="rovinato-in-cache", sha256="0" * 64)
        self.righe["BID"].insert(1, r)                                 # prima rovinato, poi riscaricato: una sola valida
        self.scrivi_registri()
        self.assertEqual(self.manifesto()["anomalie"], [])

    def test_quarantena_dal_consuntivo(self):
        m = self.manifesto(quarantena={"2024-01-03": "ASK: 40% dei minuti mancanti nella fascia operativa"})
        q = [x for x in m["elenco"] if x[2] == "2024-01-03"]
        self.assertEqual([x[3] for x in q], ["quarantena", "quarantena"])
        self.assertEqual(m["quarantena"], {"2024-01-03": "ASK: 40% dei minuti mancanti nella fascia operativa"})
        self.assertNotEqual(m["impronta_elenco"], self.manifesto()["impronta_elenco"])


class TestByteAlDecodificatore(Cache):
    def setUp(self):
        super().setUp()
        self.scheda = Path(self._t.name) / "H-999.md"
        self.scheda.write_text("# H-999\n", encoding="utf-8")
        self.registro = Path(self._t.name) / "registro_prove.json"
        S.sigilla(self.registro, "H-999", self.scheda, ["V-T"], ORA)

    def carica(self, attese, inizio=date(2024, 1, 2), fine=date(2024, 1, 8)):
        return C.carica(self.cache / "XAUUSD", self.cache / "XAUUSD_ASK", inizio, fine, "sviluppo", self.registro,
                        "H-999", self.scheda, attese=attese)

    def test_byte_conformi(self):
        bid, ask, info = self.carica(MF.attese(self.manifesto()))
        self.assertEqual((len(bid), len(ask)), (5, 5))
        self.assertTrue(info["byte_verificati"])

    def test_i_byte_controllati_sono_quelli_decodificati(self):
        visti = []
        vero = DK.decodifica

        def spia(dati, giorno, scala):
            visti.append((giorno.isoformat(), sha(dati)))
            return vero(dati, giorno, scala)
        attese = MF.attese(self.manifesto())
        with mock.patch.object(DK, "decodifica", side_effect=spia):
            self.carica(attese)
        self.assertEqual(len(visti), 10)                                # 5 feriali × 2 lati (i vuoti non si decodificano)
        for giorno, h in visti:
            self.assertIn(h, (attese[("BID", giorno)], attese[("ASK", giorno)]))

    def test_file_difforme_dopo_il_manifesto(self):
        attese = MF.attese(self.manifesto())
        (self.cache / "XAUUSD_ASK" / "2024-01-04.bi5").write_bytes(bi5(2009999))   # sostituito dopo
        with self.assertRaisesRegex(C.FileDifforme, "ASK 2024-01-04"):
            self.carica(attese)

    def test_file_sparito_o_non_previsto(self):
        attese = MF.attese(self.manifesto())
        (self.cache / "XAUUSD" / "2024-01-05.bi5").unlink()
        with self.assertRaisesRegex(C.FileDifforme, "BID 2024-01-05"):
            self.carica(attese)
        self.rifai()
        attese = MF.attese(self.manifesto(fine=date(2024, 1, 7)))
        with self.assertRaisesRegex(C.FileDifforme, "2024-01-08"):     # giorno letto ma non nel manifesto
            self.carica(attese)

    def test_senza_attese_come_prima(self):
        bid, ask, info = self.carica(None)
        self.assertFalse(info["byte_verificati"])
        self.assertEqual(len(bid), 5)


if __name__ == "__main__":
    unittest.main()
