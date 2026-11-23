"""Test della diagnosi del manifesto sui registri dello scaricamento (laboratorio/studi/diagnosi_manifesto.py),
23/11/2026. Scritti PRIMA del codice. Solo dati e registri inventati (mercato sintetico), nessuna rete.

Perché: il manifesto (DGS-14 Q1) non è mai stato confrontato con i registri VERI. Il BID fino al 07/06/2009 è stato
scaricato prima che esistesse il registro per giorno, e `--riprova-vuoti` aggiunge una seconda riga valida per lo
stesso giorno: in entrambi i casi il manifesto bloccherebbe ogni finestra di quegli anni. La diagnosi lo dice prima,
contando le anomalie per tipo, lato e anno, e controllando che i byte in cache abbiano l'impronta del registro.
Stampa e scrive SOLO conteggi e date: mai impronte, mai prezzi.
Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_diagnosi_manifesto
"""
import csv
import io
import json
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.laboratorio.studi import diagnosi_manifesto as DM        # noqa: E402
from brain.laboratorio.tests import mercato_sintetico as MS         # noqa: E402

INIZIO, FINE = date(2023, 12, 27), date(2024, 1, 5)


class TestDiagnosi(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.cache = Path(self._t.name) / "cache"
        MS.scrivi(self.cache, INIZIO, FINE, 0.5, 7)

    def tearDown(self):
        self._t.cleanup()

    def registro(self, lato):
        return self.cache / f"registro_scaricamento_XAUUSD_{lato}.csv"

    def righe(self, lato):
        with open(self.registro(lato), encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def riscrivi(self, lato, righe):
        with open(self.registro(lato), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=MS.CAMPI)
            w.writeheader()
            w.writerows(righe)

    def test_registri_coerenti_nessuna_anomalia(self):
        d = DM.diagnosi(self.cache, "XAUUSD", INIZIO, FINE)
        self.assertTrue(d["pulito"])
        self.assertEqual(d["giorni_attesi"], {"ASK": 10, "BID": 10})
        self.assertEqual((d["per_tipo"], d["voci_doppie_esiti"], d["date"]), ({}, {}, {}))
        self.assertEqual(d["byte_controllati"], {"ASK": 10, "BID": 10})

    def test_giorno_omesso_contato_per_lato_e_anno(self):
        self.riscrivi("BID", [r for r in self.righe("BID") if r["giorno"] != "2024-01-03"])
        d = DM.diagnosi(self.cache, "XAUUSD", INIZIO, FINE)
        self.assertFalse(d["pulito"])
        self.assertEqual(d["per_tipo"], {"omesso": {"BID": {"2024": 1}}})
        self.assertEqual(d["date"], {"omesso": ["BID 2024-01-03"]})

    def test_voce_doppia_con_la_combinazione_degli_esiti(self):
        # come dopo --riprova-vuoti: prima «vuoto-200», poi «dati» per lo stesso giorno e lato
        rr = self.righe("ASK")
        prima = dict(next(r for r in rr if r["giorno"] == "2023-12-28"), esito="vuoto-200", byte="0")
        errore = dict(prima, esito="http-503")                          # non valida: fuori dalla combinazione
        opposta = dict(prima, lato="BID")                               # lato sbagliato: fuori dalla combinazione
        self.riscrivi("ASK", [errore, prima, opposta] + rr)
        d = DM.diagnosi(self.cache, "XAUUSD", INIZIO, FINE)
        self.assertEqual(d["per_tipo"], {"voce doppia": {"ASK": {"2023": 1}}, "lato sbagliato": {"ASK": {"2023": 1}}})
        self.assertEqual(d["voci_doppie_esiti"], {"vuoto-200+dati": 1})

    def test_righe_non_valide_ignorate_come_nel_manifesto(self):
        rr = self.righe("BID")
        self.riscrivi("BID", [dict(rr[1], esito="http-503", byte="0")] + rr)
        self.assertTrue(DM.diagnosi(self.cache, "XAUUSD", INIZIO, FINE)["pulito"])

    def test_lato_e_mercato_sbagliati(self):
        rr = self.righe("BID")
        altra = dict(rr[2], lato="ASK")
        altro_mercato = dict(rr[3], url=rr[3]["url"].replace("/XAUUSD/", "/GBPJPY/"))
        self.riscrivi("BID", [r for r in rr if r["giorno"] not in (rr[2]["giorno"], rr[3]["giorno"])]
                      + [altra, altro_mercato])
        d = DM.diagnosi(self.cache, "XAUUSD", INIZIO, FINE)
        self.assertEqual(d["per_tipo"]["lato sbagliato"], {"BID": {"2023": 1}})
        self.assertEqual(d["per_tipo"]["mercato sbagliato"], {"BID": {"2023": 1}})
        self.assertEqual(d["per_tipo"]["omesso"], {"BID": {"2023": 2}})

    def test_byte_diversi_dal_registro_e_file_mancante(self):
        (self.cache / "XAUUSD" / "2024-01-02.bi5").write_bytes(b"altro")
        (self.cache / "XAUUSD_ASK" / "2024-01-04.bi5").unlink()
        d = DM.diagnosi(self.cache, "XAUUSD", INIZIO, FINE)
        self.assertEqual(d["per_tipo"], {"impronta diversa": {"BID": {"2024": 1}},
                                         "file mancante": {"ASK": {"2024": 1}}})
        self.assertEqual(d["byte_controllati"], {"ASK": 9, "BID": 10})

    def test_senza_controllo_dei_byte(self):
        (self.cache / "XAUUSD" / "2024-01-02.bi5").write_bytes(b"altro")
        d = DM.diagnosi(self.cache, "XAUUSD", INIZIO, FINE, byte=False)
        self.assertTrue(d["pulito"])
        self.assertEqual(d["byte_controllati"], {})

    def test_mai_impronte_ne_prezzi_nell_uscita(self):
        self.riscrivi("BID", [r for r in self.righe("BID") if r["giorno"] != "2024-01-03"])
        (self.cache / "XAUUSD_ASK" / "2024-01-02.bi5").write_bytes(b"altro")
        out = io.StringIO()
        j = Path(self._t.name) / "d.json"
        with redirect_stdout(out):
            codice = DM.main(["--cache", str(self.cache), "--inizio", INIZIO.isoformat(), "--fine", FINE.isoformat(),
                              "--json", str(j)])
        self.assertEqual(codice, 1)                                     # anomalie: codice 1
        for testo in (out.getvalue(), j.read_text(encoding="utf-8")):
            self.assertIsNone(re.search(r"[0-9a-f]{64}", testo))
            self.assertIsNone(re.search(r"\d+\.\d{2,}", testo))
        self.assertEqual(json.loads(j.read_text(encoding="utf-8"))["date"]["omesso"], ["BID 2024-01-03"])

    def test_riga_di_comando(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(DM.main(["--cache", str(self.cache), "--inizio", "2023-12-27", "--fine", "2024-01-05"]), 0)
            self.assertEqual(DM.main(["--cache", str(self.cache), "--inizio", "2024-01-05", "--fine", "2023-12-27"]), 2)
            (self.cache / "XAUUSD" / "2024-01-02.bi5").write_bytes(b"altro")
            self.assertEqual(DM.main(["--cache", str(self.cache), "--inizio", "2023-12-27", "--fine", "2024-01-05"]), 1)
            self.assertEqual(DM.main(["--cache", str(self.cache), "--inizio", "2023-12-27", "--fine", "2024-01-05",
                                      "--senza-byte"]), 0)
            self.assertEqual(DM.main(["--cache", str(self.cache / "niente"), "--inizio", "2023-12-27",
                                      "--fine", "2024-01-05"]), 2)


if __name__ == "__main__":
    unittest.main()
