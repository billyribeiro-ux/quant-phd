"""Lab F6-L06-1: Net Sharpe Ratio and Turnover Optimization under Transaction Costs.

Evaluates the real-world economic impact of market frictions on machine learning return signals.
Compares unconstrained rebalancing against Garleanu & Pedersen (2013) turnover-penalized
dynamic execution under 25 bps round-trip transaction costs.
"""

from __future__ import annotations

import math

import numpy as np


def run_lab(seed: int = 42) -> dict[str, float]:
    """Execute transaction cost and turnover optimization simulation."""
    rng = np.random.default_rng(seed)

    n_assets = 30
    n_periods = 36
    cost_rate = 0.0025  # 25 bps round-trip transaction cost
    k_quant = n_assets // 3

    # Generate cross-sectional predictions and realized returns with realistic S/N
    raw_predictions = rng.normal(0.0, 0.020, size=(n_assets, n_periods))
    realized_returns = rng.normal(0.005, 0.050, size=(n_assets, n_periods)) + 0.15 * raw_predictions

    # Strategy 1: Raw Unconstrained Quantile Rebalancing
    w_raw_prev = np.zeros(n_assets, dtype=np.float64)
    gross_raw = np.zeros(n_periods, dtype=np.float64)
    net_raw = np.zeros(n_periods, dtype=np.float64)
    turnover_raw = np.zeros(n_periods, dtype=np.float64)

    for t in range(n_periods):
        ord_idx = np.argsort(raw_predictions[:, t])
        w = np.zeros(n_assets, dtype=np.float64)
        w[ord_idx[-k_quant:]] = 1.0 / k_quant
        w[ord_idx[:k_quant]] = -1.0 / k_quant

        to = float(np.sum(np.abs(w - w_raw_prev)))
        g = float(np.dot(w, realized_returns[:, t]))

        gross_raw[t] = g
        net_raw[t] = g - to * cost_rate
        turnover_raw[t] = to
        w_raw_prev = w

    # Strategy 2: Turnover-Penalized Partial Adjustment (Lambda = 0.35)
    lambda_param = 0.35
    w_smooth_prev = np.zeros(n_assets, dtype=np.float64)
    gross_smooth = np.zeros(n_periods, dtype=np.float64)
    net_smooth = np.zeros(n_periods, dtype=np.float64)
    turnover_smooth = np.zeros(n_periods, dtype=np.float64)

    for t in range(n_periods):
        ord_idx = np.argsort(raw_predictions[:, t])
        w_target = np.zeros(n_assets, dtype=np.float64)
        w_target[ord_idx[-k_quant:]] = 1.0 / k_quant
        w_target[ord_idx[:k_quant]] = -1.0 / k_quant

        w = (1.0 - lambda_param) * w_smooth_prev + lambda_param * w_target
        to = float(np.sum(np.abs(w - w_smooth_prev)))
        g = float(np.dot(w, realized_returns[:, t]))

        gross_smooth[t] = g
        net_smooth[t] = g - to * cost_rate
        turnover_smooth[t] = to
        w_smooth_prev = w

    sharpe_gross_raw = float(math.sqrt(12.0) * np.mean(gross_raw) / np.std(gross_raw, ddof=1))
    sharpe_net_raw = float(math.sqrt(12.0) * np.mean(net_raw) / np.std(net_raw, ddof=1))
    mean_to_raw = float(np.mean(turnover_raw))

    sharpe_gross_smooth = float(math.sqrt(12.0) * np.mean(gross_smooth) / np.std(gross_smooth, ddof=1))
    sharpe_net_smooth = float(math.sqrt(12.0) * np.mean(net_smooth) / np.std(net_smooth, ddof=1))
    mean_to_smooth = float(np.mean(turnover_smooth))

    return {
        "sharpe_gross_raw": sharpe_gross_raw,
        "sharpe_net_raw": sharpe_net_raw,
        "mean_turnover_raw": mean_to_raw,
        "sharpe_gross_smooth": sharpe_gross_smooth,
        "sharpe_net_smooth": sharpe_net_smooth,
        "mean_turnover_smooth": mean_to_smooth,
    }


def main() -> None:
    res = run_lab(seed=42)
    print("=== Lab F6-L06-1: Transaction Cost & Turnover Optimization ===")
    raw_msg = (
        f"Raw Strategy:    Gross Sharpe={res['sharpe_gross_raw']:.4f}, "
        f"Net Sharpe={res['sharpe_net_raw']:.4f}, Turnover={res['mean_turnover_raw']:.4f}"
    )
    smooth_msg = (
        f"Smooth Strategy: Gross Sharpe={res['sharpe_gross_smooth']:.4f}, "
        f"Net Sharpe={res['sharpe_net_smooth']:.4f}, Turnover={res['mean_turnover_smooth']:.4f}"
    )
    print(raw_msg)
    print(smooth_msg)


main()
