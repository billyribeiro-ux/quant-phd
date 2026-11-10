"""Starter code for PM3 project: Unsmoothing private credit returns.

Learner implementation template. Complete each function to satisfy the project specification
and pass the autograder test suite across all evaluation seeds.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def estimate_smoothing_parameter(reported_returns: np.ndarray) -> float:
    """Estimate the first-order appraisal smoothing parameter phi via sample autocorrelation."""
    raise NotImplementedError("Implement estimate_smoothing_parameter")


def unsmooth_returns_ar1(reported_returns: np.ndarray, phi: float) -> np.ndarray:
    """Invert the AR(1) smoothing filter to recover the unobserved true return series."""
    raise NotImplementedError("Implement unsmooth_returns_ar1")


def compute_risk_metrics(returns: np.ndarray, rf_quarterly: float) -> dict[str, float]:
    """Calculate annualized mean, volatility, Sharpe ratio, max drawdown, and autocorrelation."""
    raise NotImplementedError("Implement compute_risk_metrics")


def estimate_systematic_risk(asset_returns: np.ndarray, market_returns: np.ndarray) -> dict[str, float]:
    """Compute market beta, alpha, R-squared, and tracking error against a benchmark."""
    raise NotImplementedError("Implement estimate_systematic_risk")


def solve_project(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute the complete private credit de-smoothing and risk evaluation pipeline."""
    raise NotImplementedError("Implement solve_project")
