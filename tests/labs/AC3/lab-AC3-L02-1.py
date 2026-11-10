"""AC3 lab L02: standardized unexpected earnings (SUE) and seasonal random walk models.

SIMULATED: the quarterly earnings series for 12 firms across 20 quarters are generated from
a seeded seasonal random walk process with firm-specific drift and heteroskedastic innovation
volatility. They are not real corporate filings. All calculations use standard library float and math.
"""

from __future__ import annotations

import math
import random

SEED = 20261110
N_FIRMS = 12
N_QUARTERS = 20
EST_QUARTERS = 16  # quarters 0..15 used for estimation, quarter 16 tested


def simulate_quarterly_earnings(seed: int) -> tuple[list[list[float]], list[float], list[float]]:
    """Simulate quarterly earnings with seasonal persistence, drift, and heteroskedastic noise.

    Returns (earnings_matrix, firm_scale, true_drifts).
    """
    rng = random.Random(seed)
    earnings: list[list[float]] = []
    scales: list[float] = []
    drifts: list[float] = []

    for _ in range(N_FIRMS):
        # Varying scale: large cap (scale 100) vs small cap (scale 5)
        scale = rng.uniform(5.0, 100.0)
        drift = rng.uniform(0.01, 0.05) * scale
        sigma = rng.uniform(0.05, 0.20) * scale
        scales.append(scale)
        drifts.append(drift)

        # Seasonal base for 4 quarters
        base = [scale * (1.0 + 0.1 * q) for q in range(4)]
        series = list(base)
        for t in range(4, N_QUARTERS):
            eps = rng.gauss(0.0, sigma)
            val = series[t - 4] + drift + eps
            series.append(val)
        earnings.append(series)

    return earnings, scales, drifts


def estimate_sue(series: list[float], test_q: int) -> tuple[float, float, float, float]:
    """Estimate seasonal random walk with drift and compute SUE for quarter test_q.

    Returns (forecast, raw_error, error_std, sue).
    """
    # Historical seasonal differences up to test_q - 1
    # Quarter t has seasonal difference diff_t = series[t] - series[t-4]
    diffs = [series[t] - series[t - 4] for t in range(4, test_q)]
    if len(diffs) < 4:
        raise ValueError("Need at least 4 historical seasonal differences")

    drift_hat = sum(diffs) / len(diffs)
    forecast = series[test_q - 4] + drift_hat
    raw_error = series[test_q] - forecast

    # Historical forecast errors: error_tau = diffs[tau] - drift_hat
    errors = [d - drift_hat for d in diffs]
    variance = sum(e**2 for e in errors) / (len(errors) - 1)
    error_std = math.sqrt(variance)

    sue = raw_error / error_std if error_std > 0 else 0.0
    return forecast, raw_error, error_std, sue


def main() -> None:
    earnings, scales, _drifts = simulate_quarterly_earnings(SEED)

    raw_errors: list[float] = []
    sue_scores: list[float] = []
    pct_surprises: list[float] = []

    print(f"seed {SEED} firms {N_FIRMS} test_quarter {EST_QUARTERS}")
    print(f"{'Firm':4s} | {'Scale':5s} | {'Actual':6s} | {'Fore':6s} | {'RawErr':7s} | {'Std':5s} | {'SUE':6s}")
    print("-" * 55)

    for i in range(N_FIRMS):
        series = earnings[i]
        actual = series[EST_QUARTERS]
        forecast, raw_err, s_dev, sue = estimate_sue(series, EST_QUARTERS)

        raw_errors.append(raw_err)
        sue_scores.append(sue)
        # Scale-relative surprise: raw error / prior year quarter earnings
        prior_q = series[EST_QUARTERS - 4]
        pct_surprises.append(raw_err / prior_q)

        row = f"{i:4d} | {scales[i]:5.1f} | {actual:6.2f} | {forecast:6.2f}"
        row += f" | {raw_err:+7.2f} | {s_dev:5.2f} | {sue:+6.3f}"
        print(row)

    # Heteroskedasticity comparison: ratio of max variance to min variance across firms
    var_raw = sum(r**2 for r in raw_errors) / len(raw_errors)
    var_sue = sum(s**2 for s in sue_scores) / len(sue_scores)

    print("-" * 65)
    print(f"cross_sectional_variance_raw_error: {var_raw:.3f}")
    print(f"cross_sectional_variance_sue: {var_sue:.3f}")
    print(f"sue_sample_mean: {sum(sue_scores) / len(sue_scores):+.3f}")
    print(f"all_sue_finite: {all(math.isfinite(s) for s in sue_scores)}")
    print(f"sue_within_normal_range: {all(-4.0 <= s <= 4.0 for s in sue_scores)}")


main()
