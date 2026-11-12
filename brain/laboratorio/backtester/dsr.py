"""
Calcolo Metriche di Rischio e Deflated Sharpe Ratio (DSR).
Implementazione analitica conforme a Bailey & Lopez de Prado (2014):
"The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality".
Collegato a trial_registry.json per tracciare globalmente il numero di tentativi N.
"""

import json
import math
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import List, Dict, Any, Optional

from .portfolio import Portfolio


class DSRCalculator:
    def __init__(self, registry_path: Optional[Path] = None):
        if registry_path is None:
            # Di default in brain/laboratorio/trial_registry.json
            repo_root = Path(__file__).resolve().parents[3]
            self.registry_path = repo_root / "brain" / "laboratorio" / "trial_registry.json"
        else:
            self.registry_path = Path(registry_path)

        self._ensure_registry_exists()

    def _ensure_registry_exists(self):
        if not self.registry_path.exists():
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            initial_data = {
                "protocol": "TRIAL_REGISTRY_V1",
                "epistemic_type": "REGOLA",
                "condition_h": "{H_trial_counter_integro}",
                "total_trials": 0,
                "trials": [],
            }
            with open(self.registry_path, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=2)

    def register_trial(self, strategy_name: str, parameters: Dict[str, Any], metrics: Dict[str, Any]) -> int:
        """
        Registra una prova nel contatore globale N e restituisce il nuovo valore di N.
        """
        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["total_trials"] += 1
        n = data["total_trials"]

        record = {
            "trial_id": n,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "strategy_name": strategy_name,
            "parameters": parameters,
            "sharpe_ratio": float(metrics.get("sharpe_ratio", 0.0)),
            "deflated_sharpe_ratio": float(metrics.get("deflated_sharpe_ratio", 0.0)),
            "total_trades": metrics.get("total_trades", 0),
        }
        data["trials"].append(record)

        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return n

    def get_total_trials(self) -> int:
        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["total_trials"]

    @staticmethod
    def calculate_dsr(
        sharpe_estimated: float,
        num_trials: int,
        track_record_length: int,
        skewness: float = 0.0,
        kurtosis: float = 3.0,
        benchmark_sharpe: float = 0.0,
    ) -> float:
        """
        Calcola il Deflated Sharpe Ratio (DSR).
        num_trials: N (numero cumulativo di strategie/parametri testati)
        track_record_length: T (numero di osservazioni/rendimenti)
        skewness: gamma_3
        kurtosis: gamma_4 (3.0 per normale)
        """
        if track_record_length <= 1:
            return 0.0

        if num_trials <= 1:
            # Con 1 solo trial, SR* = benchmark_sharpe
            sr_star = benchmark_sharpe
        else:
            # Stima di Bailey & Lopez de Prado del max Sharpe sotto ipotesi nulla H0: SR=0
            # E[max(SR_N)] ~ (1 - gamma_euler) * Z^-1(1 - 1/N) + gamma_euler * Z^-1(1 - 1/(N*e))
            # Approssimazione standard asintotica di estremi:
            # SR* ~ sqrt(2 * ln(N)) + euler_gamma / sqrt(2 * ln(N))
            gamma_euler = 0.5772156649
            ln_n = math.log(num_trials)
            denom = math.sqrt(2.0 * ln_n)
            sr_star = denom + (gamma_euler / denom)

        # Deviazione standard asintotica dello Sharpe sotto non-normalita'
        # V(SR) = (1 - gamma_3 * SR + ((gamma_4 - 1) / 4) * SR^2) / (T - 1)
        sr = sharpe_estimated
        variance_term = 1.0 - (skewness * sr) + (((kurtosis - 1.0) / 4.0) * (sr ** 2))
        if variance_term <= 0:
            variance_term = 1e-6
        std_sr = math.sqrt(variance_term / (track_record_length - 1))

        if std_sr <= 0:
            return 0.0

        # Statistica z
        z_stat = (sr - sr_star) / std_sr

        # CDF normale standard Phi(z) = 0.5 * (1 + erf(z / sqrt(2)))
        dsr_prob = 0.5 * (1.0 + math.erf(z_stat / math.sqrt(2.0)))
        return max(0.0, min(1.0, dsr_prob))

    @classmethod
    def evaluate_portfolio(cls, portfolio: Portfolio, registry_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Calcola tutte le metriche prestazionali ed aggiorna il DSR.
        """
        trades = portfolio.trade_history
        if not trades:
            return {
                "total_trades": 0,
                "gross_pnl": Decimal("0.00"),
                "net_pnl": Decimal("0.00"),
                "win_rate": 0.0,
                "profit_factor": 0.0,
                "sharpe_ratio": 0.0,
                "deflated_sharpe_ratio": 0.0,
                "max_drawdown": Decimal("0.00"),
            }

        net_pnls = [float(t.net_pnl) for t in trades]
        t_len = len(net_pnls)
        wins = [p for p in net_pnls if p > 0]
        losses = [p for p in net_pnls if p < 0]

        win_rate = len(wins) / t_len if t_len > 0 else 0.0
        gross_pnl = sum([t.gross_pnl for t in trades], Decimal("0.00"))
        net_pnl = sum([t.net_pnl for t in trades], Decimal("0.00"))

        sum_wins = sum(wins)
        sum_losses = abs(sum(losses))
        profit_factor = float(sum_wins / sum_losses) if sum_losses > 0 else (999.0 if sum_wins > 0 else 0.0)

        # Media e Deviazione Standard
        mean_pnl = sum(net_pnls) / t_len
        if t_len > 1:
            var_pnl = sum((x - mean_pnl) ** 2 for x in net_pnls) / (t_len - 1)
            std_pnl = math.sqrt(var_pnl)
        else:
            std_pnl = 0.0

        sharpe = (mean_pnl / std_pnl) if std_pnl > 0 else 0.0

        # Skewness e Kurtosis
        if std_pnl > 0 and t_len > 2:
            skew = sum(((x - mean_pnl) / std_pnl) ** 3 for x in net_pnls) / t_len
            kurt = sum(((x - mean_pnl) / std_pnl) ** 4 for x in net_pnls) / t_len
        else:
            skew = 0.0
            kurt = 3.0

        # Calcolo DSR
        calc = cls(registry_path=registry_path)
        trials = calc.get_total_trials() + 1  # Conta questa prova
        dsr = cls.calculate_dsr(
            sharpe_estimated=sharpe,
            num_trials=trials,
            track_record_length=t_len,
            skewness=skew,
            kurtosis=kurt,
        )

        # Calcolo Max Drawdown su equity curve
        peak = portfolio.initial_cash
        max_dd = Decimal("0.00")
        for _, eq in portfolio.equity_curve:
            if eq > peak:
                peak = eq
            dd = peak - eq
            if dd > max_dd:
                max_dd = dd

        return {
            "total_trades": t_len,
            "gross_pnl": gross_pnl,
            "net_pnl": net_pnl,
            "win_rate": round(win_rate, 4),
            "profit_factor": round(profit_factor, 4),
            "sharpe_ratio": round(sharpe, 4),
            "deflated_sharpe_ratio": round(dsr, 6),
            "max_drawdown": max_dd,
            "skewness": round(skew, 4),
            "kurtosis": round(kurt, 4),
        }
