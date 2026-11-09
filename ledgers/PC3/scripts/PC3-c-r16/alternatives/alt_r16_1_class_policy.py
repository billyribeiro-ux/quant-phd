"""Alternative 1 (class-based policy, integer accounting in a class): quotes 10 cents either side of the last fill, size 1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, cast


@dataclass
class Maker:
    start: int = 10_000
    half: int = 10
    unit: int = 1
    _mid_log: list[int] = field(default_factory=list)

    def mid(self, history: list[dict[str, Any]]) -> int:
        value = self.start
        for record in history:
            if record["filled"] is True:
                value = int(record["fill_price_cents"])
        return value

    def quote(self, state: dict[str, object]) -> tuple[int, int, int]:
        mid = self.mid(cast(list[dict[str, Any]], state["history"]))
        return mid - self.half, mid + self.half, self.unit


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    return Maker().quote(state)


class Accounts:
    def __init__(self) -> None:
        self.cash = 0
        self.units = 0

    def book(self, bid: int, ask: int, price: int) -> None:
        if price == ask:
            self.cash += price
            self.units -= 1
        else:
            self.cash -= price
            self.units += 1


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, Any]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    accounts = Accounts()
    for record in turns:
        if record["filled"] is True:
            if record["fill_price_cents"] is None:
                raise ValueError("a filled turn needs a fill price")
            accounts.book(int(record["bid_cents"]), int(record["ask_cents"]), int(record["fill_price_cents"]))
    mark = accounts.units * int(cast(int, log["settlement_cents"]))
    return {
        "cash_flow_cents": accounts.cash,
        "inventory_end": accounts.units,
        "inventory_mark_cents": mark,
        "pnl_cents": accounts.cash + mark,
    }
