"""Rung 2 completed solution: the annuity by its recurrence, and the balance update of an amortization schedule."""

import math


def nearest_cent(amount: float) -> int:
    """The nearest whole cent of a non-negative amount, with a tie going up."""
    return math.floor(amount + 0.5)


def annuity_by_recurrence(rate: float, periods: int) -> float:
    """The annuity factor sum of v**k for k = 1..periods, built one period at a time: a(k) = a(k-1) + v**k."""
    v = 1.0 / (1.0 + rate)
    total = 0.0
    for k in range(1, periods + 1):
        total = total + v**k
    return total


def main() -> None:
    rate = 0.005  # per month
    periods = 360
    recurrence = annuity_by_recurrence(rate, periods)
    closed = (1 - (1 + rate) ** -periods) / rate
    print("recurrence:", f"{recurrence:.9f}", "| closed form:", f"{closed:.9f}")
    print("difference:", f"{abs(recurrence - closed):.1e}")
    principal_cents = 25_000_000
    payment = nearest_cent(principal_cents / closed)
    balance = principal_cents
    for _ in range(12):
        interest = nearest_cent(balance * rate)
        balance = balance + interest - payment
    print("balance after 12 payments (cents):", balance)


main()
