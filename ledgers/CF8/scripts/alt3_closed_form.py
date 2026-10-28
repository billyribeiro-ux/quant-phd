"""Alternative 3: closed-form draw and repayment per week, with the cumulative path written as running sums."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

HALF = Fraction(1, 2)


def _rnd(x: Fraction) -> int:
    return (x + HALF).__floor__()


def _daily(weekly: list[int], day: int) -> Fraction:
    return Fraction(weekly[0], 7) if day <= 0 else Fraction(weekly[(day - 1) // 7], 7)


def _collected(weekly: list[int], lag: int, week: int) -> Fraction:
    start = 7 * (week - 1) + 1
    return sum((_daily(weekly, d - lag) for d in range(start, start + 7)), Fraction(0))


def _valid(case: dict[str, Any]) -> None:
    if case["horizon_weeks"] != 13:
        raise ValueError("the 13-week horizon is required")
    if case["revolver_commitment_cents"] < 0:
        raise ValueError("the commitment must be non-negative")


def _simulate(case: dict[str, Any], capped: bool) -> list[dict[str, int]]:
    cash = case["opening_cash_cents"]
    drawn = case["opening_drawn_cents"]
    out = []
    for w in range(1, 14):
        r = _rnd(_collected(case["weekly_sales_cents"], case["collection_lag_days"], w))
        d = _rnd(_collected(case["weekly_purchases_cents"], case["payment_lag_days"], w)) + case["weekly_opex_cents"][w - 1]
        pre = cash + r - d
        need = max(case["minimum_cash_cents"] - pre, 0)
        avail = case["revolver_commitment_cents"] - drawn if capped else need
        draw = min(need, avail)
        repay = min(max(pre - case["minimum_cash_cents"], 0), drawn) if need == 0 else 0
        cash = pre + draw - repay
        drawn = drawn + draw - repay
        liq = cash + case["revolver_commitment_cents"] - drawn
        out.append(
            {
                "receipts_cents": r,
                "disbursements_cents": d,
                "draw_cents": draw,
                "repay_cents": repay,
                "ending_cash_cents": cash,
                "drawn_balance_cents": drawn,
                "liquidity_cents": liq,
                "headroom_cents": liq - case["covenant_threshold_cents"],
            }
        )
    return out


def forecast(case: dict[str, Any]) -> list[dict[str, int]]:
    _valid(case)
    return _simulate(case, True)


def revolver_plan(case: dict[str, Any]) -> dict[str, int]:
    _valid(case)
    rows = _simulate(case, True)
    unc = _simulate(case, False)
    peak = max([case["opening_drawn_cents"]] + [x["drawn_balance_cents"] for x in rows])
    req = max([case["opening_drawn_cents"]] + [x["drawn_balance_cents"] for x in unc])
    short = max([0] + [max(case["minimum_cash_cents"] - x["ending_cash_cents"], 0) for x in rows])
    return {"peak_drawn_cents": peak, "required_commitment_cents": req, "shortfall_cents": short}


def covenant_pinch(case: dict[str, Any]) -> dict[str, int]:
    _valid(case)
    rows = _simulate(case, True)
    best_week, best = 1, rows[0]["headroom_cents"]
    for i, x in enumerate(rows[1:], start=2):
        if x["headroom_cents"] < best:
            best_week, best = i, x["headroom_cents"]
    return {"week": best_week, "headroom_cents": best}


def action_cash_impact(case: dict[str, Any], action: str, days: int) -> int:
    _valid(case)
    if action == "dso":
        lag = case["collection_lag_days"]
        if not 0 <= days <= lag:
            raise ValueError("DSO change out of range")
        total = sum((_daily(case["weekly_sales_cents"], k) for k in range(92 - lag, 92 - lag + days)), Fraction(0))
        return _rnd(total)
    if action == "dpo":
        if days < 0:
            raise ValueError("DPO change out of range")
        lag = case["payment_lag_days"]
        total = sum((_daily(case["weekly_purchases_cents"], k) for k in range(92 - lag - days, 92 - lag)), Fraction(0))
        return _rnd(total)
    raise ValueError("the action must be dso or dpo")
