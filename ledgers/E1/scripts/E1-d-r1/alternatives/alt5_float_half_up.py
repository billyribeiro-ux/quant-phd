"""Alt 5: float arithmetic, with the same half-up rule applied to each float value."""
import math
STRUCTURES = ("monopoly", "cournot", "bertrand")

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
    return math.floor(x + 0.5)

def outcome(structure, a, b, c):
    _check(structure, a, b, c)
    d = (a - b * c) * 1.0
    if structure == "monopoly":
        Q, f = d / 2, (a + b * c) / (2 * b)
    elif structure == "cournot":
        Q, f = 2 * d / 3, (a + 2 * b * c) / (3 * b)
    else:
        Q, f = d, float(c)
    pi = (f - c) * Q
    cs = Q * Q / (2 * b)
    W = cs + pi
    L = (d - Q) ** 2 / (2 * b)
    return {"volume_trades": _r(Q), "fee_cents": _r(f), "profit_cents": _r(pi),
            "consumer_surplus_cents": _r(cs), "welfare_cents": _r(W), "deadweight_loss_cents": _r(L)}
