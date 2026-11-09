"""Correct alternative: quote posts size 0 when the inventory it sees is at the limit, and the reference rule otherwise."""

from __future__ import annotations

from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = 10_000
    for record in cast(list[dict[str, object]], state["history"]):
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    size = 0 if abs(cast(int, state["inventory"])) >= cast(int, state["limit"]) else 1
    return mid - 10, mid + 10, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash = 0
    inv = 0
    for r in turns:
        if r["filled"] is not True:
            continue
        if r["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        p = cast(int, r["fill_price_cents"])
        side = 1 if p == r["bid_cents"] else -1
        cash -= side * p
        inv += side
    mark = inv * cast(int, log["settlement_cents"])
    return {"cash_flow_cents": cash, "inventory_end": inv, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
