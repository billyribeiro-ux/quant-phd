"""Alternative correct solution: fee from the inverse demand at each volume, and rounding by integer arithmetic."""
from __future__ import annotations

from fractions import Fraction

STRUCTURES: tuple[str, ...] = ("monopoly", "cournot", "bertrand")


def _round(x: Fraction) -> int:
    # nearest integer with a tie going up, from the exact numerator and denominator
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


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
    gap = a - b * c
    volume = {"monopoly": Fraction(gap, 2), "cournot": Fraction(2 * gap, 3), "bertrand": Fraction(gap)}[structure]
    fee = Fraction(a - volume, b)  # inverse demand evaluated at the exact volume
    profit = (fee - c) * volume
    consumer = Fraction(volume**2, 2 * b)
    welfare = consumer + profit
    deadweight = Fraction((gap - volume) ** 2, 2 * b)
    return {
        "volume_trades": _round(volume),
        "fee_cents": _round(fee),
        "profit_cents": _round(profit),
        "consumer_surplus_cents": _round(consumer),
        "welfare_cents": _round(welfare),
        "deadweight_loss_cents": _round(deadweight),
    }
