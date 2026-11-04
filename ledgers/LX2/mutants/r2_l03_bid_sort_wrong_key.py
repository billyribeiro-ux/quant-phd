"""LX2 lab L03: cancel-to-fill ratios per trader on a seeded SIMULATED order flow, exact in Fraction.

Standard library only. No network and no data. The order flow is generated from a fixed seed, so it is SIMULATED and
every run prints the same numbers. The book follows the rules of the FC1 lesson on order types: price-time priority,
a fill at the resting order's price, limit and market orders, and an unfilled remainder of a market order that is
cancelled. This lab has no stop orders.

Each trader has a cancel rate, a whole percentage that the generator uses as its input. A trader's cancel removes the
remaining quantity of one of that trader's resting orders. A market order's unfilled remainder is cancelled by the
book, and that cancellation is not counted as a trader cancel.

For each trader the lab prints the cancel count, the fill count and the exact ratio cancels / fills. A fill is one
execution in which one of the trader's orders takes part. An execution between two orders of the same trader counts
twice for that trader. A trader with no fills has no ratio, and the lab prints "none" for it.

The threshold DEMO_THRESHOLD = 2 is a demonstration value, chosen before the run. It is not a regulatory threshold, and
the lab takes it from no source. The flag says only that the ratio exceeds 2 on this flow.
After every event the lab checks two things: the book is not crossed, and the share identity
entered = resting + 2 * traded + market cancelled + trader cancelled holds, where the traded term counts each executed
share once for each of its two orders. It also checks that a tally of the event log reproduces the book's order and
cancel counts per trader. The lab does not decide whether any trader's behaviour is lawful, and it does not model
latency, brokers or several venues.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Final

SEED: Final[int] = 2026
EVENTS: Final[int] = 400
TRADERS: Final[int] = 6
REFERENCE_PRICE: Final[int] = 10000  # cents
PRICE_BAND: Final[int] = 20  # limit prices lie within this many cents of the reference price
QTY_UNIT: Final[int] = 10  # shares; an order has 1 to 5 units
QTY_STEPS: Final[int] = 5
MARKET_PCT: Final[int] = 10  # percent of submissions that are market orders
CANCEL_PCT: Final[tuple[int, ...]] = (5, 10, 25, 40, 60, 85)  # generator input, one per trader
DEMO_THRESHOLD: Final[Fraction] = Fraction(2)


@dataclass
class Order:
    """One order. Price is in whole cents and is ignored for a market order. Shares are whole numbers."""

    trader: int
    side: int  # +1 for a buy, -1 for a sell
    price: int
    market: bool
    remaining: int
    seq: int  # arrival number; a lower number arrived earlier


def bid_priority(order: Order) -> tuple[int, int]:
    """Sort key for resting bids: the highest price first, then the earliest arrival."""
    return (-order.price, order.seq)


def ask_priority(order: Order) -> tuple[int, int]:
    """Sort key for resting asks: the lowest price first, then the earliest arrival."""
    return (order.price, order.seq)


def crosses(incoming: Order, resting: Order) -> bool:
    """Whether the incoming order can trade with the resting order at the resting order's price."""
    if incoming.market:
        return True
    if incoming.side > 0:
        return resting.price <= incoming.price
    return resting.price >= incoming.price


class Book:
    """A limit order book with price-time priority, and the counts the lab reports."""

    def __init__(self) -> None:
        self.bids: list[Order] = []
        self.asks: list[Order] = []
        self.orders = [0] * TRADERS
        self.fills = [0] * TRADERS
        self.cancels = [0] * TRADERS
        self.entered = 0
        self.executions = 0
        self.traded = 0
        self.market_cancelled = 0
        self.trader_cancelled = 0

    def resting(self) -> int:
        """Shares resting in the book."""
        return sum(o.remaining for o in self.bids) + sum(o.remaining for o in self.asks)

    def submit(self, order: Order) -> None:
        """Match an arriving order against the opposite side, then rest any limit remainder."""
        self.orders[order.trader] += 1
        self.entered += order.remaining
        opposite = self.asks if order.side > 0 else self.bids
        while order.remaining > 0 and opposite and crosses(order, opposite[0]):
            best = opposite[0]
            q = min(order.remaining, best.remaining)
            order.remaining -= q
            best.remaining -= q
            self.traded += q
            self.executions += 1
            self.fills[order.trader] += 1
            self.fills[best.trader] += 1
            if best.remaining == 0:
                opposite.pop(0)
        if order.remaining > 0:
            if order.market:
                self.market_cancelled += order.remaining
                order.remaining = 0
            elif order.side > 0:
                self.bids.append(order)
                self.bids.sort(key=ask_priority)
            else:
                self.asks.append(order)
                self.asks.sort(key=ask_priority)

    def cancel(self, target: Order) -> None:
        """Remove a resting order of its own trader and count the cancel against that trader."""
        if target.side > 0:
            self.bids = [o for o in self.bids if o is not target]
        else:
            self.asks = [o for o in self.asks if o is not target]
        self.trader_cancelled += target.remaining
        self.cancels[target.trader] += 1
        target.remaining = 0

    def best_bid(self) -> int | None:
        """The highest resting bid price, or None when no bid rests."""
        return self.bids[0].price if self.bids else None

    def best_ask(self) -> int | None:
        """The lowest resting ask price, or None when no ask rests."""
        return self.asks[0].price if self.asks else None


def run() -> tuple[Book, list[tuple[str, int]], int, int]:
    """Generate the seeded flow and apply it to a book. Returns the book, the event log, and the two failure counts."""
    rng = random.Random(SEED)
    book = Book()
    log: list[tuple[str, int]] = []
    crossed = 0
    identity_failures = 0
    for seq in range(EVENTS):
        trader = rng.randrange(TRADERS)
        own = [o for o in book.bids + book.asks if o.trader == trader]
        if own and rng.randrange(100) < CANCEL_PCT[trader]:
            book.cancel(own[rng.randrange(len(own))])
            log.append(("cancel", trader))
        else:
            side = 1 if rng.randrange(2) == 0 else -1
            qty = QTY_UNIT * rng.randrange(1, QTY_STEPS + 1)
            market = rng.randrange(100) < MARKET_PCT
            price = REFERENCE_PRICE + rng.randrange(-PRICE_BAND, PRICE_BAND + 1)
            book.submit(Order(trader, side, price, market, qty, seq))
            log.append(("market" if market else "limit", trader))
        bid, ask = book.best_bid(), book.best_ask()
        if bid is not None and ask is not None and bid >= ask:
            crossed += 1
        if book.entered != book.resting() + 2 * book.traded + book.market_cancelled + book.trader_cancelled:
            identity_failures += 1
    return book, log, crossed, identity_failures


def tally_mismatches(book: Book, log: list[tuple[str, int]]) -> int:
    """Trader counts that the event log does not reproduce: orders submitted and cancels, per trader."""
    orders = [0] * TRADERS
    cancels = [0] * TRADERS
    for kind, trader in log:
        if kind == "cancel":
            cancels[trader] += 1
        else:
            orders[trader] += 1
    mismatches = sum(orders[t] != book.orders[t] for t in range(TRADERS))
    return mismatches + sum(cancels[t] != book.cancels[t] for t in range(TRADERS))


def main() -> None:
    book, log, crossed, identity_failures = run()
    total_orders = sum(book.orders)
    total_cancels = sum(book.cancels)
    print(
        f"SIMULATED flow: {EVENTS} events from seed {SEED}, {TRADERS} traders, reference price {REFERENCE_PRICE} "
        f"cents, limit prices within {PRICE_BAND} cents, quantities of {QTY_UNIT} to {QTY_UNIT * QTY_STEPS} shares"
    )
    print(
        f"orders {total_orders}, executions {book.executions}, shares traded {book.traded}, "
        f"trader cancel events {total_cancels}"
    )
    print(f"events with a crossed book: {crossed}")
    print(f"events where entered != resting + 2 * traded + market cancelled + trader cancelled: {identity_failures}")
    print(
        f"shares resting {book.resting()}, market shares cancelled {book.market_cancelled}, "
        f"trader shares cancelled {book.trader_cancelled}"
    )
    print(f"fills total {sum(book.fills)}, which equals 2 * executions: {sum(book.fills) == 2 * book.executions}")
    print(f"tally from the event log disagrees with the book in {tally_mismatches(book, log)} trader counts")
    print(
        f"demonstration threshold {DEMO_THRESHOLD} (not a regulatory threshold): "
        f"flag when cancels / fills > {DEMO_THRESHOLD}"
    )
    print("trader  cancel_pct  orders  cancels  fills  ratio  flag")
    flagged = 0
    ratios: list[Fraction] = []
    for t in range(TRADERS):
        fills = book.fills[t]
        if fills == 0:
            ratio_text, flag = "none", "undefined"
        else:
            ratio = Fraction(book.cancels[t], fills)
            ratios.append(ratio)
            ratio_text = str(ratio)
            is_flagged = ratio > DEMO_THRESHOLD
            flagged += is_flagged
            flag = "yes" if is_flagged else "no"
        print(f"{t:<7} {CANCEL_PCT[t]:<11} {book.orders[t]:<7} {book.cancels[t]:<8} {fills:<6} {ratio_text:<6} {flag}")
    print(f"traders flagged: {flagged} of {TRADERS}")
    print(f"largest ratio {max(ratios)}: a threshold at or above it flags no trader on this flow")


main()
