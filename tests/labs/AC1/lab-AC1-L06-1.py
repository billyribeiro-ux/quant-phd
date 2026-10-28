"""AC1 L06 lab 1: one SIMULATED lease, its liability and right-of-use asset roll-forward, and an articulation check.

SIMULATED: the lease is generated from a seeded generator. No lessor, lessee or filing is represented.
Units: integer cents for every money amount, and the discount rate is in basis points (1 bp = 0.01 percent a year).

The lease has fixed annual payments in arrears over a term of four to seven years, starting at the beginning of
year 1. The liability at commencement is the present value of the payments at the discount rate. The right-of-use
asset at commencement equals that liability, because the generated lease has no initial direct costs, prepayments
or incentives.

Each year the liability accrues interest at the discount rate and is reduced by the payment. The right-of-use asset
is amortized straight-line over the term. Two expense patterns for the same lease are compared:
pattern F (front-loaded) is interest plus amortization, and pattern S (straight-line) spreads the total payments
evenly over the term. Both patterns are conventions of this lab; the lab does not claim either is the required
treatment of any framework.

The only floating-point step is the present value, which is rounded once to whole cents. Every later step is integer
arithmetic. The final payment absorbs the schedule's rounding, and the lab prints the size of that adjustment.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

SEED = 2606


@dataclass(frozen=True)
class Lease:
    """A SIMULATED fixed-payment lease: annual payments in arrears, all money in integer cents."""

    term_years: int
    payment_cents: int
    rate_bps: int  # annual discount rate in basis points


def generate(seed: int) -> Lease:
    """Seeded term (4 to 7 years), annual payment (120,000.00 to 300,000.00 CU), and rate (4.00 to 8.00 percent)."""
    rng = random.Random(seed)
    term = rng.randint(4, 7)
    payment = rng.randint(120_000_00, 300_000_00)
    rate = rng.randint(400, 800)
    return Lease(term, payment, rate)


def present_value_cents(lease: Lease) -> int:
    """Present value of the contractual payments at commencement, rounded once to whole cents."""
    rate = lease.rate_bps / 10_000
    pv = sum(lease.payment_cents / (1 + rate) ** t for t in range(1, lease.term_years + 1))
    return round(pv)


def interest_cents(opening: int, rate_bps: int) -> int:
    """One year of interest in cents on an opening balance, rounded half up in integer arithmetic."""
    return (opening * rate_bps + 5_000) // 10_000


def straight_line(total: int, years: int) -> list[int]:
    """Equal yearly shares of a total in cents; the last year takes the remainder so the shares sum to the total."""
    base = total // years
    return [base] * (years - 1) + [total - base * (years - 1)]


@dataclass(frozen=True)
class Year:
    """One year of the roll-forward, every amount in integer cents."""

    opening_liability: int
    interest: int
    payment: int
    closing_liability: int
    rou_opening: int
    amortization: int
    rou_closing: int


def roll_forward(lease: Lease, initial_liability: int) -> tuple[list[Year], int]:
    """The liability and right-of-use schedule. Returns the years and the final payment's adjustment in cents.

    The last year's payment is the balance owed plus that year's interest, so the liability ends at exactly zero.
    Its difference from the contractual payment is the schedule's rounding residual, returned as the second value.
    """
    amort = straight_line(initial_liability, lease.term_years)
    years: list[Year] = []
    liability = initial_liability
    rou = initial_liability
    adjustment = 0
    for year in range(lease.term_years):
        interest = interest_cents(liability, lease.rate_bps)
        if year == lease.term_years - 1:
            payment = liability + interest
            adjustment = payment - lease.payment_cents
        else:
            payment = lease.payment_cents
        closing = liability + interest - payment
        rou_closing = rou - amort[year]
        years.append(Year(liability, interest, payment, closing, rou, amort[year], rou_closing))
        liability = closing
        rou = rou_closing
    return years, adjustment


def main() -> None:
    lease = generate(SEED)
    initial = present_value_cents(lease)
    years, adjustment = roll_forward(lease, initial)
    print(
        f"seed {SEED} term_years {lease.term_years} annual_payment_cents {lease.payment_cents} "
        f"rate_bps {lease.rate_bps}"
    )
    print(f"initial_liability_cents {initial} initial_rou_asset_cents {initial}")
    expense_f = [y.interest + y.amortization for y in years]
    total_payments = lease.payment_cents * (lease.term_years - 1) + years[-1].payment
    expense_s = straight_line(total_payments, lease.term_years)
    for t, y in enumerate(years, start=1):
        print(
            f"year {t} opening_liability {y.opening_liability} interest {y.interest} payment {y.payment} "
            f"closing_liability {y.closing_liability} rou_opening {y.rou_opening} amortization {y.amortization} "
            f"rou_closing {y.rou_closing} expense_front_loaded {expense_f[t - 1]} "
            f"expense_straight_line {expense_s[t - 1]}"
        )
    print(f"final_payment_cents {years[-1].payment} contractual_payment_cents {lease.payment_cents}")
    print(f"final_payment_adjustment_cents {adjustment}")
    print(f"liability_ends_at_zero {years[-1].closing_liability == 0} rou_ends_at_zero {years[-1].rou_closing == 0}")

    # Identity 1: the total expense of each pattern equals the total payments.
    print(f"sum_payments_cents {total_payments}")
    print(f"sum_expense_front_loaded_cents {sum(expense_f)} sum_expense_straight_line_cents {sum(expense_s)}")
    print(f"total_expense_identity {sum(expense_f) == total_payments and sum(expense_s) == total_payments}")

    # Identity 2 (articulation): each year, the change in (ROU asset less liability) equals cash paid
    # less the pattern F expense.
    articulation = all(
        (y.rou_closing - y.closing_liability) - (y.rou_opening - y.opening_liability) == y.payment - expense_f[t]
        for t, y in enumerate(years)
    )
    print(f"articulation_every_year {articulation}")
    print(f"net_position_change_total_cents {years[-1].rou_closing - years[-1].closing_liability}")

    # Difference between the patterns, by year: front-loaded expense minus straight-line expense.
    difference = [f - s for f, s in zip(expense_f, expense_s, strict=True)]
    print(
        f"expense_difference_year_1_cents {difference[0]} "
        f"expense_difference_year_{lease.term_years}_cents {difference[-1]}"
    )
    print(f"cumulative_difference_zero_at_end {sum(difference) == 0}")


main()
