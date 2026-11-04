"""Verifier alternative 8 (round 2): a quote 25 cents either side of the last fill (or of 10000 before any fill), size 2
that falls to 0 once |inventory| reaches the limit of 10; a replay that splits the fills into purchases and sales with
comprehensions and checks the named refusal in a loop before either.

Correct by the rules of project.html section "Rung 3 · Specification": every quote has bid below ask and size in 0..5, and
the replay returns the fill cash flow, the fill inventory, the mark at the settlement value and their sum.
"""

from __future__ import annotations

from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, object]], state["history"])
    last_fill = next(
        (cast(int, record["fill_price_cents"]) for record in reversed(history) if record["filled"] is True),
        10_000,
    )
    inventory = cast(int, state["inventory"])
    size = 0 if abs(inventory) >= 10 else 2
    return last_fill - 25, last_fill + 25, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    for record in turns:
        if record["filled"] is True and record["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    filled = [record for record in turns if record["filled"] is True]
    purchases = [cast(int, r["fill_price_cents"]) for r in filled if r["fill_price_cents"] == r["bid_cents"]]
    sales = [cast(int, r["fill_price_cents"]) for r in filled if r["fill_price_cents"] != r["bid_cents"]]
    cash = sum(sales) - sum(purchases)
    units = len(purchases) - len(sales)
    mark = units * cast(int, log["settlement_cents"])
    return {"cash_flow_cents": cash, "inventory_end": units, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
