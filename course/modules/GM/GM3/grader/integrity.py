"""Integrity and input validation module for GM3 Grader.

Ensures strict typing, bounds checking, shape consistency, and mathematical invariants
for FOMC event studies, futures scaling, and out-of-sample drift evaluation.
"""

from __future__ import annotations

import numpy as np


def validate_futures_inputs(
    pre_rates: np.ndarray,
    post_rates: np.ndarray,
    days_in_month: np.ndarray,
    announcement_days: np.ndarray,
) -> None:
    """Validate arrays for Kuttner futures scaling."""
    if not isinstance(pre_rates, np.ndarray) or not isinstance(post_rates, np.ndarray):
        raise TypeError("pre_rates and post_rates must be numpy.ndarray instances")
    if pre_rates.ndim != 1 or post_rates.ndim != 1:
        raise ValueError(f"rates must be 1D arrays (got {pre_rates.ndim}D and {post_rates.ndim}D)")
    if len(pre_rates) != len(post_rates):
        raise ValueError("length mismatch between pre_rates and post_rates")
    if len(pre_rates) != len(days_in_month) or len(pre_rates) != len(announcement_days):
        raise ValueError("calendar arrays must match length of rate arrays")
    if np.any(np.isnan(pre_rates)) or np.any(np.isnan(post_rates)):
        raise ValueError("rate arrays contain NaN values")
    if np.any(np.isinf(pre_rates)) or np.any(np.isinf(post_rates)):
        raise ValueError("rate arrays contain infinite values")


def validate_event_indices(event_indices: np.ndarray, n_days: int) -> None:
    """Validate event day index array."""
    if not isinstance(event_indices, np.ndarray):
        raise TypeError("event_indices must be numpy.ndarray")
    if event_indices.ndim != 1:
        raise ValueError("event_indices must be 1D array")
    if len(event_indices) == 0:
        raise ValueError("event_indices must not be empty")
    if np.any(event_indices < 1) or np.any(event_indices >= n_days):
        raise ValueError(f"event indices outside valid range [1, {n_days})")
    if np.any(np.diff(event_indices) <= 0):
        raise ValueError("event indices must be strictly monotonically increasing")
