"""Rung 3 check: the hand-computed fixtures and the rounding case on the project page, in exact arithmetic.

Standard library only. The values printed here are the hand-computed values stated on the project page. The autograder
checks some of them, and the note after Lab 3 on the page says which.
"""

from fractions import Fraction


def half_away(x: Fraction) -> int:
    """The nearest whole cent of an exact amount; an exact half goes away from zero."""
    magnitude = abs(x)
    whole = (2 * magnitude.numerator + magnitude.denominator) // (2 * magnitude.denominator)
    return whole if x >= 0 else -whole


def bond_events(face_cents: int, coupon_bps: int, periods: int) -> list[tuple[int, int]]:
    """Coupon in periods 1..periods, the face added in the last period."""
    coupon = half_away(Fraction(face_cents * coupon_bps, 10_000))
    rows = [(t, coupon) for t in range(1, periods + 1)]
    rows[-1] = (periods, rows[-1][1] + face_cents)
    return rows


def bond_price(events: list[tuple[int, int]], yield_bps: int) -> int:
    """Present value at a per-period yield, summed exactly and rounded once."""
    y = Fraction(yield_bps, 10_000)
    return half_away(sum((Fraction(a) / (1 + y) ** t for t, a in events), Fraction(0)))


def term_by_term_price(events: list[tuple[int, int]], yield_bps: int) -> int:
    """Each discounted term rounded to the cent before the terms are added. Not the rule; shown for contrast."""
    y = Fraction(yield_bps, 10_000)
    return sum(half_away(Fraction(a) / (1 + y) ** t) for t, a in events)


def main() -> None:
    par = bond_events(10_000, 500, 1)
    print("fixture A events (one period, par):", par)
    print("fixture A price at 500 bps (cents):", bond_price(par, 500))
    negative = bond_events(10_000, 500, 1)
    exact_negative = Fraction(10_500) / Fraction(95, 100)
    print(
        "fixture B price at -500 bps (cents):", bond_price(negative, -500), "| exact:", f"{float(exact_negative):.4f}"
    )
    half_cent = bond_events(10_001, 5_000, 2)
    print("fixture C events (half-cent coupon, two periods):", half_cent)
    one_cent = bond_events(1, 5_000, 1)
    print("fixture D events (one-cent face, half coupon):", one_cent)
    rounding = bond_events(10_000, 500, 3)
    print("rounding case events (three periods):", rounding)
    print("rounding case, rounded once (the rule):", bond_price(rounding, 400))
    print("rounding case, each term rounded first (not the rule):", term_by_term_price(rounding, 400))
    buy = (2, -10 * 9_850)
    print("fixture E trade event (buy 10 at 9850, settles in period 2):", buy)
    exact_half = bond_events(1, 0, 1)
    print("fixture F events (one cent of face, no coupon, one period):", exact_half)
    print("fixture F price at 10000 bps (cents), exact value 1/2:", bond_price(exact_half, 10_000))
    half_five_thousand = bond_events(10_001, 0, 1)
    print("fixture G events (10001 cents of face, one period):", half_five_thousand)
    print("fixture G price at 10000 bps (cents), exact value 5000.5:", bond_price(half_five_thousand, 10_000))


main()
