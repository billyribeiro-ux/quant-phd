"""FC1 L05 lab 1: trace one seeded trade from order entry to settlement, then net a seeded batch of trades.

SIMULATED: every order, price, quantity and participant in this lab is drawn from random.Random(SEED) or written
into the code. No market, participant or settlement record is read, and the lab uses no network.

The first part traces one trade through the states of the trade lifecycle in the order the lesson gives: order
entry, matching, trade capture, clearing and settlement, then the position update. Each state is printed with its
business-day offset from the trade date (offset 0), and the lab prints whether the offsets never decrease. The
second part nets a batch of trades among five participants. It prints the gross payments, the net payments, their
ratio, and the sum of the net positions, which is zero by construction.

Units: prices are integer cents per share, quantities are whole shares, and every consideration is an exact
integer number of cents (quantity times price). A business day is a Monday to Friday; no holiday calendar is used.
The clearing offset and the settlement lag are parameters of this lab, not facts about any market. The net-to-gross
ratio is printed to three decimals, rounded half up from the exact integer quotient.
"""

from __future__ import annotations

import datetime
import itertools
import random
from collections.abc import Sequence
from dataclasses import dataclass

SEED = 2026  # seed for every draw in this lab
TRADE_DATE = datetime.date(2026, 10, 28)  # fixed, so the output does not depend on the day the lab runs
CLEARING_OFFSET = 1
SETTLEMENT_LAG = 2  # business days after the trade date at which settlement is due (a parameter)
PARTICIPANTS: tuple[str, ...] = ("P1", "P2", "P3", "P4", "P5")  # SIMULATED participant names
BATCH_SIZE = 20  # number of trades in the netting batch


@dataclass(frozen=True)
class Order:
    """A limit order: price_cents is an integer price per share, quantity a whole number of shares.

    time is the arrival sequence. At one price, a lower time has priority.
    """

    owner: str
    side: str
    price_cents: int
    quantity: int
    time: int


@dataclass(frozen=True)
class Trade:
    """A trade between a buyer and a seller at one price per share."""

    buyer: str
    seller: str
    price_cents: int
    quantity: int

    @property
    def consideration_cents(self) -> int:
        """The cash the buyer pays the seller, in integer cents: quantity times price_cents, exact."""
        return self.quantity * self.price_cents


def business_day_after(start: datetime.date, offset: int) -> datetime.date:
    """The date offset business days after start, counting Monday to Friday. An offset of 0 returns start.

    Raises ValueError for a negative offset, because no state of a trade precedes its trade date.
    """
    if offset < 0:
        raise ValueError("a business-day offset cannot be negative")
    day = start
    counted = 0
    while counted < offset:
        day += datetime.timedelta(days=1)
        if day.weekday() < 5:
            counted += 1
    return day


def match(incoming: Order, resting: Sequence[Order]) -> list[tuple[Order, int]]:
    """Match an incoming buy order against resting sell orders: best price first, then earliest arrival.

    Returns (resting order, quantity) pairs in fill order. A trade takes the resting order's price, not the
    incoming limit. Matching stops when the incoming quantity is filled or no eligible resting order is left.
    """
    if incoming.side != "buy":
        raise ValueError("this lab matches an incoming buy order")
    eligible = sorted(
        (o for o in resting if o.side == "sell" and o.price_cents <= incoming.price_cents),
        key=lambda o: (o.price_cents, o.time),
    )
    fills: list[tuple[Order, int]] = []
    remaining = incoming.quantity
    for order in eligible:
        if remaining == 0:
            break
        filled = min(remaining, order.quantity)
        fills.append((order, filled))
        remaining -= filled
    return fills


def seeded_book(rng: random.Random) -> tuple[list[Order], Order]:
    """Three resting sell orders from P2, P3 and P4, and one incoming buy order from P1 that crosses the best ask.

    Resting prices are integer cents from 10000 to 10400 (100.00 to 104.00 in currency units). The incoming
    quantity is at most the best ask's quantity, so the first fill is the whole trade.
    """
    resting: list[Order] = []
    for time in range(3):
        resting.append(
            Order(
                owner=PARTICIPANTS[time + 1],
                side="sell",
                price_cents=10_000 + rng.randint(0, 400),
                quantity=rng.randint(100, 500),
                time=time,
            )
        )
    best = min(resting, key=lambda o: (o.price_cents, o.time))
    incoming = Order(
        owner="P1",
        side="buy",
        price_cents=best.price_cents + rng.randint(0, 200),
        quantity=rng.randint(1, best.quantity),
        time=3,
    )
    return resting, incoming


def seeded_batch(rng: random.Random) -> list[Trade]:
    """BATCH_SIZE trades, each between two different participants at a seeded price and quantity.

    The price is drawn from 5000 to 20000 cents per share and the quantity from 1 to 500 shares.
    """
    trades: list[Trade] = []
    for _ in range(BATCH_SIZE):
        buyer, seller = rng.sample(PARTICIPANTS, 2)
        trades.append(
            Trade(
                buyer=buyer,
                seller=seller,
                price_cents=rng.randint(5_000, 20_000),
                quantity=rng.randint(1, 500),
            )
        )
    return trades


def net_positions(trades: Sequence[Trade]) -> dict[str, int]:
    """Each participant's net cash in integer cents: consideration received as seller minus paid as buyer.

    Every trade adds its consideration to the seller and subtracts the same amount from the buyer, so the
    positions sum to zero.
    """
    net = dict.fromkeys(PARTICIPANTS, 0)
    for trade in trades:
        net[trade.seller] += trade.consideration_cents
        net[trade.buyer] -= trade.consideration_cents
    return net


def ratio_milli_half_up(numerator: int, denominator: int) -> int:
    """The quotient numerator / denominator in thousandths, rounded half up, computed in integers.

    The result is floor(1000 * numerator / denominator + 1/2). Raises ValueError for a non-positive denominator
    or a negative numerator.
    """
    if denominator <= 0 or numerator < 0:
        raise ValueError("the ratio needs a positive denominator and a non-negative numerator")
    return (2 * 1000 * numerator + denominator) // (2 * denominator)


def fmt_ratio(milli: int) -> str:
    """A thousandths integer as a decimal with three digits after the point."""
    return f"{milli // 1000}.{milli % 1000:03d}"


def main() -> None:
    rng = random.Random(SEED)
    resting, incoming = seeded_book(rng)
    print(
        f"seed {SEED} trade_date {TRADE_DATE.isoformat()} {TRADE_DATE.strftime('%A')} "
        f"clearing_offset {CLEARING_OFFSET} settlement_lag {SETTLEMENT_LAG} units cents shares"
    )
    for order in sorted(resting, key=lambda o: (o.price_cents, o.time)):
        print(
            f"resting sell owner {order.owner} price_cents {order.price_cents} "
            f"quantity {order.quantity} time {order.time}"
        )
    print(
        f"incoming buy owner {incoming.owner} price_cents {incoming.price_cents} "
        f"quantity {incoming.quantity} time {incoming.time}"
    )

    fills = match(incoming, resting)
    print(f"fills {len(fills)}")
    best, filled = fills[0]
    trade = Trade(buyer=incoming.owner, seller=best.owner, price_cents=best.price_cents, quantity=filled)
    cash = trade.consideration_cents
    ccp_receipts = cash  # from the buyer, after novation
    ccp_payments = cash  # to the seller, after novation
    print(f"trade_price_is_resting_price {trade.price_cents == best.price_cents} incoming_limit {incoming.price_cents}")
    print(f"consideration_check {cash == trade.quantity * trade.price_cents} consideration_cents {cash}")

    states = [
        (
            "order_entry",
            0,
            f"buy {incoming.owner} limit {incoming.price_cents} quantity {incoming.quantity}; "
            f"sell {best.owner} limit {best.price_cents} quantity {best.quantity}",
        ),
        (
            "matching",
            0,
            f"one trade of {trade.quantity} shares at {trade.price_cents} cents with {trade.seller}",
        ),
        ("trade_capture", 0, f"buyer {trade.buyer} and seller {trade.seller} record the same terms"),
        (
            "clearing",
            CLEARING_OFFSET,
            f"{trade.buyer} owes the CCP {cash} cents and the CCP owes {trade.seller} {cash} cents; "
            f"the CCP net cash is {ccp_receipts - ccp_payments}",
        ),
        (
            "settlement",
            SETTLEMENT_LAG,
            f"cash {cash} cents moves {trade.buyer} to the CCP and the CCP to {trade.seller}; "
            f"{trade.quantity} shares move {trade.seller} to the CCP and the CCP to {trade.buyer}",
        ),
        (
            "position_update",
            SETTLEMENT_LAG,
            f"{trade.buyer} holds {trade.quantity} more shares; {trade.seller} holds {trade.quantity} fewer",
        ),
    ]
    for name, offset, text in states:
        day = business_day_after(TRADE_DATE, offset)
        print(f"state {name} offset {offset} date {day.isoformat()} {day.strftime('%A')} {text}")
    offsets = [offset for _, offset, _ in states]
    print(f"offsets_nondecreasing {all(a <= b for a, b in itertools.pairwise(offsets))}")

    batch = seeded_batch(rng)
    gross = sum(t.consideration_cents for t in batch)
    net = net_positions(batch)
    net_payments = sum(max(-value, 0) for value in net.values())
    payers = sum(1 for value in net.values() if value < 0)
    ratio = ratio_milli_half_up(net_payments, gross)
    print(f"batch_trades {len(batch)} gross_payments_cents {gross} net_payments_cents {net_payments}")
    print(f"net_to_gross_ratio {fmt_ratio(ratio)} basis net_payments over gross_payments, half up to three decimals")
    print(f"net_payers {payers} net_payments_at_most_gross {net_payments <= gross}")
    print(f"sum_of_net_positions_cents {sum(net.values())}")
    for participant in PARTICIPANTS:
        print(f"net {participant} cents {net[participant]}")


main()
