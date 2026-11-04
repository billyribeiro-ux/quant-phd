"""Alternative 2: a closure returned by make_quoter, and a replay written as one fold over the turns."""

from __future__ import annotations

from collections.abc import Callable
from functools import reduce
from typing import cast

HORIZON = 20
START_CENTS = 10_000
HALF_SPREAD = 10
SIZE = 1


def make_quoter() -> Callable[[dict[str, object]], tuple[int, int, int]]:
    def quote(state: dict[str, object]) -> tuple[int, int, int]:
        last = START_CENTS
        for record in cast(list[dict[str, object]], state["history"]):
            if record["filled"] is True:
                last = cast(int, record["fill_price_cents"])
        return last - HALF_SPREAD, last + HALF_SPREAD, SIZE

    return quote


quote = make_quoter()


def _step(acc: tuple[int, int], record: dict[str, object]) -> tuple[int, int]:
    cash, units = acc
    if record["filled"] is not True:
        return cash, units
    price = record["fill_price_cents"]
    if price is None:
        raise ValueError("a filled turn needs a fill price")
    price_cents = cast(int, price)
    if price_cents == record["ask_cents"]:
        return cash + price_cents, units - 1
    return cash - price_cents, units + 1


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != HORIZON:
        raise ValueError("a log has exactly 20 turns")
    settlement = cast(int, log["settlement_cents"])
    cash, units = reduce(_step, turns, (0, 0))
    mark = units * settlement
    return {"cash_flow_cents": cash, "inventory_end": units, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
