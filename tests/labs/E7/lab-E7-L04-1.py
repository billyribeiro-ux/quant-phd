"""Lab E7-L04-1: Operating Frameworks: Corridor vs Floor Systems and Bech-Klee Arbitrage.

Models the equilibrium interbank overnight rate under:
1. Symmetric corridor framework (standing lending facility ceiling, deposit facility floor, scarce reserves)
2. Floor framework (abundant reserves, IORB, and non-bank GSE cash suppliers per Bech-Klee 2011)

Calculates the equilibrium trading volume and the Bech-Klee arbitrage spread:
r_eff = (1 - lambda) * r_IOR + lambda * r_bargain
"""

from __future__ import annotations


def solve_corridor_equilibrium(
    reserve_supply: float,
    reserve_target: float,
    rate_lending: float,
    rate_deposit: float,
    target_rate: float,
) -> float:
    """Interbank clearing rate in a symmetric corridor system."""
    # When supply equals target, clearing rate hits the target exactly
    # Deviations move linearly toward standing facilities
    corridor_width = rate_lending - rate_deposit
    deviation = (reserve_supply - reserve_target) / reserve_target
    rate = target_rate - 0.5 * corridor_width * max(-1.0, min(1.0, deviation))
    return rate


def solve_bech_klee_floor_arbitrage(
    rate_iorb: float,  # Rate paid to commercial banks on reserves
    rate_on_rrp: float,  # Sub-floor offered to non-bank financial institutions (e.g. GSEs, MMFs)
    bank_balance_sheet_cost: float,  # Leverage ratio / FDIC assessment fee per dollar of reserves
    bargaining_power_nonbank: float,  # Nash bargaining weight lambda of cash lenders
) -> dict[str, float]:
    """Calculate the equilibrium federal funds rate below IORB in a floor system with non-banks.

    Per Bech and Klee (2011): Government-Sponsored Enterprises (Fannie Mae, Freddie Mac, FHLBs)
    hold deposits at the Fed but are ineligible to earn IORB. Commercial banks borrow from GSEs
    at rate r_eff and deposit at the Fed earning r_iorb, incurring balance-sheet cost c.
    GSEs receive outside option rate_on_rrp.
    Surplus = rate_iorb - bank_balance_sheet_cost - rate_on_rrp.
    """
    surplus = rate_iorb - bank_balance_sheet_cost - rate_on_rrp
    rate_eff = rate_on_rrp if surplus < 0 else rate_on_rrp + bargaining_power_nonbank * surplus

    arbitrage_margin_bank = rate_iorb - rate_eff - bank_balance_sheet_cost
    spread_below_iorb = rate_iorb - rate_eff

    return {
        "rate_eff": rate_eff,
        "spread_below_iorb_bps": spread_below_iorb * 100.0,
        "bank_arbitrage_margin_bps": arbitrage_margin_bank * 100.0,
        "net_surplus_bps": surplus * 100.0,
    }


def main() -> None:
    # 1. Corridor system benchmark
    r_lend = 5.25
    r_dep = 4.25
    r_target = 4.75
    r_corridor_scarce = solve_corridor_equilibrium(95.0, 100.0, r_lend, r_dep, r_target)

    # 2. Floor system with Bech-Klee non-bank segmentation
    r_iorb = 5.40
    r_on_rrp = 5.30
    c_cost = 0.05  # 5 bps regulatory balance sheet cost
    lambda_gse = 0.40  # GSE bargaining power

    bk = solve_bech_klee_floor_arbitrage(r_iorb, r_on_rrp, c_cost, lambda_gse)

    print("Operating Frameworks Comparison:")
    print("Corridor Framework (Scarce Reserves):")
    print(f"  Ceiling (Lending facility): {r_lend:.2f}%")
    print(f"  Floor (Deposit facility):   {r_dep:.2f}%")
    print(f"  Market rate (5% scarcity):  {r_corridor_scarce:.4f}%")

    print("\nFloor Framework with Bech-Klee (2011) Market Segmentation:")
    print(f"  IORB rate (Commercial bank floor): {r_iorb:.2f}%")
    print(f"  ON RRP rate (Non-bank sub-floor):  {r_on_rrp:.2f}%")
    print(f"  Effective interbank rate:          {bk['rate_eff']:.4f}%")
    print(f"  Discount below IORB:               {bk['spread_below_iorb_bps']:.1f} bps")
    print(f"  Commercial bank net margin:        {bk['bank_arbitrage_margin_bps']:.1f} bps")


main()
