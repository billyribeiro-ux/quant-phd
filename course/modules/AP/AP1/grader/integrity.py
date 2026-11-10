"""Input and output integrity validation for AP1: No-Arbitrage & the Stochastic Discount Factor.

Provides structural invariant checks, matrix condition checks, and input/output
validation for SDF estimation and recovery routines.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray

_RANK_TOL: float = 1e-10


def validate_payoffs(payoffs: ArrayLike, name: str = "payoffs") -> NDArray[np.float64]:
    """Validate a payoff matrix (T_observations x N_assets)."""
    arr = np.array(payoffs, dtype=np.float64)
    if arr.ndim != 2:
        raise ValueError(f"{name} must be two-dimensional (observations x assets)")
    if arr.shape[0] < 1 or arr.shape[1] < 1:
        raise ValueError(f"{name} needs at least one observation and one asset")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must be finite")
    return arr


def validate_prices(prices: ArrayLike, length: int | None = None, name: str = "prices") -> NDArray[np.float64]:
    """Validate a price vector (N_assets)."""
    v = np.array(prices, dtype=np.float64)
    if v.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if length is not None and v.size != length:
        raise ValueError(f"{name} must have one entry per asset ({length}), not {v.size}")
    if not np.all(np.isfinite(v)):
        raise ValueError(f"{name} must be finite")
    return v


def validate_probs(probs: ArrayLike, length: int | None = None, name: str = "probs") -> NDArray[np.float64]:
    """Validate a probability vector across states (S_states)."""
    pi = np.array(probs, dtype=np.float64)
    if pi.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if length is not None and pi.size != length:
        raise ValueError(f"{name} must have one entry per state ({length}), not {pi.size}")
    if not np.all(np.isfinite(pi)):
        raise ValueError(f"{name} must be finite")
    if np.any(pi <= 0.0):
        raise ValueError("probs must be strictly positive")
    if abs(float(pi.sum()) - 1.0) > 1e-9:
        raise ValueError("probs must sum to one")
    return pi


def validate_sdf(sdf: ArrayLike, length: int | None = None, name: str = "sdf") -> NDArray[np.float64]:
    """Validate a realized SDF vector (T_observations)."""
    m = np.array(sdf, dtype=np.float64)
    if m.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if length is not None and m.size != length:
        raise ValueError(f"{name} must have one entry per observation ({length}), not {m.size}")
    if not np.all(np.isfinite(m)):
        raise ValueError(f"{name} must be finite")
    return m


def check_linear_independence(payoffs: NDArray[np.float64], name: str = "payoffs", tol: float = _RANK_TOL) -> None:
    """Verify that payoff columns are linearly independent (no redundant assets)."""
    if payoffs.shape[0] < payoffs.shape[1]:
        raise ValueError(f"{name} needs at least as many observations as assets")
    s = np.linalg.svd(payoffs, compute_uv=False)
    if s[-1] <= tol * s[0]:
        raise ValueError(f"{name} must have linearly independent columns (no redundant payoff)")


def validate_recovery_result(result: Any) -> bool:
    """Validate structural invariants of an SDFRecoveryResult."""
    required_attrs = (
        "weights",
        "in_sample_pricing_errors",
        "in_sample_rms",
        "out_of_sample_pricing_errors",
        "out_of_sample_rms",
        "train_mean",
        "train_std",
        "test_share_negative",
    )
    for attr in required_attrs:
        if not hasattr(result, attr):
            raise ValueError(f"Result missing required attribute: {attr}")

    weights = np.asarray(result.weights, dtype=np.float64)
    if weights.ndim != 1 or not np.all(np.isfinite(weights)):
        raise ValueError("weights must be finite 1D array")

    train_mean = float(result.train_mean)
    train_std = float(result.train_std)
    if not (math.isfinite(train_mean) and math.isfinite(train_std) and train_std >= 0.0):
        raise ValueError("train_mean and train_std must be finite, std non-negative")

    share_neg = float(result.test_share_negative)
    if not (0.0 <= share_neg <= 1.0):
        raise ValueError("test_share_negative must be in [0, 1]")

    return True
