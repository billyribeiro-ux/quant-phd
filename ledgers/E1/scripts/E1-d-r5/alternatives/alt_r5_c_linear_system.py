"""Cournot by solving the 2x2 linear system of the two reaction equations 2 q1 + q2 = d, q1 + 2 q2 = d (Cramer's rule)."""

from fractions import Fraction
import math


def _half_up(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def _solve_2x2(m: list[list[int]], r: list[Fraction]) -> tuple[Fraction, Fraction]:
    det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    if det == 0:
        raise ArithmeticError("singular system")
    x = (r[0] * m[1][1] - m[0][1] * r[1]) / det
    y = (m[0][0] * r[1] - r[0] * m[1][0]) / det
    return x, y


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if not isinstance(structure, str) or structure not in ("monopoly", "cournot", "bertrand"):
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    d = Fraction(a - b * c)
    if structure == "cournot":
        q1, q2 = _solve_2x2([[2, 1], [1, 2]], [d, d])
        volume = q1 + q2
        fee = (a - volume) / b
        profit = (fee - c) * volume
    elif structure == "monopoly":
        volume = Fraction(a - b * c, 2)  # first-order condition a - b c - 2Q = 0
        fee = (a - volume) / b
        profit = (fee - c) * volume
    else:
        volume = d
        fee = (a - volume) / b
        profit = (fee - c) * volume
    consumer = volume * volume / (2 * b)
    welfare = consumer + profit
    dwl = (d - volume) ** 2 / (2 * b)
    return {
        "volume_trades": _half_up(volume),
        "fee_cents": _half_up(fee),
        "profit_cents": _half_up(profit),
        "consumer_surplus_cents": _half_up(consumer),
        "welfare_cents": _half_up(welfare),
        "deadweight_loss_cents": _half_up(dwl),
    }
