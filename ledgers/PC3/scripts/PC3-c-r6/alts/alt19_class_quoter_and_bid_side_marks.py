"""Alternative correct implementation 19: a class quoter with a quote method, the sides read from the bid, and an integer-only replay with explicit int() casts."""

from __future__ import annotations

from typing import Any


class Maker:
    def __init__(self) -> None:
        self.reference = 10_000

    def quote(self, state: dict[str, Any]) -> tuple[int, int, int]:
        for r in state["history"]:
            if r["filled"] is True:
                self.reference = int(r["fill_price_cents"])
        return self.reference - 10, self.reference + 10, 1


_MAKER = Maker()


def quote(state: dict[str, Any]) -> tuple[int, int, int]:
    if state["turn"] == 1:
        _MAKER.reference = 10_000
    return _MAKER.quote(state)


def replay(log: dict[str, Any]) -> dict[str, int]:
    turns = log["turns"]
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash_flow = 0
    inventory = 0
    for r in turns:
        if not r["filled"]:
            continue
        if r["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        price = int(r["fill_price_cents"])
        if price == int(r["bid_cents"]):
            inventory += 1
            cash_flow -= price
        else:
            inventory -= 1
            cash_flow += price
    mark = int(inventory) * int(log["settlement_cents"])
    return {"cash_flow_cents": int(cash_flow), "inventory_end": int(inventory), "inventory_mark_cents": mark, "pnl_cents": int(cash_flow) + mark}
