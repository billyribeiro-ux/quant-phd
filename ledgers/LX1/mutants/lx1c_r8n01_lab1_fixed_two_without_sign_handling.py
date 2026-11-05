"""Student drops the absolute value in the two-decimal formatter, so a negative burden change is formatted wrongly. LX1 project lab 1 (rung 1 worked example)."""

from __future__ import annotations

import math
from fractions import Fraction

NOMINAL_DEBT_CENTS = 10_000_000  # 100000.00 dollars, fixed in every period (A1)
PATHS: dict[str, tuple[Fraction, ...]] = {
    "falling": tuple(Fraction(p, 100) for p in (100, 97, 94, 91, 88, 85)),
    "rising": tuple(Fraction(p, 100) for p in (100, 103, 106, 109, 112, 115)),
}


def real_debt_cents(nominal_cents: int, price_level: Fraction) -> Fraction:
    """The real debt in cents: the nominal debt divided by the price level, which must be positive (A2)."""
    if price_level <= 0:
        raise ValueError(f"price level must be positive, got {price_level}")
    return Fraction(nominal_cents) / price_level


def burden_change_percent(start_price: Fraction, end_price: Fraction) -> Fraction:
    """The change in real debt from the start to the end of a path, in percent of the start: 100 * (start / end - 1)."""
    return 100 * (start_price / end_price - 1)


def round_half_up(value: Fraction) -> int:
    """The nearest integer to a value of either sign, a tie going away from zero."""
    magnitude = math.floor(abs(value) + Fraction(1, 2))
    return magnitude if value >= 0 else -magnitude


def fixed_two(hundredths: int) -> str:
    """An integer count of hundredths as a decimal with two places, for example -1304 as -13.04."""
    sign = "-" if hundredths < 0 else ""
    whole, part = divmod(hundredths, 100)
    return f"{sign}{whole}.{part:02d}"


def main() -> None:
    print("SIMULATED price paths, P_0 = 1.00; nominal debt 100000.00 dollars, fixed (A1)")
    for name, path in PATHS.items():
        print(f"Part A, path {name}, real debt in dollars by period:")
        for t, price in enumerate(path):
            cents = round_half_up(real_debt_cents(NOMINAL_DEBT_CENTS, price))
            print(f"  t={t} price={fixed_two(int(price * 100))} real debt={fixed_two(cents)}")
    print("Part B, burden change from t=0 to t=5, percent of the period-0 real debt:")
    for name, path in PATHS.items():
        change = burden_change_percent(path[0], path[-1])
        print(f"  path {name}: {fixed_two(round_half_up(change * 100))}")
    falling_end = real_debt_cents(NOMINAL_DEBT_CENTS, PATHS["falling"][-1])
    rising_end = real_debt_cents(NOMINAL_DEBT_CENTS, PATHS["rising"][-1])
    print("Part C, period 5, falling path minus rising path, real debt in dollars:")
    print(f"  difference: {fixed_two(round_half_up(falling_end - rising_end))}")


main()
