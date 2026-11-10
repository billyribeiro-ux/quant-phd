"""Lab CAP2-L04-1: Empirical tests for algorithmic complexity and trend following post-2009.

Evaluates out-of-sample prediction error across model parameterizations (double
descent curve) and quantifies the post-2009 structural break in time-series
momentum (TSMOM) returns.
"""

from __future__ import annotations

import numpy as np


def evaluate_double_descent(
    n_samples: int = 150,
    param_counts: list[int] | None = None,
    noise_sigma: float = 0.5,
    ridge_lambda: float = 1e-4,
    seed: int = 2020,
) -> dict[int, tuple[float, float]]:
    """Simulate out-of-sample prediction error across varying parameter-to-sample ratios."""
    rng = np.random.default_rng(seed)
    if param_counts is None:
        param_counts = [20, 60, 120, 150, 180, 300, 600]

    # Generate test set
    n_test = 500
    max_p = max(param_counts)
    x_test_full = rng.normal(0.0, 1.0, size=(n_test, max_p))
    # True signal lies in first 10 features
    beta_true = np.zeros(max_p)
    beta_true[:10] = rng.normal(0.5, 0.2, size=10)
    y_test = x_test_full @ beta_true + rng.normal(0.0, noise_sigma, size=n_test)

    results = {}
    for p in param_counts:
        # Generate training set with p features
        x_train = rng.normal(0.0, 1.0, size=(n_samples, p))
        y_train = x_train @ beta_true[:p] + rng.normal(0.0, noise_sigma, size=n_samples)

        # Ridge regression: (X^T X + lambda I)^{-1} X^T y
        reg = ridge_lambda * np.eye(p)
        beta_hat = np.linalg.solve(x_train.T @ x_train + reg, x_train.T @ y_train)

        # Predictions
        y_pred_train = x_train @ beta_hat
        y_pred_test = x_test_full[:, :p] @ beta_hat

        mse_train = float(np.mean((y_train - y_pred_train) ** 2))
        mse_test = float(np.mean((y_test - y_pred_test) ** 2))
        results[p] = (mse_train, mse_test)

    return results


def evaluate_tsmom_break(
    tsmom_returns: np.ndarray,
    break_index: int,
) -> tuple[float, float, float, float, float]:
    """Decompose time-series momentum returns pre- and post-2009."""
    pre_ret = tsmom_returns[:break_index]
    post_ret = tsmom_returns[break_index:]

    m_pre = float(np.mean(pre_ret) * 12.0)
    m_post = float(np.mean(post_ret) * 12.0)
    s_pre = float(np.std(pre_ret, ddof=1) * np.sqrt(12.0))
    s_post = float(np.std(post_ret, ddof=1) * np.sqrt(12.0))

    sr_pre = m_pre / s_pre if s_pre > 0 else 0.0
    sr_post = m_post / s_post if s_post > 0 else 0.0

    retention = m_post / m_pre if abs(m_pre) > 1e-12 else 0.0

    return m_pre, sr_pre, m_post, sr_post, retention


def main() -> None:
    rng = np.random.default_rng(2012)

    # 1. Resolution 7: Complexity Double Descent
    n_obs = 150
    p_grid = [30, 75, 135, 150, 180, 300, 600]
    dd_res = evaluate_double_descent(n_samples=n_obs, param_counts=p_grid, ridge_lambda=1e-3, seed=42)

    print("--- Resolution 7: Algorithmic Complexity & Double Descent ---")
    print(f"{'Parameters (P)':<16} | {'P/N Ratio':<12} | {'Train MSE':<12} | {'Test OOS MSE'}")
    print("-" * 56)
    for p, (tr_mse, te_mse) in dd_res.items():
        gamma = p / n_obs
        print(f"{p:<16} | {gamma:<12.2f} | {tr_mse:<12.4f} | {te_mse:.4f}")

    # 2. Resolution 8: Trend Following Post-2009
    # Simulate 360 months (1985 - 2014): 24 years pre-2009, 6 years post-2009
    # Pre-2009: SR ~ 0.85, Post-2009: compressed SR ~ 0.35 (Moskowitz et al. 2012)
    pre_r = rng.normal(0.009, 0.035, size=288)  # 24 years
    post_r = rng.normal(0.003, 0.032, size=72)  # 6 years post-2009
    tsmom = np.concatenate([pre_r, post_r])

    m_pre, sr_pre, m_post, sr_post, _ = evaluate_tsmom_break(tsmom, break_index=288)

    print("\n--- Resolution 8: Trend Following Post-2009 Regime Break ---")
    print(f"Pre-2009 Annualized Return:  {m_pre * 100.0:.2f}% (Sharpe: {sr_pre:.2f})")
    print(f"Post-2009 Annualized Return: {m_post * 100.0:.2f}% (Sharpe: {sr_post:.2f})")
    print(f"Sharpe Ratio Retention:      {sr_post / sr_pre * 100.0:.1f}%")
    print(f"Post-2009 Status:            {'Surviving with Decay' if sr_post > 0.2 else 'Defunct'}")


main()
