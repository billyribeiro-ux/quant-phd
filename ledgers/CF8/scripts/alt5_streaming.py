"""Alternative 5: generator-based streaming of weekly cash states; the summary reads the stream once."""

from __future__ import annotations

import math
from collections.abc import Iterator
from fractions import Fraction
from typing import Any


def _stream(weekly: list[int], lag: int) -> Iterator[Fraction]:
    for w in range(13):
        total = Fraction(0)
        for d in range(7 * w + 1, 7 * w + 8):
            src = d - lag
            total += Fraction(weekly[0] if src < 1 else weekly[(src - 1) // 7], 7)
        yield total


def _check(case: dict[str, Any]) -> None:
    if case["horizon_weeks"] != 13:
        raise ValueError("the 13-week horizon is required")
    if case["revolver_commitment_cents"] < 0:
        raise ValueError("the commitment must be non-negative")


def _states(case: dict[str, Any], capped: bool) -> Iterator[dict[str, int]]:
    cash, drawn = case["opening_cash_cents"], case["opening_drawn_cents"]
    m, commit = case["minimum_cash_cents"], case["revolver_commitment_cents"]
    for rec, pay, opex in zip(
        _stream(case["weekly_sales_cents"], case["collection_lag_days"]),
        _stream(case["weekly_purchases_cents"], case["payment_lag_days"]),
        case["weekly_opex_cents"],
        strict=True,
    ):
        r = math.floor(rec + Fraction(1, 2))
        d = math.floor(pay + opex + Fraction(1, 2))
        pre = cash + r - d
        draw = max(m - pre, 0)
        if capped:
            draw = min(draw, commit - drawn)
        repay = 0 if draw or pre < m else min(pre - m, drawn)
        cash = pre + draw - repay
        drawn += draw - repay
        liq = cash + commit - drawn
        yield {
            "receipts_cents": r,
            "disbursements_cents": d,
            "draw_cents": draw,
            "repay_cents": repay,
            "ending_cash_cents": cash,
            "drawn_balance_cents": drawn,
            "liquidity_cents": liq,
            "headroom_cents": liq - case["covenant_threshold_cents"],
        }


def forecast(case: dict[str, Any]) -> list[dict[str, int]]:
    _check(case)
    return list(_states(case, True))


def revolver_plan(case: dict[str, Any]) -> dict[str, int]:
    _check(case)
    rows = list(_states(case, True))
    peak = max([case["opening_drawn_cents"]] + [r["drawn_balance_cents"] for r in rows])
    unc = list(_states(case, False))
    required = max([case["opening_drawn_cents"]] + [r["drawn_balance_cents"] for r in unc])
    short = max([0] + [max(case["minimum_cash_cents"] - r["ending_cash_cents"], 0) for r in rows])
    return {"peak_drawn_cents": peak, "required_commitment_cents": required, "shortfall_cents": short}


def covenant_pinch(case: dict[str, Any]) -> dict[str, int]:
    _check(case)
    best: tuple[int, int] | None = None
    for week, row in enumerate(_states(case, True), start=1):
        if best is None or row["headroom_cents"] < best[1]:
            best = (week, row["headroom_cents"])
    assert best is not None
    return {"week": best[0], "headroom_cents": best[1]}


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
