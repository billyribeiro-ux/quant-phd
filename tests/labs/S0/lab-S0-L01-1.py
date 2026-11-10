"""Lab S0-L01-1: Empirical distribution and robust summaries on FX daily rates.

Demonstrates empirical CDF, histogram quantile properties, and compares classical
vs robust location (mean vs median vs trimmed mean) and scale (standard deviation vs MAD)
on Board of Governors H.10 foreign exchange rates before and after a planted outlier.
Data source: Board of Governors of the Federal Reserve System, G.5/H.10 Foreign Exchange Rates.
Retrieved from MANIFEST: 2026-10-19.
"""

from __future__ import annotations

import csv
import math
import statistics
from pathlib import Path


def main() -> None:
    data_path = Path("data") / "fx_daily.csv"
    with data_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        prices: list[float] = [float(row["EUR"]) for row in reader if row.get("EUR")]

    # Compute daily log returns: r_t = ln(P_t / P_{t-1})
    rets: list[float] = [
        math.log(prices[t] / prices[t - 1]) for t in range(1, len(prices))
    ]
    n = len(rets)

    # Clean summary statistics
    mean_clean = statistics.mean(rets)
    median_clean = statistics.median(rets)
    stdev_clean = statistics.stdev(rets)

    rets_sorted = sorted(rets)
    k_trim = int(0.10 * n)
    trimmed_clean = statistics.mean(rets_sorted[k_trim : n - k_trim])

    mad_clean = statistics.median([abs(x - median_clean) for x in rets])
    # Normal consistency factor: 1 / Phi^(-1)(0.75) ~ 1.4826022185
    mad_scaled_clean = mad_clean * 1.4826022185

    # Empirical quantiles at 1%, 5%, 50%, 95%, 99%
    q01 = rets_sorted[int(0.01 * n)]
    q05 = rets_sorted[int(0.05 * n)]
    q50 = rets_sorted[int(0.50 * n)]
    q95 = rets_sorted[int(0.95 * n)]
    q99 = rets_sorted[int(0.99 * n)]

    # Contaminated series: plant a single severe outlier (+50% return shock) at index 100
    rets_contaminated = list(rets)
    rets_contaminated[100] = 0.50

    mean_bad = statistics.mean(rets_contaminated)
    median_bad = statistics.median(rets_contaminated)
    stdev_bad = statistics.stdev(rets_contaminated)

    rets_bad_sorted = sorted(rets_contaminated)
    trimmed_bad = statistics.mean(rets_bad_sorted[k_trim : n - k_trim])

    mad_bad = statistics.median([abs(x - median_bad) for x in rets_bad_sorted])
    mad_scaled_bad = mad_bad * 1.4826022185

    print(f"Sample size: {n}")
    print(f"Empirical quantiles: q01={q01:.5f} q05={q05:.5f} q50={q50:.5f} q95={q95:.5f} q99={q99:.5f}")
    print(
        f"Clean series: mean={mean_clean:.6f} median={median_clean:.6f} "
        f"trim10={trimmed_clean:.6f} sd={stdev_clean:.6f} mad_scaled={mad_scaled_clean:.6f}"
    )
    print(
        f"Contaminated: mean={mean_bad:.6f} median={median_bad:.6f} "
        f"trim10={trimmed_bad:.6f} sd={stdev_bad:.6f} mad_scaled={mad_scaled_bad:.6f}"
    )
    print(f"Mean inflation factor: {mean_bad / mean_clean:.2f}")
    print(f"SD inflation factor: {stdev_bad / stdev_clean:.2f}")
    print(f"Median preserved: {median_clean == median_bad}")
    print(f"MAD preserved within 0.1%: {abs(mad_scaled_bad - mad_scaled_clean) / mad_scaled_clean < 0.001}")


main()
