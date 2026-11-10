"""Instance generator for FI5 Inflation-Expectations Decomposition autograder.

Generates deterministic market states with nominal Treasury yields, TIPS yields,
survey expected inflation forecasts, TIPS liquidity proxies, base/ref CPI levels,
and market prices.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic simulated inflation-linked market state from an integer seed."""
    rng = random.Random(seed)

    # Nominal 10-year Treasury yield (3.0% to 5.5%)
    nominal_yield = round(rng.uniform(0.030, 0.055), 4)

    # Real 10-year TIPS yield (0.5% to 2.5%, always strictly less than nominal_yield)
    real_yield = round(rng.uniform(0.005, min(0.025, nominal_yield - 0.008)), 4)

    # Survey-expected 10-year inflation (e.g. SPF / Blue Chip forecast, 1.8% to 3.0%)
    survey_inflation = round(rng.uniform(0.018, 0.030), 4)

    # TIPS liquidity proxy (e.g. yield dispersion / bid-ask spread proxy, 5 bps to 50 bps)
    tips_liquidity_proxy = round(rng.uniform(0.0005, 0.0050), 4)
    beta_liquidity = round(rng.uniform(0.8, 1.2), 2)

    # TIPS bond parameters
    maturity_years = rng.choice([5, 10, 20, 30])
    real_coupon_rate = round(rng.uniform(0.010, 0.025), 4)

    # CPI levels
    base_cpi = round(rng.uniform(240.0, 280.0), 2)
    # Inflation shock: can be positive (inflation) or occasionally negative (deflation shock)
    cpi_growth = rng.uniform(-0.08, 0.25)
    ref_cpi = round(base_cpi * (1.0 + cpi_growth), 2)

    # Market prices & swaps
    face_value = 100.0
    mod_duration = round(maturity_years * rng.uniform(0.75, 0.90), 2)
    swap_rate = round(rng.uniform(0.018, 0.032), 4)
    # Cash price of nominal Treasury
    cash_nominal_price = round(rng.uniform(96.0, 104.0), 2)

    return {
        "seed": seed,
        "nominal_yield": nominal_yield,
        "real_yield": real_yield,
        "survey_inflation": survey_inflation,
        "tips_liquidity_proxy": tips_liquidity_proxy,
        "beta_liquidity": beta_liquidity,
        "maturity_years": maturity_years,
        "real_coupon_rate": real_coupon_rate,
        "base_cpi": base_cpi,
        "ref_cpi": ref_cpi,
        "face_value": face_value,
        "mod_duration": mod_duration,
        "swap_rate": swap_rate,
        "cash_nominal_price": cash_nominal_price,
    }
