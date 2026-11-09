"""M5 L05 lab 1: the functions x^n on [0, 1] and on [0, 1/2], checked on exact rational grids.

Standard library only. No randomness and no network: every grid is enumerated with Fraction arithmetic, so every run
prints the same lines. A supremum over a grid is a maximum over finitely many points. A grid that contains the
endpoint of an interval gives the supremum of a monotone function exactly, because the monotone maximum sits at that
endpoint. The output is therefore exact for these functions, and it says nothing about grids that omit the endpoint.

Part A: f_n(x) = x^n on the grid k/100 for k = 0, ..., 100 (which contains 1). The sup distance from f_n to the
function 0 on [0, 1] is printed for n in (1, 2, 5, 10, 50), with the value at x = 1/2 beside it.
Part B: the same functions on [0, 1/2], on the grid k/200 for k = 0, ..., 100 (which contains 1/2). The sup distance
is printed for the same n, with a check that it equals (1/2)^n, and the least n with (1/2)^n below 1/1000.
Part C: the values of f_n at x = 0.99 are printed for n = 10, 100, 1000 as floats, and a check prints True
when f_n(1) = 1 for n = 1, 10, 100 and 1000. The pointwise limit is not computed by the program; the page states it.
"""

from __future__ import annotations

from fractions import Fraction

ORDERS = (1, 2, 5, 10, 50)
HALF = Fraction(1, 2)


def grid(right: Fraction, steps: int) -> list[Fraction]:
    """The points k * right / steps for k = 0, ..., steps, all exact. The last point is right."""
    return [right * Fraction(k, steps) for k in range(steps + 1)]


def power(x: Fraction, n: int) -> Fraction:
    """The exact value x^n for a whole number n >= 1."""
    return x**n


def sup_on_grid(values: list[Fraction]) -> Fraction:
    """The largest of the sampled values, exact. The list is nonempty."""
    return max(values)


def least_order_below(bound: Fraction, base: Fraction) -> int:
    """The least n >= 1 with base^n < bound, for 0 < base < 1 and bound > 0."""
    n = 1
    while base**n >= bound:
        n += 1
    return n


def main() -> None:
    """Print Parts A, B and C. Every value is an exact fraction, an integer, a boolean, or a float with ten decimals."""
    print("Part A: sup distance from x^n to 0 on [0, 1], grid k/100")
    unit = grid(Fraction(1), 100)
    for n in ORDERS:
        sup = sup_on_grid([power(x, n) for x in unit])
        print(f"order {n} sup_distance {sup} value_at_half {power(HALF, n)}")

    print("Part B: sup distance from x^n to 0 on [0, 1/2], grid k/200, with the check (1/2)^n")
    half_grid = grid(HALF, 100)
    for n in ORDERS:
        sup = sup_on_grid([power(x, n) for x in half_grid])
        print(f"order {n} sup_distance {sup} equals_half_power {sup == power(HALF, n)}")
    threshold = Fraction(1, 1000)
    print(f"least_order_with_half_power_below_1_over_1000 {least_order_below(threshold, HALF)}")

    print("Part C: pointwise limit of x^n on [0, 1] is 0 on [0, 1) and 1 at 1")
    for n in (10, 100, 1000):
        print(f"order {n} value_at_0_99 {float(power(Fraction(99, 100), n)):.10f}")
    print(f"value_at_one_for_every_order {all(power(Fraction(1), n) == 1 for n in (1, 10, 100, 1000))}")


main()
