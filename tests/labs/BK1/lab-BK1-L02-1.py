"""Lab BK1-L02-1: Maturity transformation and refinancing risk.

Maturity transformation occurs when a financial institution funds long-term, fixed-rate
assets using short-term, rolling liabilities. This generates a structural refinancing gap:
the asset yield is locked, while funding liabilities reprice at prevailing market rates.

This lab simulates:
1. A 3-year fixed-rate asset of 10,000,000 cents ($100,000) earning 6.00% per year.
2. Funded by rolling 1-year deposits, resetting each year at rates:
   Year 1: 3.00% (300 bp)
   Year 2: 5.00% (500 bp)
   Year 3: 7.50% (750 bp)
3. The refinancing gap, annual net interest income, and margin compression.
"""

from __future__ import annotations

from fractions import Fraction

PRINCIPAL_CENTS = 10_000_000  # $100,000 principal
ASSET_RATE_BP = 600  # 6.00% annual coupon / yield
DEPOSIT_RATES_BP = [300, 500, 750]  # Rolling 1-year deposit rates in bp


def annual_cash_flows(principal_cents: int, asset_rate_bp: int, dep_rates_bp: list[int]) -> list[dict[str, int]]:
    """Compute interest income, interest expense, and net interest income in cents per year."""
    flows: list[dict[str, int]] = []
    for year_idx, dep_rate_bp in enumerate(dep_rates_bp, start=1):
        income = Fraction(principal_cents * asset_rate_bp, 10_000)
        expense = Fraction(principal_cents * dep_rate_bp, 10_000)
        net_income = income - expense
        flows.append(
            {
                "year": year_idx,
                "asset_rate_bp": asset_rate_bp,
                "dep_rate_bp": dep_rate_bp,
                "income_cents": int(income),
                "expense_cents": int(expense),
                "nii_cents": int(net_income),
            }
        )
    return flows


def main() -> None:
    print("A. Maturity Mismatch: 3-Year Fixed Asset vs Rolling 1-Year Liabilities (SIMULATED, in cents)")
    flows = annual_cash_flows(PRINCIPAL_CENTS, ASSET_RATE_BP, DEPOSIT_RATES_BP)

    cumulative_nii = 0
    for row in flows:
        cumulative_nii += row["nii_cents"]
        spread_bp = row["asset_rate_bp"] - row["dep_rate_bp"]
        print(
            f"Year {row['year']} | Asset: {row['asset_rate_bp']} bp, Dep: {row['dep_rate_bp']} bp | "
            f"Spread: {spread_bp:+4d} bp | Income: {row['income_cents']:8d} | "
            f"Expense: {row['expense_cents']:8d} | NII: {row['nii_cents']:+8d} cents"
        )

    print()
    print("B. Cumulative Net Interest Income across 3 Years")
    print(f"Total Cumulative NII: {cumulative_nii:+8d} cents")

    print()
    print("C. Refinancing Gap and Invariant Checks")
    # Asset repricing occurs only at year 3; liability repricing occurs at years 1, 2, 3
    # At t=1 and t=2, rate-sensitive liabilities = 10,000,000, rate-sensitive assets = 0
    refinancing_gap_t1 = 0 - PRINCIPAL_CENTS
    refinancing_gap_t2 = 0 - PRINCIPAL_CENTS
    refinancing_gap_t3 = PRINCIPAL_CENTS - PRINCIPAL_CENTS  # Both mature
    print(f"Refinancing Gap Year 1: {refinancing_gap_t1} cents (negative indicates liability sensitive)")
    print(f"Refinancing Gap Year 2: {refinancing_gap_t2} cents")
    print(f"Refinancing Gap Year 3: {refinancing_gap_t3} cents")
    print(f"Margin inversion occurs in Year 3 (deposit rate > asset rate): {flows[2]['nii_cents'] < 0}")


main()
