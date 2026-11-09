"""Alternative 3 (inventory-skewed quotes: both sides shifted by minus one cent per unit held; replay from the cash identity)."""

from __future__ import annotations

from typing import Any, cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, Any]], state["history"])
    mid = 10_000
    for record in history:
        if record["filled"] is True:
            mid = int(record["fill_price_cents"])
    skew = int(cast(int, state["inventory"]))
    return mid - 10 - skew, mid + 10 - skew, 1


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, Any]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash_flow = 0
    inventory = 0
    for record in turns:
        if not record["filled"]:
            continue
        price = record["fill_price_cents"]
        if price is None:
            raise ValueError("a filled turn needs a fill price")
        if price == record["ask_cents"]:
            cash_flow += int(price)
            inventory -= 1
        else:
            cash_flow -= int(price)
            inventory += 1
    settlement = int(cast(int, log["settlement_cents"]))
    mark = inventory * settlement
    pnl = cash_flow + mark
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": pnl}
