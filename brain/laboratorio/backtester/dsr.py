"""
Calcolo Metriche di Rischio e Deflated Sharpe Ratio (DSR) conforme a Bailey & Lopez de Prado (2014).
Governance Epistemica:
- Restituisce oggetti Valore (tipo="STIMA", operazione="inferenza").
- Se total_trades < 30 o varianza nulla, restituisce incertezza = NON_STIMABILE e valore = None (MAI float 0.0!).
- Tutti i calcoli di momenti usano Decimal, convertendo solo per le funzioni trascendenti (erf, sqrt, log).
- Integrazione automatica con trial_registry.json (salvo dry_run=True).
"""

import json
import math
import statistics
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from brain.guardian.g0.valori import Valore, NON_STIMABILE
from .portfolio import Portfolio


class DSRCalculator:
    def __init__(self, registry_path: Optional[Path] = None):
        if registry_path is None:
            repo_root = Path(__file__).resolve().parents[3]
            self.registry_path = repo_root / "brain" / "laboratorio" / "trial_registry.json"
        else:
            self.registry_path = Path(registry_path)

        self._ensure_registry_exists()

    def _ensure_registry_exists(self):
        if not self.registry_path.exists():
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            initial_data = {
                "protocol": "TRIAL_REGISTRY_V2",
                "epistemic_type": "REGOLA",
                "condition_h": "{H_trial_counter_integro}",
                "total_trials": 0,
                "trials": [],
            }
            with open(self.registry_path, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=2)

    def register_trial(
        self,
        strategy_name: str,
        parameters: Dict[str, Any],
        metrics: Dict[str, Any],
    ) -> int:
        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["total_trials"] += 1
        n = data["total_trials"]

        sr_val = metrics.get("sharpe_ratio")
        dsr_val = metrics.get("deflated_sharpe_ratio")

        record = {
            "trial_id": n,
            "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "strategy_name": strategy_name,
            "parameters": {k: str(v) if isinstance(v, Decimal) else v for k, v in parameters.items()},
            "sharpe_ratio": str(sr_val.valore) if (isinstance(sr_val, Valore) and sr_val.valore is not None) else None,
            "deflated_sharpe_ratio": str(dsr_val.valore) if (isinstance(dsr_val, Valore) and dsr_val.valore is not None) else None,
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
    def calculate_dsr_analytical(
        sharpe_estimated: float,
        num_trials: int,
        track_record_length: int,
        skewness: float = 0.0,
        kurtosis: float = 3.0,
        benchmark_sharpe: float = 0.0,
    ) -> Tuple[float, float]:
        """
        Restituisce (dsr_probability, std_error_sr).
        """
        if track_record_length <= 1:
            return 0.0, 1.0

        if num_trials <= 1:
            sr_star = benchmark_sharpe
        else:
            gamma_euler = 0.57721566490153286060
            inv_cdf = statistics.NormalDist().inv_cdf
            sr_star = (1.0 - gamma_euler) * inv_cdf(1.0 - 1.0 / num_trials) + gamma_euler * inv_cdf(1.0 - 1.0 / (num_trials * math.e))

        sr = sharpe_estimated
        variance_term = 1.0 - (skewness * sr) + (((kurtosis - 1.0) / 4.0) * (sr ** 2))
        if variance_term <= 0:
            variance_term = 1e-6
        std_sr = math.sqrt(variance_term / (track_record_length - 1))

        if std_sr <= 0:
            return 0.0, 1.0

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
        Se total_trades < 30 o varianza nulla, restituisce Valore con incertezza NON STIMABILE.
        Registra automaticamente in trial_registry.json salvo dry_run=True.
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

        calc = cls(registry_path=registry_path)

        # Controllo rigore inferenziale: Minimo 30 trade per validità statistica
        if t_len < 30:
            sharpe_valore = Valore(
                valore=None,
                unita="",
                tipo="STIMA",
                operazione="inferenza",
                fonte="DSRCalculator",
                incertezza=NON_STIMABILE,
                nota=f"Campione insufficiente ({t_len} < 30 trades richiesti per inferenza)",
            )
            dsr_valore = Valore(
                valore=None,
                unita="",
                tipo="STIMA",
                operazione="inferenza",
                fonte="DSRCalculator",
                incertezza=NON_STIMABILE,
                nota=f"Campione insufficiente ({t_len} < 30 trades)",
            )
            skew_valore = Valore(
                valore=None,
                unita="",
                tipo="STIMA",
                operazione="inferenza",
                fonte="DSRCalculator",
                incertezza=NON_STIMABILE,
                nota="Campione insufficiente",
            )
            kurt_valore = Valore(
                valore=None,
                unita="",
                tipo="STIMA",
                operazione="inferenza",
                fonte="DSRCalculator",
                incertezza=NON_STIMABILE,
                nota="Campione insufficiente",
            )
        else:
            # Calcolo momenti su Decimal convertendo a float solo per funzioni trascendenti
            mean_pnl = sum(net_pnls_dec, Decimal("0.00")) / Decimal(t_len)
            diffs_sq = [(x - mean_pnl) ** 2 for x in net_pnls_dec]
            var_pnl = sum(diffs_sq, Decimal("0.00")) / Decimal(t_len - 1)

            if var_pnl <= Decimal("0"):
                sharpe_valore = Valore(
                    valore=None,
                    unita="",
                    tipo="STIMA",
                    operazione="inferenza",
                    fonte="DSRCalculator",
                    incertezza=NON_STIMABILE,
                    nota="Varianza nulla nei rendimenti",
                )
                dsr_valore = Valore(
                    valore=None,
                    unita="",
                    tipo="STIMA",
                    operazione="inferenza",
                    fonte="DSRCalculator",
                    incertezza=NON_STIMABILE,
                    nota="Varianza nulla nei rendimenti",
                )
                skew_valore = Valore(valore=None, unita="", tipo="STIMA", operazione="inferenza", fonte="DSRCalculator", incertezza=NON_STIMABILE)
                kurt_valore = Valore(valore=None, unita="", tipo="STIMA", operazione="inferenza", fonte="DSRCalculator", incertezza=NON_STIMABILE)
            else:
                std_pnl = Decimal(str(math.sqrt(float(var_pnl))))
                sharpe_float = float(mean_pnl / std_pnl)

                diffs_norm = [float((x - mean_pnl) / std_pnl) for x in net_pnls_dec]
                skew_float = sum(x ** 3 for x in diffs_norm) / t_len
                kurt_float = sum(x ** 4 for x in diffs_norm) / t_len

                trials = calc.get_total_trials() + (0 if dry_run else 1)
                dsr_float, std_sr = cls.calculate_dsr_analytical(
                    sharpe_estimated=sharpe_float,
                    num_trials=max(1, trials),
                    track_record_length=t_len,
                    skewness=skew_float,
                    kurtosis=kurt_float,
                )

                sharpe_valore = Valore(
                    valore=Decimal(str(round(sharpe_float, 4))),
                    unita="",
                    tipo="STIMA",
                    operazione="inferenza",
                    fonte="DSRCalculator",
                    incertezza=f"+/-{round(std_sr, 4)}",
                    nota="Sharpe stimato su PnL netto",
                )
                dsr_valore = Valore(
                    valore=Decimal(str(round(dsr_float, 6))),
                    unita="",
                    tipo="STIMA",
                    operazione="inferenza",
                    fonte="DSRCalculator",
                    incertezza=f"+/-{round(std_sr, 4)}",
                    nota=f"Deflated Sharpe Ratio (N={max(1, trials)} trials)",
                )
                skew_valore = Valore(
                    valore=Decimal(str(round(skew_float, 4))),
                    unita="",
                    tipo="STIMA",
                    operazione="inferenza",
                    fonte="DSRCalculator",
                    incertezza=f"+/-{round(math.sqrt(6.0 / t_len), 4)}",
                )
                kurt_valore = Valore(
                    valore=Decimal(str(round(kurt_float, 4))),
                    unita="",
                    tipo="STIMA",
                    operazione="inferenza",
                    fonte="DSRCalculator",
                    incertezza=f"+/-{round(math.sqrt(24.0 / t_len), 4)}",
                )

        results = {
            "total_trades": t_len,
            "gross_pnl": gross_pnl_dec,
            "net_pnl": net_pnl_dec,
            "win_rate": win_rate_dec,
            "profit_factor": profit_factor_dec,
            "sharpe_ratio": sharpe_valore,
            "deflated_sharpe_ratio": dsr_valore,
            "skewness": skew_valore,
            "kurtosis": kurt_valore,
            "max_drawdown_close": portfolio.max_drawdown_close,
            "max_drawdown_intrabar": portfolio.max_drawdown_intrabar,
        }

        # Registrazione automatica nel trial registry
        if not dry_run:
            calc.register_trial(
                strategy_name=strategy_name,
                parameters=parameters,
                metrics=results,
            )

        return results
