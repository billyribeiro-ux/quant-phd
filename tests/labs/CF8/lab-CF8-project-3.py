"""CF8 project lab 3 (rung 3, reference run): the outcome table of a second SIMULATED case, to check your engine.

SIMULATED: a case written here for teaching. It is not any company's data. Money is in whole cents on input; the
printed values are dollars to two decimals. Standard library only, no randomness, no network.

Run treasury_forecast.py on exactly this case (the dict CASE below, with the same keys) and compare the printed
lines with your engine's output, after dividing money by 100. A line that differs is a defect in one of the two. The
printed numbers are a check, not a target to copy.

The case is stressed: sales fall from week 6, receipts follow after the 30-day collection lag, the commitment binds
in week 13 only, and the shortfall below minimum cash is reported.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any

CASE: dict[str, Any] = {
    "horizon_weeks": 13,
    "opening_cash_cents": 100_000,
    "minimum_cash_cents": 300_000,
    "revolver_commitment_cents": 800_000,
    "opening_drawn_cents": 200_000,
    "covenant_threshold_cents": 400_000,
    "collection_lag_days": 30,
    "payment_lag_days": 20,
    "weekly_sales_cents": [1_000_000] * 5 + [700_000] * 8,
    "weekly_purchases_cents": [700_000] * 13,
    "weekly_opex_cents": [250_000] * 13,
}


def daily(weekly: list[int], day: int) -> Fraction:
    """Cents of one day's flow; the days before day 1 use week 1's rate, as the specification states."""
    week = 1 if day < 1 else (day - 1) // 7 + 1
    return Fraction(weekly[week - 1], 7)


def week_total(weekly: list[int], lag: int, week: int) -> Fraction:
    first = 7 * (week - 1) + 1
    return sum((daily(weekly, day - lag) for day in range(first, first + 7)), Fraction(0))


def half_up(value: Fraction) -> int:
    return math.floor(value + Fraction(1, 2))


def path(capped: bool) -> list[tuple[int, int, int, int, int, int, int, int]]:
    """Week rows: receipts, disbursements, draw, repay, ending cash, drawn, liquidity, headroom, in cents."""
    rows = []
    cash = CASE["opening_cash_cents"]
    drawn = CASE["opening_drawn_cents"]
    for w in range(1, 14):
        got = half_up(week_total(CASE["weekly_sales_cents"], CASE["collection_lag_days"], w))
        out = half_up(week_total(CASE["weekly_purchases_cents"], CASE["payment_lag_days"], w))
        out += CASE["weekly_opex_cents"][w - 1]
        before = cash + got - out
        need = max(CASE["minimum_cash_cents"] - before, 0)
        room = CASE["revolver_commitment_cents"] - drawn
        draw = min(need, room) if capped else need
        repay = 0 if need > 0 else min(before - CASE["minimum_cash_cents"], drawn)
        cash = before + draw - repay
        drawn = drawn + draw - repay
        liquidity = cash + CASE["revolver_commitment_cents"] - drawn
        rows.append((got, out, draw, repay, cash, drawn, liquidity, liquidity - CASE["covenant_threshold_cents"]))
    return rows


def usd(cents: int) -> str:
    return f"{cents / 100:.2f}"


def cumulative(weekly: list[int], lag: int) -> Fraction:
    """Cents of the sales of days -300 to 91 - lag, each sale collected lag days after its day.

    The sum starts at day -300, so it is not the total flow by day 91. Two calls that differ only in lag share the
    same start, and their difference is the flow in the days between the two lags.
    """
    return sum((daily(weekly, k) for k in range(-300, 92 - lag)), Fraction(0))


def main() -> None:
    capped = path(capped=True)
    free = path(capped=False)
    print("week: receipts, disbursements, draw, repay, ending cash, drawn, headroom (dollars)")
    for w, row in enumerate(capped, start=1):
        print(f"  week {w:2d}: " + "  ".join(usd(x) for x in row[:4]) + "  " + "  ".join(usd(x) for x in row[4:]))
    peak = max([CASE["opening_drawn_cents"]] + [row[5] for row in capped])
    required = max([CASE["opening_drawn_cents"]] + [row[5] for row in free])
    shortfall = max([0] + [max(CASE["minimum_cash_cents"] - row[4], 0) for row in capped])
    print(f"peak drawn balance: {usd(peak)} dollars")
    print(f"required commitment: {usd(required)} dollars, against {usd(CASE['revolver_commitment_cents'])} in the case")
    print(f"largest shortfall below minimum cash: {usd(shortfall)} dollars")
    pinch = min(range(13), key=lambda i: (capped[i][7], i))
    print(f"covenant pinch: week {pinch + 1}, headroom {usd(capped[pinch][7])} dollars")
    lag = CASE["collection_lag_days"]
    dso = half_up(cumulative(CASE["weekly_sales_cents"], lag - 5) - cumulative(CASE["weekly_sales_cents"], lag))
    lag = CASE["payment_lag_days"]
    dpo = half_up(cumulative(CASE["weekly_purchases_cents"], lag) - cumulative(CASE["weekly_purchases_cents"], lag + 5))
    print(f"cash impact of a 5-day DSO shortening: {usd(dso)} dollars")
    print(f"cash impact of a 5-day DPO lengthening: {usd(dpo)} dollars")


main()
