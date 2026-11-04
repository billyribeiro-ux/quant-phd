"""Alternative correct solution: asymmetric quotes that lean against the inventory (a 1-cent skew per unit held), replay by loop.

Quote: mid is the last fill price; the bid is 12 cents below and the ask 8 cents above when long, mirrored when short.
Size is 2 units while |inventory| is at most 3 and 1 otherwise, always within 0..5.
"""

from __future__ import annotations

from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, object]], state["history"])
    inventory = cast(int, state["inventory"])
    mid = 10_000
    for record in history:
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    if inventory > 0:
        bid, ask = mid - 12, mid + 8
    elif inventory < 0:
        bid, ask = mid - 8, mid + 12
    else:
        bid, ask = mid - 10, mid + 10
    size = 2 if abs(inventory) <= 3 else 1
    return bid, ask, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash_flow = 0
    inventory = 0
    for record in turns:
        if record["filled"] is not True:
            continue
        if record["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        price = cast(int, record["fill_price_cents"])
        if price == record["ask_cents"]:
            cash_flow += price
            inventory -= 1
        else:
            cash_flow -= price
            inventory += 1
    mark = inventory * cast(int, log["settlement_cents"])
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }
