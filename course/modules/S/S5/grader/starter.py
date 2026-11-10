"""Starter skeleton for S5 project: Two-pass Fama-MacBeth and Shanken correction.

Implement each function below according to the project specification.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np


class FMResult(NamedTuple):
    """Container for Fama-MacBeth estimation results."""

    premia: np.ndarray
    naive_se: np.ndarray
    shanken_se: np.ndarray
    gmm_se: np.ndarray


def loadings(excess: np.ndarray, factors: np.ndarray, train: int) -> np.ndarray:
    """Estimate time-series factor loadings for each asset over the training window."""
    raise NotImplementedError("implement loadings")


def monthly_slopes(excess_t: np.ndarray, loadings: np.ndarray) -> np.ndarray:
    """Perform single-month cross-sectional regression of asset returns on estimated loadings."""
    raise NotImplementedError("implement monthly_slopes")


def shanken_factor(premium_slopes: np.ndarray, factor_cov: np.ndarray) -> float:
    """Calculate the Shanken (1992) errors-in-variables correction multiplier."""
    raise NotImplementedError("implement shanken_factor")


def fama_macbeth(excess: np.ndarray, factors: np.ndarray, train: int) -> FMResult:
    """Execute complete two-pass Fama-MacBeth pipeline with Shanken and GMM standard errors."""
    raise NotImplementedError("implement fama_macbeth")


def conclusion_changes(estimate: float, naive_se: float, shanken_se: float, critical: float) -> bool:
    """Check whether statistical significance conclusion changes between naive and Shanken standard errors."""
    raise NotImplementedError("implement conclusion_changes")
