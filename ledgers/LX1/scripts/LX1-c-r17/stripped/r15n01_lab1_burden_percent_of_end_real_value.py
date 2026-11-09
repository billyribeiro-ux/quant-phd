"""LX1 project lab 1 (rung 1). Student error: the burden change is taken as a percent of the period-5 real value, not of the period-0 real value.
LX1 project lab 1 (rung 1, worked example): the real burden of a fixed nominal debt on two price paths.

SIMULATED. Both price paths are illustrative values written into this file. They are not data, and no random draws
are used, so every run prints the same lines.

Assumptions. A1: the nominal debt is fixed at 10,000,000 cents (100000.00 dollars) in every period. A2: the price
level P_t is a positive ratio with P_0 = 1, so the real debt in period t is the nominal debt divided by P_t.

Part A: the real debt of each period of each path, in dollars to the cent.
Part B: the burden change of each path from period 0 to period 5, in percent of the period-0 real debt. It is
100 * (P_0 / P_5 - 1), a ratio of price levels, so no real debt has to be rounded before it is computed.
Part C: one comparison, the period-5 real debt of the falling path minus that of the rising path, in dollars.

Every value is an exact Fraction. A value is rounded once, when it is printed: half up (a tie goes away from zero),
to the whole cent for dollar amounts and to two decimals for percentages.
"""

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
    whole, part = divmod(abs(hundredths), 100)
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
        change = 100 * (real_debt_cents(NOMINAL_DEBT_CENTS, path[0]) - real_debt_cents(NOMINAL_DEBT_CENTS, path[-1])) / real_debt_cents(NOMINAL_DEBT_CENTS, path[-1])
        print(f"  path {name}: {fixed_two(round_half_up(change * 100))}")
    falling_end = real_debt_cents(NOMINAL_DEBT_CENTS, PATHS["falling"][-1])
    rising_end = real_debt_cents(NOMINAL_DEBT_CENTS, PATHS["rising"][-1])
    print("Part C, period 5, falling path minus rising path, real debt in dollars:")
    print(f"  difference: {fixed_two(round_half_up(falling_end - rising_end))}")


main()
