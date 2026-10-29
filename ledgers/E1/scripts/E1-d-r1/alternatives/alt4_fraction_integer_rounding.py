"""Alt 4: Fraction throughout, with the half-up rounding done on numerator and denominator."""
from fractions import Fraction

def _check(structure, a, b, c):
    if structure not in ("monopoly", "cournot", "bertrand"):
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")

def _r(x):
    p, q = x.numerator, x.denominator
    return (2 * p + q) // (2 * q)

def outcome(structure, a, b, c):
    _check(structure, a, b, c)
    d = Fraction(a - b * c)
    if structure == "monopoly":
        Q, f = d / 2, Fraction(a + b * c, 2 * b)
    elif structure == "cournot":
        Q, f = Fraction(2, 3) * d, Fraction(a + 2 * b * c, 3 * b)
    else:
        Q, f = d, Fraction(c)
    pi = Fraction(f - c) * Q
    cs = Q ** 2 / Fraction(2 * b)
    W = cs + pi
    L = Fraction((d - Q) ** 2) / Fraction(2 * b)
    return {"volume_trades": _r(Q), "fee_cents": _r(f), "profit_cents": _r(pi),
            "consumer_surplus_cents": _r(cs), "welfare_cents": _r(W), "deadweight_loss_cents": _r(L)}
