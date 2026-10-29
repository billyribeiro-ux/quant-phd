"""Alternative C (valid): every quantity in 80-digit Decimal, one ROUND_HALF_UP quantize per output."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, localcontext

STRUCTURES = ("monopoly", "cournot", "bertrand")


def check(structure: str, a: int, b: int, c: int) -> None:
    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")


def rnd(x: Decimal) -> int:
    return int(x.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    check(structure, a, b, c)
    with localcontext() as ctx:
        ctx.prec = 80
        A, B, C = Decimal(a), Decimal(b), Decimal(c)
        d = A - B * C
        if structure == "monopoly":
            volume, fee = d / 2, (A + B * C) / (2 * B)
        elif structure == "cournot":
            volume, fee = 2 * d / 3, (A + 2 * B * C) / (3 * B)
        else:
            volume, fee = d, C
        profit = (fee - C) * volume
        consumer = volume * volume / (2 * B)
        welfare = consumer + profit
        deadweight = (d - volume) ** 2 / (2 * B)
        return {
            "volume_trades": rnd(volume),
            "fee_cents": rnd(fee),
            "profit_cents": rnd(profit),
            "consumer_surplus_cents": rnd(consumer),
            "welfare_cents": rnd(welfare),
            "deadweight_loss_cents": rnd(deadweight),
        }
