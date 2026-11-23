"""Ogni mutante degli script di mutation testing si applica ESATTAMENTE una volta al codice attuale (22/11/2026).

Perché: tre volte (V10 dopo #128; VD26, VD35, VD72 dopo #124; VD30, VD39, VD111 dopo la seconda parte di #124) una
correzione ha cambiato le righe che un mutante modificava e la cosa si è vista solo nella corsa completa dei mutanti,
ore dopo il commit. Dal 23/11 controlla anche che il file mutato resti Python valido (PR12 ed EV33
erano «NON VALIDI»). Questo controllo è veloce (nessuna copia, nessuna suite) e gira con i test normali.
Uso: python3 -s -B -W error -m unittest brain.laboratorio.tests.test_mutanti_applicabili
"""
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

QUI = Path(__file__).resolve().parent
SCRIPT = ("mutazioni_esecuzione.py", "mutazioni_verdetto.py", "mutazioni_percorso.py")


class TestMutantiApplicabili(unittest.TestCase):
    def test_ogni_sostituzione_compare_una_volta(self):
        for nome in SCRIPT:
            with self.subTest(script=nome), tempfile.TemporaryDirectory() as t, \
                    mock.patch.object(sys, "argv", [nome, t]):
                g = runpy.run_path(str(QUI / nome), run_name="controllo_applicabilita")
                brain = g["BRAIN"]
                problemi = []
                for mutante, sostituzioni in g["M"].items():
                    testi = {}
                    for f, vecchio, nuovo in sostituzioni:
                        testo = testi.get(f) or (brain / f).read_text(encoding="utf-8")
                        n = testo.count(vecchio)
                        if n != 1:
                            problemi.append(f"{mutante}: {n} volte in {f}")
                        if vecchio == nuovo:
                            problemi.append(f"{mutante}: sostituzione identica")
                        testi[f] = testo.replace(vecchio, nuovo)
                    for f, testo in testi.items():                  # il mutante deve restare Python valido
                        try:
                            compile(testo, f, "exec")
                        except SyntaxError as e:
                            problemi.append(f"{mutante}: sintassi rotta in {f} ({e.msg})")
                self.assertEqual(problemi, [])
                self.assertEqual(len(set(g["M"])), len(g["M"]))


if __name__ == "__main__":
    unittest.main()
