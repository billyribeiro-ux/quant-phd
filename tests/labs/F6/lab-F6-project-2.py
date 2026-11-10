"""Lab F6-project-2: Project Rung 2 Completion Problem Solution Twin.

Implements the three core mathematical engines of the ML cross-section study:
1. Zero-benchmark out-of-sample R2 (Gu, Kelly & Xiu 2020).
2. Long-short quantile spread portfolio with linear transaction cost deduction.
3. Minimum-norm ridgeless interpolator for underparameterized and overparameterized regimes.
"""

from __future__ import annotations

import math

import numpy as np


def compute_oos_r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute out-of-sample R-squared with zero return benchmark."""
    y_t = np.asarray(y_true, dtype=np.float64)
    y_p = np.asarray(y_pred, dtype=np.float64)
    denom = float(np.sum(y_t**2))
    num = float(np.sum((y_t - y_p) ** 2))
    return float(1.0 - (num / denom))


def construct_spread_portfolio(
    predictions: np.ndarray,
    returns: np.ndarray,
    cost_bps: float = 15.0,
) -> dict[str, float]:
    """Construct top-bottom quantile long-short spread portfolio net of costs."""
    n_assets, n_periods = predictions.shape
    k_quant = max(1, n_assets // 3)
    cost_factor = cost_bps * 1e-4

    prev_weights = np.zeros(n_assets, dtype=np.float64)
    gross_returns = np.zeros(n_periods, dtype=np.float64)
    net_returns = np.zeros(n_periods, dtype=np.float64)
    turnovers = np.zeros(n_periods, dtype=np.float64)

    for t in range(n_periods):
        scores = predictions[:, t]
        order = np.argsort(scores)

        weights = np.zeros(n_assets, dtype=np.float64)
        short_idx = order[:k_quant]
        long_idx = order[-k_quant:]

        weights[long_idx] = 1.0 / k_quant
        weights[short_idx] = -1.0 / k_quant

        turnover = float(np.sum(np.abs(weights - prev_weights)))
        cost = turnover * cost_factor

        r_gross = float(np.dot(weights, returns[:, t]))
        r_net = r_gross - cost

        gross_returns[t] = r_gross
        net_returns[t] = r_net
        turnovers[t] = turnover
        prev_weights = weights

    gross_mean = float(np.mean(gross_returns))
    gross_vol = float(np.std(gross_returns, ddof=1))
    gross_sharpe = float(math.sqrt(12.0) * (gross_mean / gross_vol)) if gross_vol > 1e-8 else 0.0

    net_mean = float(np.mean(net_returns))
    net_vol = float(np.std(net_returns, ddof=1))
    net_sharpe = float(math.sqrt(12.0) * (net_mean / net_vol)) if net_vol > 1e-8 else 0.0

    return {
        "gross_mean": gross_mean,
        "gross_sharpe": gross_sharpe,
        "net_mean": net_mean,
        "net_sharpe": net_sharpe,
        "mean_turnover": float(np.mean(turnovers)),
    }


def fit_minimum_norm_interpolator(z_train: np.ndarray, y_train: np.ndarray) -> np.ndarray:
    """Fit minimum-norm ridgeless interpolator across under- and over-parameterized regimes."""
    m_samples, d_features = z_train.shape
    if d_features <= m_samples:
        gram = z_train.T @ z_train + 1e-5 * np.eye(d_features)
        beta_hat = np.linalg.solve(gram, z_train.T @ y_train)
    else:
        dual_gram = z_train @ z_train.T + 1e-5 * np.eye(m_samples)
        alpha_dual = np.linalg.solve(dual_gram, y_train)
        beta_hat = z_train.T @ alpha_dual
    return beta_hat


def run_completion_lab(seed: int = 42) -> dict[str, float]:
    """Execute completion problem test cases."""
    rng = np.random.default_rng(seed)

    # 1. Test OOS R2
    y_true = np.array([0.02, -0.01, 0.03, -0.04, 0.05])
    y_pred = np.array([0.015, -0.005, 0.025, -0.030, 0.040])
    r2_val = compute_oos_r2(y_true, y_pred)

    # 2. Test spread portfolio
    n_a, t_p = 12, 10
    preds_sim = rng.normal(0.0, 0.02, size=(n_a, t_p))
    rets_sim = rng.normal(0.005, 0.04, size=(n_a, t_p)) + 0.2 * preds_sim
    perf = construct_spread_portfolio(preds_sim, rets_sim, cost_bps=15.0)

    # 3. Test minimum-norm interpolator
    z_under = rng.normal(0.0, 1.0, size=(50, 20))
    y_under = rng.normal(0.0, 1.0, size=50)
    beta_under = fit_minimum_norm_interpolator(z_under, y_under)

    z_over = rng.normal(0.0, 1.0, size=(30, 60))
    y_over = rng.normal(0.0, 1.0, size=30)
    beta_over = fit_minimum_norm_interpolator(z_over, y_over)

    norm_under = float(np.linalg.norm(beta_under))
    norm_over = float(np.linalg.norm(beta_over))

    return {
        "r2_oos": r2_val,
        "spread_gross_sharpe": perf["gross_sharpe"],
        "spread_net_sharpe": perf["net_sharpe"],
        "spread_mean_turnover": perf["mean_turnover"],
        "norm_beta_under": norm_under,
        "norm_beta_over": norm_over,
    }


def main() -> None:
    res = run_completion_lab(seed=42)
    print("=== Lab F6-project-2: Project Rung 2 Completion Problem Solution ===")
    print(f"Out-of-Sample R2:             {res['r2_oos']:.4f}")
    print(f"Spread Portfolio Gross Sharpe: {res['spread_gross_sharpe']:.4f}")
    print(f"Spread Portfolio Net Sharpe:   {res['spread_net_sharpe']:.4f}")
    print(f"Spread Portfolio Turnover:     {res['spread_mean_turnover']:.4f}")
    print(f"Underparameterized Beta Norm:  {res['norm_beta_under']:.4f}")
    print(f"Overparameterized Beta Norm:   {res['norm_beta_over']:.4f}")


main()
