"""Lab Project 1 (Rung 1 Worked Example): Full Risk Engine Core Pipeline.

A fully solved instance of the Atlas A12 risk measurement and backtesting pipeline,
annotated with architectural rationale at each stage.
"""

from __future__ import annotations

import math

import numpy as np
import scipy.stats


def main() -> None:
    rng = np.random.default_rng(100)
    t_obs = 500
    portfolio_equity = 10_000_000.0
    alpha = 0.99

    # 1. Generate loss series with leptokurtosis (Student-t df=4)
    returns = rng.standard_t(df=4, size=t_obs) * 0.014 - 0.0004
    losses = -returns

    # 2. Risk Estimation Engines
    # Historical Simulation
    var_hist = float(np.quantile(losses, alpha, method="linear"))
    es_hist = float(np.mean(losses[losses > var_hist]))

    # Parametric Gaussian
    mu = float(np.mean(losses))
    sigma = float(np.std(losses, ddof=1))
    z = float(scipy.stats.norm.ppf(alpha))
    phi = float(scipy.stats.norm.pdf(z))
    var_norm = mu + sigma * z
    es_norm = mu + sigma * (phi / (1.0 - alpha))

    # Parametric Student-t
    df = 4
    scale = sigma * math.sqrt((df - 2.0) / float(df))
    q = float(scipy.stats.t.ppf(alpha, df=df))
    g_q = float(scipy.stats.t.pdf(q, df=df))
    var_t = mu + scale * q
    es_t = mu + scale * ((g_q / (1.0 - alpha)) * ((df + q * q) / (df - 1.0)))

    # Extreme Value Theory (POT / GPD)
    u = float(np.quantile(losses, 0.90, method="linear"))
    excesses = losses[losses > u] - u
    n_u = len(excesses)
    m_e = float(np.mean(excesses))
    v_e = float(np.var(excesses, ddof=1))
    xi = 0.5 * (1.0 - (m_e**2) / v_e)
    beta = m_e * (1.0 - xi)
    factor = (t_obs / n_u) * (1.0 - alpha)
    var_evt = u + (beta / xi) * (factor ** (-xi) - 1.0)
    es_evt = (var_evt + beta - xi * u) / (1.0 - xi)

    # 3. Kupiec POF Backtest over 250 out-of-sample days
    hits = (losses[-250:] > var_hist).astype(int)
    x = int(np.sum(hits))
    t_back = 250
    p = 1.0 - alpha
    p_hat = x / t_back
    lr_pof = -2.0 * (
        (t_back - x) * math.log(1.0 - p) + x * math.log(p) - (t_back - x) * math.log(1.0 - p_hat) - x * math.log(p_hat)
    )
    lr_pof = max(0.0, float(lr_pof))
    p_val_pof = float(math.erfc(math.sqrt(lr_pof / 2.0)))

    # 4. Stress Scenario P&L
    weights = np.array([0.4, 0.3, 0.2, 0.1], dtype=np.float64)
    shocks = np.array([-0.18, -0.10, 0.04, -0.22], dtype=np.float64)
    stress_pnl = float(portfolio_equity * np.dot(weights, shocks))

    print(f"Base Portfolio Equity: ${portfolio_equity:,.2f}")
    print(f"Historical 99% VaR:  {var_hist:.5f} | ES: {es_hist:.5f}")
    print(f"Gaussian 99% VaR:    {var_norm:.5f} | ES: {es_norm:.5f}")
    print(f"Student-t 99% VaR:   {var_t:.5f} | ES: {es_t:.5f}")
    print(f"EVT POT 99% VaR:     {var_evt:.5f} | ES: {es_evt:.5f}")
    print("-" * 60)
    print(f"Backtest Hits: {x}/{t_back} | Kupiec LR: {lr_pof:.4f} | p-value: {p_val_pof:.4f}")
    print(f"Macro Stress Dollar P&L: ${stress_pnl:,.2f} ({stress_pnl / portfolio_equity * 100:.2f}%)")


main()
