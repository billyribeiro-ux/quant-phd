"""Alternative 1: exact rationals as (numerator, denominator) integer pairs; half-up by integer arithmetic."""
from __future__ import annotations

STRUCTURES = ("monopoly", "cournot", "bertrand")


def _round_half_up(num: int, den: int) -> int:
    assert num >= 0 and den > 0
    return (2 * num + den) // (2 * den)


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if not isinstance(structure, str) or structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    d = a - b * c
    if structure == "monopoly":
        vn, vd = d, 2
        fn, fd = a + b * c, 2 * b
    elif structure == "cournot":
        vn, vd = 2 * d, 3
        fn, fd = a + 2 * b * c, 3 * b
    else:
        vn, vd = d, 1
        fn, fd = c, 1
    # profit = (fee - c) * volume, all as one fraction
    pn, pd = (fn - c * fd) * vn, fd * vd
    # consumer = volume^2 / (2b)
    cn, cd = vn * vn, vd * vd * 2 * b
    # welfare = consumer + profit
    wn, wd = cn * pd + pn * cd, cd * pd
    # deadweight = (d - volume)^2 / (2b)
    dn, dd = (d * vd - vn) ** 2, vd * vd * 2 * b
    return {
        "volume_trades": _round_half_up(vn, vd),
        "fee_cents": _round_half_up(fn, fd),
        "profit_cents": _round_half_up(pn, pd),
        "consumer_surplus_cents": _round_half_up(cn, cd),
        "welfare_cents": _round_half_up(wn, wd),
        "deadweight_loss_cents": _round_half_up(dn, dd),
    }
