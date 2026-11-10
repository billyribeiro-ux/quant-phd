"""Lab BK1-L08-1: Liquidity regulation — Liquidity Coverage Ratio (LCR) and Net Stable Funding Ratio (NSFR).

The Basel III framework introduces two complementary liquidity standards:
1. Liquidity Coverage Ratio (LCR): Short-term 30-day survival under acute stress:
       LCR = HQLA / Total Net Cash Outflows over 30 Days >= 100%
   where HQLA comprises Level 1 (0% haircut) and Level 2A (15% haircut) assets,
   and net outflows equal gross outflows minus inflows (capped at 75% of outflows).

2. Net Stable Funding Ratio (NSFR): Structural 1-year maturity transformation constraint:
       NSFR = Available Stable Funding (ASF) / Required Stable Funding (RSF) >= 100%

This lab evaluates:
1. Base HQLA, 30-day net outflows, and LCR on a SIMULATED balance sheet (in cents).
2. Base Available Stable Funding, Required Stable Funding, and NSFR.
3. Impact on LCR when retail deposit stress escalates (outflow rate rises from 5% to 25%).
"""

from __future__ import annotations

from fractions import Fraction

# --- LCR Inputs in cents ---
# Liquid Assets
CASH_RESERVES_CENTS = 25_000_000  # Level 1 (0% haircut) -> 100% value
SOVEREIGN_BONDS_CENTS = 35_000_000  # Level 1 (0% haircut) -> 100% value
CORPORATE_BONDS_CENTS = 20_000_000  # Level 2A (15% haircut) -> 85% value

# 30-Day Outflow Liabilities
RETAIL_DEPOSITS_CENTS = 120_000_000  # Base run-off: 5%
WHOLESALE_DEPOSITS_CENTS = 60_000_000  # Non-operational: 40% run-off
UNDRAWN_COMMITTED_CENTS = 40_000_000  # Committed facilities: 10% draw

# 30-Day Contractual Inflows
CONTRACTUAL_INFLOWS_CENTS = 15_000_000  # Cap applies at 75% of outflows

# --- NSFR Inputs in cents ---
CAPITAL_AND_LONG_DEBT = 40_000_000  # 100% ASF factor
STABLE_RETAIL_DEPOSITS = 120_000_000  # 90% ASF factor
SHORT_WHOLESALE_FUNDING = 40_000_000  # 0% ASF factor

LEVEL1_LIQUID_ASSETS = 60_000_000  # 0% RSF factor
MORTGAGES_LONG = 70_000_000  # 65% RSF factor
COMMERCIAL_LOANS_LONG = 70_000_000  # 85% RSF factor


def compute_hqla() -> int:
    """Total High-Quality Liquid Assets in cents."""
    lvl1 = CASH_RESERVES_CENTS + SOVEREIGN_BONDS_CENTS
    lvl2a = Fraction(CORPORATE_BONDS_CENTS * 85, 100)
    return int(lvl1 + lvl2a)


def compute_net_outflows(retail_run_pct: int) -> int:
    """Total 30-day net outflows in cents given retail deposit run-off percent."""
    out_retail = Fraction(RETAIL_DEPOSITS_CENTS * retail_run_pct, 100)
    out_wholesale = Fraction(WHOLESALE_DEPOSITS_CENTS * 40, 100)
    out_commit = Fraction(UNDRAWN_COMMITTED_CENTS * 10, 100)
    gross_outflows = out_retail + out_wholesale + out_commit

    # Inflow cap: max 75% of gross outflows
    cap = gross_outflows * Fraction(75, 100)
    capped_inflows = min(Fraction(CONTRACTUAL_INFLOWS_CENTS, 1), cap)
    net_outflows = gross_outflows - capped_inflows
    return int(net_outflows)


def compute_nsfr() -> tuple[int, int, int]:
    """Compute (ASF_cents, RSF_cents, nsfr_ratio_bp)."""
    asf = (
        Fraction(CAPITAL_AND_LONG_DEBT, 1) * 1
        + Fraction(STABLE_RETAIL_DEPOSITS, 1) * Fraction(90, 100)
        + Fraction(SHORT_WHOLESALE_FUNDING, 1) * 0
    )
    rsf = (
        Fraction(LEVEL1_LIQUID_ASSETS, 1) * 0
        + Fraction(MORTGAGES_LONG, 1) * Fraction(65, 100)
        + Fraction(COMMERCIAL_LOANS_LONG, 1) * Fraction(85, 100)
    )
    ratio_bp = (asf * 10_000) / rsf
    return int(asf), int(rsf), int(ratio_bp)


def main() -> None:
    print("A. Liquidity Coverage Ratio (30-Day Stress, SIMULATED, in cents)")
    hqla = compute_hqla()
    net_outflows_base = compute_net_outflows(retail_run_pct=5)
    lcr_base_bp = int(Fraction(hqla, net_outflows_base) * 10_000)

    print(f"Total HQLA (after haircuts):      {hqla:11d} cents")
    print(f"Base 30-Day Net Outflows (5% run): {net_outflows_base:11d} cents")
    print(f"Base LCR:                         {lcr_base_bp:5d} bp ({lcr_base_bp / 100:.2f}%) [Min = 10000 bp / 100%]")

    print()
    print("B. Severe Retail Deposit Stress Scenario (Run-off rises to 25%)")
    net_outflows_stress = compute_net_outflows(retail_run_pct=25)
    lcr_stress_bp = int(Fraction(hqla, net_outflows_stress) * 10_000)
    print(f"Stressed 30-Day Net Outflows:     {net_outflows_stress:11d} cents")
    print(f"Stressed LCR:                     {lcr_stress_bp:5d} bp ({lcr_stress_bp / 100:.2f}%)")
    print(f"LCR deficit below 100% regulatory standard: {lcr_stress_bp < 10_000}")

    print()
    print("C. Net Stable Funding Ratio (1-Year Horizon, SIMULATED, in cents)")
    asf, rsf, nsfr_bp = compute_nsfr()
    print(f"Available Stable Funding (ASF):   {asf:11d} cents")
    print(f"Required Stable Funding (RSF):    {rsf:11d} cents")
    print(f"NSFR:                             {nsfr_bp:5d} bp ({nsfr_bp / 100:.2f}%) [Min = 10000 bp / 100%]")

    print()
    print("D. Invariant Checks")
    print(f"Base LCR satisfies regulatory standard: {lcr_base_bp >= 10_000}")
    print(f"Base NSFR satisfies regulatory standard: {nsfr_bp >= 10_000}")
    print(f"Severe deposit run strictly reduces LCR: {lcr_stress_bp < lcr_base_bp}")


main()
