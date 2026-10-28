"""AC1 L05 lab 1: one SIMULATED multi-element contract, its allocation, and two timing conventions.

SIMULATED: the contract is generated from a seeded generator. No customer, filing or company is represented.
Units: integer cents for every money amount. Percentages printed below are unitless shares.

The contract has two to four performance obligations. Each obligation is either delivered at a point in time
or delivered over twelve months. The transaction price is allocated to the obligations in proportion to their
stand-alone prices, using whole cents. Revenue for a point obligation is recognized in its delivery month. Revenue
for an over-time obligation is recognized in twelve monthly shares (a straight-line measure of progress): each of
months 1 to 11 receives the amount divided by twelve, rounded down to whole cents, and month 12 takes the remainder.

Two conventions are labelled here for comparison. Convention 1 is the schedule described above. Convention 2
recognizes every over-time obligation in month 12 instead. Neither convention is claimed to be the rule of any
accounting framework. The lab shows only what each convention does to the timing of the same total.

Billing: 40 percent of the price is billed at signing (month 0). The rest is billed in twelve monthly instalments,
as equal as whole cents allow (months 1 to 12). Cash is collected when billed, so the contract balance is cumulative
billing less cumulative revenue.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

SEED = 2605
MONTHS = 12
UPFRONT_PERCENT = 40


@dataclass(frozen=True)
class Obligation:
    """One performance obligation of the SIMULATED contract."""

    name: str
    over_time: bool  # True: recognized evenly over MONTHS; False: recognized in delivery_month
    delivery_month: int  # 1..MONTHS, used only for point obligations
    standalone_cents: int  # stand-alone price in cents, the allocation weight


@dataclass(frozen=True)
class Contract:
    """A SIMULATED contract: its obligations and its transaction price in integer cents."""

    obligations: tuple[Obligation, ...]
    price_cents: int


def generate(seed: int) -> Contract:
    """Two to four obligations with seeded stand-alone prices, and a price that is 80 to 95 percent of their sum."""
    rng = random.Random(seed)
    count = rng.randint(2, 4)
    obligations: list[Obligation] = []
    for i in range(count):
        over_time = rng.random() < 0.5
        delivery = rng.randint(1, MONTHS)
        standalone = rng.randint(50_000_00, 400_000_00)
        name = f"O{i + 1}"
        obligations.append(Obligation(name, over_time, delivery, standalone))
    discount_bps = rng.randint(8000, 9500)
    total = sum(o.standalone_cents for o in obligations)
    price = total * discount_bps // 10000
    return Contract(tuple(obligations), price)


def allocate(total: int, weights: list[int]) -> list[int]:
    """Split total cents in proportion to integer weights, exactly.

    Each share starts at its floor. Each remainder is less than the weight sum, and the leftover cents are fewer than
    the number of shares, so the largest remainders (ties to the lower index) take one cent each and the result sums
    to total.
    """
    weight_sum = sum(weights)
    floors = [total * w // weight_sum for w in weights]
    remainders = [total * w - f * weight_sum for w, f in zip(weights, floors, strict=True)]
    leftover = total - sum(floors)
    order = sorted(range(len(weights)), key=lambda i: (-remainders[i], i))
    for i in order[:leftover]:
        floors[i] += 1
    return floors


def over_time_schedule(amount: int) -> list[int]:
    """Monthly shares of an amount over MONTHS months: each of the first MONTHS - 1 is the amount
    divided by MONTHS, rounded down to whole cents; the last month takes the remainder."""
    base = amount // MONTHS
    return [base] * (MONTHS - 1) + [amount - base * (MONTHS - 1)]


def revenue_schedule(contract: Contract, allocation: list[int], over_time_as_end: bool) -> list[int]:
    """Revenue in cents for months 1..MONTHS. over_time_as_end=True is convention 2 (over-time amounts in month 12)."""
    revenue = [0] * MONTHS
    for obligation, amount in zip(contract.obligations, allocation, strict=True):
        if obligation.over_time and not over_time_as_end:
            for month, share in enumerate(over_time_schedule(amount)):
                revenue[month] += share
        elif obligation.over_time:
            revenue[MONTHS - 1] += amount
        else:
            revenue[obligation.delivery_month - 1] += amount
    return revenue


def billing_schedule(price: int, upfront_percent: int) -> list[int]:
    """Billing in cents for months 0..MONTHS: upfront at month 0, the rest in instalments as equal as cents allow."""
    upfront = price * upfront_percent // 100
    instalments = allocate(price - upfront, [1] * MONTHS)
    return [upfront, *instalments]


def cumulative(values: list[int]) -> list[int]:
    """Running total in cents."""
    total = 0
    out: list[int] = []
    for value in values:
        total += value
        out.append(total)
    return out


def main() -> None:
    contract = generate(SEED)
    allocation = allocate(contract.price_cents, [o.standalone_cents for o in contract.obligations])
    total_standalone = sum(o.standalone_cents for o in contract.obligations)
    print(f"seed {SEED} obligations {len(contract.obligations)} price_cents {contract.price_cents}")
    print(f"standalone_total_cents {total_standalone}")
    for obligation, amount in zip(contract.obligations, allocation, strict=True):
        kind = "over_time" if obligation.over_time else "point"
        share = amount / contract.price_cents
        print(
            f"{obligation.name} kind {kind} delivery_month {obligation.delivery_month} "
            f"standalone_cents {obligation.standalone_cents} allocated_cents {amount} share {share:.4f}"
        )
    print(f"allocated_sum_equals_price {sum(allocation) == contract.price_cents}")

    revenue = revenue_schedule(contract, allocation, over_time_as_end=False)
    revenue_cum = cumulative(revenue)
    recognized_cum = [0, *cumulative(revenue_schedule(contract, allocation, over_time_as_end=False))]
    revenue_cum = recognized_cum[1:]
    print(f"revenue_total_cents {revenue_cum[-1]} equals_price {revenue_cum[-1] == contract.price_cents}")
    print(
        f"revenue_cum_month_6_cents {revenue_cum[5]} "
        f"share_recognized_month_6 {revenue_cum[5] / contract.price_cents:.4f}"
    )

    # Billing scenarios: 40 percent upfront (the contract's billing), and 0 percent upfront (all in instalments).
    for upfront_percent in (UPFRONT_PERCENT, 0):
        billing = billing_schedule(contract.price_cents, upfront_percent)
        billed_cum = cumulative(billing)  # months 0..MONTHS
        balance = [b - r for b, r in zip(billed_cum, recognized_cum, strict=True)]  # positive: contract liability
        print(
            f"upfront_percent {upfront_percent} billing_month_0_cents {billing[0]} billing_total_cents {billed_cum[-1]}"
        )
        print(f"upfront_percent {upfront_percent} balance_end_cents {balance[-1]}")
        print(
            f"upfront_percent {upfront_percent} balance_identity "
            f"{all(balance[m] == billed_cum[m] - recognized_cum[m] for m in range(MONTHS + 1))}"
        )
        print(
            f"upfront_percent {upfront_percent} max_contract_liability_cents {max(balance)} "
            f"max_contract_asset_cents {-min(balance)} months_with_contract_asset {sum(1 for b in balance if b < 0)}"
        )

    # Convention 2: the same allocation with every over-time obligation recognized in month 12.
    revenue_2 = revenue_schedule(contract, allocation, over_time_as_end=True)
    revenue_2_cum = cumulative(revenue_2)
    print(f"convention_2_month_6_cents {revenue_2_cum[5]} convention_2_total_cents {revenue_2_cum[-1]}")
    print(f"totals_equal_under_both_conventions {revenue_2_cum[-1] == revenue_cum[-1]}")
    print(f"month_6_difference_cents {revenue_cum[5] - revenue_2_cum[5]}")

    # Convention-1 revenue from the over-time obligations through month 6: the first six monthly shares of each.
    over_time_month_6 = sum(
        sum(over_time_schedule(amount)[:6])
        for obligation, amount in zip(contract.obligations, allocation, strict=True)
        if obligation.over_time
    )
    print(f"over_time_convention_1_month_6_cents {over_time_month_6}")
    print(f"month_6_difference_equals_over_time_revenue {revenue_cum[5] - revenue_2_cum[5] == over_time_month_6}")


main()
