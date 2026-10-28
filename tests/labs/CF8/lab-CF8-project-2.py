"""CF8 project lab 2 (rung 2, completion): the revolver draw line of the rung-1 case.

SIMULATED: the same case as lab 1, written here for teaching. It is not any company's data. Money is in whole cents;
the printed values are dollars to two decimals. Standard library only, no randomness, no network.

Replace the one blank, ___, with the expression for the revolver draw. The rule: if cash before the draw is below
minimum cash, draw the shortfall, but no more than the undrawn availability. Every other line is given. When the blank
is right, the output matches the expected output below exactly.
"""

from __future__ import annotations

import math
from fractions import Fraction

COLLECTION_LAG = 45  # days
PAYMENT_LAG = 30  # days
SALES = [1_000_000] * 3 + [800_000] * 10  # cents of sales in weeks 1 to 13
PURCHASES = [700_000] * 13  # cents of purchases in weeks 1 to 13
OPEX = [250_000] * 13  # cents of operating cost in weeks 1 to 13
OPENING_CASH = 150_000
MINIMUM_CASH = 400_000
COMMITMENT = 1_000_000
OPENING_DRAWN = 0
THRESHOLD = 1_200_000


def usd(cents: int) -> str:
    return f"{cents / 100:.2f}"


def daily(weekly: list[int], day: int) -> Fraction:
    week = 1 if day < 1 else (day - 1) // 7 + 1
    return Fraction(weekly[week - 1], 7)


def week_total(weekly: list[int], lag: int, week: int) -> Fraction:
    first = 7 * (week - 1) + 1
    return sum((daily(weekly, day - lag) for day in range(first, first + 7)), Fraction(0))


def half_up(value: Fraction) -> int:
    return math.floor(value + Fraction(1, 2))


def main() -> None:
    cash, drawn = OPENING_CASH, OPENING_DRAWN
    lowest = THRESHOLD
    for w in range(1, 14):
        receipts = half_up(week_total(SALES, COLLECTION_LAG, w))
        disbursements = half_up(week_total(PURCHASES, PAYMENT_LAG, w) + OPEX[w - 1])
        before = cash + receipts - disbursements
        draw = min(max(MINIMUM_CASH - before, 0), COMMITMENT - drawn)
        repay = 0 if draw > 0 else min(max(before - MINIMUM_CASH, 0), drawn)
        cash = before + draw - repay
        drawn = drawn + draw - repay
        headroom = cash + COMMITMENT - drawn - THRESHOLD
        lowest = min(lowest, headroom)
        print(
            f"week {w:2d}: draw {usd(draw)}, repay {usd(repay)}, ending cash {usd(cash)}, "
            f"drawn {usd(drawn)}, headroom {usd(headroom)} dollars"
        )
    print(f"lowest headroom over the horizon: {usd(lowest)} dollars")


main()
