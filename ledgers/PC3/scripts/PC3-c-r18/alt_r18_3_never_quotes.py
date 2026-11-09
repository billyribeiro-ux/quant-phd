"""Alternative r18-3: a legal policy that never quotes a size (size 0 every turn) and replays by summing the fills with an explicit loop."""

from __future__ import annotations

from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = 10_000
    return mid - 10, mid + 10, 0


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash = 0
    units = 0
    for t in turns:
        if t["filled"] is True:
            if t["fill_price_cents"] is None:
                raise ValueError("a filled turn needs a fill price")
            price = cast(int, t["fill_price_cents"])
            if price == t["ask_cents"]:
                cash, units = cash + price, units - 1
            else:
                cash, units = cash - price, units + 1
    mark = units * cast(int, log["settlement_cents"])
    return {"cash_flow_cents": cash, "inventory_end": units, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
