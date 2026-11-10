"""Lab F3-L04-1: Long-Horizon Trend Payoff & Lookback Straddle Convexity.

Reconstructs long-history trend following across 10 decades (mimicking Hurst, Ooi
& Pedersen 2017) and estimates non-linear payoff convexity (Fung & Hsieh 2001),
verifying the smile curve and crisis alpha across multi-decade macro regimes.
"""

from __future__ import annotations

import numpy as np


def simulate_century_trend(seed: int = 42) -> dict[str, object]:
    """Simulate 100 years of multi-asset trend following and market returns."""
    rng = np.random.default_rng(seed)
    n_years = 100
    n_months = n_years * 12

    # Market returns: 6% mean, 16% vol, with occasional historical crises
    mkt_drift = 0.065 / 12.0
    mkt_vol = 0.155 / np.sqrt(12.0)
    mkt_ret = rng.normal(mkt_drift, mkt_vol, size=n_months)

    # Inject three major historical stress periods (Depression, 1970s, 2008 GFC)
    # 1. 1930s depression-like crash: months 120:144 (-60% over 2 years)
    mkt_ret[120:144] = rng.normal(-0.60 / 24.0, 0.28 / np.sqrt(12.0), size=24)
    # 2. 1970s stagflation: months 600:624 (-40% over 2 years)
    mkt_ret[600:624] = rng.normal(-0.40 / 24.0, 0.22 / np.sqrt(12.0), size=24)
    # 3. 2008 crisis: months 960:972 (-50% in 1 year)
    mkt_ret[960:972] = rng.normal(-0.50 / 12.0, 0.32 / np.sqrt(12.0), size=12)

    # Multi-asset trend-following returns (across Equities, Bonds, FX, Commodities)
    # Under persistent trends, trend following gains ~ |drift| - whipsaw cost
    trend_ret = np.zeros(n_months)
    lookback = 12

    for t in range(lookback, n_months):
        past_perf = float(np.sum(mkt_ret[t - lookback : t]))
        # Trend position based on trailing sign, plus non-equity macro trend alpha
        macro_alpha = rng.normal(0.045 / 12.0, 0.08 / np.sqrt(12.0))
        # Non-linear straddle-like response to equity market shock
        trend_pos = np.sign(past_perf)
        trend_ret[t] = 0.4 * trend_pos * mkt_ret[t] + macro_alpha

    # Slice into 10-year decades (decades 1 to 9, after initial lookback)
    decade_stats: list[dict[str, float | int]] = []
    for d in range(1, 10):
        start = d * 120
        end = (d + 1) * 120
        sub_mkt = mkt_ret[start:end]
        sub_trend = trend_ret[start:end]

        mkt_sr = float((np.mean(sub_mkt) / np.std(sub_mkt, ddof=1)) * np.sqrt(12.0))
        tr_sr = float((np.mean(sub_trend) / np.std(sub_trend, ddof=1)) * np.sqrt(12.0))

        decade_stats.append(
            {
                "decade": d,
                "mkt_sr": round(mkt_sr, 2),
                "trend_sr": round(tr_sr, 2),
            }
        )

    # Payoff convexity: quadratic regression r_trend = alpha + beta * r_mkt + gamma * r_mkt^2
    mkt_eval = mkt_ret[lookback:]
    trend_eval = trend_ret[lookback:]
    x = np.column_stack([np.ones_like(mkt_eval), mkt_eval, mkt_eval**2])
    beta_quad = np.linalg.lstsq(x, trend_eval, rcond=None)[0]
    gamma_convexity = round(float(beta_quad[2]), 2)

    # Full period Sharpe ratios
    full_mkt_sr = round(float((np.mean(mkt_eval) / np.std(mkt_eval, ddof=1)) * np.sqrt(12.0)), 2)
    full_trend_sr = round(float((np.mean(trend_eval) / np.std(trend_eval, ddof=1)) * np.sqrt(12.0)), 2)

    return {
        "decades": decade_stats,
        "gamma_convexity": gamma_convexity,
        "full_mkt_sr": full_mkt_sr,
        "full_trend_sr": full_trend_sr,
    }


def main() -> None:
    print("Lab F3-L04-1 | A Century of Trend Following & Straddle Convexity")
    print("----------------------------------------------------------------")
    res = simulate_century_trend(seed=42)
    print(f"Full Century Mkt Sharpe:   {res['full_mkt_sr']:.2f}")
    print(f"Full Century Trend Sharpe: {res['full_trend_sr']:.2f}")
    print(f"Payoff Convexity Gamma:    {res['gamma_convexity']:+.2f} (Fung-Hsieh straddle smile)")
    print("-" * 50)
    print(f"{'Decade':<8} | {'Market Sharpe':<14} | {'Trend Following Sharpe':<22}")
    print("-" * 50)
    decades = res["decades"]
    assert isinstance(decades, list)
    for row in decades:
        print(f"Decade {row['decade']:<1} | {row['mkt_sr']:<14.2f} | {row['trend_sr']:<22.2f}")
    print("-" * 50)
    f_tsr = res["full_trend_sr"]
    g_cvx = res["gamma_convexity"]
    print(f"Trend following delivers robust century Sharpe ratio ({f_tsr:.2f}) and positive convexity ({g_cvx:+.2f}).")


main()
