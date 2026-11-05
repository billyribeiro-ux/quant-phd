"""Correct alternative: quotes size 0 on every turn (no trade can fill), with the standard replay."""

from __future__ import annotations

from typing import Any


def quote(state: dict[str, Any]) -> tuple[int, int, int]:
    return 9_990, 10_010, 0


def replay(log: dict[str, Any]) -> dict[str, int]:
    if len(log["turns"]) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash = 0
    inv = 0
    for t in log["turns"]:
        if t["filled"] is True:
            if t["fill_price_cents"] is None:
                raise ValueError("a filled turn needs a fill price")
            side = 1 if t["fill_price_cents"] == t["bid_cents"] else -1
            cash -= side * t["fill_price_cents"]
            inv += side
    mark = inv * log["settlement_cents"]
    return {"cash_flow_cents": cash, "inventory_end": inv, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
