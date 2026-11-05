"""Alternative 20: a class-based maker that ignores the history and quotes a constant mid, with a fold-based replay."""

from __future__ import annotations

from functools import reduce


class Maker:
    """Quotes 7 cents either side of 10000 cents, size 2 inside |inventory| <= 4 and size 1 beyond."""

    MID = 10_000
    HALF = 7

    def quote(self, state: dict[str, object]) -> tuple[int, int, int]:
        inventory = int(state["inventory"])  # type: ignore[call-overload]
        size = 2 if abs(inventory) <= 4 else 1
        return self.MID - self.HALF, self.MID + self.HALF, size


_MAKER = Maker()


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    return _MAKER.quote(state)


def _step(acc: tuple[int, int], record: dict[str, object]) -> tuple[int, int]:
    cash, inventory = acc
    if record["filled"] is not True:
        return acc
    price_raw = record["fill_price_cents"]
    if price_raw is None:
        raise ValueError("a filled turn needs a fill price")
    price = int(price_raw)  # type: ignore[call-overload]
    side = 1 if price == int(record["bid_cents"]) else -1  # type: ignore[call-overload]
    return cash - side * price, inventory + side


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = list(log["turns"])  # type: ignore[call-overload]
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash, inventory = reduce(_step, turns, (0, 0))
    mark = inventory * int(log["settlement_cents"])  # type: ignore[call-overload]
    return {"pnl_cents": cash + mark, "cash_flow_cents": cash, "inventory_mark_cents": mark, "inventory_end": inventory}
