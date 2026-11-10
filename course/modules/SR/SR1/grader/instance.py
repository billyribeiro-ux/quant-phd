"""Instance generator for SR1 Run Dynamics Model (SIMULATED).

Generates deterministic, per-seed instances of bank balance sheet parameters
and prudential target thresholds. All generated instances are valid, strictly
interior, and SIMULATED.
"""

from __future__ import annotations

import random


def make_instance(seed: int) -> dict[str, float]:
    """Generate a deterministic, valid parameter instance for the Run Dynamics Model."""
    rng = random.Random(seed)
    uninsured_share = round(rng.uniform(0.50, 0.85), 4)
    liquidation_value = round(rng.uniform(0.60, 0.95), 4)

    # Attainable threshold range is (0, min(1.0, uninsured_share / liquidation_value))
    max_thresh = min(0.90, (uninsured_share / liquidation_value) * 0.95)
    min_thresh = 0.15
    target_thresh = round(rng.uniform(min_thresh, max_thresh), 4)

    # Choose a liquid buffer that yields a threshold inside (0, 1)
    thresh_draw = rng.uniform(0.20, 0.80) * min(1.0, uninsured_share / liquidation_value)
    denom = 1.0 - liquidation_value * thresh_draw
    buffer_val = round((uninsured_share - liquidation_value * thresh_draw) / denom, 4)
    buffer_val = max(0.05, min(uninsured_share - 0.05, buffer_val))

    return {
        "uninsured_share": uninsured_share,
        "liquidation_value": liquidation_value,
        "liquid_buffer": buffer_val,
        "target_threshold": target_thresh,
    }
