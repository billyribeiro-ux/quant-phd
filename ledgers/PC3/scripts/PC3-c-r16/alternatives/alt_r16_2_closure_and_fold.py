"""Alternative 2 (closure factory for quote, replay as one fold over the turns with functools.reduce)."""

from __future__ import annotations

from functools import reduce
from typing import Any, cast


def make_quoter(start: int = 10_000, half: int = 10, size: int = 1) -> Any:
    def quote(state: dict[str, object]) -> tuple[int, int, int]:
        history = cast(list[dict[str, Any]], state["history"])
        last = [int(r["fill_price_cents"]) for r in history if r["filled"] is True]
        mid = last[-1] if last else start
        return mid - half, mid + half, size

    return quote


quote = make_quoter()


def _step(acc: tuple[int, int], record: dict[str, Any]) -> tuple[int, int]:
    cash, units = acc
    if record["filled"] is not True:
        return acc
    price = int(record["fill_price_cents"])
    if price == record["ask_cents"]:
        return cash + price, units - 1
    return cash - price, units + 1


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, Any]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    for record in turns:
        if record["filled"] is True and record["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
    cash, units = reduce(_step, turns, (0, 0))
    mark = units * int(cast(int, log["settlement_cents"]))
    return {"cash_flow_cents": cash, "inventory_end": units, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
