"""M5 lab L01: bisection brackets the supremum of S = {x >= 0 : x * x < 2}, with exact brackets.

Standard library only. No randomness and no network. Every bracket is a rational number held as a
fractions.Fraction, so each printed inequality and each printed width is exact. The lab uses two
tests on the midpoint m >= 0: m is in S when m * m < 2, and m is an upper bound of S when m * m >= 2
(Lemma 1.5 of the page proves that these two cases cover every m >= 0). The lab brackets the
supremum by exact rational numbers. It does not compute the supremum as a decimal, and a finite
run of bisection is evidence about where the supremum lies, not a proof of its value.
"""

from __future__ import annotations

from fractions import Fraction

STEPS = 12


def in_set(x: Fraction) -> bool:
    """Membership in S = {x >= 0 : x * x < 2}."""
    return x >= 0 and x * x < 2


def bisect(steps: int) -> list[tuple[Fraction, Fraction]]:
    """Brackets [a, b] after 0, 1, ..., steps bisection steps, starting from a = 0 and b = 2.

    Invariant kept at every step: a is in S and b is an upper bound of S, so a <= sup S <= b.
    At the midpoint m = (a + b) / 2 (which is at least 0), either m is in S and a becomes m, or
    m * m >= 2 and m is an upper bound of S, so b becomes m. Each step halves the width.
    """
    a, b = Fraction(0), Fraction(2)
    brackets = [(a, b)]
    for _ in range(steps):
        m = (a + b) / 2
        if in_set(m):
            a = m
        else:
            b = m
        brackets.append((a, b))
    return brackets


def first_step_below(brackets: list[tuple[Fraction, Fraction]], tol: Fraction) -> int:
    """The least step index n with width b - a < tol, or -1 if no bracket in the list is that narrow."""
    for n, (a, b) in enumerate(brackets):
        if b - a < tol:
            return n
    return -1


def main() -> None:
    brackets = bisect(STEPS)
    for n, (a, b) in enumerate(brackets):
        print(f"step {n:2d}: a = {a}, b = {b}, width = {b - a}")
    sandwich = sum(a * a < 2 <= b * b for a, b in brackets)
    print(f"brackets with a*a < 2 <= b*b: {sandwich} of {len(brackets)}")
    halving = sum((b - a) == Fraction(2, 2**n) for n, (a, b) in enumerate(brackets))
    print(f"width equals 2 / 2^n after n steps: {halving} of {len(brackets)} brackets")
    nested = all(
        brackets[n + 1][0] >= brackets[n][0] and brackets[n + 1][1] <= brackets[n][1] for n in range(len(brackets) - 1)
    )
    print(f"each bracket lies inside the one before it: {nested}")
    step = first_step_below(brackets, Fraction(1, 1000))
    print(f"first step with width below 1/1000: {step}")


main()
