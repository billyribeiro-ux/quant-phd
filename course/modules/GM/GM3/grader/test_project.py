"""Autograder test suite for GM3: Trading Monetary Policy.

Runs identically in native pytest and Pyodide:
    pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import math
import os
from typing import Any, cast

import numpy as np
import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]
from reference import (  # type: ignore[import-not-found, unused-ignore]
    compute_kuttner_surprises,
    estimate_drift_statistics,
    evaluate_drift_decay,
    placebo_permutation_test,
    regress_equity_response,
)

pytestmark = pytest.mark.filterwarnings("error")


def _get_instance() -> dict[str, Any]:
    """Retrieve test instance seeded by environment SEED or fallback to 0."""
    seed_env = os.environ.get("SEED", "0")
    try:
        seed = int(seed_env)
    except ValueError:
        seed = 0
    return cast(dict[str, Any], make_instance(seed))


def test_kuttner_scaling_invariants() -> None:
    """Property 1: Kuttner futures scaling factor must be >= 1.0, and zero jump yields zero surprise."""
    inst = _get_instance()
    pre = inst["pre_rates"]
    post = inst["post_rates"]
    m = inst["days_in_month"]
    d = inst["announcement_days"]

    surprises = compute_kuttner_surprises(pre, post, m, d)
    assert len(surprises) == len(pre), "Output array length must equal input length"
    assert np.all(np.isfinite(surprises)), "Surprises must be finite real numbers"

    # Zero jump test
    zeros = compute_kuttner_surprises(pre, pre, m, d)
    np.testing.assert_allclose(zeros, 0.0, atol=1e-10, err_msg="Zero futures jump must yield zero surprise")

    # Positive jump should yield surprise strictly larger in absolute magnitude than unscaled jump
    unscaled_jumps_bps = (post - pre) * 100.0
    for i in range(len(pre)):
        if d[i] < m[i] - 1 and abs(unscaled_jumps_bps[i]) > 1e-4:
            scale_expected = m[i] / (m[i] - d[i])
            assert scale_expected > 1.0, "Scale factor must exceed 1 for d >= 1"
            assert abs(surprises[i]) > abs(unscaled_jumps_bps[i]), "Scaled surprise magnitude must exceed raw jump"


def test_kuttner_boundary_adjustment() -> None:
    """Property 2: Month-end boundary condition d >= M - 1 must not diverge or divide by zero."""
    m_test = np.array([30, 30, 31, 31])
    d_test = np.array([29, 30, 30, 31])  # d >= M - 1
    pre = np.array([4.0, 4.0, 4.0, 4.0])
    post = np.array([4.10, 4.10, 4.10, 4.10])  # +10 bps jump

    surprises = compute_kuttner_surprises(pre, post, m_test, d_test)
    assert np.all(np.isfinite(surprises)), "Boundary cases must not produce NaN or Inf"
    # Unscaled jump is 10.0 bps
    np.testing.assert_allclose(surprises, 10.0, atol=1e-6, err_msg="Boundary cases must default to unscaled jump")


def test_equity_regression_properties() -> None:
    """Property 3: Equity sensitivity to monetary surprises must be negative and R^2 in [0, 1]."""
    inst = _get_instance()
    pre = inst["pre_rates"]
    post = inst["post_rates"]
    m = inst["days_in_month"]
    d = inst["announcement_days"]
    events = inst["event_indices"]
    returns = inst["daily_returns"]

    surprises = compute_kuttner_surprises(pre, post, m, d)
    event_returns_bps = returns[events] * 10000.0

    reg = regress_equity_response(surprises, event_returns_bps)
    assert "alpha_bps" in reg
    assert "beta" in reg
    assert "r_squared" in reg
    assert "t_stat_beta" in reg

    assert reg["beta"] < 0.0, f"Monetary surprise beta should be negative (found {reg['beta']})"
    assert 0.0 <= reg["r_squared"] <= 1.0, f"R^2 must be in [0, 1] (found {reg['r_squared']})"


def test_drift_statistics_properties() -> None:
    """Property 4: Analytical identities for t-statistic, Sharpe ratio, and win rate."""
    sample_returns = np.array([35.0, 45.0, -10.0, 60.0, 50.0, 20.0, 40.0, -5.0])
    stats = estimate_drift_statistics(sample_returns)

    n = len(sample_returns)
    mu = float(np.mean(sample_returns))
    sigma = float(np.std(sample_returns, ddof=1))
    expected_t = mu / (sigma / math.sqrt(n))
    expected_sharpe = mu / sigma * math.sqrt(8.0)
    expected_win_rate = float(np.mean(sample_returns > 0))

    assert math.isclose(stats["mean_bps"], mu, rel_tol=1e-5)
    assert math.isclose(stats["std_bps"], sigma, rel_tol=1e-5)
    assert math.isclose(stats["t_stat"], expected_t, rel_tol=1e-5)
    assert math.isclose(stats["annualized_sharpe"], expected_sharpe, rel_tol=1e-5)
    assert math.isclose(stats["win_rate"], expected_win_rate, rel_tol=1e-5)
    assert 0.0 <= stats["p_value"] <= 1.0


def test_placebo_permutation_null() -> None:
    """Property 5: Placebo distribution must exclude actual event days and center near zero."""
    inst = _get_instance()
    returns = inst["daily_returns"]
    events = inst["in_sample_events"]

    p_val, placebos = placebo_permutation_test(returns, events, n_sims=500, seed=123)
    assert len(placebos) == 500
    assert 0.0 <= p_val <= 1.0
    # Mean of placebos across large number of random draws from zero-mean background returns should be close to zero
    assert abs(float(np.mean(placebos))) < 10.0, "Placebo null distribution must be approximately centered around zero"
    assert p_val < 0.05, f"Actual in-sample drift (~49 bps) must reject placebo null at 5% level (got p={p_val})"


def test_out_of_sample_decay_invariants() -> None:
    """Property 6: Out-of-sample decay Welch t-test must reflect degradation from in-sample drift."""
    inst = _get_instance()
    returns = inst["daily_returns"]
    is_events = inst["in_sample_events"]
    oos_events = inst["out_of_sample_events"]

    is_drift = returns[is_events - 1] * 10000.0
    oos_drift = returns[oos_events - 1] * 10000.0

    eval_decay = evaluate_drift_decay(is_drift, oos_drift)
    assert "decay_ratio" in eval_decay
    assert "welch_t_stat" in eval_decay
    assert "survived" in eval_decay

    # The drift strongly decays out-of-sample in synthetic instance
    assert eval_decay["in_sample_mean_bps"] > eval_decay["out_of_sample_mean_bps"], (
        "In-sample drift must exceed OOS drift"
    )
    assert eval_decay["decay_ratio"] < 0.5, "Decay ratio must indicate substantial reduction post-2011"
    assert eval_decay["welch_t_stat"] < 0.0, "Welch t-stat for (OOS - IS) must be negative"


def test_input_validation_and_failures() -> None:
    """Property 7: Input validation. Length mismatches and empty inputs must raise ValueError."""
    with pytest.raises(ValueError):
        compute_kuttner_surprises(np.array([]), np.array([]), np.array([]), np.array([]))

    with pytest.raises(ValueError):
        compute_kuttner_surprises(np.array([4.0]), np.array([4.1, 4.2]), np.array([30]), np.array([15]))

    with pytest.raises(ValueError):
        regress_equity_response(np.array([1.0]), np.array([2.0]))

    with pytest.raises(ValueError):
        estimate_drift_statistics(np.array([10.0]))

    with pytest.raises(ValueError):
        evaluate_drift_decay(np.array([10.0]), np.array([5.0]))
