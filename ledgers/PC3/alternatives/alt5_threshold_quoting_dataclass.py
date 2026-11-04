"""Alternative 5: a threshold rule that quotes size 0 unless the spread is at least 10 cents, and a dataclass per fill."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

HORIZON = 20
START_CENTS = 10_000
HALF_SPREAD = 5
MIN_SPREAD = 10
SIZE = 1


@dataclass(frozen=True)
class Fill:
    """A fill of one unit: side +1 when the maker bought at the bid, -1 when it sold at the ask."""

    side: int
    price_cents: int


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = START_CENTS
    for record in cast(list[dict[str, object]], state["history"]):
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    bid, ask = mid - HALF_SPREAD, mid + HALF_SPREAD
    size = SIZE if ask - bid >= MIN_SPREAD else 0
    return bid, ask, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != HORIZON:
        raise ValueError("a log has exactly 20 turns")
    settlement = cast(int, log["settlement_cents"])
    fills: list[Fill] = []
    for turn in turns:
        if turn["filled"] is not True:
            continue
        if turn["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        price = cast(int, turn["fill_price_cents"])
        fills.append(Fill(side=-1 if price == turn["ask_cents"] else 1, price_cents=price))
    cash_flow = 0
    units = 0
    for fill in fills:
        cash_flow -= fill.side * fill.price_cents
        units += fill.side
    mark = units * settlement
    return {"cash_flow_cents": cash_flow, "inventory_end": units, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
