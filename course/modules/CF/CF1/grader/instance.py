"""Per-learner instances for the CF1 capital-budgeting autograder.

make_instance(seed) is deterministic: the same seed always gives the same project, and different seeds give
different projects. Every instance is a valid project (positive life, rates above -1, non-negative revenues and
costs). Every number is SIMULATED: the project is generated here and is not any company's. Standard library only.

The project's cash flows have one sign change (an outlay, then inflows), so its NPV falls as the rate rises and its
IRR is unique. Units: money in whole cents on input; rates are decimals per period.
"""

from __future__ import annotations

import json
import random
from typing import Any

MC_DRAWS = 20_000


def make_instance(seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    life = rng.randint(4, 8)
    year_one_revenue = rng.randrange(400_000, 800_001, 1_000)  # cents: $4,000 to $8,000 in year one
    growth = rng.uniform(-0.02, 0.05)
    cost_ratio = rng.uniform(0.40, 0.65)
    revenue: list[float] = []
    cash_costs: list[float] = []
    for t in range(life):
        year_revenue = round(year_one_revenue * (1.0 + growth) ** t, 2)
        revenue.append(year_revenue)
        cash_costs.append(round(year_revenue * cost_ratio, 2))
    capex = rng.randrange(1_000_000, 3_000_001, 1_000)  # cents: $10,000 to $30,000
    project: dict[str, Any] = {
        "capex": capex,
        "life": life,
        "revenue": revenue,
        "cash_costs": cash_costs,
        "tax_rate": rng.choice([0.20, 0.25, 0.30, 0.35]),
        "nwc_share": rng.choice([0.05, 0.10, 0.15]),
        "inflation": rng.choice([0.02, 0.03, 0.04]),  # positive, so real and nominal flows always differ
    }
    return {
        "seed": seed,
        "label": f"SIMULATED project {seed}",
        "payload": json.dumps(project, sort_keys=True),
        "nominal_rate": rng.choice([0.06, 0.08, 0.10, 0.12]),
        "volatility": rng.choice([0.10, 0.20, 0.30]),
        "mc_draws": MC_DRAWS,
    }
