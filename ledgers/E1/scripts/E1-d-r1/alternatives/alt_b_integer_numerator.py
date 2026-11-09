"""Correct alternative B (verifier round 1): every quantity as an integer numerator over a denominator; round by (2p+q)//(2q)."""

from __future__ import annotations


def _r(p: int, q: int) -> int:
    # nearest integer to p/q for p/q >= 0, a tie going up; q > 0
    return (2 * p + q) // (2 * q)


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
    # volume = vp / vq, fee = fp / fq (fq = b or 3b), all integers
    if structure == "monopoly":
        vp, vq = d, 2
        fp, fq = a + b * c, 2 * b
    elif structure == "cournot":
        vp, vq = 2 * d, 3
        fp, fq = a + 2 * b * c, 3 * b
    else:
        vp, vq = d, 1
        fp, fq = c, 1
    # profit = (fee - c) * volume = ((fp - c*fq) / fq) * (vp / vq)
    pp, pq = (fp - c * fq) * vp, fq * vq
    # consumer surplus = volume^2 / (2b)
    cp, cq = vp * vp, vq * vq * 2 * b
    # welfare = consumer + profit, common denominator cq and pq
    wq = _lcm(cq, pq)
    wp = cp * (wq // cq) + pp * (wq // pq)
    # deadweight = (d - volume)^2 / (2b) = (d*vq - vp)^2 / (vq^2 * 2b)
    dp, dq = (d * vq - vp) ** 2, vq * vq * 2 * b
    return {
        "volume_trades": _r(vp, vq),
        "fee_cents": _r(fp, fq),
        "profit_cents": _r(pp, pq),
        "consumer_surplus_cents": _r(cp, cq),
        "welfare_cents": _r(wp, wq),
        "deadweight_loss_cents": _r(dp, dq),
    }


def _lcm(x: int, y: int) -> int:
    from math import gcd

    return x // gcd(x, y) * y
