from fractions import Fraction
from typing import Any

# SIMULATED plant, not a real company. Money is whole cents; quantities are whole units.
INPUT_PRICE = 200  # cents per input unit: the standard price and the price actually paid
FIXED = 5_000_000  # fixed overhead in cents, the same in the budget and in the actual period
ACTUAL_INPUTS = 5_300  # input units actually used in the period

PRODUCTS: list[dict[str, Any]] = [
    {
        "name": "Standard",
        "budget_units": 1000,
        "budget_price": 5000,
        "standard": 3,
        "actual_units": 1200,
        "actual_price": 5200,
    },
    {
        "name": "Deluxe",
        "budget_units": 400,
        "budget_price": 9000,
        "standard": 5,
        "actual_units": 300,
        "actual_price": 8800,
    },
]


def nearest_cent(amount: Fraction) -> int:
    """The nearest whole cent, halves up. The amounts in this case are never negative."""
    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)


def main() -> None:
    # Step 1. Master budget. Why: it is the plan the actual period is compared with, at the budgeted volume and mix.
    budget_units = sum(p["budget_units"] for p in PRODUCTS)
    budget_revenue = sum(p["budget_units"] * p["budget_price"] for p in PRODUCTS)
    budget_variable = sum(p["budget_units"] * p["standard"] * INPUT_PRICE for p in PRODUCTS)
    master = budget_revenue - budget_variable - FIXED
    print("step 1 master budget profit (cents):", master)

    # Step 2. Flexed budget. Why: the same budgeted mix at the volume actually sold, so volume is separated from mix.
    actual_total = sum(p["actual_units"] for p in PRODUCTS)
    flex_revenue = nearest_cent(Fraction(actual_total * budget_revenue, budget_units))
    flex_variable = nearest_cent(Fraction(actual_total * budget_variable, budget_units))
    flexed = flex_revenue - flex_variable - FIXED
    print("step 2 flexed budget at", actual_total, "units, profit (cents):", flexed)

    # Step 3. Sales price variance. Why: each unit sold is compared with its budgeted price, favourable when positive.
    price = sum((p["actual_price"] - p["budget_price"]) * p["actual_units"] for p in PRODUCTS)
    print("step 3 sales price variance (cents):", price)

    # Step 4. Sales volume variance. Why: the change in total units, valued at the budgeted mix.
    volume = flexed - master
    print("step 4 sales volume variance (cents):", volume)

    # Step 5. Efficiency variance. Why: the inputs the actual output should have used, against the inputs used.
    standard_inputs = sum(p["standard"] * p["actual_units"] for p in PRODUCTS)
    efficiency = INPUT_PRICE * (standard_inputs - ACTUAL_INPUTS)
    print("step 5 efficiency variance (cents):", efficiency)

    # Step 6. Sales mix variance. Why: the actual mix priced at budgeted margins, less the flexed profit.
    actual_mix_margin = sum(p["actual_units"] * (p["budget_price"] - p["standard"] * INPUT_PRICE) for p in PRODUCTS)
    actual_mix_contribution = actual_mix_margin - FIXED
    mix = actual_mix_contribution - flexed
    print("step 6 sales mix variance (cents):", mix)
    exact_flexed = Fraction(actual_total * budget_revenue, budget_units)
    exact_flexed -= Fraction(actual_total * budget_variable, budget_units) + FIXED
    print("step 6 exact flexed profit minus whole-cent flexed profit (cents):", exact_flexed - flexed)

    # Step 7. Total profit variance. Why: the reported profit of the period less the master budget profit.
    actual_profit = sum(p["actual_units"] * p["actual_price"] for p in PRODUCTS)
    actual_profit -= INPUT_PRICE * ACTUAL_INPUTS + FIXED
    total = actual_profit - master
    print("step 7 total profit variance (cents):", total)

    # Step 8. Reconciliation. Why: the four variances must add to the total with no residual.
    print("step 8 four variances sum to total:", price + volume + mix + efficiency == total)


main()
