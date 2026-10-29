"""CF8 project lab 1 (rung 1, worked example): a 13-week forecast with a revolver on a SIMULATED stressed case.

SIMULATED: a manufacturer case written here for teaching. It is not any company's data. Money is in whole cents; the
printed values, daily rates included, are dollars to two decimals. Standard library only, no randomness, no
network. The rules are those of the specification on the project page:

* a week has seven days, and a day's sales are collected collection_lag days after the sale;
* a day's purchases are paid payment_lag days after the purchase, and opex is paid in its week;
* before day 1 the daily rate of sales and purchases is week 1's rate (the run-rate before the horizon);
* if cash before a draw is below minimum cash, the revolver draws the shortfall, capped at availability;
* if cash before a draw is at or above minimum cash, the revolver repays from the cash above minimum, capped at the
  drawn balance;
* liquidity is cash plus undrawn availability; headroom is liquidity minus the covenant threshold.
"""

from __future__ import annotations

import math
from fractions import Fraction

COLLECTION_LAG = 45  # days: the collection lag, the days of sales a steady business holds as receivables
PAYMENT_LAG = 30  # days
SALES = [1_000_000] * 3 + [800_000] * 10  # cents of sales in weeks 1 to 13: a slowdown from week 4
PURCHASES = [700_000] * 13  # cents of purchases in weeks 1 to 13
OPEX = [250_000] * 13  # cents of operating cost paid in weeks 1 to 13
OPENING_CASH = 150_000
MINIMUM_CASH = 400_000
COMMITMENT = 1_000_000
OPENING_DRAWN = 0
THRESHOLD = 1_200_000


def usd(cents: int) -> str:
    """Cents shown as dollars with two decimals."""
    return f"{cents / 100:.2f}"


def daily(weekly: list[int], day: int) -> Fraction:
    """Cents of one day's flow on day `day`: a week's amount spread over its seven days, week 1's rate before day 1."""
    week = 1 if day < 1 else (day - 1) // 7 + 1
    return Fraction(weekly[week - 1], 7)


def week_total(weekly: list[int], lag: int, week: int) -> Fraction:
    """Exact cents paid or collected in `week` when each day's flow falls `lag` days after it is due."""
    first = 7 * (week - 1) + 1
    return sum((daily(weekly, day - lag) for day in range(first, first + 7)), Fraction(0))


def half_up(value: Fraction) -> int:
    """The exact value rounded once to the nearest cent, a half going up."""
    return math.floor(value + Fraction(1, 2))


def main() -> None:
    print(f"step 1, the run-rate before week 1: sales {usd(SALES[0])} a week, {SALES[0] / 7 / 100:.2f} a day")
    print(f"step 2, the collection lag is {COLLECTION_LAG} days and the payment lag is {PAYMENT_LAG} days")
    receipts = [half_up(week_total(SALES, COLLECTION_LAG, w)) for w in range(1, 14)]
    disbursements = [half_up(week_total(PURCHASES, PAYMENT_LAG, w) + OPEX[w - 1]) for w in range(1, 14)]
    print("step 3, receipts in dollars, weeks 1 to 13:", ", ".join(usd(x) for x in receipts))
    print("step 4, disbursements in dollars, weeks 1 to 13:", ", ".join(usd(x) for x in disbursements))
    cash, drawn = OPENING_CASH, OPENING_DRAWN
    print("step 5, week by week: receipts, disbursements, draw, repay, ending cash, drawn, headroom (dollars)")
    rows: list[tuple[int, int, int, int, int, int, int]] = []
    for w in range(13):
        before = cash + receipts[w] - disbursements[w]
        draw = min(max(MINIMUM_CASH - before, 0), COMMITMENT - drawn)
        repay = 0 if draw > 0 else min(max(before - MINIMUM_CASH, 0), drawn)
        new_cash = before + draw - repay
        new_drawn = drawn + draw - repay
        liquidity = new_cash + COMMITMENT - new_drawn
        headroom = liquidity - THRESHOLD
        rows.append((receipts[w], disbursements[w], draw, repay, new_cash, new_drawn, headroom))
        print(
            f"  week {w + 1:2d}: {usd(receipts[w])}  {usd(disbursements[w])}  {usd(draw)}  {usd(repay)}  "
            f"{usd(new_cash)}  {usd(new_drawn)}  {usd(headroom)}"
        )
        cash, drawn = new_cash, new_drawn
    draws, repays = sum(row[2] for row in rows), sum(row[3] for row in rows)
    closing_check = OPENING_CASH + sum(receipts) - sum(disbursements) + draws - repays
    print(f"step 6, opening cash plus the horizon's flows equals week 13 ending cash: {closing_check == cash}")
    peak = max([OPENING_DRAWN] + [row[5] for row in rows])
    print(f"step 7, peak drawn balance: {usd(peak)} dollars")
    pinch = min(range(13), key=lambda i: (rows[i][6], i))
    print(f"step 8, covenant pinch: week {pinch + 1}, headroom {usd(rows[pinch][6])} dollars")
    lowest = min(row[4] for row in rows)
    print(f"step 9, lowest week-end cash: {usd(lowest)} dollars, against minimum cash of {usd(MINIMUM_CASH)}")


main()
