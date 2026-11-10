"""Lab SR4-L04-1: Treasury Market Liquidity and Dealer Intermediation Headroom.

SIMULATED. Simulates primary dealer inventory capacity and Treasury market liquidity
during the March 2020 'dash for cash' episode (He, Nagel & Song, 2022; Federal
Reserve Board, 2020). Computes balance-sheet headroom under the Supplementary
Leverage Ratio (SLR), price impact of unabsorbed supply, and the stabilizing effect
of emergency regulatory exclusion of Treasuries and reserves from the SLR denominator.
"""

from __future__ import annotations


def simulate_treasury_liquidity(
    dealer_equity: float,
    initial_assets: float,
    slr_ratio: float,
    inbound_selling: float,
    price_impact_coef_bps_per_billion: float,
    slr_relief_granted: bool,
    exempted_safe_assets: float,
) -> dict[str, float | bool]:
    """Simulate primary dealer balance-sheet capacity and market liquidity dislocation."""
    if dealer_equity <= 0 or slr_ratio <= 0:
        raise ValueError("equity and SLR ratio must be positive")

    # Under standard SLR: TLE = Assets. Maximum balance sheet = Equity / slr_ratio
    # Under SLR relief: TLE = Assets - exempted_safe_assets
    if slr_relief_granted:
        max_total_assets = (dealer_equity / slr_ratio) + exempted_safe_assets
    else:
        max_total_assets = dealer_equity / slr_ratio

    # Balance-sheet headroom for absorbing inbound Treasury sales
    initial_headroom = max(0.0, max_total_assets - initial_assets)

    # Actual absorption by primary dealers
    absorbed_volume = min(inbound_selling, initial_headroom)
    unabsorbed_selling = max(0.0, inbound_selling - initial_headroom)

    # Market price impact: bid-ask spread widening and yield dislocation
    # Base spread in tranquil conditions: 0.25 bps
    base_spread_bps = 0.25
    dislocation_bps = unabsorbed_selling * price_impact_coef_bps_per_billion
    effective_spread_bps = base_spread_bps + dislocation_bps

    return {
        "max_assets": max_total_assets,
        "initial_headroom": initial_headroom,
        "absorbed_volume": absorbed_volume,
        "unabsorbed_selling": unabsorbed_selling,
        "dislocation_bps": dislocation_bps,
        "effective_spread_bps": effective_spread_bps,
        "slr_relief_granted": slr_relief_granted,
    }


def main() -> None:
    # Calibrated to primary dealer aggregates during March 2020 ($ billions)
    dealer_equity = 120.0  # $120B Tier 1 capital across primary dealer bank holding companies
    initial_assets = 2220.0  # $2,220B existing balance-sheet exposure
    slr_ratio = 0.05  # 5% enhanced SLR requirement (20x leverage cap)
    inbound_selling = 320.0  # $320B customer selling wave (basis trade unwind + foreign reserves)
    price_impact_param = 0.08  # 0.08 bps spread widening per $1B unabsorbed flow
    exempted_assets = 600.0  # $600B reserves + Treasuries exempted under FRB April 2020 interim rule

    # Scenario 1: Pre-relief binding SLR constraint
    res_tight = simulate_treasury_liquidity(
        dealer_equity=dealer_equity,
        initial_assets=initial_assets,
        slr_ratio=slr_ratio,
        inbound_selling=inbound_selling,
        price_impact_coef_bps_per_billion=price_impact_param,
        slr_relief_granted=False,
        exempted_safe_assets=0.0,
    )

    # Scenario 2: Post-relief Federal Reserve temporary SLR exclusion
    res_relief = simulate_treasury_liquidity(
        dealer_equity=dealer_equity,
        initial_assets=initial_assets,
        slr_ratio=slr_ratio,
        inbound_selling=inbound_selling,
        price_impact_coef_bps_per_billion=price_impact_param,
        slr_relief_granted=True,
        exempted_safe_assets=exempted_assets,
    )

    print("=== TREASURY MARKET LIQUIDITY AND DEALER SLR CAPACITY (SIMULATED) ===")
    print(f"Dealer Equity: ${dealer_equity:.1f}B | Inbound Selling Shock: ${inbound_selling:.1f}B\n")

    print("Scenario 1: Pre-Relief (Standard 5.0% SLR Binding):")
    print(f"  Maximum Total Assets: ${res_tight['max_assets']:.1f}B")
    print(f"  Dealer Headroom: ${res_tight['initial_headroom']:.1f}B")
    print(f"  Absorbed Volume: ${res_tight['absorbed_volume']:.1f}B")
    print(f"  Unabsorbed Selling: ${res_tight['unabsorbed_selling']:.1f}B")
    print(f"  Yield Dislocation: +{res_tight['dislocation_bps']:.2f} bps")
    print(f"  Treasury Bid-Ask Spread: {res_tight['effective_spread_bps']:.2f} bps")

    print("\nScenario 2: Post-Relief (Federal Reserve SLR Safe-Asset Exclusion):")
    print(f"  Maximum Total Assets: ${res_relief['max_assets']:.1f}B")
    print(f"  Dealer Headroom: ${res_relief['initial_headroom']:.1f}B")
    print(f"  Absorbed Volume: ${res_relief['absorbed_volume']:.1f}B")
    print(f"  Unabsorbed Selling: ${res_relief['unabsorbed_selling']:.1f}B")
    print(f"  Yield Dislocation: +{res_relief['dislocation_bps']:.2f} bps")
    print(f"  Treasury Bid-Ask Spread: {res_relief['effective_spread_bps']:.2f} bps")


main()
