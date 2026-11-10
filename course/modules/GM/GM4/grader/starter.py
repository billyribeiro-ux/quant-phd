"""Starter code for Atlas A20: macro trade-construction engine (atlas.strategy)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class MacroView:
    """Specification of a macroeconomic view."""

    view_id: str
    asset_ids: list[str]
    view_type: str
    expected_move_bps: float
    confidence: float
    horizon_days: int


def compute_dv01_hedge_ratio(dv01_leg1: float, dv01_leg2: float) -> float:
    """Calculate duration-neutral hedge ratio: units of leg 2 per unit of leg 1."""
    raise NotImplementedError


def construct_curve_spread(
    notional_leg1: float,
    dv01_leg1: float,
    dv01_leg2: float,
    direction: str = "steepener",
) -> tuple[float, float]:
    """Calculate signed notional positions (N1, N2) for a duration-neutral curve trade."""
    raise NotImplementedError


def evaluate_carry_and_rolldown(
    spot_yield: float,
    duration: float,
    roll_down_bps: float,
    repo_rate: float,
    horizon_years: float,
) -> dict[str, float]:
    """Compute gross carry, roll-down gain, repo financing drag, and net carry."""
    raise NotImplementedError


def compute_expression_convexity(
    spot: float,
    strikes: np.ndarray,
    vols: np.ndarray,
    expiry: float,
    rate: float,
    weights: np.ndarray,
    is_call: np.ndarray,
) -> dict[str, float]:
    """Compute aggregate Greeks (delta, gamma, vega, theta) for an options/delta-one portfolio."""
    raise NotImplementedError


def compute_asymmetry_ratio(pnl_distribution: np.ndarray) -> float:
    """Compute ratio of expected upside to expected downside from a scenario P&L distribution."""
    raise NotImplementedError


def size_trade_fractional_kelly(
    expected_excess_return: float,
    variance: float,
    fraction: float = 0.25,
    max_leverage: float = 5.0,
) -> float:
    """Calculate fractional Kelly portfolio weight subject to maximum leverage cap."""
    raise NotImplementedError


def scenario_pnl_grid(
    spot_shocks: np.ndarray,
    vol_shocks: np.ndarray,
    base_spot: float,
    base_vols: np.ndarray,
    strikes: np.ndarray,
    expiry: float,
    rate: float,
    weights: np.ndarray,
    is_call: np.ndarray,
    holding_period: float = 0.0,
) -> np.ndarray:
    """Compute 2D grid of scenario P&L across spot shocks (columns) and vol shocks (rows)."""
    raise NotImplementedError


class MacroTradeEngine:
    """End-to-end macro trade construction engine (Milestone A20)."""

    def __init__(self, risk_free_rate: float = 0.045) -> None:
        raise NotImplementedError

    def construct_trade(
        self,
        view: MacroView,
        leg1_params: dict[str, float],
        leg2_params: dict[str, float] | None = None,
        sizing_budget: float = 1_000_000.0,
        kelly_fraction: float = 0.25,
        max_leverage: float = 4.0,
    ) -> dict[str, Any]:
        """Construct full trade package."""
        raise NotImplementedError
