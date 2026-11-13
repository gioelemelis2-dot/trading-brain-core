"""DSR con la scala di Bailey e López de Prado (2014), rilievo di Gemini G-20261113-01 verificato da Claude.

Soglia sotto l'ipotesi nulla (Sharpe per trade):
    SR0 = sqrt(V) × [ (1 − γ) Φ⁻¹(1 − 1/N) + γ Φ⁻¹(1 − 1/(N e)) ]
con V = varianza degli Sharpe stimati delle N prove. Il codice di prima usava V = 1 (nessuna scala): con N ≥ 2 la
soglia diventava 0,52 (N = 2) o 1,90 (N = 20) per trade, cioè bocciava qualunque strategia reale.
Senza altre informazioni V è la varianza dello stimatore sotto l'ipotesi nulla: 1/(T − 1).

I valori attesi sono calcolati a parte (statistics.NormalDist, γ = 0,5772156649), non dal codice sotto test:
  N=20, T=600, SR=0,10           → SR0 = 0,077661, DSR = 0,707253
  N=20, T=600, SR=0,10, V=0,01   → SR0 = 0,190071, DSR = 0,013941
  N=5,  T=100, SR=0,20           → SR0 = 0,119860, DSR = 0,785097
  N=2,  T=600, SR=0,05           → SR0 = 0,021237, DSR = 0,759137
Uso (dalla radice del repository): python3 -s -B -W error -m unittest brain.laboratorio.tests.test_dsr_scala
"""
import json
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.guardian.g0.strumenti import Strumento                       # noqa: E402
from brain.laboratorio.backtester import DSRCalculator, Direction, Portfolio   # noqa: E402
from brain.laboratorio.backtester.events import TradeRecord             # noqa: E402

DSR = DSRCalculator.calculate_dsr_analytical


def portafoglio(pnls):
    s = Strumento(simbolo="EURUSD", classe="fx", valuta_base="EUR", valuta_profitto="USD",
                  dimensione_contratto=Decimal("100000"), fonte="test")
    p = Portfolio(s, initial_cash=Decimal("100000.00"))
    t0 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for i, x in enumerate(pnls):
        p.trade_history.append(TradeRecord(
            symbol="EURUSD", direction=Direction.BUY, quantity=Decimal("1"),
            entry_time=t0 + timedelta(hours=i), entry_price=Decimal("1.08"),
            exit_time=t0 + timedelta(hours=i + 1), exit_price=Decimal("1.081"),
            gross_pnl=x, net_pnl=x, total_commission=Decimal("0"), total_spread_cost=Decimal("0"),
            total_slippage=Decimal("0"), exit_reason="TEST"))
    return p


class TestSogliaConScala(unittest.TestCase):
    def test_vettori_calcolati_a_parte(self):
        for sr, n, t, v, atteso in ((0.10, 20, 600, None, 0.707253), (0.10, 20, 600, 0.01, 0.013941),
                                    (0.20, 5, 100, None, 0.785097), (0.05, 2, 600, None, 0.759137)):
            dsr, _ = DSR(sr, n, t, varianza_sr_prove=v) if v is not None else DSR(sr, n, t)
            self.assertAlmostEqual(dsr, atteso, places=5, msg=f"N={n} T={t} SR={sr} V={v}")

    def test_una_sola_prova_soglia_zero(self):
        """N = 1: SR0 = 0 (benchmark), quindi DSR = Φ(SR / errore standard), come prima della correzione."""
        dsr, se = DSR(0.10, 1, 600)
        self.assertAlmostEqual(se, ((1 + 0.5 * 0.01) / 599) ** 0.5, places=12)
        self.assertAlmostEqual(dsr, 0.992684, places=5)

    def test_piu_prove_soglia_piu_alta(self):
        self.assertGreater(DSR(0.10, 5, 600)[0], DSR(0.10, 50, 600)[0])

    def test_varianza_non_valida_rifiutata(self):
        for v in (0.0, -0.01, float("nan"), float("inf")):
            with self.assertRaises(ValueError, msg=repr(v)):
                DSR(0.10, 20, 600, varianza_sr_prove=v)


class TestInputNonValidi(unittest.TestCase):
    """Rilievo di Gemini G3-01: con SR = NaN la probabilità diventava 1,0 (min(1.0, nan) == 1.0 in Python) e
    N <= 0 era trattato come N = 1."""

    def test_valori_non_finiti_rifiutati(self):
        base = dict(sharpe_estimated=0.10, num_trials=20, track_record_length=600, skewness=0.0, kurtosis=3.0,
                    benchmark_sharpe=0.0)
        for campo in ("sharpe_estimated", "skewness", "kurtosis", "benchmark_sharpe"):
            for x in (float("nan"), float("inf"), float("-inf")):
                with self.assertRaises(ValueError, msg=f"{campo}={x}"):
                    DSR(**dict(base, **{campo: x}))

    def test_numero_prove_non_valido(self):
        for n in (0, -3, 2.5, True):
            with self.assertRaises(ValueError, msg=repr(n)):
                DSR(0.10, n, 600)

    def test_lunghezza_non_intera(self):
        for t in (600.5, True):
            with self.assertRaises(ValueError, msg=repr(t)):
                DSR(0.10, 20, t)
        self.assertEqual(DSR(0.10, 20, 1), (None, None))             # caso patologico già previsto

    def test_nota_con_una_sola_prova(self):
        """Con N = 1 la soglia è 0 e nessuna varianza delle prove entra nel calcolo: la nota non deve citarla."""
        with tempfile.TemporaryDirectory() as tmp:
            pnls = [Decimal("100") if i % 2 == 0 else Decimal("-50") for i in range(35)]
            m = DSRCalculator.evaluate_portfolio(portafoglio(pnls), registry_path=Path(tmp) / "r.json", dry_run=True)
        nota = m["deflated_sharpe_ratio"].nota
        self.assertIn("N=1", nota)
        self.assertIn("soglia 0", nota)
        self.assertNotIn("varianza", nota)


class TestVarianzaDalRegistro(unittest.TestCase):
    """evaluate_portfolio usa V = max(1/(T − 1), varianza empirica degli Sharpe registrati + quello corrente):
    scelta prudente (STIMA di Claude). Con prove molto disperse la soglia sale."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_dsr_scala_"))
        self.pnls = [Decimal("100") if i % 2 == 0 else Decimal("-50") for i in range(35)]

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def registro(self, sharpe):
        path = self.tmp / f"reg_{len(list(self.tmp.iterdir()))}.json"
        trials = [{"trial_id": i + 1, "sharpe_ratio": s, "total_trades": 35} for i, s in enumerate(sharpe)]
        path.write_text(json.dumps({"protocol": "TRIAL_REGISTRY_V2", "total_trials": len(trials),
                                    "trials": trials}), encoding="utf-8")
        return path

    def valuta(self, path):
        m = DSRCalculator.evaluate_portfolio(portafoglio(self.pnls), registry_path=path, dry_run=True)
        return float(m["deflated_sharpe_ratio"].valore), m

    def test_senza_sharpe_registrati_varianza_nulla(self):
        dsr, m = self.valuta(self.registro([None, None]))
        sr = float(m["sharpe_ratio"].valore)
        atteso, _ = DSR(sr, 3, 35, float(m["skewness"].valore), float(m["kurtosis"].valore),
                        varianza_sr_prove=1 / 34)
        self.assertAlmostEqual(dsr, atteso, places=4)
        self.assertIn("N=3", m["deflated_sharpe_ratio"].nota)

    def test_prove_disperse_alzano_la_soglia(self):
        poco, _ = self.valuta(self.registro([None, None]))
        molto, m = self.valuta(self.registro(["0.9", "-0.9"]))
        self.assertLess(molto, poco)
        self.assertIn("varianza", m["deflated_sharpe_ratio"].nota)

    def test_prove_concentrate_non_abbassano_sotto_la_varianza_nulla(self):
        """Sharpe registrati quasi uguali al corrente: varianza empirica ~0, resta 1/(T − 1)."""
        _, m0 = self.valuta(self.registro([None, None]))
        sr = m0["sharpe_ratio"].valore
        uguali, _ = self.valuta(self.registro([str(sr), str(sr)]))
        nulla, _ = self.valuta(self.registro([None, None]))
        self.assertAlmostEqual(uguali, nulla, places=6)


if __name__ == "__main__":
    unittest.main()
