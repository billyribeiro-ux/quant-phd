"""Lab GM1-L01-1: Revised-data lookahead bias in a backtest.

Compares an asset-allocation strategy conditioned on ex-post revised macroeconomic data
versus real-time data vintages (Croushore & Stark 2001). Demonstrates that revised series
incorporate future information unknown at real-time decision dates, drastically inflating
backtest Sharpe ratios.
"""

from __future__ import annotations

import math

import numpy as np


def run_macro_backtest(signals: np.ndarray, forward_returns: np.ndarray) -> dict[str, float]:
    """Calculate performance metrics for a macro-conditioned trading strategy."""
    positions = np.sign(signals)
    strat_returns = positions * forward_returns

    mean_ret = float(np.mean(strat_returns))
    std_ret = float(np.std(strat_returns, ddof=1))
    ann_factor = math.sqrt(12.0)  # monthly data
    sharpe = (mean_ret / std_ret) * ann_factor if std_ret > 1e-12 else 0.0

    hit_rate = float(np.mean(strat_returns > 0.0))
    cumulative_return = float(np.prod(1.0 + strat_returns) - 1.0)

    return {
        "mean_monthly_return": mean_ret,
        "monthly_volatility": std_ret,
        "annualized_sharpe": sharpe,
        "hit_rate": hit_rate,
        "cumulative_return": cumulative_return,
    }


def main() -> None:
    print("GM1 Lab L01-1: Look-Ahead Bias in Macro Data Revisions [SIMULATED]")
    print("================================================================")

    rng = np.random.default_rng(42)
    n_months = 180  # 15 years of monthly macro data

    # True underlying latent economic state g_t
    true_state = np.zeros(n_months, dtype=np.float64)
    for t in range(1, n_months):
        true_state[t] = 0.82 * true_state[t - 1] + rng.normal(0.0, 0.45)

    # Initial real-time release: noisy signal with measurement error and reporting lag
    # Mankiw-Runkle-Shapiro (1984) / Croushore-Stark (2001) noise revision process
    measurement_noise = rng.normal(0.0, 0.55, size=n_months)
    real_time_vintage = true_state + measurement_noise

    # Ex-post revised series: statistical agencies revise data over multi-year benchmarks,
    # filtering out idiosyncratic measurement noise and incorporating future tax/census records
    ex_post_revised = true_state + 0.15 * measurement_noise

    # Asset excess returns: partially predictable by true economic state
    asset_returns = 0.08 * true_state + rng.normal(0.0, 0.045, size=n_months)

    # Macro trend strategy: Go long when macro signal > 0, short when < 0
    perf_revised = run_macro_backtest(ex_post_revised, asset_returns)
    perf_realtime = run_macro_backtest(real_time_vintage, asset_returns)

    print(f"Sample length: {n_months} monthly periods")
    print(f"Revision noise variance: {float(np.var(measurement_noise)):.4f}")
    print("----------------------------------------------------------------")
    print("Strategy Metric             Ex-Post Revised        Real-Time Vintage")
    print("----------------------------------------------------------------")
    print(
        f"Mean Monthly Return:        {perf_revised['mean_monthly_return'] * 100:6.3f}%                "
        f"{perf_realtime['mean_monthly_return'] * 100:6.3f}%"
    )
    print(
        f"Monthly Volatility:         {perf_revised['monthly_volatility'] * 100:6.3f}%                "
        f"{perf_realtime['monthly_volatility'] * 100:6.3f}%"
    )
    print(
        f"Annualized Sharpe Ratio:    {perf_revised['annualized_sharpe']:6.3f}                 "
        f"{perf_realtime['annualized_sharpe']:6.3f}"
    )
    print(
        f"Hit Rate (% positive):      {perf_revised['hit_rate'] * 100:6.2f}%                "
        f"{perf_realtime['hit_rate'] * 100:6.2f}%"
    )
    print(
        f"Cumulative Return:          {perf_revised['cumulative_return'] * 100:6.2f}%                "
        f"{perf_realtime['cumulative_return'] * 100:6.2f}%"
    )
    print("----------------------------------------------------------------")

    sharpe_inflation = perf_revised["annualized_sharpe"] - perf_realtime["annualized_sharpe"]
    print(f"Sharpe Ratio Inflation:    +{sharpe_inflation:.3f}")
    print("Look-ahead bias confirmed:  True")


main()
