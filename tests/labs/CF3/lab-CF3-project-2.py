"""CF3 project lab 2 (rung 2, completion solution): Core governance and regression calculations.

SIMULATED: Completion exercise testing implementation of E-index, Tobin's Q,
OLS Bessel degrees-of-freedom normalization, and statistical power non-centrality.
Standard library only; deterministic execution.
"""

from __future__ import annotations

import math
from statistics import NormalDist


def main() -> None:
    # 5 Sample firms for quick completion check
    provisions_panel = [
        {
            "staggered_board": 1,
            "poison_pill": 1,
            "golden_parachute": 1,
            "limit_bylaw_amendment": 1,
            "limit_charter_amendment": 0,
            "supermajority_merger": 1,
        },
        {
            "staggered_board": 0,
            "poison_pill": 0,
            "golden_parachute": 1,
            "limit_bylaw_amendment": 0,
            "limit_charter_amendment": 0,
            "supermajority_merger": 0,
        },
        {
            "staggered_board": 1,
            "poison_pill": 0,
            "golden_parachute": 0,
            "limit_bylaw_amendment": 1,
            "limit_charter_amendment": 1,
            "supermajority_merger": 0,
        },
        {
            "staggered_board": 0,
            "poison_pill": 0,
            "golden_parachute": 0,
            "limit_bylaw_amendment": 0,
            "limit_charter_amendment": 0,
            "supermajority_merger": 0,
        },
        {
            "staggered_board": 1,
            "poison_pill": 1,
            "golden_parachute": 1,
            "limit_bylaw_amendment": 1,
            "limit_charter_amendment": 1,
            "supermajority_merger": 1,
        },
    ]

    core_keys = [
        "staggered_board",
        "poison_pill",
        "golden_parachute",
        "limit_bylaw_amendment",
        "limit_charter_amendment",
        "supermajority_merger",
    ]

    # Completed Line 1: E-index calculation
    e_indices = [sum(p[k] for k in core_keys) for p in provisions_panel]

    # Firm balance sheet numbers in cents
    assets = [100_000_00, 80_000_00, 150_000_00, 120_000_00, 90_000_00]
    book_eq = [60_000_00, 50_000_00, 90_000_00, 80_000_00, 50_000_00]
    mkt_eq = [110_000_00, 120_000_00, 150_000_00, 200_000_00, 70_000_00]

    # Completed Line 2: Tobin's Q calculation
    q_vals = [(a - be + me) / a for a, be, me in zip(assets, book_eq, mkt_eq, strict=True)]

    # Bivariate OLS
    n = len(e_indices)
    mean_e = sum(e_indices) / n
    mean_q = sum(q_vals) / n
    s_ee = sum((ei - mean_e) ** 2 for ei in e_indices)
    s_eq = sum((ei - mean_e) * (qi - mean_q) for ei, qi in zip(e_indices, q_vals, strict=True))

    # Completed Line 3: OLS slope beta
    beta = s_eq / s_ee
    alpha = mean_q - beta * mean_e

    rss = sum((qi - (alpha + beta * ei)) ** 2 for ei, qi in zip(e_indices, q_vals, strict=True))

    # Completed Line 4: Residual variance with n - 2 degrees of freedom
    s_squared = rss / (n - 2)
    se_beta = math.sqrt(s_squared / s_ee)

    # Completed Line 5: Non-centrality parameter delta
    delta = abs(beta) / se_beta

    dist = NormalDist()
    z_crit = dist.inv_cdf(1.0 - 0.05 / 2.0)
    power = (1.0 - dist.cdf(z_crit - delta)) + dist.cdf(-z_crit - delta)

    print("CF3 Project Rung 2: Completion Lab Results")
    print(f"Computed E-indices:      {e_indices}")
    print(f"Computed Tobin's Q:      {[round(q, 4) for q in q_vals]}")
    print(f"OLS Slope (beta):        {beta:.4f}")
    print(f"Residual variance (s^2): {s_squared:.6f}")
    print(f"SE of Slope (se_beta):   {se_beta:.4f}")
    print(f"Non-centrality (delta):  {delta:.4f}")
    print(f"Statistical Power:       {power:.2%}")


main()
