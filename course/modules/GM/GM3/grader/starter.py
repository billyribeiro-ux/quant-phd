"""Starter code for GM3 Project: Pre-FOMC Drift Out-of-Sample Check.

Implement the functions below. Do not modify signatures or type annotations.
"""

from __future__ import annotations

import numpy as np


def compute_kuttner_surprises(
    pre_rates: np.ndarray,
    post_rates: np.ndarray,
    days_in_month: np.ndarray,
    announcement_days: np.ndarray,
) -> np.ndarray:
    """Compute discrete target rate surprises from Fed funds futures price jumps."""
    raise NotImplementedError("compute_kuttner_surprises not implemented")


def regress_equity_response(
    surprises_bps: np.ndarray,
    equity_returns_bps: np.ndarray,
) -> dict[str, float]:
    """Estimate the Bernanke & Kuttner (2005) equity sensitivity regression."""
    raise NotImplementedError("regress_equity_response not implemented")


def compute_event_window_returns(
    daily_returns: np.ndarray,
    event_indices: np.ndarray,
    window_pre: int = 1,
    window_post: int = 0,
) -> np.ndarray:
    """Compute cumulative equity returns across specified event windows."""
    raise NotImplementedError("compute_event_window_returns not implemented")


def estimate_drift_statistics(window_returns_bps: np.ndarray) -> dict[str, float]:
    """Estimate mean, standard deviation, t-statistic, Sharpe ratio, and win rate."""
    raise NotImplementedError("estimate_drift_statistics not implemented")


def placebo_permutation_test(
    daily_returns: np.ndarray,
    actual_event_indices: np.ndarray,
    n_sims: int = 1000,
    seed: int = 42,
) -> tuple[float, np.ndarray]:
    """Run non-parametric placebo permutation test for pre-announcement drift."""
    raise NotImplementedError("placebo_permutation_test not implemented")


def evaluate_drift_decay(
    in_sample_returns_bps: np.ndarray,
    out_of_sample_returns_bps: np.ndarray,
) -> dict[str, float]:
    """Test for post-publication decay of the pre-FOMC announcement drift."""
    raise NotImplementedError("evaluate_drift_decay not implemented")
