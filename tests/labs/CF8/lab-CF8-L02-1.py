"""CF8 lab L02: early-payment discounts, credit-term break-evens and supply-chain financing, on SIMULATED terms.

SIMULATED: every term, balance, margin and rate below is an invented input for this lab. No company, supplier or
financier is real, and the lab reads no data file and makes no network request. Money is in dollars, not cents:
Part B uses exact dollar Fractions, and each printed dollar amount is rounded half up to the cent for display only.
The break-even margin and the NPV checks use fractions.Fraction and are exact. The compounded implied cost in Part A
is computed in floating point and printed to two decimals. Part D draws its cases from a seeded random number
generator. Standard library only.
"""

from __future__ import annotations

import random
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction

DAYS_PER_YEAR = 365
SEED = 20261029
RATE = Fraction(1, 10)


def pct_text(value: Fraction) -> str:
    """A rate as a percentage rounded half up to two decimals, for display only."""
    quotient = Decimal(value.numerator) * 100 / Decimal(value.denominator)
    return str(quotient.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)) + "%"


def dollars_text(value: Fraction) -> str:
    """A dollar amount shown to two decimals, rounded half up for display only; the exact value is kept elsewhere."""
    quotient = Decimal(value.numerator) / Decimal(value.denominator)
    return str(quotient.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def implied_simple_cost(discount: Fraction, days_early: int, days_late: int) -> Fraction:
    """Annual simple cost of giving up a discount d for paying N - k days later: d/(1-d) times 365/(N-k)."""
    if days_late <= days_early:
        raise ValueError("the full payment must fall after the discount date")
    return discount / (1 - discount) * Fraction(DAYS_PER_YEAR, days_late - days_early)


def implied_compound_cost(discount: Fraction, days_early: int, days_late: int) -> float:
    """Annual compounded cost in floating point: (1/(1-d)) raised to 365/(N-k), minus one."""
    factor = float(1 / (1 - discount))
    power = float(factor ** (DAYS_PER_YEAR / (days_late - days_early)))
    return power - 1.0


def npv_extension(margin: Fraction, extra_margin_base: Fraction, extra_invest: Fraction, years: int) -> Fraction:
    """NPV at RATE of an extension: pay the investment now, earn margin times the extra revenue each year, get the
    investment back at year n. The extra revenue is extra_margin_base; the investment is extra_invest."""
    annuity = sum((1 / (1 + RATE)) ** t for t in range(1, years + 1))
    return -extra_invest + margin * extra_margin_base * annuity + extra_invest / (1 + RATE) ** years


def break_even_margin(extra_revenue: Fraction, extra_invest: Fraction) -> Fraction:
    """Break-even margin m* = r times the investment over the extra revenue (the closed form of Section 3)."""
    return RATE * extra_invest / extra_revenue


def extension_investment(revenue: Fraction, days_old: int, days_new: int, extra_revenue: Fraction) -> Fraction:
    """Extra receivables from the new terms: (revenue + extra revenue) times the new days, less the old balance."""
    new_balance = (revenue + extra_revenue) * days_new / DAYS_PER_YEAR
    old_balance = revenue * days_old / DAYS_PER_YEAR
    return new_balance - old_balance


def main() -> None:
    print("A. Early-payment terms: implied annual cost of giving up the discount (SIMULATED terms)")
    terms = [
        ("2/10 net 30", Fraction(2, 100), 10, 30),
        ("1/10 net 30", Fraction(1, 100), 10, 30),
        ("2/10 net 60", Fraction(2, 100), 10, 60),
        ("3/15 net 45", Fraction(3, 100), 15, 45),
    ]
    for label, discount, early, late in terms:
        simple = implied_simple_cost(discount, early, late)
        compound = implied_compound_cost(discount, early, late)
        print(
            f"{label}: discount {pct_text(discount)}, days paid early {early}, days paid late {late}, "
            f"simple annual cost {pct_text(simple)}, compounded annual cost {compound * 100:.2f}%"
        )
    supplier_discount = Fraction(5, 1000)
    financed = implied_simple_cost(supplier_discount, 10, 60)
    print(
        f"financed payment (SIMULATED): discount {pct_text(supplier_discount)} for paying 50 days early, "
        f"simple annual cost {pct_text(financed)}"
    )

    print()
    print("B. Credit-term extension: break-even margin m*, equal to r times the investment over the extra revenue")
    revenue = Fraction(12_000_000)
    days_old, days_new = 30, 45
    extra_revenue = Fraction(1_500_000)
    years = 5
    invest = extension_investment(revenue, days_old, days_new, extra_revenue)
    print(f"revenue before the extension, in dollars: {dollars_text(revenue)}")
    print(f"extra revenue from the extension, in dollars: {dollars_text(extra_revenue)}")
    print(f"investment in receivables, in dollars, to the cent: {dollars_text(invest)}")
    m_star = break_even_margin(extra_revenue, invest)
    print(f"break-even margin m*, as a share of extra revenue: {pct_text(m_star)}")
    print(f"NPV at m* over {years} years, exact value: {npv_extension(m_star, extra_revenue, invest, years)}")
    below = npv_extension(m_star - Fraction(1, 100), extra_revenue, invest, years)
    above = npv_extension(m_star + Fraction(1, 100), extra_revenue, invest, years)
    print(f"NPV at m* minus one point is negative: {below < 0}")
    print(f"NPV at m* plus one point is positive: {above > 0}")
    print(
        "NPV at a 5 percent margin, in dollars: "
        + dollars_text(npv_extension(Fraction(5, 100), extra_revenue, invest, years))
    )
    same = all(
        npv_extension(break_even_margin(extra_revenue, invest), extra_revenue, invest, n) == 0 for n in range(1, 11)
    )
    print(f"m* gives an NPV of exactly zero for every horizon from 1 to 10 years: {same}")

    print()
    print("C. Closed form check")
    closed_form = RATE * invest / extra_revenue
    print(f"closed form r times investment over extra revenue equals m*: {closed_form == m_star}")

    print()
    print("D. Two hundred seeded SIMULATED extensions: the exact break-even is a zero of the NPV")
    rng = random.Random(SEED)
    zeros = 0
    accepted_at_ten = 0
    for _ in range(200):
        base = Fraction(rng.randint(2_000_000, 40_000_000))
        old_days = rng.randint(20, 40)
        new_days = old_days + rng.randint(5, 30)
        extra = Fraction(rng.randint(100_000, 5_000_000))
        term = rng.randint(1, 8)
        inv = extension_investment(base, old_days, new_days, extra)
        m = break_even_margin(extra, inv)
        zeros += npv_extension(m, extra, inv, term) == 0
        accepted_at_ten += m < Fraction(10, 100)
    print(f"cases whose NPV at m* is exactly zero, out of 200: {zeros}")
    print(f"cases whose break-even margin is below ten percent, out of 200: {accepted_at_ten}")


main()
