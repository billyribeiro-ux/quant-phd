"""Round 11 alternative: the mid is the last fill price, shifted by one cent per 1000 cents of cash, with a 2-cent spread each side of 1; size 1."""

from __future__ import annotations

from typing import cast


class Maker:
    def __init__(self) -> None:
        self.last_fill: int | None = None

    def quote(self, state: dict[str, object]) -> tuple[int, int, int]:
        if state["turn"] == 1:
            self.last_fill = None
        history = cast(list[dict[str, object]], state["history"])
        for record in history:
            if record["filled"] is True:
                self.last_fill = cast(int, record["fill_price_cents"])
        base = self.last_fill if self.last_fill is not None else 10_000
        mid = base + cast(int, state["cash_cents"]) // 1_000
        return mid - 1, mid + 1, 1


_MAKER = Maker()


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    return _MAKER.quote(state)


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    settlement = cast(int, log["settlement_cents"])
    cash_flow = 0
    inventory = 0
    for record in turns:
        if record["filled"] is not True:
            continue
        if record["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        price = cast(int, record["fill_price_cents"])
        side = -1 if price == record["ask_cents"] else 1
        cash_flow -= side * price
        inventory += side
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": inventory * settlement,
        "pnl_cents": cash_flow + inventory * settlement,
    }
