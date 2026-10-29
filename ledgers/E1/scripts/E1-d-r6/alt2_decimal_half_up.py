"""Alternative 2: Decimal at 60 significant digits, quantized with ROUND_HALF_UP."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, getcontext

getcontext().prec = 60
STRUCTURES = ("monopoly", "cournot", "bertrand")


def _r(x: Decimal) -> int:
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
        vol, fee = d / 2, (A + B * C) / (2 * B)
    elif structure == "cournot":
        vol, fee = 2 * d / 3, (A + 2 * B * C) / (3 * B)
    else:
        vol, fee = d, C
    profit = (fee - C) * vol
    cons = vol * vol / (2 * B)
    welf = cons + profit
    dwl = (d - vol) ** 2 / (2 * B)
    return {
        "volume_trades": _r(vol),
        "fee_cents": _r(fee),
        "profit_cents": _r(profit),
        "consumer_surplus_cents": _r(cons),
        "welfare_cents": _r(welf),
        "deadweight_loss_cents": _r(dwl),
    }
