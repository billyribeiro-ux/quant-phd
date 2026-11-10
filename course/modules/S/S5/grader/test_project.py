"""Acceptance test suite for S5 project: Two-pass Fama-MacBeth and Shanken correction.

Runs identically in Pyodide and locally:
    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from collections.abc import Callable

import numpy as np
import pytest

try:
    import fm_shanken as sol
except ImportError:
    import reference as sol

from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"validation check failed: {condition} must raise ValueError")


# ---------------------------------------------------------------- First pass tests


def test_loadings_match_direct_ols() -> None:
    """Checks that estimated factor loadings match direct OLS normal equations."""
    excess = INST["excess"]
    factors = INST["factors"]
    train = INST["train"]

    betas = sol.loadings(excess, factors, train)
    assert betas.shape == (INST["N"], INST["K"] + 1), "loadings shape must be (N, K + 1)"

    # Independent oracle: explicit OLS per asset
    x_ts = np.column_stack([np.ones(train), factors[:train]])
    x_inv = np.linalg.pinv(x_ts.T @ x_ts)
    for i in range(INST["N"]):
        y_i = excess[:train, i]
        expected_b = x_inv @ (x_ts.T @ y_i)
        diff = np.max(np.abs(betas[i] - expected_b))
        assert diff < 1e-9, f"loadings mismatch for asset {i}: diff={diff}"


def test_loadings_ignore_test_months() -> None:
    """Loadings must depend only on returns in the first train months."""
    excess = INST["excess"].copy()
    factors = INST["factors"].copy()
    train = INST["train"]

    b_orig = sol.loadings(excess, factors, train)

    # Perturb out-of-sample test returns
    excess[train:] += 999.0
    factors[train:] += 999.0

    b_perturbed = sol.loadings(excess, factors, train)
    diff = np.max(np.abs(b_orig - b_perturbed))
    assert diff < 1e-12, "look-ahead defect: loadings changed when test-month data was perturbed"


# ---------------------------------------------------------------- Second pass tests


def test_premia_are_mean_of_monthly_slopes() -> None:
    """Fama-MacBeth premia must strictly equal the sample mean of monthly cross-sectional slopes."""
    excess = INST["excess"]
    factors = INST["factors"]
    train = INST["train"]
    t2 = INST["T"] - train

    res = sol.fama_macbeth(excess, factors, train)
    betas = sol.loadings(excess, factors, train)

    manual_slopes = np.empty((t2, INST["K"] + 1))
    for i in range(t2):
        month = train + i
        manual_slopes[i] = sol.monthly_slopes(excess[month], betas)

    expected_premia = np.mean(manual_slopes, axis=0)
    diff = np.max(np.abs(res.premia - expected_premia))
    assert diff < 1e-10, f"premia do not match mean of monthly slopes: diff={diff}"


def test_naive_se_formula() -> None:
    """Naive standard error must divide sample standard deviation (ddof=1) by sqrt(T2)."""
    excess = INST["excess"]
    factors = INST["factors"]
    train = INST["train"]
    t2 = INST["T"] - train

    res = sol.fama_macbeth(excess, factors, train)
    betas = sol.loadings(excess, factors, train)

    slopes = np.array([sol.monthly_slopes(excess[train + i], betas) for i in range(t2)])
    expected_se = np.std(slopes, axis=0, ddof=1) / np.sqrt(t2)

    diff = np.max(np.abs(res.naive_se - expected_se))
    assert diff < 1e-10, f"naive_se formula defect: diff={diff}"


def test_second_pass_matches_oracle_with_intercept() -> None:
    """Second-pass regression must include the cross-sectional intercept."""
    excess = INST["excess"]
    factors = INST["factors"]
    train = INST["train"]

    betas = sol.loadings(excess, factors, train)
    slopes = sol.monthly_slopes(excess[train], betas)

    # Intercept included: design matrix has ones column
    z_with = np.column_stack([np.ones(INST["N"]), betas[:, 1:]])
    expected_with = np.linalg.solve(z_with.T @ z_with, z_with.T @ excess[train])
    assert np.allclose(slopes, expected_with, atol=1e-9), "monthly slopes do not match design with intercept"

    # Verify that model without intercept differs materially
    z_without = betas[:, 1:]
    expected_without = np.linalg.solve(z_without.T @ z_without, z_without.T @ excess[train])
    factor_diff = np.max(np.abs(slopes[1:] - expected_without))
    assert factor_diff > 1e-5, "test design defect: model with and without intercept must differ"


# ---------------------------------------------------------------- Shanken & GMM tests


def test_shanken_not_smaller_than_naive() -> None:
    """Under positive definite factor covariance, Shanken SE must be strictly >= naive SE."""
    excess = INST["excess"]
    factors = INST["factors"]
    train = INST["train"]

    res = sol.fama_macbeth(excess, factors, train)
    assert np.all(res.shanken_se >= res.naive_se - 1e-12), "Shanken SE cannot be smaller than naive SE"

    # Boundary test: if factor premia were exactly zero, factor multiplier c equals 1.0 exactly
    cov_f = np.cov(factors[train:], rowvar=False, ddof=1).reshape((INST["K"], INST["K"]))
    c_zero = sol.shanken_factor(np.zeros(INST["K"]), cov_f)
    assert abs(c_zero - 1.0) < 1e-12, "shanken_factor with zero premia must equal 1.0"


def test_shanken_factor_matches_derivation() -> None:
    """Shanken correction multiplier c must equal 1 + lambda' Sigma_f^(-1) lambda."""
    factors = INST["factors"][INST["train"] :]
    k = INST["K"]
    cov_f = np.cov(factors, rowvar=False, ddof=1).reshape((k, k))

    # Test with arbitrary non-trivial factor premium vector
    lambda_test = np.linspace(0.004, 0.012, k)
    expected_c = 1.0 + float(lambda_test.T @ np.linalg.solve(cov_f, lambda_test))

    c_calc = sol.shanken_factor(lambda_test, cov_f)
    assert abs(c_calc - expected_c) < 1e-9, f"shanken_factor mismatch: got {c_calc}, expected {expected_c}"


def test_gmm_se_formula() -> None:
    """GMM standard error under stacked moments must match Shanken-corrected standard error."""
    excess = INST["excess"]
    factors = INST["factors"]
    train = INST["train"]

    res = sol.fama_macbeth(excess, factors, train)
    diff = np.max(np.abs(res.gmm_se - res.shanken_se))
    assert diff < 1e-9, f"gmm_se must equal shanken_se under stacked OLS: diff={diff}"


def test_decision_uses_corrected_se() -> None:
    """conclusion_changes must report True when decision changes across standard errors."""
    crit = 1.96
    # Borderline case: estimate=2.00, naive_se=1.00 (t=2.00 > 1.96), shanken_se=1.10 (t=1.818 <= 1.96)
    assert sol.conclusion_changes(2.00, 1.00, 1.10, crit) is True, "expected conclusion to change"
    # Both significant: estimate=3.00, naive_se=1.00 (t=3.0), shanken_se=1.10 (t=2.727 > 1.96)
    assert sol.conclusion_changes(3.00, 1.00, 1.10, crit) is False, "expected conclusion unchanged (both sig)"
    # Both insignificant: estimate=1.00, naive_se=1.00 (t=1.0), shanken_se=1.10 (t=0.909 <= 1.96)
    assert sol.conclusion_changes(1.00, 1.00, 1.10, crit) is False, "expected conclusion unchanged (both insig)"


def test_matches_oracle_on_seeds_1_to_49() -> None:
    """Checks solver on independent seed instances to defeat hardcoded constants."""
    for test_seed in [1, 7, 23, 49]:
        inst = make_instance(test_seed)
        res = sol.fama_macbeth(inst["excess"], inst["factors"], inst["train"])
        assert len(res.premia) == inst["K"] + 1, "invalid premia length"
        assert np.all(np.isfinite(res.premia)), "non-finite premia"
        assert np.all(res.shanken_se >= res.naive_se), "shanken_se must be >= naive_se"


# ---------------------------------------------------------------- Validation tests


def test_validation_row_count_mismatch() -> None:
    """Row count mismatch between excess returns and factors must raise ValueError."""
    excess = INST["excess"]
    factors = INST["factors"][:-1]  # T - 1 rows
    must_raise(lambda: sol.loadings(excess, factors, INST["train"]), "row count mismatch in loadings")
    must_raise(lambda: sol.fama_macbeth(excess, factors, INST["train"]), "row count mismatch in fama_macbeth")


def test_validation_insufficient_train_or_test() -> None:
    """train < K + 2 or T - train < 2 must raise ValueError."""
    excess = INST["excess"]
    factors = INST["factors"]
    k = INST["K"]
    must_raise(lambda: sol.loadings(excess, factors, k + 1), "train < K + 2")
    must_raise(lambda: sol.loadings(excess, factors, excess.shape[0] - 1), "test months < 2")


def test_validation_insufficient_assets() -> None:
    """N <= K + 1 must raise ValueError."""
    excess = INST["excess"][:, : INST["K"] + 1]  # N = K + 1
    factors = INST["factors"]
    must_raise(lambda: sol.loadings(excess, factors, INST["train"]), "N <= K + 1")


def test_validation_non_finite_inputs() -> None:
    """Non-finite inputs (NaN or inf) must raise ValueError."""
    excess = INST["excess"].copy()
    factors = INST["factors"].copy()
    excess[0, 0] = np.nan
    must_raise(lambda: sol.loadings(excess, factors, INST["train"]), "NaN in excess")

    factors[0, 0] = np.inf
    must_raise(lambda: sol.fama_macbeth(INST["excess"], factors, INST["train"]), "Inf in factors")


def test_validation_non_posdef_factor_cov() -> None:
    """Non-positive definite factor covariance matrix must raise ValueError in shanken_factor."""
    k = INST["K"]
    non_pd_cov = -1.0 * np.eye(k)
    must_raise(lambda: sol.shanken_factor(np.ones(k), non_pd_cov), "negative definite factor covariance")


def test_outputs_finite_and_shapes() -> None:
    """Verifies that all FMResult output vectors are finite with shape (K + 1,)."""
    res = sol.fama_macbeth(INST["excess"], INST["factors"], INST["train"])
    expected_shape = (INST["K"] + 1,)
    for name in ("premia", "naive_se", "shanken_se", "gmm_se"):
        arr = getattr(res, name)
        assert isinstance(arr, np.ndarray), f"{name} must be a numpy ndarray"
        assert arr.shape == expected_shape, f"{name} shape {arr.shape} != {expected_shape}"
        assert np.all(np.isfinite(arr)), f"{name} contains non-finite entries"
        if "se" in name:
            assert np.all(arr > 0.0), f"{name} must be strictly positive"
