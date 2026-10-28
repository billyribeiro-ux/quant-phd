"""AC1 L04 lab 1: one SIMULATED transaction set, two recognition rules, two cash-flow presentations.

SIMULATED: every transaction is generated from a seeded generator. No filing is read and no company is represented.
Units: integer cents for every money amount. The ratios printed below are unitless.

Rule A recognizes a prepaid service in full when it is paid. Rule B recognizes the same payment in four shares over
the four quarters the service covers: the first three are the payment divided by four, rounded down, and the last
takes the remainder. These two rules are labelled conventions of this lab. The lab does not claim
that either one is the rule of any accounting framework.

Presentation 1 places interest paid in operating cash flow. Presentation 2 places it in financing cash flow. Both
presentations start from the same cash movements, so the only difference between them is the section that holds
the interest.

Every identity printed as True is an algebraic consequence of the construction, not an empirical result.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

SEED = 2604
QUARTERS = 8
TERM = 4  # quarters covered by one prepaid service under rule B
PREPAID_PROBABILITY = 1.0 / 3.0


@dataclass(frozen=True)
class Quarter:
    """One quarter of SIMULATED activity; every field is an amount in integer cents."""

    cash_sales: int  # sales collected in the quarter of sale
    credit_sales: int  # sales collected one quarter later
    prepaid_paid: int  # service paid in advance in this quarter (zero when none is bought)
    opex: int  # operating expenses, paid in the quarter they are incurred
    interest: int  # interest paid in the quarter


def generate(seed: int) -> list[Quarter]:
    """Eight quarters of seeded activity: one of each item per quarter, and a prepaid purchase with probability 1/3."""
    rng = random.Random(seed)
    quarters: list[Quarter] = []
    for _ in range(QUARTERS):
        cash_sales = rng.randint(50_000_00, 120_000_00)
        credit_sales = rng.randint(20_000_00, 60_000_00)
        prepaid_paid = rng.randint(40_000_00, 90_000_00) if rng.random() < PREPAID_PROBABILITY else 0
        opex = rng.randint(30_000_00, 70_000_00)
        interest = rng.randint(2_000_00, 5_000_00)
        quarters.append(Quarter(cash_sales, credit_sales, prepaid_paid, opex, interest))
    return quarters


def shares(amount: int) -> list[int]:
    """Split an amount into TERM whole-cent shares that sum to it exactly; the last share takes the remainder."""
    base = amount // TERM
    return [base] * (TERM - 1) + [amount - base * (TERM - 1)]


def expense_rule_b(quarters: list[Quarter]) -> list[int]:
    """Rule B expense in cents for each quarter: each prepaid payment spread over the TERM quarters it covers."""
    expense = [0] * QUARTERS
    for start, item in enumerate(quarters):
        for offset, share in enumerate(shares(item.prepaid_paid)):
            if start + offset < QUARTERS:
                expense[start + offset] += share
    return expense


def cumulative(values: list[int]) -> list[int]:
    """Running total in cents from the first quarter."""
    total = 0
    out: list[int] = []
    for value in values:
        total += value
        out.append(total)
    return out


def main() -> None:
    quarters = generate(SEED)
    entries = sum(1 for q in quarters for amount in (q.cash_sales, q.credit_sales, q.opex, q.interest) if amount)
    entries += sum(1 for q in quarters if q.prepaid_paid)
    print(f"seed {SEED} quarters {QUARTERS} ledger_entries {entries}")

    revenue = [q.cash_sales + q.credit_sales for q in quarters]
    collections = [0] + [quarters[t - 1].credit_sales for t in range(1, QUARTERS)]  # one-quarter collection lag
    receipts = [q.cash_sales + c for q, c in zip(quarters, collections, strict=True)]
    paid = [q.prepaid_paid + q.opex + q.interest for q in quarters]

    # Net income under each rule: revenue less the expenses that rule recognizes in the quarter.
    expense_b = expense_rule_b(quarters)
    ni_a = [r - q.opex - q.interest - q.prepaid_paid for r, q in zip(revenue, quarters, strict=True)]
    ni_b = [r - q.opex - q.interest - e for r, q, e in zip(revenue, quarters, expense_b, strict=True)]

    cash_change = [r - p for r, p in zip(receipts, paid, strict=True)]
    cash_end = cumulative(cash_change)
    receivable_end = [q.credit_sales for q in quarters]
    prepaid_balance_b = [
        c - e for c, e in zip(cumulative([q.prepaid_paid for q in quarters]), cumulative(expense_b), strict=True)
    ]

    for t, q in enumerate(quarters):
        print(
            f"q{t} revenue {revenue[t]} ni_rule_a {ni_a[t]} ni_rule_b {ni_b[t]} "
            f"cash_change {cash_change[t]} prepaid_balance_b {prepaid_balance_b[t]} interest {q.interest}"
        )

    # Identity 1: the cash balance does not depend on the recognition rule.
    cash_rule_a = cumulative(cash_change)[-1]
    cash_rule_b = cash_end[-1]
    print(f"cash_end_cents_rule_a {cash_rule_a} cash_end_cents_rule_b {cash_rule_b}")
    print(f"cash_identical_across_rules {cash_rule_a == cash_rule_b}")

    # Identity 2: at each quarter end, cash plus receivables equals cumulative net income under the rule.
    # Under rule B the unexpired prepaid balance is an asset as well.
    cum_ni_a = cumulative(ni_a)
    cum_ni_b = cumulative(ni_b)
    balance_a = all(c + r == n for c, r, n in zip(cash_end, receivable_end, cum_ni_a, strict=True))
    balance_b = all(
        c + r + p == n for c, r, p, n in zip(cash_end, receivable_end, prepaid_balance_b, cum_ni_b, strict=True)
    )
    print(f"balance_identity_rule_a {balance_a}")
    print(f"balance_identity_rule_b {balance_b}")

    # Identity 3: over the horizon, the cumulative difference in net income is minus the unexpired prepaid balance.
    diff_cum = cum_ni_a[-1] - cum_ni_b[-1]
    print(f"cum_ni_rule_a_cents {cum_ni_a[-1]} cum_ni_rule_b_cents {cum_ni_b[-1]}")
    print(f"cum_difference_cents {diff_cum} unexpired_prepaid_end_rule_b_cents {prepaid_balance_b[-1]}")
    print(f"cumulative_difference_identity {diff_cum == -prepaid_balance_b[-1]}")

    # Presentation 1 (interest in operating) and presentation 2 (interest in financing) of the same cash movements.
    cfo_1 = cash_change
    cfo_2 = [c + q.interest for c, q in zip(cash_change, quarters, strict=True)]
    cff_2 = [-q.interest for q in quarters]
    presentation_ok = all(a - b == -q.interest for a, b, q in zip(cfo_1, cfo_2, quarters, strict=True))
    totals_ok = all(a == b + c for a, b, c in zip(cash_change, cfo_2, cff_2, strict=True))
    print(f"presentation_identity {presentation_ok and totals_ok}")
    print(f"interest_moved_total_cents {sum(q.interest for q in quarters)}")
    print(f"cfo_presentation_1_total_cents {sum(cfo_1)} cfo_presentation_2_total_cents {sum(cfo_2)}")
    print(f"cff_presentation_2_total_cents {sum(cff_2)}")


import sys
quarters = generate(SEED)
print("prepaid_paid", [q.prepaid_paid for q in quarters])
print("expense_b", expense_rule_b(quarters))
