"""Alternative 4: the path is stored as dictionary-of-lists columns, and the rows are assembled at the end."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any


def _check(case: dict[str, Any]) -> None:
    if case["horizon_weeks"] != 13:
        raise ValueError("the 13-week horizon is required")
    if case["revolver_commitment_cents"] < 0:
        raise ValueError("the commitment must be non-negative")


def _flows(weekly: list[int], lag: int) -> list[Fraction]:
    daily = {d: Fraction(weekly[0] if d - lag < 1 else weekly[(d - lag - 1) // 7], 7) for d in range(1, 92)}
    return [sum((daily[d] for d in range(7 * w + 1, 7 * w + 8)), Fraction(0)) for w in range(13)]


def _columns(case: dict[str, Any], capped: bool) -> dict[str, list[int]]:
    rec = [math.floor(x + Fraction(1, 2)) for x in _flows(case["weekly_sales_cents"], case["collection_lag_days"])]
    pay = _flows(case["weekly_purchases_cents"], case["payment_lag_days"])
    cols: dict[str, list[int]] = {k: [] for k in (
        "receipts_cents", "disbursements_cents", "draw_cents", "repay_cents",
        "ending_cash_cents", "drawn_balance_cents", "liquidity_cents", "headroom_cents")}
    cash, drawn = case["opening_cash_cents"], case["opening_drawn_cents"]
    for w in range(13):
        out = math.floor(pay[w] + case["weekly_opex_cents"][w] + Fraction(1, 2))
        pre = cash + rec[w] - out
        m = case["minimum_cash_cents"]
        if pre < m:
            draw = min(m - pre, case["revolver_commitment_cents"] - drawn) if capped else m - pre
            repay = 0
        else:
            draw, repay = 0, min(pre - m, drawn)
        cash = pre + draw - repay
        drawn += draw - repay
        liq = cash + case["revolver_commitment_cents"] - drawn
        for key, value in (
            ("receipts_cents", rec[w]), ("disbursements_cents", out), ("draw_cents", draw), ("repay_cents", repay),
            ("ending_cash_cents", cash), ("drawn_balance_cents", drawn), ("liquidity_cents", liq),
            ("headroom_cents", liq - case["covenant_threshold_cents"]),
        ):
            cols[key].append(value)
    return cols


def forecast(case: dict[str, Any]) -> list[dict[str, int]]:
    _check(case)
    cols = _columns(case, True)
    return [{k: cols[k][w] for k in cols} for w in range(13)]


def revolver_plan(case: dict[str, Any]) -> dict[str, int]:
    _check(case)
    cols = _columns(case, True)
    unc = _columns(case, False)
    return {
        "peak_drawn_cents": max([case["opening_drawn_cents"]] + cols["drawn_balance_cents"]),
        "required_commitment_cents": max([case["opening_drawn_cents"]] + unc["drawn_balance_cents"]),
        "shortfall_cents": max([0] + [max(case["minimum_cash_cents"] - c, 0) for c in cols["ending_cash_cents"]]),
    }


def covenant_pinch(case: dict[str, Any]) -> dict[str, int]:
    _check(case)
    head = _columns(case, True)["headroom_cents"]
    w = min(range(13), key=lambda i: (head[i], i))
    return {"week": w + 1, "headroom_cents": head[w]}


def action_cash_impact(case: dict[str, Any], action: str, days: int) -> int:
    _check(case)
    if action == "dso":
        lag = case["collection_lag_days"]
        if not 0 <= days <= lag:
            raise ValueError("DSO change out of range")
        s = case["weekly_sales_cents"]
        gain = sum((Fraction(s[0] if k < 1 else s[(k - 1) // 7], 7) for k in range(92 - lag, 92 - lag + days)), Fraction(0))
        return math.floor(gain + Fraction(1, 2))
    if action == "dpo":
        if days < 0:
            raise ValueError("DPO change out of range")
        lag = case["payment_lag_days"]
        p = case["weekly_purchases_cents"]
        kept = sum((Fraction(p[0] if k < 1 else p[(k - 1) // 7], 7) for k in range(92 - lag - days, 92 - lag)), Fraction(0))
        return math.floor(kept + Fraction(1, 2))
    raise ValueError("the action must be dso or dpo")
