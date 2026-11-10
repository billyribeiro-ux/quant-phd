"""Lab BK1-L06-1: Deposit franchise and deposit beta pass-through.

Deposit beta measures the pass-through of market interest rate changes to deposit rates:
    beta = Delta r_D / Delta r,  where beta in [0, 1]

Drechsler, Savov & Schnabl (2017, 2021) show that market power enables banks to pay
sticky below-market deposit rates (beta < 1), generating a deposit franchise that acts
as a hedge against rising rates. However, as Jiang, Matvos, Piskorski & Seru (2024) show,
run risk and deposit disintermediation can rapidly erode this hedge.

This lab simulates:
1. Floating assets of 100,000,000 cents ($1,000,000) repricing fully with market rates.
2. Core non-maturity deposits of 80,000,000 cents ($800,000) with deposit beta.
3. Market rate shock Delta r = +200 bp.
4. Net Interest Income (NII) change across betas [0.00, 0.25, 0.50, 0.75, 1.00].
5. Exact linearity check: Delta NII at beta=0.50 is the midpoint between beta=0.00 and beta=1.00.
"""

from __future__ import annotations

from fractions import Fraction

ASSETS_CENTS = 100_000_000  # $1,000,000 floating-rate assets
DEPOSITS_CENTS = 80_000_000  # $800,000 core deposits
SHOCK_BP = 200  # +200 bp rate rise


def compute_nii_change(assets_cents: int, deposits_cents: int, shock_bp: int, beta_bp: int) -> int:
    """Calculate annual NII change in cents for given deposit beta in bp."""
    shock_frac = Fraction(shock_bp, 10_000)
    beta_frac = Fraction(beta_bp, 10_000)

    asset_income_change = Fraction(assets_cents, 1) * shock_frac
    dep_expense_change = Fraction(deposits_cents, 1) * (beta_frac * shock_frac)

    delta_nii = asset_income_change - dep_expense_change
    # Round half away from zero
    if delta_nii >= 0:
        return (delta_nii.numerator * 2 + delta_nii.denominator) // (delta_nii.denominator * 2)
    else:
        return -((-delta_nii.numerator * 2 + delta_nii.denominator) // (delta_nii.denominator * 2))


def main() -> None:
    print("A. Deposit Beta and 1-Year NII Sensitivity (+200 bp shock, SIMULATED, in cents)")
    betas_bp = [0, 2500, 5000, 7500, 10_000]

    results: dict[int, int] = {}
    for b_bp in betas_bp:
        delta_nii = compute_nii_change(ASSETS_CENTS, DEPOSITS_CENTS, SHOCK_BP, b_bp)
        results[b_bp] = delta_nii
        beta_float = b_bp / 10_000
        # Deposit franchise margin gain: (1 - beta) * shock * deposits
        franchise_gain = Fraction(DEPOSITS_CENTS, 1) * Fraction(10_000 - b_bp, 10_000) * Fraction(SHOCK_BP, 10_000)
        print(
            f"Beta = {beta_float:4.2f} ({b_bp:5d} bp) | "
            f"Delta NII: {delta_nii:+9d} cents | Franchise Benefit: {int(franchise_gain):8d} cents"
        )

    print()
    print("B. Linearity and Invariant Checks")
    nii_0 = results[0]
    nii_50 = results[5000]
    nii_100 = results[10_000]

    print(f"NII change at beta 0.50 equals midpoint of beta 0 and 1: {nii_50 == (nii_0 + nii_100) // 2}")
    print(f"Monotonicity: Higher deposit beta strictly reduces NII gain: {nii_0 > nii_50 > nii_100}")
    print(f"Franchise hedge positive for beta < 1: {results[5000] > results[10_000]}")


main()
