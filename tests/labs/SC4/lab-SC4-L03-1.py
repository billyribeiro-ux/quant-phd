"""Lab SC4-L03-1 · Feynman-Kac Stochastic Representation vs. Parabolic PDE Analytical Solution.

Verifies the Feynman-Kac equivalence between the conditional expectation of discounted terminal payoff
and the solution of the Black-Scholes parabolic PDE using Monte Carlo simulation (SIMULATED).
"""

from __future__ import annotations

import math
import random


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def main() -> None:
    s0 = 100.0
    k = 105.0
    horizon = 1.0
    rate = 0.05
    vol = 0.20
    n_pairs = 25000  # 50,000 total antithetic paths
    seed = 42

    # 1. Analytical PDE solution via Black-Scholes formula
    sqrt_h = math.sqrt(horizon)
    d1 = (math.log(s0 / k) + (rate + 0.5 * vol * vol) * horizon) / (vol * sqrt_h)
    d2 = d1 - vol * sqrt_h
    disc = math.exp(-rate * horizon)
    pde_price = s0 * norm_cdf(d1) - k * disc * norm_cdf(d2)

    # 2. Feynman-Kac conditional expectation via Monte Carlo
    rng = random.Random(seed)
    drift_term = (rate - 0.5 * vol * vol) * horizon
    vol_term = vol * sqrt_h

    payoffs: list[float] = []
    for _ in range(n_pairs):
        z = rng.gauss(0.0, 1.0)
        s_pos = s0 * math.exp(drift_term + vol_term * z)
        s_neg = s0 * math.exp(drift_term - vol_term * z)
        pay_pos = disc * max(s_pos - k, 0.0)
        pay_neg = disc * max(s_neg - k, 0.0)
        payoffs.append(0.5 * (pay_pos + pay_neg))

    mc_estimate = sum(payoffs) / n_pairs
    sample_var = sum((x - mc_estimate) ** 2 for x in payoffs) / (n_pairs - 1)
    se = math.sqrt(sample_var / n_pairs)
    z_stat = abs(mc_estimate - pde_price) / se

    print(f"Analytical PDE solution (Black-Scholes): {pde_price:.6f}")
    print(f"Feynman-Kac Monte Carlo estimate:       {mc_estimate:.6f} (se: {se:.6f})")
    print(f"Pricing absolute difference:            {abs(mc_estimate - pde_price):.4f}")
    print(f"Standardized z-score:                  {z_stat:.3f}")
    print(f"Estimate within 3 standard errors:      {z_stat <= 3.0}")


main()
