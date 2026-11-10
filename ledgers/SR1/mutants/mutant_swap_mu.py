"""Swap insured and uninsured shares in the solvency calculation."""

from __future__ import annotations


def solve_model(uninsured_share: float, liquidation_value: float, liquid_buffer: float) -> dict[str, float]:
    """Wrong solution: swaps mu and 1-mu."""
    if not (0.0 <= uninsured_share <= 1.0):
        raise ValueError("uninsured share must lie in [0, 1]")
    if not (0.0 < liquidation_value <= 1.0):
        raise ValueError("liquidation value must lie in (0, 1]")
    if not (0.0 < liquid_buffer < 1.0):
        raise ValueError("liquid buffer must lie in (0, 1)")

    # Error: uses (1 - mu) instead of mu
    wrong_mu = 1.0 - uninsured_share
    if wrong_mu <= liquid_buffer:
        return {"run_threshold": 0.0, "run_fraction": 0.0}

    raw = (wrong_mu - liquid_buffer) / (liquidation_value * (1.0 - liquid_buffer))
    run_threshold = min(1.0, max(0.0, raw))
    return {"run_threshold": run_threshold, "run_fraction": 1.0 if run_threshold > 0 else 0.0}


def calibrate_buffer(target_threshold: float, uninsured_share: float, liquidation_value: float) -> float:
    """Calibrate buffer using formula."""
    denom = 1.0 - liquidation_value * target_threshold
    return (uninsured_share - liquidation_value * target_threshold) / denom
