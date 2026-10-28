"""One-week lookahead: week w collects the receipts of week w + 1.

Standard library only. Money is whole cents on input and on output. Every money output is computed from exact
Fractions and rounded once, half up, to the nearest cent. This file is the instructor's solution. It is excluded
from publication; the suite never imports it.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from fractions import Fraction
from typing import Any

HORIZON = 13
DAYS_PER_WEEK = 7
MONEY_KEYS = ("receipts_cents", "disbursements_cents", "draw_cents", "repay_cents")
ROW_KEYS = (
    "receipts_cents",
    "disbursements_cents",
    "draw_cents",
    "repay_cents",
    "ending_cash_cents",
    "drawn_balance_cents",
    "liquidity_cents",
    "headroom_cents",
)


def _half_up(value: Fraction) -> int:
    return math.floor(value + Fraction(1, 2))


def _check_case(case: Mapping[str, Any]) -> None:
    if case["horizon_weeks"] != HORIZON:
        raise ValueError("the forecast covers the 13-week horizon: horizon_weeks must be 13")
    if case["revolver_commitment_cents"] < 0:
        raise ValueError("the commitment must be non-negative: a revolver cannot have a negative commitment")


def _daily_rate(weekly: list[int], day: int) -> Fraction:
    """Cents per day of a flow on day `day`: weekly[w - 1] / 7 for days in week w; week 1's rate before day 1."""
    week = 1 if day < 1 else (day - 1) // DAYS_PER_WEEK + 1
    return Fraction(weekly[week - 1], DAYS_PER_WEEK)


def _week_total(weekly: list[int], lag_days: int, week: int) -> Fraction:
    """Exact cents of a flow that is paid or collected lag_days after it falls due, in week `week` (1 to 13)."""
    first = DAYS_PER_WEEK * (week - 1) + 1
    return sum((_daily_rate(weekly, day - lag_days) for day in range(first, first + DAYS_PER_WEEK)), Fraction(0))


def _receipts(case: Mapping[str, Any], week: int) -> Fraction:
    return _week_total(case["weekly_sales_cents"], case["collection_lag_days"], week)


def _disbursements(case: Mapping[str, Any], week: int) -> Fraction:
    purchases = _week_total(case["weekly_purchases_cents"], case["payment_lag_days"], week)
    return purchases + case["weekly_opex_cents"][week - 1]


def _path(case: Mapping[str, Any], capped: bool) -> list[dict[str, int]]:
    """Week-by-week cash and revolver path. capped=False lets the draw exceed availability (for the required size)."""
    minimum = case["minimum_cash_cents"]
    commitment = case["revolver_commitment_cents"]
    threshold = case["covenant_threshold_cents"]
    cash = case["opening_cash_cents"]
    drawn = case["opening_drawn_cents"]
    rows: list[dict[str, int]] = []
    for week in range(1, HORIZON + 1):
        receipts = _half_up(_receipts(case, min(week + 1, HORIZON)))
        disbursements = _half_up(_disbursements(case, week))
        before = cash + receipts - disbursements
        if before < minimum:
            need = minimum - before
            draw = min(need, commitment - drawn) if capped else need
            repay = 0
        else:
            draw = 0
            repay = min(before - minimum, drawn)
        cash = before + draw - repay
        drawn = drawn + draw - repay
        liquidity = cash + commitment - drawn
        rows.append(
            {
                "receipts_cents": receipts,
                "disbursements_cents": disbursements,
                "draw_cents": draw,
                "repay_cents": repay,
                "ending_cash_cents": cash,
                "drawn_balance_cents": drawn,
                "liquidity_cents": liquidity,
                "headroom_cents": liquidity - threshold,
            }
        )
    return rows


def forecast(case: Mapping[str, Any]) -> list[dict[str, int]]:
    """Thirteen weekly rows of the capped revolver forecast, in cents."""
    _check_case(case)
    return _path(case, capped=True)


def revolver_plan(case: Mapping[str, Any]) -> dict[str, int]:
    """Peak drawn balance, required commitment (the uncapped peak) and the largest shortfall below minimum cash."""
    _check_case(case)
    rows = _path(case, capped=True)
    peak = max([case["opening_drawn_cents"]] + [row["drawn_balance_cents"] for row in rows])
    uncapped = _path(case, capped=False)
    required = max([case["opening_drawn_cents"]] + [row["drawn_balance_cents"] for row in uncapped])
    minimum = case["minimum_cash_cents"]
    shortfall = max([0] + [max(0, minimum - row["ending_cash_cents"]) for row in rows])
    return {"peak_drawn_cents": peak, "required_commitment_cents": required, "shortfall_cents": shortfall}


def covenant_pinch(case: Mapping[str, Any]) -> dict[str, int]:
    """The week (1 to 13) with the smallest covenant headroom, earliest on a tie, and that headroom in cents."""
    _check_case(case)
    rows = _path(case, capped=True)
    best = min(range(HORIZON), key=lambda i: (rows[i]["headroom_cents"], i))
    return {"week": best + 1, "headroom_cents": rows[best]["headroom_cents"]}


def action_cash_impact(case: Mapping[str, Any], action: str, days: int) -> int:
    """Change in cumulative cash by the end of week 13, in cents, from a DSO or DPO change of `days` days.

    Collections through day 91 are the sales of days up to 91 - lag. Shortening DSO by `days` moves the sales of
    days 91 - lag + 1 to 91 - lag + days into the horizon's collections; those are the cents gained. Lengthening DPO
    by `days` postpones the purchases of days 91 - lag - days + 1 to 91 - lag, which are the cents kept. Flows that
    move before week 1 are included, because they change the cash position at the end of week 13.
    """
    _check_case(case)
    if action == "dso":
        lag = case["collection_lag_days"]
        if not 0 <= days <= lag:
            raise ValueError("a DSO change must be from 0 up to the current collection lag")
        sales = case["weekly_sales_cents"]
        window = range(DAYS_PER_WEEK * HORIZON - lag + 1, DAYS_PER_WEEK * HORIZON - lag + days + 1)
        return _half_up(sum((_daily_rate(sales, k) for k in window), Fraction(0)))
    if action == "dpo":
        if days < 0:
            raise ValueError("a DPO change must be zero or more days")
        lag = case["payment_lag_days"]
        purchases = case["weekly_purchases_cents"]
        window = range(DAYS_PER_WEEK * HORIZON - lag - days + 1, DAYS_PER_WEEK * HORIZON - lag + 1)
        return _half_up(sum((_daily_rate(purchases, k) for k in window), Fraction(0)))
    raise ValueError("the action must be one of the allowed action names: dso or dpo")
