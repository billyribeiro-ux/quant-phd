"""Student floors the real value to the cent instead of rounding it half up, so 41666.666... prints 41666.66. LX1 project lab 2 (rung 2, completion problem): the real burden of a fixed nominal debt on a price path."""


from __future__ import annotations

import math
from fractions import Fraction

NOMINAL_DEBT_CENTS = 4_000_000  # 40000.00 dollars, fixed in every period (A1)
PATH: tuple[Fraction, ...] = tuple(Fraction(p, 100) for p in (100, 99, 98, 96, 95, 93))


def real_debt_cents(nominal_cents: int, price_level: Fraction) -> Fraction:
    """The real debt in cents: the nominal debt divided by the price level, which must be positive (A2)."""
    if price_level <= 0:
        raise ValueError(f"price level must be positive, got {price_level}")
    return Fraction(nominal_cents) / price_level


def burden_change_percent(start_price: Fraction, end_price: Fraction) -> Fraction:
    """The change in real debt from the start to the end of a path, in percent of the start."""
    return 100 * (start_price / end_price - 1)


def round_half_up(value: Fraction) -> int:
    """The nearest integer to a value of either sign, a tie going away from zero."""
    magnitude = math.floor(abs(value) + Fraction(1, 2))
    return magnitude if value >= 0 else -magnitude


def fixed_two(hundredths: int) -> str:
    """An integer count of hundredths as a decimal with two places, for example -1304 as -13.04."""
    sign = "-" if hundredths < 0 else ""
    whole, part = divmod(abs(hundredths), 100)
    return f"{sign}{whole}.{part:02d}"


def main() -> None:
    print("SIMULATED price path, P_0 = 1.00; nominal debt 40000.00 dollars, fixed (A1)")
    print("Part A, real debt in dollars by period:")
    for t, price in enumerate(PATH):
        cents = math.floor(real_debt_cents(NOMINAL_DEBT_CENTS, price))
        print(f"  t={t} price={fixed_two(int(price * 100))} real debt={fixed_two(cents)}")
    change = burden_change_percent(PATH[0], PATH[-1])
    print("Part B, burden change from t=0 to t=5, percent of the period-0 real debt:")
    print(f"  change: {fixed_two(round_half_up(change * 100))}")


main()
