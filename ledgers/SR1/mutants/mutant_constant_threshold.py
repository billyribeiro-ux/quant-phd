"""Return a hard-coded constant run threshold regardless of inputs."""

from __future__ import annotations


def solve_model(uninsured_share: float, liquidation_value: float, liquid_buffer: float) -> dict[str, float]:
    """Wrong solver: hard-codes 0.50."""
    return {"run_threshold": 0.50, "run_fraction": 1.0}


def calibrate_buffer(target_threshold: float, uninsured_share: float, liquidation_value: float) -> float:
    """Wrong calibration: returns constant 0.20."""
    return 0.20
