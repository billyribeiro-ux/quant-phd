"""CF8 lab L01: the cash conversion cycle of a SIMULATED filer, decomposed into its three day counts.

SIMULATED: the filer below is invented for this lab. Its field names are generic. The lab reads no filing, no data file
and no network resource, and it does not parse any filing format. Amounts are integer cents. Day counts are computed
exactly with fractions.Fraction on a 365-day year, and each printed day count is rounded half up to two decimals
for display only. Part C prints the exact cent amount to four decimals and the released cash rounded half up to
whole cents. Part E generates extra filers from a seeded random number generator. Standard library only.
"""

from __future__ import annotations

import math
import random
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction

DAYS_PER_YEAR = 365
SEED = 20261028

FILER_NAME = "SIMULATED filer S-1"
YEARS = [
    {
        "year": 2024,
        "revenue_cents": 8_400_000_000,
        "cost_of_sales_cents": 5_040_000_000,
        "purchases_cents": 5_100_000_000,
        "receivables_cents": 1_050_000_000,
        "inventory_cents": 756_000_000,
        "payables_cents": 612_000_000,
    },
    {
        "year": 2025,
        "revenue_cents": 9_000_000_000,
        "cost_of_sales_cents": 5_490_000_000,
        "purchases_cents": 5_600_000_000,
        "receivables_cents": 1_200_000_000,
        "inventory_cents": 810_000_000,
        "payables_cents": 700_000_000,
    },
    {
        "year": 2026,
        "revenue_cents": 9_600_000_000,
        "cost_of_sales_cents": 5_952_000_000,
        "purchases_cents": 6_000_000_000,
        "receivables_cents": 1_344_000_000,
        "inventory_cents": 893_000_000,
        "payables_cents": 780_000_000,
    },
]


def to_cents(amount: Fraction) -> int:
    """Return a non-negative exact amount in cents as a whole number of cents, with halves taken upward."""
    return math.floor(amount + Fraction(1, 2))


def days_text(value: Fraction) -> str:
    """A day count rounded half up to two decimals, for display only; the exact value is kept elsewhere."""
    quotient = Decimal(value.numerator) / Decimal(value.denominator)
    return str(quotient.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def dso(receivables_cents: int, revenue_cents: int) -> Fraction:
    """Days sales outstanding: year-end receivables times 365 over revenue for the year."""
    return Fraction(receivables_cents * DAYS_PER_YEAR, revenue_cents)


def dio(inventory_cents: int, cost_of_sales_cents: int) -> Fraction:
    """Days inventory outstanding: year-end inventory times 365 over cost of sales for the year."""
    return Fraction(inventory_cents * DAYS_PER_YEAR, cost_of_sales_cents)


def dpo(payables_cents: int, purchases_cents: int) -> Fraction:
    """Days payables outstanding: year-end payables times 365 over purchases for the year."""
    return Fraction(payables_cents * DAYS_PER_YEAR, purchases_cents)


def cycle(
    receivables_cents: int,
    revenue_cents: int,
    inventory_cents: int,
    cost_of_sales_cents: int,
    payables_cents: int,
    purchases_cents: int,
) -> Fraction:
    """Cash conversion cycle in days: DSO plus DIO minus DPO, computed from the three exact day counts."""
    return (
        dso(receivables_cents, revenue_cents)
        + dio(inventory_cents, cost_of_sales_cents)
        - dpo(payables_cents, purchases_cents)
    )


def generated_filer(rng: random.Random) -> dict[str, int]:
    """One SIMULATED filer with plausible but invented balances; every amount is an integer number of cents."""
    revenue = rng.randint(2_000_000_000, 20_000_000_000)
    cost = revenue * rng.randint(45, 75) // 100
    purchases = cost * rng.randint(90, 115) // 100
    return {
        "revenue_cents": revenue,
        "cost_of_sales_cents": cost,
        "purchases_cents": purchases,
        "receivables_cents": revenue * rng.randint(5, 20) // 100,
        "inventory_cents": cost * rng.randint(5, 25) // 100,
        "payables_cents": purchases * rng.randint(5, 20) // 100,
    }


def main() -> None:
    print(f"A. {FILER_NAME}: year-end day counts and the cash conversion cycle, in days")
    for row in YEARS:
        d_s = dso(row["receivables_cents"], row["revenue_cents"])
        d_i = dio(row["inventory_cents"], row["cost_of_sales_cents"])
        d_p = dpo(row["payables_cents"], row["purchases_cents"])
        ccc = cycle(
            row["receivables_cents"],
            row["revenue_cents"],
            row["inventory_cents"],
            row["cost_of_sales_cents"],
            row["payables_cents"],
            row["purchases_cents"],
        )
        print(f"{row['year']}: DSO {days_text(d_s)}, DIO {days_text(d_i)}, DPO {days_text(d_p)}, CCC {days_text(ccc)}")
    identity_holds = all(
        cycle(
            row["receivables_cents"],
            row["revenue_cents"],
            row["inventory_cents"],
            row["cost_of_sales_cents"],
            row["payables_cents"],
            row["purchases_cents"],
        )
        == dso(row["receivables_cents"], row["revenue_cents"])
        + dio(row["inventory_cents"], row["cost_of_sales_cents"])
        - dpo(row["payables_cents"], row["purchases_cents"])
        for row in YEARS
    )
    print("CCC equals DSO plus DIO minus DPO exactly in every year:", identity_holds)

    print()
    print("B. One-for-one: receivables of 2025 rise by 1,000,000 dollars with revenue held fixed")
    base = YEARS[1]
    raised = base["receivables_cents"] + 100_000_000
    dso_before = dso(base["receivables_cents"], base["revenue_cents"])
    dso_after = dso(raised, base["revenue_cents"])
    ccc_before = cycle(
        base["receivables_cents"],
        base["revenue_cents"],
        base["inventory_cents"],
        base["cost_of_sales_cents"],
        base["payables_cents"],
        base["purchases_cents"],
    )
    ccc_after = cycle(
        raised,
        base["revenue_cents"],
        base["inventory_cents"],
        base["cost_of_sales_cents"],
        base["payables_cents"],
        base["purchases_cents"],
    )
    print(f"change in DSO, in days: {days_text(dso_after - dso_before)}")
    print(f"change in CCC, in days: {days_text(ccc_after - ccc_before)}")
    print("the change in CCC equals the change in DSO exactly:", ccc_after - ccc_before == dso_after - dso_before)

    print()
    print("C. Cash released by shortening DSO of 2025 by five days with revenue held fixed, in integer cents")
    released_exact = Fraction(base["revenue_cents"] * 5, DAYS_PER_YEAR)
    released_cents = to_cents(released_exact)
    shortened = Fraction(base["receivables_cents"]) - released_exact
    print(f"exact release, in cents: {released_exact.numerator / released_exact.denominator:.4f}")
    print(f"released cash, in cents, rounded half up: {released_cents}")
    print(f"receivables after the change, in cents, exact: {shortened.numerator / shortened.denominator:.4f}")
    implied = dso(to_cents(shortened), base["revenue_cents"])
    print(f"DSO implied by the rounded receivables, in days: {days_text(implied)}")

    print()
    print("D. Year-end and average receivables give different DSO for 2025 (a basis choice, not an error)")
    average_receivables = Fraction(YEARS[0]["receivables_cents"] + YEARS[1]["receivables_cents"], 2)
    dso_average = average_receivables * DAYS_PER_YEAR / base["revenue_cents"]
    print(f"DSO on year-end receivables, in days: {days_text(dso(base['receivables_cents'], base['revenue_cents']))}")
    print(f"DSO on average receivables of 2024 and 2025, in days: {days_text(dso_average)}")

    print()
    print("E. Two hundred seeded SIMULATED filers: the identity holds for every one")
    rng = random.Random(SEED)
    holds = 0
    for _ in range(200):
        filer = generated_filer(rng)
        total = cycle(
            filer["receivables_cents"],
            filer["revenue_cents"],
            filer["inventory_cents"],
            filer["cost_of_sales_cents"],
            filer["payables_cents"],
            filer["purchases_cents"],
        )
        parts = (
            dso(filer["receivables_cents"], filer["revenue_cents"])
            + dio(filer["inventory_cents"], filer["cost_of_sales_cents"])
            - dpo(filer["payables_cents"], filer["purchases_cents"])
        )
        holds += total == parts
    print(f"filers with the identity exact, out of 200: {holds}")


main()
