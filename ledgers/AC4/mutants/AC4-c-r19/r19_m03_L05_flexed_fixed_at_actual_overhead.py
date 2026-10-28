"""AC4 L05 lab 1: the master budget, then the flexible budget at actual volume. SIMULATED company.

SIMULATED: every input in this lab is an invented value chosen by the author, and every printed number is computed
from those inputs. No company's accounts are read and no published figure is reproduced. The lab checks the arithmetic
of two budgets and one comparison. It says nothing about how any real firm budgets.

All money is integer cents (1 dollar = 100 cents). Quantities are whole units or whole kilograms. Nothing is a float,
so every total below is exact.

Case, for two products A and B and one material:
    budget (master) units        A 600, B 400
    budget selling price         A 2,500 cents, B 3,400 cents per unit
    standard material per unit   A 2 kg, B 3 kg
    standard material price      500 cents per kg (the actual price equals it in this case)
    fixed overhead               500,000 cents per period, whatever the output
    actual units sold            A 650, B 500
    actual selling price         A 2,400 cents, B 3,450 cents per unit
    actual material used         1,350 kg of A's material and 1,600 kg of B's (2,950 kg in total)
    actual fixed overhead        510,000 cents

Cost behaviour used here: material is variable, so its cost is the standard kilograms per unit times the material
price, times the units. Fixed overhead does not change with units. The flexible budget applies the same cost
function to the actual units and leaves fixed overhead unchanged.

Sign convention: a variance is actual minus budget for a profit line, so a positive value is favourable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

MATERIAL_PRICE = 500  # cents per kg, standard and actual
FIXED_BUDGET = 500_000  # cents per period
FIXED_ACTUAL = 510_000  # cents per period


@dataclass(frozen=True)
class Product:
    """One product: budget inputs, then actual results. Money in cents, quantities in units or kilograms."""

    name: str
    price_budget: int  # cents per unit
    std_kg: int  # standard kilograms of material per unit
    units_budget: int
    price_actual: int  # cents per unit
    units_actual: int
    kg_actual: int  # kilograms of material used in the period


PRODUCTS: tuple[Product, ...] = (
    Product("A", 2_500, 2, 600, 2_400, 650, 1_350),
    Product("B", 3_400, 3, 400, 3_450, 500, 1_600),
)


class Totals(NamedTuple):
    """Revenue, material, contribution and operating profit for one set of units, in cents."""

    revenue: int
    material: int
    contribution: int
    fixed: int
    operating: int


def budget_at(products: tuple[Product, ...], units: dict[str, int]) -> Totals:
    """Budget figures at the given units, at budget prices and standard material cost.

    Fixed overhead is FIXED_BUDGET whatever the units, because it does not flex.
    """
    revenue = sum(p.price_budget * units[p.name] for p in products)
    material = sum(p.std_kg * MATERIAL_PRICE * units[p.name] for p in products)
    contribution = revenue - material
    return Totals(revenue, material, contribution, FIXED_ACTUAL, contribution - FIXED_ACTUAL)


def actual_totals(products: tuple[Product, ...]) -> Totals:
    """Actual results: actual prices, actual kilograms at the material price, actual fixed overhead."""
    revenue = sum(p.price_actual * p.units_actual for p in products)
    material = MATERIAL_PRICE * sum(p.kg_actual for p in products)
    contribution = revenue - material
    return Totals(revenue, material, contribution, FIXED_ACTUAL, contribution - FIXED_ACTUAL)


def main() -> None:
    master_units = {p.name: p.units_budget for p in PRODUCTS}
    actual_units = {p.name: p.units_actual for p in PRODUCTS}

    master = budget_at(PRODUCTS, master_units)
    flexed = budget_at(PRODUCTS, actual_units)
    actual = actual_totals(PRODUCTS)

    # Identity: the static variance splits into a volume-and-mix part and a flexible variance, with no residual.
    # Flexing at the budgeted units returning the master budget holds by construction (one function, one argument)
    # and is not checked here.
    static = actual.operating - master.operating
    volume_and_mix = flexed.operating - master.operating
    flexible = actual.operating - flexed.operating
    assert static == volume_and_mix + flexible

    print(f"master_units {sum(master_units.values())}")
    for p in PRODUCTS:
        rev, mat = p.price_budget * p.units_budget, p.std_kg * MATERIAL_PRICE * p.units_budget
        print(f"master_{p.name}_revenue {rev} material {mat}")
    print(f"master_contribution {master.contribution}")
    print(f"master_operating_profit {master.operating}")
    print(f"actual_units {sum(actual_units.values())}")
    for p in PRODUCTS:
        rev, mat = p.price_budget * p.units_actual, p.std_kg * MATERIAL_PRICE * p.units_actual
        print(f"flexed_{p.name}_revenue {rev} material {mat}")
    print(f"flexed_revenue {flexed.revenue} material {flexed.material} fixed {flexed.fixed}")
    print(f"flexed_contribution {flexed.contribution}")
    print(f"flexed_operating_profit {flexed.operating}")
    print(f"actual_revenue {actual.revenue} material {actual.material}")
    print(f"actual_contribution {actual.contribution}")
    print(f"actual_operating_profit {actual.operating} fixed {actual.fixed}")
    print(f"static_variance {static}")
    print(f"volume_and_mix_variance {volume_and_mix}")
    print(f"flexible_variance {flexible}")


main()
