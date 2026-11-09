"""Correct engine using integer numerator and denominator pairs only, no fractions module."""

from __future__ import annotations


def _round_half_up(num: int, den: int) -> int:
    # den > 0; floor(num/den + 1/2) = floor((2*num + den) / (2*den))
    return (2 * num + den) // (2 * den)


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if not isinstance(structure, str) or structure not in ("monopoly", "cournot", "bertrand"):
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    d = a - b * c
    if structure == "monopoly":
        vol_n, vol_d = d, 2
        fee_n, fee_d = a + b * c, 2 * b
    elif structure == "cournot":
        vol_n, vol_d = 2 * d, 3
        fee_n, fee_d = a + 2 * b * c, 3 * b
    else:
        vol_n, vol_d = d, 1
        fee_n, fee_d = c, 1
    # profit = (fee - c) * vol = (fee_n - c*fee_d)/fee_d * vol_n/vol_d
    p_n, p_d = (fee_n - c * fee_d) * vol_n, fee_d * vol_d
    # consumer = vol^2/(2b)
    cs_n, cs_d = vol_n * vol_n, vol_d * vol_d * 2 * b
    # welfare = consumer + profit
    w_n = cs_n * p_d + p_n * cs_d
    w_d = cs_d * p_d
    # deadweight = (d - vol)^2/(2b)
    g_n = d * vol_d - vol_n
    dw_n, dw_d = g_n * g_n, vol_d * vol_d * 2 * b
    return {
        "volume_trades": _round_half_up(vol_n, vol_d),
        "fee_cents": _round_half_up(fee_n, fee_d),
        "profit_cents": _round_half_up(p_n, p_d),
        "consumer_surplus_cents": _round_half_up(cs_n, cs_d),
        "welfare_cents": _round_half_up(w_n, w_d),
        "deadweight_loss_cents": _round_half_up(dw_n, dw_d),
    }
