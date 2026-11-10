"""Lab E7-L03-1: Central Bank Balance Sheet Mechanics and Reserve Demand.

Simulates central bank balance sheet expansion under asset purchases:
1. Assets: Treasury holdings, agency MBS, discount loans.
2. Liabilities: Currency in circulation, reserve balances, Treasury General Account (TGA), ON RRP.
3. Estimates the reserve demand elasticity function:
   r_t - i_IOR = f(Reserves)
   verifying the transition from a downward-sloping scarcity regime to a flat satiation plateau.
"""

from __future__ import annotations

import math


def simulate_balance_sheet_expansion(
    initial_assets: float,
    qe_purchase: float,
    currency_demand: float,
    tga_balance: float,
    on_rrp_balance: float,
) -> dict[str, float]:
    """Calculate central bank liabilities and total reserves following asset purchases."""
    total_assets = initial_assets + qe_purchase

    # Autonomous factors outside central bank direct daily control
    autonomous_liabilities = currency_demand + tga_balance + on_rrp_balance

    # Reserve balances adjust as the balancing liability item:
    # Assets = Liabilities + Capital => Reserves = Assets - Autonomous_Liabilities (assuming 0 net capital)
    reserves = total_assets - autonomous_liabilities
    if reserves < 0:
        raise ValueError("Autonomous liabilities exceed total assets")

    return {
        "total_assets": total_assets,
        "reserves": reserves,
        "autonomous_liabilities": autonomous_liabilities,
        "reserve_ratio": reserves / total_assets,
    }


def reserve_demand_curve(reserves: float, satiation_threshold: float, r_ceiling: float, r_floor: float) -> float:
    """Nonlinear reserve demand function (Poole 1968 / Afonso et al. 2020).

    When reserves < satiation_threshold, the market rate sits strictly above the floor
    and slopes downward. Once reserves exceed satiation_threshold, the market rate hits the floor.
    """
    if reserves <= 0:
        return r_ceiling

    # Logistic / smooth transition between ceiling and floor
    # As reserves -> 0, rate -> r_ceiling; as reserves >> threshold, rate -> r_floor
    spread = (r_ceiling - r_floor) / (1.0 + math.exp(4.0 * (reserves - satiation_threshold) / satiation_threshold))
    rate = r_floor + spread
    return rate


def main() -> None:
    # Units in billions USD
    initial_assets = 900.0  # Pre-crisis baseline
    qe_purchase = 3000.0  # Large-scale asset purchase program
    currency = 1200.0
    tga = 400.0
    on_rrp = 300.0

    bs = simulate_balance_sheet_expansion(initial_assets, qe_purchase, currency, tga, on_rrp)

    satiation = 1500.0  # Satiation point where demand becomes completely flat
    r_ceiling = 4.50  # Discount window rate (bps / %)
    r_floor = 3.50  # Interest on reserve balances (IORB)

    rate_pre = reserve_demand_curve(bs["total_assets"] - qe_purchase - currency - tga, satiation, r_ceiling, r_floor)
    rate_post = reserve_demand_curve(bs["reserves"], satiation, r_ceiling, r_floor)

    print("Central Bank Balance Sheet and Reserve Demand Dynamics:")
    print(f"  Pre-QE assets:   ${initial_assets:.1f}B")
    print(f"  QE expansion:    +${qe_purchase:.1f}B")
    print(f"  Post-QE assets:  ${bs['total_assets']:.1f}B")
    print(f"  Bank reserves:   ${bs['reserves']:.1f}B ({bs['reserve_ratio']:.1%} of assets)")
    print("\nInterbank Market Clearing Rate:")
    spread_pre = (rate_pre - r_floor) * 100
    spread_post = (rate_post - r_floor) * 100
    print(f"  Scarce reserves regime rate:  {rate_pre:.4f}% (spread over floor: +{spread_pre:.1f} bps)")
    print(f"  Abundant reserves regime rate: {rate_post:.4f}% (spread over floor: +{spread_post:.1f} bps)")


main()
