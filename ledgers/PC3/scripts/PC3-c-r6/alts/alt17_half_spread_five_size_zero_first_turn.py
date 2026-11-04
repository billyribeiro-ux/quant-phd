"""Alternative correct implementation 17: half-spread 5 cents, size 0 on turn 1 only, replay as one fold with truthiness tests."""

from __future__ import annotations

from functools import reduce
from typing import Any


def quote(state: dict[str, Any]) -> tuple[int, int, int]:
    history = state["history"]
    mids = [r["fill_price_cents"] for r in history if r["filled"]]
    mid = mids[-1] if mids else 10_000
    size = 0 if state["turn"] == 1 else 1
    return mid - 5, mid + 5, size


def replay(log: dict[str, Any]) -> dict[str, int]:
    turns = log["turns"]
    if not len(turns) == 20:
        raise ValueError("a log has exactly 20 turns")
    fills = [r for r in turns if r["filled"]]
    for r in fills:
        if r["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")

    def step(acc: tuple[int, int], r: dict[str, Any]) -> tuple[int, int]:
        cash, inv = acc
        price = int(r["fill_price_cents"])
        side = -1 if price == r["ask_cents"] else 1
        return cash - side * price, inv + side

    cash_flow, inventory = reduce(step, fills, (0, 0))
    mark = inventory * int(log["settlement_cents"])
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
