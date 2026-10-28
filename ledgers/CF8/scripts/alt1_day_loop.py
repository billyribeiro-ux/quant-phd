"""Alternative 1: day-level Fraction arrays and a per-week loop, no shared helpers."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any


def _days(weekly: list[int], lag: int) -> list[Fraction]:
    rates = [Fraction(v, 7) for v in weekly]
    out = [Fraction(0)] * 92
    for day in range(1, 92):
        src = day - lag
        out[day] = rates[0] if src < 1 else rates[(src - 1) // 7]
    return out


def _weekly(weekly: list[int], lag: int) -> list[Fraction]:
    days = _days(weekly, lag)
    return [sum(days[7 * w + 1 : 7 * w + 8], Fraction(0)) for w in range(13)]


def _cum(weekly: list[int], lag: int) -> Fraction:
    total = Fraction(0)
    for k in range(-300, 92 - lag):
        total += Fraction(weekly[0] if k < 1 else weekly[(k - 1) // 7], 7)
    return total


def _rnd(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def _check(case: dict[str, Any]) -> None:
    if case["horizon_weeks"] != 13:
        raise ValueError("the 13-week horizon is required")
    if case["revolver_commitment_cents"] < 0:
        raise ValueError("the commitment must be non-negative")


def _run(case: dict[str, Any], capped: bool = True) -> tuple[list[dict[str, int]], int]:
    rec = _weekly(case["weekly_sales_cents"], case["collection_lag_days"])
    pay = _weekly(case["weekly_purchases_cents"], case["payment_lag_days"])
    rows = []
    cash, drawn = case["opening_cash_cents"], case["opening_drawn_cents"]
    shortfall = 0
    for w in range(13):
        r = _rnd(rec[w])
        d = _rnd(pay[w] + case["weekly_opex_cents"][w])
        pre = cash + r - d
        m = case["minimum_cash_cents"]
        if pre < m:
            need = m - pre
            draw = min(need, case["revolver_commitment_cents"] - drawn) if capped else need
            repay = 0
        else:
            draw = 0
            repay = min(pre - m, drawn)
        cash = pre + draw - repay
        drawn = drawn + draw - repay
        liq = cash + case["revolver_commitment_cents"] - drawn
        rows.append(
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
        shortfall = max(shortfall, m - cash)
    return rows, max(shortfall, 0)


def forecast(case: dict[str, Any]) -> list[dict[str, int]]:
    _check(case)
    return _run(case)[0]


def revolver_plan(case: dict[str, Any]) -> dict[str, int]:
    _check(case)
    rows, short = _run(case, True)
    free, _ = _run(case, False)
    peak = max([case["opening_drawn_cents"]] + [r["drawn_balance_cents"] for r in rows])
    required = max([case["opening_drawn_cents"]] + [r["drawn_balance_cents"] for r in free])
    return {"peak_drawn_cents": peak, "required_commitment_cents": required, "shortfall_cents": short}


def covenant_pinch(case: dict[str, Any]) -> dict[str, int]:
    _check(case)
    rows = _run(case)[0]
    w = min(range(13), key=lambda i: rows[i]["headroom_cents"])
    return {"week": w + 1, "headroom_cents": rows[w]["headroom_cents"]}


def action_cash_impact(case: dict[str, Any], action: str, days: int) -> int:
    _check(case)
    if action == "dso":
        if not 0 <= days <= case["collection_lag_days"]:
            raise ValueError("DSO change out of range")
        lag = case["collection_lag_days"]
        return _rnd(_cum(case["weekly_sales_cents"], lag - days) - _cum(case["weekly_sales_cents"], lag))
    if action == "dpo":
        if days < 0:
            raise ValueError("DPO change out of range")
        lag = case["payment_lag_days"]
        return _rnd(_cum(case["weekly_purchases_cents"], lag) - _cum(case["weekly_purchases_cents"], lag + days))
    raise ValueError("the action must be dso or dpo")
