"""Lab PR6-project-2: Project Rung 2 Completion Problem Twin.

SIMULATED: Solution twin for human capital present valuation and optimal lifecycle allocation.
"""

from __future__ import annotations

import numpy as np


def compute_human_capital_and_allocation(
    wages: np.ndarray,
    financial_wealth: np.ndarray,
    r_discount: float,
    gamma: float,
    equity_premium: float,
    equity_vol: float,
    wage_beta: float = 0.0,
    leverage_cap: float = 1.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute human capital profile, Merton total wealth target, and financial equity weights."""
    n = len(wages)
    hc = np.zeros(n)

    # Step 1: Backward present value discounting of remaining career wages
    for t in range(n):
        discounts = (1.0 + r_discount) ** (-np.arange(n - t))
        hc[t] = float(np.sum(wages[t:] * discounts))

    # Step 2: Unconstrained Merton fraction on total wealth
    alpha_star = equity_premium / (gamma * equity_vol**2)

    # Step 3: Optimal financial portfolio weight adjusting for human capital leverage and wage beta
    alpha_f = np.zeros(n)
    for t in range(n):
        w_t = max(financial_wealth[t], 1000.0)
        hc_ratio = hc[t] / w_t
        raw_alloc = alpha_star + (alpha_star - wage_beta) * hc_ratio
        alpha_f[t] = min(leverage_cap, max(0.0, raw_alloc))

    # Target-date fund linear benchmark (90% to 30%)
    tdf = 0.90 - (0.90 - 0.30) * (np.arange(n) / max(1, n - 1))

    return hc, alpha_f, tdf


def main() -> None:
    # 5 sample career checkpoints across 40 years (ages 25, 35, 45, 55, 65)
    ages = np.array([25, 35, 45, 55, 65])
    wages = np.array([50000.0, 70000.0, 85000.0, 80000.0, 65000.0])
    wealth = np.array([25000.0, 150000.0, 450000.0, 950000.0, 1800000.0])

    r_discount = 0.02
    gamma = 4.0
    equity_premium = 0.05
    equity_vol = 0.18
    wage_beta = 0.0

    hc, alpha_f, tdf = compute_human_capital_and_allocation(
        wages=wages,
        financial_wealth=wealth,
        r_discount=r_discount,
        gamma=gamma,
        equity_premium=equity_premium,
        equity_vol=equity_vol,
        wage_beta=wage_beta,
    )

    alpha_merton = equity_premium / (gamma * equity_vol**2)

    print("Project Rung 2 · Completion Lab: Human Capital & Lifecycle Allocation")
    print(f"Base Total-Wealth Merton Weight: {alpha_merton:.4f} (38.58%)")
    print("=" * 76)
    print(
        f"{'Age':<6} {'Wage ($)':<12} {'Wealth ($)':<14} {'Human Capital ($)':<20} {'Alpha Opt':<12} {'TDF Glide':<10}"
    )
    print("-" * 76)
    for i in range(len(ages)):
        print(
            f"{ages[i]:<6d} {wages[i]:<12.1f} {wealth[i]:<14.1f} {hc[i]:<20.1f} "
            f"{alpha_f[i] * 100:8.2f}%   {tdf[i] * 100:8.2f}%"
        )


main()
