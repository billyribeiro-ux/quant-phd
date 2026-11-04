"""Alt12: half-spread of 1 cent, last fill found by a reversed scan, size 5, replay with a dataclass-free accumulator."""

from __future__ import annotations

from typing import Any, cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, Any]], state["history"])
    mid = 10_000
    for record in reversed(history):
        if record["filled"] is True:
            mid = int(record["fill_price_cents"])
            break
    return mid - 1, mid + 1, 5


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, Any]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash_flow = 0
    inventory = 0
    for r in turns:
        if not r["filled"]:
            continue
        price = r["fill_price_cents"]
        if price is None:
            raise ValueError("a filled turn needs a fill price")
        price = int(price)
        step = 1 if price == r["bid_cents"] else -1
        inventory += step
        cash_flow -= step * price
    settlement = int(log["settlement_cents"])
    mark = settlement * inventory
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }
