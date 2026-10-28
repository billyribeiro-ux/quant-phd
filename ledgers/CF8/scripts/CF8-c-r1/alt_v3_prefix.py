"""Alternative correct engine (verifier, CF8-c r1): prefix sums over sale days, read as differences of cumulative totals."""

from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction
from typing import Any

HORIZON = 13
END = 7 * HORIZON  # day 91, the last day of the horizon


def _check(case: Mapping[str, Any]) -> None:
    if case["horizon_weeks"] != HORIZON:
        raise ValueError("horizon_weeks must be 13")
    if case["revolver_commitment_cents"] < 0:
        raise ValueError("the revolver commitment must be non-negative")


class _Sales:
    """Prefix sums of one weekly flow over sale days from `floor` to day 91. upto(s) = cents of sale days <= s."""

    def __init__(self, weekly: list[int], floor: int) -> None:
        self.floor = floor
        self.prefix: list[Fraction] = []
        running = Fraction(0)
        for s in range(floor, END + 1):
            week = 1 if s < 1 else (s - 1) // 7 + 1
            running += Fraction(weekly[week - 1], 7)
            self.prefix.append(running)

    def upto(self, s: int) -> Fraction:
        return self.prefix[s - self.floor] if s >= self.floor else Fraction(0)


def _round(value: Fraction) -> int:
    return int(value + Fraction(1, 2))  # every value passed here is non-negative


def _weekly_paid(weekly: list[int], lag: int) -> list[int]:
    """Cents paid or collected in week w: sale days s with s + lag in days 7w-6 .. 7w."""
    sales = _Sales(weekly, -lag - 7)
    out = []
    for w in range(1, HORIZON + 1):
        upper = sales.upto(7 * w - lag)
        lower = sales.upto(7 * (w - 1) - lag)
        out.append(_round(upper - lower))
    return out


def _path(case: Mapping[str, Any], capped: bool) -> list[dict[str, int]]:
    got = _weekly_paid(case["weekly_sales_cents"], case["collection_lag_days"])
    paid = _weekly_paid(case["weekly_purchases_cents"], case["payment_lag_days"])
    cash = case["opening_cash_cents"]
    drawn = case["opening_drawn_cents"]
    commitment = case["revolver_commitment_cents"]
    rows: list[dict[str, int]] = []
    for w in range(HORIZON):
        out = paid[w] + case["weekly_opex_cents"][w]
        before = cash + got[w] - out
        need = max(0, case["minimum_cash_cents"] - before)
        draw = min(need, commitment - drawn) if capped else need
        repay = min(before - case["minimum_cash_cents"], drawn) if need == 0 else 0
        cash = before + draw - repay
        drawn += draw - repay
        liquidity = cash + commitment - drawn
        rows.append(
            {
                "receipts_cents": got[w],
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
    heads = [r["headroom_cents"] for r in _path(case, True)]
    best = heads.index(min(heads))  # the first occurrence is the earliest week on a tie
    return {"week": best + 1, "headroom_cents": heads[best]}


def action_cash_impact(case: Mapping[str, Any], action: str, days: int) -> int:
    _check(case)
    if action == "dso":
        lag = case["collection_lag_days"]
        sales = _Sales(case["weekly_sales_cents"], -lag - days - 7)
        # collections by day 91 with lag - days, less collections by day 91 with lag
        gained = sales.upto(END - (lag - days)) - sales.upto(END - lag)
        return _round(gained)
    if action == "dpo":
        lag = case["payment_lag_days"]
        buys = _Sales(case["weekly_purchases_cents"], -lag - days - 7)
        kept = buys.upto(END - lag) - buys.upto(END - lag - days)
        return _round(kept)
    raise ValueError("the action must be dso or dpo")
