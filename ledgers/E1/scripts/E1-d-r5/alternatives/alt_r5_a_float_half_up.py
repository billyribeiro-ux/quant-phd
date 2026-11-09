"""Float arithmetic throughout, with the same half-up rule floor(x + 1/2) applied to each float output."""

import math


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if not isinstance(structure, str) or structure not in ("monopoly", "cournot", "bertrand"):
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    d = float(a - b * c)
    if structure == "monopoly":
        q, f = d / 2, (a + b * c) / (2 * b)
    elif structure == "cournot":
        q, f = 2 * d / 3, (a + 2 * b * c) / (3 * b)
    else:
        q, f = d, float(c)
    profit = (f - c) * q
    cs = q * q / (2 * b)
    welfare = cs + profit
    dwl = (d - q) ** 2 / (2 * b)
    h = lambda x: int(math.floor(x + 0.5))
    return {
        "volume_trades": h(q),
        "fee_cents": h(f),
        "profit_cents": h(profit),
        "consumer_surplus_cents": h(cs),
        "welfare_cents": h(welfare),
        "deadweight_loss_cents": h(dwl),
    }
