"""Deterministic instance generator for DV4 autograder suite."""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, parameter-varied instance for DV4 pricing tests."""
    rng = random.Random(seed)

    spot = round(rng.uniform(75.0, 125.0), 2)
    strike = round(rng.uniform(80.0, 120.0), 2)
    rate = round(rng.uniform(0.015, 0.065), 4)
    vol = round(rng.uniform(0.14, 0.36), 4)
    maturity = round(rng.uniform(0.30, 1.25), 2)
    dividend_yield = round(rng.uniform(0.0, 0.025), 4)
    is_call = rng.choice([True, False])

    # Distinct test cases for American put early exercise premium
    american_spot = round(rng.uniform(80.0, 95.0), 2)  # In-the-money put
    american_strike = 100.0
    american_rate = round(rng.uniform(0.04, 0.08), 4)
    american_vol = round(rng.uniform(0.18, 0.30), 4)
    american_maturity = round(rng.uniform(0.50, 1.50), 2)

    return {
        "seed": seed,
        "spot": spot,
        "strike": strike,
        "rate": rate,
        "vol": vol,
        "maturity": maturity,
        "dividend_yield": dividend_yield,
        "is_call": is_call,
        "tolerance": 0.06,
        "american_spot": american_spot,
        "american_strike": american_strike,
        "american_rate": american_rate,
        "american_vol": american_vol,
        "american_maturity": american_maturity,
    }
