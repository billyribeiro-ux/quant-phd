"""The cost check tests c < 0 instead of c <= 0, so a zero cost per trade is accepted where the page requires a ValueError."""

from __future__ import annotations

import math
from fractions import Fraction

STRUCTURES: tuple[str, ...] = ("monopoly", "cournot", "bertrand")


def half_up(x: Fraction) -> int:
    """The nearest whole number to a non-negative exact value, a tie going up."""
    return math.floor(x + Fraction(1, 2))


def check_inputs(structure: str, a: int, b: int, c: int) -> None:
    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c < 0:
        raise ValueError("c must be positive")


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    check_inputs(structure, a, b, c)
    d = Fraction(a - b * c)
    if structure == "monopoly":
        volume = d / 2
        fee = Fraction(a + b * c, 2 * b)
    elif structure == "cournot":
        volume = 2 * d / 3
        fee = Fraction(a + 2 * b * c, 3 * b)
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
