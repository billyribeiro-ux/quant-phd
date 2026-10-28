"""AC4 L06 lab 1: the four-way variance decomposition, reconciled exactly. SIMULATED company.

SIMULATED: every input below is invented by the author for this lab. No company's accounts are read and no published
figure is reproduced. The lab shows that four named variances sum to the total contribution variance with zero
residual. It does not show how real firms classify their variances.

All money is integer cents. Fractions are used for the intermediate mix shares, so the reconciliation is exact, and the
lab fails loudly if any reported variance is not a whole number of cents.

Case (the same case as L05, lab 1):
    budget units        A 600, B 400
    budget price        A 2,500 cents, B 3,400 cents per unit
    standard material   A 2 kg, B 3 kg per unit, at 500 cents per kg (the actual price equals it)
    actual units        A 650, B 500
    actual price        A 2,400 cents, B 3,450 cents per unit
    actual material     A 1,350 kg, B 1,600 kg (2,950 kg in total)
    fixed overhead      budget 500,000 cents, actual 510,000 cents (outside the four variances)

Definitions used by the code. Let q_b,i and q_a,i be budget and actual units of product i, Q_b and Q_a the totals,
and m_i = q_b,i / Q_b the budget mix share. Let CM_i = p_b,i - s_i * pi be the budget contribution per unit at standard
cost, where s_i is standard kilograms per unit and pi the material price.

    sales price variance   SP = sum_i (p_a,i - p_b,i) * q_a,i
    sales volume variance  V  = (Q_a - Q_b) * CMbar_b, with CMbar_b = sum_i m_i * CM_i
    sales mix variance     M  = sum_i CM_i * (q_a,i - Q_a * m_i)
    efficiency variance    E  = -pi * sum_i (kg_a,i - s_i * q_a,i)

The four sum to the total contribution variance T = C_a - C_b. The code checks this identity and
raises ValueError if the residual is not zero.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

MATERIAL_PRICE = 500  # cents per kg, standard and actual
FIXED_BUDGET = 500_000
FIXED_ACTUAL = 510_000


@dataclass(frozen=True)
class Product:
    """Budget and actual inputs for one product. Money in cents; quantities in units or kilograms."""

    name: str
    price_budget: int  # cents per unit
    std_kg: int  # standard kilograms of material per unit
    units_budget: int
    price_actual: int  # cents per unit
    units_actual: int
    kg_actual: int  # kilograms of material used


PRODUCTS: tuple[Product, ...] = (
    Product("A", 2_500, 2, 600, 2_400, 650, 1_350),
    Product("B", 3_400, 3, 400, 3_450, 500, 1_600),
)


def whole_cents(value: Fraction, label: str) -> int:
    """Return value as an integer number of cents, or fail loudly if it is a fraction of a cent."""
    if value.denominator != 1:
        raise ValueError(f"{label} is {value}, which is not a whole number of cents")
    return value.numerator


def contribution_per_unit(p: Product) -> int:
    """Budget contribution per unit at standard material cost, in cents: CM_i = p_b,i - s_i * pi."""
    return p.price_budget - p.std_kg * MATERIAL_PRICE


def sales_price_by_product(products: tuple[Product, ...]) -> dict[str, int]:
    """Sales price variance of each product, (p_a,i - p_b,i) * q_a,i, in cents, keyed by product name."""
    return {p.name: (p.price_actual - p.price_budget) * p.units_actual for p in products}


def decompose(products: tuple[Product, ...]) -> dict[str, int]:
    """The four variances and the total contribution variance, in cents. Raises ValueError if they do not reconcile."""
    q_b = sum(p.units_budget for p in products)
    q_a = sum(p.units_actual for p in products)
    cm_bar = Fraction(sum(contribution_per_unit(p) * p.units_budget for p in products), q_b)

    sales_price = sum(sales_price_by_product(products).values())
    volume = Fraction(q_a - q_b) * cm_bar
    mix = sum(Fraction(contribution_per_unit(p) * p.units_actual) for p in products) - q_a * cm_bar
    efficiency = -MATERIAL_PRICE * sum(p.kg_actual - p.std_kg * p.units_actual for p in products)

    budget_contribution = sum(contribution_per_unit(p) * p.units_budget for p in products)
    actual_contribution = sum(p.price_actual * p.units_actual - MATERIAL_PRICE * p.kg_actual for p in products)
    total = actual_contribution - budget_contribution

    out = {
        "sales_price": sales_price,
        "sales_volume": whole_cents(volume, "sales volume variance"),
        "sales_mix": whole_cents(mix, "sales mix variance"),
        "efficiency": efficiency,
    }
    residual = total - sum(out.values())
    if residual != 0:
        raise ValueError(f"the four variances leave a residual of {residual} cents")
    out["total"] = total
    out["budget_contribution"] = budget_contribution
    out["actual_contribution"] = actual_contribution
    return out


def main() -> None:
    result = decompose(PRODUCTS)
    print(f"budget_contribution {result['budget_contribution']}")
    print(f"actual_contribution {result['actual_contribution']}")
    print(f"total_contribution_variance {result['total']}")
    print(f"sales_price_variance {result['sales_price']}")
    for name, value in sales_price_by_product(PRODUCTS).items():
        print(f"sales_price_variance_{name} {value}")
    print(f"sales_volume_variance {result['sales_volume']}")
    print(f"sales_mix_variance {result['sales_mix']}")
    print(f"efficiency_variance {result['efficiency']}")
    print(f"sum_of_four {result['sales_price'] + result['sales_volume'] + result['sales_mix'] + result['efficiency']}")
    print(f"fixed_cost_variance {FIXED_BUDGET - FIXED_ACTUAL}")
    print(f"operating_profit_variance {result['total'] + (FIXED_BUDGET - FIXED_ACTUAL)}")

    # Check 1: actual units in the budget mix (690 A and 460 B, 1,150 in total) at standard material use and budget
    # prices leave the mix and efficiency variances at zero. Only the volume variance remains.
    on_mix = tuple(
        Product(p.name, p.price_budget, p.std_kg, p.units_budget, p.price_budget, units, units * p.std_kg)
        for p, units in zip(PRODUCTS, (690, 460), strict=True)
    )
    check = decompose(on_mix)
    print(f"check_on_mix_sales_mix_variance {check['sales_mix']}")
    print(f"check_on_mix_efficiency_variance {check['efficiency']}")
    print(f"check_on_mix_sales_volume_variance {check['sales_volume']}")
    print(f"check_on_mix_total {check['total']}")


main()
