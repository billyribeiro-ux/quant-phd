"""Lab X4-L03-1: Macro Liquidity Regimes & Bitcoin Beta Switching.

SIMULATED daily digital asset returns, Nasdaq 100 tech equity returns, and real interest rate shocks.
Estimates rolling correlations, beta to equities, and a 2-state regime classification
identifying the structural shift from early idiosyncratic asset to high-beta macro liquidity asset.
"""

from __future__ import annotations

import math
import random


def rolling_ols_beta(y: list[float], x: list[float], window: int) -> list[float]:
    """Compute rolling window beta of y on x."""
    n = len(y)
    betas: list[float] = []
    for t in range(window, n + 1):
        y_win = y[t - window : t]
        x_win = x[t - window : t]
        m_x = sum(x_win) / window
        m_y = sum(y_win) / window
        cov = sum((xi - m_x) * (yi - m_y) for xi, yi in zip(x_win, y_win, strict=True))
        var = sum((xi - m_x) ** 2 for xi in x_win)
        b = cov / var if var > 1e-12 else 0.0
        betas.append(b)
    return betas


def rolling_correlation(y: list[float], x: list[float], window: int) -> list[float]:
    """Compute rolling Pearson correlation between y and x."""
    n = len(y)
    corrs: list[float] = []
    for t in range(window, n + 1):
        y_win = y[t - window : t]
        x_win = x[t - window : t]
        m_x = sum(x_win) / window
        m_y = sum(y_win) / window
        cov = sum((xi - m_x) * (yi - m_y) for xi, yi in zip(x_win, y_win, strict=True))
        var_x = sum((xi - m_x) ** 2 for xi in x_win)
        var_y = sum((yi - m_y) ** 2 for yi in y_win)
        denom = math.sqrt(var_x * var_y)
        corr = cov / denom if denom > 1e-12 else 0.0
        corrs.append(corr)
    return corrs


def main() -> None:
    print("Lab X4-L03-1 | Macro Liquidity Regimes & Digital Asset Beta")
    print("-----------------------------------------------------------")

    rng = random.Random(2024)
    n_days = 800  # 400 days in Regime 0, 400 days in Regime 1

    # Macro factors: Tech equity return (nasdaq) and real rate shock (delta_real_yield)
    nasdaq_returns: list[float] = []
    real_rate_shocks: list[float] = []
    btc_returns: list[float] = []

    regime_labels: list[int] = []

    for t in range(n_days):
        ret_nasdaq = rng.gauss(0.0004, 0.012)
        shock_rate = rng.gauss(0.0000, 0.0005)  # 5 bps daily shock
        nasdaq_returns.append(ret_nasdaq)
        real_rate_shocks.append(shock_rate)

        if t < 400:
            # Regime 0: Early Idiosyncratic Era (2015-2019)
            # Low equity beta (0.12), zero interest rate sensitivity
            idio = rng.gauss(0.001, 0.040)
            ret_btc = 0.12 * ret_nasdaq - 1.5 * shock_rate + idio
            regime_labels.append(0)
        else:
            # Regime 1: Macro Liquidity Era (2020-present)
            # High equity beta (1.55), severe real rate sensitivity (-25.0)
            idio = rng.gauss(0.0005, 0.025)
            ret_btc = 1.55 * ret_nasdaq - 25.0 * shock_rate + idio
            regime_labels.append(1)

        btc_returns.append(ret_btc)

    # 1. Full Sample vs. Regime-Specific OLS
    def estimate_regime_stats(indices: list[int], name: str) -> None:
        y_sub = [btc_returns[i] for i in indices]
        x_sub = [nasdaq_returns[i] for i in indices]
        r_sub = [real_rate_shocks[i] for i in indices]
        m = len(indices)

        m_y = sum(y_sub) / m
        m_x = sum(x_sub) / m
        cov_yx = sum((y - m_y) * (x - m_x) for y, x in zip(y_sub, x_sub, strict=True)) / m
        var_x = sum((x - m_x) ** 2 for x in x_sub) / m
        var_y = sum((y - m_y) ** 2 for y in y_sub) / m
        beta_nasdaq = cov_yx / var_x
        corr_nasdaq = cov_yx / math.sqrt(var_x * var_y)

        cov_yr = sum((y - m_y) * (r - sum(r_sub) / m) for y, r in zip(y_sub, r_sub, strict=True)) / m
        var_r = sum((r - sum(r_sub) / m) ** 2 for r in r_sub) / m
        beta_rate = cov_yr / var_r

        print(f"{name}:")
        print(f"  Nasdaq Beta:        {beta_nasdaq:.4f}")
        print(f"  Nasdaq Correlation: {corr_nasdaq:.4f}")
        print(f"  Real Rate Beta:     {beta_rate:.2f}")

    estimate_regime_stats(list(range(400)), "Regime 0 (Early Idiosyncratic Era)")
    print()
    estimate_regime_stats(list(range(400, 800)), "Regime 1 (Macro Liquidity Era)")

    # 2. Rolling Beta and Correlation Dynamics (60-day window)
    window = 60
    rolling_betas = rolling_ols_beta(btc_returns, nasdaq_returns, window)
    rolling_corrs = rolling_correlation(btc_returns, nasdaq_returns, window)

    early_avg_beta = sum(rolling_betas[:300]) / 300
    late_avg_beta = sum(rolling_betas[400:]) / len(rolling_betas[400:])
    late_avg_corr = sum(rolling_corrs[400:]) / len(rolling_corrs[400:])

    print("\nRolling 60-day Beta Shift:")
    print(f"  Average Beta in Early Regime: {early_avg_beta:.4f}")
    print(f"  Average Beta in Late Regime:  {late_avg_beta:.4f}")
    print(f"  Average Corr in Late Regime:  {late_avg_corr:.4f}")

    assert late_avg_beta > early_avg_beta + 0.80
    assert late_avg_corr > 0.40
    print("\nVerified structural break: Bitcoin transformed into a high-beta macro liquidity asset.")


main()
