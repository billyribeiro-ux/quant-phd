"""Alternative 2: Cournot quantity by iterated best response in floats to a 1e-12 stop, then exact outputs."""

from __future__ import annotations

import math
from fractions import Fraction


def _half(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def _cournot_quantity(d: int) -> Fraction:
    q = 0.0
    for _ in range(200):
        nxt = (d - q) / 2  # exchange i's best response to the rival's quantity q
        if abs(nxt - q) < 1e-12:
            q = nxt
            break
        q = nxt
    return Fraction(q).limit_denominator(1000)


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
        q = Fraction(d, 2)
    elif structure == "cournot":
        # each exchange's best response q = (d - rival)/2 iterated from zero, equal quantities, so 2q is the volume
        q = 2 * _cournot_quantity(d)
    else:
        q = Fraction(d)
    fee = (a - q) / b  # the inverse demand at the volume
    gross = Fraction(a, b) * q - Fraction(q * q, 2 * b)
    cs = gross - fee * q
    pi = (fee - c) * q
    wd = Fraction(d * d, 2 * b) - (gross - c * q + 0)
    return {
        "volume_trades": _half(q),
        "fee_cents": _half(fee),
        "profit_cents": _half(pi),
        "consumer_surplus_cents": _half(cs),
        "welfare_cents": _half(cs + pi),
        "deadweight_loss_cents": _half(wd),
    }
