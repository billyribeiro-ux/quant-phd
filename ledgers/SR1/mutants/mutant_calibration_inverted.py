"""Calibrate buffer searching in wrong direction (1 - target)."""

from __future__ import annotations


def solve_model(uninsured_share: float, liquidation_value: float, liquid_buffer: float) -> dict[str, float]:
    """Correct solver."""
    if not (0.0 <= uninsured_share <= 1.0):
        raise ValueError("uninsured share must lie in [0, 1]")
    if not (0.0 < liquidation_value <= 1.0):
        raise ValueError("liquidation value must lie in (0, 1]")
    if not (0.0 < liquid_buffer < 1.0):
        raise ValueError("liquid buffer must lie in (0, 1)")

    if uninsured_share == 0.0 or uninsured_share <= liquid_buffer:
        return {"run_threshold": 0.0, "run_fraction": 0.0}

    raw = (uninsured_share - liquid_buffer) / (liquidation_value * (1.0 - liquid_buffer))
    run_threshold = min(1.0, max(0.0, raw))
    return {"run_threshold": run_threshold, "run_fraction": 1.0 if run_threshold > 0 else 0.0}


def calibrate_buffer(target_threshold: float, uninsured_share: float, liquidation_value: float) -> float:
    """Wrong calibration: targets 1 - target_threshold."""
    if not (0.0 <= uninsured_share <= 1.0):
        raise ValueError("uninsured share must lie in [0, 1]")
    if not (0.0 < liquidation_value <= 1.0):
        raise ValueError("liquidation value must lie in (0, 1]")
    if uninsured_share == 0.0:
        raise ValueError("target threshold is not attainable")

    # Error: inverted target
    wrong_target = 1.0 - target_threshold
    denom = 1.0 - liquidation_value * wrong_target
    return (uninsured_share - liquidation_value * wrong_target) / denom
