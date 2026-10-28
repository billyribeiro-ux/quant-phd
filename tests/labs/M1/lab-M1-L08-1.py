"""M1 L08 lab 1: a full amortization schedule for an illustrative loan, in integer cents.

ILLUSTRATIVE INPUT, NOT DATA: the principal, rate and term are chosen for the example and are not a market quote.
Convention: the nominal annual rate j is compounded monthly, so the monthly rate is i = j / 12.
Part A is exact (fractions.Fraction, no conversion to cents): the balance formula, the closed-form payment, the zero
final balance, and the principal recursion P(k+1) = (1 + i) P(k). Part B is the schedule a borrower sees:
every amount is an integer number of cents, interest is taken to the nearest cent with halves going up, the
regular payment is the exact payment taken to the nearest cent, and the final payment is adjusted so the
balance closes at exactly zero. Part B reports how far its balances drift from two exact schedules: the one that
uses the rounded regular payment, and the exact-payment schedule of Part A.
Standard library only; no randomness and no network access.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

PRINCIPAL_CENTS = 25_000_000  # 250,000.00 CU
ANNUAL_NOMINAL = Fraction(6, 100)
PERIODS = 360
MONTHLY = ANNUAL_NOMINAL / 12  # i = 1/200


@dataclass(frozen=True)
class Row:
    period: int
    opening: int
    interest: int
    principal: int
    payment: int
    closing: int


def half_up(x: Fraction) -> int:
    """Nearest whole number, halves going up, for a non-negative exact amount."""
    return math.floor(x + Fraction(1, 2))


def cu(cents: int) -> str:
    """Format integer cents as currency units with two decimals, for example 1498.88."""
    sign = "-" if cents < 0 else ""
    value = abs(cents)
    return f"{sign}{value // 100:,}.{value % 100:02d}"


def exact_payment(principal: int, i: Fraction, n: int) -> Fraction:
    """Level payment P * i / (1 - (1 + i)**-n), exact."""
    return principal * i / (1 - (1 + i) ** (-n))


def exact_balance(principal: int, payment: Fraction, i: Fraction, k: int) -> Fraction:
    """Balance after k payments: P (1 + i)**k - A ((1 + i)**k - 1) / i, exact."""
    growth = (1 + i) ** k
    return principal * growth - payment * (growth - 1) / i


def cent_schedule(principal: int, i: Fraction, n: int) -> list[Row]:
    """The schedule in integer cents, with the final payment adjusted so the balance closes at zero."""
    regular = half_up(exact_payment(principal, i, n))
    rows: list[Row] = []
    balance = principal
    for k in range(1, n + 1):
        interest = half_up(Fraction(balance) * i)
        payment = regular if k < n else balance + interest
        principal_part = payment - interest
        closing = balance - principal_part
        rows.append(Row(k, balance, interest, principal_part, payment, closing))
        balance = closing
    return rows


def part_a() -> None:
    p = Fraction(PRINCIPAL_CENTS)
    payment = exact_payment(PRINCIPAL_CENTS, MONTHLY, PERIODS)
    if exact_balance(PRINCIPAL_CENTS, payment, MONTHLY, PERIODS) != 0:
        raise AssertionError("the exact balance does not reach zero after n payments")
    balance = p
    principal_prev: Fraction | None = None
    for k in range(1, PERIODS):
        interest = balance * MONTHLY
        principal_k = payment - interest
        balance = balance - principal_k
        if exact_balance(PRINCIPAL_CENTS, payment, MONTHLY, k) != balance:
            raise AssertionError(f"balance formula fails at k = {k}")
        if principal_prev is not None and principal_k != (1 + MONTHLY) * principal_prev:
            raise AssertionError(f"principal recursion fails at k = {k}")
        principal_prev = principal_k
    print(f"part A: exact balances match the closed form and the principal grows by 1 + i, for k = 1 to {PERIODS - 1}")
    print(f"part A: exact payment = {float(payment / 100):.6f} CU; exact balance after {PERIODS} payments = 0")
    print(f"part A: effective annual rate (1 + i)**12 - 1 = {float((1 + MONTHLY) ** 12 - 1):.6%}")


def part_b() -> None:
    regular = half_up(exact_payment(PRINCIPAL_CENTS, MONTHLY, PERIODS))
    rows = cent_schedule(PRINCIPAL_CENTS, MONTHLY, PERIODS)
    if len(rows) != PERIODS:
        raise AssertionError("the schedule must have one row per payment")
    if rows[-1].closing != 0:
        raise AssertionError("the final balance is not zero")
    if any(row.closing < 0 for row in rows):
        raise AssertionError("a balance went negative")
    total_interest = sum(row.interest for row in rows)
    total_paid = sum(row.payment for row in rows)
    total_principal = sum(row.principal for row in rows)
    if total_principal != PRINCIPAL_CENTS or total_interest != total_paid - PRINCIPAL_CENTS:
        raise AssertionError("totals do not reconcile to the loan")
    drift = 0
    for row in rows[:-1]:
        exact = exact_balance(PRINCIPAL_CENTS, Fraction(regular), MONTHLY, row.period)
        drift = max(drift, abs(row.closing - math.floor(exact + Fraction(1, 2))))
    exact_pay = exact_payment(PRINCIPAL_CENTS, MONTHLY, PERIODS)
    worst_gap = Fraction(0)
    worst_month = 0
    first_full_cu = 0
    for row in rows[:-1]:
        gap = row.closing - exact_balance(PRINCIPAL_CENTS, exact_pay, MONTHLY, row.period)
        if abs(gap) > abs(worst_gap):
            worst_gap, worst_month = gap, row.period
        if first_full_cu == 0 and abs(gap) >= 100:
            first_full_cu = row.period
    identity_months = [
        row.period for row in rows[1:-1] if Fraction(row.principal) == (1 + MONTHLY) * rows[row.period - 2].principal
    ]
    exact_cu = float(exact_pay / 100)
    print(f"part B: regular payment = {cu(regular)} CU (the exact payment is {exact_cu:.6f} CU)")
    print(f"part B: final payment = {cu(rows[-1].payment)} CU (adjustment {cu(rows[-1].payment - regular)} CU)")
    print(f"part B: total interest = {cu(total_interest)} CU; total paid = {cu(total_paid)} CU")
    print(f"part B: total principal = {cu(total_principal)} CU; final balance = {cu(rows[-1].closing)} CU")
    print(f"part B: largest drift from the exact schedule at the rounded regular payment (in cents) = {drift}")
    print(
        f"part B: largest drift from the exact-payment balances of Part A (in CU) = "
        f"{float(abs(worst_gap)) / 100:.2f}, at month {worst_month}"
    )
    print(f"part B: first month whose cent balance is 1 CU or more from the exact-payment balance = {first_full_cu}")
    print(
        f"part B: cent principal equals (1 + i) times the previous month's principal in {len(identity_months)} "
        f"of the {PERIODS - 2} months from 2 to {PERIODS - 1}, at months {identity_months}"
    )
    exact_interest = Fraction(PRINCIPAL_CENTS)
    for _ in range(PERIODS - 1):
        exact_interest = exact_interest * (1 + MONTHLY) - regular
    final_exact_interest = float((exact_interest * (1 + MONTHLY)) / 100)
    print(f"part B: final payment if interest is not taken to the cent = {final_exact_interest:.2f} CU")
    print("period  opening        interest     principal    payment       closing")
    for row in rows[:3] + rows[-2:]:
        print(
            f"{row.period:6d}  {cu(row.opening):>13}  {cu(row.interest):>10}  {cu(row.principal):>10}"
            f"  {cu(row.payment):>10}  {cu(row.closing):>13}"
        )


def main() -> None:
    part_a()
    part_b()


main()
