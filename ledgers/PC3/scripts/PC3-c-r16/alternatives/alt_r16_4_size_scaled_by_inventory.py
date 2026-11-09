"""Alternative 4 (size falls as the inventory grows: 5 - |inventory| // 2, so 0 at the limit; replay with an explicit list accumulator)."""

from __future__ import annotations

from typing import Any, cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, Any]], state["history"])
    mid = 10_000
    for record in history:
        if record["filled"] is True:
            mid = int(record["fill_price_cents"])
    inventory = int(cast(int, state["inventory"]))
    size = 5 - abs(inventory) // 2
    return mid - 10, mid + 10, max(0, min(5, size))


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, Any]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    flows: list[int] = []
    sides: list[int] = []
    for record in turns:
        if record["filled"] is True:
            price = record["fill_price_cents"]
            if price is None:
                raise ValueError("a filled turn needs a fill price")
            sides.append(-1 if price == record["ask_cents"] else 1)
            flows.append(-sides[-1] * int(price))
    cash_flow = sum(flows)
    inventory = sum(sides)
    mark = inventory * int(cast(int, log["settlement_cents"]))
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
