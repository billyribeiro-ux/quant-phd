"""Lab FI4-L01-1: Repurchase agreement settlement, interest calculation, and haircut sizing.

Standard library only. All monetary values are computed in exact integer cents using Fraction.
"""

from __future__ import annotations

import math
from fractions import Fraction


def round_cents(x: Fraction) -> int:
    """Round Fraction to nearest whole cent, half-up: floor(x + 1/2)."""
    return math.floor(x + Fraction(1, 2))


def repo_cash_lent(collateral_cents: int, haircut: Fraction) -> int:
    """Cash lent against collateral with haircut h: P = (1 - h) * V."""
    if collateral_cents <= 0 or not (Fraction(0, 1) <= haircut < Fraction(1, 1)):
        raise ValueError("Invalid collateral or haircut")
    return round_cents(Fraction(collateral_cents) * (Fraction(1, 1) - haircut))


def repo_cash_due(cash_lent_cents: int, repo_rate: Fraction, days: int) -> int:
    """Repurchase cash due on ACT/360 day-count: C_due = P * (1 + r * d / 360)."""
    if cash_lent_cents <= 0 or days <= 0 or repo_rate < Fraction(0, 1):
        raise ValueError("Invalid repo financing parameters")
    interest_fraction = Fraction(cash_lent_cents) * repo_rate * Fraction(days, 360)
    return cash_lent_cents + round_cents(interest_fraction)


def main() -> None:
    # SIMULATED collateral values and terms
    collateral_value_usd = 10_000_000
    collateral_cents = collateral_value_usd * 100  # 1,000,000,000 cents ($10,000,000.00)
    haircut = Fraction(2, 100)  # 2.0% haircut
    repo_rate = Fraction(45, 1000)  # 4.50% annualized repo rate
    term_days = 14  # 14-day term repo

    print("Repo Contract Parameters (SIMULATED):")
    print(f"  Collateral market value: ${collateral_value_usd:,.2f} ({collateral_cents} cents)")
    print(f"  Haircut: {float(haircut):.2%}")
    print(f"  Repo rate: {float(repo_rate):.2%} (ACT/360)")
    print(f"  Term: {term_days} days")

    # Step 1: Compute cash lent at settlement (T=0)
    cash_lent = repo_cash_lent(collateral_cents, haircut)
    haircut_buffer_cents = collateral_cents - cash_lent
    print("\nSettlement Cash Flow (T=0):")
    print(f"  Cash lent by buyer: ${cash_lent / 100:,.2f} ({cash_lent} cents)")
    print(f"  Collateral buffer: ${haircut_buffer_cents / 100:,.2f} ({haircut_buffer_cents} cents)")

    # Step 2: Compute repurchase cash due at maturity (T=14)
    cash_due = repo_cash_due(cash_lent, repo_rate, term_days)
    interest_paid = cash_due - cash_lent
    print("\nRepurchase Cash Flow (T=14):")
    print(f"  Repurchase cash due: ${cash_due / 100:,.2f} ({cash_due} cents)")
    print(f"  Total repo interest: ${interest_paid / 100:,.2f} ({interest_paid} cents)")

    # Step 3: Haircut sensitivity table
    print("\nHaircut Sensitivity Analysis on $10,000,000 Collateral:")
    for h_pct in [0, 1, 2, 5, 10]:
        h_frac = Fraction(h_pct, 100)
        lent = repo_cash_lent(collateral_cents, h_frac)
        due = repo_cash_due(lent, repo_rate, term_days)
        interest = due - lent
        print(f"  Haircut {h_pct:2d}%: Cash Lent = ${lent / 100:,.2f} | Interest = ${interest / 100:,.2f}")


main()
