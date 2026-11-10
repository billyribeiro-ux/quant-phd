"""Starter template for Atlas A11 portfolio construction module (atlas.portfolio).

Students implement the functions below to satisfy the contract.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray


def shrinkage_covariance(
    returns: NDArray[np.float64] | list[list[float]],
    target: str = "scaled_identity",
) -> NDArray[np.float64]:
    """Compute the Ledoit-Wolf linear shrinkage covariance matrix."""
    raise NotImplementedError("shrinkage_covariance is not implemented yet")


def marginal_risk_contributions(
    weights: NDArray[np.float64] | list[float],
    cov: NDArray[np.float64] | list[list[float]],
) -> NDArray[np.float64]:
    """Compute marginal risk contributions (MRC) d(sigma_p)/dw_i."""
    raise NotImplementedError("marginal_risk_contributions is not implemented yet")


def component_risk_contributions(
    weights: NDArray[np.float64] | list[float],
    cov: NDArray[np.float64] | list[list[float]],
) -> NDArray[np.float64]:
    """Compute total/component risk contributions (TRC) w_i * MRC_i."""
    raise NotImplementedError("component_risk_contributions is not implemented yet")


def percent_risk_contributions(
    weights: NDArray[np.float64] | list[float],
    cov: NDArray[np.float64] | list[list[float]],
) -> NDArray[np.float64]:
    """Compute percent risk contributions (PRC) TRC_i / sigma_p."""
    raise NotImplementedError("percent_risk_contributions is not implemented yet")


def risk_parity_weights(
    cov: NDArray[np.float64] | list[list[float]],
    budgets: NDArray[np.float64] | list[float] | None = None,
    tol: float = 1e-8,
    max_iter: int = 500,
) -> NDArray[np.float64]:
    """Solve for the risk budgeting / equal risk contribution portfolio."""
    raise NotImplementedError("risk_parity_weights is not implemented yet")


def mean_variance_weights(
    mean: NDArray[np.float64] | list[float],
    cov: NDArray[np.float64] | list[list[float]],
    risk_aversion: float = 1.0,
    long_only: bool = False,
) -> NDArray[np.float64]:
    """Compute mean-variance portfolio weights subject to sum(w) = 1."""
    raise NotImplementedError("mean_variance_weights is not implemented yet")


def volatility_target_weights(
    weights: NDArray[np.float64] | list[float],
    cov: NDArray[np.float64] | list[list[float]],
    target_vol: float,
    max_leverage: float | None = None,
) -> NDArray[np.float64]:
    """Scale portfolio weights to achieve a target annualized volatility."""
    raise NotImplementedError("volatility_target_weights is not implemented yet")


def run_benchmark(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute complete portfolio construction pipeline for the project benchmark."""
    raise NotImplementedError("run_benchmark is not implemented yet")
