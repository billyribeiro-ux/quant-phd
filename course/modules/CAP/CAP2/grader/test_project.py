"""Test suite for CAP2 debate tournament evidence evaluation engine."""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pytest

# The grader workspace loads the candidate solution as debate_engine
from debate_engine import (
    apply_bayesian_shrinkage,
    compute_empirical_hurdles,
    evaluate_oos_decay,
    score_debate_evidence,
    simulate_counterfactual_resolution,
)
from instance import make_instance

SEED = int(os.environ.get("QF_SEED", "42"))


@pytest.fixture(scope="module")
def inst() -> dict[str, Any]:
    """Generate instance dataset for active seed."""
    return make_instance(SEED)


def test_empirical_hurdles_properties(inst: dict[str, Any]) -> None:
    """Verify multiple testing adjusted thresholds, Bonferroni bounds, and FDR q-values."""
    t_stats = np.asarray(inst["t_stats"], dtype=np.float64)
    num_tested = int(inst["num_tested"])

    res = compute_empirical_hurdles(t_stats, num_tested, alpha=0.05)

    hurdle = float(res["hurdle_threshold"])
    # For M >= 180 and alpha = 0.05, Bonferroni hurdle exceeds 3.0 (Harvey et al. 2016)
    assert hurdle >= 3.0, f"Multiple testing hurdle {hurdle} must be >= 3.0 for M={num_tested}"

    bonf_p = np.asarray(res["bonferroni_p_values"])
    raw_p = np.asarray(res["raw_p_values"])
    bh_q = np.asarray(res["bh_q_values"])
    sig_bonf = np.asarray(res["significant_bonferroni"])
    sig_bh = np.asarray(res["significant_bh"])

    # Invariants: probabilities and q-values bounded in [0, 1]
    assert np.all(bonf_p >= 0.0) and np.all(bonf_p <= 1.0)
    assert np.all(raw_p >= 0.0) and np.all(raw_p <= 1.0)
    assert np.all(bh_q >= 0.0) and np.all(bh_q <= 1.0)

    # Bonferroni bound is weakly conservative relative to raw p-values
    assert np.all(bonf_p >= raw_p)

    # Benjamini-Hochberg FDR control is weakly less conservative than FWER Bonferroni
    # Every Bonferroni-significant test must also be BH-significant
    assert np.all(sig_bh[sig_bonf]), "Bonferroni significant claims must also be FDR significant"

    # Monotonicity: higher |t| implies lower or equal raw p-value
    sort_t = np.argsort(np.abs(t_stats))
    assert np.all(np.diff(raw_p[sort_t]) <= 1e-12), "Raw p-values must be inversely monotonic to |t|"

    # Input validation
    with pytest.raises(ValueError):
        compute_empirical_hurdles(t_stats, num_tested=len(t_stats) - 1)


def test_bayesian_shrinkage_properties(inst: dict[str, Any]) -> None:
    """Verify Empirical Bayes shrinkage intensity and posterior variance reduction."""
    means = np.asarray(inst["empirical_means"], dtype=np.float64)
    se = np.asarray(inst["standard_errors"], dtype=np.float64)
    prior_var = float(inst["prior_variance"])

    res = apply_bayesian_shrinkage(means, se, prior_variance=prior_var)

    shrunken = np.asarray(res["shrunken_means"])
    weights = np.asarray(res["shrinkage_weights"])
    post_sd = np.asarray(res["posterior_sd"])
    ci_lower = np.asarray(res["ci_lower"])
    ci_upper = np.asarray(res["ci_upper"])

    # Shrinkage weights must strictly lie in (0, 1) for positive noise and prior variance
    assert np.all(weights > 0.0) and np.all(weights < 1.0), "Shrinkage weights must lie strictly in (0, 1)"

    # Shrunken means must shrink toward prior mean (0.0): |shrunken| <= |raw|
    assert np.all(np.abs(shrunken) <= np.abs(means) + 1e-12), "Empirical Bayes must shrink estimates toward zero"

    # Posterior variance must be strictly smaller than prior variance and sampling variance
    assert np.all(post_sd < se), "Posterior standard error must be strictly smaller than sampling standard error"
    assert np.all(post_sd < np.sqrt(prior_var) + 1e-9)

    # Relative shrinkage: higher SE must receive lower weight (greater shrinkage toward 0)
    se_sorted_idx = np.argsort(se)
    assert np.all(np.diff(weights[se_sorted_idx]) <= 1e-12), "Larger standard errors must receive smaller weights"

    # Articulation of credible intervals
    assert np.all(ci_lower < shrunken) and np.all(shrunken < ci_upper)
    width = ci_upper - ci_lower
    expected_width = 2.0 * 1.959963984540054 * post_sd
    assert np.allclose(width, expected_width, rtol=1e-5)


def test_oos_decay_properties(inst: dict[str, Any]) -> None:
    """Verify out-of-sample decay, retention ratios, and Welch's two-sample test."""
    is_ret = np.asarray(inst["in_sample_returns"], dtype=np.float64)
    oos_ret = np.asarray(inst["post_discovery_returns"], dtype=np.float64)

    res = evaluate_oos_decay(is_ret, oos_ret, annualization_factor=12.0)

    mean_is = float(res["mean_is"])
    mean_oos = float(res["mean_oos"])
    decay_ratio = float(res["decay_ratio"])
    retention_ratio = float(res["retention_ratio"])
    t_decay = float(res["t_stat_decay"])
    p_decay = float(res["p_val_decay"])

    # Exact mathematical articulation: decay_ratio + retention_ratio == 1.0
    assert abs(decay_ratio + retention_ratio - 1.0) < 1e-9, "Decay ratio and retention ratio must articulate to 1.0"

    # Verify Welch t-statistic formula explicitly
    s_is = float(np.std(is_ret, ddof=1))
    s_oos = float(np.std(oos_ret, ddof=1))
    expected_denom = np.sqrt(s_is**2 / len(is_ret) + s_oos**2 / len(oos_ret))
    expected_t = (mean_is - mean_oos) / expected_denom
    assert abs(t_decay - expected_t) < 1e-6, "Welch t-statistic must match exact formula"

    # p-value valid probability
    assert 0.0 <= p_decay <= 1.0

    # Annualized Sharpe ratio check
    assert abs(res["sr_is"] - (mean_is / s_is * np.sqrt(12.0))) < 1e-6
    assert abs(res["sr_oos"] - (mean_oos / s_oos * np.sqrt(12.0))) < 1e-6


def test_counterfactual_simulation_properties(inst: dict[str, Any]) -> None:
    """Verify counterfactual trajectory generation and distribution testing."""
    base = np.asarray(inst["base_series"], dtype=np.float64)
    t0 = int(inst["intervention_point"])
    drift = float(inst["counterfactual_drift"])
    vol_mult = float(inst["counterfactual_vol_multiplier"])

    res = simulate_counterfactual_resolution(base, t0, drift, counterfactual_vol_multiplier=vol_mult)

    cf = np.asarray(res["counterfactual_series"])
    term_div = float(res["terminal_divergence"])
    max_div = float(res["max_divergence"])
    ks_stat = float(res["ks_stat"])
    ks_p = float(res["ks_pvalue"])

    # Invariant: Prior to intervention point, counterfactual series must be identical to base series
    assert np.allclose(cf[:t0], base[:t0]), "Counterfactual series must exactly match base series before intervention"

    # Since counterfactual drift is non-zero, post-intervention series must diverge from base
    assert not np.allclose(cf[t0:], base[t0:]), "Counterfactual path must diverge from baseline when drift is non-zero"
    assert abs(term_div) > 1e-4, "Terminal divergence must be non-zero for non-zero drift"

    # Terminal divergence identity
    assert abs(term_div - (cf[-1] - base[-1])) < 1e-9

    # Max absolute divergence must be >= |terminal divergence|
    assert max_div >= abs(term_div) - 1e-9

    # KS statistic properties
    assert 0.0 <= ks_stat <= 1.0
    assert 0.0 <= ks_p <= 1.0


def test_score_debate_evidence_properties(inst: dict[str, Any]) -> None:
    """Verify multi-pillar evidence scoring, normalization, and grade thresholds."""
    metrics = {
        "t_stat_hurdle_ratio": float(inst["metric_t_stat_hurdle_ratio"]),
        "shrinkage_retention": float(inst["metric_shrinkage_retention"]),
        "oos_retention": float(inst["metric_oos_retention"]),
        "counterfactual_resilience": float(inst["metric_counterfactual_resilience"]),
    }
    weights = {
        "statistical_rigor": float(inst["weight_statistical_rigor"]),
        "economic_magnitude": float(inst["weight_economic_magnitude"]),
        "oos_persistence": float(inst["weight_oos_persistence"]),
        "structural_robustness": float(inst["weight_structural_robustness"]),
    }

    res = score_debate_evidence(metrics, weights=weights)

    comp_score = float(res["composite_score"])
    grade = str(res["evidence_grade"])
    scores = dict(res["component_scores"])

    # Score bounded in [0, 100]
    assert 0.0 <= comp_score <= 100.0, "Composite score must lie in [0, 100]"

    # Grade consistency check
    if comp_score >= 85.0:
        assert grade == "A"
    elif comp_score >= 70.0:
        assert grade == "B"
    elif comp_score >= 50.0:
        assert grade == "C"
    else:
        assert grade == "D"

    # Articulation: composite score equals weighted sum of component scores
    norm_w = res["weights_applied"]
    expected_score = sum(norm_w[k] * scores[k] for k in scores)
    assert abs(comp_score - expected_score) < 1e-6, "Composite score must articulate with weighted component scores"

    # User-specified weights must be respected after normalization
    raw_w = {
        "statistical_rigor": float(inst["weight_statistical_rigor"]),
        "economic_magnitude": float(inst["weight_economic_magnitude"]),
        "oos_persistence": float(inst["weight_oos_persistence"]),
        "structural_robustness": float(inst["weight_structural_robustness"]),
    }
    w_sum = sum(raw_w.values())
    expected_norm_w = {k: v / w_sum for k, v in raw_w.items()}
    for k in expected_norm_w:
        msg = f"Applied weight for {k} must match requested normalized weight"
        assert abs(norm_w[k] - expected_norm_w[k]) < 1e-6, msg


def test_articulation_and_boundary_conditions(inst: dict[str, Any]) -> None:
    """Verify edge cases and monotonic response of evidence grading."""
    # Perfect score test
    perfect_metrics = {
        "t_stat_hurdle_ratio": 2.0,
        "shrinkage_retention": 1.0,
        "oos_retention": 1.0,
        "counterfactual_resilience": 1.0,
    }
    perfect_res = score_debate_evidence(perfect_metrics)
    assert perfect_res["composite_score"] >= 95.0
    assert perfect_res["evidence_grade"] == "A"

    # Zero score test
    zero_metrics = {
        "t_stat_hurdle_ratio": 0.0,
        "shrinkage_retention": 0.0,
        "oos_retention": 0.0,
        "counterfactual_resilience": 0.0,
    }
    zero_res = score_debate_evidence(zero_metrics)
    assert zero_res["composite_score"] == 0.0
    assert zero_res["evidence_grade"] == "D"
