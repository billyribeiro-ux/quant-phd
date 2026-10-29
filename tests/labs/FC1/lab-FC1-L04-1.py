"""FC1 lab L04: market, limit and stop orders on one limit order book, in integer cents.

Standard library only; no network. Prices are whole cents. The order flow is generated from a fixed seed, so it is
SIMULATED and every run prints the same numbers. Two fixtures are worked by hand in the lesson and are printed first.
The matching follows the lesson's rules: a fill is at the resting order's price, the best price is taken first, and
ties go to the earlier arrival. A market order keeps no residual, so its unfilled shares are cancelled. A stop order
waits until the last trade price reaches its stop price, checked once the arriving order has finished matching, and
then it becomes a market order. Every event is checked for an uncrossed book and for share conservation,
submitted = resting + 2 * traded + cancelled, which is exact in integers.
"""

from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass

SEED = 2026
MID = 10000
OFFSET_CENTS = 20
EVENTS = 300
TRACE = 8


@dataclass
class Order:
    """An order. side is +1 for a buy and -1 for a sell. kind is limit, market or stop; a stop becomes market."""

    seq: int
    side: int
    kind: str
    qty: int
    price: int | None = None
    stop: int | None = None


class Book:
    """A limit order book with price-time priority, plus a list of stop orders that have not yet activated."""

    def __init__(self) -> None:
        self.bids: list[Order] = []
        self.asks: list[Order] = []
        self.pending: list[Order] = []
        self.last: int | None = None
        self.fills: list[tuple[int, int]] = []
        self.submitted = 0
        self.traded = 0
        self.cancelled = 0

    def resting(self) -> int:
        """Shares resting in the book on both sides."""
        return sum(o.qty for o in self.bids) + sum(o.qty for o in self.asks)

    def best_bid(self) -> int | None:
        """The highest resting bid price, or None when the bid side is empty."""
        return max((o.price for o in self.bids if o.price is not None), default=None)

    def best_ask(self) -> int | None:
        """The lowest resting ask price, or None when the ask side is empty."""
        return min((o.price for o in self.asks if o.price is not None), default=None)

    def best_resting(self, side: int) -> Order | None:
        """The order an incoming order on side meets first: best price, then earliest arrival."""
        book = self.asks if side > 0 else self.bids
        if not book:
            return None
        if side > 0:
            return min(book, key=lambda o: (o.price, o.seq))
        return min(book, key=lambda o: (-(o.price or 0), o.seq))

    def match(self, order: Order) -> None:
        """Match an arriving market or limit order, then rest any limit residual. A stop is sent here once active."""
        self.submitted += order.qty
        while order.qty > 0:
            best = self.best_resting(order.side)
            if best is None or best.price is None:
                break
            if order.kind == "limit" and order.price is not None:
                crosses = best.price <= order.price if order.side > 0 else best.price >= order.price
                if not crosses:
                    break
            fill = min(order.qty, best.qty)
            best.qty -= fill
            order.qty -= fill
            self.traded += fill
            self.last = best.price
            self.fills.append((best.price, fill))
            if best.qty == 0:
                (self.asks if order.side > 0 else self.bids).remove(best)
        if order.qty > 0 and order.kind == "limit":
            (self.bids if order.side > 0 else self.asks).append(order)
        elif order.qty > 0:
            self.cancelled += order.qty
            order.qty = 0

    def activate(self) -> int:
        """Send every pending stop whose trigger the last trade price has reached, earliest arrival first.

        A buy stop triggers when the last trade price is at or above its stop price, and a sell stop when the last
        trade price is at or below it. Each activation can trade and move the last price, so the check repeats until
        none triggers.
        """
        count = 0
        while self.last is not None:
            index = next(
                (
                    i
                    for i, o in enumerate(self.pending)
                    if o.stop is not None
                    and ((o.side > 0 and self.last >= o.stop) or (o.side < 0 and self.last <= o.stop))
                ),
                None,
            )
            if index is None:
                break
            order = self.pending.pop(index)
            order.kind = "market"
            self.match(order)
            count += 1
        return count


def fixture_walk() -> None:
    """Fixture A: a market buy of 150 shares walks two ask levels. Fixture B: a stop sell fills below its stop."""
    book = Book()
    book.match(Order(0, -1, "limit", 60, price=1000))
    book.match(Order(1, -1, "limit", 100, price=1100))
    book.match(Order(2, 1, "market", 150))
    cost = sum(price * qty for price, qty in book.fills)
    filled = sum(qty for _, qty in book.fills)
    print("Fixture A, market buy of 150 shares against asks 1000 x 60 and 1100 x 100")
    print(f"fills (price, shares): {book.fills}")
    print(f"total cost {cost} cents for {filled} shares, average {cost // filled} cents")
    print(f"shares still resting on the ask side at 1100: {sum(o.qty for o in book.asks)}")

    book = Book()
    book.match(Order(0, -1, "limit", 100, price=990))
    book.match(Order(1, 1, "limit", 100, price=985))
    book.match(Order(2, 1, "limit", 100, price=980))
    book.pending.append(Order(3, -1, "stop", 100, stop=990))
    book.activate()
    book.match(Order(4, 1, "market", 100))
    activated = book.activate()
    print("Fixture B, asks 990 x 100, bids 985 x 100 and 980 x 100, a sell stop of 100 at 990")
    print(f"market buy fills, then the stop activates: {activated} stop(s) activated")
    print(f"all fills (price, shares): {book.fills}")
    print(f"the stop sell filled at {book.fills[-1][0]} cents, below its stop of 990 cents")


def random_order(rng: random.Random, seq: int) -> Order:
    """A SIMULATED order: a limit, market or stop order on a random side, for a whole number of lots of 10 shares."""
    side = rng.choice((1, -1))
    qty = 10 * rng.randint(1, 10)
    roll = rng.random()
    if roll < 0.6:
        return Order(seq, side, "limit", qty, price=MID - side * rng.randint(0, OFFSET_CENTS))
    if roll < 0.85:
        return Order(seq, side, "market", qty)
    return Order(seq, side, "stop", qty, stop=MID + side * rng.randint(0, OFFSET_CENTS))


def label(value: int | None) -> str:
    """The price in cents, or none when the side is empty."""
    return "none" if value is None else f"{value}"


def main() -> None:
    fixture_walk()

    rng = random.Random(SEED)
    book = Book()
    kinds: Counter[str] = Counter()
    uncrossed_failures = 0
    conservation_failures = 0
    stops_activated = 0
    for seq in range(EVENTS):
        order = random_order(rng, seq)
        kinds[order.kind] += 1
        if order.kind == "stop":
            book.pending.append(order)
        else:
            book.match(order)
        stops_activated += book.activate()
        bid, ask = book.best_bid(), book.best_ask()
        if bid is not None and ask is not None and bid >= ask:
            uncrossed_failures += 1
        if book.submitted != book.resting() + 2 * book.traded + book.cancelled:
            conservation_failures += 1
        if seq < TRACE:
            print(
                f"event {seq}: {order.kind} {'buy' if order.side > 0 else 'sell'}, "
                f"best bid {label(bid)}, best ask {label(ask)}, last trade {label(book.last)}"
            )

    print(
        f"SIMULATED flow of {EVENTS} events, seed {SEED}: {kinds['limit']} limit, "
        f"{kinds['market']} market, {kinds['stop']} stop arrivals"
    )
    print(
        f"trades {len(book.fills)}, shares traded {book.traded}, stops activated {stops_activated}, "
        f"stops still pending {len(book.pending)}"
    )
    print(f"market shares cancelled {book.cancelled}, shares resting {book.resting()}")
    print(f"events with a crossed book: {uncrossed_failures}")
    print(f"events where submitted != resting + 2 * traded + cancelled: {conservation_failures}")
    print(f"best bid and ask at the end: {label(book.best_bid())} and {label(book.best_ask())}")


main()
