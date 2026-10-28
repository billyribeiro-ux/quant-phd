"""M1 L06 lab 1: the geometric-sum identity, checked in exact arithmetic for n = 1 to 60.

Claim checked: for every rational q with q != 1 and every integer n >= 1,
    sum_{k=0}^{n-1} q**k  ==  (1 - q**n) / (1 - q).
Both sides are Fraction values, so the comparison is exact and no approximation enters.
A second part shows that the same closed form computed in floating point loses digits when q is
close to 1. Standard library only. No randomness and no network access.
"""

from __future__ import annotations

from fractions import Fraction

QS: tuple[Fraction, ...] = (
    Fraction(1, 2),
    Fraction(2, 3),
    Fraction(-3, 2),
    Fraction(7, 5),
    Fraction(-1, 3),
    Fraction(0),
    Fraction(1, 1000),
)
N_MAX = 60


def direct_sum(q: Fraction, n: int) -> Fraction:
    """Return sum_{k=0}^{n-1} q**k, adding the terms one at a time."""
    total = Fraction(0)
    for k in range(n):
        total += q**k
    return total


def closed_form(q: Fraction, n: int) -> Fraction:
    """Return (1 - q**n) / (1 - q). Requires q != 1."""
    if q == 1:
        raise ValueError("the closed form needs q != 1")
    return (1 - q**n) / (1 - q)


def float_relative_error(q_float: float, n: int) -> float:
    """Relative error of the floating-point closed form, against the exact value at the same float q."""
    exact = closed_form(Fraction(q_float), n)  # Fraction(q_float) is the float's exact value
    approx = (1.0 - q_float**n) / (1.0 - q_float)
    return abs(approx - float(exact)) / float(exact)


def main() -> None:
    checks = 0
    for q in QS:
        for n in range(1, N_MAX + 1):
            if direct_sum(q, n) != closed_form(q, n):
                raise AssertionError(f"identity fails at q = {q}, n = {n}")
            checks += 1
    print(f"exact checks passed: {checks} (q takes {len(QS)} values, n = 1 to {N_MAX})")

    for n in range(1, N_MAX + 1):
        if direct_sum(Fraction(1), n) != n:
            raise AssertionError(f"the q = 1 sum should equal n, failed at n = {n}")
    print(f"q = 1: the sum equals n for n = 1 to {N_MAX} (checked exactly)")

    q, n = Fraction(1, 2), 3
    print(f"q = 1/2, n = 3: direct sum = {direct_sum(q, n)}, closed form = {closed_form(q, n)}")
    q, n = Fraction(-1), 10
    print(f"q = -1, n = 10: direct sum = {direct_sum(q, n)}, closed form = {closed_form(q, n)}")

    for q_float in (1.001, 1.0 + 1e-9):
        error = float_relative_error(q_float, 60)
        print(f"floating-point closed form at q = {q_float!r}, n = 60: relative error {error:.3e}")


main()
