"""Test dell'esportazione redatta per i revisori (governance/esporta_redatto.py), scritti PRIMA del codice.
Richiesta del DGS (DGS-10, difetto #43): il pacchetto non deve contenere dati personali.
Uso: python3 -s -B -W error -m unittest brain.governance.test_esporta_redatto
"""
import csv
import hashlib
import io
import subprocess
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.governance import esporta_redatto as X                    # noqa: E402

SOST = [("Mario Rossi", "<titolare>"), ("mrossi-dot", "<utente-github>"), ("mario", "<utente>")]


class TestEsporta(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.dir = Path(self._t.name)
        self.repo = self.dir / "repo"
        self.repo.mkdir()
        g = ["git", "-C", str(self.repo), "-c", "user.name=t", "-c", "user.email=t@invalid"]
        (self.repo / "a.md").write_text("Autore: Mario Rossi (GitHub mrossi-dot), percorso /Users/mario/Downloads/x.\n"
                                        "MARIO e /Users/qualcuno/y\n", encoding="utf-8")
        (self.repo / "b.bin").write_bytes(bytes(range(256)))
        (self.repo / "dir").mkdir()
        (self.repo / "dir" / "c.py").write_text("x = 1\n", encoding="utf-8")
        subprocess.run(g + ["init", "-q"], check=True)
        subprocess.run(g + ["add", "."], check=True)
        subprocess.run(g + ["commit", "-q", "-m", "primo"], check=True)
        (self.repo / "non_committato.md").write_text("Mario Rossi\n", encoding="utf-8")   # non deve entrare
        self.g = g

    def tearDown(self):
        self._t.cleanup()

    def leggi(self, zp):
        with zipfile.ZipFile(zp) as z:
            return {n: z.read(n) for n in z.namelist()}

    def test_redige_e_scrive_il_manifest(self):
        zp = self.dir / "fuori" / "pacchetto.zip"
        r = X.esporta(self.repo, "HEAD", zp, SOST)
        f = self.leggi(zp)
        testo = f["a.md"].decode("utf-8")
        self.assertNotIn("Mario", testo)
        self.assertNotIn("mario", testo.lower())
        self.assertIn("<titolare>", testo)
        self.assertIn("<utente-github>", testo)
        self.assertIn("/Users/<utente>/Downloads/x", testo)
        self.assertIn("/Users/<utente>/y", testo)                                # anche altri nomi utente nei percorsi
        self.assertEqual(f["b.bin"], bytes(range(256)))
        self.assertNotIn("non_committato.md", f)                                  # solo il contenuto del commit
        righe = list(csv.DictReader(io.StringIO(f["MANIFEST.tsv"].decode("utf-8")), delimiter="\t"))
        per = {x["percorso"]: x for x in righe}
        self.assertEqual(set(per), {"a.md", "b.bin", "dir/c.py"})
        self.assertEqual(per["a.md"]["sha256"], hashlib.sha256(f["a.md"]).hexdigest())
        self.assertEqual(per["a.md"]["redatto"], "sì")
        self.assertEqual(per["dir/c.py"]["redatto"], "no")
        self.assertEqual(per["dir/c.py"]["sha256"], per["dir/c.py"]["sha256_originale"])
        self.assertNotEqual(per["a.md"]["sha256"], per["a.md"]["sha256_originale"])
        self.assertIn("LEGGIMI-PACCHETTO.md", f)
        commit = subprocess.run(["git", "-C", str(self.repo), "rev-parse", "HEAD"], capture_output=True,
                                text=True).stdout.strip()
        self.assertIn(commit, f["LEGGIMI-PACCHETTO.md"].decode("utf-8"))
        self.assertEqual((r["file"], r["redatti"]), (3, 1))
        for nome, contenuto in f.items():                                         # niente dati nemmeno nei file aggiunti
            self.assertNotIn(b"Mario", contenuto, nome)
            self.assertNotIn(b"mrossi", contenuto, nome)

    def test_rifiuta_se_resta_un_dato_personale(self):
        (self.repo / "d.bin").write_bytes(b"\xff\xfe binario con mario dentro \x00")
        subprocess.run(self.g + ["add", "d.bin"], check=True)
        subprocess.run(self.g + ["commit", "-q", "-m", "binario"], check=True)
        zp = self.dir / "fuori" / "p.zip"
        with self.assertRaises(ValueError) as e:
            X.esporta(self.repo, "HEAD", zp, SOST)
        self.assertIn("d.bin", str(e.exception))
        self.assertFalse(zp.exists())

    def test_rifiuta_un_nome_di_file_con_un_dato_personale(self):
        (self.repo / "note_di_mario.md").write_text("pulito\n", encoding="utf-8")
        subprocess.run(self.g + ["add", "note_di_mario.md"], check=True)
        subprocess.run(self.g + ["commit", "-q", "-m", "nome"], check=True)
        with self.assertRaises(ValueError) as e:
            X.esporta(self.repo, "HEAD", self.dir / "fuori" / "p.zip", SOST)
        self.assertIn("note_di_mario.md", str(e.exception))

    def test_destinazione_fuori_dal_repository(self):
        with self.assertRaises(ValueError):
            X.esporta(self.repo, "HEAD", self.repo / "p.zip", SOST)

    def test_riga_di_comando_non_stampa_i_dati(self):
        zp = self.dir / "fuori" / "p.zip"
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = X.main(["--repo", str(self.repo), "--uscita", str(zp), "--sostituisci", "Mario Rossi=<titolare>",
                         "--sostituisci", "mrossi-dot=<utente-github>", "--sostituisci", "mario=<utente>"])
        self.assertEqual(rc, 0)
        self.assertTrue(zp.exists())
        self.assertNotIn("Mario", buf.getvalue())
        self.assertNotIn("mario", buf.getvalue().lower().replace("<utente>", ""))
        self.assertEqual(X.main(["--repo", str(self.repo), "--uscita", str(self.dir / "q.zip"), "--sostituisci", "senza-uguale"]), 2)
        self.assertEqual(X.main(["--repo", str(self.repo), "--uscita", str(self.dir / "q.zip"), "--sostituisci", "Mario Rossi=<titolare>",
                                 "--sostituisci", "mrossi-dot=<utente-github>", "--sostituisci", "mario=<utente>",
                                 "--sostituisci", "=<vuoto>"]), 2)
        self.assertFalse((self.dir / "q.zip").exists())


if __name__ == "__main__":
    unittest.main()
