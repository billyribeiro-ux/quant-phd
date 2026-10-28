"""Alternative B (valid): consumer surplus, welfare and deadweight loss by exact Simpson integration (exact for a line); Fraction."""

from __future__ import annotations

import math
from fractions import Fraction

STRUCTURES = ("monopoly", "cournot", "bertrand")


def half_up(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def check(structure: str, a: int, b: int, c: int) -> None:
    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")


def gross(x: Fraction, a: int, b: int) -> Fraction:
    """Integral of (a - t)/b over [0, x] by Simpson's rule with two panels: exact for linear integrands."""
    f = lambda t: (a - t) / b  # noqa: E731
    h = x / 2
    return h / 3 * (f(Fraction(0)) + 4 * f(h) + f(x))


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    check(structure, a, b, c)
    d = Fraction(a - b * c)
    if structure == "monopoly":
        volume, fee = d / 2, Fraction(a + b * c, 2 * b)
    elif structure == "cournot":
        volume, fee = 2 * d / 3, Fraction(a + 2 * b * c, 3 * b)
    else:
        volume, fee = d, Fraction(c)
    g = gross(volume, a, b)
    consumer = g - fee * volume
    profit = (fee - c) * volume
    welfare = g - c * volume
    deadweight = (gross(d, a, b) - c * d) - welfare
    return {
        "volume_trades": half_up(volume),
        "fee_cents": half_up(fee),
        "profit_cents": half_up(profit),
        "consumer_surplus_cents": half_up(consumer),
        "welfare_cents": half_up(welfare),
        "deadweight_loss_cents": half_up(deadweight),
    }
