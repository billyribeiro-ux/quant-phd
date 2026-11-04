"""BK4 lab L02: multilateral netting before and after a central counterparty, for one seeded SIMULATED set of trades.

SIMULATED. Four members and six trades come from a fixed seed. They describe no real market, member or clearing house.
Each trade has one payer, who owes one receiver the trade amount, and the two parties are distinct members. Every amount
is an integer number of cents. The lab uses no rounding except the floor in the basis-point reduction, which is an
integer division of nonnegative integers.

Before novation, each trade is a bilateral claim of its receiver on its payer. After novation, the central counterparty
is the counterparty to each side, so each member has one net obligation to the counterparty: the sum of what it is owed
minus the sum of what it owes. A positive net obligation is owed to the member by the counterparty. A negative one is
owed by the member to the counterparty.

Standard library only; no network; the only random numbers come from the seeded generator.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

SEED = 2026
MEMBERS = 4
TRADES = 6
MIN_DOLLARS = 500
MAX_DOLLARS = 20000


@dataclass(frozen=True)
class Trade:
    """One trade: its number from 1, the payer that owes the amount, the receiver, and the amount in cents."""

    seq: int
    payer: int
    receiver: int
    amount_cents: int


def make_trades(seed: int) -> list[Trade]:
    """The seeded trade set: TRADES trades, each between two distinct members, in whole dollars."""
    rng = random.Random(seed)
    trades: list[Trade] = []
    for seq in range(1, TRADES + 1):
        payer, receiver = rng.sample(range(MEMBERS), 2)
        dollars = rng.randint(MIN_DOLLARS, MAX_DOLLARS)
        trades.append(Trade(seq, payer, receiver, 100 * dollars))
    return trades


def gross_notional(trades: list[Trade]) -> int:
    """Sum of all trade amounts in cents."""
    return sum(t.amount_cents for t in trades)


def receivable(trades: list[Trade], member: int) -> int:
    """Cents the member is owed, summed over the trades it receives, before any netting."""
    return sum(t.amount_cents for t in trades if t.receiver == member)


def payable(trades: list[Trade], member: int) -> int:
    """Cents the member owes, summed over the trades it pays, before any netting."""
    return sum(t.amount_cents for t in trades if t.payer == member)


def net_obligation(trades: list[Trade], member: int) -> int:
    """Receivable minus payable in cents. Positive: the counterparty owes the member. Negative: the member owes it."""
    return receivable(trades, member) - payable(trades, member)


def netted_amount(trades: list[Trade]) -> int:
    """Cents that must be paid after netting: the sum of the positive net obligations."""
    return sum(max(0, net_obligation(trades, m)) for m in range(MEMBERS))


def reduction_basis_points(gross: int, netted: int) -> int:
    """Reduction from gross notional to the netted amount, in whole basis points of gross, floored."""
    return (10000 * (gross - netted)) // gross


def main() -> None:
    trades = make_trades(SEED)
    gross = gross_notional(trades)

    print("A. The trades, SIMULATED, amounts in cents")
    for t in trades:
        print(f"trade {t.seq}: member {t.payer + 1} owes member {t.receiver + 1} {t.amount_cents:>8d} cents")

    print()
    print("B. Before novation: bilateral claims, in cents")
    for m in range(MEMBERS):
        print(f"member {m + 1}: receivable {receivable(trades, m):>8d}; payable {payable(trades, m):>8d}")
    exposure_before = sum(receivable(trades, m) for m in range(MEMBERS))
    print(f"gross notional: {gross} cents")
    print("gross exposure before novation (sum of receivables) equals gross notional:", exposure_before == gross)

    print()
    print("C. After novation: one net obligation per member to the counterparty, in cents")
    nets = [net_obligation(trades, m) for m in range(MEMBERS)]
    for m, net in enumerate(nets):
        print(f"member {m + 1}: net obligation {net:>+9d}")
    print("net obligations sum to zero:", sum(nets) == 0)

    print()
    print("D. Amount to be paid after netting, and the reduction from gross notional")
    netted = netted_amount(trades)
    owed_by_members = sum(max(0, -n) for n in nets)
    print(f"amount paid after netting (sum of positive net obligations): {netted} cents")
    print("payments in equal the payments out after netting:", netted == owed_by_members)
    print("after netting is at most gross notional:", netted <= gross)
    print(f"reduction from gross notional: {gross - netted} cents")
    print(f"reduction in basis points of gross notional, floored: {reduction_basis_points(gross, netted)}")


main()
