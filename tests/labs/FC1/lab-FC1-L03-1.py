"""FC1 lab L03: a dealer's quotes, closed sequences of trades and the bid-ask spread, in integer cents.

Standard library only; no network. The customer order flow is generated from a fixed seed, so it is SIMULATED
and every run prints the same numbers. Quotes are ask = mid + HALF and bid = mid - HALF, with mid and HALF in
whole cents, so the quoted spread is 2 * HALF cents and every amount below is an exact integer. Each check is an
exact integer identity, not a tolerance test. Part A and Part B check the identity of Proposition 2.3 and Corollary 2.4.
Part C enumerates the asks of the two-dealer tick game of Proposition 3.2 on a finite grid.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

SEED = 2026
HALF = 2
MID = 10000
COST = 100
SHARES_PER_SIDE = 1000
TICK_GRID = 10


@dataclass(frozen=True)
class Trade:
    """One trade with a customer. sign is +1 when the customer buys (the dealer sells at its ask), -1 when it sells."""

    sign: int
    shares: int
    mid: int


def trade_price(trade: Trade, half: int) -> int:
    """Price in cents at which the dealer trades: mid + half for a customer buy, mid - half for a customer sell."""
    return trade.mid + trade.sign * half


def dealer_cash(trades: list[Trade], half: int) -> int:
    """Cash the dealer receives in cents: the sum of sign * price * shares over the trades."""
    return sum(t.sign * trade_price(t, half) * t.shares for t in trades)


def dealer_inventory(trades: list[Trade]) -> int:
    """Shares the dealer holds: a customer buy lowers it and a customer sell raises it."""
    return -sum(t.sign * t.shares for t in trades)


def mark_to_mid(trades: list[Trade], half: int, terminal_mid: int) -> int:
    """Dealer cash plus the inventory valued at the terminal mid, in cents."""
    return dealer_cash(trades, half) + dealer_inventory(trades) * terminal_mid


def spread_capture(trades: list[Trade], half: int) -> int:
    """Half the quoted spread times the total shares traded, in cents."""
    return half * sum(t.shares for t in trades)


def mid_move_term(trades: list[Trade], terminal_mid: int) -> int:
    """The sum of sign * shares * (mid at the trade - terminal mid), in cents."""
    return sum(t.sign * t.shares * (t.mid - terminal_mid) for t in trades)


def partition(rng: random.Random, total: int, parts: int) -> list[int]:
    """Split total whole shares into parts positive amounts at random cut points."""
    cuts = sorted(rng.sample(range(1, total), parts - 1))
    bounds = [0, *cuts, total]
    return [bounds[i + 1] - bounds[i] for i in range(parts)]


def closed_sequence(rng: random.Random, mid: int) -> list[Trade]:
    """Trades at one fixed mid that buy and sell SHARES_PER_SIDE shares each, so inventory ends at zero."""
    buys = partition(rng, SHARES_PER_SIDE, 8)
    sells = partition(rng, SHARES_PER_SIDE, 6)
    trades = [Trade(1, q, mid) for q in buys] + [Trade(-1, q, mid) for q in sells]
    rng.shuffle(trades)
    return trades


def walking_mid_sequence(rng: random.Random, start: int) -> tuple[list[Trade], int]:
    """The closed sequence with a mid that moves by an integer step in -3 to 3 cents before each trade.

    Returns the trades and the terminal mid, which is the mid at the last trade.
    """
    mid = start
    walked: list[Trade] = []
    for trade in closed_sequence(rng, start):
        mid += rng.randint(-3, 3)
        walked.append(Trade(trade.sign, trade.shares, mid))
    return walked, mid


def profit_twice(ask: int, rival: int, cost: int, shares: int) -> int:
    """Twice the dealer's profit in cents when it asks ask against a rival ask.

    Customers buy all shares from the lower ask. A tie splits the shares equally, so the profit is halved;
    doubling keeps the arithmetic in whole cents.
    """
    if ask < rival:
        return 2 * (ask - cost) * shares
    if ask == rival:
        return (ask - cost) * shares
    return 0


def equilibria(cost: int, shares: int, asks: list[int]) -> list[tuple[int, int]]:
    """Ask pairs from the grid at which neither dealer has a deviation in the grid that strictly raises its profit."""
    found: list[tuple[int, int]] = []
    for a in asks:
        for b in asks:
            first = all(profit_twice(d, b, cost, shares) <= profit_twice(a, b, cost, shares) for d in asks)
            second = all(profit_twice(d, a, cost, shares) <= profit_twice(b, a, cost, shares) for d in asks)
            if first and second:
                found.append((a, b))
    return found


def main() -> None:
    rng = random.Random(SEED)
    spread = 2 * HALF

    trades = closed_sequence(rng, MID)
    buy_q = sum(t.shares for t in trades if t.sign == 1)
    sell_q = sum(t.shares for t in trades if t.sign == -1)
    cash = dealer_cash(trades, HALF)
    print(f"Part A, mid fixed at {MID} cents: {len(trades)} trades")
    print(f"customer buys {buy_q} shares and customer sells {sell_q} shares")
    print(f"dealer inventory after the sequence: {dealer_inventory(trades)} shares")
    print(f"cash received: {cash} cents; quoted spread {spread} cents times {buy_q} shares: {spread * buy_q} cents")
    print(f"cash equals spread times volume: {cash == spread * buy_q}")

    walked, terminal = walking_mid_sequence(rng, MID)
    capture = spread_capture(walked, HALF)
    move = mid_move_term(walked, terminal)
    pnl = mark_to_mid(walked, HALF, terminal)
    total = sum(t.shares for t in walked)
    print(f"Part B, mid moves between trades: {len(walked)} trades, terminal mid {terminal} cents")
    print(f"dealer inventory after the sequence: {dealer_inventory(walked)} shares, total shares {total}")
    print(f"spread capture, half the spread times total shares: {capture} cents")
    print(f"mid-move term, sum of sign * shares * (mid - terminal mid): {move} cents")
    print(f"mark-to-mid P&L: {pnl} cents")
    print(f"mark-to-mid P&L equals spread capture plus mid-move term: {pnl == capture + move}")

    asks = list(range(COST, COST + TICK_GRID + 1))
    found = equilibria(COST, SHARES_PER_SIDE, asks)
    listed = ", ".join(f"({a}, {b})" for a, b in found)
    print(f"Part C, tick game with cost {COST} cents, asks {COST} to {COST + TICK_GRID} cents: {len(asks) ** 2} pairs")
    print(f"pairs with no strictly profitable deviation in the grid: {listed}")
    print(f"every pair found is symmetric: {all(a == b for a, b in found)}")


main()
