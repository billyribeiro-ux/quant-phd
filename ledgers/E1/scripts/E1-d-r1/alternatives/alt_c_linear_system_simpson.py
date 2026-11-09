"""Correct alternative C (verifier round 1): Cournot from a 2x2 linear system (Cramer), consumer surplus and gross value by exact Simpson's rule."""

from __future__ import annotations

import math
from fractions import Fraction


def _half_up(x: Fraction) -> int:
    return int(x + Fraction(1, 2))  # x >= 0 here, so int() truncation equals floor


def _simpson(f, lo: Fraction, hi: Fraction) -> Fraction:  # type: ignore[no-untyped-def]
    mid = (lo + hi) / 2
    return (hi - lo) / 6 * (f(lo) + 4 * f(mid) + f(hi))


def _cournot_volume(a: int, b: int, c: int) -> Fraction:
    # q1 - (d - q2)/2 = 0 and q2 - (d - q1)/2 = 0 as 2 q1 + q2 = d, q1 + 2 q2 = d
    d = Fraction(a - b * c)
    det = Fraction(3)
    q1 = (d * 2 - d * 1) / det
    q2 = (2 * d - d * 1) / det
    return q1 + q2


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
    inverse = lambda t: (a - t) / b  # noqa: E731

    if structure == "monopoly":
        volume = d / 2
    elif structure == "cournot":
        volume = _cournot_volume(a, b, c)
    else:
        volume = d
    fee = inverse(volume)
    gross = _simpson(inverse, Fraction(0), volume)
    consumer = gross - fee * volume
    profit = (fee - c) * volume
    welfare = gross - c * volume
    gross_gap = _simpson(inverse, Fraction(0), d)
    deadweight = (gross_gap - c * d) - welfare
    return {
        "volume_trades": _half_up(volume),
        "fee_cents": _half_up(fee),
        "profit_cents": _half_up(profit),
        "consumer_surplus_cents": _half_up(consumer),
        "welfare_cents": _half_up(welfare),
        "deadweight_loss_cents": _half_up(deadweight),
    }
