"""Alternative correct solution: the mid is the last filled price, size 0 when |inventory| is 9 or more, replay by reduce over a dataclass list of fills.

Legal quotes on every turn (bid 10 cents below and ask 10 cents above the mid, size 0 or 1), replay sums the fills with functools.reduce.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from typing import cast


@dataclass(frozen=True)
class Fill:
    side: int
    price: int


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, object]], state["history"])
    inventory = cast(int, state["inventory"])
    mid = 10_000
    for record in history:
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    size = 0 if abs(inventory) >= 9 else 1
    return mid - 10, mid + 10, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    fills: list[Fill] = []
    for record in turns:
        if record["filled"] is not True:
            continue
        price = record["fill_price_cents"]
        if price is None:
            raise ValueError("a filled turn needs a fill price")
        p = cast(int, price)
        fills.append(Fill(side=1 if p == record["bid_cents"] else -1, price=p))
    cash_flow = reduce(lambda acc, f: acc - f.side * f.price, fills, 0)
    inventory = reduce(lambda acc, f: acc + f.side, fills, 0)
    settlement = cast(int, log["settlement_cents"])
    mark = inventory * settlement
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }
