"""Test del riconteggio indipendente delle esecuzioni (governance/censimento/riconta.py), scritti PRIMA del codice.
Trascrizioni finte nei due formati (Antigravity e Claude Code). Uso (dalla radice del repository):
  python3 -s -B -W error -m unittest brain.governance.censimento.test_riconta
"""
import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

_spec = importlib.util.spec_from_file_location("riconta", Path(__file__).with_name("riconta.py"))
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)

PREZZI = "2005-03-01 427.35 428.10 2005-03-02 430.55 431.20 2005-03-03 433.80 2005-03-04 434.12 2005-03-07 436.90"


def antigravity(cartella: Path) -> Path:
    righe = [
        {"step_index": 1, "type": "USER_INPUT", "content": "parliamo del periodo 2005-01-01 → 2023-10-31", "created_at": "t1"},
        {"step_index": 2, "type": "PLANNER_RESPONSE", "created_at": "t2",
         "tool_calls": [{"name": "run_command", "args": {"CommandLine": "(cd /Users/u/tb-x; python3 -c 'import caricatore; x = 1234.56')"}},
                        {"name": "view_file", "args": {"AbsolutePath": "/Users/u/brain/dati/reali/XAUUSD_15m.csv"}}]},
        {"step_index": 3, "type": "GENERIC", "content": PREZZI, "created_at": "t3"},
        {"step_index": 4, "type": "PLANNER_RESPONSE", "created_at": "t4",
         "tool_calls": [{"name": "run_command", "args": {"CommandLine": "/usr/bin/python3 analisi.py --periodo sviluppo"}},
                        {"name": "send_command_input", "args": {"Input": "carica('verifica')"}}]},
        {"step_index": 5, "type": "GENERIC", "content": "R medio -0.051 su 456 trade, 2024-01-03 .. 2026-11-10", "created_at": "t5"},
        {"step_index": 6, "type": "PLANNER_RESPONSE", "created_at": "t6",
         "tool_calls": [{"name": "run_command", "args": {"CommandLine": "ls -la"}}]},
    ]
    f = cartella / "6ad" / ".system_generated" / "logs" / "transcript_full.jsonl"
    f.parent.mkdir(parents=True)
    f.write_text("\n".join(json.dumps(r) for r in righe) + "\n")
    (cartella / "6ad" / ".system_generated" / "tasks").mkdir(parents=True)
    (cartella / "6ad" / ".system_generated" / "tasks" / "task-9.log").write_text("ok\n" + PREZZI + "\n")
    return f


def claude(cartella: Path) -> Path:
    righe = [
        {"type": "user", "timestamp": "c1", "message": {"role": "user", "content": "ciao"}},
        {"type": "assistant", "timestamp": "c2", "message": {"role": "assistant", "content": [
            {"type": "text", "text": "eseguo"},
            {"type": "tool_use", "id": "x1", "name": "Bash",
             "input": {"command": "cd ~/tb && python3 -m brain.dati.pipeline.controlla_cache --cache brain/dati/reali/cache_dukascopy"}},
            {"type": "tool_use", "id": "x2", "name": "Read", "input": {"file_path": "/Users/u/brain/dati/reali/x.csv"}}]}},
        {"type": "user", "timestamp": "c3", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "x1", "content": "2005 | 365 | 0 | 365\n2006 | 365 | 0 | 365"}]}},
        {"type": "user", "timestamp": "c4", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "x2", "content": [{"type": "text", "text": PREZZI}]}]}},
    ]
    f = cartella / "progetto" / "sessione.jsonl"
    f.parent.mkdir(parents=True)
    f.write_text("\n".join(json.dumps(r) for r in righe) + "\nriga non json\n")
    return f


class TestRiconta(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.dir = Path(self._t.name)

    def tearDown(self):
        self._t.cleanup()

    def test_antigravity_tutte_le_chiamate_e_tutti_gli_strumenti(self):
        r = R.esamina_file(antigravity(self.dir))
        self.assertEqual(r["formato"], "antigravity")
        self.assertEqual(r["strumenti"], {"run_command": 3, "view_file": 1, "send_command_input": 1})
        sens = {(c["passo"], c["strumento"]) for c in r["chiamate_sensibili"]}
        self.assertEqual(sens, {(2, "run_command"), (2, "view_file"), (4, "send_command_input")})
        esec = {(c["passo"], c["strumento"]) for c in r["esecuzioni"]}
        self.assertEqual(esec, {(2, "run_command"), (4, "run_command"), (4, "send_command_input")})   # (cd …; python3 e /usr/bin/python3

    def test_uscite_con_date_della_riserva_e_numeri_da_prezzo(self):
        r = R.esamina_file(antigravity(self.dir))
        u = {x["passo"]: x for x in r["uscite_riserva"]}
        self.assertEqual(set(u), {3})                     # il passo 1 è testo dell'utente, il 5 è dello sviluppo
        self.assertEqual((u[3]["date"], u[3]["prima"], u[3]["ultima"]), (5, "2005-03-01", "2005-03-07"))
        self.assertGreaterEqual(u[3]["numeri_prezzo"], 5)
        self.assertTrue(u[3]["da_guardare"])
        self.assertEqual(r["testo_con_date_riserva"], 1)   # il passo 1, contato a parte

    def test_log_dei_task(self):
        r = R.esamina_file(antigravity(self.dir).parents[1] / "tasks" / "task-9.log")
        self.assertEqual(r["formato"], "log")
        self.assertEqual(len(r["uscite_riserva"]), 1)
        self.assertTrue(r["uscite_riserva"][0]["da_guardare"])

    def test_claude_code(self):
        r = R.esamina_file(claude(self.dir))
        self.assertEqual(r["formato"], "claude")
        self.assertEqual(r["strumenti"], {"Bash": 1, "Read": 1})
        self.assertEqual({c["strumento"] for c in r["chiamate_sensibili"]}, {"Bash", "Read"})
        self.assertEqual(len(r["esecuzioni"]), 1)
        u = {x["passo"]: x for x in r["uscite_riserva"]}
        self.assertNotIn(3, u)                             # solo anni nei conteggi della cache: nessuna data, nessun prezzo
        self.assertTrue(u[4]["da_guardare"])
        self.assertEqual(r["righe_illeggibili"], 1)

    def test_rapporto_senza_contenuti_ne_prezzi(self):
        antigravity(self.dir)
        claude(self.dir)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = R.main([str(self.dir)])
        testo = buf.getvalue()
        self.assertEqual(rc, 0)
        for vietato in ("427.35", "436.90", "R medio", "-0.051", "1234.56"):        # 1234.56: nel comando, mascherato
            self.assertNotIn(vietato, testo)
        self.assertIn("DA GUARDARE", testo)
        self.assertIn("view_file", testo)
        self.assertIn("transcript_full.jsonl", testo)
        self.assertNotIn(str(Path.home()) + "/", testo.replace("~/", ""))  # cartella personale abbreviata

    def test_il_risultato_non_conserva_il_testo_delle_uscite(self):
        r = R.esamina_file(antigravity(self.dir))
        for u in r["uscite_riserva"]:
            self.assertEqual(set(u), {"passo", "ora", "date", "prima", "ultima", "numeri_prezzo", "da_guardare"})
        self.assertNotIn("427.35", repr(r))

    def test_date_dukascopy_e_limiti_della_riserva(self):
        self.assertEqual(R.date_riserva("XAUUSD/2009/05/07/BID_candles_min_1.bi5 2023-10-31 2023-11-01 2004-12-31"),
                         ["2009-06-07", "2023-10-31"])     # mesi da 0 negli URL di Dukascopy; 2023-11-01 e 2004 fuori


class TestR12bis(unittest.TestCase):
    """Rilievi R12bis-C-01, C-02, C-03 di Gemini (#56, #57)."""

    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.dir = Path(self._t.name)

    def tearDown(self):
        self._t.cleanup()

    def scrivi(self, nome, righe):
        f = self.dir / nome
        f.write_text("\n".join(json.dumps(r) for r in righe) + "\n")
        return f

    def test_argomenti_in_campi_diversi_e_uscite_di_altri_tipi(self):
        f = self.scrivi("a.jsonl", [
            {"step_index": 1, "type": "PLANNER_RESPONSE", "tool_calls": [
                {"name": "run_command", "arguments": {"CommandLine": "python3 run.py --cache cache_dukascopy"}},
                {"name": "read_file", "params": {"Path": "/r/brain/dati/reali/x.csv"}}]},
            {"step_index": 2, "type": "TOOL_OUTPUT", "content": "2012-05-01 1650.25 1651.10 1652.30 1649.90"},
        ])
        r = R.esamina_file(f)
        self.assertEqual(len(r["esecuzioni"]), 1)
        self.assertEqual(len(r["chiamate_sensibili"]), 2)
        self.assertEqual([u["passo"] for u in r["uscite_riserva"]], [2])
        g = self.scrivi("c.jsonl", [{"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Bash", "args": {"command": "python3 x.py cache_dukascopy"}}]}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "content": [
                {"type": "json", "data": {"msg": "2014-08-15 1300.50 1301.25 1299.75"}}]}]}}])
        r = R.esamina_file(g)
        self.assertEqual((len(r["esecuzioni"]), len(r["chiamate_sensibili"])), (1, 1))
        self.assertEqual(r["uscite_riserva"][0]["numeri_prezzo"], 3)

    def test_esecuzioni_in_altre_forme(self):
        f = self.scrivi("e.jsonl", [{"step_index": k, "tool_calls": [c]} for k, c in enumerate([
            {"name": "run_command", "args": {"CommandLine": "bash /tmp/lancia.sh"}},
            {"name": "run_command", "args": {"CommandLine": "source /tmp/run.sh && ./eseguibile_compilato"}},
            {"name": "run_command", "args": {"CommandLine": "awk '{print}' dati.txt"}},
            {"name": "invoke_subagent", "args": {"Prompt": "fai qualcosa"}},
            {"name": "run_command", "args": {"CommandLine": "ls -la && cat note.md"}},
            {"name": "run_command", "args": {"CommandLine": "cd x && ./eseguibile_compilato --veloce"}},
        ], 1)])
        self.assertEqual(sorted(e["passo"] for e in R.esamina_file(f)["esecuzioni"]), [1, 2, 3, 4, 6])

    def test_formato_sconosciuto_trattato_come_uscita(self):
        f = self.scrivi("x.jsonl", [{"evento": "risultato", "dati": "2010-03-01 1110.25 1111.50 1109.75"}])
        r = R.esamina_file(f)
        self.assertEqual(len(r["uscite_riserva"]), 1)
        self.assertTrue(r["uscite_riserva"][0]["da_guardare"])
        self.assertEqual(r["testo_con_date_riserva"], 0)

    def test_date_in_altri_formati(self):
        casi = {
            "03/01/2005": ["2005-01-03", "2005-03-01"],          # giorno/mese o mese/giorno: tutte e due
            "25/12/2010": ["2010-12-25"],
            "2005.01.03": ["2005-01-03"],
            "03.01.2005": ["2005-01-03"],
            "20150615": ["2015-06-15"],
            "20150615..20160720": ["2015-06-15", "2016-07-20"],                 # vicine a un punto (#68)
            "fino al 20150615.": ["2015-06-15"],
            "valore 1.20150615 e 20150615.5": [],                             # dentro un numero decimale: no
            "ts=1434326400 ms=1434326400000": ["2015-06-15"],
            "cache_dukascopy/XAUUSD/2015/05/15/12h_ticks.bi5": ["2015-06-15"],
            "datafeed/2015/05/15/12h_ticks.bi5": ["2015-06-15"],          # senza simbolo: mesi da 0 lo stesso
            "2015/05/03/BID_candles_min_1.bi5": ["2015-06-03"],
            "backup/2015/06/15": ["2015-06-15"],                          # percorso qualsiasi: data normale
            "ms=1434326400000": ["2015-06-15"],
            "s=1434326400": ["2015-06-15"],
            "2015/06/15": ["2015-06-15"],
            "20250615 1734326400 2026/01/02": [],                # fuori dalla riserva
            "versione 3.13.18, hash a3944ac0": [],
        }
        for testo, atteso in casi.items():
            self.assertEqual(R.date_riserva(testo), atteso, testo)

    def test_prezzi_in_altre_forme_contati_e_mascherati(self):
        forme = ["1850,75", "1,850.75", "1.850,75", "2650.45", "1850.1234", "395.50"]
        for x in forme:
            self.assertEqual(len(R.numeri_prezzo(f"prezzo={x} fine")), 1, x)
            self.assertNotIn(x, R._breve(f"prezzo={x} fine", "/casa"), x)
        self.assertEqual(R.numeri_prezzo("versione 3.13 e 2 trade, R -0.05"), [])

    def test_contenuti_dei_file_mai_stampati(self):
        self.scrivi("w.jsonl", [{"step_index": 1, "tool_calls": [{"name": "write_file", "args": {
            "Path": "/repo/brain/note.md", "Content": "cache_dukascopy 2012-05-04 SEGRETO_IN_CHIARO"}}]},
            {"step_index": 2, "tool_calls": [{"name": "edit_file", "args": {
                "Path": "/repo/x.py", "Replacement": "cache_dukascopy ALTRO_SEGRETO", "TargetContent": "y"}}]}])
        buf = io.StringIO()
        with redirect_stdout(buf):
            R.main([str(self.dir)])
        testo = buf.getvalue()
        for vietato in ("SEGRETO_IN_CHIARO", "ALTRO_SEGRETO", "2012-05-04"):
            self.assertNotIn(vietato, testo)
        self.assertIn("/repo/brain/note.md", testo)
        self.assertIn("Content", testo)                       # si dice QUALI campi c'erano, non cosa contenevano


if __name__ == "__main__":
    unittest.main()
