"""Verifier round 2 alternative: Cournot quantity from 200 best-response steps (inexact by d/(3 2^200)).

The other structures are closed forms. Not an exact-fraction implementation, so the suite must reject it."""

from __future__ import annotations

import math
from fractions import Fraction

STRUCTURES: tuple[str, ...] = ("monopoly", "cournot", "bertrand")


def half_up(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def check(structure: str, a: int, b: int, c: int) -> None:
    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if b <= 0:
        raise ValueError("b must be positive")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if c <= 0:
        raise ValueError("c must be positive")


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    check(structure, a, b, c)
    d = Fraction(a - b * c)
    if structure == "cournot":
        q = Fraction(0)
        for _ in range(200):
            q = (d - q) / 2  # best response of one exchange to the rival's quantity q
        volume = 2 * q
        fee = (a - volume) / b
    elif structure == "monopoly":
        volume = d / 2
        fee = Fraction(a + b * c, 2 * b)
    else:
        volume = d
        fee = Fraction(c)
    profit = (fee - c) * volume
    consumer = volume * volume / (2 * b)
    welfare = (a * volume - volume * volume / 2) / b - c * volume
    deadweight = (d - volume) ** 2 / (2 * b)
    return {
        "volume_trades": half_up(volume),
        "fee_cents": half_up(fee),
        "profit_cents": half_up(profit),
        "consumer_surplus_cents": half_up(consumer),
        "welfare_cents": half_up(welfare),
        "deadweight_loss_cents": half_up(deadweight),
    }
