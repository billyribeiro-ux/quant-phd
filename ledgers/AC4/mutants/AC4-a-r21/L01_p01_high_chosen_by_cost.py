"""AC4 lab L01: fit a mixed cost with the high-low method on a SIMULATED monthly history.

SIMULATED: the twelve months, the machine hours and the costs are generated from a seeded
random number generator. They are not any firm's figures. Money is integer cents. The fitted
parameters are exact rationals (fractions.Fraction); a value is converted to the nearest cent
only when it is printed. Standard library only; no network; every number printed is computed here.
"""

from __future__ import annotations

import random
from fractions import Fraction

SEED = 20261027
MONTHS = 12
GEN_FIXED_CENTS = 1_800_000  # generator's fixed part, 18000.00 USD a month; printed only for comparison
GEN_VARIABLE_CENTS = 4_250  # generator's variable rate, 42.50 USD an hour; printed only for comparison
NOISE_CENTS = 40_000  # the noise is uniform on [-40000, 40000] cents, 400.00 USD either way


def simulate(seed: int, months: int) -> list[tuple[int, int]]:
    """Return (machine_hours, total_cost_cents) per month, from a seeded generator.

    Hours are integers in [400, 1200]. Cost is GEN_FIXED + GEN_VARIABLE * hours + noise, in integer cents.
    """
    rng = random.Random(seed)
    rows: list[tuple[int, int]] = []
    for _ in range(months):
        hours = rng.randint(400, 1200)
        noise = rng.randint(-NOISE_CENTS, NOISE_CENTS)
        rows.append((hours, GEN_FIXED_CENTS + GEN_VARIABLE_CENTS * hours + noise))
    return rows


def cents(x: Fraction) -> int:
    """Nearest integer number of cents; a half goes up. Exact on a Fraction."""
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


def high_low(rows: list[tuple[int, int]]) -> tuple[Fraction, Fraction]:
    """Fit cost = fixed + variable * hours through the highest- and lowest-activity months.

    Returns (fixed_cents, variable_cents_per_hour) as exact Fractions. A tie on activity takes the
    earliest month. Raises ValueError when there are fewer than two months, or when the highest and
    lowest activity are equal, because the slope is then undefined.
    """
    if len(rows) < 2:
        raise ValueError("high-low needs at least two months of data")
    high = max(range(len(rows)), key=lambda i: (rows[i][1], -i))
    low = min(range(len(rows)), key=lambda i: (rows[i][0], i))
    high_hours, high_cost = rows[high]
    low_hours, low_cost = rows[low]
    if high_hours == low_hours:
        raise ValueError("high-low needs different highest and lowest activity; the slope is undefined")
    variable = Fraction(high_cost - low_cost, high_hours - low_hours)
    fixed = Fraction(high_cost) - variable * high_hours
    return fixed, variable


def main() -> None:
    """Fit the history, print the parameters, the residual of each month, and the loud failures."""
    rows = simulate(SEED, MONTHS)
    fixed, variable = high_low(rows)
    print(f"seed {SEED} months {len(rows)}")
    print(f"generator fixed_cents {GEN_FIXED_CENTS} variable_cents_per_hour {GEN_VARIABLE_CENTS}")
    print(f"high-low fixed_cents {cents(fixed)} variable_cents_per_hour {float(variable):.2f}")
    residuals: list[int] = []
    for month, (hours, cost) in enumerate(rows, start=1):
        residual = Fraction(cost) - (fixed + variable * hours)
        residuals.append(cents(residual))
        print(f"month {month:2d} hours {hours:5d} cost_cents {cost:9d} residual_cents {cents(residual):7d}")
    high_hours = max(hours for hours, _ in rows)
    low_hours = min(hours for hours, _ in rows)
    on_line = [m for m, (h, _) in enumerate(rows, start=1) if h in (high_hours, low_hours)]
    print(f"months on the fitted line exactly {on_line}")
    print(f"largest absolute residual_cents {max(abs(r) for r in residuals)}")
    print(f"months with nonzero residual {sum(1 for r in residuals if r != 0)} of {len(rows)}")
    for label, data in (("one month", rows[:1]), ("equal activity", [(500, 100), (500, 200)])):
        try:
            high_low(data)
        except ValueError as exc:
            print(f"ValueError for {label}: {exc}")
        else:
            print(f"no error for {label}")


main()
