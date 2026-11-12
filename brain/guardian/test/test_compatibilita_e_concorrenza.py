"""Rifinitura dopo l'audit incrociato con Gemini (macOS, Python 3.9.6 di sistema), 12/11/2026. Test scritti PRIMA
delle correzioni (TDD):
1. compatibilità con Python 3.9: TOML senza `tomllib` (fallback su `tomli` o su un parser minimale della libreria
   standard) e orari con `Z`, che `datetime.fromisoformat` di Python 3.9/3.10 non accetta; il formato degli orari
   deve essere lo STESSO su ogni versione, altrimenti un journal scritto con 3.13 risulterebbe invalido su 3.9;
2. `probabilita` come `Decimal` finito in [0, 1];
3. lock esclusivo in `aggiungi()` contro le scritture concorrenti.
Uso (dalla cartella guardian/): python3 -s -B -m unittest discover -s test -v
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path
from unittest import mock

GUARDIAN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GUARDIAN))

from journal import indicatori as I                # noqa: E402
from journal import journal as J                   # noqa: E402

try:
    import tomllib as TOMLLIB_STD                    # Python 3.11+
except ModuleNotFoundError:
    TOMLLIB_STD = None
try:
    import fcntl
except ImportError:                                  # non Unix
    fcntl = None

FILE_TOML = sorted(GUARDIAN.glob("regole/*.toml")) + sorted(GUARDIAN.glob("esempi/*.toml"))
T = {"simbolo": "EURUSD", "direzione": "long", "aperto_utc": "2026-11-12T09:00:00Z", "ingresso": "1.085",
     "stop": "1.083", "quantita": "1", "fonte": "t"}
P = {"autore": "claude", "evento": "x", "scadenza_utc": "2026-12-01T00:00:00Z", "fonte": "t"}

CAMPIONE_TOML = r'''# commento iniziale
titolo = "con # cancelletto, \"virgolette\" e \\ barra"   # commento finale
letterale = 'C:\percorso\senza\escape'
intero = 42
negativo = -7
decimale = 0.10
esponente = 1e-3
separatori = 1_000
vero = true
falso = false
vuoto = []
lista = [1, 2, 3]
stringhe = ["a", "b # non è un commento", 'c']
unicode = "caff\u00e8 àè"

[sezione.sotto]
chiave-con-trattino = "x"

[[voci]]
n = 1

[[voci]]
n = 2

[voci.dettaglio]
k = "v"
'''


# Risultato atteso del campione, scritto a mano: serve su Python 3.9, dove tomllib non esiste e il parser minimale è
# proprio quello in uso. Su 3.11+ il test controlla anche che tomllib dia esattamente questo risultato.
ATTESO_CAMPIONE = {
    "titolo": 'con # cancelletto, "virgolette" e \\ barra', "letterale": r"C:\percorso\senza\escape",
    "intero": 42, "negativo": -7, "decimale": 0.10, "esponente": 0.001, "separatori": 1000, "vero": True,
    "falso": False, "vuoto": [], "lista": [1, 2, 3], "stringhe": ["a", "b # non è un commento", "c"],
    "unicode": "caffè àè", "sezione": {"sotto": {"chiave-con-trattino": "x"}},
    "voci": [{"n": 1}, {"n": 2, "dettaglio": {"k": "v"}}],
}


class _Datetime39(datetime):
    """`datetime.fromisoformat` come in Python 3.9/3.10: niente `Z`, frazioni di secondo solo a 3 o 6 cifre."""

    @classmethod
    def fromisoformat(cls, s):
        if s.endswith("Z"):
            raise ValueError(f"Invalid isoformat string: {s!r}")
        m = re.search(r"\.(\d+)", s)
        if m and len(m.group(1)) not in (3, 6):
            raise ValueError(f"Invalid isoformat string: {s!r}")
        return datetime.fromisoformat(s)


class TestTomlPortabile(unittest.TestCase):
    def test_parser_minimale_uguale_a_tomllib_sui_file_del_brain_e_sul_campione(self):
        """Il parser di riserva deve dare ESATTAMENTE il risultato di tomllib sui file usati dal Guardian."""
        from g0 import _toml
        self.assertIn(_toml.MOTORE, ("tomllib", "tomli", "minimale"))
        for f in FILE_TOML:
            testo = f.read_text(encoding="utf-8")
            minimale = _toml.loads_minimale(testo)
            if TOMLLIB_STD is not None:
                self.assertEqual(minimale, TOMLLIB_STD.loads(testo), f.name)
        self.assertEqual(_toml.loads_minimale(CAMPIONE_TOML), ATTESO_CAMPIONE)             # anche su Python 3.9
        if TOMLLIB_STD is not None:
            self.assertEqual(TOMLLIB_STD.loads(CAMPIONE_TOML), ATTESO_CAMPIONE)             # il letterale è giusto
        regole = _toml.loads_minimale((GUARDIAN / "regole" / "regole_personali.toml").read_text(encoding="utf-8"))
        self.assertEqual(len(regole["regola"]), 15)                  # anche senza tomllib: valori noti
        ftmo = _toml.loads_minimale((GUARDIAN / "regole" / "prop_firm_ftmo.toml").read_text(encoding="utf-8"))
        self.assertEqual(ftmo["prodotti"]["ftmo_2step"]["max_daily_loss"]["frazione"], 0.05)

    def test_parser_minimale_rifiuta_cio_che_non_sa_leggere(self):
        """Fallire in modo esplicito, mai interpretare a metà: ogni costrutto non gestito è un errore con la riga."""
        from g0 import _toml
        for testo in ('x = {a = 1}', 'x = """a"""', 'x = 2026-11-12', 'x = [\n1]', 'x = 1\nx = 2',
                      '[a]\n[a]', 'a.b = 1', '"a b" = 1', 'x = "aperta', 'x = 0x1F', 'x = nan', 'x = 01',
                      '[a\n', 'x = 1 2'):
            with self.assertRaises(ValueError, msg=testo):
                _toml.loads_minimale(testo)

    def test_scheda_e_limiti_usano_il_caricatore_portabile(self):
        """Senza tomllib (Python 3.9) scheda e limiti devono funzionare: niente `import tomllib` diretto."""
        for nome in ("g0/scheda.py", "g0/limiti.py"):
            testo = (GUARDIAN / nome).read_text(encoding="utf-8")
            self.assertNotRegex(testo, r"(?m)^import tomllib", nome)


class TestOrariPortabili(unittest.TestCase):
    ATTESO = datetime(2026, 11, 12, 9, 33, 0, 120000, tzinfo=timezone.utc)

    def test_z_e_frazioni_anche_con_fromisoformat_di_python_3_9(self):
        with mock.patch.object(J, "datetime", _Datetime39), \
                mock.patch.object(I, "datetime", _Datetime39, create=True):
            for s in ("2026-11-12T09:33:00.12Z", "2026-11-12T09:33:00.120Z", "2026-11-12T09:33:00.120000+00:00"):
                self.assertEqual(J.orario_utc("t", s), self.ATTESO, s)
                self.assertEqual(I._t(s), self.ATTESO, s)
            J.valida("trade", T)
            J.valida("previsione", dict(P, probabilita=0.5))

    def test_stesso_formato_accettato_su_ogni_versione(self):
        """Formato unico: AAAA-MM-GGTHH:MM:SS[.frazione da 1 a 6 cifre] seguito da Z o +00:00. Python 3.11+ accetta
        anche forme che 3.9 rifiuta: senza questa regola un journal valido su Linux sarebbe invalido sul Mac."""
        for s in ("2026-11-12T09:00:00Z", "2026-11-12T09:00:00+00:00", "2026-11-12T09:00:00.1Z",
                  "2026-11-12T09:00:00.123456Z"):
            J.orario_utc("t", s)
        for s in ("2026-11-12T09:00Z", "20261112T090000Z", "2026-11-12 09:00:00Z", "2026-11-12T09:00:00.1234567Z",
                  "2026-11-12T09:00:00z", "2026-11-12T09:00:00-00:00", "2026-11-12T10:00:00+01:00",
                  "2026-11-12T25:00:00Z", "2026-02-30T09:00:00Z"):
            with self.assertRaises(ValueError, msg=s):
                J.orario_utc("t", s)
            with self.assertRaises(ValueError, msg=s):
                I._t(s)
        J.valida("stato", {"data": "2026-11-12", "fonte": "t"})
        for data in ("20261112", "2026-W46-4", "2026-11-12T00:00:00Z"):
            with self.assertRaises(ValueError, msg=data):
                J.valida("stato", {"data": data, "fonte": "t"})


class TestProbabilitaDecimal(unittest.TestCase):
    def test_decimal_finito_in_0_1_accettato_e_registrato(self):
        for p in (D("0"), D("0.7"), D("1"), D("0.333333333333333333333")):
            J.valida("previsione", dict(P, probabilita=p))
        for p in (D("NaN"), D("Infinity"), D("-Infinity"), D("1.01"), D("-0.1"), True, float("nan"), "abc", None):
            with self.assertRaises(ValueError, msg=repr(p)):
                J.valida("previsione", dict(P, probabilita=p))
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            a = J.aggiungi("previsione", dict(P, probabilita=D("0.7")), d)["id"]
            J.aggiungi("previsione", {"autore": "utente", "fonte": "t", "chiude": a, "esito": 1}, d)
            self.assertEqual(J.verifica(d), [])
            self.assertAlmostEqual(J.brier(d)["claude"]["brier"], (0.7 - 1) ** 2)


def _figlio(cartella: Path, n: int) -> subprocess.Popen:
    codice = ("import json, sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); "
              "from journal import journal as J\n"
              "for i in range(int(sys.argv[3])): J.aggiungi('trade', json.loads(sys.argv[4]), Path(sys.argv[2]))")
    env = {"PATH": os.environ["PATH"], "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.Popen([sys.executable, "-s", "-B", "-c", codice, str(GUARDIAN), str(cartella), str(n),
                             json.dumps(T)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


class TestLockConcorrente(unittest.TestCase):
    @unittest.skipIf(fcntl is None, "fcntl non disponibile (non Unix)")
    def test_aggiungi_attende_il_lock_esclusivo(self):
        """Deterministico: con il lock tenuto da un altro processo, aggiungi() deve ATTENDERE, non scrivere."""
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            d.mkdir(exist_ok=True)
            fd = os.open(J.percorso_lock(d), os.O_RDWR | os.O_CREAT, 0o600)
            figlio = None
            try:
                fcntl.flock(fd, fcntl.LOCK_EX)
                figlio = _figlio(d, 1)
                time.sleep(1.0)
                in_attesa = figlio.poll() is None
                scritto = (d / "trade.jsonl").exists()
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
                os.close(fd)
                if figlio is not None:
                    _, err = figlio.communicate(timeout=60)      # sempre atteso: nessun processo orfano
            self.assertTrue(in_attesa, "aggiungi() ha scritto senza attendere il lock")
            self.assertFalse(scritto)
            self.assertEqual(figlio.returncode, 0, err)
            self.assertEqual(J.verifica(d), [])

    def test_scritture_concorrenti_catena_e_ancora_integre(self):
        """6 processi × 15 record in parallelo: 90 righe, id unici, catena e ancora integre."""
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            figli = [_figlio(d, 15) for _ in range(6)]
            esiti = [(f.communicate(timeout=120)[1], f.returncode) for f in figli]   # tutti attesi, poi i controlli
            for err, rc in esiti:
                self.assertEqual(rc, 0, err)
            righe = J._righe(d / "trade.jsonl")
            self.assertEqual(len(righe), 90)
            self.assertEqual(len({json.loads(r)["id"] for r in righe}), 90)
            self.assertEqual(J.verifica(d), [])

    def test_ripiego_senza_fcntl_con_file_di_lock_esclusivo(self):
        """Senza fcntl: file di lock creato in modo esclusivo. Un lock rimasto (processo interrotto) produce un errore
        esplicito dopo l'attesa, mai una scrittura non protetta; a scrittura conclusa il file di lock è rimosso."""
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(J, "fcntl", None), \
                mock.patch.object(J, "ATTESA_LOCK_S", 0.3):
            d = Path(tmp)
            lock = J.percorso_lock(d)
            lock.write_text("lock rimasto", encoding="utf-8")
            with self.assertRaises(TimeoutError):
                J.aggiungi("trade", T, d)
            self.assertFalse((d / "trade.jsonl").exists())
            lock.unlink()
            J.aggiungi("trade", T, d)
            self.assertFalse(lock.exists())
            self.assertEqual(J.verifica(d), [])


if __name__ == "__main__":
    unittest.main()
