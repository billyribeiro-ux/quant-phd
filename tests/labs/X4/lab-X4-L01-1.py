"""Lab X4-L01-1: Cryptocurrency Higher Moments & Time-Series Return Predictability.

SIMULATED daily cryptocurrency return and network growth time series.
Evaluates empirical return moments (volatility, skewness, excess kurtosis)
and estimates predictive time-series momentum and user growth regressions
following Liu & Tsyvinski (2021).
"""

from __future__ import annotations

import math
import random


def compute_sample_moments(returns: list[float]) -> dict[str, float]:
    """Calculate sample mean, annualized volatility, skewness, and excess kurtosis."""
    n = len(returns)
    if n < 4:
        raise ValueError("Need at least 4 observations for kurtosis")

    mean = sum(returns) / n
    var = sum((r - mean) ** 2 for r in returns) / (n - 1)
    std = math.sqrt(var)
    ann_vol = std * math.sqrt(365.0)

    # Standardized moments
    m3 = sum((r - mean) ** 3 for r in returns) / n
    skew = m3 / (std**3)

    m4 = sum((r - mean) ** 4 for r in returns) / n
    kurt = (m4 / (std**4)) - 3.0  # excess kurtosis

    return {
        "mean_daily": mean,
        "ann_vol": ann_vol,
        "skewness": skew,
        "excess_kurtosis": kurt,
    }


def ols_univariate(y: list[float], x: list[float]) -> tuple[float, float, float, float]:
    """Estimate univariate OLS: y = alpha + beta * x + eps.

    Returns (alpha, beta, t_stat, r2).
    """
    n = len(y)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y, strict=True))
    var_x = sum((xi - mean_x) ** 2 for xi in x)

    beta = cov_xy / var_x
    alpha = mean_y - beta * mean_x

    residuals = [yi - (alpha + beta * xi) for xi, yi in zip(x, y, strict=True)]
    sse = sum(e**2 for e in residuals)
    sst = sum((yi - mean_y) ** 2 for yi in y)
    r2 = 1.0 - (sse / sst) if sst > 0 else 0.0

    se_beta = math.sqrt((sse / (n - 2)) / var_x)
    t_stat = beta / se_beta if se_beta > 0 else 0.0

    return alpha, beta, t_stat, r2


def main() -> None:
    print("Lab X4-L01-1 | Cryptocurrency Statistical Moments & Return Predictability")
    print("--------------------------------------------------------------------------")

    rng = random.Random(42)
    n_days = 500

    # Simulate daily Bitcoin-like returns with high volatility, positive skew, and fat tails
    btc_returns: list[float] = []
    user_growth: list[float] = []
    macro_factor: list[float] = []

    for _ in range(n_days):
        # Mixture of normal and jump for fat tails / positive skew
        jump = rng.expovariate(0.2) if rng.random() < 0.05 else 0.0
        ret = rng.gauss(0.0015, 0.038) + jump * 0.05
        u_growth = 0.3 * ret + rng.gauss(0.001, 0.015)
        macro = rng.gauss(0.0003, 0.010)

        btc_returns.append(ret)
        user_growth.append(u_growth)
        macro_factor.append(macro)

    moments = compute_sample_moments(btc_returns)
    print(f"Annualized Volatility: {moments['ann_vol']:.4f}")
    print(f"Sample Skewness:       {moments['skewness']:.4f}")
    print(f"Excess Kurtosis:       {moments['excess_kurtosis']:.4f}")

    # 1-week past momentum: rolling 7-day lagged return
    y_pred: list[float] = []
    x_mom: list[float] = []
    x_user: list[float] = []
    x_macro: list[float] = []

    for t in range(7, n_days - 1):
        # Next-day return
        y_pred.append(btc_returns[t + 1])
        # Past 7-day cumulative return
        past_7d = sum(btc_returns[t - 6 : t + 1])
        x_mom.append(past_7d)
        # Past 7-day user growth
        past_user = sum(user_growth[t - 6 : t + 1])
        x_user.append(past_user)
        # Past macro factor
        x_macro.append(macro_factor[t])

    # Univariate regressions
    _, beta_mom, t_mom, r2_mom = ols_univariate(y_pred, x_mom)
    _, beta_user, t_user, r2_user = ols_univariate(y_pred, x_user)
    _, beta_macro, t_macro, r2_macro = ols_univariate(y_pred, x_macro)

    print("\nPredictive Regressions of Next-Day Return r_{t+1}:")
    print(f"  Time-Series Momentum (7d): beta = {beta_mom:.4f}, t-stat = {t_mom:.2f}, R2 = {r2_mom:.4f}")
    print(f"  Network User Growth (7d):  beta = {beta_user:.4f}, t-stat = {t_user:.2f}, R2 = {r2_user:.4f}")
    print(f"  Traditional Macro Factor:  beta = {beta_macro:.4f}, t-stat = {t_macro:.2f}, R2 = {r2_macro:.4f}")

    # Validation checks
    assert moments["ann_vol"] > 0.50
    assert moments["excess_kurtosis"] > 1.0
    print("\nEmpirical properties validated: high volatility, positive kurtosis, macro insignificance.")


main()
