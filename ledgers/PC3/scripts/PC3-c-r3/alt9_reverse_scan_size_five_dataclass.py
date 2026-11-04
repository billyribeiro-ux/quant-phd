"""Verifier alternative 9: quote scans the history backwards for the last filled price, quotes size 5, and replay uses a dataclass accumulator with a generator sum.

Legal under project.html Rung 3: bid 10 cents below and ask 10 cents above the mid, size 5 (inside 0..5). Fills are one unit whatever the size.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast


@dataclass
class Account:
    cash: int = 0
    inventory: int = 0


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, object]], state["history"])
    mid = 10_000
    last = next((r for r in reversed(history) if r["filled"] is True), None)
    if last is not None:
        mid = int(cast(int, last["fill_price_cents"]))
    return mid - 10, mid + 10, 5


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    fills = [r for r in turns if r["filled"] is True]
    for record in fills:
        if record["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
    acc = Account()
    for record in fills:
        price = int(cast(int, record["fill_price_cents"]))
        sold_at_ask = price == cast(int, record["ask_cents"])
        acc.cash += price if sold_at_ask else -price
        acc.inventory += -1 if sold_at_ask else 1
    settlement = int(cast(int, log["settlement_cents"]))
    mark = acc.inventory * settlement
    return {
        "cash_flow_cents": acc.cash,
        "inventory_end": acc.inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": acc.cash + mark,
    }
