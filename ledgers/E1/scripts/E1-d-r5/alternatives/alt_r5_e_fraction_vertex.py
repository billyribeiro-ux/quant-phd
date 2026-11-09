"""Fraction throughout; each monopoly and Cournot quantity is the vertex of a quadratic profit built from its coefficients."""

from fractions import Fraction
import math


def _half_up(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def _vertex(alpha: Fraction, beta: Fraction) -> Fraction:
    # maximiser of alpha * x^2 + beta * x with alpha < 0
    return -beta / (2 * alpha)


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if not isinstance(structure, str) or structure not in ("monopoly", "cournot", "bertrand"):
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    A, B, Cc = Fraction(a), Fraction(b), Fraction(c)
    d = A - B * Cc
    if structure == "monopoly":
        # profit(Q) = -Q^2 / b + (a - b c) Q / b
        volume = _vertex(-1 / B, d / B)
        fee = (A - volume) / B
    elif structure == "cournot":
        # One exchange's profit in q_i against rival q_j is (-q_i^2 + (d - q_j) q_i) / b. Its vertex is the reaction
        # (d - q_j) / 2. At the symmetric point q = q_j = q_i, the vertex gives q = (d - q) / 2, so 3 q = d.
        q_sym = d / 3
        volume = 2 * q_sym
        fee = (A - volume) / B
    else:
        volume = d
        fee = Cc
    profit = (fee - Cc) * volume
    consumer = volume * volume / (2 * B)
    welfare = consumer + profit
    dwl = (d - volume) ** 2 / (2 * B)
    return {
        "volume_trades": _half_up(volume),
        "fee_cents": _half_up(fee),
        "profit_cents": _half_up(profit),
        "consumer_surplus_cents": _half_up(consumer),
        "welfare_cents": _half_up(welfare),
        "deadweight_loss_cents": _half_up(dwl),
    }
