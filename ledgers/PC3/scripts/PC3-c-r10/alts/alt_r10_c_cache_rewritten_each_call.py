"""Alternative (round 10): quote writes a module-level mid on every call, recomputed from the history of that call, and reads it back in the same call. It keeps nothing between calls. Legal under the spec."""

from __future__ import annotations

from typing import cast

_LAST: dict[str, int] = {}


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    _LAST["mid"] = 10_000
    for record in cast(list[dict[str, object]], state["history"]):
        if record["filled"] is True:
            _LAST["mid"] = cast(int, record["fill_price_cents"])
    mid = _LAST["mid"]
    _LAST.clear()
    return mid - 1, mid + 1, 5


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
        side = 1 if price == record["bid_cents"] else -1
        cash_flow -= side * price
        inventory += side
    mark = inventory * cast(int, log["settlement_cents"])
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark,
            "pnl_cents": cash_flow + mark}
