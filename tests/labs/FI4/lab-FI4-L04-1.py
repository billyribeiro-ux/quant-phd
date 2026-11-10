"""Lab FI4-L04-1: Dealer Supplementary Leverage Ratio (SLR) constraints and ROE impact.

Evaluates primary dealer balance-sheet capacity, SLR compliance thresholds,
and the return on allocated equity for low-margin Treasury intermediation.
"""

from __future__ import annotations


def calculate_slr(tier1_equity: float, total_leverage_exposure: float) -> float:
    """Compute the Supplementary Leverage Ratio: Tier 1 Capital / TLE."""
    if total_leverage_exposure <= 0.0:
        return float("inf")
    return tier1_equity / total_leverage_exposure


def main() -> None:
    # Baseline Primary Dealer balance sheet (SIMULATED, numbers in USD Billions)
    tier1_capital = 12.0  # $12.0B Tier 1 capital
    cash_treasuries = 70.0  # $70.0B Treasury inventory
    repo_financing = 90.0  # $90.0B matched-book repo
    derivatives_pfe = 20.0  # $20.0B derivatives exposure

    baseline_tle = cash_treasuries + repo_financing + derivatives_pfe  # $180.0B
    baseline_slr = calculate_slr(tier1_capital, baseline_tle)

    print("Baseline Primary Dealer Capital & Exposure (SIMULATED):")
    print(f"  Tier 1 Capital:             ${tier1_capital:,.1f}B")
    print(f"  Treasury Inventory:         ${cash_treasuries:,.1f}B")
    print(f"  Repo Matched Book:          ${repo_financing:,.1f}B")
    print(f"  Derivatives Exposure:       ${derivatives_pfe:,.1f}B")
    print(f"  Total Leverage Exposure:    ${baseline_tle:,.1f}B")
    print(f"  Supplementary Leverage Ratio (SLR): {baseline_slr:.2%}")
    print("  Regulatory Minimum (US G-SIB):      5.00%")
    print(f"  Capital Surplus over 5% hurdle:     ${tier1_capital - 0.05 * baseline_tle:,.2f}B")

    # An arbitrage fund requests $70.0B in Treasury repo financing at a spread of 12 bps (0.12%)
    new_repo_notional = 70.0
    spread_bps = 12.0
    gross_annual_revenue = new_repo_notional * (spread_bps / 10_000.0)  # in $B

    tle_expanded = baseline_tle + new_repo_notional
    slr_expanded = calculate_slr(tier1_capital, tle_expanded)
    capital_surplus_expanded = tier1_capital - 0.05 * tle_expanded

    # Capital required to support the new $70B position under 5% SLR
    allocated_equity = 0.05 * new_repo_notional  # $3.5B equity
    roe_on_trade = gross_annual_revenue / allocated_equity

    print("\nIntermediation Trade Expansion (+$70.0B Repo at +12 bps spread):")
    print(f"  New Total Leverage Exposure: ${tle_expanded:,.1f}B")
    print(f"  Post-Trade SLR:              {slr_expanded:.2%}")
    print(f"  Compliant with 5% Rule:      {slr_expanded >= 0.05}")
    print(f"  Post-Trade Capital Surplus:  ${capital_surplus_expanded:,.2f}B (Deficit! Dealer cannot intermediate)")
    print(f"  Annual Revenue from Trade:   ${gross_annual_revenue * 1_000:,.1f}M")
    print(f"  Allocated Equity Required:   ${allocated_equity:,.1f}B")
    print(f"  Return on Allocated Equity:  {roe_on_trade:.2%} (Far below dealer hurdle rate of 10.0%)")

    # Policy Response: Federal Reserve April 2020 Temporary SLR Exclusion (frb2020federal)
    # Exclude Treasuries ($70.0B) from denominator
    tle_exempt = (baseline_tle + new_repo_notional) - cash_treasuries
    slr_exempt = calculate_slr(tier1_capital, tle_exempt)
    surplus_exempt = tier1_capital - 0.05 * tle_exempt

    print("\nCOVID-19 Regulatory Relief (FRB Temporary Exclusion of Treasuries):")
    print(f"  Exempt Leverage Exposure:    ${tle_exempt:,.1f}B (-${cash_treasuries:,.1f}B Treasuries)")
    print(f"  Exempt SLR:                  {slr_exempt:.2%}")
    print(f"  New Capital Surplus:         ${surplus_exempt:,.2f}B (Restored dealer intermediation capacity)")


main()
