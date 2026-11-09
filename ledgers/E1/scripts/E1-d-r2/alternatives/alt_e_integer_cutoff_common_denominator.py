"""Verifier round 2 alternative: integer numerators over the common denominator 18b.

Rounding is (2n + m) // (2m). Correct."""

from __future__ import annotations

STRUCTURES: tuple[str, ...] = ("monopoly", "cournot", "bertrand")


def rnd(num: int, den: int) -> int:
    # nearest integer to num/den (den > 0), a tie going up: floor(num/den + 1/2) = floor((2 num + den) / (2 den))
    return (2 * num + den) // (2 * den)


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    d = a - b * c
    k = 18 * b  # common denominator for volumes (d/2, 2d/3, d), fees (/(2b), /(3b)), and money terms
    if structure == "monopoly":
        vol_n, fee_n, fee_d = d * 9 * b, (a + b * c) * 9, 18 * b  # volume = d/2 = (9 d b)/(18 b)
    elif structure == "cournot":
        vol_n, fee_n, fee_d = 12 * d * b, (a + 2 * b * c) * 6, 18 * b
    else:
        vol_n, fee_n, fee_d = d * k, c * k, k
    # volume_n / k is the exact volume; fee_n / fee_d is the exact fee
    vol_den = k
    # profit = (fee - c) * volume, fee - c as a fraction over fee_d
    profit_n = (fee_n - c * fee_d) * vol_n
    profit_d = fee_d * vol_den
    # consumer = volume^2 / (2b), welfare = consumer + profit, deadweight = (d - volume)^2 / (2b)
    cons_n = vol_n * vol_n
    cons_d = vol_den * vol_den * 2 * b
    # bring profit and consumer to the common denominator; cross-multiply
    welfare_n = cons_n * profit_d + profit_n * cons_d
    welfare_den = cons_d * profit_d
    dw_n = (d * vol_den - vol_n) ** 2
    dw_den = vol_den * vol_den * 2 * b
    return {
        "volume_trades": rnd(vol_n, vol_den),
        "fee_cents": rnd(fee_n, fee_d),
        "profit_cents": rnd(profit_n, profit_d),
        "consumer_surplus_cents": rnd(cons_n, cons_d),
        "welfare_cents": rnd(welfare_n, welfare_den),
        "deadweight_loss_cents": rnd(dw_n, dw_den),
    }
