"""Bonifica dopo l'audit esterno «Red Team» del 12/11/2026 (ramo fix/red-team-guardian). Test scritti PRIMA delle
correzioni (TDD). Ogni classe indica il rilievo.
Uso (dalla cartella guardian/): python3 -s -B -m unittest discover -s test -v
"""
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from decimal import Decimal as D
from pathlib import Path
from unittest import mock

GUARDIAN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GUARDIAN))

from g0 import _toml                                            # noqa: E402
from g0 import limiti as L                                      # noqa: E402
from g0 import scheda as SCH                                    # noqa: E402
from g0.strumenti import Strumento, perdita_allo_stop           # noqa: E402
from g0.valori import NON_STIMABILE, Valore, ipotesi, misura    # noqa: E402
from journal import journal as J                                # noqa: E402
from journal.indicatori import metriche_dopo_perdita, pattern_r1  # noqa: E402

try:
    import tomllib as TOMLLIB_STD
except ModuleNotFoundError:
    TOMLLIB_STD = None
try:
    import fcntl
except ImportError:
    fcntl = None

ESEMPIO = GUARDIAN / "esempi" / "situazione_esempio.toml"
P = {"autore": "claude", "evento": "x", "scadenza_utc": "2026-12-01T00:00:00Z", "fonte": "t"}


def esempio():
    with open(ESEMPIO, "rb") as f:
        return _toml.load(f)


def regole_con(**conferme):
    with open(SCH.FILE_REGOLE_PERSONALI, "rb") as f:
        regole = _toml.load(f)
    for r in regole["regola"]:
        if r["id"].replace("-", "_") in conferme:
            r.update(confermata=True, valore=conferme[r["id"].replace("-", "_")])
    return regole


def non_stimabile(*args, **kwargs):
    """Perdita allo stop NON STIMABILE (per esempio una specifica del contratto non stimabile)."""
    return ipotesi(None, "USD", "specifica non stimabile (test)", "H_spec: specifica del contratto non stimabile")


class TestAlto1NonStimabile(unittest.TestCase):
    def test_stop_residui_propaga_non_stimabile(self):
        n = ipotesi(None, "USD", "t", "H_gap")
        for sr in (L.stop_residui(misura("1000", "USD", "t"), n), L.stop_residui(n, misura("200", "USD", "t"))):
            self.assertIsNone(sr.valore)
            self.assertEqual(sr.incertezza, NON_STIMABILE)
            self.assertIn("H_gap", sr.condizioni)
            self.assertEqual(sr.stato_verifica, "C")
            self.assertEqual(sr.unita, "stop")

    def test_scheda_con_perdita_non_stimabile_avvisa_e_non_esplode(self):
        """Ogni confronto con un dato NON STIMABILE diventa un avviso «non verificabile», mai un TypeError."""
        with mock.patch.object(SCH, "perdita_allo_stop", non_stimabile):
            testo = "\n".join(SCH.scheda(esempio(), regole_personali=regole_con(P_01="0.01", P_05="0.004")))
        self.assertIn("perdita allo stop (USDJPY): NON STIMABILE", testo)
        for cosa in ("Trade previsto contro il limite giornaliero", "Trade previsto contro il limite totale",
                     "Scenario di stress contro il limite giornaliero", "Scenario di stress contro il limite totale",
                     "P-01 rischio del trade previsto", "P-05 trade previsto", "P-05 scenario di stress"):
            self.assertIn(f"{cosa}: controllo non verificabile (dato NON STIMABILE)", testo, cosa)
        self.assertIn("RACCOMANDAZIONE\nnon entrare", testo)


class TestAlto5TradeSovrapposti(unittest.TestCase):
    def test_trade_sovrapposti_esclusi_da_r1(self):
        """Il secondo trade è aperto PRIMA della chiusura della perdita: non è un rientro dopo una perdita."""
        t1 = {"aperto_utc": "2026-11-12T09:00:00Z", "chiuso_utc": "2026-11-12T09:30:00Z", "pnl_conto": "-200",
              "quantita": "1"}
        t2 = {"aperto_utc": "2026-11-12T09:20:00Z", "chiuso_utc": "2026-11-12T09:40:00Z", "pnl_conto": "50",
              "quantita": "2"}
        self.assertEqual(metriche_dopo_perdita([t1, t2]), [])
        self.assertEqual(pattern_r1([t1, t2], minuti_max=10, rapporto_min=1)["casi"], [])
        t3 = dict(t2, aperto_utc="2026-11-12T09:30:00Z")                       # esattamente alla chiusura: 0 minuti
        self.assertEqual(len(pattern_r1([t1, t3], minuti_max=10, rapporto_min=1)["casi"]), 1)


class TestAlto6Basso1Strumenti(unittest.TestCase):
    def test_simbolo_fonte_e_valuta_stringhe_non_vuote(self):
        base = dict(simbolo="EURUSD", classe="fx", valuta_profitto="USD", dimensione_contratto=D(100000), fonte="t",
                    valuta_base="EUR")
        Strumento(**base)
        for campo, valore in (("simbolo", ""), ("simbolo", "  "), ("simbolo", None), ("fonte", ""), ("fonte", 5),
                              ("valuta_profitto", ""), ("valuta_profitto", None)):
            with self.assertRaises(ValueError, msg=f"{campo}={valore!r}"):
                Strumento(**dict(base, **{campo: valore}))

    def test_tick_robusto_al_rumore_float_ma_non_ai_prezzi_fuori_tick(self):
        """Decimal(4990.3) vale 4990,30000000000018…: la distanza in tick è 96,99999999999818…, cioè 97 tick."""
        fut = Strumento("FUT", "future", "USD", None, "t", passo_tick=D("0.1"), valore_tick=D("10"))
        ingresso = misura("5000", "prezzo", "t")
        stop = Valore(D(4990.3), "prezzo", "MISURA", "osservazione", "t")             # Decimal da float grezzo
        self.assertEqual(perdita_allo_stop(fut, ingresso, stop, misura("1", "contratti", "t"), "USD").valore, D(970))
        with self.assertRaises(ValueError):                                             # 97,5 tick: fuori tick
            perdita_allo_stop(fut, ingresso, misura("4990.25", "prezzo", "t"), misura("1", "contratti", "t"), "USD")


def _scrivi_previsioni(path: Path, dati_record):
    righe = []
    for i, d in enumerate(dati_record, 1):
        righe.append(J._canonico({"schema": J.SCHEMA, "registro": "previsione", "id": f"PRE-{i:05d}",
                                  "registrato_utc": "2026-11-12T22:00:00Z", "prec_hash": J.GENESI, "dati": d}))
    path.write_text("\n".join(righe) + "\n", encoding="utf-8")


class TestMedio3e4VersioniFinali(unittest.TestCase):
    def test_versioni_finali_rifiuta_riferimenti_fantasma_e_nature_diverse(self):
        esito = {"autore": "utente", "fonte": "t", "chiude": "PRE-00001", "esito": 1}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "previsione.jsonl"
            for nome, record in (
                    ("corregge fantasma", [dict(P, probabilita=0.5), dict(P, probabilita=0.6, corregge="PRE-00099")]),
                    ("chiude fantasma", [dict(P, probabilita=0.5), dict(esito, chiude="PRE-00099")]),
                    ("esito che corregge una previsione", [dict(P, probabilita=0.5), dict(esito, corregge="PRE-00001")]),
                    ("previsione che corregge un esito", [dict(P, probabilita=0.5), esito,
                                                          dict(P, probabilita=0.6, corregge="PRE-00002")])):
                _scrivi_previsioni(path, record)
                with self.assertRaises(ValueError, msg=nome):
                    J.versioni_finali(path)
                with self.assertRaises(ValueError, msg=nome):
                    J.brier(Path(tmp))
            _scrivi_previsioni(path, [dict(P, probabilita=0.5), esito])
            self.assertEqual(len(J.versioni_finali(path)), 2)                          # file coerente: nessun errore

    def test_previsione_con_esito_senza_chiude_rifiutata(self):
        for extra in ({"esito": 1}, {"esito_utc": "2026-12-01T00:00:00Z"}):
            with self.assertRaises(ValueError, msg=str(extra)):
                J.valida("previsione", dict(P, probabilita=0.5, **extra))


def _figlio_verifica(cartella: Path) -> subprocess.Popen:
    codice = ("import sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); "
              "from journal import journal as J; print(J.verifica(Path(sys.argv[2])))")
    env = {"PATH": os.environ["PATH"], "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.Popen([sys.executable, "-s", "-B", "-c", codice, str(GUARDIAN), str(cartella)], env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


class TestMedio5e6e7Lock(unittest.TestCase):
    T = {"simbolo": "EURUSD", "direzione": "long", "aperto_utc": "2026-11-12T09:00:00Z", "ingresso": "1.085",
         "stop": "1.083", "quantita": "1", "fonte": "t"}

    @unittest.skipIf(fcntl is None or not hasattr(os, "O_CLOEXEC"), "solo Unix con O_CLOEXEC")
    def test_lock_aperto_con_o_cloexec(self):
        """Irrobustimento esplicito: da Python 3.4 (PEP 446) os.open crea già descrittori non ereditabili."""
        aperture = []
        originale = os.open

        def spia(path, flags, *a):
            if str(path).endswith(J.FILE_LOCK):
                aperture.append(flags)
            return originale(path, flags, *a)

        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(J.os, "open", spia):
            J.aggiungi("trade", self.T, Path(tmp))
        self.assertTrue(aperture)
        self.assertTrue(all(f & os.O_CLOEXEC for f in aperture))

    @unittest.skipIf(fcntl is None, "fcntl non disponibile (non Unix)")
    def test_verifica_attende_il_lock_esclusivo(self):
        """verifica() durante una scrittura vedrebbe righe e ancora disallineate: deve attendere il lock."""
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            J.aggiungi("trade", self.T, d)
            fd = os.open(J.percorso_lock(d), os.O_RDWR | os.O_CREAT, 0o600)
            figlio = None
            try:
                fcntl.flock(fd, fcntl.LOCK_EX)
                figlio = _figlio_verifica(d)
                time.sleep(1.0)
                in_attesa = figlio.poll() is None
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
                os.close(fd)
                if figlio is not None:
                    out, err = figlio.communicate(timeout=60)
            self.assertTrue(in_attesa, "verifica() non ha atteso il lock")
            self.assertEqual(figlio.returncode, 0, err)
            self.assertEqual(out.strip(), "[]")

    def test_ripiego_recupera_lock_orfani_solo_se_sicuro(self):
        """Senza fcntl il file di lock contiene PID, host e orario. Un lock è recuperato SOLO se: stesso host,
        processo non più attivo e più vecchio di 2 × ATTESA_LOCK_S. In ogni altro caso: TimeoutError."""
        morto = subprocess.run([sys.executable, "-c", "import os; print(os.getpid())"], capture_output=True,
                               text=True).stdout.strip()
        host = socket.gethostname()
        vecchio = time.time() - 60
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(J, "fcntl", None), \
                mock.patch.object(J, "ATTESA_LOCK_S", 0.3):
            d = Path(tmp)
            lock = J.percorso_lock(d)
            for nome, contenuto in (("processo ancora attivo", {"pid": os.getpid(), "host": host, "t": vecchio}),
                                    ("lock recente", {"pid": int(morto), "host": host, "t": time.time()}),
                                    ("altro host", {"pid": int(morto), "host": host + "-altro", "t": vecchio}),
                                    ("contenuto illeggibile", "non è json")):
                lock.write_text(contenuto if isinstance(contenuto, str) else json.dumps(contenuto), encoding="utf-8")
                with self.assertRaises(TimeoutError, msg=nome):
                    J.aggiungi("trade", self.T, d)
                self.assertTrue(lock.exists(), nome)
            lock.write_text(json.dumps({"pid": int(morto), "host": host, "t": vecchio}), encoding="utf-8")
            J.aggiungi("trade", self.T, d)                                              # orfano: recuperato
            self.assertFalse(lock.exists())
            self.assertEqual(J.verifica(d), [])


class TestMedio10e11Toml(unittest.TestCase):
    def test_fmt_con_esponenti_estremi(self):
        for x, atteso in (("1E+100", "[MISURA] x: 10.000.000"), ("1E-100", "[MISURA] x: 0,00 USD"),
                          ("Infinity", "[MISURA] x: Infinity USD")):
            self.assertTrue(SCH.fmt(Valore(D(x), "USD", "MISURA", "osservazione", "t"), "x").startswith(atteso), x)

    def test_p01_con_capitale_non_positivo(self):
        d = esempio()
        cap, saldo0, eq = (misura(x, "USD", "t") for x in ("0", "100400", "100150"))
        pt = misura("682", "USD", "t")
        f_g, _ = L._frazioni("ftmo_2step")
        avvisi, _ = SCH._regole_personali(regole_con(P_01="0.01"), d, cap, saldo0, eq, pt, None, f_g,
                                          d["trade_previsto"])
        self.assertIn("P-01: capitale iniziale non positivo: rischio del trade non verificabile", avvisi)

    def test_toml_minimale_chiavi_tra_virgolette_e_scheda_con_cambio(self):
        testo = '[cambi]\n"JPY/EUR" = "162.00"\n\'USD/EUR\' = "1.0870"   # commento\n"" = 1\n'
        atteso = {"cambi": {"JPY/EUR": "162.00", "USD/EUR": "1.0870", "": 1}}
        self.assertEqual(_toml.loads_minimale(testo), atteso)
        if TOMLLIB_STD is not None:
            self.assertEqual(TOMLLIB_STD.loads(testo), atteso)
        situazione = """[conto]
prodotto = "ftmo_2step"
valuta = "EUR"
capitale_iniziale = "100000"
saldo_mezzanotte = "100000"
equity = "100000"
fonte = "[ESEMPIO] test"

[[strumento]]
simbolo = "USDJPY"
classe = "fx"
valuta_base = "USD"
valuta_profitto = "JPY"
dimensione_contratto = "100000"
fonte = "[ESEMPIO] test"

[cambi]
"JPY/EUR" = "162.00"

[trade_previsto]
simbolo = "USDJPY"
ingresso = "150.00"
stop = "149.50"
quantita = "1"
"""
        testo_scheda = "\n".join(SCH.scheda(_toml.loads_minimale(situazione), regole_personali=regole_con()))
        self.assertIn("perdita allo stop (USDJPY): 308,64 EUR", testo_scheda)          # 50.000 JPY / 162


if __name__ == "__main__":
    unittest.main()
