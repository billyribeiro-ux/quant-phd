"""The public engine of the PC3 market-making game: the rules of Lesson 4, played for one seed.

SIMULATED. The fair path and the arrivals come from ``instance.make_instance(seed)``. No data file is read and there
is no network access. Standard library only. Money is an integer number of cents.

``play(quote, seed)`` runs the 20 turns. Before each turn's arrival it calls ``quote(state)`` once, with the state
the page describes (turn, inventory, cash_cents, max_size, limit and history). The quote is
``(bid_cents, ask_cents, size)``. The engine refuses an illegal quote with ValueError, and it returns the log: the
seed, the settlement value and the 20 turn records.

Rules, as Lesson 4 states them:

* a customer buys one unit at the maker's ask (the maker sells) or sells one unit at the maker's bid (the maker buys);
* an uninformed buy or sell names its direction; an informed trader buys at the ask when the fair value is above the
  ask, sells at the bid when the fair value is below the bid, and otherwise does not trade;
* a fill needs a quoted size of at least 1, and the inventory after the fill must satisfy |inventory| <= 10. A breach is
  not an exception: the order is not filled, and the record says ``filled: false``.

The engine does not show the fair value to the policy. The log does show the settlement value, after the last turn.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from instance import HORIZON, make_instance

MAX_SIZE = 5  # largest quoted size, in units
LIMIT = 10  # inventory limit: a fill is refused when |inventory| would exceed it

QuoteFn = Callable[[dict[str, object]], tuple[int, int, int]]


def maker_side(arrival: str, fair_cents: int, bid_cents: int, ask_cents: int) -> int:
    """+1 when the maker buys one unit (a customer sells at the bid), -1 when the maker sells one (a customer buys
    at the ask), 0 when the arrival does not trade. Whether a trade fills is decided in ``play``."""
    if arrival == "uninformed-buy":
        return -1
    if arrival == "uninformed-sell":
        return 1
    if fair_cents > ask_cents:
        return -1
    if fair_cents < bid_cents:
        return 1
    return 0


def play(quote: QuoteFn, seed: int) -> dict[str, Any]:
    """Play the 20 turns of the game for ``seed`` with the policy ``quote``. Returns the log.

    The log has the keys ``seed``, ``settlement_cents`` (the fair value v_20) and ``turns``: 20 records, each with
    the keys ``turn``, ``bid_cents``, ``ask_cents``, ``size``, ``arrival``, ``filled``, ``fill_price_cents`` (the
    price, or None when not filled), ``inventory_after`` and ``cash_after_cents``.

    Raises ValueError with "bid must be below ask" for a crossed or locked quote, and with "size must lie in 0..5" for a
    size outside that range. Nothing else is refused.
    """
    instance = make_instance(seed)
    path: list[int] = instance["fair_path_cents"]
    arrivals: list[str] = instance["arrivals"]
    inventory = 0
    cash = 0
    turns: list[dict[str, Any]] = []
    for turn in range(1, HORIZON + 1):
        state: dict[str, object] = {
            "turn": turn,
            "inventory": inventory,
            "cash_cents": cash,
            "max_size": MAX_SIZE,
            "limit": LIMIT,
            "history": [dict(record) for record in turns],
        }
        bid, ask, size = quote(state)
        if bid >= ask:
            raise ValueError(f"turn {turn}: bid must be below ask")
        if not 0 <= size <= MAX_SIZE:
            raise ValueError(f"turn {turn}: size must lie in 0..{MAX_SIZE}")
        arrival = arrivals[turn - 1]
        side = maker_side(arrival, path[turn], bid, ask)
        filled = side != 0 and size >= 1 and abs(inventory + side) <= LIMIT
        price: int | None = None
        if filled:
            price = ask if side < 0 else bid
            inventory += side
            cash += -side * price
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
    return {"seed": int(seed), "settlement_cents": path[HORIZON], "turns": turns}
