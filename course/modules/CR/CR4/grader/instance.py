"""Deterministic instance generator for CR4 Recovery Waterfall and Fulcrum Engine.

Exposes make_instance(seed: int) -> dict[str, Any].
Produces reproducible, varied capital structures and enterprise value scenarios across seeds.
"""

from __future__ import annotations

import functools
import random
from typing import Any


@functools.lru_cache(maxsize=128)
def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic test instance for a given seed."""
    rng = random.Random(seed)

    company_names = [
        "Apex Energy Corp",
        "Beacon Logistics Group",
        "Crestview Manufacturing",
        "Delta Retail Holdings",
        "Echo Telecom Services",
        "Falcon Healthcare Inc",
        "Glacier Chemical Corp",
        "Horizon Industrial Systems",
    ]
    name = company_names[seed % len(company_names)]

    # Generate claim amounts
    dip_claim = round(rng.uniform(15.0, 35.0), 2)
    fl_claim = round(rng.uniform(70.0, 120.0), 2)
    sl_claim = round(rng.uniform(40.0, 80.0), 2)
    unsec_claim = round(rng.uniform(50.0, 100.0), 2)
    sub_claim = round(rng.uniform(25.0, 60.0), 2)

    tranches = [
        {"name": "DIP Facility", "claim": dip_claim, "seniority": 1},
        {"name": "First Lien Term Loan", "claim": fl_claim, "seniority": 2},
        {"name": "Second Lien Notes", "claim": sl_claim, "seniority": 3},
        {"name": "Senior Unsecured Notes", "claim": unsec_claim, "seniority": 4},
        {"name": "Subordinated Debentures", "claim": sub_claim, "seniority": 5},
        {"name": "Common Equity", "claim": 0.0, "seniority": 6},
    ]

    total_debt = dip_claim + fl_claim + sl_claim + unsec_claim + sub_claim

    # Generate scenarios spanning below DIP up to well above total debt
    ev_liq = round(rng.uniform(dip_claim + 0.3 * fl_claim, dip_claim + 0.9 * fl_claim), 2)
    ev_low_min = dip_claim + fl_claim + 0.2 * sl_claim
    ev_low_max = dip_claim + fl_claim + sl_claim + 0.4 * unsec_claim
    ev_low = round(rng.uniform(ev_low_min, ev_low_max), 2)
    ev_base = round(rng.uniform(dip_claim + fl_claim + sl_claim + 0.6 * unsec_claim, total_debt * 1.05), 2)
    ev_high = round(rng.uniform(total_debt * 1.15, total_debt * 1.45), 2)

    # Probabilities
    raw_probs = [rng.uniform(0.15, 0.25), rng.uniform(0.25, 0.35), rng.uniform(0.30, 0.40), rng.uniform(0.10, 0.20)]
    prob_sum = sum(raw_probs)
    probs = [round(p / prob_sum, 4) for p in raw_probs]
    probs[-1] = round(1.0 - sum(probs[:-1]), 4)

    scenarios = [
        {"name": "Liquidation", "ev": ev_liq, "prob": probs[0]},
        {"name": "Low Reorganization", "ev": ev_low, "prob": probs[1]},
        {"name": "Base Reorganization", "ev": ev_base, "prob": probs[2]},
        {"name": "High Reorganization", "ev": ev_high, "prob": probs[3]},
    ]

    # Carveout parameters
    carveout_pct = round(rng.uniform(0.04, 0.08), 3)
    carveout = {
        "source_tranche": "Senior Unsecured Notes",
        "target_tranche": "Common Equity",
        "carveout_pct": carveout_pct,
    }

    # POR parameters for Base Reorganization
    cash_dist = round(rng.uniform(10.0, 20.0), 2)
    max_new_debt = ev_base * 0.45
    new_debt_issued = round(rng.uniform(max_new_debt * 0.7, max_new_debt), 2)

    por = {
        "scenario_name": "Base Reorganization",
        "new_debt_issued": new_debt_issued,
        "cash_dist": cash_dist,
    }

    # Secondary market purchase prices (cents on dollar)
    fl_price = round(rng.uniform(0.85, 0.95), 3)
    sl_price = round(rng.uniform(0.50, 0.70), 3)
    unsec_price = round(rng.uniform(0.25, 0.45), 3)
    sub_price = round(rng.uniform(0.05, 0.18), 3)

    purchase_prices = {
        "First Lien Term Loan": fl_price,
        "Second Lien Notes": sl_price,
        "Senior Unsecured Notes": unsec_price,
        "Subordinated Debentures": sub_price,
    }

    holding_period_years = round(rng.uniform(1.2, 2.0), 2)

    return {
        "seed": seed,
        "company_name": name,
        "tranches": tranches,
        "scenarios": scenarios,
        "carveout": carveout,
        "por": por,
        "purchase_prices": purchase_prices,
        "holding_period_years": holding_period_years,
    }
