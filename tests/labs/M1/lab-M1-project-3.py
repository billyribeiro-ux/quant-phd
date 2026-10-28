"""Rung 3 reference numbers: the payments, the schedule totals and the closed forms the report quotes.

Standard library only. Copy this file into report/run_report.py, then replace the schedule and factor calls
with calls to your annuity_engine module. Your module must print the same numbers.
"""

import math


def nearest_cent(amount: float) -> int:
    """The nearest whole cent of a non-negative amount, with a tie going up."""
    return math.floor(amount + 0.5)


def annuity_factor(rate: float, periods: int) -> float:
    """PV of one unit paid at the end of each of `periods` periods at a per-period rate; rate 0 gives periods."""
    if rate == 0:
        return float(periods)
    return (1 - (1 + rate) ** -periods) / rate


def main() -> None:
    principal_cents = 30_000_000  # $300,000.00, an illustrative loan
    annual_rate = 0.045  # nominal, compounded monthly
    months = 300
    i = annual_rate / 12
    factor = annuity_factor(i, months)
    payment = nearest_cent(principal_cents / factor)
    balance = principal_cents
    interest_total = 0
    principal_total = 0
    payments_total = 0
    for month in range(1, months + 1):
        interest = nearest_cent(balance * i)
        paid = payment if month < months else balance + interest
        principal = paid - interest
        balance -= principal
        interest_total += interest
        principal_total += principal
        payments_total += paid
    print("level payment (cents):", payment)
    first_interest = nearest_cent(principal_cents * i)
    print("month 1 (cents): payment", payment, "| interest", first_interest, "| principal", payment - first_interest)
    print("final payment (cents):", paid, "| minus level payment:", paid - payment)
    print("final balance (cents):", balance)
    bound = months * (1 + i) ** months + 1
    print("bound on final minus level payment (cents):", f"{bound:.4f}")
    print("final minus level within bound:", abs(paid - payment) <= bound)
    print("sum of principal = loan:", principal_total == principal_cents)
    print("total interest (cents):", interest_total)
    print("total paid (cents):", payments_total)
    print("annuity factor:", f"{factor:.9f}")
    print("annuity due factor:", f"{factor * (1 + i):.9f}")
    print("perpetuity factor at 5%:", f"{1 / 0.05:.9f}")
    growth_factor = 1 / (0.05 - 0.02)
    print("growing perpetuity factor at 5%, growth 2%:", f"{growth_factor:.9f}")
    tail = sum(((1 + 0.02) ** (k - 1)) / (1.05**k) for k in range(1, 401))
    print("direct sum, 400 terms, growth 2%:", f"{tail:.9f}")
    print("exact tail after 400 terms, q^N / (r - g):", f"{((1 + 0.02) / 1.05) ** 400 / 0.03:.3e}")
    # The perpetuity's partial sum after N payments has error v^N / r exactly; find the least N with error below 1e-6.
    v = 1 / 1.05
    n_tolerance = 1
    while v**n_tolerance / 0.05 >= 1e-6:
        n_tolerance += 1
    print("least N with perpetuity error below 1e-6 (payments):", n_tolerance)
    print("perpetuity error at N - 1 payments:", f"{v ** (n_tolerance - 1) / 0.05:.4e}")


main()
