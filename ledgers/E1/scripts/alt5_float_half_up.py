"""Alternative 5: float arithmetic throughout, each output rounded once by floor(x + 0.5) from its float value."""

from __future__ import annotations

import math


def _half(x: float) -> int:
    return math.floor(x + 0.5)


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if structure not in ("monopoly", "cournot", "bertrand"):
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    d = float(a - b * c)
    if structure == "monopoly":
        q = d / 2.0
        fee = (a + b * c) / (2.0 * b)
    elif structure == "cournot":
        q = 2.0 * d / 3.0
        fee = (a + 2.0 * b * c) / (3.0 * b)
    else:
        q = d
        fee = float(c)
    pi = (fee - c) * q
    cs = q * q / (2.0 * b)
    wd = (d - q) ** 2 / (2.0 * b)
    return {
        "volume_trades": _half(q),
        "fee_cents": _half(fee),
        "profit_cents": _half(pi),
        "consumer_surplus_cents": _half(cs),
        "welfare_cents": _half(cs + pi),
        "deadweight_loss_cents": _half(wd),
    }
