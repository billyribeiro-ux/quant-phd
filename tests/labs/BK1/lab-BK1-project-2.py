"""Lab BK1-project-2: Rung 2 completion problem — NII weighting and deposit pass-through.

Complete the implementation of 12-month Net Interest Income sensitivity:
1. Weight each position repricing at month m <= 12 by (12 - m) / 12.
2. Incorporate deposit beta pass-through into deposit interest expense.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Position:
    cents: int
    months: int | None
    side: str


@dataclass(frozen=True)
class DepositBook:
    cents: int
    beta_bp: int


def round_cents(f: Fraction) -> int:
    if f >= 0:
        return (f.numerator * 2 + f.denominator) // (f.denominator * 2)
    else:
        return -((-f.numerator * 2 + f.denominator) // (f.denominator * 2))


def nii_change_cents(positions: list[Position], deposits: DepositBook, shock_bp: int) -> int:
    delta_nii_frac = Fraction(0, 1)
    shock_frac = Fraction(shock_bp, 10_000)

    for p in positions:
        if p.months is not None and 1 <= p.months <= 12:
            weight = Fraction(12 - p.months, 12)
            term = Fraction(p.cents, 1) * shock_frac * weight
            if p.side == "asset":
                delta_nii_frac += term
            else:
                delta_nii_frac -= term

    beta_frac = Fraction(deposits.beta_bp, 10_000)
    dep_expense = Fraction(deposits.cents, 1) * beta_frac * shock_frac
    delta_nii_frac -= dep_expense
    return round_cents(delta_nii_frac)


def main() -> None:
    # 3-position test instance (cents)
    positions = [
        Position(10_000_000, 3, "asset"),  # Reprices at m=3, weight (12-3)/12 = 9/12
        Position(6_000_000, 6, "liability"),  # Reprices at m=6, weight (12-6)/12 = 6/12
    ]
    deposits = DepositBook(cents=8_000_000, beta_bp=5000)  # beta = 0.50
    shock_bp = 100  # +100 bp (0.01)

    # Asset gain: 10,000,000 * 0.01 * (9/12) = +75,000
    # Liability expense: 6,000,000 * 0.01 * (6/12) = +30,000
    # Deposit expense: 8,000,000 * 0.5 * 0.01 = +40,000
    # Net NII change: +75,000 - 30,000 - 40,000 = +5,000 cents
    result = nii_change_cents(positions, deposits, shock_bp)
    print("A. Completion Check: 12-Month Net Interest Income Sensitivity")
    print(f"Computed NII change: {result:+6d} cents")
    print(f"Matches theoretical closed-form (+5000 cents): {result == 5000}")


main()
