"""E3 lesson L06 lab: reference-dependent value, loss aversion and the sign of a gamble's value.

Standard library only (fractions, math). No randomness and no network: every case is fixed, so the
output is the same on every run. Outcomes are changes in wealth from the reference point 0, in cents.
The prospect values printed here are on a cents-sized scale and are not money paid out. Exact cases
use fractions.Fraction with the exponents alpha = delta = 1, where the value function is linear on each
side of zero. Power cases use floats and are printed to at most four decimals or as True or False.

Value function (Definition 1.2 of the lesson):
    v(x) = x^alpha            for x >= 0
    v(x) = -lam (-x)^delta    for x < 0
A gamble with prize g (probability p) and loss l (probability 1 - p), with g, l > 0, has value
    V = p v(g) + (1 - p) v(-l).
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

Num = Fraction | float


def value_linear(x: Fraction, lam: Fraction) -> Fraction:
    """v(x) with alpha = delta = 1: x for a gain, lam * x (negative) for a loss."""
    return x if x >= 0 else lam * x


def value_power(x: float, lam: float, alpha: float, delta: float) -> float:
    """v(x) with powers alpha on gains and delta on losses, for alpha, delta in (0, 1]."""
    if x >= 0:
        return math.pow(x, alpha)
    return -lam * math.pow(-x, delta)


def gamble_value_linear(g: Fraction, loss: Fraction, p: Fraction, lam: Fraction) -> Fraction:
    """V = p v(g) + (1 - p) v(-loss) with alpha = delta = 1."""
    return p * value_linear(g, lam) + (1 - p) * value_linear(-loss, lam)


def gamble_value_power(g: float, loss: float, p: float, lam: float, alpha: float, delta: float) -> float:
    """V = p v(g) + (1 - p) v(-loss) with powers alpha and delta."""
    return p * value_power(g, lam, alpha, delta) + (1 - p) * value_power(-loss, lam, alpha, delta)


def threshold_linear(g: Fraction, loss: Fraction, p: Fraction) -> Fraction:
    """The loss-aversion coefficient at which V = 0 when alpha = delta = 1: p g / ((1 - p) loss)."""
    return p * g / ((1 - p) * loss)


def threshold_power(g: float, loss: float, p: float, alpha: float, delta: float) -> float:
    """The loss-aversion coefficient at which V = 0 for powers alpha and delta."""
    return p * math.pow(g, alpha) / ((1 - p) * math.pow(loss, delta))


def main() -> None:
    p = Fraction(1, 2)
    g = Fraction(1000)
    loss = Fraction(600)
    expected = p * g - (1 - p) * loss
    print("gamble: +1000 cents with probability 1/2, -600 cents with probability 1/2; alpha = delta = 1")
    print(f"expected value of the gamble = {expected} cents")
    star = threshold_linear(g, loss, p)
    print(f"loss-aversion threshold lam* = {star}")
    for lam in (Fraction(1), Fraction(3, 2), Fraction(2)):
        value = gamble_value_linear(g, loss, p, lam)
        print(f"lam = {lam}: prospect value V = {value}; positive: {value > 0}")
    print(f"V at lam = 1 equals the expected value: {gamble_value_linear(g, loss, p, Fraction(1)) == expected}")
    print(f"V is zero exactly at lam*: {gamble_value_linear(g, loss, p, star) == 0}")

    lam = Fraction(2)
    combined: list[tuple[Fraction, Fraction]] = [
        (Fraction(1, 4), Fraction(2000)),
        (Fraction(1, 2), Fraction(400)),
        (Fraction(1, 4), Fraction(-1200)),
    ]
    v_combined = sum((q * value_linear(x, lam) for q, x in combined), Fraction(0))
    v_single = gamble_value_linear(g, loss, p, lam)
    print("two independent copies of the gamble, at lam = 2")
    print(f"value of the combined lottery (one lottery over the sum): {v_combined}")
    print(f"two separate evaluations, one for each copy: 2 V = {2 * v_single}")
    print(f"the combined lottery is positive while each copy alone is negative: {v_combined > 0 and v_single < 0}")

    alpha = 0.5
    delta = 0.5
    lam_star = threshold_power(1000.0, 600.0, 0.5, alpha, delta)
    print(f"alpha = delta = 0.5: threshold lam* = {lam_star:.4f}")
    below = gamble_value_power(1000.0, 600.0, 0.5, lam_star * (1 - 1e-6), alpha, delta)
    above = gamble_value_power(1000.0, 600.0, 0.5, lam_star * (1 + 1e-6), alpha, delta)
    print(f"sign of V just below lam*: positive {below > 0}; just above lam*: negative {above < 0}")
    at_two = gamble_value_power(1000.0, 600.0, 0.5, 2.0, alpha, delta)
    print(f"V at lam = 2 with alpha = delta = 0.5: {at_two:.4f}")

    grid = (1.0, 2.0, 4.0, 9.0)
    gains_concave = all(
        value_power((a + b) / 2, 2.0, alpha, delta)
        >= (value_power(a, 2.0, alpha, delta) + value_power(b, 2.0, alpha, delta)) / 2
        for a in grid
        for b in grid
    )
    losses_convex = all(
        value_power(-(a + b) / 2, 2.0, alpha, delta)
        <= (value_power(-a, 2.0, alpha, delta) + value_power(-b, 2.0, alpha, delta)) / 2
        for a in grid
        for b in grid
    )
    losses = (-9.0, -4.0, -2.0, -1.0)
    increasing = all(
        value_power(x, 2.0, alpha, delta) < value_power(y, 2.0, alpha, delta) for x, y in itertools.pairwise(grid)
    ) and all(
        value_power(x, 2.0, alpha, delta) < value_power(y, 2.0, alpha, delta) for x, y in itertools.pairwise(losses)
    )
    print(f"gain part concave on the grid: {gains_concave}; loss part convex on the grid: {losses_convex}")
    print(f"value increasing along the gains grid and along the losses grid: {increasing}")
    ratio_ok = all(
        math.isclose(abs(value_power(-x, 2.0, alpha, alpha)) / value_power(x, 2.0, alpha, alpha), 2.0, rel_tol=1e-12)
        for x in grid
    )
    print(f"equal magnitudes with alpha = delta: |v(-x)| / v(x) = lam = 2 on the grid: {ratio_ok}")


main()
