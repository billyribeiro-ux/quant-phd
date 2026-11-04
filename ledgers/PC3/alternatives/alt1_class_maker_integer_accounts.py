"""Alternative 1: a class-based maker with integer-only accounting, and a replay that walks the fills with a loop."""

from __future__ import annotations

from typing import cast

HORIZON = 20
START_CENTS = 10_000
HALF_SPREAD = 10
SIZE = 1


class Maker:
    """Quotes symmetrically around the last filled price, or around 10000 cents before any fill."""

    def __init__(self) -> None:
        self.last_fill: int = START_CENTS

    def observe(self, history: list[dict[str, object]]) -> None:
        for record in history:
            if record["filled"] is True:
                self.last_fill = cast(int, record["fill_price_cents"])

    def quote(self, state: dict[str, object]) -> tuple[int, int, int]:
        self.observe(cast(list[dict[str, object]], state["history"]))
        return self.last_fill - HALF_SPREAD, self.last_fill + HALF_SPREAD, SIZE


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    return Maker().quote(state)


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != HORIZON:
        raise ValueError("a log has exactly 20 turns")
    settlement = cast(int, log["settlement_cents"])
    cash = 0
    units = 0
    for turn in turns:
        if turn["filled"] is not True:
            continue
        price = turn["fill_price_cents"]
        if price is None:
            raise ValueError("a filled turn needs a fill price")
        price_cents = cast(int, price)
        sold_by_maker = price_cents == turn["ask_cents"]
        cash += price_cents if sold_by_maker else -price_cents
        units += -1 if sold_by_maker else 1
    mark = units * settlement
    return {"cash_flow_cents": cash, "inventory_end": units, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
