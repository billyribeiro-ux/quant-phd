"""Alternative correct engine: Cournot volume by Cramer's rule on the 2x2 reaction system, surpluses by Simpson's rule."""

from __future__ import annotations

import math
from fractions import Fraction

STRUCTURES = ("monopoly", "cournot", "bertrand")


def _half_up(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def _simpson(f, lo: Fraction, hi: Fraction) -> Fraction:
    mid = (lo + hi) / 2
    return (hi - lo) / 6 * (f(lo) + 4 * f(mid) + f(hi))


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if c <= 0:
        raise ValueError("c must be positive")
    if b <= 0:
        raise ValueError("b must be positive")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if not isinstance(structure, str) or structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    A, B, C = Fraction(a), Fraction(b), Fraction(c)
    d = A - B * C
    if structure == "monopoly":
        volume = d / 2
    elif structure == "cournot":
        # 2 q1 + q2 = d and q1 + 2 q2 = d, Cramer's rule with determinant 3
        det = Fraction(2 * 2 - 1 * 1)
        q1 = (d * 2 - 1 * d) / det
        volume = q1 + q1
    else:
        volume = d
    fee = (A - volume) / B
    if structure == "bertrand":
        fee = C
    inverse = lambda t: (A - t) / B  # noqa: E731
    consumer = _simpson(lambda t: inverse(t) - fee, Fraction(0), volume)
    profit = (fee - C) * volume
    welfare = consumer + profit
    deadweight = _simpson(lambda t: inverse(t) - C, volume, d) if volume <= d else Fraction(0)
    return {
        "volume_trades": _half_up(volume),
        "fee_cents": _half_up(fee),
        "profit_cents": _half_up(profit),
        "consumer_surplus_cents": _half_up(consumer),
        "welfare_cents": _half_up(welfare),
        "deadweight_loss_cents": _half_up(deadweight),
    }
