"""Per-learner instances for the AC4 budget and variance engine (budget_engine.py).

make_instance(seed) is deterministic. It returns a SIMULATED case for a small plant with three products:
the standard quantities of one input, the budgeted and actual volumes and prices, the fixed overhead and the
input quantity actually used. Every case is valid, and the seed changes the answers: the volumes, the mix, the
prices and the efficiency all vary with it. Nothing here is a real company's figure.

The case is returned as a JSON string under ``payload``, so the value is the same bytes on every run. The
grader decodes it; a learner never calls make_instance. All money is in whole cents and all quantities are whole
units, as the project page states.
"""

from __future__ import annotations

import json
import random
from typing import Any

PRODUCT_NAMES = ("Alpha", "Beta", "Gamma")


def make_instance(seed: int) -> dict[str, Any]:
    rng = random.Random(f"AC4-budget-engine/{int(seed)}")
    n_products = 3  # fixed, so the collected test count is the same on every seed
    input_price = rng.randint(150, 400)  # cents per input unit; the standard and the actual price are the same
    fixed_overhead = rng.randint(2_000_000, 8_000_000)  # cents, the same in the budget and in the actual period
    products: list[dict[str, Any]] = []
    for name in PRODUCT_NAMES[:n_products]:
        standard_inputs = rng.randint(2, 6)  # input units per unit of this product, from the standard
        budget_price = standard_inputs * input_price + rng.randint(1500, 5000)  # a positive budgeted margin
        budget_units = rng.randint(200, 1200)
        actual_units = max(1, budget_units * rng.randint(60, 150) // 100)  # each product's volume is drawn separately
        actual_price = budget_price + rng.randint(-400, 300)
        products.append(
            {
                "name": name,
                "budget_units": budget_units,
                "budget_price_cents": budget_price,
                "standard_inputs_per_unit": standard_inputs,
                "actual_units": actual_units,
                "actual_price_cents": actual_price,
            }
        )
    standard_for_actual = sum(p["standard_inputs_per_unit"] * p["actual_units"] for p in products)
    actual_inputs = max(0, standard_for_actual * rng.randint(88, 118) // 100)  # 88% to 118% of standard; can equal it
    case: dict[str, Any] = {
        "label": f"SIMULATED budget case, seed {int(seed)}: {n_products} products, not a real company",
        "input_price_cents": input_price,
        "fixed_overhead_cents": fixed_overhead,
        "actual_inputs_used": actual_inputs,
        "products": products,
    }
    return {"seed": int(seed), "label": case["label"], "payload": json.dumps(case, sort_keys=True)}
