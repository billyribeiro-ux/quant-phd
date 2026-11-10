"""Lab F5-L04-1: Methodological Divergence and the Microcap Problem.

Anatomizes how methodological sorting choices (universe filters, NYSE breakpoints,
and equal vs. value weighting) drive empirical anomaly replication outcomes
(Chen & Zimmermann 2022, Hou, Xue & Zhang 2020).
"""

from __future__ import annotations

import numpy as np


def evaluate_methodological_divergence(seed: int = 42) -> dict[str, float | int]:
    """Decompose anomaly spread returns across universe screens and weighting schemes."""
    rng = np.random.default_rng(seed)
    n_stocks = 500
    n_months = 180

    # 1. Simulate market equity ME: log-normal with wide cross-sectional skewness
    # Typical US equity market: bottom 60% of names are microcaps (~3% market cap),
    # top 10% of names hold ~80% of aggregate market cap.
    log_me = rng.normal(loc=5.5, scale=1.8, size=n_stocks)
    me = np.exp(log_me)

    # Microcap definition: NYSE 20th percentile breakpoint
    # Simulating NYSE-listed subset (larger firms) to set the 20th percentile cut
    nyse_sub = log_me > 5.8
    nyse_p20 = float(np.percentile(me[nyse_sub], 20))
    is_microcap = me < nyse_p20
    is_non_micro = ~is_microcap

    pct_micro_count = float(np.mean(is_microcap) * 100)
    pct_micro_cap = float(np.sum(me[is_microcap]) / np.sum(me) * 100)

    # 2. Simulate anomaly characteristic X (e.g. composite debt/equity issuance)
    # Characteristic predicts returns strongly in microcaps (high limits to arbitrage)
    # but weakly in mega-caps
    x_char = rng.normal(loc=0.0, scale=1.0, size=n_stocks)

    # Anomaly return slope: 0.8% / mo per std in microcaps, 0.2% / mo in large caps
    slope_micro = 0.0080
    slope_large = 0.0020
    true_slope = np.where(is_microcap, slope_micro, slope_large)

    # Time series of returns: R_{i,t} = true_slope_i * X_i + beta_i * MKT_t + e_{i,t}
    mkt_rf = rng.normal(0.0050, 0.0450, size=n_months)
    betas = 0.8 + 0.4 * rng.uniform(0, 1, size=n_stocks)

    # Sort into deciles (D10 high vs. D1 low spread)
    # Sort A: All stocks deciles
    q10_all = x_char >= np.percentile(x_char, 90)
    q01_all = x_char <= np.percentile(x_char, 10)

    # Sort B: Non-microcap deciles (NYSE breakpoints)
    x_non_micro = x_char[is_non_micro]
    cut_hi_nyse = float(np.percentile(x_non_micro, 90))
    cut_lo_nyse = float(np.percentile(x_non_micro, 10))
    q10_nyse = is_non_micro & (x_char >= cut_hi_nyse)
    q01_nyse = is_non_micro & (x_char <= cut_lo_nyse)

    # Monthly return panel (n_stocks, n_months)
    idio_vol = np.where(is_microcap, 0.100, 0.050)
    eps = rng.normal(0.0, 1.0, size=(n_stocks, n_months)) * idio_vol[:, np.newaxis]
    returns = true_slope[:, np.newaxis] * x_char[:, np.newaxis] + betas[:, np.newaxis] * mkt_rf[np.newaxis, :] + eps

    # Compute spread returns under 4 configurations:
    # 1. All-stocks Equal-Weighted (All-EW)
    spread_all_ew = np.mean(returns[q10_all], axis=0) - np.mean(returns[q01_all], axis=0)

    # 2. All-stocks Value-Weighted (All-VW)
    w_hi_all = me[q10_all] / np.sum(me[q10_all])
    w_lo_all = me[q01_all] / np.sum(me[q01_all])
    spread_all_vw = np.sum(returns[q10_all] * w_hi_all[:, np.newaxis], axis=0) - np.sum(
        returns[q01_all] * w_lo_all[:, np.newaxis], axis=0
    )

    # 3. Non-microcap Equal-Weighted (NonMicro-EW)
    spread_nm_ew = np.mean(returns[q10_nyse], axis=0) - np.mean(returns[q01_nyse], axis=0)

    # 4. Non-microcap Value-Weighted (NonMicro-VW)
    w_hi_nm = me[q10_nyse] / np.sum(me[q10_nyse])
    w_lo_nm = me[q01_nyse] / np.sum(me[q01_nyse])
    spread_nm_vw = np.sum(returns[q10_nyse] * w_hi_nm[:, np.newaxis], axis=0) - np.sum(
        returns[q01_nyse] * w_lo_nm[:, np.newaxis], axis=0
    )

    # Metrics
    mean_all_ew_ann = float(np.mean(spread_all_ew) * 12 * 100)
    t_all_ew = float(np.mean(spread_all_ew) / (np.std(spread_all_ew, ddof=1) / np.sqrt(n_months)))

    mean_all_vw_ann = float(np.mean(spread_all_vw) * 12 * 100)
    t_all_vw = float(np.mean(spread_all_vw) / (np.std(spread_all_vw, ddof=1) / np.sqrt(n_months)))

    mean_nm_ew_ann = float(np.mean(spread_nm_ew) * 12 * 100)
    t_nm_ew = float(np.mean(spread_nm_ew) / (np.std(spread_nm_ew, ddof=1) / np.sqrt(n_months)))

    mean_nm_vw_ann = float(np.mean(spread_nm_vw) * 12 * 100)
    t_nm_vw = float(np.mean(spread_nm_vw) / (np.std(spread_nm_vw, ddof=1) / np.sqrt(n_months)))

    return {
        "n_stocks": n_stocks,
        "n_months": n_months,
        "pct_micro_count": round(pct_micro_count, 1),
        "pct_micro_cap": round(pct_micro_cap, 2),
        "mean_all_ew_ann": round(mean_all_ew_ann, 2),
        "t_all_ew": round(t_all_ew, 2),
        "mean_all_vw_ann": round(mean_all_vw_ann, 2),
        "t_all_vw": round(t_all_vw, 2),
        "mean_nm_ew_ann": round(mean_nm_ew_ann, 2),
        "t_nm_ew": round(t_nm_ew, 2),
        "mean_nm_vw_ann": round(mean_nm_vw_ann, 2),
        "t_nm_vw": round(t_nm_vw, 2),
    }


def main() -> None:
    print("Lab F5-L04-1 | Methodological Divergence and the Microcap Problem")
    print("----------------------------------------------------------------")
    res = evaluate_methodological_divergence(seed=42)
    print(f"Universe: {res['n_stocks']} equities ({res['n_months']} months)")
    print(
        f"Microcaps (NYSE p20 screen): {res['pct_micro_count']:.1f}% of firm count, "
        f"but only {res['pct_micro_cap']:.2f}% of market cap"
    )
    print("Long-Short Decile Spread Return Comparison:")
    print(
        f"  1. All Stocks Equal-Weighted (All-EW):       {res['mean_all_ew_ann']:+.2f}% ann (t = {res['t_all_ew']:.2f})"
    )
    print(
        f"  2. Non-Microcap Equal-Weighted (NonMicro-EW):{res['mean_nm_ew_ann']:+.2f}% ann (t = {res['t_nm_ew']:.2f})"
    )
    print(
        f"  3. All Stocks Value-Weighted (All-VW):       {res['mean_all_vw_ann']:+.2f}% ann (t = {res['t_all_vw']:.2f})"
    )
    print(
        f"  4. Non-Microcap Value-Weighted (NonMicro-VW):{res['mean_nm_vw_ann']:+.2f}% ann (t = {res['t_nm_vw']:.2f})"
    )


main()
