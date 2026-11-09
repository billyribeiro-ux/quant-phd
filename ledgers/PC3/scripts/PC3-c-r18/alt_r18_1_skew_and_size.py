"""Alternative r18-1: quote skews both sides by minus one cent per unit of inventory and scales size down as |inventory| grows; replay takes the side from the price relative to the turn's mid."""

from __future__ import annotations

from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = 10_000
    for record in cast(list[dict[str, object]], state["history"]):
        if record["filled"] is True:
            mid = int(cast(int, record["fill_price_cents"]))
    inventory = cast(int, state["inventory"])
    size = 5 - abs(inventory) // 2
    return mid - 10 - inventory, mid + 10 - inventory, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    fills = [t for t in turns if t["filled"] is True]
    for t in fills:
        if t["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
    sides = [
        -1 if cast(int, t["fill_price_cents"]) > (cast(int, t["bid_cents"]) + cast(int, t["ask_cents"])) // 2 else 1
        for t in fills
    ]
    cash_flow = sum(-s * cast(int, t["fill_price_cents"]) for s, t in zip(sides, fills, strict=True))
    inventory = sum(sides)
    mark = inventory * cast(int, log["settlement_cents"])
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
