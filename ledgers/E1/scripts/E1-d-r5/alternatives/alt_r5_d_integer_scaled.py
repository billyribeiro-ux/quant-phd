"""Integers only: every output is a rational p/q with integer p, q, rounded half up by (2p + q) // (2q)."""

from __future__ import annotations


def _half_up(p: int, q: int) -> int:
    if q < 0:
        p, q = -p, -q
    return (2 * p + q) // (2 * q)


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
    # profit = (fee - c) * vol
    pr_n, pr_d = (fee_n - c * fee_d) * vol_n, fee_d * vol_d
    # consumer = vol^2 / (2b)
    cs_n, cs_d = vol_n * vol_n, vol_d * vol_d * 2 * b
    # welfare = consumer + profit
    w_n = cs_n * pr_d + pr_n * cs_d
    w_d = cs_d * pr_d
    # dwl = (d - vol)^2 / (2b)
    dv_n = d * vol_d - vol_n
    dw_n, dw_d = dv_n * dv_n, vol_d * vol_d * 2 * b
    return {
        "volume_trades": _half_up(vol_n, vol_d),
        "fee_cents": _half_up(fee_n, fee_d),
        "profit_cents": _half_up(pr_n, pr_d),
        "consumer_surplus_cents": _half_up(cs_n, cs_d),
        "welfare_cents": _half_up(w_n, w_d),
        "deadweight_loss_cents": _half_up(dw_n, dw_d),
    }
