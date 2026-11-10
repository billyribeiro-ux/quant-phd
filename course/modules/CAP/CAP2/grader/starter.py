"""Starter code for CAP2 debate tournament evidence evaluation engine."""

from __future__ import annotations

import numpy as np


def compute_empirical_hurdles(
    t_stats: np.ndarray,
    num_tested: int,
    alpha: float = 0.05,
    correlation_matrix: np.ndarray | None = None,
) -> dict[str, np.ndarray | float]:
    """Compute multiple testing adjusted significance thresholds and p-values."""
    raise NotImplementedError("Student solution goes here")


def apply_bayesian_shrinkage(
    empirical_means: np.ndarray,
    standard_errors: np.ndarray,
    prior_variance: float | None = None,
) -> dict[str, np.ndarray | float]:
    """Apply Empirical Bayes shrinkage to empirical anomaly and debate return premia."""
    raise NotImplementedError("Student solution goes here")


def evaluate_oos_decay(
    in_sample_returns: np.ndarray,
    post_discovery_returns: np.ndarray,
    annualization_factor: float = 12.0,
) -> dict[str, float]:
    """Evaluate post-publication return decay and out-of-sample persistence."""
    raise NotImplementedError("Student solution goes here")


def simulate_counterfactual_resolution(
    base_series: np.ndarray,
    intervention_point: int,
    counterfactual_drift: float,
    counterfactual_vol_multiplier: float = 1.0,
    seed: int = 42,
) -> dict[str, np.ndarray | float]:
    """Simulate a counterfactual trajectory under alternative policy/mechanism assumptions."""
    raise NotImplementedError("Student solution goes here")


def score_debate_evidence(
    claim_metrics: dict[str, float],
    weights: dict[str, float] | None = None,
) -> dict[str, float | str | dict[str, float]]:
    """Score empirical debate briefs across statistical, economic, and structural pillars."""
    raise NotImplementedError("Student solution goes here")
