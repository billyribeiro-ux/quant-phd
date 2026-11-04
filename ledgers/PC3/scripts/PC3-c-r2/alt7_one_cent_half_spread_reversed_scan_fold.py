"""Verifier alternative 7 (round 2): a quote 1 cent either side of the last fill, size 5, with the mid found by a reversed
scan that stops at the first fill; a replay that folds the fills into a (cash, units) pair and books each purchase at its bid.

Correct by the rules of project.html section "Rung 3 · Specification": bid below ask, size 0..5, a fill needs size at
least 1 (the engine's rule), and replay sums the fill cash flows and the fill inventory and marks at the settlement value.
"""

from __future__ import annotations

from functools import reduce
from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, object]], state["history"])
    mid = 10_000
    for record in reversed(history):
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
            break
    return mid - 1, mid + 1, 5


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")

    def step(acc: tuple[int, int], record: dict[str, object]) -> tuple[int, int]:
        cash, units = acc
        if record["filled"] is not True:
            return acc
        if record["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        price = cast(int, record["fill_price_cents"])
        if price == record["bid_cents"]:
            return cash - price, units + 1
        return cash + price, units - 1

    cash, units = reduce(step, turns, (0, 0))
    mark = units * cast(int, log["settlement_cents"])
    return {"cash_flow_cents": cash, "inventory_end": units, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
