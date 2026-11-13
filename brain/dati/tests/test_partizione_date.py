"""Partizione per DATE in blocchi con embargo (DA-26; rilievo di Gemini G-20261113-01: la divisione 70/30 per numero
di candele non è una regola decisa prima, dipende da quanti dati arrivano).
Uso (dalla radice del repository): python3 -s -B -W error -m unittest brain.dati.tests.test_partizione_date
"""
import hashlib
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal as D
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.dati.pipeline import partizione_date as PD                 # noqa: E402
from brain.dati.pipeline.models import Candle                         # noqa: E402

UTC = timezone.utc
Q = timedelta(minutes=15)


def candele(da, giorni, per_giorno=4):
    """`per_giorno` candele da 15 minuti a partire dalle 10:00 UTC di ogni giorno."""
    out = []
    for g in range(giorni):
        t = datetime(da.year, da.month, da.day, 10, tzinfo=UTC) + timedelta(days=g)
        for i in range(per_giorno):
            p = D("2650") + g + D(i) / 10
            out.append(Candle("XAUUSD", "15m", t + i * Q, t + (i + 1) * Q, p, p + 1, p - 1, p, D("1")))
    return out


def partizione(*blocchi, embargo=1):
    return {"schema": PD.SCHEMA, "simbolo": "XAUUSD", "embargo_giorni": embargo,
            "blocco": [{"nome": n, "ruolo": r, "inizio": i, "fine": f} for n, r, i, f in blocchi]}


TRE = partizione(("verifica_vecchia", "verifica", "2026-01-01", "2026-01-04"),
                 ("sviluppo", "sviluppo", "2026-01-05", "2026-01-08"),
                 ("verifica_recente", "verifica", "2026-01-09", "2026-01-11"))


class TestValidazione(unittest.TestCase):
    def errore(self, p, testo):
        with self.assertRaises(ValueError) as e:
            PD.valida(p)
        self.assertIn(testo, str(e.exception))

    def test_partizione_valida(self):
        b = PD.valida(TRE)
        self.assertEqual([x["nome"] for x in b], ["verifica_vecchia", "sviluppo", "verifica_recente"])
        self.assertEqual(b[0]["inizio_utc"], datetime(2026, 1, 1, tzinfo=UTC))
        self.assertEqual(b[0]["fine_utc"], datetime(2026, 1, 4, tzinfo=UTC))

    def test_embargo_troppo_corto(self):
        """Fra la fine (esclusa) di un blocco e l'inizio del successivo servono almeno `embargo_giorni` giorni."""
        self.errore(partizione(("a", "sviluppo", "2026-01-01", "2026-01-05"), ("b", "verifica", "2026-01-05", "2026-01-09")),
                    "embargo")
        PD.valida(partizione(("a", "sviluppo", "2026-01-01", "2026-01-05"), ("b", "verifica", "2026-01-05", "2026-01-09"),
                             embargo=0))
        PD.valida(partizione(("a", "sviluppo", "2026-01-01", "2026-01-05"), ("b", "verifica", "2026-01-06", "2026-01-09")))

    def test_blocchi_sovrapposti_o_fuori_ordine(self):
        self.errore(partizione(("a", "sviluppo", "2026-01-01", "2026-01-09"), ("b", "verifica", "2026-01-05", "2026-01-12")),
                    "embargo")
        self.errore(partizione(("b", "verifica", "2026-01-10", "2026-01-12"), ("a", "sviluppo", "2026-01-01", "2026-01-05")),
                    "ordine")

    def test_campi_non_validi(self):
        self.errore(dict(TRE, schema="altro/1"), "schema")
        self.errore(partizione(("a", "sviluppo", "2026-01-05", "2026-01-05"), ("b", "verifica", "2026-01-07", "2026-01-09")),
                    "inizio")
        self.errore(partizione(("a", "sviluppo", "2026-01-01", "2026-01-03"), ("a", "verifica", "2026-01-05", "2026-01-09")),
                    "nome")
        self.errore(partizione(("../x", "sviluppo", "2026-01-01", "2026-01-03"), ("b", "verifica", "2026-01-05", "2026-01-09")),
                    "nome")
        self.errore(partizione(("a", "test", "2026-01-01", "2026-01-03"), ("b", "verifica", "2026-01-05", "2026-01-09")),
                    "ruolo")
        self.errore(partizione(("a", "sviluppo", "2026-01-01", "2026-01-03"), ("b", "sviluppo", "2026-01-05", "2026-01-09")),
                    "verifica")
        self.errore(partizione(("a", "sviluppo", "2026-1-1", "2026-01-03"), ("b", "verifica", "2026-01-05", "2026-01-09")),
                    "data")
        self.errore(dict(TRE, embargo_giorni=-1), "embargo")
        self.errore(dict(TRE, embargo_giorni=True), "embargo")


class TestPartizione(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.dati, self.nonce = base / "partizioni" / "XAUUSD_15m_date", base / "fuori" / "nonce"
        self.cc = candele(datetime(2026, 1, 1, tzinfo=UTC), 11)          # 1–11 gennaio, 4 candele al giorno

    def tearDown(self):
        self.tmp.cleanup()

    def test_blocchi_embargo_e_sigilli(self):
        comm = PD.partiziona(self.cc, TRE, self.dati, self.nonce, partizione_sha256="ab" * 32)
        b = {x["nome"]: x for x in comm["blocchi"]}
        self.assertEqual({k: v["candele"] for k, v in b.items()},
                         {"verifica_vecchia": 12, "sviluppo": 12, "verifica_recente": 8})
        self.assertEqual(comm["candele_totali"], 44)
        self.assertEqual(comm["candele_escluse"], 12)                    # 4, 8 e 11 gennaio
        self.assertEqual(b["sviluppo"]["prima_utc"], "2026-01-05T10:00:00+00:00")
        self.assertEqual(b["sviluppo"]["ultima_utc"], "2026-01-07T11:00:00+00:00")
        self.assertNotIn("commitment_hash", b["sviluppo"])              # lo sviluppo non è sigillato
        self.assertIn("commitment_hash", b["verifica_recente"])
        self.assertEqual(comm["partizione_sha256"], "ab" * 32)
        self.assertEqual(comm["embargo_giorni"], 1)
        testo = (self.dati / "sviluppo.jsonl").read_text(encoding="utf-8")
        self.assertEqual(hashlib.sha256(testo.encode("utf-8")).hexdigest(), b["sviluppo"]["sha256"])
        nonce = (self.nonce / "sealed_nonce.secret").read_text(encoding="utf-8").strip()
        v = (self.dati / "verifica_recente.jsonl").read_text(encoding="utf-8")
        self.assertEqual(hashlib.sha256((nonce + v).encode("utf-8")).hexdigest(), b["verifica_recente"]["commitment_hash"])
        self.assertEqual(json.loads((self.dati / "commitment.json").read_text(encoding="utf-8")), comm)
        self.assertFalse((self.dati / "sealed_nonce.secret").exists())  # il nonce non sta con i dati
        self.assertTrue(PD.verifica(self.dati, self.nonce / "sealed_nonce.secret", TRE, "ab" * 32)["valido"])

    def test_blocco_manomesso_scoperto(self):
        PD.partiziona(self.cc, TRE, self.dati, self.nonce, partizione_sha256="00" * 32)
        f = self.dati / "verifica_vecchia.jsonl"
        f.write_text(f.read_text(encoding="utf-8").replace("2650", "2651", 1), encoding="utf-8")
        esito = PD.verifica(self.dati, self.nonce / "sealed_nonce.secret", TRE, "00" * 32)
        self.assertFalse(esito["valido"])
        self.assertEqual(esito["blocchi"]["verifica_vecchia"], {"sha256": False, "commitment": False})
        self.assertEqual(esito["blocchi"]["verifica_recente"], {"sha256": True, "commitment": True})
        PD.partiziona(self.cc, TRE, self.dati / "altra", self.nonce / "altro", partizione_sha256="00" * 32)
        self.assertEqual(PD.verifica(self.dati / "altra", self.nonce / "altro" / "sealed_nonce.secret", TRE,
                                     "00" * 32)["blocchi"]
                         ["sviluppo"], {"sha256": True, "commitment": None})

    def test_nonce_sbagliato_scoperto(self):
        """Dati intatti ma nonce diverso: lo SHA-256 torna, il sigillo no, e la verifica non è valida
        (mutante P11 sopravvissuto al primo giro: la verifica guardava solo lo SHA-256)."""
        PD.partiziona(self.cc, TRE, self.dati, self.nonce, partizione_sha256="00" * 32)
        altro = self.nonce.parent / "altro.secret"
        altro.write_text("0" * 64 + "\n", encoding="utf-8")
        esito = PD.verifica(self.dati, altro, TRE, "00" * 32)
        self.assertFalse(esito["valido"])
        self.assertEqual(esito["blocchi"]["verifica_recente"], {"sha256": True, "commitment": False})
        self.assertEqual(esito["blocchi"]["sviluppo"], {"sha256": True, "commitment": None})

    def test_ruoli_declassati_nel_commitment_scoperti(self):
        """Rilievo di Gemini G3-02 (riprodotto da Claude): dati di verifica alterati, TUTTI i blocchi di verifica
        declassati a «sviluppo» in commitment.json con SHA-256 ricalcolato e nonce finto. La verifica confronta i
        blocchi con la partizione (il file TOML pubblicato), quindi non è valida."""
        PD.partiziona(self.cc, TRE, self.dati, self.nonce, partizione_sha256="00" * 32)
        comm = json.loads((self.dati / "commitment.json").read_text(encoding="utf-8"))
        for b in comm["blocchi"]:
            if b["ruolo"] == "verifica":
                f = self.dati / f"{b['nome']}.jsonl"
                testo = f.read_text(encoding="utf-8").replace("2650", "2651", 1)
                f.write_text(testo, encoding="utf-8")
                b["ruolo"] = "sviluppo"
                b["sha256"] = hashlib.sha256(testo.encode("utf-8")).hexdigest()
                del b["commitment_hash"]
        (self.dati / "commitment.json").write_text(json.dumps(comm), encoding="utf-8")
        finto = self.nonce.parent / "finto.secret"
        finto.write_text("deadbeef\n", encoding="utf-8")
        esito = PD.verifica(self.dati, finto, TRE, "00" * 32)
        self.assertFalse(esito["valido"])
        self.assertFalse(esito["partizione"])
        # il sigillo dei blocchi di verifica (ruolo preso dalla partizione) è controllato comunque, e fallisce
        self.assertEqual(esito["blocchi"]["verifica_recente"]["commitment"], False)
        self.assertEqual(esito["blocchi"]["verifica_vecchia"]["commitment"], False)

    def test_partizione_o_protocollo_diversi_scoperti(self):
        PD.partiziona(self.cc, TRE, self.dati, self.nonce, partizione_sha256="00" * 32)
        nonce = self.nonce / "sealed_nonce.secret"
        self.assertTrue(PD.verifica(self.dati, nonce, TRE, "00" * 32)["valido"])
        self.assertFalse(PD.verifica(self.dati, nonce, TRE, "11" * 32)["valido"])          # file TOML diverso
        altra = json.loads(json.dumps(TRE))
        altra["blocco"][2]["fine"] = "2026-01-12"
        self.assertFalse(PD.verifica(self.dati, nonce, altra, "00" * 32)["valido"])        # confini diversi
        comm = json.loads((self.dati / "commitment.json").read_text(encoding="utf-8"))
        comm["protocol"] = "ALTRO"
        (self.dati / "commitment.json").write_text(json.dumps(comm), encoding="utf-8")
        self.assertFalse(PD.verifica(self.dati, nonce, TRE, "00" * 32)["valido"])

    def test_nonce_esistente_non_si_sovrascrive(self):
        """Un nuovo nonce renderebbe inverificabile il sigillo già pubblicato: ci si ferma, prima di scrivere."""
        PD.partiziona(self.cc, TRE, self.dati, self.nonce, partizione_sha256="00" * 32)
        prima = (self.nonce / "sealed_nonce.secret").read_text(encoding="utf-8")
        with self.assertRaises(FileExistsError):
            PD.partiziona(self.cc, TRE, self.dati / "bis", self.nonce, partizione_sha256="00" * 32)
        self.assertEqual((self.nonce / "sealed_nonce.secret").read_text(encoding="utf-8"), prima)
        self.assertFalse((self.dati / "bis").exists())

    def test_blocco_vuoto_ferma(self):
        p = partizione(("sviluppo", "sviluppo", "2026-01-01", "2026-01-05"),
                       ("verifica", "verifica", "2026-02-01", "2026-02-05"))
        with self.assertRaises(ValueError) as e:
            PD.partiziona(self.cc, p, self.dati, self.nonce, partizione_sha256="00" * 32)
        self.assertIn("verifica", str(e.exception))
        self.assertFalse((self.nonce / "sealed_nonce.secret").exists())

    def test_simbolo_diverso_ferma(self):
        with self.assertRaises(ValueError):
            PD.partiziona(self.cc, dict(TRE, simbolo="EURUSD"), self.dati, self.nonce, partizione_sha256="00" * 32)

    def test_leggi_file_toml(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "p.toml"
            f.write_text('schema = "partizione-date/1"\nsimbolo = "XAUUSD"\nembargo_giorni = 1\n\n'
                         '[[blocco]]\nnome = "sviluppo"\nruolo = "sviluppo"\ninizio = "2026-01-01"\nfine = "2026-01-05"\n\n'
                         '[[blocco]]\nnome = "verifica"\nruolo = "verifica"\ninizio = "2026-01-06"\nfine = "2026-01-09"\n',
                         encoding="utf-8")
            p, sha = PD.leggi(f)
            self.assertEqual(sha, hashlib.sha256(f.read_bytes()).hexdigest())
            self.assertEqual(len(PD.valida(p)), 2)


if __name__ == "__main__":
    unittest.main()
