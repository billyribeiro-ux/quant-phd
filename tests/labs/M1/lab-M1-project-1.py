"""Rung 1 worked example: the level payment and the full schedule of one fixed-rate loan, in integer cents."""

import math


def nearest_cent(amount: float) -> int:
    """The nearest whole cent of a non-negative amount, with a tie going up."""
    return math.floor(amount + 0.5)


def main() -> None:
    principal_cents = 25_000_000  # $250,000.00, an illustrative loan, not market data
    annual_rate = 0.06  # nominal annual rate, compounded monthly
    months = 360
    # Step 1. The monthly rate is the nominal annual rate divided by 12, not a conversion to an effective rate.
    i = annual_rate / 12
    # Step 2. The annuity factor a = (1 - (1 + i)^-n) / i is the present value of one dollar per month.
    factor = (1 - (1 + i) ** -months) / i
    # Step 3. The level payment is the loan divided by the factor, to the nearest cent.
    payment = nearest_cent(principal_cents / factor)
    print("monthly rate:", f"{i:.6f}", "| annuity factor:", f"{factor:.6f}")
    print("level payment (cents):", payment)
    # Step 4. Each month: interest on the opening balance, principal is what remains of the payment.
    balance = principal_cents
    total_interest = 0
    for month in range(1, months + 1):
        interest = nearest_cent(balance * i)
        paid = payment if month < months else balance + interest  # the last payment clears the balance exactly
        principal = paid - interest
        balance = balance - principal
        total_interest += interest
        if month <= 2 or month == months:
            print(f"month {month}: payment {paid}, interest {interest}, principal {principal}, balance {balance}")
    print("final balance (cents):", balance)
    print("total interest (cents):", total_interest)


main()
