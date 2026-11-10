"""Starter implementation for SR1 Run Dynamics Model.

Students complete solve_model and calibrate_buffer according to the project specification.
"""

from __future__ import annotations


def solve_model(uninsured_share: float, liquidation_value: float, liquid_buffer: float) -> dict[str, float]:
    """Calculate the run threshold theta* and run fraction for given bank balance sheet parameters."""
    raise NotImplementedError("solve_model is not implemented")


def calibrate_buffer(target_threshold: float, uninsured_share: float, liquidation_value: float) -> float:
    """Calibrate the required liquid buffer ell to achieve target_threshold."""
    raise NotImplementedError("calibrate_buffer is not implemented")
