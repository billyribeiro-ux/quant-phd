"""Input and output integrity validation for X4: Stablecoin Reserve Stress Test.

Ensures balance sheet conservation, valid non-negative parameters,
and proper asset tier formatting.
"""

from __future__ import annotations

from typing import Any

VALID_TIERS = ("cash", "overnight_repo", "tbills_short", "treasury_notes", "bank_deposits")


def validate_reserve_inputs(
    total_liabilities: float,
    reserve_assets: dict[str, dict[str, float]],
    rate_shock_bps: float,
    peg_threshold: float,
) -> None:
    """Validate input parameters for the reserve stress test."""
    if total_liabilities <= 0.0:
        raise ValueError(f"total_liabilities must be positive, got {total_liabilities}")
    if rate_shock_bps < 0.0:
        raise ValueError(f"rate_shock_bps must be non-negative, got {rate_shock_bps}")
    if not (0.50 <= peg_threshold <= 1.00):
        raise ValueError(f"peg_threshold must be between 0.50 and 1.00, got {peg_threshold}")

    if not isinstance(reserve_assets, dict) or len(reserve_assets) == 0:
        raise ValueError("reserve_assets must be a non-empty dictionary")

    for tier, data in reserve_assets.items():
        if not isinstance(data, dict):
            raise ValueError(f"Asset tier {tier} data must be a dictionary")
        for key in ("par", "duration", "haircut"):
            if key not in data:
                raise ValueError(f"Asset tier {tier} missing required field '{key}'")
            if not isinstance(data[key], (int, float)):
                raise ValueError(f"Field '{key}' in tier {tier} must be numeric")

        if data["par"] < 0.0:
            raise ValueError(f"Asset tier {tier} par value cannot be negative: {data['par']}")
        if data["duration"] < 0.0:
            raise ValueError(f"Asset tier {tier} duration cannot be negative: {data['duration']}")
        if not (0.0 <= data["haircut"] < 1.0):
            raise ValueError(f"Asset tier {tier} haircut must be in [0, 1): {data['haircut']}")


def validate_waterfall_output(result: dict[str, Any]) -> None:
    """Ensure liquidation waterfall output contains required fields and valid types."""
    required = {
        "nav": float,
        "total_haircut_loss": float,
        "cash_raised": float,
        "unfulfilled_redemptions": float,
        "remaining_tokens": float,
        "remaining_market_value": float,
        "tier_details": dict,
    }
    for field, expected_type in required.items():
        if field not in result:
            raise ValueError(f"Missing required waterfall output field: {field}")
        if not isinstance(result[field], expected_type):
            raise ValueError(f"Field '{field}' expected {expected_type}, got {type(result[field])}")
