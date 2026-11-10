"""Lab F2-L02-1: Cross-Sectional Momentum and Momentum Crash Dynamics.

Simulates monthly returns across 200 equities to implement Jegadeesh-Titman (1993)
and Carhart (1997) cross-sectional momentum (12-2 formation, 1-month holding),
demonstrating positive unconditional risk-adjusted alpha alongside severe left-tail
crash risk during market rebounds (Daniel & Moskowitz 2016).
"""

from __future__ import annotations

import numpy as np


def simulate_momentum_and_crashes(seed: int = 42) -> dict[str, float | int]:
    """Simulate cross-sectional momentum strategy and measure return asymmetry."""
    rng = np.random.default_rng(seed)
    n_stocks = 200
    n_months = 180  # 15 years

    # Persistent stock-level fundamental quality / drift (annual 6% cross-sectional spread)
    firm_drift = rng.normal(0.0, 0.08 / 12, size=n_stocks)
    base_betas = rng.uniform(0.7, 1.3, size=n_stocks)

    # Market factor with a major panic drawdown and violent recovery
    mkt_rf = rng.normal(0.07 / 12, 0.15 / np.sqrt(12), size=n_months)
    # Month 60 to 65: crash (-35% cumulative)
    mkt_rf[60:66] = rng.normal(-0.07, 0.03, size=6)
    # Month 66 to 70: sudden violent recovery (+40% cumulative)
    mkt_rf[66:70] = rng.normal(+0.09, 0.02, size=4)

    stock_rets = np.zeros((n_months, n_stocks))
    for t in range(n_months):
        # In panic states, distressed past losers experience massive beta expansion
        if 66 <= t < 70:
            # Losers during crash (month 65) had negative cumulative return; beta surges
            cum_crash = np.sum(stock_rets[60:66, :], axis=0)
            beta_t = base_betas.copy()
            beta_t[cum_crash < np.median(cum_crash)] += 1.4  # option-like beta surge
        else:
            beta_t = base_betas

        idio = rng.normal(0, 0.20 / np.sqrt(12), size=n_stocks)
        stock_rets[t, :] = firm_drift + beta_t * mkt_rf[t] + idio

    # Form momentum portfolios from month t = 12 onward
    wml_returns = []
    winners_returns = []
    losers_returns = []

    for t in range(12, n_months):
        # 11-month formation window [t-12, t-2], skipping month t-1
        cum_ret = np.prod(1.0 + stock_rets[t - 12 : t - 1, :], axis=0) - 1.0

        p10 = np.percentile(cum_ret, 10)
        p90 = np.percentile(cum_ret, 90)

        losers_mask = cum_ret <= p10
        winners_mask = cum_ret >= p90

        r_win = float(np.mean(stock_rets[t, winners_mask]))
        r_los = float(np.mean(stock_rets[t, losers_mask]))

        winners_returns.append(r_win)
        losers_returns.append(r_los)
        wml_returns.append(r_win - r_los)

    wml = np.array(wml_returns)
    win = np.array(winners_returns)
    los = np.array(losers_returns)

    mean_ann = float(np.mean(wml) * 12 * 100)
    std_ann = float(np.std(wml, ddof=1) * np.sqrt(12) * 100)
    sharpe = float((np.mean(wml) * 12) / (np.std(wml, ddof=1) * np.sqrt(12)))

    # Sample skewness
    skewness = float(np.mean(((wml - np.mean(wml)) / np.std(wml, ddof=1)) ** 3))
    worst_month = float(np.min(wml) * 100)

    # Rebound months (relative to t=12 start, months 66-70 are indices 54-57)
    rebound_wml_mean = float(np.mean(wml[54:58]) * 100)
    rebound_los_mean = float(np.mean(los[54:58]) * 100)
    rebound_win_mean = float(np.mean(win[54:58]) * 100)

    return {
        "n_stocks": n_stocks,
        "n_eval_months": len(wml),
        "mean_ann": round(mean_ann, 2),
        "std_ann": round(std_ann, 2),
        "sharpe": round(sharpe, 2),
        "skewness": round(skewness, 2),
        "worst_month": round(worst_month, 2),
        "rebound_wml_mean": round(rebound_wml_mean, 2),
        "rebound_los_mean": round(rebound_los_mean, 2),
        "rebound_win_mean": round(rebound_win_mean, 2),
    }


def main() -> None:
    print("Lab F2-L02-1 | Cross-Sectional Momentum & Daniel-Moskowitz Crashes")
    print("-----------------------------------------------------------------")
    res = simulate_momentum_and_crashes(seed=42)
    print(f"Evaluation window: {res['n_eval_months']} months across {res['n_stocks']} equities")
    print(
        f"Unconditional WML Premium: {res['mean_ann']:+.2f}% ann (vol {res['std_ann']:.2f}%, SR = {res['sharpe']:.2f})"
    )
    print(f"WML Return Skewness:       {res['skewness']:+.2f} (pronounced left tail)")
    print(f"Worst Monthly Drawdown:    {res['worst_month']:.2f}%")
    print(f"Rebound Performance - Winners: {res['rebound_win_mean']:+.2f}% / month")
    print(f"Rebound Performance - Losers:  {res['rebound_los_mean']:+.2f}% / month")
    print(f"Rebound Performance - WML:     {res['rebound_wml_mean']:+.2f}% / month (crash)")


main()
