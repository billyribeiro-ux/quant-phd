"""Rung 3 check: the outcome table of the reference case a = 120, b = 1, c = 20, and of the tie case a = 121.

Standard library only (fractions, math). No randomness and no network. The inputs are those of the project
specification, not market data. Copy this file to run_report.py beside market_structure.py, and replace the call to
closed_form_outcome with a call to outcome from your market_structure module. Your module must print the same lines.
The lab prints the six outputs of each structure for two cases: the reference case, and a = 121, which makes the
monopoly fee and volume exact halves, so the tie-going-up rule decides the printed values. Every money value is rounded
once from its exact value, and volume_trades is rounded from the exact volume.
"""

from __future__ import annotations

import math
from fractions import Fraction

KEYS = (
    "volume_trades",
    "fee_cents",
    "profit_cents",
    "consumer_surplus_cents",
    "welfare_cents",
    "deadweight_loss_cents",
)


def half_up(x: Fraction) -> int:
    """The nearest whole number to a non-negative exact value, a tie going up."""
    return math.floor(x + Fraction(1, 2))


def closed_form_outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    """The six outputs of one structure, from the closed forms, each rounded once from its exact value."""
    d = Fraction(a - b * c)
    if structure == "monopoly":
        volume, fee = d / 2, Fraction(a + b * c, 2 * b)
    elif structure == "cournot":
        volume, fee = 2 * d / 3, Fraction(a + 2 * b * c, 3 * b)
    else:
        volume, fee = d, Fraction(c)
    profit = (fee - c) * volume
    consumer = volume * volume / (2 * b)
    welfare = consumer + profit
    deadweight = (d - volume) ** 2 / (2 * b)
    exact = [volume, fee, profit, consumer, welfare, deadweight]
    return {key: half_up(value) for key, value in zip(KEYS, exact, strict=True)}


def main() -> None:
    for a in (120, 121):
        print(f"case a = {a}, b = 1, c = 20")
        for structure in ("monopoly", "cournot", "bertrand"):
            result = closed_form_outcome(structure, a, 1, 20)
            print(structure, " ".join(f"{key}={result[key]}" for key in KEYS))


main()
