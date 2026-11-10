"""Lab 5: Volatility-managed factor portfolios and Moreira-Muir (2017) alpha.

Demonstrates Moreira & Muir (2017) volatility-management framework:
Scaling factor exposure inversely by trailing realized variance:
f^sigma_{t+1} = (c / RV_t) * f_{t+1}
generates positive alpha in spanning regressions against the original factor.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # SIMULATED: Monthly factor returns with daily realized variance over 360 months (30 years)
    rng = np.random.default_rng(42)
    n_months = 360
    days_per_month = 21

    monthly_returns = np.zeros(n_months)
    realized_variance = np.zeros(n_months)

    # Volatility process with leverage feedback: negative returns increase future volatility
    vol_state = 0.01  # baseline daily vol (~16% annualized)
    for m in range(n_months):
        daily_rets = np.zeros(days_per_month)
        for d in range(days_per_month):
            z = rng.standard_normal()
            daily_rets[d] = 0.0004 + vol_state * z
            vol_state = max(0.004, min(0.04, 0.95 * vol_state + 0.05 * 0.01 - 0.2 * daily_rets[d]))
        monthly_returns[m] = float(np.sum(daily_rets))
        realized_variance[m] = float(np.sum(daily_rets**2))

    # Moreira-Muir scaling: f^sigma_{t+1} = (c / RV_t) * f_{t+1}
    unscaled_managed = np.zeros(n_months - 1)
    for m in range(n_months - 1):
        unscaled_managed[m] = (1.0 / realized_variance[m]) * monthly_returns[m + 1]

    target_returns = monthly_returns[1:]
    target_vol = float(np.std(target_returns, ddof=1))

    # In-sample constant c matching unconditional factor volatility
    c = target_vol / float(np.std(unscaled_managed, ddof=1))
    managed_factor = c * unscaled_managed

    # Spanning regression: managed_factor = alpha + beta * target_returns + eps
    x = np.column_stack([np.ones(len(target_returns)), target_returns])
    y = managed_factor
    beta_hat = np.linalg.lstsq(x, y, rcond=None)[0]
    alpha_monthly, beta_f = float(beta_hat[0]), float(beta_hat[1])

    residuals = y - x @ beta_hat
    s2 = float(np.sum(residuals**2) / (len(y) - 2))
    se_alpha = float(np.sqrt(s2 * np.linalg.inv(x.T @ x)[0, 0]))
    t_stat = alpha_monthly / se_alpha
    alpha_annualized = alpha_monthly * 12.0

    sr_base = float(np.mean(target_returns) / np.std(target_returns, ddof=1) * np.sqrt(12.0))
    sr_managed = float(np.mean(managed_factor) / np.std(managed_factor, ddof=1) * np.sqrt(12.0))

    print(f"Base Factor Annualized Return: {np.mean(target_returns) * 12.0 * 100:.2f}%")
    print(f"Base Factor Annualized Vol: {target_vol * np.sqrt(12.0) * 100:.2f}%")
    print(f"Base Factor Sharpe Ratio: {sr_base:.4f}")
    print(f"Managed Factor Sharpe Ratio: {sr_managed:.4f}")
    print(f"Sharpe Ratio Expansion: {sr_managed - sr_base:+.4f}")
    print(f"Spanning Regression Beta: {beta_f:.4f}")
    print(f"Annualized Moreira-Muir Alpha: {alpha_annualized * 100:.2f}%")
    print(f"Alpha t-statistic: {t_stat:.2f}")


main()
