"""Alt 2: Cournot quantity by iterating the best response to convergence, then recovered exactly."""
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

def _half_up(x):
    return int(x.numerator * 2 + x.denominator) // int(2 * x.denominator)

def _cournot_quantity_each(d):
    q = Fraction(0)
    for _ in range(400):
        nxt = max(Fraction(0), (Fraction(d) - q) / 2)
        if abs(nxt - q) < Fraction(1, 10**40):
            q = nxt
            break
        q = nxt
    return (q.limit_denominator(10**12))

def outcome(structure, a, b, c):
    _check(structure, a, b, c)
    d = a - b * c
    if structure == "monopoly":
        Q = Fraction(d, 2)
        fee = (Fraction(a) - Q) / b
    elif structure == "cournot":
        each = _cournot_quantity_each(d)
        Q = 2 * each
        fee = (Fraction(a) - Q) / b
    else:
        Q = Fraction(d)
        fee = Fraction(c)
    profit = (fee - c) * Q
    cs = Fraction(Q * Q, 2 * b)
    welfare = cs + profit
    dwl = Fraction((d - Q) ** 2, 2 * b)
    return {"volume_trades": _half_up(Q), "fee_cents": _half_up(fee), "profit_cents": _half_up(profit),
            "consumer_surplus_cents": _half_up(cs), "welfare_cents": _half_up(welfare),
            "deadweight_loss_cents": _half_up(dwl)}
