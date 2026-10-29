"""Alternative 6: all arithmetic in integers of 1/7 cent; each money output is (2X + 7) // 14 for X sevenths."""

from __future__ import annotations

from typing import Any

HORIZON = 13


def _check(case: dict[str, Any]) -> None:
    if case["horizon_weeks"] != HORIZON:
        raise ValueError("horizon must be 13 weeks")
    if case["revolver_commitment_cents"] < 0:
        raise ValueError("commitment must be non-negative")


def _day_units(weekly: list[int], day: int) -> int:
    # a day's flow is weekly/7 cents = weekly sevenths-of-a-cent units of 1/7 cent? no: weekly/7 cents == weekly units of 1/7 cent
    week = 1 if day < 1 else (day - 1) // 7 + 1
    return weekly[week - 1]


def _sevenths_in_week(weekly: list[int], lag: int, week: int) -> int:
    first = 7 * (week - 1) + 1
    return sum(_day_units(weekly, d - lag) for d in range(first, first + 7))


def _cents(sevenths: int) -> int:
    return (2 * sevenths + 7) // 14  # sevenths/7 cents, rounded half up


def _path(case: dict[str, Any], capped: bool) -> list[dict[str, int]]:
    cash = case["opening_cash_cents"]
    drawn = case["opening_drawn_cents"]
    commit = case["revolver_commitment_cents"]
    rows: list[dict[str, int]] = []
    for w in range(1, HORIZON + 1):
        got = _cents(_sevenths_in_week(case["weekly_sales_cents"], case["collection_lag_days"], w))
        out = _cents(_sevenths_in_week(case["weekly_purchases_cents"], case["payment_lag_days"], w))
        out += case["weekly_opex_cents"][w - 1]
        before = cash + got - out
        if before < case["minimum_cash_cents"]:
            need = case["minimum_cash_cents"] - before
            draw = min(need, commit - drawn) if capped else need
            repay = 0
        else:
            draw = 0
            repay = min(before - case["minimum_cash_cents"], drawn)
        cash = before + draw - repay
        drawn += draw - repay
        liq = cash + commit - drawn
        rows.append(
            {
                "receipts_cents": got,
                "disbursements_cents": out,
                "draw_cents": draw,
                "repay_cents": repay,
                "ending_cash_cents": cash,
                "drawn_balance_cents": drawn,
                "liquidity_cents": liq,
                "headroom_cents": liq - case["covenant_threshold_cents"],
            }
        )
    return rows


def forecast(case: dict[str, Any]) -> list[dict[str, int]]:
    _check(case)
    return _path(case, True)


def revolver_plan(case: dict[str, Any]) -> dict[str, int]:
    _check(case)
    rows = _path(case, True)
    free = _path(case, False)
    peak = max([case["opening_drawn_cents"]] + [r["drawn_balance_cents"] for r in rows])
    required = max([case["opening_drawn_cents"]] + [r["drawn_balance_cents"] for r in free])
    short = max([0] + [max(0, case["minimum_cash_cents"] - r["ending_cash_cents"]) for r in rows])
    return {"peak_drawn_cents": peak, "required_commitment_cents": required, "shortfall_cents": short}


def covenant_pinch(case: dict[str, Any]) -> dict[str, int]:
    _check(case)
    rows = _path(case, True)
    order = sorted(range(HORIZON), key=lambda i: (rows[i]["headroom_cents"], i))
    i = order[0]
    return {"week": i + 1, "headroom_cents": rows[i]["headroom_cents"]}


def _window_sum(weekly: list[int], lo: int, hi: int) -> int:
    return sum(_day_units(weekly, k) for k in range(lo, hi + 1))


def action_cash_impact(case: dict[str, Any], action: str, days: int) -> int:
    _check(case)
    if action == "dso":
        lag = case["collection_lag_days"]
        if days < 0 or days > lag:
            raise ValueError("DSO change out of range")
        return _cents(_window_sum(case["weekly_sales_cents"], 92 - lag, 91 - lag + days))
    if action == "dpo":
        if days < 0:
            raise ValueError("DPO change must be non-negative")
        lag = case["payment_lag_days"]
        return _cents(_window_sum(case["weekly_purchases_cents"], 92 - lag - days, 91 - lag))
    raise ValueError("action must be dso or dpo")
