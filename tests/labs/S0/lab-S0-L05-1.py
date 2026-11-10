"""Lab S0-L05-1: Anscombe's quartet and graphical perception.

Demonstrates that identical summary statistics (mean, variance, correlation, OLS line)
can disguise completely different bivariate data-generating structures.
Data label: SIMULATED (constructed quartet labelled as not Anscombe's original table
per Phase 2 architect ruling 2 until a cleared source locator is confirmed).
"""

from __future__ import annotations

import math
import statistics


def analyze_bivariate(x: list[float], y: list[float]) -> dict[str, float]:
    """Compute summary statistics and OLS regression parameters for a bivariate pair."""
    n = len(x)
    mx = statistics.mean(x)
    my = statistics.mean(y)
    vx = statistics.variance(x)
    vy = statistics.variance(y)
    cov = sum((x[i] - mx) * (y[i] - my) for i in range(n)) / (n - 1)
    r = cov / math.sqrt(vx * vy)
    slope = cov / vx
    intercept = my - slope * mx
    return {
        "n": float(n),
        "mean_x": mx,
        "mean_y": my,
        "var_x": vx,
        "var_y": vy,
        "r": r,
        "slope": slope,
        "intercept": intercept,
    }


def main() -> None:
    # Constructed SIMULATED quartet datasets
    # Set 1: linear relationship with homogeneous scatter
    x1 = [10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0]
    y1 = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]

    # Set 2: deterministic quadratic curve
    x2 = [10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0]
    y2 = [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]

    # Set 3: linear relationship with a single vertical outlier
    x3 = [10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0]
    y3 = [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]

    # Set 4: vertical line with a single high-leverage outlier
    x4 = [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 19.0]
    y4 = [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 5.56, 7.91, 6.89, 12.50]

    datasets = [("Set 1", x1, y1), ("Set 2", x2, y2), ("Set 3", x3, y3), ("Set 4", x4, y4)]

    print("Quartet summary statistics:")
    for label, x, y in datasets:
        stats = analyze_bivariate(x, y)
        print(
            f"{label}: n={int(stats['n'])} "
            f"mean_x={stats['mean_x']:.2f} "
            f"mean_y={stats['mean_y']:.2f} "
            f"var_x={stats['var_x']:.2f} "
            f"var_y={stats['var_y']:.3f} "
            f"r={stats['r']:.3f} "
            f"OLS: y = {stats['intercept']:.2f} + {stats['slope']:.3f}x"
        )

    # Invariant checks across all four datasets
    stats_list = [analyze_bivariate(x, y) for _, x, y in datasets]
    all_n_equal = all(s["n"] == 11.0 for s in stats_list)
    all_mean_x_equal = all(abs(s["mean_x"] - 9.0) < 0.01 for s in stats_list)
    all_mean_y_equal = all(abs(s["mean_y"] - 7.50) < 0.02 for s in stats_list)
    all_var_x_equal = all(abs(s["var_x"] - 11.0) < 0.01 for s in stats_list)
    all_var_y_equal = all(abs(s["var_y"] - 4.125) < 0.01 for s in stats_list)
    all_r_equal = all(abs(s["r"] - 0.816) < 0.005 for s in stats_list)
    all_slope_equal = all(abs(s["slope"] - 0.500) < 0.005 for s in stats_list)

    print(f"Sample size identical (11): {all_n_equal}")
    print(f"Mean x identical (9.00): {all_mean_x_equal}")
    print(f"Mean y identical (7.50): {all_mean_y_equal}")
    print(f"Variance x identical (11.00): {all_var_x_equal}")
    print(f"Variance y identical (4.125): {all_var_y_equal}")
    print(f"Correlation r identical (~0.816): {all_r_equal}")
    print(f"Regression slope identical (~0.500): {all_slope_equal}")


main()
