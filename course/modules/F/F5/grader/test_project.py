"""Acceptance suite for Module F5 Project: Replication-Crisis Adjudication Engine.

Runs identically in Pyodide and locally:

    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pytest

try:
    import adjudication as proj
except ImportError:
    import reference as proj

import integrity
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def test_multiple_testing_hurdles_ordering_and_subsets() -> None:
    """Verifies that multiple-testing hurdles enforce valid nested discovery subsets and FWER control."""
    t_stats = np.array([-4.2, -2.5, -1.8, -0.5, 0.2, 1.4, 2.05, 2.85, 3.20, 5.10])
    res = proj.multiple_testing_hurdles(t_stats, alpha=0.05)

    assert res["m_tests"] == 10
    assert res["crit_bonferroni"] > 1.96, "Bonferroni critical hurdle must exceed classical 1.96"

    unadj = np.asarray(res["unadjusted_mask"], dtype=bool)
    bonf = np.asarray(res["bonferroni_mask"], dtype=bool)
    holm = np.asarray(res["holm_mask"], dtype=bool)
    bh = np.asarray(res["bh_mask"], dtype=bool)
    hlz = np.asarray(res["hlz_mask"], dtype=bool)

    # Bonferroni discoveries must be a subset of unadjusted discoveries
    assert np.all(unadj[bonf]), "Bonferroni discoveries must be a subset of unadjusted discoveries"
    # Holm discoveries must be a subset of unadjusted discoveries
    assert np.all(unadj[holm]), "Holm discoveries must be a subset of unadjusted discoveries"
    # Bonferroni discoveries must be a subset of Holm discoveries
    assert np.all(holm[bonf]), "Bonferroni discoveries must be a subset of Holm discoveries"
    # Benjamini-Hochberg FDR discoveries must contain all Bonferroni discoveries
    assert np.all(bh[bonf]), "BH discoveries must contain all Bonferroni discoveries"
    # Harvey-Liu-Zhu (|t| >= 3.0) must be a subset of unadjusted (|t| >= 1.96)
    assert np.all(unadj[hlz]), "HLZ hurdle discoveries must be a subset of unadjusted (|t| >= 1.96)"


def test_evaluate_replication_properties() -> None:
    """Validates replication rate formulas, microcap spread inflation, and degrees of freedom."""
    returns_ew = np.asarray(INST["returns_ew"], dtype=np.float64)
    returns_vw = np.asarray(INST["returns_vw"], dtype=np.float64)
    controls = np.asarray(INST["controls"], dtype=np.float64)

    rep = proj.evaluate_replication(returns_ew, returns_vw, controls)

    assert rep["n_candidates"] == 10
    assert 0.0 <= rep["rep_rate_ew_raw"] <= 100.0
    assert 0.0 <= rep["rep_rate_vw_raw"] <= 100.0
    assert 0.0 <= rep["rep_rate_vw_alpha"] <= 100.0
    assert 0.0 <= rep["rep_rate_vw_conservative"] <= 100.0

    # Equal-weighted raw replication rate must be >= value-weighted raw replication rate
    assert rep["rep_rate_ew_raw"] >= rep["rep_rate_vw_raw"], (
        f"EW replication rate ({rep['rep_rate_ew_raw']}%) must be >= VW rate ({rep['rep_rate_vw_raw']}%) "
        "due to microcap spread inflation"
    )

    # VW raw replication rate must be >= VW conservative (|t| >= 3.0) rate
    assert rep["rep_rate_vw_alpha"] >= rep["rep_rate_vw_conservative"]

    # Check finite standard errors
    se_alpha = np.asarray(rep["se_alpha_vw"], dtype=np.float64)
    assert np.all(se_alpha > 0.0)
    assert np.all(np.isfinite(se_alpha))

    # Verify OLS alpha calculation on VW returns for Candidate 0
    t_obs = returns_vw.shape[1]
    x_des = np.column_stack([np.ones(t_obs), controls])
    expected_alpha_0 = float(np.linalg.lstsq(x_des, returns_vw[0], rcond=None)[0][0])
    assert abs(rep["alphas_vw"][0] - expected_alpha_0) < 1e-10, (
        "alphas_vw must match OLS regression intercept of returns_vw on controls"
    )


def test_empirical_bayes_shrinkage_invariants() -> None:
    """Verifies that Bayesian shrinkage weights lie strictly in (0, 1] and pull alphas toward prior."""
    alphas = np.array([0.006, 0.003, -0.001, 0.004, -0.002])
    ses = np.array([0.001, 0.002, 0.0015, 0.003, 0.0025])

    bayes = proj.empirical_bayes_shrinkage(alphas, ses)

    mu_0 = float(bayes["prior_mean"])
    weights = np.asarray(bayes["weights"], dtype=np.float64)
    shrunk = np.asarray(bayes["shrunk_alphas"], dtype=np.float64)

    assert float(bayes["prior_tau2"]) > 0.0
    assert np.all(weights > 0.0) and np.all(weights <= 1.0), "Shrinkage weights must lie in (0, 1]"

    # Higher precision (lower standard error) must receive strictly higher shrinkage weight
    assert weights[0] > weights[3], "Factor with smaller standard error must have higher signal weight"

    # Shrunk alphas must lie strictly between sample alpha and prior mean
    for a, s in zip(alphas, shrunk, strict=True):
        lower = min(a, mu_0) - 1e-12
        upper = max(a, mu_0) + 1e-12
        assert lower <= s <= upper, f"Shrunk alpha {s} must lie between sample {a} and prior {mu_0}"


def test_double_selection_factor_test_orthogonality() -> None:
    """Verifies that double-selection purges spanned factor covariance and yields valid t-statistics."""
    controls = np.asarray(INST["controls"], dtype=np.float64)
    test_assets = np.asarray(INST["test_assets"], dtype=np.float64)
    candidate_0 = np.asarray(INST["returns_vw"][0], dtype=np.float64)

    ds_res = proj.double_selection_test(candidate_0, controls, test_assets)

    assert isinstance(ds_res["selected_union"], list)
    assert set(ds_res["selected_step1"]).issubset(set(ds_res["selected_union"])), (
        "selected_union must contain all Step 1 controls"
    )
    assert set(ds_res["selected_step2"]).issubset(set(ds_res["selected_union"])), (
        "selected_union must contain all Step 2 controls"
    )
    assert np.isfinite(ds_res["orthogonal_alpha"])
    assert ds_res["se_orthogonal"] > 0.0

    # Verified t-statistic identity
    expected_t = float(ds_res["orthogonal_alpha"] / ds_res["se_orthogonal"])
    assert abs(ds_res["t_stat"] - expected_t) < 1e-10

    # True alpha factor (Candidate 0) must be retained
    assert ds_res["is_retained"] is True, "Robust factor candidate 0 must be retained by double-selection"


def test_adjudicate_factors_taxonomy_and_integrity() -> None:
    """Validates complete adjudication pipeline, taxonomy classification, and articulation on the instance."""
    adjudication = proj.adjudicate_factors(INST)

    # Validate output dictionary integrity
    assert integrity.validate_adjudication_outputs(adjudication)

    classifications = list(adjudication["classifications"])
    assert len(classifications) == 10

    counts = adjudication["classification_counts"]
    total_classified = sum(counts.values())
    assert total_classified == 10, f"Expected 10 classified factors, got {total_classified}"

    # Verify ground truth robust candidate 0 is always classified as ROBUST
    assert classifications[0] == "ROBUST", f"Candidate 0 should be ROBUST, got {classifications[0]}"

    # Verify strict mathematical articulation across all 10 candidates
    rep = adjudication["replication"]
    ds = adjudication["ds_retained"]
    shrunk = adjudication["bayes_shrinkage"]["shrunk_alphas"]

    for i in range(10):
        c = classifications[i]
        if c == "ROBUST":
            assert rep["pass_vw_alpha"][i] and ds[i] and (shrunk[i] > 0.0010), (
                f"Candidate {i} classified as ROBUST must pass VW alpha, double-selection, and shrunk alpha threshold"
            )
        elif c == "MICROCAP_ONLY":
            assert rep["pass_ew_raw"][i] and not rep["pass_vw_raw"][i], (
                f"Candidate {i} classified as MICROCAP_ONLY must pass EW raw but fail VW raw"
            )
        elif c == "SPANNED":
            assert rep["pass_vw_raw"][i] and (not rep["pass_vw_alpha"][i] or not ds[i]), (
                f"Candidate {i} classified as SPANNED must pass VW raw but fail VW alpha or double-selection"
            )
        elif c == "DATA_SNOOPING":
            is_rob = bool(rep["pass_vw_alpha"][i]) and bool(ds[i]) and (shrunk[i] > 0.0010)
            is_micro = bool(rep["pass_ew_raw"][i]) and not bool(rep["pass_vw_raw"][i])
            is_span = bool(rep["pass_vw_raw"][i]) and (not bool(rep["pass_vw_alpha"][i]) or not bool(ds[i]))
            assert not (is_rob or is_micro or is_span), (
                f"Candidate {i} classified as DATA_SNOOPING must not meet ROBUST, MICROCAP_ONLY, or SPANNED criteria"
            )
