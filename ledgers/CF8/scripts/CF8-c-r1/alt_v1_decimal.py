"""Alternative correct engine (verifier, CF8-c r1): Decimal arithmetic at 40 significant digits, ROUND_HALF_UP to cents."""

from __future__ import annotations

from collections.abc import Mapping
from decimal import ROUND_HALF_UP, Decimal, localcontext
from typing import Any

DAYS = 7
HORIZON = 13


def _check(case: Mapping[str, Any]) -> None:
    if case["horizon_weeks"] != HORIZON:
        raise ValueError("horizon_weeks must be 13")
    if case["revolver_commitment_cents"] < 0:
        raise ValueError("a revolver commitment cannot be negative")


def _rate(weekly: list[int], day: int) -> Decimal:
    week = 1 if day < 1 else (day - 1) // DAYS + 1
    return Decimal(weekly[week - 1]) / Decimal(DAYS)


def _span(weekly: list[int], lag: int, week: int) -> Decimal:
    first = DAYS * (week - 1) + 1
    total = Decimal(0)
    for day in range(first, first + DAYS):
        total += _rate(weekly, day - lag)
    return total


def _cents(value: Decimal) -> int:
    return int(value.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def _path(case: Mapping[str, Any], capped: bool) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    cash = int(case["opening_cash_cents"])
    drawn = int(case["opening_drawn_cents"])
    minimum = int(case["minimum_cash_cents"])
    commitment = int(case["revolver_commitment_cents"])
    threshold = int(case["covenant_threshold_cents"])
    with localcontext() as ctx:
        ctx.prec = 40
        for week in range(1, HORIZON + 1):
            got = _cents(_span(case["weekly_sales_cents"], int(case["collection_lag_days"]), week))
            paid = _span(case["weekly_purchases_cents"], int(case["payment_lag_days"]), week)
            out = _cents(paid) + int(case["weekly_opex_cents"][week - 1])
            before = cash + got - out
            need = max(minimum - before, 0)
            avail = commitment - drawn
            draw = (min(need, avail) if capped else need) if need > 0 else 0
            repay = 0 if need > 0 else min(before - minimum, drawn)
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
                    "headroom_cents": liquidity - threshold,
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
    opening = int(case["opening_drawn_cents"])
    minimum = int(case["minimum_cash_cents"])
    return {
        "peak_drawn_cents": max([opening] + [r["drawn_balance_cents"] for r in capped]),
        "required_commitment_cents": max([opening] + [r["drawn_balance_cents"] for r in free]),
        "shortfall_cents": max([0] + [max(minimum - r["ending_cash_cents"], 0) for r in capped]),
    }


def covenant_pinch(case: Mapping[str, Any]) -> dict[str, int]:
    _check(case)
    rows = _path(case, True)
    week, row = min(enumerate(rows, start=1), key=lambda t: (t[1]["headroom_cents"], t[0]))
    return {"week": week, "headroom_cents": row["headroom_cents"]}


def action_cash_impact(case: Mapping[str, Any], action: str, days: int) -> int:
    _check(case)
    if action not in ("dso", "dpo"):
        raise ValueError("action must be dso or dpo")
    with localcontext() as ctx:
        ctx.prec = 40
        if action == "dso":
            lag = int(case["collection_lag_days"])
            weekly = case["weekly_sales_cents"]
            window = range(HORIZON * DAYS - lag + 1, HORIZON * DAYS - lag + days + 1)
        else:
            lag = int(case["payment_lag_days"])
            weekly = case["weekly_purchases_cents"]
            window = range(HORIZON * DAYS - lag - days + 1, HORIZON * DAYS - lag + 1)
        total = Decimal(0)
        for k in window:
            total += _rate(weekly, k)
    return _cents(total)
