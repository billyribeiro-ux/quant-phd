"""Alternative 2: float arithmetic throughout, with the half-up rule applied to each float money output."""

from __future__ import annotations

import math
from typing import Any


def _rate(weekly: list[float], day: int) -> float:
    return weekly[0] / 7.0 if day < 1 else weekly[(day - 1) // 7] / 7.0


def _flow(weekly: list[float], lag: int, w: int) -> float:
    return sum(_rate(weekly, d - lag) for d in range(7 * (w - 1) + 1, 7 * w + 1))


def _half(x: float) -> int:
    return int(math.floor(x + 0.5))


def _check(case: dict[str, Any]) -> None:
    if case["horizon_weeks"] != 13:
        raise ValueError("the 13-week horizon is required")
    if case["revolver_commitment_cents"] < 0:
        raise ValueError("the commitment must be non-negative")


def _path(case: dict[str, Any], capped: bool) -> tuple[list[dict[str, int]], int]:
    cash = float(case["opening_cash_cents"])
    drawn = float(case["opening_drawn_cents"])
    commit = float(case["revolver_commitment_cents"])
    m = float(case["minimum_cash_cents"])
    rows: list[dict[str, int]] = []
    peak_uncapped = drawn
    low = 0
    for w in range(1, 14):
        r = _half(_flow(case["weekly_sales_cents"], case["collection_lag_days"], w))
        d = _half(_flow(case["weekly_purchases_cents"], case["payment_lag_days"], w) + case["weekly_opex_cents"][w - 1])
        pre = cash + r - d
        if pre < m:
            need = m - pre
            draw = min(need, commit - drawn) if capped else need
            repay = 0.0
        else:
            draw = 0.0
            repay = min(pre - m, drawn)
        cash = pre + draw - repay
        drawn = drawn + draw - repay
        peak_uncapped = max(peak_uncapped, drawn) if capped else peak_uncapped
        liq = cash + commit - drawn
        low = max(low, int(max(0.0, m - cash)))
        rows.append(
            {
                "receipts_cents": r,
                "disbursements_cents": d,
                "draw_cents": int(draw),
                "repay_cents": int(repay),
                "ending_cash_cents": int(cash),
                "drawn_balance_cents": int(drawn),
                "liquidity_cents": int(liq),
                "headroom_cents": int(liq - case["covenant_threshold_cents"]),
            }
        )
    return rows, low


def forecast(case: dict[str, Any]) -> list[dict[str, int]]:
    _check(case)
    return _path(case, True)[0]


def _uncapped_peak(case: dict[str, Any]) -> int:
    cash = float(case["opening_cash_cents"])
    drawn = float(case["opening_drawn_cents"])
    m = float(case["minimum_cash_cents"])
    peak = drawn
    for w in range(1, 14):
        r = _half(_flow(case["weekly_sales_cents"], case["collection_lag_days"], w))
        d = _half(_flow(case["weekly_purchases_cents"], case["payment_lag_days"], w) + case["weekly_opex_cents"][w - 1])
        pre = cash + r - d
        if pre < m:
            draw = m - pre
            cash = m
            drawn += draw
        else:
            rep = min(pre - m, drawn)
            cash = pre - rep
            drawn -= rep
        peak = max(peak, drawn)
    return int(peak)


def revolver_plan(case: dict[str, Any]) -> dict[str, int]:
    _check(case)
    rows, low = _path(case, True)
    peak = max([case["opening_drawn_cents"]] + [r["drawn_balance_cents"] for r in rows])
    return {"peak_drawn_cents": peak, "required_commitment_cents": _uncapped_peak(case), "shortfall_cents": low}


def covenant_pinch(case: dict[str, Any]) -> dict[str, int]:
    _check(case)
    rows = _path(case, True)[0]
    w = min(range(13), key=lambda i: rows[i]["headroom_cents"])
    return {"week": w + 1, "headroom_cents": rows[w]["headroom_cents"]}


def action_cash_impact(case: dict[str, Any], action: str, days: int) -> int:
    _check(case)
    if action == "dso":
        lag = case["collection_lag_days"]
        if not 0 <= days <= lag:
            raise ValueError("DSO change out of range")
        s = case["weekly_sales_cents"]
        gain = sum(_rate(s, k) for k in range(92 - lag, 92 - lag + days))
        return _half(gain)
    if action == "dpo":
        if days < 0:
            raise ValueError("DPO change out of range")
        lag = case["payment_lag_days"]
        p = case["weekly_purchases_cents"]
        kept = sum(_rate(p, k) for k in range(92 - lag - days, 92 - lag))
        return _half(kept)
    raise ValueError("the action must be dso or dpo")
