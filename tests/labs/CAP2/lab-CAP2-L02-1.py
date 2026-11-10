"""Lab CAP2-L02-1: Empirical tests for the value factor and the factor zoo.

Implements Harvey-Liu-Zhu (2016) multiple testing hurdle trajectory as candidate
factor count expands, and evaluates Fama-French HML value factor drawdowns and
valuation spread dynamics.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def multiple_testing_hurdles(factor_counts: list[int], alpha: float = 0.05) -> list[float]:
    """Compute critical t-statistic thresholds under Bonferroni multiple testing adjustment."""
    hurdles = []
    for m in factor_counts:
        alpha_adj = alpha / float(m)
        z_crit = float(stats.norm.ppf(1.0 - alpha_adj / 2.0))
        hurdles.append(z_crit)
    return hurdles


def analyze_value_spread_and_drawdown(
    hml_returns: np.ndarray,
    growth_bm: np.ndarray,
    value_bm: np.ndarray,
) -> tuple[float, float, float]:
    """Compute value spread (B/M ratio between value and growth) and maximum drawdown."""
    val_spread = value_bm / growth_bm
    mean_spread = float(np.mean(val_spread))

    # Wealth index and drawdown
    wealth = np.cumprod(1.0 + hml_returns)
    peak = np.maximum.accumulate(wealth)
    drawdowns = (wealth - peak) / peak
    max_dd = float(np.min(drawdowns))

    ann_ret = float(np.mean(hml_returns) * 12.0)

    return mean_spread, max_dd, ann_ret


def main() -> None:
    rng = np.random.default_rng(2016)

    # 1. Multiple testing hurdles across factor zoo expansion
    factor_universe = [1, 10, 50, 100, 200, 316, 500]
    hurdles = multiple_testing_hurdles(factor_universe, alpha=0.05)

    print("--- Resolution 4: Factor Zoo Multiple Testing Hurdles ---")
    print(f"{'Candidate Factors (M)':<22} | {'Bonferroni t-Hurdle':<20} | {'Implied p-value'}")
    print("-" * 62)
    for m, h in zip(factor_universe, hurdles, strict=True):
        p_equiv = 2.0 * (1.0 - stats.norm.cdf(h))
        print(f"{m:<22} | {h:<20.3f} | {p_equiv:.6f}")

    # 2. Resolution 3: Value Factor (HML) Dynamics and Valuation Spread
    n_months = 180
    # Simulate pre-2010 positive alpha, post-2010 compression
    hml_pre = rng.normal(0.0035, 0.030, size=100)
    hml_post = rng.normal(-0.0010, 0.035, size=80)
    hml_all = np.concatenate([hml_pre, hml_post])

    # Valuation spread: B/M of value vs growth
    growth_bm = rng.normal(0.20, 0.02, size=n_months)
    value_bm = rng.normal(0.85, 0.08, size=n_months)
    # Stretch valuation spread during value drawdown
    value_bm[120:] += 0.35

    mean_spread, max_dd, ann_ret = analyze_value_spread_and_drawdown(hml_all, growth_bm, value_bm)

    print("\n--- Resolution 3: Is Value Dead? Factor Spread & Drawdowns ---")
    print(f"Full Sample Annualized HML Return: {ann_ret * 100.0:.2f}%")
    print(f"Pre-2010 Annualized HML Return:   {float(np.mean(hml_pre) * 12.0) * 100.0:.2f}%")
    print(f"Post-2010 Annualized HML Return:  {float(np.mean(hml_post) * 12.0) * 100.0:.2f}%")
    print(f"Average Value Spread (B/M Value / B/M Growth): {mean_spread:.2f}x")
    print(f"Maximum HML Drawdown:              {max_dd * 100.0:.2f}%")


main()
