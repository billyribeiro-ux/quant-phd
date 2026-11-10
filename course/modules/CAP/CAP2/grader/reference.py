"""Reference implementation of CAP2 debate tournament evidence evaluation engine.

Implements empirical multiple testing hurdles, empirical Bayes shrinkage,
out-of-sample decay analysis, counterfactual policy simulation, and composite
evidence grading.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def compute_empirical_hurdles(
    t_stats: np.ndarray,
    num_tested: int,
    alpha: float = 0.05,
    correlation_matrix: np.ndarray | None = None,
) -> dict[str, np.ndarray | float]:
    """Compute multiple testing adjusted significance thresholds and p-values.

    Implements Bonferroni and Benjamini-Hochberg (FDR) adjustments for multiple
    hypothesis testing in asset pricing and macroeconomic debates.

    Args:
        t_stats: 1D array of test statistics across tested specifications.
        num_tested: Total number of models/factors tested in universe (M >= len(t_stats)).
        alpha: Nominal family-wise / false discovery error rate (default 0.05).
        correlation_matrix: Optional cross-test correlation matrix.

    Returns:
        Dictionary containing hurdle threshold, adjusted p-values, q-values,
        and boolean significance flags.
    """
    t_arr = np.asarray(t_stats, dtype=np.float64)
    if t_arr.ndim != 1:
        raise ValueError("t_stats must be a 1D array")
    if num_tested < len(t_arr):
        raise ValueError("num_tested cannot be less than the number of provided t-stats")

    # Critical hurdle using Harvey, Liu & Zhu (2016) / Bonferroni normal quantile
    alpha_bonf = alpha / float(num_tested)
    hurdle_threshold = float(stats.norm.ppf(1.0 - alpha_bonf / 2.0))

    # Single-test two-sided p-values
    raw_p_values = 2.0 * (1.0 - stats.norm.cdf(np.abs(t_arr)))

    # Bonferroni adjusted p-values capped at 1.0
    bonferroni_p_values = np.clip(raw_p_values * float(num_tested), 0.0, 1.0)
    significant_bonferroni = np.abs(t_arr) >= hurdle_threshold

    # Benjamini-Hochberg FDR procedure
    n_claims = len(t_arr)
    sort_idx = np.argsort(raw_p_values)
    reverse_idx = np.empty(n_claims, dtype=int)
    reverse_idx[sort_idx] = np.arange(n_claims)

    sorted_p = raw_p_values[sort_idx]
    # Effective rank scaling factor based on total tested models num_tested
    ranks = np.arange(1, n_claims + 1, dtype=np.float64)
    # q-value calculation: (p * M / rank)
    q_raw = sorted_p * float(num_tested) / ranks

    # Monotonicity enforcement (working backwards)
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
    """Apply Empirical Bayes shrinkage to empirical anomaly and debate return premia.

    Shrinks observed noisy empirical estimates toward zero (or a common prior)
    following McLean & Pontiff (2016) and Harvey (2017).

    Args:
        empirical_means: 1D array of observed sample mean premiums.
        standard_errors: 1D array of standard errors for each mean.
        prior_variance: Cross-sectional variance of true premia (tau^2). If None,
            estimated via empirical Bayes marginal maximum likelihood.

    Returns:
        Dictionary containing shrunken means, shrinkage weights, posterior standard
        deviations, prior variance, and 95% credible intervals.
    """
    means = np.asarray(empirical_means, dtype=np.float64)
    se = np.asarray(standard_errors, dtype=np.float64)
    if means.ndim != 1 or se.ndim != 1 or len(means) != len(se):
        raise ValueError("empirical_means and standard_errors must be 1D arrays of matching length")
    if np.any(se <= 0.0):
        raise ValueError("standard errors must be strictly positive")

    k = len(means)
    if prior_variance is None:
        # Estimate cross-sectional true variance tau^2 by subtracting sampling noise
        sample_var = float(np.var(means, ddof=1)) if k > 1 else float(np.mean(means**2))
        avg_se_sq = float(np.mean(se**2))
        tau_sq = max(1e-8, sample_var - avg_se_sq)
    else:
        tau_sq = float(prior_variance)
        if tau_sq <= 0.0:
            raise ValueError("prior_variance must be strictly positive")

    # Shrinkage weight w_i: precision of prior / total precision
    # Estimate is shrunk towards zero: hat{mu}_EB = w_i * hat{mu}
    se_sq = se**2
    weights = tau_sq / (tau_sq + se_sq)
    shrunken_means = weights * means

    # Posterior variance and standard deviations
    posterior_var = weights * se_sq
    posterior_sd = np.sqrt(posterior_var)

    # 95% Credible intervals (normal posterior)
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
    """Evaluate post-publication return decay and out-of-sample persistence.

    Computes Sharpe ratio decay, retention ratio, and Welch's two-sample test
    for structural breakdown between in-sample and out-of-sample periods.

    Args:
        in_sample_returns: 1D array of in-sample returns.
        post_discovery_returns: 1D array of post-discovery returns.
        annualization_factor: Periods per year (default 12 for monthly).

    Returns:
        Dictionary of performance metrics, decay ratios, and test statistics.
    """
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

    # Welch's two-sample t-statistic: H0: mean_is == mean_oos
    n_is = len(is_ret)
    n_oos = len(oos_ret)
    denom = np.sqrt((std_is**2 / n_is) + (std_oos**2 / n_oos))
    t_stat_decay = float((mean_is - mean_oos) / denom) if denom > 1e-12 else 0.0
    # Two-sided p-value
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
    """Simulate a counterfactual trajectory under alternative policy/mechanism assumptions.

    Generates counterfactual paths by modifying innovation drift and volatility
    subsequent to an intervention timestamp.

    Args:
        base_series: 1D baseline empirical series (e.g. cumulative return, inflation, spread).
        intervention_point: Integer index T_0 at which counterfactual policy takes effect.
        counterfactual_drift: Incremental drift per period added to innovations post-intervention.
        counterfactual_vol_multiplier: Multiplier on innovation volatility post-intervention.
        seed: Random seed for optional stochastic residual generation.

    Returns:
        Dictionary with counterfactual series, divergence statistics, and distribution tests.
    """
    series = np.asarray(base_series, dtype=np.float64)
    if series.ndim != 1:
        raise ValueError("base_series must be a 1D array")
    n = len(series)
    if not (1 <= intervention_point < n):
        raise ValueError("intervention_point must be strictly between 1 and len(base_series) - 1")

    # Historical innovations
    innovations = np.diff(series)

    # Counterfactual series starts identical to base series up to intervention
    cf_series = np.copy(series)
    for t in range(intervention_point, n):
        idx = t - 1
        innov_base = innovations[idx]
        cf_innov = innov_base * counterfactual_vol_multiplier + counterfactual_drift
        cf_series[t] = cf_series[t - 1] + cf_innov

    # Metrics
    factual_post = series[intervention_point:]
    cf_post = cf_series[intervention_point:]
    terminal_divergence = float(cf_series[-1] - series[-1])
    max_divergence = float(np.max(np.abs(cf_post - factual_post)))

    # Two-sample Kolmogorov-Smirnov test between post-intervention factual and counterfactual distributions
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
    """Score empirical debate briefs across statistical, economic, and structural pillars.

    Maps multi-dimensional evidence diagnostics into a composite score (0-100)
    and an evidence grade (A, B, C, D).

    Args:
        claim_metrics: Dictionary containing:
            - 't_stat_hurdle_ratio': ratio of empirical t-stat to required hurdle
            - 'shrinkage_retention': ratio of shrunken mean to raw mean
            - 'oos_retention': ratio of OOS mean to IS mean (clamped [0, 1])
            - 'counterfactual_resilience': structural stability metric in [0, 1]
        weights: Optional dictionary of weights for the 4 pillars.

    Returns:
        Dictionary with composite score, assigned evidence grade, component scores,
        and applied normalized weights.
    """
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

    # Pillar scores calibrated to [0, 100]
    # 1. Statistical rigor: ratio of 1.0 (meeting hurdle) gives 80 pts, 1.25 gives 100 pts
    s_stat = float(np.clip(claim_metrics["t_stat_hurdle_ratio"] * 80.0, 0.0, 100.0))
    # 2. Economic magnitude: shrinkage retention (1.0 = no shrinkage, 0.0 = total shrinkage)
    s_econ = float(np.clip(claim_metrics["shrinkage_retention"] * 100.0, 0.0, 100.0))
    # 3. OOS persistence: retention ratio (1.0 = zero decay)
    s_oos = float(np.clip(claim_metrics["oos_retention"] * 100.0, 0.0, 100.0))
    # 4. Structural robustness: resilience under counterfactual interventions
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

    # Grade thresholds: A >= 85, B >= 70, C >= 50, D < 50
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
