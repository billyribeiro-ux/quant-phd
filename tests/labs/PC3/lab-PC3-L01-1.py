"""PC3 lab L01: bounds on a Fermi product, its log-error width, and a second-order bound for (1 + x)^n.

Standard library only. No randomness and no network. Every factor range below is an assumed range chosen for
this example. It is not an estimate of any market, and the lab reads no data file. Bounds and products are
fractions.Fraction, so every printed bound and every checked inequality is exact. Decimal columns print to ten
places and are used only for the log-error widths and for the displayed values of the Taylor bound.

The product bounds rest on the monotonicity argument of Theorem 1.2 on the page. The lab checks that every
product over a regular grid of factor values lies inside them. A finite grid is a check, not a proof.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

Factor = tuple[str, Fraction, Fraction]

# Assumed ranges (lower end, upper end) for this example. They are not estimates of any market.
FACTORS: tuple[Factor, ...] = (
    ("symbols quoted", Fraction(20), Fraction(60)),
    ("quote updates per symbol per minute", Fraction(2), Fraction(10)),
    ("minutes of quoting per day", Fraction(300), Fraction(390)),
)

# Narrowed ranges, one factor at a time, for Part 2.
NARROWED: dict[str, tuple[Fraction, Fraction]] = {
    "symbols quoted": (Fraction(20), Fraction(40)),
    "quote updates per symbol per minute": (Fraction(4), Fraction(8)),
    "minutes of quoting per day": (Fraction(330), Fraction(360)),
}

GRID_POINTS = 5


def product_bounds(factors: tuple[Factor, ...]) -> tuple[Fraction, Fraction]:
    """Lower and upper bounds of the product of the factor ranges. Every lower end must be positive."""
    lower = Fraction(1)
    upper = Fraction(1)
    for name, lo, hi in factors:
        if lo <= 0 or hi < lo:
            raise ValueError(f"factor {name!r} needs 0 < lower end <= upper end")
        lower *= lo
        upper *= hi
    return lower, upper


def log_width(lower: Fraction, upper: Fraction) -> float:
    """The log-error width ln(upper / lower) of an interval with positive ends, in natural-log units."""
    return math.log(float(upper / lower))


def grid_products(factors: tuple[Factor, ...]) -> list[Fraction]:
    """Products over a regular grid of GRID_POINTS values in each range, both ends included."""
    axes = [[lo + (hi - lo) * Fraction(k, GRID_POINTS - 1) for k in range(GRID_POINTS)] for _, lo, hi in factors]
    products: list[Fraction] = []
    for combo in itertools.product(*axes):
        value = Fraction(1)
        for x in combo:
            value *= x
        products.append(value)
    return products


def remainder(n: int, x: Fraction) -> Fraction:
    """(1 + x)^n - 1 - n x: the part of the expansion of (1 + x)^n after its first-order term."""
    return (1 + x) ** n - 1 - n * x


def binomial_tail(n: int, x: Fraction) -> Fraction:
    """The sum of C(n, j) x^j for j from 2 to n, computed term by term."""
    return sum((math.comb(n, j) * x**j for j in range(2, n + 1)), Fraction(0))


def lagrange_bound(n: int, x: Fraction) -> Fraction:
    """n(n - 1)/2 times (1 + x)^(n - 2) times x^2, the bound on the remainder for 0 <= x."""
    return Fraction(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x


def part_one() -> None:
    print("Part 1 · product of assumed factor ranges")
    lower, upper = product_bounds(FACTORS)
    print(f"product lower bound = {int(lower)}")
    print(f"product upper bound = {int(upper)}")
    print(f"upper / lower = {float(upper / lower):.10f}")
    width = log_width(lower, upper)
    print(f"log-error width ln(upper / lower) = {width:.10f}")
    print(f"geometric midpoint sqrt(lower * upper) = {math.sqrt(float(lower * upper)):.10f}")
    parts = [log_width(lo, hi) for _, lo, hi in FACTORS]
    for (name, lo, hi), part in zip(FACTORS, parts, strict=True):
        print(f"  factor log-width, {name} ({lo} to {hi}) = {part:.10f}")
    print(f"sum of factor log-widths = {sum(parts):.10f}")
    print(f"sum equals product log-width: {abs(sum(parts) - width) < 1e-12}")
    grid = grid_products(FACTORS)
    inside = sum(lower <= p <= upper for p in grid)
    print(f"grid products inside the bounds: {inside} of {len(grid)}")


def part_two() -> None:
    print("Part 2 · narrowing one factor at a time (total log-error width)")
    base = log_width(*product_bounds(FACTORS))
    print(f"baseline total log-error width = {base:.10f}")
    for name, lo_hi in NARROWED.items():
        changed = tuple((n, lo_hi[0], lo_hi[1]) if n == name else (n, lo, hi) for n, lo, hi in FACTORS)
        total = log_width(*product_bounds(changed))
        print(f"narrow {name} to {lo_hi[0]} to {lo_hi[1]}: total {total:.10f}, reduction {base - total:.10f}")


def part_three() -> None:
    print("Part 3 · second-order remainder of (1 + x)^n for 0 <= x")
    ok_bound = True
    ok_tail = True
    for n in (2, 5, 10):
        for x in (Fraction(1, 100), Fraction(1, 20)):
            exact = (1 + x) ** n
            rem = remainder(n, x)
            bound = lagrange_bound(n, x)
            ok_bound = ok_bound and 0 <= rem <= bound
            ok_tail = ok_tail and rem == binomial_tail(n, x)
            print(
                f"n={n} x={float(x):.2f}: first-order 1 + n x = {float(1 + n * x):.10f}, "
                f"exact = {float(exact):.10f}, remainder = {float(rem):.10f}, bound = {float(bound):.10f}"
            )
    print(f"0 <= remainder <= bound in every case: {ok_bound}")
    print(f"remainder equals the binomial tail in every case: {ok_tail}")


def main() -> None:
    part_one()
    part_two()
    part_three()


main()
