"""Alternative r7-A: pure integer arithmetic on numerator/denominator pairs, no Fraction, rounding by integer division."""

from __future__ import annotations


def _half_up(num: int, den: int) -> int:
    # nearest integer to num/den (den > 0, num >= 0), ties up: floor((2num + den) / (2den))
    return (2 * num + den) // (2 * den)


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if structure not in ("monopoly", "cournot", "bertrand"):
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
    # profit = (fee - c) * vol = ((fee_n - c*fee_d)/fee_d) * (vol_n/vol_d)
    p_n = (fee_n - c * fee_d) * vol_n
    p_d = fee_d * vol_d
    # consumer = vol^2 / (2b)
    k_n = vol_n * vol_n
    k_d = vol_d * vol_d * 2 * b
    # welfare = consumer + profit, exact sum of fractions
    w_d = k_d * p_d // _gcd(k_d, p_d) * 1
    w_n = k_n * (w_d // k_d) + p_n * (w_d // p_d)
    # deadweight = (d - vol)^2 / (2b)
    dv_n = d * vol_d - vol_n
    e_n = dv_n * dv_n
    e_d = vol_d * vol_d * 2 * b
    return {
        "volume_trades": _half_up(vol_n, vol_d),
        "fee_cents": _half_up(fee_n, fee_d),
        "profit_cents": _half_up(p_n, p_d),
        "consumer_surplus_cents": _half_up(k_n, k_d),
        "welfare_cents": _half_up(w_n, w_d),
        "deadweight_loss_cents": _half_up(e_n, e_d),
    }


def _gcd(x: int, y: int) -> int:
    while y:
        x, y = y, x % y
    return x
