"""Alternative 4: Fraction throughout; each exchange's profit is a quadratic whose vertex is the best quantity."""

from __future__ import annotations

import math
from fractions import Fraction


def _half(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def _vertex(alpha: Fraction, beta: Fraction) -> Fraction:
    # maximiser of alpha q^2 + beta q with alpha < 0
    return -beta / (2 * alpha)


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if structure not in ("monopoly", "cournot", "bertrand"):
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    A, Bf, Cc = Fraction(a), Fraction(b), Fraction(c)
    if structure == "monopoly":
        # profit (A - q)/B - C) q = -q^2 / B + (A/B - C) q
        q = _vertex(-1 / Bf, A / Bf - Cc)
        fee = (A - q) / Bf
    elif structure == "cournot":
        # each exchange's vertex against rival quantity r is (A - B C - r) / 2; the symmetric point solves q = (d - q) / 2
        d = A - Bf * Cc
        each = d / 3  # the symmetric fixed point of q = (d - q) / 2, solved exactly
        q = 2 * each
        fee = (A - q) / Bf
    else:
        q = A - Bf * Cc
        fee = Cc
    pi = (fee - Cc) * q
    gross = A / Bf * q - q * q / (2 * Bf)
    cs = gross - fee * q
    gap = A - Bf * Cc
    wd = gap * gap / (2 * Bf) - (gross - Cc * q)
    return {
        "volume_trades": _half(q),
        "fee_cents": _half(fee),
        "profit_cents": _half(pi),
        "consumer_surplus_cents": _half(cs),
        "welfare_cents": _half(cs + pi),
        "deadweight_loss_cents": _half(wd),
    }
