"""Correct alternative A (verifier round 1): exact closed forms in Decimal at 60 digits, ROUND_HALF_UP; checks in b, c, a, structure order."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, localcontext
from fractions import Fraction

STRUCTURES = ("monopoly", "cournot", "bertrand")


def _round(x: Fraction) -> int:
    with localcontext() as ctx:
        ctx.prec = 60
        value = Decimal(x.numerator) / Decimal(x.denominator)
        return int(value.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    d = Fraction(a - b * c)
    if structure == "monopoly":
        volume, fee = d / 2, Fraction(a + b * c, 2 * b)
    elif structure == "cournot":
        volume, fee = Fraction(2 * (a - b * c), 3), Fraction(a + 2 * b * c, 3 * b)
    else:
        volume, fee = d, Fraction(c)
    profit = (fee - c) * volume
    consumer = volume**2 / (2 * b)
    welfare = (a * volume - Fraction(volume * volume, 2)) / b - c * volume
    deadweight = (d - volume) ** 2 / (2 * b)
    return {
        "volume_trades": _round(volume),
        "fee_cents": _round(fee),
        "profit_cents": _round(profit),
        "consumer_surplus_cents": _round(consumer),
        "welfare_cents": _round(welfare),
        "deadweight_loss_cents": _round(deadweight),
    }
