"""Verifier round 2 alternative: Decimal arithmetic at 80 digits, rounded with quantize(ROUND_HALF_UP). Correct."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, getcontext
from fractions import Fraction

getcontext().prec = 80
STRUCTURES: tuple[str, ...] = ("monopoly", "cournot", "bertrand")


def to_dec(x: Fraction) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def rnd(x: Decimal) -> int:
    return int(x.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    d = Decimal(a - b * c)
    if structure == "monopoly":
        volume = d / 2
        fee = (Decimal(a) + Decimal(b * c)) / (2 * Decimal(b))
    elif structure == "cournot":
        volume = 2 * d / 3
        fee = (Decimal(a) + 2 * Decimal(b * c)) / (3 * Decimal(b))
    else:
        volume = d
        fee = Decimal(c)
    profit = (fee - c) * volume
    consumer = volume * volume / (2 * Decimal(b))
    welfare = consumer + profit
    deadweight = (d - volume) ** 2 / (2 * Decimal(b))
    return {
        "volume_trades": rnd(volume),
        "fee_cents": rnd(fee),
        "profit_cents": rnd(profit),
        "consumer_surplus_cents": rnd(consumer),
        "welfare_cents": rnd(welfare),
        "deadweight_loss_cents": rnd(deadweight),
    }
