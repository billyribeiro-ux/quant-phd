"""Lab S0-L02-1: Quantile diagnostics (Q-Q plot) and robust outlier detection on Treasury yields.

Demonstrates heavy-tailed quantile diagnostics against the standard normal reference,
and evaluates classical 3-sigma vs robust Hampel MAD outlier detection under masking.
Data source: Board of Governors of the Federal Reserve System, H.15 Selected Interest Rates.
Retrieved from MANIFEST: 2026-10-20.
"""

from __future__ import annotations

import csv
import statistics
from pathlib import Path
from statistics import NormalDist


def main() -> None:
    data_path = Path("data") / "ust_daily.csv"
    with data_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        yields: list[float] = [float(row["cmt_10y"]) for row in reader if row.get("cmt_10y")]

    # Daily changes in 10-year Treasury yield (percentage points)
    dy: list[float] = [yields[t] - yields[t - 1] for t in range(1, len(yields))]
    n = len(dy)

    phi = NormalDist()
    dy_sorted = sorted(dy)

    med = statistics.median(dy)
    stdev = statistics.stdev(dy)
    mad = statistics.median([abs(x - med) for x in dy])
    mad_scaled = mad * 1.4826022185

    # Empirical vs theoretical normal quantiles at 0.1%, 1%, 99%, 99.9%
    p_levels = (0.001, 0.01, 0.99, 0.999)
    emp_quantiles = [dy_sorted[int(p * n)] for p in p_levels]
    norm_quantiles = [med + phi.inv_cdf(p) * mad_scaled for p in p_levels]

    # Clean full-sample outlier counts: classical 3*sigma vs robust 3*MAD*
    clean_classical_outliers = [x for x in dy if abs(x - med) > 3.0 * stdev]
    clean_robust_outliers = [x for x in dy if abs(x - med) > 3.0 * mad_scaled]

    # Masking experiment on a local window of N=100 daily yield changes
    sub = dy[:100]
    sub_contaminated = list(sub)
    planted_indices = list(range(10, 15))
    planted_val = 0.25  # +25 bps jump
    for idx in planted_indices:
        sub_contaminated[idx] = planted_val

    mean_contam = statistics.mean(sub_contaminated)
    stdev_contam = statistics.stdev(sub_contaminated)
    med_contam = statistics.median(sub_contaminated)
    mad_contam = statistics.median([abs(x - med_contam) for x in sub_contaminated])
    mad_scaled_contam = mad_contam * 1.4826022185

    classical_detected = sum(
        1 for idx in planted_indices if abs(sub_contaminated[idx] - mean_contam) > 3.0 * stdev_contam
    )
    robust_detected = sum(
        1 for idx in planted_indices if abs(sub_contaminated[idx] - med_contam) > 3.0 * mad_scaled_contam
    )

    is_heavy = abs(emp_quantiles[0]) > abs(norm_quantiles[0]) and emp_quantiles[3] > norm_quantiles[3]

    print(f"Sample size: {n}")
    print(f"Location and scale: median={med:.4f} stdev={stdev:.4f} mad_scaled={mad_scaled:.4f}")
    print(f"Empirical 0.1% vs Normal 0.1%: {emp_quantiles[0]:.3f} vs {norm_quantiles[0]:.3f}")
    print(f"Empirical 99.9% vs Normal 99.9%: {emp_quantiles[3]:.3f} vs {norm_quantiles[3]:.3f}")
    print(f"Heavy tail confirmed: {is_heavy}")
    print(f"Clean outlier flags: classical={len(clean_classical_outliers)} robust={len(clean_robust_outliers)}")
    print(f"Masking experiment (N=100): planted {len(planted_indices)} clustered outliers")
    print(f"Classical 3-sigma detected: {classical_detected}/{len(planted_indices)}")
    print(f"Robust 3-MAD detected: {robust_detected}/{len(planted_indices)}")


main()
