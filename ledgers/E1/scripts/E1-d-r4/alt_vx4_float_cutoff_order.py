"""Alternative correct engine: float arithmetic with a 1e-9 half-up cutoff; checks b, c, a in that order, then structure."""

from __future__ import annotations

import math


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if b <= 0 or isinstance(b, bool):
        if b <= 0:
            raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if not isinstance(structure, str) or structure not in ("monopoly", "cournot", "bertrand"):
        raise ValueError("structure must be one of monopoly, cournot, bertrand")

    def rnd(x: float) -> int:
        return math.floor(x + 0.5 + 1e-9)

    d = float(a - b * c)
    if structure == "monopoly":
        q = d / 2.0
        f = (a + b * c) / (2.0 * b)
    elif structure == "cournot":
        q = 2.0 * d / 3.0
        f = (a + 2.0 * b * c) / (3.0 * b)
    else:
        q = d
        f = float(c)
    profit = (f - c) * q
    cs = q * q / (2.0 * b)
    welfare = cs + profit
    dwl = (d - q) ** 2 / (2.0 * b)
    return {
        "volume_trades": rnd(q),
        "fee_cents": rnd(f),
        "profit_cents": rnd(profit),
        "consumer_surplus_cents": rnd(cs),
        "welfare_cents": rnd(welfare),
        "deadweight_loss_cents": rnd(dwl),
    }
