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
        self.assertNotIn("non_committato.md", f)                                  # solo il contenuto del commit
        righe = list(csv.DictReader(io.StringIO(f["MANIFEST.tsv"].decode("utf-8")), delimiter="\t"))
        per = {x["percorso"]: x for x in righe}
        self.assertEqual(set(per), {"a.md", "dir/c.py"})        # R14: niente binari nel pacchetto di prova
        self.assertEqual(per["a.md"]["sha256"], hashlib.sha256(f["a.md"]).hexdigest())
        self.assertEqual(per["a.md"]["redatto"], "sì")
        self.assertEqual(per["dir/c.py"]["redatto"], "no")
        self.assertEqual(per["dir/c.py"]["sha256"], per["dir/c.py"]["sha256_originale"])
        self.assertNotEqual(per["a.md"]["sha256"], per["a.md"]["sha256_originale"])
        self.assertIn("LEGGIMI-PACCHETTO.md", f)
        commit = subprocess.run(["git", "-C", str(self.repo), "rev-parse", "HEAD"], capture_output=True,
                                text=True).stdout.strip()
        self.assertIn(commit, f["LEGGIMI-PACCHETTO.md"].decode("utf-8"))
        self.assertEqual((r["file"], r["redatti"]), (2, 1))
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

    def committa(self, nome, dati):
        f = self.repo / nome
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(dati)
        subprocess.run(self.g + ["add", nome], check=True)
        subprocess.run(self.g + ["commit", "-q", "-m", nome], check=True)

    def test_altre_codifiche_rifiutate(self):
        """#72 (revisione notturna): UTF-16 e latin-1 passavano come «binari» non controllabili."""
        for nome, dati in (("u16.txt", "Autore: Mario Rossi".encode("utf-16")),
                           ("lat.txt", "Relazione di José".encode("latin-1"))):
            with self.subTest(nome):
                self.committa(nome, dati)
                with self.assertRaises(ValueError) as e:
                    X.esporta(self.repo, "HEAD", self.dir / "fuori" / "p.zip", SOST + [("José", "<titolare>")])
                self.assertIn(nome, str(e.exception))
                subprocess.run(self.g + ["rm", "-q", nome], check=True)
                subprocess.run(self.g + ["commit", "-q", "-m", "via"], check=True)

    def test_forma_nfd_redatta(self):
        self.committa("nfd.md", "Autore: Jose\u0301 Rossi\n".encode("utf-8"))
        zp = self.dir / "fuori" / "p.zip"
        X.esporta(self.repo, "HEAD", zp, SOST + [("José", "<titolare>")])
        testo = self.leggi(zp)["nfd.md"].decode("utf-8")
        self.assertNotIn("Jos", testo)

    def test_archivi_annidati_rifiutati_o_esclusi(self):
        """#72: uno ZIP annidato con un nome dentro passava (contenuto compresso). Successo davvero: pacchetto DGS-05."""
        import io as _io
        buf = _io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("dentro.md", "Autore: Mario Rossi\n")
        self.committa("vecchio/pacchetto.zip", buf.getvalue())
        with self.assertRaises(ValueError) as e:
            X.esporta(self.repo, "HEAD", self.dir / "fuori" / "p.zip", SOST)
        self.assertIn("vecchio/pacchetto.zip", str(e.exception))
        zp = self.dir / "fuori" / "q.zip"
        r = X.esporta(self.repo, "HEAD", zp, SOST, escludi=["vecchio/pacchetto.zip"])
        f = self.leggi(zp)
        self.assertNotIn("vecchio/pacchetto.zip", f)
        self.assertIn("vecchio/pacchetto.zip", f["LEGGIMI-PACCHETTO.md"].decode("utf-8"))   # esclusione dichiarata
        self.assertEqual(r["esclusi"], 1)

    def test_percorsi_mac_nei_binari_rifiutati(self):
        """#84 (rilievo 10): un /Users/<nome> non dato al lancio, dentro un binario o un testo non UTF-8, passava."""
        self.committa("dati.bin", b"\x00\xff/Users/qualcuno/Library\x00")
        with self.assertRaises(ValueError) as ex:
            X.esporta(self.repo, "HEAD", self.dir / "fuori" / "p.zip", SOST)
        self.assertIn("dati.bin", str(ex.exception))

    def test_file_non_di_testo_rifiutati_salvo_esclusione(self):
        """R14-04, R14-05 (Gemini): codifiche e formati non previsti (UTF-16, archivi con un prefisso, flussi zlib)
        passavano. Regola nuova e più semplice: ogni file che non è testo UTF-8 si rifiuta, salvo esclusione
        dichiarata. Nel repository vero ce ne sono due, gli zip già esclusi."""
        import io as _io, zlib
        buf = _io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("dentro.md", "Autore: Mario Rossi\n" * 20)
        for nome, dati in (("img.bin", bytes(range(256))), ("pref.dat", b"PREF" + buf.getvalue()),
                           ("flusso.z", zlib.compress(b"Autore: Mario Rossi"))):
            with self.subTest(nome):
                self.committa(nome, dati)
                with self.assertRaises(ValueError) as e:
                    X.esporta(self.repo, "HEAD", self.dir / "fuori" / "p.zip", SOST)
                self.assertIn(nome, str(e.exception))
                self.assertIn("non è testo", str(e.exception))
                r = X.esporta(self.repo, "HEAD", self.dir / "fuori" / "q.zip", SOST, escludi=[nome])
                self.assertEqual(r["esclusi"], 1)
                subprocess.run(self.g + ["rm", "-q", nome], check=True)
                subprocess.run(self.g + ["commit", "-q", "-m", "via"], check=True)

    def test_percorsi_mac_in_utf16_o_utf32_senza_bom(self):
        """R14-04: UTF-16/32 senza BOM di testo ASCII è UTF-8 valido (byte nulli in mezzo): /Users/<nome> passava."""
        for cod in ("utf-16-le", "utf-16-be", "utf-32-le"):
            with self.subTest(cod):
                self.committa("note.txt", "vedi /Users/alice_inventata/segreto.txt".encode(cod))
                with self.assertRaises(ValueError) as e:
                    X.esporta(self.repo, "HEAD", self.dir / "fuori" / "p.zip", SOST)
                self.assertIn("note.txt", str(e.exception))
                subprocess.run(self.g + ["rm", "-q", "note.txt"], check=True)
                subprocess.run(self.g + ["commit", "-q", "-m", "via"], check=True)

    def test_nome_in_utf32_dentro_un_testo_valido(self):
        """Copertura (M-R14-05 di Gemini): un nome in UTF-32 dentro un file che è comunque UTF-8 valido."""
        self.committa("u32.txt", b"testo " + "Mario Rossi".encode("utf-32-le"))
        with self.assertRaises(ValueError) as e:
            X.esporta(self.repo, "HEAD", self.dir / "fuori" / "p.zip", SOST)
        self.assertIn("u32.txt", str(e.exception))

    def test_sostituzione_con_barre_rovesciate(self):
        zp = self.dir / "fuori" / "p.zip"
        X.esporta(self.repo, "HEAD", zp, [("Mario Rossi", "C:\\utenti\\g"), ("mrossi-dot", "<u>"), ("mario", "<u>")])
        self.assertIn("C:\\utenti\\g", self.leggi(zp)["a.md"].decode("utf-8"))

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
