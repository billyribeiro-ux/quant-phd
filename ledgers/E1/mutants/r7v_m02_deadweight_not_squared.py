"""Student writes the deadweight loss as the linear gap (d - Q)/(2b), dropping the square of the triangle.

Standard library only. Every quantity is an exact fractions.Fraction. Each output is rounded once, to the nearest
whole unit, with a tie going up: half_up(x) = floor(x + 1/2). The money outputs are in cents. volume_trades is in
whole trades.
No money output uses a rounded volume: the deadweight loss and the consumer surplus are taken from the exact volume.

Inputs: a, b, c, integers with a > b*c > 0. a is in trades, b in trades per (cent per trade), c in cents per trade. The
gap is d = a - b*c. The structures are the monopoly, two exchanges competing on quantity (Cournot), and two exchanges
competing on fee (Bertrand).
"""

from __future__ import annotations

import math
from fractions import Fraction

STRUCTURES: tuple[str, ...] = ("monopoly", "cournot", "bertrand")


def half_up(x: Fraction) -> int:
    """The nearest whole number to a non-negative exact value, a tie going up."""
    return math.floor(x + Fraction(1, 2))


def check_inputs(structure: str, a: int, b: int, c: int) -> None:
    """Raise ValueError naming the condition the inputs violate, in the order the specification lists them."""
    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    """Trade volume, fee, exchange profit, consumer surplus, welfare and deadweight loss of one market structure.

    Money keys are in cents and each is rounded once from its exact value. volume_trades is rounded from the exact
    volume. The keys are exactly volume_trades, fee_cents, profit_cents, consumer_surplus_cents, welfare_cents and
    deadweight_loss_cents, and every value is an int.
    """
    check_inputs(structure, a, b, c)
    d = Fraction(a - b * c)
    if structure == "monopoly":
        volume = d / 2
        fee = Fraction(a + b * c, 2 * b)
    elif structure == "cournot":
        volume = 2 * d / 3
        fee = Fraction(a + 2 * b * c, 3 * b)
    else:
        volume = d
        fee = Fraction(c)
    profit = (fee - c) * volume
    consumer = volume * volume / (2 * b)
    welfare = consumer + profit
    deadweight = (d - volume) / (2 * b)
    return {
        "volume_trades": half_up(volume),
        "fee_cents": half_up(fee),
        "profit_cents": half_up(profit),
        "consumer_surplus_cents": half_up(consumer),
        "welfare_cents": half_up(welfare),
        "deadweight_loss_cents": half_up(deadweight),
    }
