"""Alternative correct engine: integer numerator and denominator, rounded by (2n + m) // (2m) with no Fraction."""

from __future__ import annotations

STRUCTURES = ("monopoly", "cournot", "bertrand")


def _round(num: int, den: int) -> int:
    if den < 0:
        num, den = -num, -den
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
    # every exact value as num/den: volume V = vn/vd, fee F = fn/fd, the rest over a common denominator 18b
    if structure == "monopoly":
        vn, vd = d, 2
        fn, fd = a + b * c, 2 * b
    elif structure == "cournot":
        vn, vd = 2 * d, 3
        fn, fd = a + 2 * b * c, 3 * b
    else:
        vn, vd = d, 1
        fn, fd = c, 1
    # profit = (F - c) V = (fn - c fd) vn / (fd vd)
    pn, pd = (fn - c * fd) * vn, fd * vd
    # consumer = V^2 / (2b) = vn^2 / (2b vd^2)
    cn, cd = vn * vn, 2 * b * vd * vd
    # welfare = consumer + profit over the common denominator cd * pd (both have a positive denominator)
    wn, wd = cn * pd + pn * cd, cd * pd
    # deadweight = (d - V)^2 / (2b) = ((d vd - vn)^2) / (vd^2 * 2b)
    dn, dd = (d * vd - vn) ** 2, 2 * b * vd * vd
    return {
        "volume_trades": _round(vn, vd),
        "fee_cents": _round(fn, fd),
        "profit_cents": _round(pn, pd),
        "consumer_surplus_cents": _round(cn, cd),
        "welfare_cents": _round(wn, wd),
        "deadweight_loss_cents": _round(dn, dd),
    }
