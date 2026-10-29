"""Alternative D (valid): Cournot volume by best-response iteration with a float stop test, then the exact closed form is used for every output."""

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


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    check(structure, a, b, c)
    d = Fraction(a - b * c)
    if structure == "cournot":
        q = 0.0
        for _ in range(10_000):
            nxt = (float(d) - q) / 2.0  # the best response of one exchange to its rival's quantity q
            if abs(nxt - q) < 1e-9:
                break
            q = nxt
        assert abs(q - float(d) / 3.0) < 1e-6  # the iteration has found the symmetric point
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
