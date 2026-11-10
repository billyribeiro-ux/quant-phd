"""Lab MS4-L03-1: Strategy capacity modeling and alpha degradation under square-root impact.

Derives the portfolio market impact friction coefficient kappa, solves for break-even AUM
and profit-maximizing AUM, and traces net alpha decay (Frazzini, Israel & Moskowitz 2018).
SIMULATED: deterministic calibrated equity universe and rebalancing targets.
"""

from __future__ import annotations

import math


def run_strategy_capacity_modeling() -> None:
    # Portfolio universe: 10 representative assets
    # (weight_initial, weight_target, daily_adv_dollars, daily_vol)
    universe = [
        (0.12, 0.02, 45000000.0, 0.018),
        (0.08, 0.16, 28000000.0, 0.022),
        (0.15, 0.05, 60000000.0, 0.016),
        (0.05, 0.15, 22000000.0, 0.025),
        (0.10, 0.10, 35000000.0, 0.019),
        (0.06, 0.14, 18000000.0, 0.028),
        (0.14, 0.04, 50000000.0, 0.017),
        (0.09, 0.11, 30000000.0, 0.021),
        (0.11, 0.09, 40000000.0, 0.020),
        (0.10, 0.14, 25000000.0, 0.024),
    ]

    prefactor_y = 0.50
    gross_alpha = 0.08  # 8.0% annualized gross alpha

    # Compute portfolio friction coefficient kappa
    # kappa = Y * sum( sigma_i * |Delta w_i|^{1.5} / sqrt(ADV_i) )
    kappa = prefactor_y * sum(
        vol * (abs(w_tgt - w_init) ** 1.5) / math.sqrt(adv) for w_init, w_tgt, adv, vol in universe
    )

    # Break-even capacity A* (where net alpha hits 0)
    # alpha_0 - kappa * sqrt(A*) = 0 => A* = (alpha_0 / kappa)^2
    a_star = (gross_alpha / kappa) ** 2

    # Profit-maximizing capacity A_opt = (4/9) * A*
    a_opt = (4.0 / 9.0) * a_star

    # Maximum dollar alpha at A_opt
    max_dollar_alpha = (4.0 / 27.0) * (gross_alpha**3) / (kappa**2)
    net_alpha_at_opt = gross_alpha / 3.0

    print(f"Gross Annualized Alpha:      {gross_alpha * 100.0:.2f}% ({gross_alpha * 10000.0:.1f} bps)")
    print(f"Friction Coefficient Kappa:  {kappa:.8e}")
    print(f"Break-even Capacity A*:      {a_star:.2f}")
    print(f"Profit-maximizing AUM A_opt: {a_opt:.2f}")
    print(f"Capacity Ratio A_opt / A*:   {a_opt / a_star:.4f}")
    print(f"Net Alpha at A_opt:          {net_alpha_at_opt * 100.0:.2f}% ({net_alpha_at_opt * 10000.0:.1f} bps)")
    print(f"Max Annual Dollar Alpha:     {max_dollar_alpha:.2f}")
    print("-----------------------------------------------------------------------------------------")
    print("AUM Level            | Unit Cost bps | Net Alpha (%) | Dollar Alpha ($)")
    print("-----------------------------------------------------------------------------------------")

    grid_fractions = [0.10, 4.0 / 9.0, 0.75, 1.00, 1.25]
    for frac in grid_fractions:
        aum = frac * a_star
        cost_dollars = kappa * (aum**1.5)
        cost_fraction = cost_dollars / aum
        cost_bps = cost_fraction * 10000.0
        net_alpha = gross_alpha - cost_fraction
        dollar_alpha = aum * net_alpha
        print(f"{aum:20.2f} | {cost_bps:13.2f} | {net_alpha * 100.0:13.2f} | {dollar_alpha:16.2f}")


def main() -> None:
    run_strategy_capacity_modeling()


main()
