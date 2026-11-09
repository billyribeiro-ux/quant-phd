"""Correct engine: surpluses from the explicit integral of inverse demand, midpoint Riemann sum is NOT used, exact antiderivative."""

from __future__ import annotations

from fractions import Fraction
import math


def _half_up(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def _antiderivative(x: Fraction, a: int, b: int) -> Fraction:
    # integral_0^x (a - t)/b dt
    return (a * x - x * x / 2) / b


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if structure not in ("monopoly", "cournot", "bertrand") or not isinstance(structure, str):
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    d = Fraction(a - b * c)
    if structure == "monopoly":
        q, f = d / 2, Fraction(a + b * c, 2 * b)
    elif structure == "cournot":
        q, f = 2 * d / 3, Fraction(a + 2 * b * c, 3 * b)
    else:
        q, f = d, Fraction(c)
    profit = (f - c) * q
    gross = _antiderivative(q, a, b)
    cs = gross - f * q
    welfare = gross - c * q
    dwl = _antiderivative(d, a, b) - c * d - welfare
    return {
        "volume_trades": _half_up(q),
        "fee_cents": _half_up(f),
        "profit_cents": _half_up(profit),
        "consumer_surplus_cents": _half_up(cs),
        "welfare_cents": _half_up(welfare),
        "deadweight_loss_cents": _half_up(dwl),
    }
