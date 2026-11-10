"""Lab QR5-L06-1: Non-Stationarity, Regime Shifts & Policy Collapse in Financial RL.

Demonstrates:
1. Training an RL momentum/leverage policy under stationary Gaussian market returns.
2. In-sample performance metrics: Sharpe ratio, return, and maximum drawdown.
3. Out-of-sample evaluation under a non-stationary Markov regime shift (volatility explosion and trend reversal).
4. Catastrophic policy collapse: breakdown of Sharpe ratio and severe drawdown under distribution shift.
"""

from __future__ import annotations

import numpy as np


def simulate_market_regimes(
    n_days: int,
    regime_shift_day: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate asset price series with a regime shift from bull/low-vol to bear/high-vol."""
    returns = np.zeros(n_days)
    regimes = np.zeros(n_days, dtype=int)

    # Regime 0 (Stationary training regime): mu = +12% ann., sigma = 12% ann.
    mu_0 = 0.12 / 252.0
    sigma_0 = 0.12 / np.sqrt(252.0)

    # Regime 1 (Crisis/Stress regime): mu = -30% ann., sigma = 40% ann.
    mu_1 = -0.30 / 252.0
    sigma_1 = 0.40 / np.sqrt(252.0)

    for d in range(n_days):
        if d < regime_shift_day:
            returns[d] = rng.normal(mu_0, sigma_0)
            regimes[d] = 0
        else:
            returns[d] = rng.normal(mu_1, sigma_1)
            regimes[d] = 1

    prices = 100.0 * np.exp(np.cumsum(returns))
    return returns, prices


def evaluate_policy_performance(returns: np.ndarray, positions: np.ndarray) -> dict[str, float]:
    """Compute annualized return, annualized volatility, Sharpe ratio, and max drawdown."""
    strat_returns = positions[:-1] * returns[1:]
    if len(strat_returns) == 0:
        return {"return": 0.0, "vol": 0.0, "sharpe": 0.0, "max_dd": 0.0}

    ann_ret = float(np.mean(strat_returns) * 252.0)
    ann_vol = float(np.std(strat_returns) * np.sqrt(252.0))
    sharpe = float(ann_ret / ann_vol) if ann_vol > 1e-8 else 0.0

    cum_wealth = np.cumprod(1.0 + strat_returns)
    peak = np.maximum.accumulate(cum_wealth)
    drawdowns = (cum_wealth - peak) / peak
    max_dd = float(np.min(drawdowns))

    return {
        "return": ann_ret,
        "vol": ann_vol,
        "sharpe": sharpe,
        "max_dd": max_dd,
    }


def main() -> None:
    rng = np.random.default_rng(6)
    n_days = 504  # 2 years
    regime_shift_day = 252  # year 1 = stationary training, year 2 = regime shift

    returns, _ = simulate_market_regimes(n_days, regime_shift_day, rng)

    # Trend-following RL policy trained on Regime 0
    window = 10
    positions = np.zeros(n_days)
    for d in range(window, n_days):
        roll_ret = np.mean(returns[d - window : d])
        if roll_ret > 0.0:
            positions[d] = 2.0  # max leverage learned in low-vol bull regime
        else:
            positions[d] = 0.2

    # In-sample evaluation (Regime 0)
    perf_is = evaluate_policy_performance(returns[:regime_shift_day], positions[:regime_shift_day])

    # Out-of-sample evaluation (Regime 1: crisis shift)
    perf_oos = evaluate_policy_performance(returns[regime_shift_day:], positions[regime_shift_day:])

    print("--- IN-SAMPLE PERFORMANCE (Stationary Regime 0) ---")
    print(f"Annualized Return:    {perf_is['return'] * 100.0:6.2f}%")
    print(f"Annualized Volatility:{perf_is['vol'] * 100.0:6.2f}%")
    print(f"Sharpe Ratio:         {perf_is['sharpe']:6.2f}")
    print(f"Maximum Drawdown:     {perf_is['max_dd'] * 100.0:6.2f}%")

    print("\n--- OUT-OF-SAMPLE PERFORMANCE (Regime-Shifted Regime 1) ---")
    print(f"Annualized Return:    {perf_oos['return'] * 100.0:6.2f}%")
    print(f"Annualized Volatility:{perf_oos['vol'] * 100.0:6.2f}%")
    print(f"Sharpe Ratio:         {perf_oos['sharpe']:6.2f}")
    print(f"Maximum Drawdown:     {perf_oos['max_dd'] * 100.0:6.2f}%")

    collapse_detected = perf_oos["sharpe"] < 0.0 and perf_oos["max_dd"] < -0.30
    print(f"\nPolicy Collapse Detected: {collapse_detected}")


main()
