"""Correct alternative: asymmetric quote (bid 3 below mid, ask 7 above), size 1, replay that returns zeros early for no fills."""

from __future__ import annotations

from typing import Any


def quote(state: dict[str, Any]) -> tuple[int, int, int]:
    mid = 10_000
    for record in reversed(state["history"]):
        if record["filled"] is True:
            mid = int(record["fill_price_cents"])
            break
    return mid - 3, mid + 7, 1


def replay(log: dict[str, Any]) -> dict[str, int]:
    turns = log["turns"]
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    fills = [t for t in turns if t["filled"] is True]
    for t in fills:
        if t["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
    if not fills:
        return {"cash_flow_cents": 0, "inventory_end": 0, "inventory_mark_cents": 0, "pnl_cents": 0}
    signs = [1 if int(t["fill_price_cents"]) == t["bid_cents"] else -1 for t in fills]
    cash = sum(-s * int(t["fill_price_cents"]) for s, t in zip(signs, fills))
    inv = sum(signs)
    mark = inv * int(log["settlement_cents"])
    return {"cash_flow_cents": cash, "inventory_end": inv, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
