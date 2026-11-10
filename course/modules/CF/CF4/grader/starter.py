"""Starter template for Atlas A16 Valuation Engine (atlas.valuation).

Students implement the required valuation functions according to atlas/A16.contract.md.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np


def calculate_fcff(
    ebit: float | np.ndarray,
    tax_rate: float,
    depreciation: float | np.ndarray,
    capex: float | np.ndarray,
    delta_nwc: float | np.ndarray,
) -> float | np.ndarray:
    """Calculate Free Cash Flow to the Firm (FCFF)."""
    raise NotImplementedError("Implement calculate_fcff")


def dcf_enterprise_value(
    fcff_forecast: Sequence[float] | np.ndarray,
    wacc: float,
    terminal_method: str = "gordon",
    terminal_growth: float | None = None,
    exit_multiple: float | None = None,
    terminal_metric: float | None = None,
    mid_year: bool = False,
) -> dict[str, Any]:
    """Discount explicit FCFF forecast and terminal value to determine Enterprise Value."""
    raise NotImplementedError("Implement dcf_enterprise_value")


def enterprise_to_equity_bridge(
    enterprise_value: float,
    total_debt: float,
    cash: float,
    minority_interest: float = 0.0,
    preferred_stock: float = 0.0,
    non_operating_assets: float = 0.0,
    shares_outstanding: float = 1.0,
) -> dict[str, float]:
    """Reconcile enterprise value to common equity value and per-share price."""
    raise NotImplementedError("Implement enterprise_to_equity_bridge")


def residual_income_valuation(
    initial_book_equity: float,
    net_income_forecast: Sequence[float] | np.ndarray,
    dividends_forecast: Sequence[float] | np.ndarray,
    cost_of_equity: float,
    omega: float = 0.0,
) -> dict[str, Any]:
    """Compute equity value via Ohlson residual income model with clean surplus dynamics."""
    raise NotImplementedError("Implement residual_income_valuation")


def multiples_valuation(
    metric_value: float,
    multiple: float,
    multiple_type: str = "ev_ebitda",
    net_debt: float = 0.0,
    shares_outstanding: float = 1.0,
) -> dict[str, float]:
    """Calculate implied enterprise and equity values from peer multiples."""
    raise NotImplementedError("Implement multiples_valuation")


def sensitivity_grid_2d(
    fcff_forecast: Sequence[float] | np.ndarray,
    wacc_range: Sequence[float],
    growth_range: Sequence[float],
    total_debt: float = 0.0,
    cash: float = 0.0,
    shares_outstanding: float = 1.0,
) -> dict[str, Any]:
    """Compute 2D grid of per-share equity values across WACC and terminal growth rates."""
    raise NotImplementedError("Implement sensitivity_grid_2d")


def scenario_valuation(
    scenarios: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Compute probability-weighted expected enterprise and equity values across scenarios."""
    raise NotImplementedError("Implement scenario_valuation")
