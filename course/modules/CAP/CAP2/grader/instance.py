"""Deterministic instance generator for CAP2 debate tournament project."""

from __future__ import annotations

import numpy as np


def make_instance(seed: int) -> dict[str, object]:
    """Generate synthetic debate evidence datasets for a specific seed.

    Returns:
        Dictionary containing test statistics, factor universes, empirical
        premia, time series returns, and macro policy series.
    """
    rng = np.random.default_rng(seed)

    # Number of claims and total tested universe M
    n_claims = int(rng.integers(8, 16))
    num_tested = int(rng.integers(180, 360))

    # Empirical t-statistics: a mix of strong, marginal, and spurious claims
    # Shift slightly with seed
    t_base = rng.normal(2.2, 0.9, size=n_claims)
    # Ensure at least two strong claims and two weak claims
    t_base[0] = 3.6 + float(rng.uniform(0.1, 0.8))
    t_base[1] = 1.4 + float(rng.uniform(0.1, 0.4))
    t_stats = np.abs(t_base)

    # Random correlation matrix (valid symmetric positive semi-definite)
    raw_w = rng.normal(0.0, 1.0, size=(n_claims, 4))
    cov = raw_w @ raw_w.T + np.eye(n_claims) * 0.5
    d_inv = np.diag(1.0 / np.sqrt(np.diag(cov)))
    corr_matrix = d_inv @ cov @ d_inv

    # Cross-sectional empirical anomaly means and standard errors
    n_anomalies = int(rng.integers(6, 12))
    empirical_means = rng.uniform(0.003, 0.015, size=n_anomalies)
    standard_errors = rng.uniform(0.0015, 0.0045, size=n_anomalies)
    prior_variance = float(0.00005 + rng.uniform(0.00001, 0.0001))

    # In-sample vs post-discovery returns
    n_is = int(rng.integers(100, 180))
    n_oos = int(rng.integers(48, 84))

    true_is_mean = float(rng.uniform(0.007, 0.012))
    true_oos_mean = true_is_mean * float(rng.uniform(0.40, 0.85))  # partial decay
    vol = float(rng.uniform(0.035, 0.055))

    in_sample_returns = rng.normal(true_is_mean, vol, size=n_is)
    post_discovery_returns = rng.normal(true_oos_mean, vol * 1.05, size=n_oos)

    # Baseline macro / inflation / spread series for counterfactual simulation
    n_series = int(rng.integers(150, 240))
    intervention_point = int(n_series * 0.65)
    innovations = rng.normal(0.001, 0.02, size=n_series)
    base_series = 100.0 + np.cumsum(innovations)

    counterfactual_drift = float(rng.uniform(-0.005, -0.001))
    counterfactual_vol_multiplier = float(rng.uniform(1.10, 1.40))

    # Claim metrics and weights as flat scalar floats
    metric_t_stat_hurdle_ratio = float(rng.uniform(0.85, 1.35))
    metric_shrinkage_retention = float(rng.uniform(0.65, 0.95))
    metric_oos_retention = float(rng.uniform(0.50, 0.90))
    metric_counterfactual_resilience = float(rng.uniform(0.60, 0.92))

    weight_statistical_rigor = 0.35
    weight_economic_magnitude = 0.25
    weight_oos_persistence = 0.25
    weight_structural_robustness = 0.15

    return {
        "seed": seed,
        "t_stats": t_stats,
        "num_tested": num_tested,
        "corr_matrix": corr_matrix,
        "empirical_means": empirical_means,
        "standard_errors": standard_errors,
        "prior_variance": prior_variance,
        "in_sample_returns": in_sample_returns,
        "post_discovery_returns": post_discovery_returns,
        "base_series": base_series,
        "intervention_point": intervention_point,
        "counterfactual_drift": counterfactual_drift,
        "counterfactual_vol_multiplier": counterfactual_vol_multiplier,
        "metric_t_stat_hurdle_ratio": metric_t_stat_hurdle_ratio,
        "metric_shrinkage_retention": metric_shrinkage_retention,
        "metric_oos_retention": metric_oos_retention,
        "metric_counterfactual_resilience": metric_counterfactual_resilience,
        "weight_statistical_rigor": weight_statistical_rigor,
        "weight_economic_magnitude": weight_economic_magnitude,
        "weight_oos_persistence": weight_oos_persistence,
        "weight_structural_robustness": weight_structural_robustness,
    }
