"""Reference solution for SR1 Run Dynamics Model.

Implements the frozen interface:
- solve_model(uninsured_share, liquidation_value, liquid_buffer) -> dict[str, float]
- calibrate_buffer(target_threshold, uninsured_share, liquidation_value) -> float
"""

from __future__ import annotations


def solve_model(uninsured_share: float, liquidation_value: float, liquid_buffer: float) -> dict[str, float]:
    """Calculate the run threshold theta* and run fraction for given bank balance sheet parameters."""
    if not (0.0 <= uninsured_share <= 1.0):
        raise ValueError("uninsured share must lie in [0, 1]")
    if not (0.0 < liquidation_value <= 1.0):
        raise ValueError("liquidation value must lie in (0, 1]")
    if not (0.0 < liquid_buffer < 1.0):
        raise ValueError("liquid buffer must lie in (0, 1)")

    if uninsured_share == 0.0 or uninsured_share <= liquid_buffer:
        return {"run_threshold": 0.0, "run_fraction": 0.0}

    raw_threshold = (uninsured_share - liquid_buffer) / (liquidation_value * (1.0 - liquid_buffer))
    run_threshold = min(1.0, max(0.0, raw_threshold))
    run_fraction = 1.0 if run_threshold > 0.0 else 0.0
    return {"run_threshold": run_threshold, "run_fraction": run_fraction}


def calibrate_buffer(target_threshold: float, uninsured_share: float, liquidation_value: float) -> float:
    """Calibrate the required liquid buffer ell to achieve target_threshold."""
    if not (0.0 <= uninsured_share <= 1.0):
        raise ValueError("uninsured share must lie in [0, 1]")
    if not (0.0 < liquidation_value <= 1.0):
        raise ValueError("liquidation value must lie in (0, 1]")
    if uninsured_share == 0.0:
        raise ValueError("target threshold is not attainable")

    max_attainable = min(1.0, uninsured_share / liquidation_value)
    if not (0.0 < target_threshold < max_attainable):
        raise ValueError("target threshold is not attainable")

    denom = 1.0 - liquidation_value * target_threshold
    buffer_val = (uninsured_share - liquidation_value * target_threshold) / denom
    return buffer_val
