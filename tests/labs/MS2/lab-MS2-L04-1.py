"""Lab MS2-L04-1: Dark pool and PFOF cream-skimming simulator.

Simulates order segmentation between retail (uninformed) and institutional (informed)
traders, demonstrating how off-exchange internalization widens lit bid-ask spreads.
"""

from __future__ import annotations

import random


def simulate_market_segmentation(
    n_orders: int,
    retail_share: float,
    internalize_rate: float,
    informed_impact: float,
    order_processing_cost: float,
    rng: random.Random,
) -> dict[str, float]:
    """Simulate order flow routing with off-exchange retail internalization.

    Returns:
        dict of metrics for the lit exchange and overall market.
    """
    lit_informed = 0
    lit_uninformed = 0
    internalized_retail = 0

    for _ in range(n_orders):
        is_retail = rng.random() < retail_share
        if is_retail:
            if rng.random() < internalize_rate:
                # Internalized by wholesaler off-exchange
                internalized_retail += 1
            else:
                # Spills over to lit exchange
                lit_uninformed += 1
        else:
            # Informed / toxic flow must execute on lit exchange
            lit_informed += 1

    total_lit = lit_informed + lit_uninformed
    lit_informed_share = lit_informed / total_lit if total_lit > 0 else 0.0

    # Competitive half-spread on lit exchange under zero-profit condition:
    # H = (P(informed | lit) * informed_impact) + order_processing_cost
    lit_half_spread = lit_informed_share * informed_impact + order_processing_cost

    return {
        "total_orders": float(n_orders),
        "internalized_retail": float(internalized_retail),
        "lit_orders": float(total_lit),
        "lit_informed_share": round(lit_informed_share, 4),
        "lit_half_spread": round(lit_half_spread, 4),
    }


def main() -> None:
    rng = random.Random(42)
    n_orders = 10000
    retail_share = 0.65  # 65% of all orders are uninformed retail
    informed_impact = 0.20  # adverse selection cost of informed trade ($0.20)
    proc_cost = 0.02  # order handling cost ($0.02)

    # Evaluate internalization rate from 0% (consolidated lit market) to 90% (heavy PFOF)
    internalize_rates = [0.0, 0.25, 0.50, 0.75, 0.90]

    print("PFOF Cream-Skimming: Internalization Rate vs Lit Spread (N=10000 orders):")
    print("Internalize % | Lit Orders | Lit Informed Share | Lit Quoted Spread ($) | Spread Widening")
    print("-----------------------------------------------------------------------------------------")

    base_spread = 0.0
    for rho in internalize_rates:
        res = simulate_market_segmentation(
            n_orders,
            retail_share,
            rho,
            informed_impact,
            proc_cost,
            rng,
        )
        quoted_spread = 2.0 * res["lit_half_spread"]
        if rho == 0.0:
            base_spread = quoted_spread
        widening_pct = ((quoted_spread - base_spread) / base_spread) * 100.0 if base_spread > 0 else 0.0

        print(
            f"   {rho * 100.0:5.1f}%     | {int(res['lit_orders']):10d} | "
            f"{res['lit_informed_share']:18.4f} | ${quoted_spread:20.4f} | {widening_pct:14.2f}%"
        )


main()
