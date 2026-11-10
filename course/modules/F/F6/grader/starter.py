"""Starter template for F6: Machine Learning in Asset Pricing (ml_study.py).

Implement:
- compute_oos_r2
- construct_spread_portfolio
- evaluate_complexity_curve
- run_ml_study
"""

from __future__ import annotations

from typing import Any

import numpy as np


def compute_oos_r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute out-of-sample R-squared with zero return benchmark."""
    raise NotImplementedError("compute_oos_r2 not implemented")


def construct_spread_portfolio(
    predictions: np.ndarray,
    returns: np.ndarray,
    cost_bps: float = 15.0,
) -> dict[str, float]:
    """Construct top-bottom quantile long-short spread portfolio net of costs."""
    raise NotImplementedError("construct_spread_portfolio not implemented")


def evaluate_complexity_curve(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    gammas: list[float],
    seed: int = 42,
) -> dict[str, list[float]]:
    """Evaluate overparameterized random feature regression across complexity ratios."""
    raise NotImplementedError("evaluate_complexity_curve not implemented")


def run_ml_study(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute complete cross-sectional ML asset pricing study."""
    raise NotImplementedError("run_ml_study not implemented")
