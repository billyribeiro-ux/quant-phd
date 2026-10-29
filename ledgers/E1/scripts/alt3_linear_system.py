"""Alternative 3: the first-order conditions as a linear system solved by Cramer's rule in Fractions."""

from __future__ import annotations

import math
from fractions import Fraction


def _half(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def _solve2(m: tuple[tuple[int, int], tuple[int, int]], rhs: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    x = (rhs[0] * m[1][1] - m[0][1] * rhs[1]) / det
    y = (m[0][0] * rhs[1] - m[1][0] * rhs[0]) / det
    return x, y


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if structure not in ("monopoly", "cournot", "bertrand"):
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    d = Fraction(a - b * c)
    if structure == "monopoly":
        # FOC of (a - Q)/b - c) Q in Q: 2 Q = d
        q = Fraction(d / 2)
        fee = Fraction(a, b) - q / b
    elif structure == "cournot":
        # FOCs: 2 q1 + q2 = d and q1 + 2 q2 = d
        q1, q2 = _solve2(((2, 1), (1, 2)), (d, d))
        q = q1 + q2
        fee = Fraction(a, b) - q / b
    else:
        q = d
        fee = Fraction(c)
    pi = (fee - c) * q
    gross = Fraction(a, b) * q - q * q / (2 * b)
    cs = gross - fee * q
    welfare = cs + pi
    wd = Fraction(d * d, 2 * b) - (gross - c * q)
    return {
        "volume_trades": _half(q),
        "fee_cents": _half(fee),
        "profit_cents": _half(pi),
        "consumer_surplus_cents": _half(cs),
        "welfare_cents": _half(welfare),
        "deadweight_loss_cents": _half(wd),
    }
