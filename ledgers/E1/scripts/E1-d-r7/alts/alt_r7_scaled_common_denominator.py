"""Alternative r7-B: every output as an exact fraction over a common denominator 36*b*(fee/vol denominators), via Fraction from integer pairs."""

from __future__ import annotations

import math
from fractions import Fraction


def _nearest(x: Fraction) -> int:
    fl = math.floor(x)
    return fl + 1 if x - fl >= Fraction(1, 2) else fl


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if not isinstance(structure, str) or structure not in ("monopoly", "cournot", "bertrand"):
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    gap = Fraction(a - b * c, 1)
    if structure == "monopoly":
        vol = gap / 2
        fee = Fraction(a + b * c, 2 * b)
    elif structure == "cournot":
        vol = Fraction(2, 3) * gap
        fee = Fraction(a + 2 * b * c, 3 * b)
    else:
        vol = gap
        fee = Fraction(c)
    margin = fee - c
    profit = margin * vol
    surplus = vol * vol / (2 * b)
    welfare = surplus + profit
    loss = (gap - vol) * (gap - vol) / (2 * b)
    return {
        "volume_trades": _nearest(vol),
        "fee_cents": _nearest(fee),
        "profit_cents": _nearest(profit),
        "consumer_surplus_cents": _nearest(surplus),
        "welfare_cents": _nearest(welfare),
        "deadweight_loss_cents": _nearest(loss),
    }
