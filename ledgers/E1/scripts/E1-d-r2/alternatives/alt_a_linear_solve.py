"""Alternative A (valid): the Cournot and monopoly volumes from a small exact linear-system solve; Fraction throughout."""

from __future__ import annotations

import math
from fractions import Fraction

STRUCTURES = ("monopoly", "cournot", "bertrand")


def half_up(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def solve2(m: list[list[Fraction]], v: list[Fraction]) -> list[Fraction]:
    (p, q), (r, s) = m
    det = p * s - q * r
    return [(v[0] * s - q * v[1]) / det, (p * v[1] - r * v[0]) / det]


def check(structure: str, a: int, b: int, c: int) -> None:
    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    check(structure, a, b, c)
    d = Fraction(a - b * c)
    if structure == "monopoly":
        # FOC of (a - Q)/b - c) Q: -2Q/b + d/b = 0, written as a 1x1 system
        q, _ = solve2([[Fraction(2), Fraction(0)], [Fraction(0), Fraction(1)]], [d, Fraction(0)])
        volume = q
        fee = (a - volume) / b
    elif structure == "cournot":
        # symmetric FOC system: 2 q1 + q2 = d, q1 + 2 q2 = d
        q1, q2 = solve2([[Fraction(2), Fraction(1)], [Fraction(1), Fraction(2)]], [d, d])
        volume = q1 + q2
        fee = (a - volume) / b
    else:
        volume = d
        fee = Fraction(c)
    profit = (fee - c) * volume
    consumer = volume * volume / (2 * b)
    welfare = consumer + profit
    deadweight = (d - volume) ** 2 / (2 * b)
    return {
        "volume_trades": half_up(volume),
        "fee_cents": half_up(fee),
        "profit_cents": half_up(profit),
        "consumer_surplus_cents": half_up(consumer),
        "welfare_cents": half_up(welfare),
        "deadweight_loss_cents": half_up(deadweight),
    }
