"""Lab 5: Debt sustainability analysis (DSA) and stochastic fan chart projection.

SIMULATED 10-year Monte Carlo paths (N=1000). Standard library only.
Verifies stochastic debt-to-GDP accumulation under macroeconomic volatility,
computes fan chart percentile profiles, and estimates fiscal stabilization gaps.
"""

from __future__ import annotations

import random

SEED = 42


def simulate_dsa_paths(
    n_paths: int,
    horizon: int,
    b0: float,
    mean_r: float,
    mean_g: float,
    mean_s: float,
    sigma_r: float,
    sigma_g: float,
    sigma_s: float,
    seed: int,
) -> list[list[float]]:
    """Simulate N Monte Carlo paths of debt-to-GDP ratios over H periods."""
    rng = random.Random(seed)
    paths: list[list[float]] = []

    for _ in range(n_paths):
        path = [b0]
        b_curr = b0
        for _ in range(horizon):
            # Macroeconomic shocks
            r_t = mean_r + rng.gauss(0.0, sigma_r)
            g_t = mean_g + rng.gauss(0.0, sigma_g)
            s_t = mean_s + rng.gauss(0.0, sigma_s)

            # Debt dynamics step: b_t = [(1 + r_t) / (1 + g_t)] * b_{t-1} - s_t
            b_curr = ((1.0 + r_t) / (1.0 + g_t)) * b_curr - s_t
            path.append(b_curr)
        paths.append(path)

    return paths


def compute_percentiles(paths: list[list[float]], p_values: list[float]) -> dict[float, list[float]]:
    """Compute percentile curves across simulation paths for each period."""
    horizon = len(paths[0])
    results: dict[float, list[float]] = {p: [] for p in p_values}

    for t in range(horizon):
        vals_at_t = sorted(path[t] for path in paths)
        n = len(vals_at_t)
        for p in p_values:
            idx = round(p * (n - 1))
            results[p].append(vals_at_t[idx])

    return results


def breach_probability(paths: list[list[float]], ceiling: float) -> float:
    """Compute empirical probability of exceeding debt ceiling at any point in horizon."""
    breaches = sum(1 for path in paths if any(b > ceiling for b in path))
    return breaches / len(paths)


def main() -> None:
    # Baseline macroeconomic calibration
    b0 = 0.85  # 85% debt-to-GDP
    mean_r = 0.025  # 2.5% real interest rate
    mean_g = 0.020  # 2.0% real growth rate (r - g = +0.5%)
    mean_s = -0.010  # 1.0% primary deficit
    sigma_r = 0.015  # 1.5% interest rate volatility
    sigma_g = 0.020  # 2.0% growth volatility
    sigma_s = 0.010  # 1.0% fiscal policy volatility

    n_paths = 1000
    horizon = 10
    debt_ceiling = 1.00  # 100% debt threshold

    paths = simulate_dsa_paths(
        n_paths,
        horizon,
        b0,
        mean_r,
        mean_g,
        mean_s,
        sigma_r,
        sigma_g,
        sigma_s,
        SEED,
    )
    percentiles = compute_percentiles(paths, [0.10, 0.25, 0.50, 0.75, 0.90])
    p_breach = breach_probability(paths, debt_ceiling)

    # Primary gap required to stabilize debt at initial b0
    # s* = [(mean_r - mean_g) / (1 + mean_g)] * b0
    # primary_gap = s* - mean_s
    s_star = ((mean_r - mean_g) / (1.0 + mean_g)) * b0
    primary_gap = s_star - mean_s

    print("=== Sovereign Debt Sustainability Analysis (DSA) ===")
    print(f"Initial Debt Ratio b0:           {b0:.4f}")
    print(f"Mean r: {mean_r:.4f}, Mean g: {mean_g:.4f}, Mean s: {mean_s:.4f}")
    print(f"Debt Ceiling Threshold:          {debt_ceiling:.4f}")
    print(f"Debt Ceiling Breach Probability: {p_breach * 100.0:.2f}%")
    print(f"Debt-Stabilizing Balance s*:     {s_star:.4f}")
    print(f"Required Fiscal Adjustment Gap:  {primary_gap * 100.0:.2f}% of GDP")
    print("\n=== Fan Chart Percentile Trajectory (Horizon = 10 Years) ===")
    print("Period |   P10   |   P25   |   P50   |   P75   |   P90  ")
    for t in (0, 2, 5, 8, 10):
        print(
            f"  t={t:2d}  | {percentiles[0.10][t]:7.4f} | {percentiles[0.25][t]:7.4f} | "
            f"{percentiles[0.50][t]:7.4f} | {percentiles[0.75][t]:7.4f} | {percentiles[0.90][t]:7.4f}"
        )

    assert percentiles[0.10][10] < percentiles[0.50][10] < percentiles[0.90][10], "Percentiles must be strictly ordered"
    assert 0.0 < p_breach < 1.0, "Breach probability must be non-trivial"
    assert primary_gap > 0.0, "Fiscal consolidation is required when r > g and running deficit"


main()
