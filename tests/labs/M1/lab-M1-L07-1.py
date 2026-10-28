"""M1 L07 lab 1: annuity closed form against direct summation, and the growing-perpetuity limit case.

Amounts are in currency units (CU). Payments fall at the end of each period, r is the rate per period,
and v = 1 / (1 + r) is the discount factor. Part A uses exact rational arithmetic (fractions.Fraction).
Part B uses floats and prints partial sums for several horizons N, next to the closed form and the
remainder formula of Proposition 3.2. Part C shows the case g = r, where the partial sums are unbounded and
the closed form must be refused. Standard library only; no randomness and no network access.
"""

from __future__ import annotations

import math
from fractions import Fraction

RATES: tuple[Fraction, ...] = (Fraction(1, 20), Fraction(3, 100), Fraction(1, 10), Fraction(1, 3))
N_MAX = 40
PAYMENT = Fraction(100)


def annuity_closed(c: Fraction, r: Fraction, n: int) -> Fraction:
    """PV of n payments of c at ends of periods 1..n. Requires r > 0; the r = 0 case is n * c."""
    if r <= 0:
        raise ValueError("this closed form needs r > 0; at r = 0 the value is n * c")
    v = 1 / (1 + r)
    return c * (1 - v**n) / r


def annuity_direct(c: Fraction, r: Fraction, n: int) -> Fraction:
    """PV of n payments of c at ends of periods 1..n, by adding the discounted payments."""
    total = Fraction(0)
    for t in range(1, n + 1):
        total += c / (1 + r) ** t
    return total


def annuity_due_direct(c: Fraction, r: Fraction, n: int) -> Fraction:
    """PV of n payments of c at the start of periods 1..n, that is at times 0..n-1."""
    total = Fraction(0)
    for t in range(0, n):
        total += c / (1 + r) ** t
    return total


def growing_pv_partial(c: float, r: float, g: float, n: int) -> float:
    """PV of the first n payments of c * (1 + g)**(t - 1) at times t = 1..n."""
    return sum(c * (1 + g) ** (t - 1) / (1 + r) ** t for t in range(1, n + 1))


def growing_perpetuity_value(c: float, r: float, g: float) -> float:
    """Value C / (r - g) of a growing perpetuity. Refuses inputs outside the domain -1 < g < r, r > 0."""
    if r <= 0:
        raise ValueError("a perpetuity needs a positive discount rate r")
    if g <= -1:
        raise ValueError("a growing perpetuity needs g > -1 so that its payments stay positive")
    if not r > g:
        raise ValueError("a growing perpetuity needs r > g; when g >= r its partial values grow without bound")
    return c / (r - g)


def part_a() -> None:
    checks = 0
    for r in RATES:
        for n in range(1, N_MAX + 1):
            direct = annuity_direct(PAYMENT, r, n)
            if direct != annuity_closed(PAYMENT, r, n):
                raise AssertionError(f"annuity closed form fails at r = {r}, n = {n}")
            due = annuity_due_direct(PAYMENT, r, n)
            if due != (1 + r) * direct:
                raise AssertionError(f"annuity-due relation fails at r = {r}, n = {n}")
            checks += 2
    print(f"part A: exact checks passed: {checks} (r takes {len(RATES)} values, n = 1 to {N_MAX})")
    r, n = Fraction(1, 10), 3
    ordinary = annuity_direct(PAYMENT, r, n)
    due = annuity_due_direct(PAYMENT, r, n)
    print(f"part A example, c = 100, r = 1/10, n = 3: ordinary PV = {float(ordinary):.4f}, due PV = {float(due):.4f}")
    print(f"part A example, due / ordinary = {float(due / ordinary):.1f} (equals 1 + r = {float(1 + r):.1f})")


def part_b() -> None:
    c, r, g = 100.0, 0.08, 0.03
    closed = growing_perpetuity_value(c, r, g)
    q = (1 + g) / (1 + r)
    print(f"part B: c = {c:g}, r = {r:g}, g = {g:g}, q = (1 + g)/(1 + r) = {q:.6f}")
    print(f"part B: closed form C/(r - g) = {closed:.1f}")
    for n in (1, 5, 10, 50, 100, 200, 400):  # float sums: abs_tol covers the last digits at N = 400
        partial = growing_pv_partial(c, r, g, n)
        remainder = closed - partial
        predicted = closed * q**n
        if not math.isclose(remainder, predicted, rel_tol=1e-9, abs_tol=1e-9):
            raise AssertionError(f"remainder formula fails at n = {n}")
        print(f"part B: N = {n:3d}  PV of first N = {partial:10.4f}  remainder to closed form = {remainder:10.4f}")
    print("part B: the remainder equals (C / (r - g)) * q**N at every horizon listed")


def part_c() -> None:
    c, r = 100.0, 0.08
    g = r
    for n in (10, 100):
        partial = growing_pv_partial(c, r, g, n)
        if not math.isclose(partial, n * c / (1 + r), rel_tol=1e-12):
            raise AssertionError(f"g = r partial sums differ from N * C / (1 + r) at N = {n}")
        print(f"part C: g = r = {g:g}, N = {n:3d}  PV of first N = {partial:10.4f} (equals N * C / (1 + r))")
    try:
        growing_perpetuity_value(c, r, g)
    except ValueError as exc:
        print(f"part C: the closed form is refused: {exc}")


def main() -> None:
    part_a()
    part_b()
    part_c()


main()
