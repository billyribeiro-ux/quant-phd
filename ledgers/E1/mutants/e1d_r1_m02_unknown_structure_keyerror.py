"""An unknown structure name raises KeyError from a dict lookup, not the ValueError the page names.
"""

from __future__ import annotations

import math
from fractions import Fraction

TABLE = {"monopoly": 0, "cournot": 1, "bertrand": 2}


def half_up(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def check_inputs(structure: str, a: int, b: int, c: int) -> None:
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    check_inputs(structure, a, b, c)
    which = TABLE[structure]
    d = Fraction(a - b * c)
    if which == 0:
        volume = d / 2
        fee = Fraction(a + b * c, 2 * b)
    elif which == 1:
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
