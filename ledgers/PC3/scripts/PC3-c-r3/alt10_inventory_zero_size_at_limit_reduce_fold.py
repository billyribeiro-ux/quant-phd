"""Verifier alternative 10: quote skews the mid by minus one cent per unit of inventory and quotes size 0 at the inventory limit; replay folds the fills with functools.reduce.

Legal under project.html Rung 3: bid below ask on every turn, size 0 is inside 0..5, and fills take one unit with |I| <= 10.
"""

from __future__ import annotations

from functools import reduce
from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, object]], state["history"])
    mid = 10_000
    for record in history:
        if record["filled"] is True:
            mid = int(cast(int, record["fill_price_cents"]))
    inventory = int(cast(int, state["inventory"]))
    limit = int(cast(int, state["limit"]))
    size = 0 if abs(inventory) >= limit else 1
    return mid - 10 - inventory, mid + 10 - inventory, size


def _step(acc: tuple[int, int], record: dict[str, object]) -> tuple[int, int]:
    if record["filled"] is not True:
        return acc
    price = cast(object, record["fill_price_cents"])
    if price is None:
        raise ValueError("a filled turn needs a fill price")
    p = int(cast(int, price))
    side = -1 if p == cast(int, record["ask_cents"]) else 1
    return acc[0] - side * p, acc[1] + side


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash, inventory = reduce(_step, turns, (0, 0))
    mark = inventory * int(cast(int, log["settlement_cents"]))
    return {
        "cash_flow_cents": cash,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash + mark,
    }
