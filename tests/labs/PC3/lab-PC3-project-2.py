"""PC3 project, rung 2: the completed replay. The seeded game of rung 1, with the two lines the completion removes.

SIMULATED. The fair path and the arrivals come from random.Random(0), in the order of Lesson 4 and of the project's
instance generator. No data file is read and there is no network access. Standard library only. Money is an integer
number of cents.

The quoting rule is the rung 1 rule: 10 cents either side of the last filled price, or of 10000 cents before any
fill, for one unit. This file is the completed solution. On the page, the lines that define cash_flow and mark are
blanked with ___, and every other line is the same as here.
"""

from __future__ import annotations

import random
from typing import Any

HORIZON = 20  # turns
START_CENTS = 10_000  # v_0, in cents
MOVE_CENTS = 5  # the fair value moves by +5 or -5 cents each turn
HALF_SPREAD = 10  # cents either side of the mid
SIZE = 1  # units quoted on each side
LIMIT = 10  # inventory limit
SEED = 0


def draw_game(seed: int) -> tuple[list[int], list[str]]:
    """The fair path v_0 .. v_20 in cents and the 20 arrivals, drawn in the order of Lesson 4."""
    rng = random.Random(seed)
    path = [START_CENTS]
    arrivals: list[str] = []
    for _ in range(HORIZON):
        move = MOVE_CENTS if rng.random() < 0.5 else -MOVE_CENTS
        path.append(path[-1] + move)
        draw = rng.random()
        if draw < 0.25:
            arrivals.append("uninformed-buy")
        elif draw < 0.5:
            arrivals.append("uninformed-sell")
        else:
            arrivals.append("informed")
    return path, arrivals


def maker_side(arrival: str, fair: int, bid: int, ask: int) -> int:
    """+1 when the maker buys one unit at the bid, -1 when it sells one at the ask, 0 when there is no trade."""
    if arrival == "uninformed-buy":
        return -1
    if arrival == "uninformed-sell":
        return 1
    if fair > ask:
        return -1
    if fair < bid:
        return 1
    return 0


def play(seed: int) -> dict[str, Any]:
    """Play the 20 turns with the rung 1 rule and return the log."""
    path, arrivals = draw_game(seed)
    inventory = 0
    cash = 0
    last_fill: int | None = None
    turns: list[dict[str, Any]] = []
    for turn in range(1, HORIZON + 1):
        mid = START_CENTS if last_fill is None else last_fill
        bid, ask, size = mid - HALF_SPREAD, mid + HALF_SPREAD, SIZE
        arrival = arrivals[turn - 1]
        side = maker_side(arrival, path[turn], bid, ask)
        filled = side != 0 and size >= 1 and abs(inventory + side) <= LIMIT
        price: int | None = None
        if filled:
            price = ask if side < 0 else bid
            inventory += side
            cash += -side * price
            last_fill = price
        turns.append(
            {
                "turn": turn,
                "bid_cents": bid,
                "ask_cents": ask,
                "size": size,
                "arrival": arrival,
                "filled": filled,
                "fill_price_cents": price,
                "inventory_after": inventory,
                "cash_after_cents": cash,
            }
        )
    return {"seed": seed, "settlement_cents": path[HORIZON], "turns": turns}


def replay(log: dict[str, Any]) -> dict[str, int]:
    """Replay the fills of a log: the cash flow, the ending inventory, the mark at settlement and the P&L, in cents."""
    turns: list[dict[str, Any]] = log["turns"]
    if len(turns) != HORIZON:
        raise ValueError("a log has exactly 20 turns")
    fills: list[tuple[int, int]] = []
    for record in turns:
        if record["filled"] is True:
            if record["fill_price_cents"] is None:
                raise ValueError("a filled turn needs a fill price")
            price = int(record["fill_price_cents"])
            fills.append((1 if price == record["bid_cents"] else -1, price))
    inventory = sum(side for side, _ in fills)
    cash_flow = sum(-side * price for side, price in fills)
    mark = inventory * int(log["settlement_cents"])
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }


def main() -> None:
    print("Rung 2 completed replay · seed 0 · SIMULATED · quote 10 cents either side of the last fill, size 1")
    log = play(SEED)
    result = replay(log)
    fills = sum(1 for record in log["turns"] if record["filled"])
    print(f"settlement v_{HORIZON} = {log['settlement_cents']} cents, fills = {fills} of {HORIZON} turns")
    print(f"cash_flow_cents = {result['cash_flow_cents']}")
    print(f"inventory_end = {result['inventory_end']}")
    print(f"inventory_mark_cents = {result['inventory_mark_cents']}")
    print(f"pnl_cents = {result['pnl_cents']}")
    identity = result["pnl_cents"] == result["cash_flow_cents"] + result["inventory_end"] * log["settlement_cents"]
    print(f"identity P&L = cash flow + inventory x settlement holds: {identity}")


main()
