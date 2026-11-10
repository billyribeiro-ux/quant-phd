"""Starter template for Module F3 Project: Multi-Asset Factor Book.

Student implementation template. Fill in each function according to the
mathematical specifications in project.html.
"""

from __future__ import annotations

import numpy as np


def compute_carry_factor(signals: np.ndarray, returns: np.ndarray) -> np.ndarray:
    """Build dollar-neutral cross-sectional carry factor returns."""
    raise NotImplementedError


def compute_tsmom_factor(
    returns: np.ndarray,
    lookback: int = 12,
    target_vol: float = 0.10,
) -> np.ndarray:
    """Build time-series momentum factor with trailing inverse-volatility scaling."""
    raise NotImplementedError


def compute_value_factor(signals: np.ndarray, returns: np.ndarray) -> np.ndarray:
    """Build dollar-neutral cross-sectional value factor returns."""
    raise NotImplementedError


def compute_factor_diagnostics(
    factor_returns: np.ndarray,
    annualization: float = 12.0,
) -> dict[str, float]:
    """Compute risk, return, and crash tail diagnostics for a factor return series."""
    raise NotImplementedError


def construct_multi_asset_factor_book(
    instance_data: dict[str, object],
    weighting_scheme: str = "risk_parity",
) -> dict[str, object]:
    """Construct a diversified multi-asset factor book across Rates, FX, and Commodities."""
    raise NotImplementedError
