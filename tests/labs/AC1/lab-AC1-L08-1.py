"""Lab AC1-L08-1: a book-tax difference schedule and the deferred tax roll-forward.

Every asset, every pretax income figure and the tax rate are SIMULATED: a seeded
generator draws the asset and income, and the rate is a model parameter chosen for
the arithmetic, not a statement about any jurisdiction. No company is represented.
Money is in integer cents of simulated currency units (SCU). The model has one
depreciable asset, straight-line book depreciation over LIFE years, a fixed tax
depreciation schedule that totals the cost, and one flat rate applied to every year.
"""

from __future__ import annotations

import random

SEED = 20260702
LIFE = 5  # book straight-line life in years
TAX_PERCENT = (40, 30, 20, 10, 0)  # tax depreciation as a percent of cost, years 1 to 5; sums to 100
RATE_PERCENT = 21  # the model's flat tax rate in percent (a parameter of the model)


def cents_text(cents: int) -> str:
    """Format integer cents as SCU dollars and cents, for example 1234567 gives 12,345.67."""
    sign = "-" if cents < 0 else ""
    whole, frac = divmod(abs(cents), 100)
    return f"{sign}{whole:,}.{frac:02d}"


def main() -> None:
    """Draw the asset and pretax income, roll the deferred tax balance, and check the identities."""
    rng = random.Random(SEED)
    cost = rng.randrange(1_000_000, 5_000_001, 10_000)  # SCU $10,000 to $50,000, a multiple of $100
    # Pretax income of $40,000 to $90,000 exceeds the largest yearly difference
    # (40% of a $50,000 cost), so taxable income stays positive.
    pretax = [rng.randrange(4_000_000, 9_000_001, 100) for _ in range(LIFE)]
    assert cost % LIFE == 0
    assert sum(TAX_PERCENT) == 100

    print(
        f"SIMULATED asset (seed {SEED}): cost={cents_text(cost)} SCU; book life={LIFE} years; "
        f"tax depreciation percent={TAX_PERCENT}; flat rate={RATE_PERCENT}%"
    )
    print("year  pretax  book_dep  tax_dep  cum_temp_diff  DTL  current_tax  deferred_exp  tax_exp  net_income")

    book_total = 0
    tax_total = 0
    cumulative = 0
    previous_dtl = 0
    exact_rate = 0
    deferred_ok = 0
    tax_ok = 0
    for year in range(1, LIFE + 1):
        index = year - 1
        book_dep = cost // LIFE
        tax_dep = cost * TAX_PERCENT[index] // 100
        assert RATE_PERCENT * tax_dep % 100 == 0 and RATE_PERCENT * book_dep % 100 == 0
        difference = tax_dep - book_dep
        cumulative += difference
        dtl = RATE_PERCENT * cumulative // 100
        taxable = pretax[index] - difference
        current = RATE_PERCENT * taxable // 100
        deferred = dtl - previous_dtl
        tax_expense = current + deferred
        net_income = pretax[index] - tax_expense

        exact_rate += RATE_PERCENT * pretax[index] % 100 == 0
        deferred_ok += deferred == RATE_PERCENT * difference // 100
        tax_ok += tax_expense == RATE_PERCENT * pretax[index] // 100
        book_total += book_dep
        tax_total += tax_dep
        previous_dtl = dtl
        print(
            f"{year:>4}  {cents_text(pretax[index]):>10}  {cents_text(book_dep):>10}  {cents_text(tax_dep):>10}  "
            f"{cents_text(cumulative):>13}  {cents_text(dtl):>10}  {cents_text(current):>11}  "
            f"{cents_text(deferred):>12}  {cents_text(tax_expense):>10}  {cents_text(net_income):>12}"
        )

    print(f"book depreciation total equals cost: {book_total == cost}")
    print(f"tax depreciation total equals cost: {tax_total == cost}")
    print(f"deferred tax balance at the end of year {LIFE}: {cents_text(previous_dtl)} SCU")
    print(f"pretax income times the rate is exact in every year: {exact_rate}/{LIFE}")
    print(f"deferred expense equals rate times the year's difference: {deferred_ok}/{LIFE}")
    print(f"tax expense equals rate times pretax income: {tax_ok}/{LIFE}")
    assert book_total == tax_total == cost
    assert previous_dtl == 0
    assert exact_rate == deferred_ok == tax_ok == LIFE


main()
