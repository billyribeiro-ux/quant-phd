"""Lab AP5-L07-1: Cyclically Adjusted Price-Earnings (CAPE) and 10-Year Return Predictability.

SIMULATED: generates real earnings and stock price series to construct Shiller's CAPE ratio
and estimate 10-year predictive regressions with Hansen-Hodrick overlapping error adjustments.
"""

from __future__ import annotations

import numpy as np


def hansen_hodrick_se(x: np.ndarray, e: np.ndarray, overlap: int) -> float:
    """Compute Hansen-Hodrick (1980) standard error for overlapping returns."""
    x_mean = np.mean(x)
    x_dev = x - x_mean
    sxx = float(np.sum(x_dev**2))

    u = x_dev * e
    omega = float(np.sum(u**2))
    for j in range(1, overlap):
        gamma = float(np.sum(u[j:] * u[:-j]))
        omega += 2.0 * gamma

    var_beta = omega / (sxx**2)
    return float(np.sqrt(max(1e-12, var_beta)))


def main() -> None:
    rng = np.random.default_rng(1881)
    n_total = 100  # 100 years of annual data
    horizon = 10  # 10-year horizon

    # Simulate real earnings with business cycle volatility and steady trend
    g_e = 0.02  # 2% real trend earnings growth
    sigma_e = 0.14  # annual earnings volatility
    delta_e = g_e + sigma_e * rng.standard_normal(n_total)
    earnings = np.zeros(n_total)
    earnings[0] = 5.0
    for t in range(1, n_total):
        earnings[t] = earnings[t - 1] * np.exp(delta_e[t])

    # 10-year moving average earnings E10_t
    e10 = np.zeros(n_total)
    for t in range(9, n_total):
        e10[t] = np.mean(earnings[t - 9 : t + 1])

    # Valuation multiple (log CAPE): mean approx ln(18) = 2.89, persistent AR(1)
    phi_cape = 0.88
    cape_mean_log = np.log(18.0)
    sigma_cape = 0.22
    log_cape = np.zeros(n_total)
    log_cape[9] = cape_mean_log
    for t in range(10, n_total):
        log_cape[t] = cape_mean_log + phi_cape * (log_cape[t - 1] - cape_mean_log) + sigma_cape * rng.standard_normal()

    # Reconstruct stock prices: P_t = E10_t * exp(log_cape_t)
    price = np.zeros(n_total)
    for t in range(9, n_total):
        price[t] = e10[t] * np.exp(log_cape[t])

    # Compute 10-year annualized return: r_{t->t+10} = (ln(P_{t+10}) - ln(P_t)) / 10 + avg_dividend_yield
    valid_t = n_total - horizon - 9
    ret_10y = np.zeros(valid_t)
    x_cape = np.zeros(valid_t)

    div_yield = 0.035  # 3.5% constant average dividend yield component
    for i, t in enumerate(range(9, n_total - horizon)):
        ret_10y[i] = (np.log(price[t + horizon]) - np.log(price[t])) / horizon + div_yield
        x_cape[i] = log_cape[t]

    # OLS Regression: ret_10y = alpha + beta * x_cape + e
    x_mean = float(np.mean(x_cape))
    y_mean = float(np.mean(ret_10y))
    sxx = float(np.sum((x_cape - x_mean) ** 2))
    sxy = float(np.sum((x_cape - x_mean) * (ret_10y - y_mean)))
    syy = float(np.sum((ret_10y - y_mean) ** 2))

    beta_ols = sxy / sxx
    alpha_ols = y_mean - beta_ols * x_mean
    r2 = (sxy**2) / (sxx * syy)

    resids = ret_10y - (alpha_ols + beta_ols * x_cape)
    se_hh = hansen_hodrick_se(x_cape, resids, overlap=horizon)
    t_hh = beta_ols / se_hh

    # Summary statistics of CAPE
    cape_levels = np.exp(x_cape)
    mean_cape = float(np.mean(cape_levels))
    min_cape = float(np.min(cape_levels))
    max_cape = float(np.max(cape_levels))

    print("Shiller CAPE 10-Year Return Predictive Regression")
    print(f"Sample length:               {valid_t} overlapping 10-year windows")
    print(f"Mean CAPE level:             {mean_cape:.2f}")
    print(f"Min / Max CAPE level:        {min_cape:.2f} / {max_cape:.2f}")
    print(f"Predictive slope (annual):   {beta_ols:.4f}")
    print(f"Hansen-Hodrick SE (t-stat):  {se_hh:.4f} ({t_hh:.2f})")
    print(f"Regression R^2:              {r2 * 100:.2f}%")
    print(f"10-year expected return gap: {abs(beta_ols * (np.log(30) - np.log(12))) * 100:.2f}% per year")


main()
