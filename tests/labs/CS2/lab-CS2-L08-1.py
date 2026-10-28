"""CS2 L08 lab 1: an order book of integer-cent price levels with FIFO queues, checked against a sorted scan.

SIMULATED: prices, quantities and the message stream come from a fixed seed; no real order flow is used.
Prices are integer cents (10000 is 100.00 in currency units) and quantities are integer shares; the code
raises an error for any other type. The book's prices and quantities are never floats; Part A passes one
float to show that it is refused. Each side of the book keeps a sorted list of the prices that have resting
orders, and each price keeps a first-in first-out queue of its orders. An
incoming limit order first trades against resting orders on the other side that it crosses, at the resting
order's price, taking the best price first and then the earliest arrival; any remainder rests in the book.
A cancel removes a resting order by its id.

Part A: hand-built cases of price-time priority, cancellation and refusal of bad input. Part B: 400 seeded
messages, each applied to the book and to a reference that keeps a flat list of resting orders and sorts the crossing
candidates by (price, arrival number) on every match. After every message the trades must be identical, and the best bid
and best ask must equal a sorted scan of the reference. Part C: operation counts. The binary search over each
sorted price list is counted, and the queue steps are counted against the number of orders added. The lab
counts operations only; it does not time anything. Standard library only, no network access, no randomness
other than the seeded generator.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import cast

LCG_MULT = 1103515245
LCG_INC = 12345
LCG_MOD = 2**31
SEED = 20261029
MESSAGES = 400
MID = 10000
HALF_RANGE = 20
MAX_QTY = 20
CANCEL_PERCENT = 25


class Lcg:
    """A linear congruential generator on integers, so every run draws the same numbers."""

    def __init__(self, seed: int) -> None:
        self.state = seed % LCG_MOD

    def below(self, n: int) -> int:
        """Return an integer k with 0 <= k < n."""
        if n < 1:
            raise ValueError("below needs n >= 1")
        self.state = (LCG_MULT * self.state + LCG_INC) % LCG_MOD
        return (self.state >> 16) % n


@dataclass
class Order:
    """A resting order. qty is the remaining shares; it is 0 once the order is filled or cancelled."""

    oid: int
    side: str
    price: int
    qty: int


@dataclass(frozen=True)
class Trade:
    """One execution: qty shares at price cents, between the resting order maker and the incoming order taker."""

    price: int
    qty: int
    maker: int
    taker: int


@dataclass
class Level:
    """All orders resting at one price, in arrival order. head is the first entry not yet passed."""

    queue: list[Order] = field(default_factory=list)
    head: int = 0
    live: int = 0


@dataclass
class Counts:
    """Operation counts. queue_steps counts entries the head passed. Binary-search tests go to Book.search_log."""

    orders_added: int = 0
    queue_steps: int = 0
    levels_created: int = 0
    levels_removed: int = 0


def check_order(price: object, qty: object) -> None:
    """Refuse anything but integer cents and integer shares, with an error that says why."""
    if type(price) is not int or type(qty) is not int:
        raise TypeError("prices must be integer cents and quantities integer shares")
    if qty < 1:
        raise ValueError("a quantity must be at least 1 share")
    if price < 1:
        raise ValueError("a price must be at least 1 cent")


class Book:
    """Two sides, each a sorted price list and a dict of FIFO levels, plus an index of live orders by id."""

    def __init__(self) -> None:
        self.prices: dict[str, list[int]] = {"B": [], "S": []}
        self.levels: dict[str, dict[int, Level]] = {"B": {}, "S": {}}
        self.live: dict[int, Order] = {}
        self.counts = Counts()
        self.search_log: list[tuple[int, int]] = []

    def best(self, side: str) -> int | None:
        """Best bid ("B": highest price) or best ask ("S": lowest price), or None when that side is empty."""
        prices = self.prices[side]
        if not prices:
            return None
        return prices[-1] if side == "B" else prices[0]

    def _search(self, prices: list[int], price: int) -> int:
        """Binary search for the index of price in a sorted list: the first index whose entry is not below price."""
        lo, hi, comparisons = 0, len(prices), 0
        while lo < hi:
            mid = (lo + hi) // 2
            comparisons += 1
            if prices[mid] < price:
                lo = mid + 1
            else:
                hi = mid
        self.search_log.append((len(prices), comparisons))
        return lo

    def _front(self, level: Level) -> Order | None:
        """The earliest live entry at a level. The head passes each entry it finds with qty 0, once."""
        while level.head < len(level.queue) and level.queue[level.head].qty == 0:
            level.head += 1
            self.counts.queue_steps += 1
        if level.head < len(level.queue):
            return level.queue[level.head]
        return None

    def _rest(self, order: Order) -> None:
        prices = self.prices[order.side]
        levels = self.levels[order.side]
        level = levels.get(order.price)
        if level is None:
            index = self._search(prices, order.price)
            prices.insert(index, order.price)
            level = Level()
            levels[order.price] = level
            self.counts.levels_created += 1
        level.queue.append(order)
        level.live += 1
        self.live[order.oid] = order

    def _drop_if_empty(self, side: str, price: int) -> None:
        level = self.levels[side][price]
        if level.live != 0:
            return
        prices = self.prices[side]
        index = self._search(prices, price)
        if index >= len(prices) or prices[index] != price:
            raise RuntimeError("a price level is missing from its sorted list")
        del prices[index]
        del self.levels[side][price]
        self.counts.levels_removed += 1

    def submit(self, side: str, price: int, qty: int, oid: int) -> list[Trade]:
        """Match an incoming limit order against the other side, then rest any remainder. Returns its trades."""
        check_order(price, qty)
        self.counts.orders_added += 1
        opposite = "S" if side == "B" else "B"
        incoming = Order(oid, side, price, qty)
        trades: list[Trade] = []
        while incoming.qty > 0:
            best = self.best(opposite)
            if best is None or (side == "B" and best > price) or (side == "S" and best < price):
                break
            level = self.levels[opposite][best]
            resting = self._front(level)
            if resting is None:
                raise RuntimeError("a level in the price index has no live order")
            fill = min(incoming.qty, resting.qty)
            resting.qty -= fill
            incoming.qty -= fill
            trades.append(Trade(best, fill, resting.oid, oid))
            if resting.qty == 0:
                level.live -= 1
                del self.live[resting.oid]
            self._drop_if_empty(opposite, best)
        if incoming.qty > 0:
            self._rest(incoming)
        return trades

    def cancel(self, oid: int) -> bool:
        """Remove a live order by id. Returns False when no live order has that id."""
        order = self.live.pop(oid, None)
        if order is None:
            return False
        level = self.levels[order.side][order.price]
        order.qty = 0
        level.live -= 1
        self._drop_if_empty(order.side, order.price)
        return True


@dataclass
class Resting:
    oid: int
    side: str
    price: int
    qty: int


class Reference:
    """A flat list of resting orders. Every match sorts the candidates by (price, arrival number)."""

    def __init__(self) -> None:
        self.resting: list[Resting] = []

    def submit(self, side: str, price: int, qty: int, oid: int) -> list[Trade]:
        opposite = "S" if side == "B" else "B"
        if side == "B":
            candidates = [r for r in self.resting if r.side == opposite and r.price <= price]
            candidates.sort(key=lambda r: (r.price, r.oid))
        else:
            candidates = [r for r in self.resting if r.side == opposite and r.price >= price]
            candidates.sort(key=lambda r: (-r.price, r.oid))
        trades: list[Trade] = []
        remaining = qty
        for r in candidates:
            if remaining == 0:
                break
            fill = min(remaining, r.qty)
            trades.append(Trade(r.price, fill, r.oid, oid))
            r.qty -= fill
            remaining -= fill
        self.resting = [r for r in self.resting if r.qty > 0]
        if remaining > 0:
            self.resting.append(Resting(oid, side, price, remaining))
        return trades

    def cancel(self, oid: int) -> bool:
        before = len(self.resting)
        self.resting = [r for r in self.resting if r.oid != oid]
        return len(self.resting) < before

    def best(self, side: str) -> int | None:
        """A sorted scan: sort the prices on this side, then take the first (ask) or last (bid)."""
        prices = sorted(r.price for r in self.resting if r.side == side)
        if not prices:
            return None
        return prices[-1] if side == "B" else prices[0]


def describe(trades: list[Trade]) -> str:
    if not trades:
        return "none"
    return "; ".join(f"{t.qty} at {t.price} from order {t.maker}" for t in trades)


def part_a() -> None:
    book = Book()
    book.submit("S", 10000, 5, 1)
    book.submit("S", 10000, 3, 2)
    book.submit("S", 10000, 4, 3)
    book.submit("S", 10010, 2, 4)
    trades = book.submit("B", 10010, 7, 5)
    print(f"part A: buy 7 at 10010 trades: {describe(trades)}")
    print(f"part A: best bid {book.best('B')}, best ask {book.best('S')}, resting orders {len(book.live)}")
    book.submit("B", 9990, 1, 6)
    print(f"part A: buy 1 at 9990 does not cross and rests: best bid {book.best('B')}, best ask {book.best('S')}")
    book.cancel(3)
    trades = book.submit("B", 10000, 5, 7)
    print(f"part A: after cancelling order 3, buy 5 at 10000 trades: {describe(trades)}")
    print(f"part A: best bid {book.best('B')}, best ask {book.best('S')}, ask price levels {len(book.prices['S'])}")
    try:
        book.submit("B", cast(int, 100.5), 1, 8)
    except TypeError as exc:
        print(f"part A: a float price is refused: {exc}")
    try:
        book.submit("B", 10000, 0, 9)
    except ValueError as exc:
        print(f"part A: a zero quantity is refused: {exc}")


def part_b() -> None:
    gen = Lcg(SEED)
    book, ref = Book(), Reference()
    next_id = 1
    trades_total = 0
    cancels = 0
    crossing_messages = 0
    for step in range(MESSAGES):
        live_ids = sorted(r.oid for r in ref.resting)
        if live_ids and gen.below(100) < CANCEL_PERCENT:
            oid = live_ids[gen.below(len(live_ids))]
            if not (book.cancel(oid) and ref.cancel(oid)):
                raise AssertionError(f"step {step}: cancel of live order {oid} failed")
            cancels += 1
        else:
            side = "B" if gen.below(2) == 0 else "S"
            price = MID - HALF_RANGE + gen.below(2 * HALF_RANGE + 1)
            qty = 1 + gen.below(MAX_QTY)
            book_trades = book.submit(side, price, qty, next_id)
            ref_trades = ref.submit(side, price, qty, next_id)
            if book_trades != ref_trades:
                raise AssertionError(f"step {step}: trades differ from the reference")
            trades_total += len(book_trades)
            crossing_messages += bool(book_trades)
            next_id += 1
        if book.best("B") != ref.best("B") or book.best("S") != ref.best("S"):
            raise AssertionError(f"step {step}: best bid or ask differs from the sorted scan")
        if set(book.live) != {r.oid for r in ref.resting}:
            raise AssertionError(f"step {step}: resting orders differ from the reference")
    print(f"part B: messages applied: {MESSAGES}; cancels: {cancels}; new orders: {next_id - 1}")
    print(f"part B: messages that traded: {crossing_messages}; executions: {trades_total}")
    print("part B: after every message, trades, best bid and best ask match the reference")
    print(f"part B: final best bid {book.best('B')}, best ask {book.best('S')}, resting orders {len(book.live)}")


def part_c() -> None:
    gen = Lcg(SEED)
    book, ref = Book(), Reference()
    next_id = 1
    for _ in range(MESSAGES):
        live_ids = sorted(r.oid for r in ref.resting)
        if live_ids and gen.below(100) < CANCEL_PERCENT:
            oid = live_ids[gen.below(len(live_ids))]
            book.cancel(oid)
            ref.cancel(oid)
        else:
            side = "B" if gen.below(2) == 0 else "S"
            price = MID - HALF_RANGE + gen.below(2 * HALF_RANGE + 1)
            qty = 1 + gen.below(MAX_QTY)
            book.submit(side, price, qty, next_id)
            ref.submit(side, price, qty, next_id)
            next_id += 1
    counts = book.counts
    if counts.queue_steps > counts.orders_added:
        raise AssertionError("the queue head passed more entries than orders were added")
    for length, comparisons in book.search_log:
        if comparisons > length.bit_length():
            raise AssertionError(f"a search over {length} prices made {comparisons} comparisons")
    worst = max((c for _, c in book.search_log), default=0)
    print(f"part C: orders added: {counts.orders_added}; queue steps: {counts.queue_steps} (at most orders added)")
    print(f"part C: price levels created: {counts.levels_created}; removed: {counts.levels_removed}")
    print(f"part C: binary searches: {len(book.search_log)}; largest comparison count: {worst}")
    print("part C: every search met its bound of floor(log2 L) + 1 comparisons, where L is the list length")


def main() -> None:
    part_a()
    part_b()
    part_c()


main()
