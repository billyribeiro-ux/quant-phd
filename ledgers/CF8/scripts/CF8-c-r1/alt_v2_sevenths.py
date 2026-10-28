"""Alternative correct engine (verifier, CF8-c r1): all flows as integers counted in sevenths of a cent."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

HORIZON = 13


def _check(case: Mapping[str, Any]) -> None:
    if case["horizon_weeks"] != HORIZON:
        raise ValueError("the horizon must be 13 weeks")
    if case["revolver_commitment_cents"] < 0:
        raise ValueError("revolver_commitment_cents must be zero or more")


def _unit_per_day(weekly: list[int], day: int) -> int:
    """A day's flow in sevenths of a cent: a week's whole cents, spread over seven days, is the same count of sevenths."""
    week = 1 if day < 1 else (day - 1) // 7 + 1
    return weekly[week - 1]


def _cents_from_sevenths(v: int) -> int:
    """Nearest whole cent of v/7, a half going up: floor(v/7 + 1/2) = floor((2v + 7) / 14)."""
    return (2 * v + 7) // 14


def _window(weekly: list[int], lag: int, week: int) -> int:
    first = 7 * (week - 1) + 1
    return sum(_unit_per_day(weekly, d - lag) for d in range(first, first + 7))


def _path(case: Mapping[str, Any], capped: bool) -> list[dict[str, int]]:
    cash = case["opening_cash_cents"]
    drawn = case["opening_drawn_cents"]
    minimum = case["minimum_cash_cents"]
    commitment = case["revolver_commitment_cents"]
    rows: list[dict[str, int]] = []
    for week in range(1, HORIZON + 1):
        got = _cents_from_sevenths(_window(case["weekly_sales_cents"], case["collection_lag_days"], week))
        pay = _cents_from_sevenths(_window(case["weekly_purchases_cents"], case["payment_lag_days"], week))
        out = pay + case["weekly_opex_cents"][week - 1]
        before = cash + got - out
        if before < minimum:
            need = minimum - before
            draw = min(need, commitment - drawn) if capped else need
            repay = 0
        else:
            draw = 0
            repay = min(before - minimum, drawn)
        cash = before + draw - repay
        drawn += draw - repay
        liquidity = cash + commitment - drawn
        rows.append(
            {
                "receipts_cents": got,
                "disbursements_cents": out,
                "draw_cents": draw,
                "repay_cents": repay,
                "ending_cash_cents": cash,
                "drawn_balance_cents": drawn,
                "liquidity_cents": liquidity,
                "headroom_cents": liquidity - case["covenant_threshold_cents"],
            }
        )
    return rows


def forecast(case: Mapping[str, Any]) -> list[dict[str, int]]:
    _check(case)
    return _path(case, True)


def revolver_plan(case: Mapping[str, Any]) -> dict[str, int]:
    _check(case)
    capped = _path(case, True)
    free = _path(case, False)
    opening = case["opening_drawn_cents"]
    return {
        "peak_drawn_cents": max([opening] + [r["drawn_balance_cents"] for r in capped]),
        "required_commitment_cents": max([opening] + [r["drawn_balance_cents"] for r in free]),
        "shortfall_cents": max([0] + [max(case["minimum_cash_cents"] - r["ending_cash_cents"], 0) for r in capped]),
    }


def covenant_pinch(case: Mapping[str, Any]) -> dict[str, int]:
    _check(case)
    rows = _path(case, True)
    best = 0
    for i in range(1, HORIZON):
        if rows[i]["headroom_cents"] < rows[best]["headroom_cents"]:
            best = i
    return {"week": best + 1, "headroom_cents": rows[best]["headroom_cents"]}


def action_cash_impact(case: Mapping[str, Any], action: str, days: int) -> int:
    _check(case)
    end = 7 * HORIZON  # day 91
    if action == "dso":
        lag = case["collection_lag_days"]
        weekly = case["weekly_sales_cents"]
        lo, hi = end - lag + 1, end - lag + days
    elif action == "dpo":
        lag = case["payment_lag_days"]
        weekly = case["weekly_purchases_cents"]
        lo, hi = end - lag - days + 1, end - lag
    else:
        raise ValueError("action must be dso or dpo")
    return _cents_from_sevenths(sum(_unit_per_day(weekly, k) for k in range(lo, hi + 1)))
