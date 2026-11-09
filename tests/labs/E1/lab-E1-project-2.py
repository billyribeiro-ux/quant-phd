"""Rung 2 completed solution: the Cournot best quantity iterated to the symmetric quantity, and the welfare line.

Standard library only (fractions, math). No randomness and no network. The reference case is a = 120, b = 1, c = 20,
so the gap is d = a - b*c = 100. The best quantity of one exchange against its rival's quantity q is q_i = (d -
q_j)/2, the solution of the first-order condition of its profit ((a - Q)/b - c) q_i. Starting from zero, the iteration
converges to the symmetric quantity d/3 for each exchange, so the volume is 2d/3 = 200/3 trades. The lab prints whether
the gap from d/3 after 60 steps is below 10^-12, and prints the volume, the fee and the welfare of the Cournot market.
The welfare is the gross value (a Q - Q^2/2)/b less the cost c Q, rounded once, a tie going up.
"""

from __future__ import annotations

import math
from fractions import Fraction

A = 120  # trades at a fee of zero
B = 1  # trades per (cent per trade)
C = 20  # cents per trade


def half_up(x: Fraction) -> int:
    """The nearest whole number to a non-negative exact value, a tie going up."""
    return math.floor(x + Fraction(1, 2))


def reaction(d: Fraction, rival: Fraction) -> Fraction:
    """The best quantity of one exchange against a rival quantity: q_i = (d - q_j) / 2, in trades."""
    return (d - rival) / 2


def welfare_cents(volume: Fraction, a: int, b: int, c: int) -> int:
    """Total surplus at a volume in trades: the gross value (a Q - Q^2/2)/b less the cost c Q, rounded once."""
    return half_up((a * volume - volume * volume / 2) / b - c * volume)


def main() -> None:
    d = Fraction(A - B * C)
    q = Fraction(0)
    for _ in range(60):
        q = reaction(d, q)
    print("gap from d/3 after 60 steps is below 10^-12:", abs(q - d / 3) < Fraction(1, 10**12))
    volume = 2 * d / 3
    print("Cournot volume in trades, rounded:", half_up(volume))
    print("Cournot fee in cents, rounded:", half_up((A - volume) / B))
    print("Cournot welfare in cents, rounded:", welfare_cents(volume, A, B, C))


main()
