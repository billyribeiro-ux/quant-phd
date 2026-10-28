"""Alternative 1: the closed forms of the specification, with each profit and surplus written as its closed form."""

from __future__ import annotations

import math
from fractions import Fraction


def _half(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if structure not in ("monopoly", "cournot", "bertrand"):
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    d = a - b * c
    if structure == "monopoly":
        q, f, pi = Fraction(d, 2), Fraction(a + b * c, 2 * b), Fraction(d * d, 4 * b)
    elif structure == "cournot":
        q, f, pi = Fraction(2 * d, 3), Fraction(a + 2 * b * c, 3 * b), Fraction(2 * d * d, 9 * b)
    else:
        q, f, pi = Fraction(d), Fraction(c), Fraction(0)
    cs = Fraction(q * q, 2 * b)
    dwl = Fraction((d * d) - 2 * d * q + q * q, 2 * b)
    return {
        "volume_trades": _half(q),
        "fee_cents": _half(f),
        "profit_cents": _half(pi),
        "consumer_surplus_cents": _half(cs),
        "welfare_cents": _half(cs + pi),
        "deadweight_loss_cents": _half(dwl),
    }
