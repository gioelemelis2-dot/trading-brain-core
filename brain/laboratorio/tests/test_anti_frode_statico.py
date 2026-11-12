"""
Test Statico Anti-Frode per Codice Sorgente e Documenti.
Verifica Meccanica Inviolabile:
1. Fallisce se trova '.replace(tzinfo=' in qualsiasi file sorgente di pipeline o backtester.
2. Fallisce se trova hash della V3.3 diversi da '6fb9d76e54daabecd5215aaa255ef3b94f2a0052569b20734b1ac90181627638'.
3. Fallisce se engine.py o portfolio.py non importano Strumento e Valore da brain.guardian.g0.
"""

import ast
import re
import unittest
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]

HASH_CANONICO_V3_3 = "6fb9d76e54daabecd5215aaa255ef3b94f2a0052569b20734b1ac90181627638"


class TestAntiFrodeStatico(unittest.TestCase):
    def setUp(self):
        self.pipeline_dir = repo_root / "brain" / "dati" / "pipeline"
        self.backtester_dir = repo_root / "brain" / "laboratorio" / "backtester"
        self.consegne_gemini_dir = repo_root / "brain" / "collaborazione" / "da-gemini"

    def test_01_no_replace_tzinfo_allowed(self):
        """Divieto assoluto di usare .replace(tzinfo=...) per mascherare timestamp senza fuso."""
        python_files = list(self.pipeline_dir.glob("*.py")) + list(self.backtester_dir.glob("*.py"))
        for py_path in python_files:
            text = py_path.read_text(encoding="utf-8")
            self.assertNotIn(
                ".replace(tzinfo=",
                text,
                f"Trovata violazione anti-frode: '.replace(tzinfo=' in {py_path.name}! "
                f"I timestamp devono essere verificati e rifiutati se privi di timezone, non mascherati.",
            )

    def test_02_v3_3_hash_strictly_canonical(self):
        """Verifica che nessun file contenga hash V3.3 spuri o allucinati (tipo 6fb9d76e73fbf...)."""
        # Cerca stringhe esadecimali di 64 caratteri che iniziano per 6fb9d76e
        pattern = re.compile(r"\b6fb9d76e[0-9a-fA-F]{56}\b")
        
        # Scansiona tutti i file md e txt della cartella consegne
        files_to_check = list(self.consegne_gemini_dir.rglob("*.md")) + list(self.consegne_gemini_dir.rglob("*.sha256"))
        for fpath in files_to_check:
            text = fpath.read_text(encoding="utf-8")
            matches = pattern.findall(text)
            for m in matches:
                self.assertEqual(
                    m.lower(),
                    HASH_CANONICO_V3_3.lower(),
                    f"Trovato hash V3.3 non canonico '{m}' in {fpath.relative_to(repo_root)}! "
                    f"Atteso esclusivamente: {HASH_CANONICO_V3_3}",
                )

    def test_03_engine_and_portfolio_import_guardian_g0(self):
        """Verifica che engine.py e portfolio.py importino Strumento e Valore da brain.guardian.g0."""
        engine_path = self.backtester_dir / "engine.py"
        portfolio_path = self.backtester_dir / "portfolio.py"

        for target_path in [engine_path, portfolio_path]:
            text = target_path.read_text(encoding="utf-8")
            tree = ast.parse(text, filename=str(target_path))

            imported_names = set()
            imported_modules = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        imported_modules.add(node.module)
                    for alias in node.names:
                        imported_names.add(alias.name)

            self.assertTrue(
                any("brain.guardian.g0" in mod for mod in imported_modules),
                f"{target_path.name} non importa da brain.guardian.g0!",
            )
            self.assertIn("Strumento", imported_names, f"{target_path.name} non importa Strumento!")
            self.assertIn("Valore", imported_names, f"{target_path.name} non importa Valore!")


if __name__ == "__main__":
    unittest.main()
