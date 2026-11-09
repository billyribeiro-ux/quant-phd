"""Cournot volume by best-response iteration to convergence; the closed form is the stop check, outputs from closed forms."""

from fractions import Fraction
import math


def _half_up(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


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
        q_i = Fraction(0)
        for _ in range(200):
            q_next = (d - q_i) / 2  # best response of one exchange to the rival's quantity q_i
            if abs(q_next - q_i) < Fraction(1, 10**30):
                break
            q_i = q_next
        if abs(q_i - d / 3) > Fraction(1, 10**20):
            raise ArithmeticError("iteration did not converge")
        volume = 2 * d / 3  # stop condition: the iterate equals the closed form d/3 per exchange
        fee = Fraction(a + 2 * b * c, 3 * b)
        profit = (fee - c) * volume
    elif structure == "monopoly":
        volume = d / 2
        fee = Fraction(a + b * c, 2 * b)
        profit = (fee - c) * volume
    else:
        volume, fee = d, Fraction(c)
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
