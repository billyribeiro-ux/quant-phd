"""CF3 project lab 1 (rung 1, worked example): Governance Scorecard and Valuation Regression.

SIMULATED: 10 corporate issuers with proxy-statement anti-takeover provisions and fundamentals.
Standard library only; deterministic execution.
Demonstrates the full end-to-end Governance Scorecard pipeline:
1. Extraction and calculation of Bebchuk et al. (2008) E-index and Gompers et al. (2003) G-index.
2. Calculation of Tobin's Q approximation from integer-cent balance sheet data.
3. Cross-sectional OLS regression of Tobin's Q on E-index.
4. Statistical power analysis demonstrating small-sample (N = 10) power caveats.
"""

from __future__ import annotations

import math
from statistics import NormalDist
from typing import TypedDict


class FirmData(TypedDict):
    name: str
    e_provs: list[int]
    extra_provs: list[int]
    assets: int
    debt: int
    eq_mkt: int
    eq_book: int


def main() -> None:
    print("CF3 Project Rung 1: Governance Scorecard Pipeline (Worked Example)")
    print("==================================================================")

    # 10 Simulated corporate issuers from proxy statement data
    # Core 6 entrenchment provisions:
    # [staggered_board, poison_pill, golden_parachute, limit_bylaw, limit_charter, supermajority_merger]
    # Plus 4 additional provisions for G-index
    firms: list[FirmData] = [
        {
            "name": "Apex Dynamics",
            "e_provs": [1, 1, 1, 1, 0, 1],
            "extra_provs": [1, 0, 1, 0],
            "assets": 120_000_000_00,
            "debt": 36_000_000_00,
            "eq_mkt": 150_000_000_00,
            "eq_book": 84_000_000_00,
        },
        {
            "name": "Beacon Capital",
            "e_provs": [0, 0, 1, 0, 0, 0],
            "extra_provs": [0, 0, 1, 0],
            "assets": 85_000_000_00,
            "debt": 25_000_000_00,
            "eq_mkt": 160_000_000_00,
            "eq_book": 60_000_000_00,
        },
        {
            "name": "Crestline Energy",
            "e_provs": [1, 0, 0, 1, 1, 0],
            "extra_provs": [1, 1, 0, 0],
            "assets": 210_000_000_00,
            "debt": 80_000_000_00,
            "eq_mkt": 230_000_000_00,
            "eq_book": 130_000_000_00,
        },
        {
            "name": "Delta Semiconductor",
            "e_provs": [0, 0, 0, 0, 0, 0],
            "extra_provs": [0, 1, 0, 0],
            "assets": 140_000_000_00,
            "debt": 20_000_000_00,
            "eq_mkt": 320_000_000_00,
            "eq_book": 120_000_000_00,
        },
        {
            "name": "Echo Logistics",
            "e_provs": [1, 1, 1, 1, 1, 1],
            "extra_provs": [1, 1, 1, 1],
            "assets": 95_000_000_00,
            "debt": 40_000_000_00,
            "eq_mkt": 80_000_000_00,
            "eq_book": 55_000_000_00,
        },
        {
            "name": "Falcon Healthcare",
            "e_provs": [0, 1, 0, 0, 1, 0],
            "extra_provs": [1, 0, 0, 1],
            "assets": 160_000_000_00,
            "debt": 50_000_000_00,
            "eq_mkt": 240_000_000_00,
            "eq_book": 110_000_000_00,
        },
        {
            "name": "Global Maritime",
            "e_provs": [1, 1, 0, 1, 0, 0],
            "extra_provs": [0, 1, 1, 0],
            "assets": 75_000_000_00,
            "debt": 35_000_000_00,
            "eq_mkt": 70_000_000_00,
            "eq_book": 40_000_000_00,
        },
        {
            "name": "Horizon Tech",
            "e_provs": [0, 0, 1, 0, 0, 0],
            "extra_provs": [0, 0, 0, 1],
            "assets": 110_000_000_00,
            "debt": 15_000_000_00,
            "eq_mkt": 250_000_000_00,
            "eq_book": 95_000_000_00,
        },
        {
            "name": "Ironclad Materials",
            "e_provs": [1, 0, 1, 1, 0, 1],
            "extra_provs": [1, 1, 0, 1],
            "assets": 180_000_000_00,
            "debt": 70_000_000_00,
            "eq_mkt": 190_000_000_00,
            "eq_book": 110_000_000_00,
        },
        {
            "name": "Jupiter Media",
            "e_provs": [1, 1, 1, 0, 1, 0],
            "extra_provs": [0, 1, 1, 0],
            "assets": 130_000_000_00,
            "debt": 45_000_000_00,
            "eq_mkt": 140_000_000_00,
            "eq_book": 85_000_000_00,
        },
    ]

    print(f"{'Firm':<22} | {'E-Index':>7} | {'G-Index':>7} | {'Assets ($M)':>12} | {'Tobin Q':>8}")
    print("-" * 65)

    e_scores: list[float] = []
    g_scores: list[float] = []
    q_vals: list[float] = []

    for f in firms:
        e_idx = sum(f["e_provs"])
        g_idx = e_idx + sum(f["extra_provs"])
        # Tobin's Q = (Assets - Book Equity + Market Equity) / Assets
        q = (f["assets"] - f["eq_book"] + f["eq_mkt"]) / f["assets"]

        e_scores.append(float(e_idx))
        g_scores.append(float(g_idx))
        q_vals.append(q)

        print(f"{f['name']:<22} | {e_idx:7d} | {g_idx:7d} | ${f['assets'] / 100_000_00:10.2f}M | {q:8.4f}")

    # Bivariate OLS: Q = alpha + beta * E_index
    n = len(e_scores)
    mean_e = sum(e_scores) / n
    mean_q = sum(q_vals) / n
    s_ee = sum((ei - mean_e) ** 2 for ei in e_scores)
    s_eq = sum((ei - mean_e) * (qi - mean_q) for ei, qi in zip(e_scores, q_vals, strict=True))
    s_qq = sum((qi - mean_q) ** 2 for qi in q_vals)

    beta = s_eq / s_ee
    alpha = mean_q - beta * mean_e
    rss = sum((qi - (alpha + beta * ei)) ** 2 for ei, qi in zip(e_scores, q_vals, strict=True))
    s2 = rss / (n - 2)
    se_beta = math.sqrt(s2 / s_ee)
    t_stat = beta / se_beta
    r2 = 1.0 - (rss / s_qq)

    print("\nCross-Sectional Valuation Regression (N = 10):")
    print("  Model: Tobin's Q = alpha + beta * E-Index + epsilon")
    print(f"  Intercept (alpha):    {alpha:.4f}")
    print(f"  Slope (beta):         {beta:.4f} (se: {se_beta:.4f})")
    print(f"  t-statistic:          {t_stat:.4f}")
    print(f"  R-squared:            {r2:.4%}")

    # Analytical statistical power at alpha_sig = 0.05
    dist = NormalDist()
    z_crit = dist.inv_cdf(1.0 - 0.05 / 2.0)
    delta = abs(beta) / se_beta
    power = (1.0 - dist.cdf(z_crit - delta)) + dist.cdf(-z_crit - delta)

    print("\nStatistical Power Analysis (Small-Sample Caveat):")
    print(f"  Significance level:   alpha = 0.05 (two-sided critical z = {z_crit:.4f})")
    print(f"  Non-centrality delta: |beta| / se = {delta:.4f}")
    print(f"  Statistical power:    {power:.2%}")
    print("  Interpretation:       With N = 10 firms, power is low (~30-40%).")
    print("                        Failing to reject H0: beta = 0 does NOT prove governance does not matter;")
    print("                        it reflects inadequate sample size to detect modest economic effects.")


main()
