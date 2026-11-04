"""PC3 lab L06: one forward-price check and one case cash-flow calculation, in exact fractions.

Every input is an assumption made for this example. None is a market quote, a market rate or a company's figure, and the
lab reads no data file. Standard library only, with no randomness and no network access.

Money is an integer number of cents. Every value is held as a fractions.Fraction, so every identity is exact. Display
is the only place a value is changed: a displayed value is the exact value taken half up, toward plus infinity, to the
stated number of decimal places, applied once to the exact value.

Part 1 is a forward-price check. A discount factor D = 97/100 for the expiry is an input, with D = exp(-r tau) in the
convention of the lesson. The no-arbitrage forward price is F = S / D. The portfolio of a long asset, a loan of S repaid
as S / D, and a short forward at a quoted price F' pays F' - S / D at expiry in every spot state.

Part 2 is a case. A machine costs 150000 USD. It earns a contribution of 50 USD per unit sold for three years, and
units per year are sized by a Fermi product of three assumed factor ranges. The net present value is the sum of
C_t / (1 + r)^t at the stated rate, with the outlay at t = 0.
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Sequence
from fractions import Fraction

SPOT_CENTS = 9_700  # spot price today, 97.00 USD
DISCOUNT = Fraction(97, 100)  # assumed discount factor for the expiry
QUOTED_CENTS = 10_100  # a forward quoted above the no-arbitrage price

OUTLAY_CENTS = 15_000_000  # 150000 USD at t = 0
MARGIN_CENTS = 5_000  # contribution per unit: 50 USD
YEARS = 3
RATE = Fraction(10, 100)  # assumed rate for the case


def half_up(x: Fraction, places: int) -> str:
    """The exact value x shown to the given number of decimal places, taken half up once, toward plus infinity."""
    scale = 10**places
    n = math.floor(x * scale + Fraction(1, 2))
    sign = "-" if n < 0 else ""
    n = abs(n)
    if places == 0:
        return f"{sign}{n}"
    whole, frac = divmod(n, scale)
    return f"{sign}{whole}.{frac:0{places}d}"


def npv(cash_flows: Sequence[Fraction], rate: Fraction) -> Fraction:
    """Net present value: the sum over t of C_t / (1 + rate)^t, with cash_flows[0] at t = 0. Exact."""
    return sum((c / (1 + rate) ** t for t, c in enumerate(cash_flows)), Fraction(0))


def part_one() -> None:
    print("Part 1 · forward price check, cents, discount factor 97/100 (assumed)")
    spot = Fraction(SPOT_CENTS)
    no_arb = spot / DISCOUNT
    print(f"no-arbitrage forward price F = S / D = {no_arb} cents")
    print(f"value at inception of a forward struck at F, S - D F = {spot - DISCOUNT * no_arb} cents")
    for label, quoted in (("no-arbitrage price", no_arb), ("quoted above it", Fraction(QUOTED_CENTS))):
        payoffs: list[Fraction] = []
        for spot_t in (8_000, 9_000, 10_000, 11_000, 12_000):
            asset = Fraction(spot_t)  # the long asset, worth S_T at expiry
            forward = quoted - Fraction(spot_t)  # short forward: receive F, deliver the asset worth S_T
            loan = -spot / DISCOUNT  # the loan of S today is repaid as S / D
            payoffs.append(asset + forward + loan)
        constant = len(set(payoffs)) == 1
        print(f"{label}, F = {quoted}: payoff at expiry for S_T = 8000..12000 is {[str(p) for p in payoffs]}")
        equals_formula = payoffs[0] == quoted - spot / DISCOUNT
        print(f"  payoff the same in every spot state: {constant}; equals F - S / D: {equals_formula}")
    initial = -spot + spot  # buy the asset for S, lend nothing; borrow S today
    print(f"initial outlay of the portfolio: -S for the asset plus S from the loan = {initial} cents")


def fermi_units() -> tuple[Fraction, Fraction]:
    """Lower and upper bounds on units per year, as the product of customers, orders per customer and share."""
    customers = (Fraction(2_000), Fraction(4_000))
    orders = (Fraction(1), Fraction(2))
    share = (Fraction(1, 10), Fraction(1, 5))
    lower = customers[0] * orders[0] * share[0]
    upper = customers[1] * orders[1] * share[1]
    return lower, upper


def cash_flows(units: Fraction) -> list[Fraction]:
    """C_0 = -outlay, and C_1 = C_2 = C_3 = units x margin, all in cents."""
    return [Fraction(-OUTLAY_CENTS)] + [units * MARGIN_CENTS] * YEARS


def part_two() -> None:
    print("Part 2 · case: machine cost 150000 USD, margin 50 USD per unit, 3 years, rate 10% (assumed)")
    lower, upper = fermi_units()
    print(f"Fermi bounds on units per year: lower {lower}, upper {upper}")
    annuity = sum((1 / (1 + RATE) ** t for t in range(1, YEARS + 1)), Fraction(0))
    print(f"annuity factor sum of (1 + r)^-t for t = 1..3 = {annuity}")
    break_even = Fraction(OUTLAY_CENTS, MARGIN_CENTS) / annuity
    print(f"break-even units per year = {break_even} = {half_up(break_even, 2)} to two decimals")
    npv_break_even = npv(cash_flows(break_even), RATE)
    print(f"NPV at the break-even units is exactly zero: {npv_break_even == 0}")
    grid = [Fraction(u) for u in range(200, 1601, 100)]
    values = [npv(cash_flows(u), RATE) for u in grid]
    increasing = all(a < b for a, b in itertools.pairwise(values))
    print(f"NPV increases with units on the grid 200 to 1600 in steps of 100: {increasing}")
    lower_npv = npv(cash_flows(lower), RATE)
    print(f"NPV at the lower bound = {half_up(lower_npv, 0)} cents (exact {lower_npv})")
    print(f"NPV at the upper bound = {half_up(npv(cash_flows(upper), RATE), 0)} cents")
    print(f"the Fermi range contains the break-even: {lower <= break_even <= upper}")
    print("sensitivity to the rate, cents, displayed to the whole cent:")
    for rate in (Fraction(8, 100), Fraction(10, 100), Fraction(12, 100)):
        low_npv = npv(cash_flows(lower), rate)
        high_npv = npv(cash_flows(upper), rate)
        be = Fraction(OUTLAY_CENTS, MARGIN_CENTS) / sum((1 / (1 + rate) ** t for t in range(1, YEARS + 1)), Fraction(0))
        print(
            f"  rate {half_up(rate * 100, 0)}%: NPV at lower {half_up(low_npv, 0)}, at upper {half_up(high_npv, 0)}, "
            f"break-even units {half_up(be, 2)}"
        )


def main() -> None:
    part_one()
    part_two()


main()
