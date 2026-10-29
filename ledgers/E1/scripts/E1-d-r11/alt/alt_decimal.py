"""Alternative correct solution: exact Fraction volumes, money rounded half up with Decimal quantize."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, localcontext
from fractions import Fraction

STRUCTURES: tuple[str, ...] = ("monopoly", "cournot", "bertrand")


def _round(x: Fraction) -> int:
    with localcontext() as ctx:
        ctx.prec = 400
        value = Decimal(x.numerator) / Decimal(x.denominator)
        return int(value.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def check_inputs(structure: str, a: int, b: int, c: int) -> None:
    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    check_inputs(structure, a, b, c)
    d = Fraction(a - b * c)
    if structure == "monopoly":
        volume = d / 2
        fee = Fraction(a + b * c, 2 * b)
    elif structure == "cournot":
        volume = Fraction(2, 3) * d
        fee = Fraction(a + 2 * b * c, 3 * b)
    else:
        volume = d
        fee = Fraction(c)
    profit = (fee - c) * volume
    consumer = volume * volume / (2 * b)
    welfare = consumer + profit
    deadweight = (d - volume) ** 2 / (2 * b)
    return {
        "volume_trades": _round(volume),
        "fee_cents": _round(fee),
        "profit_cents": _round(profit),
        "consumer_surplus_cents": _round(consumer),
        "welfare_cents": _round(welfare),
        "deadweight_loss_cents": _round(deadweight),
    }
