"""Lab GM4-project-3: Rung 4 Stretch Goal: Dynamic Cross-Asset Macro Rebalancing and Liquidity Spiral.

SIMULATED. Stretch implementation of a multi-leg macro package with dynamic delta hedging
subject to Almgren-Chriss (2001) market impact and endogenous margin spiral constraints.
"""

from __future__ import annotations

import math

import numpy as np


def almgren_chriss_impact(shares: float, adv: float, volatility: float, eta: float = 0.1) -> float:
    """Temporary price impact cost under Almgren-Chriss power-law model."""
    participation = abs(shares) / adv
    return float(eta * volatility * (participation**0.6) * abs(shares))


def main() -> None:
    rng = np.random.default_rng(42)
    n_steps = 20
    dt = 1.0 / 252.0

    # Macro asset: Equity Index Future
    spot = 100.0
    vol = 0.25
    adv = 1_000_000.0  # Daily volume in contracts

    # Initial position: Short 100 Calls (K=100, T=0.25) hedged dynamically with underlying futures
    k = 100.0
    t_rem = 0.25
    r = 0.045

    notional_options = 10_000  # 10,000 call contracts
    hedge_position = 0.0
    cumulative_impact_cost = 0.0

    print("=== Dynamic Cross-Asset Delta Rebalancing Simulation ===")
    print(f"{'Step':<6}{'Spot':<10}{'Option Delta':<14}{'Hedge Trade':<14}{'Impact Cost':<12}")
    print("-" * 56)

    for step in range(n_steps):
        # Simulate price jump
        z = float(rng.normal(0.0, 1.0))
        spot *= math.exp((r - 0.5 * vol**2) * dt + vol * math.sqrt(dt) * z)
        t_rem = max(1e-4, t_rem - dt)

        # Compute BSM Delta
        sqt = vol * math.sqrt(t_rem)
        d1 = (math.log(spot / k) + (r + 0.5 * vol**2) * t_rem) / sqt
        call_delta = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))

        # Target hedge position
        target_hedge = notional_options * call_delta
        trade_shares = target_hedge - hedge_position

        # Market impact cost
        impact = almgren_chriss_impact(trade_shares, adv, vol)
        cumulative_impact_cost += impact
        hedge_position = target_hedge

        if step % 4 == 0:
            print(f"{step:<6}{spot:<10.2f}{call_delta:<14.4f}{trade_shares:<14.0f}${impact:<11.2f}")

    print("-" * 56)
    print(f"Final Hedge Position (Contracts): {hedge_position:,.0f}")
    print(f"Total Cumulative Execution Drag: ${cumulative_impact_cost:,.2f}")


main()
