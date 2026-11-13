"""
Calcolo Metriche di Rischio e Deflated Sharpe Ratio (DSR) conforme a Bailey & Lopez de Prado (2014).
Governance Epistemica:
- Restituisce oggetti Valore (tipo="STIMA", operazione="inferenza").
- Se total_trades < 30, varianza nulla o variance_term <= 0, restituisce incertezza = NON_STIMABILE e valore = None.
- Tutti i calcoli di momenti usano Decimal, convertendo solo per le funzioni trascendenti.
- Integrazione atomica e concorrente (con lock esclusivo) con trial_registry.json;
  con dry_run=True e' rigorosamente readonly (non crea ne' scrive su disco) e include il trial nel conteggio N = total_trials + 1.
"""

from contextlib import contextmanager
import json
import math
import os
import statistics
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

try:
    import fcntl
except ImportError:
    fcntl = None

from brain.guardian.g0.valori import Valore, NON_STIMABILE
from .portfolio import Portfolio


class DSRCalculator:
    def __init__(self, registry_path: Optional[Path] = None, readonly: bool = False):
        if registry_path is None:
            repo_root = Path(__file__).resolve().parents[3]
            self.registry_path = repo_root / "brain" / "laboratorio" / "trial_registry.json"
        else:
            self.registry_path = Path(registry_path)
        self.readonly = readonly

    @contextmanager
    def _exclusive_lock(self, timeout_seconds: float = 10.0):
        """
        Lock esclusivo cross-processo basato su fcntl.flock (Unix) con fallback su file lock O_EXCL.
        """
        lock_path = self.registry_path.with_name(self.registry_path.name + ".lock")
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        if fcntl is not None:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_RDWR, 0o600)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX)
                yield
            finally:
                try:
                    fcntl.flock(fd, fcntl.LOCK_UN)
                finally:
                    os.close(fd)
        else:
            deadline = time.monotonic() + timeout_seconds
            while True:
                try:
                    fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                    os.close(fd)
                    break
                except FileExistsError:
                    if time.monotonic() >= deadline:
                        raise TimeoutError(f"Timeout acquisizione lock su {lock_path}")
                    time.sleep(0.01)
            try:
                yield
            finally:
                try:
                    os.unlink(str(lock_path))
                except FileNotFoundError:
                    pass

    @staticmethod
    def _default_registry_data() -> Dict[str, Any]:
        return {
            "protocol": "TRIAL_REGISTRY_V2",
            "epistemic_type": "REGOLA",
            "condition_h": "{H_trial_counter_integro}",
            "total_trials": 0,
            "trials": [],
        }

    def _read_or_init_unlocked(self, create_if_missing: bool) -> Dict[str, Any]:
        if not self.registry_path.exists():
            data = self._default_registry_data()
            if create_if_missing and not self.readonly:
                self.registry_path.parent.mkdir(parents=True, exist_ok=True)
                self._write_atomic_unlocked(data)
            return data
        with open(self.registry_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_atomic_unlocked(self, data: Dict[str, Any]) -> None:
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.registry_path.with_name(f".{self.registry_path.name}.{os.getpid()}.tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(str(tmp_path), str(self.registry_path))

    @staticmethod
    def _build_record(
        trial_id: int,
        strategy_name: str,
        parameters: Dict[str, Any],
        metrics: Dict[str, Any],
    ) -> Dict[str, Any]:
        sr_val = metrics.get("sharpe_ratio")
        dsr_val = metrics.get("deflated_sharpe_ratio")
        return {
            "trial_id": trial_id,
            "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "strategy_name": strategy_name,
            "parameters": {k: str(v) if isinstance(v, Decimal) else v for k, v in parameters.items()},
            "sharpe_ratio": str(sr_val.valore) if (isinstance(sr_val, Valore) and sr_val.valore is not None) else None,
            "deflated_sharpe_ratio": str(dsr_val.valore) if (isinstance(dsr_val, Valore) and dsr_val.valore is not None) else None,
            "total_trades": metrics.get("total_trades", 0),
        }

    def register_trial(
        self,
        strategy_name: str,
        parameters: Dict[str, Any],
        metrics: Dict[str, Any],
    ) -> int:
        if self.readonly:
            raise PermissionError("Impossibile registrare trial in modalita' readonly (dry_run=True).")
        with self._exclusive_lock():
            data = self._read_or_init_unlocked(create_if_missing=True)
            data["total_trials"] += 1
            n = data["total_trials"]
            record = self._build_record(n, strategy_name, parameters, metrics)
            data["trials"].append(record)
            self._write_atomic_unlocked(data)
            return n

    @staticmethod
    def _sharpe_registrati(data: Dict[str, Any]) -> List[float]:
        """Sharpe delle prove già registrate (quelle con Sharpe stimabile), come float finiti."""
        out = []
        for t in data.get("trials", []):
            s = t.get("sharpe_ratio")
            if s is None:
                continue
            x = float(s)
            if not math.isfinite(x):
                raise ValueError(f"trial_registry: sharpe_ratio non finito nella prova {t.get('trial_id')!r}")
            out.append(x)
        return out

    def get_total_trials(self) -> int:
        if not self.registry_path.exists():
            return 0
        if self.readonly:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return int(data.get("total_trials", 0))
        with self._exclusive_lock():
            data = self._read_or_init_unlocked(create_if_missing=False)
            return int(data.get("total_trials", 0))

    @staticmethod
    def calculate_dsr_analytical(
        sharpe_estimated: float,
        num_trials: int,
        track_record_length: int,
        skewness: float = 0.0,
        kurtosis: float = 3.0,
        benchmark_sharpe: float = 0.0,
        varianza_sr_prove: Optional[float] = None,
    ) -> Tuple[Optional[float], Optional[float]]:
        """
        Restituisce (dsr_probability, std_error_sr), oppure (None, None) in caso patologico
        (es. variance_term <= 0 o track_record_length <= 1).

        Soglia con N > 1 prove (Bailey e López de Prado 2014):
            SR0 = sqrt(V) * [(1 - gamma) * inv_cdf(1 - 1/N) + gamma * inv_cdf(1 - 1/(N e))]
        V = varianza degli Sharpe stimati delle prove; se non è data, la varianza dello stimatore sotto l'ipotesi
        nulla, 1/(T - 1). Senza sqrt(V) (versione precedente) la soglia era in unità sbagliate e, per Sharpe per
        trade, bocciava qualunque strategia già con N = 2.
        """
        for nome, x in (("sharpe_estimated", sharpe_estimated), ("skewness", skewness), ("kurtosis", kurtosis),
                        ("benchmark_sharpe", benchmark_sharpe)):
            if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
                raise ValueError(f"{nome} deve essere un numero finito: {x!r}")       # NaN diventava DSR = 1,0
        if isinstance(num_trials, bool) or not isinstance(num_trials, int) or num_trials < 1:
            raise ValueError(f"num_trials deve essere un intero >= 1: {num_trials!r}")
        if isinstance(track_record_length, bool) or not isinstance(track_record_length, int):
            raise ValueError(f"track_record_length deve essere un intero: {track_record_length!r}")
        if varianza_sr_prove is not None and not (math.isfinite(varianza_sr_prove) and varianza_sr_prove > 0):
            raise ValueError(f"varianza_sr_prove deve essere finita e positiva: {varianza_sr_prove!r}")
        if track_record_length <= 1:
            return None, None

        if num_trials <= 1:
            sr_star = benchmark_sharpe
        else:
            gamma_euler = 0.57721566490153286060
            inv_cdf = statistics.NormalDist().inv_cdf
            v = varianza_sr_prove if varianza_sr_prove is not None else 1.0 / (track_record_length - 1)
            sr_star = math.sqrt(v) * (
                (1.0 - gamma_euler) * inv_cdf(1.0 - 1.0 / num_trials)
                + gamma_euler * inv_cdf(1.0 - 1.0 / (num_trials * math.e))
            )

        sr = sharpe_estimated
        variance_term = 1.0 - (skewness * sr) + (((kurtosis - 1.0) / 4.0) * (sr ** 2))
        if variance_term <= 0:
            return None, None
        std_sr = math.sqrt(variance_term / (track_record_length - 1))

        if std_sr <= 0:
            return None, None

        z_stat = (sr - sr_star) / std_sr
        dsr_prob = 0.5 * (1.0 + math.erf(z_stat / math.sqrt(2.0)))
        return max(0.0, min(1.0, dsr_prob)), std_sr

    @classmethod
    def evaluate_portfolio(
        cls,
        portfolio: Portfolio,
        strategy_name: str = "Strategy_Evaluation",
        parameters: Optional[Dict[str, Any]] = None,
        registry_path: Optional[Path] = None,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Valuta il portafoglio.
        Se total_trades < 30, varianza nulla o variance_term <= 0, restituisce Valore con incertezza NON STIMABILE.
        Con dry_run=True e' readonly (non crea ne' scrive trial_registry.json) e conta N = total_trials + 1.
        Con dry_run=False legge N, calcola DSR e registra il trial atomicamente sotto lock esclusivo.
        """
        trades = portfolio.trade_history
        t_len = len(trades)
        parameters = parameters or {}

        # Metriche deterministiche
        net_pnls_dec = [t.net_pnl for t in trades]
        gross_pnl_dec = sum([t.gross_pnl for t in trades], Decimal("0.00"))
        net_pnl_dec = sum(net_pnls_dec, Decimal("0.00"))

        wins = [p for p in net_pnls_dec if p > Decimal("0")]
        losses = [p for p in net_pnls_dec if p < Decimal("0")]
        win_rate_dec = (Decimal(len(wins)) / Decimal(t_len)) if t_len > 0 else Decimal("0.00")
        sum_wins = sum(wins, Decimal("0.00"))
        sum_losses = abs(sum(losses, Decimal("0.00")))
        profit_factor_dec = (sum_wins / sum_losses) if sum_losses > Decimal("0") else (
            Decimal("999.00") if sum_wins > Decimal("0") else Decimal("0.00")
        )

        calc = cls(registry_path=registry_path, readonly=dry_run)

        def _build_inferential_metrics(num_trials: int, sr_registrati: List[float]) -> Tuple[Valore, Valore, Valore, Valore]:
            if t_len < 30:
                return (
                    Valore(
                        valore=None, unita="", tipo="STIMA", operazione="inferenza",
                        fonte="DSRCalculator", incertezza=NON_STIMABILE,
                        nota=f"Campione insufficiente ({t_len} < 30 trades richiesti per inferenza)",
                    ),
                    Valore(
                        valore=None, unita="", tipo="STIMA", operazione="inferenza",
                        fonte="DSRCalculator", incertezza=NON_STIMABILE,
                        nota=f"Campione insufficiente ({t_len} < 30 trades)",
                    ),
                    Valore(
                        valore=None, unita="", tipo="STIMA", operazione="inferenza",
                        fonte="DSRCalculator", incertezza=NON_STIMABILE,
                        nota="Campione insufficiente",
                    ),
                    Valore(
                        valore=None, unita="", tipo="STIMA", operazione="inferenza",
                        fonte="DSRCalculator", incertezza=NON_STIMABILE,
                        nota="Campione insufficiente",
                    ),
                )

            mean_pnl = sum(net_pnls_dec, Decimal("0.00")) / Decimal(t_len)
            diffs_sq = [(x - mean_pnl) ** 2 for x in net_pnls_dec]
            var_pnl = sum(diffs_sq, Decimal("0.00")) / Decimal(t_len - 1)

            if var_pnl <= Decimal("0"):
                return (
                    Valore(valore=None, unita="", tipo="STIMA", operazione="inferenza", fonte="DSRCalculator", incertezza=NON_STIMABILE, nota="Varianza nulla nei rendimenti"),
                    Valore(valore=None, unita="", tipo="STIMA", operazione="inferenza", fonte="DSRCalculator", incertezza=NON_STIMABILE, nota="Varianza nulla nei rendimenti"),
                    Valore(valore=None, unita="", tipo="STIMA", operazione="inferenza", fonte="DSRCalculator", incertezza=NON_STIMABILE),
                    Valore(valore=None, unita="", tipo="STIMA", operazione="inferenza", fonte="DSRCalculator", incertezza=NON_STIMABILE),
                )

            std_pnl = Decimal(str(math.sqrt(float(var_pnl))))
            sharpe_float = float(mean_pnl / std_pnl)
            diffs_norm = [float((x - mean_pnl) / std_pnl) for x in net_pnls_dec]
            skew_float = sum(x ** 3 for x in diffs_norm) / t_len
            kurt_float = sum(x ** 4 for x in diffs_norm) / t_len

            # V = max(varianza sotto l'ipotesi nulla, varianza empirica degli Sharpe delle prove): scelta prudente
            # (STIMA di Claude, 13/11/2026). Prove molto disperse alzano la soglia; prove quasi uguali non la
            # abbassano sotto 1/(T - 1).
            v_nulla = 1.0 / (t_len - 1)
            campione = sr_registrati + [sharpe_float]
            v_emp = statistics.variance(campione) if len(campione) >= 2 else 0.0
            varianza = max(v_nulla, v_emp)
            dsr_float, std_sr = cls.calculate_dsr_analytical(
                sharpe_estimated=sharpe_float,
                num_trials=max(1, num_trials),
                track_record_length=t_len,
                skewness=skew_float,
                kurtosis=kurt_float,
                varianza_sr_prove=varianza,
            )

            skew_v = Valore(
                valore=Decimal(str(round(skew_float, 4))),
                unita="", tipo="STIMA", operazione="inferenza", fonte="DSRCalculator",
                incertezza=f"+/-{round(math.sqrt(6.0 / t_len), 4)}",
            )
            kurt_v = Valore(
                valore=Decimal(str(round(kurt_float, 4))),
                unita="", tipo="STIMA", operazione="inferenza", fonte="DSRCalculator",
                incertezza=f"+/-{round(math.sqrt(24.0 / t_len), 4)}",
            )

            if dsr_float is None or std_sr is None:
                sharpe_v = Valore(
                    valore=None,
                    unita="", tipo="STIMA", operazione="inferenza", fonte="DSRCalculator",
                    incertezza=NON_STIMABILE,
                    nota="Errore standard SR non stimabile (variance_term <= 0)",
                )
                dsr_v = Valore(
                    valore=None, unita="", tipo="STIMA", operazione="inferenza", fonte="DSRCalculator",
                    incertezza=NON_STIMABILE,
                    nota="Varianza stimatore DSR patologica (variance_term <= 0)",
                )
            else:
                sharpe_v = Valore(
                    valore=Decimal(str(round(sharpe_float, 4))),
                    unita="", tipo="STIMA", operazione="inferenza", fonte="DSRCalculator",
                    incertezza=f"+/-{round(std_sr, 4)}",
                    nota="Sharpe stimato su PnL netto",
                )
                dsr_v = Valore(
                    valore=Decimal(str(round(dsr_float, 6))),
                    unita="", tipo="STIMA", operazione="inferenza", fonte="DSRCalculator",
                    incertezza=f"+/-{round(std_sr, 4)}",
                    nota=(f"Deflated Sharpe Ratio (N={max(1, num_trials)} trials; soglia 0: nessuna selezione fra più "
                          f"prove)" if num_trials <= 1 else
                          f"Deflated Sharpe Ratio (N={num_trials} trials; varianza degli Sharpe = "
                          f"{'empirica delle prove' if v_emp > v_nulla else 'sotto ipotesi nulla 1/(T-1)'} "
                          f"{round(varianza, 6)})"),
                )
            return sharpe_v, dsr_v, skew_v, kurt_v

        def _assemble_results(sr_v: Valore, dsr_v: Valore, skew_v: Valore, kurt_v: Valore) -> Dict[str, Any]:
            return {
                "total_trades": t_len,
                "gross_pnl": gross_pnl_dec,
                "net_pnl": net_pnl_dec,
                "win_rate": win_rate_dec,
                "profit_factor": profit_factor_dec,
                "sharpe_ratio": sr_v,
                "deflated_sharpe_ratio": dsr_v,
                "skewness": skew_v,
                "kurtosis": kurt_v,
                "max_drawdown_close": portfolio.max_drawdown_close,
                "max_drawdown_intrabar": portfolio.max_drawdown_intrabar,
            }

        if dry_run:
            # Readonly: non crea ne' modifica trial_registry.json, usa N = total_trials + 1
            if calc.registry_path.exists():
                with open(calc.registry_path, "r", encoding="utf-8") as f:
                    dati_reg = json.load(f)
            else:
                dati_reg = cls._default_registry_data()
            trials = int(dati_reg.get("total_trials", 0)) + 1
            sr_v, dsr_v, skew_v, kurt_v = _build_inferential_metrics(trials, cls._sharpe_registrati(dati_reg))
            return _assemble_results(sr_v, dsr_v, skew_v, kurt_v)

        # Operazione atomica sotto lock esclusivo: lettura N, calcolo DSR, incremento e scrittura
        with calc._exclusive_lock():
            data = calc._read_or_init_unlocked(create_if_missing=True)
            trials = int(data.get("total_trials", 0)) + 1
            sr_v, dsr_v, skew_v, kurt_v = _build_inferential_metrics(trials, cls._sharpe_registrati(data))
            results = _assemble_results(sr_v, dsr_v, skew_v, kurt_v)
            data["total_trials"] = trials
            data["trials"].append(calc._build_record(trials, strategy_name, parameters, results))
            calc._write_atomic_unlocked(data)
            return results
