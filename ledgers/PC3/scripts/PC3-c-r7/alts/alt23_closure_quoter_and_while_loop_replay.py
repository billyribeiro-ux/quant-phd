"""Alternative 23: a closure-made quoter (no state kept between games), and a replay written with an index-based while loop."""

from __future__ import annotations

from collections.abc import Callable


def make_quoter() -> Callable[[dict[str, object]], tuple[int, int, int]]:
    def quote(state: dict[str, object]) -> tuple[int, int, int]:
        mid = 10_000
        history = list(state["history"])  # type: ignore[call-overload]
        for record in history:
            if record["filled"] is True:
                mid = int(record["fill_price_cents"])  # type: ignore[call-overload]
        return mid - 10, mid + 10, 1

    return quote


quote = make_quoter()


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = list(log["turns"])  # type: ignore[call-overload]
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash_flow = 0
    inventory = 0
    i = 0
    while i < len(turns):
        record = turns[i]
        i += 1
        if record["filled"] is not True:
            continue
        price_value = record["fill_price_cents"]
        if price_value is None:
            raise ValueError("a filled turn needs a fill price")
        price = int(price_value)  # type: ignore[call-overload]
        if price == int(record["ask_cents"]):  # type: ignore[call-overload]
            cash_flow += price
            inventory -= 1
        else:
            cash_flow -= price
            inventory += 1
    mark = inventory * int(log["settlement_cents"])  # type: ignore[call-overload]
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
