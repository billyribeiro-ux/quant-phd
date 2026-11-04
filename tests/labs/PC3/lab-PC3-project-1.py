"""PC3 project, rung 1: a worked example. One seeded game, one fixed quoting rule, and the replay of its log.

SIMULATED. The fair path and the arrivals are generated from random.Random(0), in the order of the project's instance
generator, which is the order of Lesson 4. No data file is read and there is no network access. Standard library only.
Money is an integer number of cents, and every accounting value is an int.

The quoting rule is fixed: bid and ask sit 10 cents either side of the last filled price, or of 10000 cents before any
fill, and each side is for one unit. The log has the fields the project specifies. The replay below computes the cash
flow, the ending inventory, the mark at the settlement value and the P&L from the fills of the log, and then checks the
identity P&L = cash flow + inventory x settlement exactly. The numbers describe this one seed and this one rule.
"""

from __future__ import annotations

import random
from typing import Any

HORIZON = 20  # turns
START_CENTS = 10_000  # v_0, in cents
MOVE_CENTS = 5  # the fair value moves by +5 or -5 cents each turn
HALF_SPREAD = 10  # cents either side of the mid
SIZE = 1  # units quoted on each side
LIMIT = 10  # inventory limit: a fill is refused when |inventory| would exceed it
SEED = 0


def draw_game(seed: int) -> tuple[list[int], list[str]]:
    """The fair path v_0 .. v_20 in cents and the 20 arrivals. Turn t draws its move first, then its arrival."""
    rng = random.Random(seed)
    path = [START_CENTS]
    arrivals: list[str] = []
    for _ in range(HORIZON):
        # Step 1a. The fair value moves by +5 cents when the draw is below 0.5, otherwise by -5 cents.
        move = MOVE_CENTS if rng.random() < 0.5 else -MOVE_CENTS
        path.append(path[-1] + move)
        # Step 1b. The arrival: an uninformed buy below 0.25, an uninformed sell below 0.5, else an informed trader.
        draw = rng.random()
        if draw < 0.25:
            arrivals.append("uninformed-buy")
        elif draw < 0.5:
            arrivals.append("uninformed-sell")
        else:
            arrivals.append("informed")
    return path, arrivals


def quote(last_fill: int | None) -> tuple[int, int, int]:
    """The fixed rule: the mid is the last filled price, or 10000 cents before any fill. Returns (bid, ask, size)."""
    # Step 2. Quote around the mid, so the market is symmetric about the last price the maker traded at.
    mid = START_CENTS if last_fill is None else last_fill
    return mid - HALF_SPREAD, mid + HALF_SPREAD, SIZE


def maker_side(arrival: str, fair: int, bid: int, ask: int) -> int:
    """+1 when the maker buys one unit at the bid, -1 when it sells one at the ask, 0 when there is no trade."""
    if arrival == "uninformed-buy":
        return -1  # the customer buys, so the maker sells at the ask
    if arrival == "uninformed-sell":
        return 1  # the customer sells, so the maker buys at the bid
    if fair > ask:
        return -1  # an informed trader buys when the fair value is strictly above the ask
    if fair < bid:
        return 1  # and sells when the fair value is strictly below the bid
    return 0


def play(seed: int) -> dict[str, Any]:
    """Play the 20 turns and return the log: the seed, the settlement value and the turn records."""
    path, arrivals = draw_game(seed)
    inventory = 0
    cash = 0
    last_fill: int | None = None
    turns: list[dict[str, Any]] = []
    for turn in range(1, HORIZON + 1):
        bid, ask, size = quote(last_fill)
        arrival = arrivals[turn - 1]
        side = maker_side(arrival, path[turn], bid, ask)
        # Step 3. A fill needs a size of at least 1, a trade on the arrival, and |inventory| within the limit after it.
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
    # Step 4. A log has exactly 20 turns. Every fill is one unit: a fill at the ask is a sale by the maker, a fill at
    # the bid is a purchase by the maker. The cash flow of a sale is +price, and of a purchase is -price.
    if len(turns) != HORIZON:
        raise ValueError("a log has exactly 20 turns")
    cash_flow = 0
    inventory = 0
    for record in turns:
        if record["filled"] is not True:
            continue
        price = int(record["fill_price_cents"])
        side = -1 if price == record["ask_cents"] else 1
        step = -side * price
        cash_flow += step
        inventory += side
        print(
            f"  turn {record['turn']:>2}: maker {'sells at the ask' if side < 0 else 'buys at the bid'} "
            f"{price} cents, cash flow {step:+d} cents, inventory {inventory:+d}"
        )
    # Step 5. The inventory is marked at the settlement value, not at the last quote, because the game is settled there.
    mark = inventory * int(log["settlement_cents"])
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }


def main() -> None:
    print("Rung 1 worked example · seed 0 · SIMULATED · quote 10 cents either side of the last fill, size 1")
    log = play(SEED)
    settlement = log["settlement_cents"]
    print(f"settlement v_{HORIZON} = {settlement} cents")
    print("replay of the fills:")
    result = replay(log)
    final = log["turns"][-1]
    fills = sum(1 for record in log["turns"] if record["filled"])
    print(f"fills = {fills} of {HORIZON} turns")
    print(f"cash_flow_cents = {result['cash_flow_cents']}")
    print(f"inventory_end = {result['inventory_end']}")
    print(f"inventory_mark_cents = {result['inventory_mark_cents']}")
    print(f"pnl_cents = {result['pnl_cents']}")
    identity = result["pnl_cents"] == result["cash_flow_cents"] + result["inventory_end"] * settlement
    print(f"identity P&L = cash flow + inventory x settlement holds: {identity}")
    print(f"cash flow equals the cash after the last turn: {result['cash_flow_cents'] == final['cash_after_cents']}")
    largest = max(abs(record["inventory_after"]) for record in log["turns"])
    print(f"largest |inventory| over the run = {largest} (limit {LIMIT}): {largest <= LIMIT}")


main()
