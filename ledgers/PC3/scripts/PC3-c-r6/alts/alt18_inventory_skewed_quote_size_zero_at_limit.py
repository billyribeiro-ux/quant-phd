"""Alternative correct implementation 18: both sides shifted by minus one cent per unit of inventory, size 0 at |inventory| 10, replay with a list accumulator."""

from __future__ import annotations

from typing import Any


def quote(state: dict[str, Any]) -> tuple[int, int, int]:
    inventory = int(state["inventory"])
    mid = 10_000
    for r in state["history"]:
        if r["filled"] is True:
            mid = int(r["fill_price_cents"])
    bid = mid - 10 - inventory
    ask = mid + 10 - inventory
    size = 0 if abs(inventory) >= 10 else 1
    return bid, ask, size


def replay(log: dict[str, Any]) -> dict[str, int]:
    turns: list[dict[str, Any]] = log["turns"]
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    flows: list[int] = []
    sides: list[int] = []
    for r in turns:
        if r["filled"] is not True:
            continue
        if r["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        p = int(r["fill_price_cents"])
        s = -1 if p == r["ask_cents"] else 1
        flows.append(-s * p)
        sides.append(s)
    cash_flow = sum(flows)
    inventory = sum(sides)
    mark = inventory * int(log["settlement_cents"])
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
