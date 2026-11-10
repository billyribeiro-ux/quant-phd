"""Integrity and input validation module for GM2 Grader.

Ensures strict typing, bounds checking, shape consistency, and mathematical invariants
for regime classification, moment estimation, and asset allocation.
"""

from __future__ import annotations

from typing import cast

import numpy as np


def validate_series_pair(growth: np.ndarray, inflation: np.ndarray) -> None:
    """Validate that growth and inflation series are 1D, identical length, and non-empty."""
    if not isinstance(growth, np.ndarray) or not isinstance(inflation, np.ndarray):
        raise TypeError("growth and inflation must be numpy.ndarray instances")
    if growth.ndim != 1 or inflation.ndim != 1:
        raise ValueError(f"growth and inflation must be 1D (got {growth.ndim}D and {inflation.ndim}D)")
    if len(growth) != len(inflation):
        raise ValueError(f"growth and inflation length mismatch: {len(growth)} != {len(inflation)}")
    if len(growth) < 36:
        raise ValueError(f"sample size too short for regime analysis: {len(growth)} < 36")
    if np.any(np.isnan(growth)) or np.any(np.isnan(inflation)):
        raise ValueError("input series contain NaN values")
    if np.any(np.isinf(growth)) or np.any(np.isinf(inflation)):
        raise ValueError("input series contain infinite values")


def validate_returns_and_regimes(returns: np.ndarray, regimes: np.ndarray) -> None:
    """Validate asset returns panel and discrete regime labels."""
    if not isinstance(returns, np.ndarray) or not isinstance(regimes, np.ndarray):
        raise TypeError("returns and regimes must be numpy.ndarray instances")
    if returns.ndim != 2:
        raise ValueError(f"returns must be 2D array of shape (T, N), got {returns.ndim}D")
    if regimes.ndim != 1:
        raise ValueError(f"regimes must be 1D array of shape (T,), got {regimes.ndim}D")
    if len(returns) != len(regimes):
        raise ValueError(f"length mismatch between returns ({len(returns)}) and regimes ({len(regimes)})")
    if np.any(np.isnan(returns)) or np.any(np.isinf(returns)):
        raise ValueError("returns contain NaN or infinite values")


def validate_simplex_weights(weights: np.ndarray, tol: float = 1e-5) -> None:
    """Check that portfolio weights lie on the standard simplex (sum to 1, non-negative)."""
    if np.any(weights < -tol):
        raise ValueError(f"weights contain negative entries (min: {np.min(weights)})")
    weight_sum = float(np.sum(weights))
    if abs(weight_sum - 1.0) > tol:
        raise ValueError(f"weights do not sum to 1.0 (sum: {weight_sum})")


def project_to_simplex(v: np.ndarray) -> np.ndarray:
    """Project a real vector v onto the standard probability simplex.

    Solves: min_w 0.5 ||w - v||_2^2 s.t. sum(w) = 1, w >= 0.
    Implementation follows Duchi, Shalev-Shwartz, Singer & Chandra (2008).
    """
    n = len(v)
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u) - 1.0
    ind = np.arange(1, n + 1)
    cond = u - cssv / ind > 0
    if not np.any(cond):
        return np.full(n, 1.0 / n)
    rho = np.nonzero(cond)[0][-1]
    theta = cssv[rho] / (rho + 1)
    w = np.maximum(v - theta, 0.0)
    return cast(np.ndarray, w / np.sum(w))
