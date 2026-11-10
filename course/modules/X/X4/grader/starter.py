"""Starter scaffold for X4: Stablecoin Reserve Stress Test.

Complete the functions below to implement reserve portfolio stress testing,
interest rate duration shocks, liquidation waterfall accounting, and peg-break search.
"""

from __future__ import annotations

from typing import Any


def validate_inputs(
    total_liabilities: float,
    reserve_assets: dict[str, dict[str, float]],
    rate_shock_bps: float,
    peg_threshold: float,
) -> None:
    """Validate all project inputs."""
    raise NotImplementedError("Student implementation required.")


def apply_rate_shock(
    reserve_assets: dict[str, dict[str, float]],
    rate_shock_bps: float,
) -> dict[str, dict[str, float]]:
    """Apply interest rate shock to reserve assets using modified duration."""
    raise NotImplementedError("Student implementation required.")


def simulate_redemption_waterfall(
    total_liabilities: float,
    shocked_assets: dict[str, dict[str, float]],
    redemptions: float,
) -> dict[str, Any]:
    """Execute redemption liquidation waterfall across reserve asset tiers."""
    raise NotImplementedError("Student implementation required.")


def find_peg_break_run_size(
    total_liabilities: float,
    shocked_assets: dict[str, dict[str, float]],
    peg_threshold: float,
    tol: float = 1e-5,
) -> dict[str, Any]:
    """Find the minimal cumulative redemption run size R* that causes NAV < peg_threshold."""
    raise NotImplementedError("Student implementation required.")


def compute_liquidity_coverage_ratio(
    reserve_assets: dict[str, dict[str, float]],
    stressed_outflow_30d: float,
) -> float:
    """Compute Liquidity Coverage Ratio (LCR) = HQLA / stressed_outflow_30d."""
    raise NotImplementedError("Student implementation required.")


def run_stress_grid(
    total_liabilities: float,
    base_assets: dict[str, dict[str, float]],
    rate_shocks_bps: list[float],
    redemption_fractions: list[float],
    peg_threshold: float = 0.995,
) -> dict[str, Any]:
    """Evaluate reserve portfolio across a 2D grid of rate shocks and redemption sizes."""
    raise NotImplementedError("Student implementation required.")
