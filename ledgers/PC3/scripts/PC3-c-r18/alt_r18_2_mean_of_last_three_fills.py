"""Alternative r18-2: quote centres on the rounded mean of the last three fill prices; replay is a class with a fold over the turns and integer accounting."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    prices = [
        cast(int, r["fill_price_cents"])
        for r in cast(list[dict[str, object]], state["history"])
        if r["filled"] is True
    ]
    recent = prices[-3:]
    mid = 10_000 if not recent else (sum(recent) + len(recent) // 2) // len(recent)
    return mid - 10, mid + 10, 1


@dataclass
class _Account:
    cash: int = 0
    units: int = 0


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")

    def step(acc: _Account, t: dict[str, object]) -> _Account:
        if t["filled"] is not True:
            return acc
        if t["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        price = cast(int, t["fill_price_cents"])
        side = -1 if price == cast(int, t["ask_cents"]) else 1
        return _Account(acc.cash - side * price, acc.units + side)

    acc = _Account()
    for t in turns:
        acc = step(acc, t)
    mark = acc.units * cast(int, log["settlement_cents"])
    return {"cash_flow_cents": acc.cash, "inventory_end": acc.units, "inventory_mark_cents": mark, "pnl_cents": acc.cash + mark}
