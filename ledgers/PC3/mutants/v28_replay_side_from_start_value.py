"""Student error: replay takes the side of a fill by comparing its price with the starting value of 10000 cents, not with the turn's quote."""

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
        side = -1 if price > 10_000 else 1
        cash_flow += -side * price
        inventory += side
    settlement = int(log["settlement_cents"])  # type: ignore[call-overload]
    mark = inventory * settlement
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
