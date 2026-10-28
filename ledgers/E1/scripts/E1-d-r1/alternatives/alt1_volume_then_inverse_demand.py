"""Alt 1: volume first, fee from the inverse demand at that volume, rounding by integer arithmetic."""
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

def _round(x):
    n, dd = x.numerator, x.denominator
    return (2 * n + dd) // (2 * dd)

def outcome(structure, a, b, c):
    _check(structure, a, b, c)
    d = a - b * c
    if structure == "monopoly":
        q = Fraction(d, 2)
    elif structure == "cournot":
        q = Fraction(2 * d, 3)
    else:
        q = Fraction(d)
    fee = (Fraction(a) - q) / b
    gross = Fraction(a) * q / b - q * q / (2 * b)
    cs = Fraction(q * q, 2 * b)
    profit = (fee - c) * q
    welfare = gross - c * q
    dwl = Fraction((d - q) ** 2, 2 * b)
    return {"volume_trades": _round(q), "fee_cents": _round(fee), "profit_cents": _round(profit),
            "consumer_surplus_cents": _round(cs), "welfare_cents": _round(welfare),
            "deadweight_loss_cents": _round(dwl)}
