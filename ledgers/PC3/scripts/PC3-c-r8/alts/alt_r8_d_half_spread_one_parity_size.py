"""Correct alternative: half-spread of 1 cent around the last fill, size 5 on even turns and 1 on odd turns."""

from __future__ import annotations

from typing import Any


def quote(state: dict[str, Any]) -> tuple[int, int, int]:
    mid = 10_000
    for record in state["history"]:
        if record["filled"] is True:
            mid = int(record["fill_price_cents"])
    size = 5 if state["turn"] % 2 == 0 else 1
    return mid - 1, mid + 1, size


def replay(log: dict[str, Any]) -> dict[str, int]:
    turns = log["turns"]
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash_flow = 0
    inventory = 0
    for t in turns:
        if not t["filled"]:
            continue
        price = t["fill_price_cents"]
        if price is None:
            raise ValueError("a filled turn needs a fill price")
        if price == t["ask_cents"]:
            cash_flow += int(price)
            inventory -= 1
        else:
            cash_flow -= int(price)
            inventory += 1
    mark = inventory * int(log["settlement_cents"])
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }
