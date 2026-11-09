"""Alternative correct engine: Decimal at 60 significant digits, quantized with ROUND_HALF_UP."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
STRUCTURES = ("monopoly", "cournot", "bertrand")


def _round(x: Decimal) -> int:
    return int(x.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if not isinstance(structure, str) or structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    A, B, C = Decimal(a), Decimal(b), Decimal(c)
    d = A - B * C
    if structure == "monopoly":
        volume = d / 2
        fee = (A + B * C) / (2 * B)
    elif structure == "cournot":
        volume = 2 * d / 3
        fee = (A + 2 * B * C) / (3 * B)
    else:
        volume = d
        fee = C
    profit = (fee - C) * volume
    consumer = volume * volume / (2 * B)
    welfare = consumer + profit
    deadweight = (d - volume) ** 2 / (2 * B)
    return {
        "volume_trades": _round(volume),
        "fee_cents": _round(fee),
        "profit_cents": _round(profit),
        "consumer_surplus_cents": _round(consumer),
        "welfare_cents": _round(welfare),
        "deadweight_loss_cents": _round(deadweight),
    }
