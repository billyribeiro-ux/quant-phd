"""Correct engine: closed-form dispatch table, structure KeyError mapped to ValueError, checks in a different order."""

from __future__ import annotations

from fractions import Fraction
import math


def _half_up(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    d = Fraction(a - b * c)
    closed = {
        "monopoly": (lambda: (d / 2, Fraction(a + b * c, 2 * b))),
        "cournot": (lambda: (2 * d / 3, Fraction(a + 2 * b * c, 3 * b))),
        "bertrand": (lambda: (d, Fraction(c))),
    }
    try:
        pick = closed[structure]
    except (KeyError, TypeError) as exc:
        raise ValueError("structure must be one of monopoly, cournot, bertrand") from exc
    vol, fee = pick()
    profit = (fee - c) * vol
    cs = vol**2 / (2 * b)
    welfare = cs + profit
    dwl = (d - vol) ** 2 / (2 * b)
    return {
        "volume_trades": _half_up(vol),
        "fee_cents": _half_up(fee),
        "profit_cents": _half_up(profit),
        "consumer_surplus_cents": _half_up(cs),
        "welfare_cents": _half_up(welfare),
        "deadweight_loss_cents": _half_up(dwl),
    }
