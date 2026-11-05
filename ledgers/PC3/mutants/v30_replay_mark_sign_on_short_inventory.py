"""Student error: replay marks a net short inventory with the wrong sign, so the P&L adds the settlement value of a short position."""

from __future__ import annotations


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = 10_000
    for record in state["history"]:  # type: ignore[attr-defined]
        if record["filled"] is True:
            mid = int(record["fill_price_cents"])
    return mid - 10, mid + 10, 1


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = log["turns"]
    if len(turns) != 20:  # type: ignore[arg-type]
        raise ValueError("a log has exactly 20 turns")
    cash_flow = 0
    inventory = 0
    for record in turns:  # type: ignore[attr-defined]
        if record["filled"] is not True:
            continue
        price = int(record["fill_price_cents"])
        side = 1 if price == int(record["bid_cents"]) else -1
        cash_flow += -side * price
        inventory += side
    settlement = int(log["settlement_cents"])  # type: ignore[call-overload]
    mark = abs(inventory) * settlement if inventory < 0 else inventory * settlement
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
