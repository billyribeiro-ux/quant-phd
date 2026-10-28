"""Alt 3: first-order conditions written as linear systems and solved by Gaussian elimination in Fractions."""
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

def _solve(M, v):
    n = len(v)
    A = [[Fraction(x) for x in row] + [Fraction(v[i])] for i, row in enumerate(M)]
    for col in range(n):
        piv = next(r for r in range(col, n) if A[r][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        for r in range(n):
            if r != col and A[r][col] != 0:
                f = A[r][col] / A[col][col]
                A[r] = [x - f * y for x, y in zip(A[r], A[col])]
    return [A[i][n] / A[i][i] for i in range(n)]

def _half_up(x):
    import math
    return math.floor(x + Fraction(1, 2))

def outcome(structure, a, b, c):
    _check(structure, a, b, c)
    if structure == "monopoly":
        # d/dQ of ((a - Q)/b - c) Q = 0  ->  2 Q = a - b c   (one unknown)
        (Q,) = _solve([[2]], [a - b * c])
    elif structure == "cournot":
        # 2 q1 + q2 = d ; q1 + 2 q2 = d  (symmetric FOCs of the two exchanges)
        d = a - b * c
        q1, q2 = _solve([[2, 1], [1, 2]], [d, d])
        Q = q1 + q2
    else:
        # fee equals the cost: the unknown is the volume at fee c, Q = a - b c
        (Q,) = _solve([[1]], [a - b * c])
    fee = (Fraction(a) - Q) / b
    profit = (fee - c) * Q
    cs = Q * Q / (2 * b)
    welfare = cs + profit
    d = Fraction(a - b * c)
    dwl = (d - Q) ** 2 / (2 * b)
    return {"volume_trades": _half_up(Q), "fee_cents": _half_up(fee), "profit_cents": _half_up(profit),
            "consumer_surplus_cents": _half_up(cs), "welfare_cents": _half_up(welfare),
            "deadweight_loss_cents": _half_up(dwl)}
