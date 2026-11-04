"""Alt11: legal skewed quote (mid shifted against inventory), size 0 within 1 unit of the limit, replay by fills list."""

from __future__ import annotations

from typing import Any, cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = 10_000
    for record in cast(list[dict[str, Any]], state["history"]):
        if record["filled"]:
            mid = int(record["fill_price_cents"])
    inventory = cast(int, state["inventory"])
    skewed = mid - 2 * inventory
    size = 0 if abs(inventory) >= cast(int, state["limit"]) - 1 else 1
    return skewed - 10, skewed + 10, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, Any]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    fills = [r for r in turns if r["filled"]]
    for r in fills:
        if r["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
    sides = [(-1 if int(r["fill_price_cents"]) == r["ask_cents"] else 1, int(r["fill_price_cents"])) for r in fills]
    cash_flow = sum(-side * price for side, price in sides)
    inventory = sum(side for side, _ in sides)
    mark = inventory * int(log["settlement_cents"])
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }
