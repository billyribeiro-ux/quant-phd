"""Student error: quote keeps the mid in a module global between turns, read from the previous turn record only, and resets it on turn 1, so a game never sees another game's mid. Behaviourally the same as the reference on every game the engine plays, but it keeps state outside the state it is given (project.html: 'it keeps nothing between turns or games outside that state').
"""

from __future__ import annotations

from typing import cast

_MID: dict[str, int] = {"mid": 10_000}


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, object]], state["history"])
    if state["turn"] == 1:
        _MID["mid"] = 10_000
    for record in history[-1:]:
        if record["filled"] is True:
            _MID["mid"] = cast(int, record["fill_price_cents"])
    mid = _MID["mid"]
    return mid - 10, mid + 10, 1


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
        cash_flow += -side * price
        inventory += side
    mark = inventory * settlement
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }
