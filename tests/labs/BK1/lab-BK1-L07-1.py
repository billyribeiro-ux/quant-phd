"""Lab BK1-L07-1: Basel III capital requirements and loss absorption.

Basel III capital regulation requires banks to maintain capital ratios against
Risk-Weighted Assets (RWA):
    Capital Ratio = Capital / RWA

The framework establishes hierarchical capital tiers:
- Common Equity Tier 1 (CET1): pure loss-absorbing equity (common stock, retained earnings).
- Tier 1 Capital: CET1 + Additional Tier 1 (AT1 instruments).
- Total Capital: Tier 1 + Tier 2 (subordinated debt, qualifying loan loss reserves).

This lab evaluates:
1. A banking book with illustrative risk-weighted assets (SIMULATED, in cents):
   - Cash / Reserves: 0% risk weight
   - High-grade sovereign debt: 0% risk weight
   - Residential mortgages: 50% risk weight
   - Commercial loans: 100% risk weight
2. Pre-loss CET1 and Total Capital ratios.
3. Post-loss ratios after a credit write-down L on commercial loans (100% risk weight).
4. The exact loss threshold L* that reduces CET1 to a target ratio (e.g. 4.50% = 450 bp).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class AssetExposure:
    name: str
    cents: int
    weight_bp: int


# Illustrative balance sheet in cents
ASSETS: list[AssetExposure] = [
    AssetExposure("Cash & Reserves", 20_000_000, 0),
    AssetExposure("Sovereign Debt", 30_000_000, 0),
    AssetExposure("Residential Mortgages", 60_000_000, 5000),  # 50%
    AssetExposure("Commercial Loans", 90_000_000, 10_000),  # 100%
]

CET1_CENTS = 14_000_000  # $140,000 Common Equity Tier 1
TIER2_CENTS = 6_000_000  # $60,000 Tier 2 subordinated debt
TOTAL_CAPITAL_CENTS = CET1_CENTS + TIER2_CENTS  # 20,000,000 cents


def compute_rwa(asset_list: list[AssetExposure]) -> int:
    """Compute total RWA in cents."""
    total_rwa = Fraction(0, 1)
    for a in asset_list:
        w_frac = Fraction(a.weight_bp, 10_000)
        total_rwa += Fraction(a.cents, 1) * w_frac
    return int(total_rwa)


def capital_ratios(cet1: int, total_cap: int, rwa: int) -> tuple[int, int]:
    """Return (cet1_ratio_bp, total_cap_ratio_bp) rounded to nearest basis point."""
    cet1_bp = (cet1 * 10_000 * 2 + rwa) // (rwa * 2)
    total_bp = (total_cap * 10_000 * 2 + rwa) // (rwa * 2)
    return cet1_bp, total_bp


def solve_loss_for_target_cet1(cet1_0: int, rwa_0: int, target_bp: int, loan_weight_bp: int = 10_000) -> int:
    """Solve for credit loss L on commercial loans such that:

    (CET1_0 - L) / (RWA_0 - w * L) = target_bp / 10000
    => (CET1_0 - L) = t * (RWA_0 - w * L)
    => CET1_0 - t * RWA_0 = L * (1 - t * w)
    => L = (CET1_0 - t * RWA_0) / (1 - t * w)
    """
    t = Fraction(target_bp, 10_000)
    w = Fraction(loan_weight_bp, 10_000)
    num = Fraction(cet1_0, 1) - t * Fraction(rwa_0, 1)
    denom = Fraction(1, 1) - t * w
    loss_frac = num / denom
    # Round half away from zero
    return (loss_frac.numerator * 2 + loss_frac.denominator) // (loss_frac.denominator * 2)


def main() -> None:
    print("A. Base Balance Sheet and Capital Ratios (SIMULATED, in cents)")
    base_rwa = compute_rwa(ASSETS)
    total_assets = sum(a.cents for a in ASSETS)
    cet1_bp, total_bp = capital_ratios(CET1_CENTS, TOTAL_CAPITAL_CENTS, base_rwa)

    print(f"Total Assets:            {total_assets:11d} cents")
    print(f"Risk-Weighted Assets:    {base_rwa:11d} cents (RWA density: {base_rwa * 100 // total_assets}%)")
    print(f"CET1 Capital:            {CET1_CENTS:11d} cents | CET1 Ratio:  {cet1_bp:5d} bp ({cet1_bp / 100:.2f}%)")
    print(f"Total Capital:           {TOTAL_CAPITAL_CENTS:11d} cents | Total Ratio: {total_bp:5d} bp")

    print()
    print("B. Solvency Stress: Credit Loss to Reach Target CET1 Ratio (4.50% / 450 bp)")
    target_bp = 450  # 4.50%
    loss_cents = solve_loss_for_target_cet1(CET1_CENTS, base_rwa, target_bp, loan_weight_bp=10_000)
    print(f"Credit Loss required to reach {target_bp} bp CET1: {loss_cents:9d} cents")

    # Verify post-loss position
    post_cet1 = CET1_CENTS - loss_cents
    post_rwa = base_rwa - loss_cents  # 100% risk weight written off
    post_cet1_bp, _ = capital_ratios(post_cet1, TOTAL_CAPITAL_CENTS - loss_cents, post_rwa)
    print(f"Post-loss CET1 Capital:  {post_cet1:11d} cents")
    print(f"Post-loss RWA:           {post_rwa:11d} cents")
    print(f"Post-loss CET1 Ratio:    {post_cet1_bp:5d} bp (matches target {target_bp} bp)")

    print()
    print("C. Mathematical Invariant Checks")
    print(f"Post-loss ratio matches target exactly: {post_cet1_bp == target_bp}")
    print(f"Loss is less than total CET1 (bank maintains solvency): {0 < loss_cents < CET1_CENTS}")


main()
