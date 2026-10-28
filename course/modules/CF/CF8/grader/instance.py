"""Per-learner instances for the CF8 treasury-forecast autograder.

SIMULATED: make_instance(seed) generates a stressed 13-week case for a manufacturer. The numbers are generated here
and are not any company's data. Every seed gives a deterministic, valid case: positive minimum cash, a revolver
commitment at least the opening drawn balance, a collection lag between 20 and 90 days and a payment lag between 20
and 60 days. Money is whole cents; days are whole days; the horizon is 13 weeks of 7 days.

Standard library only. The payload is the case as a JSON string, with the keys the specification names.
"""

from __future__ import annotations

import json
import random
from typing import Any

HORIZON_WEEKS = 13


def make_instance(seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    base_sales = rng.randrange(900_000, 1_600_001, 1_000)  # cents of sales in week 1
    drift = rng.uniform(-0.12, 0.15)  # weekly growth of sales; negative means slower sales
    sales = [round(base_sales * (1.0 + drift) ** w) for w in range(HORIZON_WEEKS)]
    cost_ratio = rng.uniform(0.60, 0.95)
    purchases = [round(s * cost_ratio) for s in sales]
    opex_base = rng.randrange(150_000, 450_001, 1_000)
    opex = [round(opex_base * (1.0 + rng.uniform(-0.10, 0.10))) for _ in range(HORIZON_WEEKS)]
    commitment = rng.randrange(2_000_000, 6_000_001, 1_000)
    case: dict[str, Any] = {
        "horizon_weeks": HORIZON_WEEKS,
        "opening_cash_cents": rng.randrange(300_000, 3_000_001, 1_000),
        "minimum_cash_cents": rng.randrange(400_000, 900_001, 1_000),
        "revolver_commitment_cents": commitment,
        "opening_drawn_cents": rng.randrange(0, commitment // 3, 1_000),
        "covenant_threshold_cents": rng.randrange(600_000, 2_500_001, 1_000),
        "collection_lag_days": rng.randint(35, 80),
        "payment_lag_days": rng.randint(25, 50),
        "weekly_sales_cents": sales,
        "weekly_purchases_cents": purchases,
        "weekly_opex_cents": opex,
    }
    return {
        "seed": seed,
        "label": f"SIMULATED case {seed}",
        "payload": json.dumps(case, sort_keys=True),
    }
