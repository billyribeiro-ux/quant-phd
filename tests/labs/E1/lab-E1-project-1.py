"""Rung 1 worked example: the monopoly, Cournot and Bertrand outcomes of the reference case a = 120, b = 1, c = 20.

Standard library only (fractions, math). No randomness and no network. The three inputs are the reference case of the
project specification: a = 120 trades at a fee of zero, b = 1 trade per (cent per trade), c = 20 cents per trade. They
are inputs of the specification, not market data. The gap is d = a - b*c = 100. The lab computes each structure's exact
volume and fee, then profit, consumer surplus, welfare and deadweight loss as Fractions, and rounds each output once, a
tie going up. It prints the exact value and the rounded value. Expected: monopoly volume 50 trades and fee 70 cents;
Cournot volume 200/3 trades (67 after rounding) and fee 160/3 cents (53 after rounding); Bertrand volume 100 trades and
fee 20 cents. Profit is (fee - c) times volume. Consumer surplus is Q^2/(2b). Welfare is consumer surplus plus profit.
The deadweight loss is (d - Q)^2/(2b), which is zero for Bertrand. The lab prints the reference case only.
"""

from __future__ import annotations

import math
from fractions import Fraction

A = 120  # trades at a fee of zero
B = 1  # trades per (cent per trade) that the fee removes
C = 20  # cents per trade, the cost to the exchange


def half_up(x: Fraction) -> int:
    """The nearest whole number to a non-negative exact value, a tie going up."""
    return math.floor(x + Fraction(1, 2))


def volume_and_fee(structure: str) -> tuple[Fraction, Fraction]:
    """The exact volume in trades and fee in cents of one structure, from the closed forms of the specification."""
    d = Fraction(A - B * C)
    if structure == "monopoly":
        return d / 2, Fraction(A + B * C, 2 * B)
    if structure == "cournot":
        return 2 * d / 3, Fraction(A + 2 * B * C, 3 * B)
    return d, Fraction(C)


def main() -> None:
    d = A - B * C
    # Step 1. The gap d = a - b*c is the trade volume at which the fee equals the cost, the competitive benchmark.
    print(f"step 1: gap d = a - b*c = {d} trades")
    for structure in ("monopoly", "cournot", "bertrand"):
        volume, fee = volume_and_fee(structure)
        # Step 2. Profit per trade is fee minus cost, and profit is that margin times the volume.
        profit = (fee - C) * volume
        # Step 3. Consumer surplus is the area under the inverse demand (a - t)/b above the fee: Q^2/(2b).
        consumer = volume * volume / (2 * B)
        # Step 4. Welfare is consumer surplus plus profit, and the deadweight loss is the gap from the benchmark.
        welfare = consumer + profit
        deadweight = (d - volume) ** 2 / (2 * B)
        print(f"{structure}: volume {volume} trades -> {half_up(volume)}; fee {fee} cents -> {half_up(fee)}")
        print(
            f"{structure}: profit {profit} -> {half_up(profit)}; consumer surplus {consumer} -> {half_up(consumer)}; "
            f"welfare {welfare} -> {half_up(welfare)}; deadweight loss {deadweight} -> {half_up(deadweight)} cents"
        )
    # Step 5. The Bertrand fee equals the cost, so the Bertrand exchanges earn nothing, and the volume is the gap d.
    bertrand_volume, bertrand_fee = volume_and_fee("bertrand")
    print("bertrand fee equals cost:", bertrand_fee == C, "| volume equals the gap:", bertrand_volume == d)


main()
