"""Student error: inverts shrinkage weights, inflating estimates with high noise instead of shrinking."""

from __future__ import annotations

import numpy as np
from scipy import stats


def compute_empirical_hurdles(
    t_stats: np.ndarray,
    num_tested: int,
    alpha: float = 0.05,
    correlation_matrix: np.ndarray | None = None,
) -> dict[str, np.ndarray | float]:
    t_arr = np.asarray(t_stats, dtype=np.float64)
    if t_arr.ndim != 1:
        raise ValueError("t_stats must be a 1D array")
    if num_tested < len(t_arr):
        raise ValueError("num_tested cannot be less than the number of provided t-stats")

    alpha_bonf = alpha / float(num_tested)
    hurdle_threshold = float(stats.norm.ppf(1.0 - alpha_bonf / 2.0))
    raw_p_values = 2.0 * (1.0 - stats.norm.cdf(np.abs(t_arr)))
    bonferroni_p_values = np.clip(raw_p_values * float(num_tested), 0.0, 1.0)
    significant_bonferroni = np.abs(t_arr) >= hurdle_threshold

    n_claims = len(t_arr)
    sort_idx = np.argsort(raw_p_values)
    reverse_idx = np.empty(n_claims, dtype=int)
    reverse_idx[sort_idx] = np.arange(n_claims)

    sorted_p = raw_p_values[sort_idx]
    ranks = np.arange(1, n_claims + 1, dtype=np.float64)
    q_raw = sorted_p * float(num_tested) / ranks
    q_monotone = np.minimum.accumulate(q_raw[::-1])[::-1]
    bh_q_values = np.clip(q_monotone[reverse_idx], 0.0, 1.0)
    significant_bh = bh_q_values <= alpha

    return {
        "hurdle_threshold": hurdle_threshold,
        "raw_p_values": raw_p_values,
        "bonferroni_p_values": bonferroni_p_values,
        "bh_q_values": bh_q_values,
        "significant_bonferroni": significant_bonferroni,
        "significant_bh": significant_bh,
    }


def apply_bayesian_shrinkage(
    empirical_means: np.ndarray,
    standard_errors: np.ndarray,
    prior_variance: float | None = None,
) -> dict[str, np.ndarray | float]:
    means = np.asarray(empirical_means, dtype=np.float64)
    se = np.asarray(standard_errors, dtype=np.float64)
    if means.ndim != 1 or se.ndim != 1 or len(means) != len(se):
        raise ValueError("empirical_means and standard_errors must be 1D arrays of matching length")
    if np.any(se <= 0.0):
        raise ValueError("standard errors must be strictly positive")

    k = len(means)
    if prior_variance is None:
        sample_var = float(np.var(means, ddof=1)) if k > 1 else float(np.mean(means**2))
        avg_se_sq = float(np.mean(se**2))
        tau_sq = max(1e-8, sample_var - avg_se_sq)
    else:
        tau_sq = float(prior_variance)
        if tau_sq <= 0.0:
            raise ValueError("prior_variance must be strictly positive")

    se_sq = se**2
    # MUTANT BUG: inverts shrinkage weights, weighting by noise instead of precision
    weights = se_sq / (tau_sq + se_sq)
    shrunken_means = (1.0 + weights) * means

    posterior_var = weights * se_sq
    posterior_sd = np.sqrt(posterior_var)

    z_crit = 1.959963984540054
    ci_lower = shrunken_means - z_crit * posterior_sd
    ci_upper = shrunken_means + z_crit * posterior_sd

    return {
        "shrunken_means": shrunken_means,
        "shrinkage_weights": weights,
        "posterior_sd": posterior_sd,
        "prior_variance": tau_sq,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
    }


def evaluate_oos_decay(
    in_sample_returns: np.ndarray,
    post_discovery_returns: np.ndarray,
    annualization_factor: float = 12.0,
) -> dict[str, float]:
    is_ret = np.asarray(in_sample_returns, dtype=np.float64)
    oos_ret = np.asarray(post_discovery_returns, dtype=np.float64)
    if is_ret.ndim != 1 or oos_ret.ndim != 1:
        raise ValueError("Returns series must be 1D arrays")
    if len(is_ret) < 3 or len(oos_ret) < 3:
        raise ValueError("At least 3 observations required for each period")

    mean_is = float(np.mean(is_ret))
    mean_oos = float(np.mean(oos_ret))
    std_is = float(np.std(is_ret, ddof=1))
    std_oos = float(np.std(oos_ret, ddof=1))

    scale = np.sqrt(annualization_factor)
    sr_is = (mean_is / std_is * scale) if std_is > 1e-12 else 0.0
    sr_oos = (mean_oos / std_oos * scale) if std_oos > 1e-12 else 0.0

    retention_ratio = (mean_oos / mean_is) if abs(mean_is) > 1e-12 else 0.0
    decay_ratio = 1.0 - retention_ratio

    n_is = len(is_ret)
    n_oos = len(oos_ret)
    denom = np.sqrt((std_is**2 / n_is) + (std_oos**2 / n_oos))
    t_stat_decay = float((mean_is - mean_oos) / denom) if denom > 1e-12 else 0.0
    p_val_decay = float(2.0 * (1.0 - stats.norm.cdf(abs(t_stat_decay))))

    variance_ratio = float((std_oos**2) / (std_is**2)) if std_is > 1e-12 else 1.0

    return {
        "mean_is": mean_is,
        "mean_oos": mean_oos,
        "sr_is": sr_is,
        "sr_oos": sr_oos,
        "decay_ratio": decay_ratio,
        "retention_ratio": retention_ratio,
        "t_stat_decay": t_stat_decay,
        "p_val_decay": p_val_decay,
        "variance_ratio": variance_ratio,
    }


def simulate_counterfactual_resolution(
    base_series: np.ndarray,
    intervention_point: int,
    counterfactual_drift: float,
    counterfactual_vol_multiplier: float = 1.0,
    seed: int = 42,
) -> dict[str, np.ndarray | float]:
    series = np.asarray(base_series, dtype=np.float64)
    if series.ndim != 1:
        raise ValueError("base_series must be a 1D array")
    n = len(series)
    if not (1 <= intervention_point < n):
        raise ValueError("intervention_point must be strictly between 1 and len(base_series) - 1")

    innovations = np.diff(series)

    cf_series = np.copy(series)
    for t in range(intervention_point, n):
        idx = t - 1
        innov_base = innovations[idx]
        cf_innov = innov_base * counterfactual_vol_multiplier + counterfactual_drift
        cf_series[t] = cf_series[t - 1] + cf_innov

    factual_post = series[intervention_point:]
    cf_post = cf_series[intervention_point:]
    terminal_divergence = float(cf_series[-1] - series[-1])
    max_divergence = float(np.max(np.abs(cf_post - factual_post)))

    ks_res = stats.ks_2samp(factual_post, cf_post)
    ks_stat = float(ks_res.statistic)
    ks_pvalue = float(ks_res.pvalue)

    return {
        "counterfactual_series": cf_series,
        "terminal_divergence": terminal_divergence,
        "max_divergence": max_divergence,
        "ks_stat": ks_stat,
        "ks_pvalue": ks_pvalue,
    }


def score_debate_evidence(
    claim_metrics: dict[str, float],
    weights: dict[str, float] | None = None,
) -> dict[str, float | str | dict[str, float]]:
    required_keys = [
        "t_stat_hurdle_ratio",
        "shrinkage_retention",
        "oos_retention",
        "counterfactual_resilience",
    ]
    for key in required_keys:
        if key not in claim_metrics:
            raise ValueError(f"Missing required metric in claim_metrics: {key}")

    default_weights = {
        "statistical_rigor": 0.30,
        "economic_magnitude": 0.25,
        "oos_persistence": 0.25,
        "structural_robustness": 0.20,
    }
    raw_weights = weights if weights is not None else default_weights
    w_sum = sum(raw_weights.values())
    if w_sum <= 0.0:
        raise ValueError("Weights must sum to a positive number")
    norm_weights = {k: v / w_sum for k, v in raw_weights.items()}

    s_stat = float(np.clip(claim_metrics["t_stat_hurdle_ratio"] * 80.0, 0.0, 100.0))
    s_econ = float(np.clip(claim_metrics["shrinkage_retention"] * 100.0, 0.0, 100.0))
    s_oos = float(np.clip(claim_metrics["oos_retention"] * 100.0, 0.0, 100.0))
    s_struct = float(np.clip(claim_metrics["counterfactual_resilience"] * 100.0, 0.0, 100.0))

    comp_scores = {
        "statistical_rigor": s_stat,
        "economic_magnitude": s_econ,
        "oos_persistence": s_oos,
        "structural_robustness": s_struct,
    }

    composite_score = float(
        norm_weights["statistical_rigor"] * s_stat
        + norm_weights["economic_magnitude"] * s_econ
        + norm_weights["oos_persistence"] * s_oos
        + norm_weights["structural_robustness"] * s_struct
    )

    if composite_score >= 85.0:
        grade = "A"
    elif composite_score >= 70.0:
        grade = "B"
    elif composite_score >= 50.0:
        grade = "C"
    else:
        grade = "D"

    return {
        "composite_score": composite_score,
        "evidence_grade": grade,
        "component_scores": comp_scores,
        "weights_applied": norm_weights,
    }
