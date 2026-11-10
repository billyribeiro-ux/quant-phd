"""Lab AP6-L03-1: Slow-Moving Capital and Dynamic Supply Shock Absorption.

SIMULATED: Calibrates the Duffie (2010) search-and-matching framework where outside
investor capital arrives with search friction intensity lambda. Demonstrates the
immediate price drop (liquidity discount) and subsequent exponential price recovery.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # Model parameters calibrated to Duffie (2010) Presidential Address
    # Asset pays steady dividend flow d = 5.0 per year. Risk-free rate r = 0.05
    r = 0.05
    d = 5.0
    p_fundamental = d / r  # $100.00 fundamental price

    # Sudden supply shock at t = 0: Delta S = 20 units dumped on the dealer market
    # Dealer inventory capacity parameter gamma_d (holding cost / risk aversion)
    # Outside capital arrival rate: lambda = 0.8 per year (mean search time 1.25 years)
    delta_s = 20.0
    gamma_d = 0.15  # dealer marginal holding cost per unit of inventory
    lambda_arrival = 0.80  # search arrival intensity of long-term investors

    # Time grid: t in [0, 5] years
    n_points = 21
    time_grid = np.linspace(0.0, 5.0, n_points)

    # Dealer inventory path: I(t) = Delta S * exp(-lambda * t)
    # For a pure transitory dislocation with gamma_outside -> 0:
    # Discount Delta P(t) = - gamma_d / (r + lambda) * Delta S * exp(-lambda * t)
    discount_initial = (gamma_d / (r + lambda_arrival)) * delta_s
    price_path = np.zeros(n_points)
    inventory_path = np.zeros(n_points)

    for i, t in enumerate(time_grid):
        inventory_path[i] = delta_s * np.exp(-lambda_arrival * t)
        dislocation_t = discount_initial * np.exp(-lambda_arrival * t)
        price_path[i] = p_fundamental - dislocation_t

    half_life = np.log(2.0) / lambda_arrival

    print("Duffie (2010) Slow-Moving Capital Supply Shock Dynamics")
    print(f"Fundamental asset price P*:       ${p_fundamental:.2f}")
    print(f"Supply shock magnitude Delta S:   {delta_s:.1f} shares")
    print(f"Outside capital search rate lambda: {lambda_arrival:.2f} / year")
    print(f"Dislocation half-life:            {half_life:.2f} years ({half_life * 12:.1f} months)")
    print(f"Post-shock price at t=0:          ${price_path[0]:.2f}")
    print(f"Initial liquidity discount:       ${discount_initial:.2f} ({discount_initial / p_fundamental * 100:.2f}%)")
    print(f"Recovered price at t=1 year:      ${price_path[4]:.2f}")
    print(f"Recovered price at t=5 years:     ${price_path[-1]:.2f}")
    print(f"Rebound share after 1 year:       {(price_path[4] - price_path[0]) / discount_initial * 100:.2f}%")


main()
