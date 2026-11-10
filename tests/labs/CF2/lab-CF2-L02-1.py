"""CF2 lab L02-1: Beta estimation, unlevering, and relevering.

SIMULATED: Firm and market returns are generated from a seeded normal distribution.
No real financial company data is used.
Demonstrates OLS beta estimation via sample covariance over sample variance,
unlevering equity beta to asset beta under the Hamada relationship, and the
exact mathematical inversion of the relevering round-trip.
"""

from __future__ import annotations

import random
from collections.abc import Sequence

SEED = 20261110


def simulate_returns(
    n_periods: int,
    true_beta: float,
    seed: int,
) -> tuple[list[float], list[float]]:
    """Generate SIMULATED monthly market and firm returns."""
    rng = random.Random(seed)
    market = [rng.gauss(0.008, 0.045) for _ in range(n_periods)]
    firm = [0.002 + true_beta * m + rng.gauss(0.0, 0.030) for m in market]
    return firm, market


def estimate_beta(firm: Sequence[float], market: Sequence[float]) -> float:
    """Compute OLS beta as sample covariance over sample variance (with n - 1)."""
    n = len(firm)
    if n != len(market) or n < 2:
        raise ValueError("Return series must have identical length >= 2")
    mean_m = sum(market) / n
    mean_f = sum(firm) / n
    cov_fm = sum((f - mean_f) * (m - mean_m) for f, m in zip(firm, market, strict=True)) / (n - 1)
    var_m = sum((m - mean_m) ** 2 for m in market) / (n - 1)
    return cov_fm / var_m


def unlever(beta_l: float, de_ratio: float, tax_rate: float) -> float:
    """Hamada formula: beta_U = beta_L / [1 + (1 - tau_c) * (D/E)]."""
    return beta_l / (1.0 + (1.0 - tax_rate) * de_ratio)


def relever(beta_u: float, de_ratio: float, tax_rate: float) -> float:
    """Inverse Hamada: beta_L = beta_U * [1 + (1 - tau_c) * (D/E)]."""
    return beta_u * (1.0 + (1.0 - tax_rate) * de_ratio)


def main() -> None:
    print("CF2 Lab L02-1: Beta Estimation and Hamada Unlevering/Relevering")
    print("-------------------------------------------------------------")

    true_b = 1.35
    n_obs = 60
    firm_ret, mkt_ret = simulate_returns(n_obs, true_b, SEED)

    b_est = estimate_beta(firm_ret, mkt_ret)
    print(f"SIMULATED 60-month sample: true beta = {true_b:.2f}")
    print(f"Estimated levered beta (beta_L): {b_est:.4f}")

    # Unlevering under stated capital structure
    debt = 40_000_000
    equity = 60_000_000
    de_ratio = debt / equity
    tax_rate = 0.25

    beta_u = unlever(b_est, de_ratio, tax_rate)
    beta_relevered = relever(beta_u, de_ratio, tax_rate)
    round_trip_diff = abs(beta_relevered - b_est)

    print(f"\nCapital structure: D = ${debt:,}, E = ${equity:,}, D/E = {de_ratio:.4f}")
    print(f"Corporate tax rate (tau_c): {tax_rate:.1%}")
    print(f"Unlevered asset beta (beta_U):  {beta_u:.4f}")
    print(f"Relevered equity beta:          {beta_relevered:.4f}")
    print(f"Round-trip difference:          {round_trip_diff:.2e}")
    print(f"Exact round-trip recovered:     {round_trip_diff < 1e-14}")

    print("\nRelevered equity beta across target D/E ratios:")
    for target_de in [0.0, 0.25, 0.50, 0.75, 1.0, 1.5, 2.0]:
        target_bl = relever(beta_u, target_de, tax_rate)
        print(f"  Target D/E = {target_de:4.2f}: Relevered beta_L = {target_bl:.4f}")


main()
