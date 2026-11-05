"""Alternative (round 10): class-based quote that skews both sides by the inventory and quotes size 0 at the limit. Legal under the spec."""

from __future__ import annotations

from typing import cast


class Maker:
    def __init__(self) -> None:
        self.start = 10_000

    def quote(self, state: dict[str, object]) -> tuple[int, int, int]:
        mid = self.start
        for record in cast(list[dict[str, object]], state["history"]):
            if record["filled"] is True:
                mid = cast(int, record["fill_price_cents"])
        inventory = cast(int, state["inventory"])
        skew = 5 * inventory
        size = 0 if abs(inventory) >= 5 else 1
        return mid - 5 - skew, mid + 5 - skew, size


_MAKER = Maker()


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    return _MAKER.quote(state)


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash_flow = 0
    inventory = 0
    for record in turns:
        if record["filled"] is not True:
            continue
        price = record["fill_price_cents"]
        if price is None:
            raise ValueError("a filled turn needs a fill price")
        price_i = int(cast(int, price))
        step = 1 if price_i == record["bid_cents"] else -1
        cash_flow -= step * price_i
        inventory += step
    settlement = cast(int, log["settlement_cents"])
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory,
            "inventory_mark_cents": inventory * settlement,
            "pnl_cents": cash_flow + inventory * settlement}
