"""BK4 lab L01: two settlement designs for one seeded day of payments among three banks.

SIMULATED. The twelve payments come from a fixed seed. They describe no real bank and no real payment system. Every
amount and every balance is an integer number of cents, so no rounding is used. The lab compares two designs:

* gross real-time settlement (RTGS): each payment settles when it is sent. A bank's peak intraday liquidity need is the
  least opening balance that keeps its running balance nonnegative after every payment, taken in sending order.
* deferred net settlement (DNS): payments wait until the end of the day, and each bank settles only its net position.
  Its net debit is the larger of zero and minus its net position. It is the amount the bank must fund at settlement.

The settlement lag in Part D is a lab parameter in business days. It is not a rule of any market. Standard library only;
no network; the only random numbers come from the seeded generator.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

SEED = 20260
BANKS = ("Bank A", "Bank B", "Bank C")
PAYMENTS = 12
MIN_DOLLARS = 100
MAX_DOLLARS = 5000
SETTLEMENT_LAG_DAYS = 1


@dataclass(frozen=True)
class Payment:
    """One payment: its place in the sending order (from 1), the sending and receiving bank, and its amount in cents."""

    seq: int
    sender: int
    receiver: int
    amount_cents: int


def make_day(seed: int) -> list[Payment]:
    """The seeded day: PAYMENTS payments between two distinct banks, in whole dollars within the bounds above."""
    rng = random.Random(seed)
    day: list[Payment] = []
    for seq in range(1, PAYMENTS + 1):
        sender, receiver = rng.sample(range(len(BANKS)), 2)
        dollars = rng.randint(MIN_DOLLARS, MAX_DOLLARS)
        day.append(Payment(seq, sender, receiver, 100 * dollars))
    return day


def net_position(day: list[Payment], bank: int) -> int:
    """Cents received minus cents sent by the bank over the whole day. A positive value is a net credit."""
    received = sum(p.amount_cents for p in day if p.receiver == bank)
    sent = sum(p.amount_cents for p in day if p.sender == bank)
    return received - sent


def rtgs_peak_need(day: list[Payment], bank: int) -> int:
    """Least opening balance in cents that keeps the running balance nonnegative after each payment, in sending order.

    The list is in sending order, so each payment is applied after the ones before it.
    """
    balance = 0
    lowest = 0
    for p in day:
        if p.sender == bank:
            balance -= p.amount_cents
        elif p.receiver == bank:
            balance += p.amount_cents
        lowest = min(lowest, balance)
    return -lowest


def dns_net_debit(day: list[Payment], bank: int) -> int:
    """Cents the bank must fund at settlement under deferred net settlement: max(0, minus its net position)."""
    return max(0, -net_position(day, bank))


def settlement_day(trade_day: int, lag: int) -> int:
    """Business day on which a trade made on trade_day settles, given a lag in business days."""
    return trade_day + lag


def main() -> None:
    day = make_day(SEED)
    print("A. The day: payments in sending order, SIMULATED, amounts in cents")
    for p in day:
        print(f"payment {p.seq:2d}: {BANKS[p.sender]} pays {BANKS[p.receiver]} {p.amount_cents:>9d} cents")

    print()
    print("B. Each bank under the two designs, in cents")
    checks: list[bool] = []
    for bank in range(len(BANKS)):
        need = rtgs_peak_need(day, bank)
        net = net_position(day, bank)
        debit = dns_net_debit(day, bank)
        checks.append(need >= debit)
        print(
            f"{BANKS[bank]}: RTGS peak need {need:>8d}; net position {net:>+9d}; "
            f"DNS net debit {debit:>8d}; RTGS need at least DNS net debit: {need >= debit}"
        )

    print()
    print("C. Checks and totals")
    nets = sum(net_position(day, b) for b in range(len(BANKS)))
    print("net positions sum to zero:", nets == 0)
    print("RTGS need is at least the DNS net debit for every bank:", all(checks))
    gross = sum(p.amount_cents for p in day)
    moved = sum(dns_net_debit(day, b) for b in range(len(BANKS)))
    print(f"gross value of the day's payments: {gross} cents")
    print(f"amount moved at settlement under DNS (sum of net debits): {moved} cents")
    funded = sum(1 for b in range(len(BANKS)) if dns_net_debit(day, b) > 0)
    print(f"banks with a positive DNS net debit: {funded} of {len(BANKS)}")
    beyond = sum(1 for b in range(len(BANKS)) if rtgs_peak_need(day, b) > dns_net_debit(day, b))
    print(f"banks whose RTGS need exceeds their DNS net debit: {beyond} of {len(BANKS)}")

    print()
    print("D. Settlement lag, a lab parameter in business days (not a market rule)")
    print(f"lag: {SETTLEMENT_LAG_DAYS} business day")
    for trade_day in range(3):
        settles = settlement_day(trade_day, SETTLEMENT_LAG_DAYS)
        print(f"trade on business day {trade_day} settles on business day {settles}")


main()
