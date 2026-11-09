"""Verifier round 2 alternative: reference closed forms, ValueError checks in the order c, b, a, structure.

Correct: the spec lets any one message stand when several conditions hold."""

from __future__ import annotations

import math
from fractions import Fraction

STRUCTURES: tuple[str, ...] = ("monopoly", "cournot", "bertrand")


def half_up(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if c <= 0:
        raise ValueError("c must be positive")
    if b <= 0:
        raise ValueError("b must be positive")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    d = Fraction(a - b * c)
    if structure == "monopoly":
        volume, fee = d / 2, Fraction(a + b * c, 2 * b)
    elif structure == "cournot":
        volume, fee = 2 * d / 3, Fraction(a + 2 * b * c, 3 * b)
    else:
        volume, fee = d, Fraction(c)
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
