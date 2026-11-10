"""Lab CR1-L05-1: Distance to default and Bharath-Shumway (2008) empirical comparison.

Demonstrates the numerical inversion of the simultaneous Merton/KMV system for
unobservable firm asset value and volatility, compares Merton DD with Bharath-Shumway
naive DD across a cross-section of firms, and verifies their near-perfect correlation.
"""

from __future__ import annotations

import math


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def solve_merton_system(
    e: float,
    d: float,
    t: float,
    r: float,
    sigma_e: float,
    mu: float,
) -> tuple[float, float, float, float]:
    """Solve Merton/KMV system for (V, sigma_V) and compute distance to default."""
    v = e + d
    sigma_v = sigma_e * (e / v)

    for _ in range(150):
        vol_sqrt = max(1e-8, sigma_v * math.sqrt(t))
        d1 = (math.log(v / d) + (r + 0.5 * sigma_v * sigma_v) * t) / vol_sqrt
        d2 = d1 - vol_sqrt
        n_d1 = norm_cdf(d1)
        n_d2 = norm_cdf(d2)

        f_val = v * n_d1 - d * math.exp(-r * t) * n_d2 - e
        if abs(f_val) < 1e-11:
            break
        v = max(e * 0.8, v - f_val / max(1e-5, n_d1))

        vol_sqrt = max(1e-8, sigma_v * math.sqrt(t))
        d1 = (math.log(v / d) + (r + 0.5 * sigma_v * sigma_v) * t) / vol_sqrt
        sigma_v = max(1e-6, sigma_e * e / (v * max(1e-5, norm_cdf(d1))))

    vol_sqrt = max(1e-8, sigma_v * math.sqrt(t))
    dd = (math.log(v / d) + (mu - 0.5 * sigma_v * sigma_v) * t) / vol_sqrt
    pd = norm_cdf(-dd)
    return v, sigma_v, dd, pd


def bharath_shumway_naive(
    e: float,
    d: float,
    t: float,
    sigma_e: float,
    mu: float,
) -> tuple[float, float, float, float]:
    """Compute Bharath & Shumway (2008) naive distance to default."""
    v_naive = e + d
    sigma_d = 0.05 + 0.25 * sigma_e
    sigma_v_naive = (e / v_naive) * sigma_e + (d / v_naive) * sigma_d
    vol_sqrt = max(1e-8, sigma_v_naive * math.sqrt(t))
    dd_naive = (math.log(v_naive / d) + (mu - 0.5 * sigma_v_naive * sigma_v_naive) * t) / vol_sqrt
    pd_naive = norm_cdf(-dd_naive)
    return v_naive, sigma_v_naive, dd_naive, pd_naive


def main() -> None:
    # Stylized cross-section of 5 firms varying from high credit quality to distress
    firms = [
        ("Firm A (AAA)", 200.0, 50.0, 0.20, 0.08),
        ("Firm B (A)", 120.0, 60.0, 0.25, 0.08),
        ("Firm C (BBB)", 80.0, 70.0, 0.32, 0.09),
        ("Firm D (BB)", 45.0, 65.0, 0.42, 0.10),
        ("Firm E (CCC)", 15.0, 60.0, 0.65, 0.12),
    ]

    t_horizon = 1.0
    r_rf = 0.04

    print("Distance to Default Comparison: Merton KMV vs Bharath-Shumway (2008) Naive:")
    print("  Firm         | Merton V | Merton sigV | Merton DD | Merton PD | Naive DD | Naive PD")
    print("---------------+----------+-------------+-----------+-----------+----------+---------")

    merton_dds: list[float] = []
    naive_dds: list[float] = []

    for name, e_val, d_val, s_e, mu_val in firms:
        v_m, sv_m, dd_m, pd_m = solve_merton_system(e_val, d_val, t_horizon, r_rf, s_e, mu_val)
        _v_n, _sv_n, dd_n, pd_n = bharath_shumway_naive(e_val, d_val, t_horizon, s_e, mu_val)

        merton_dds.append(dd_m)
        naive_dds.append(dd_n)

        # Inversion precision check
        vol_sqrt = sv_m * math.sqrt(t_horizon)
        d1 = (math.log(v_m / d_val) + (r_rf + 0.5 * sv_m**2) * t_horizon) / vol_sqrt
        d2 = d1 - vol_sqrt
        reconstructed_e = v_m * norm_cdf(d1) - d_val * math.exp(-r_rf * t_horizon) * norm_cdf(d2)
        assert abs(reconstructed_e - e_val) < 1e-5

        print(
            f"  {name:12s} |  {v_m:7.2f} |    {sv_m:6.4f}   |   {dd_m:6.2f}  |   {pd_m:6.4f}  |  "
            f"{dd_n:6.2f}  |  {pd_n:6.4f}"
        )

    # Compute correlation between Merton DD and Naive DD across the cross-section
    n = len(merton_dds)
    mean_m = sum(merton_dds) / n
    mean_n = sum(naive_dds) / n
    cov = sum((merton_dds[i] - mean_m) * (naive_dds[i] - mean_n) for i in range(n))
    var_m = sum((merton_dds[i] - mean_m) ** 2 for i in range(n))
    var_n = sum((naive_dds[i] - mean_n) ** 2 for i in range(n))
    corr = cov / math.sqrt(var_m * var_n)

    print(f"\nCorrelation between Merton DD and Bharath-Shumway Naive DD: {corr:6.4f}")
    assert corr > 0.98


main()
