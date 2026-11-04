"""Verifier alternative 6: a legal policy that quotes size 0 on every third turn, and a replay written with zip over the fills.

Correct by the rules of project.html section "Rung 3 · Specification": the quote is bid below ask with size 0..5, and the
replay sums the fill cash flows and the fill inventory from the log, marking at the settlement value.
"""

from __future__ import annotations

from typing import cast

HORIZON = 20
START_CENTS = 10_000
HALF_SPREAD = 10


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = START_CENTS
    for record in cast(list[dict[str, object]], state["history"]):
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    turn = cast(int, state["turn"])
    size = 0 if turn % 3 == 0 else 1
    return mid - HALF_SPREAD, mid + HALF_SPREAD, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != HORIZON:
        raise ValueError("a log has exactly 20 turns")
    settlement = cast(int, log["settlement_cents"])
    filled = [record for record in turns if record["filled"] is True]
    for record in filled:
        if record["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
    prices = [cast(int, record["fill_price_cents"]) for record in filled]
    signs = [-1 if price == record["ask_cents"] else 1 for price, record in zip(prices, filled, strict=True)]
    cash_flow = sum(-sign * price for sign, price in zip(signs, prices, strict=True))
    inventory = sum(signs)
    mark = inventory * settlement
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
