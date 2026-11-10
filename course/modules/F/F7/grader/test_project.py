"""Pytest autograder suite for F7: Manager Due-Diligence Tool.

Validates student solution against econometric invariants, finite-sample properties,
HAC orthogonality, Lo (2002) serial correlation corrections, GLM unsmoothing bounds,
and honest manager ranking.
"""

from __future__ import annotations

import os
from typing import Any

# Import student solution (in Pyodide/workspace, named due_diligence.py)
try:
    import due_diligence as student
except ImportError:
    import reference as student

import numpy as np
import pytest
from instance import make_instance
from integrity import validate_due_diligence_instance, validate_evaluation_output


@pytest.fixture(scope="module")
def dataset() -> dict[str, Any]:
    """Load deterministic instance derived from environment seed."""
    seed_str = os.environ.get("QF_SEED", "0")
    try:
        seed = int(seed_str)
    except ValueError:
        seed = 0
    inst: dict[str, Any] = make_instance(seed)
    validate_due_diligence_instance(inst)
    return inst


def test_instance_structure_and_integrity(dataset: dict[str, Any]) -> None:
    """Verify instance contains valid factors, market return, and manager returns."""
    assert dataset["n_months"] == 180
    assert len(dataset["factor_names"]) == 4
    assert len(dataset["manager_names"]) == 5
    factors = np.asarray(dataset["factors"])
    returns = np.asarray(dataset["manager_returns"])
    assert factors.shape == (180, 4)
    assert returns.shape == (180, 5)


def test_factor_alpha_hac_properties(dataset: dict[str, Any]) -> None:
    """Verify OLS orthogonality, valid HAC standard error, and R-squared bounds."""
    factors = np.asarray(dataset["factors"], dtype=np.float64)
    r_mgr = np.asarray(dataset["manager_returns"], dtype=np.float64)[:, 0]

    res = student.compute_factor_alpha(r_mgr, factors, bandwidth=4)
    assert "alpha_ann" in res
    assert "se_alpha_hac" in res
    assert "t_stat_hac" in res
    assert "r_squared" in res

    assert res["se_alpha_hac"] > 0.0
    assert 0.0 <= res["r_squared"] <= 1.0
    expected_t = res["alpha_monthly"] / res["se_alpha_hac"]
    assert np.isclose(res["t_stat_hac"], expected_t, atol=1e-5)
    assert np.isclose(res["alpha_ann"], res["alpha_monthly"] * 12.0, atol=1e-6)


def test_lo_autocorrelation_adjusted_sharpe(dataset: dict[str, Any]) -> None:
    """Verify Lo (2002) time aggregation factor eta(q) and adjusted Sharpe ratio."""
    r_mgr = np.asarray(dataset["manager_returns"], dtype=np.float64)[:, 1]  # Harbor (smoothed)

    res = student.compute_autocorrelation_adjusted_sharpe(r_mgr, q_horizon=12)
    assert "sr_naive_ann" in res
    assert "rho_1" in res
    assert "eta_q" in res
    assert "sr_adjusted_ann" in res

    assert -1.0 <= res["rho_1"] <= 1.0
    assert 0.40 <= res["eta_q"] <= 0.92
    assert res["rho_1"] > 0.25  # Harbor has strong positive serial persistence
    # Check that adjusted Sharpe equals eta_q * sr_naive_ann
    assert np.isclose(res["sr_adjusted_ann"], res["eta_q"] * res["sr_naive_ann"], atol=1e-5)


def test_glm_return_unsmoothing_invariants(dataset: dict[str, Any]) -> None:
    """Verify GLM (2004) parameter constraints, concentration index xi, and volatility recovery."""
    r_mgr = np.asarray(dataset["manager_returns"], dtype=np.float64)[:, 1]  # Harbor (smoothed)

    res = student.unsmooth_returns_glm(r_mgr)
    assert "theta_0" in res and "theta_1" in res and "theta_2" in res
    assert "xi" in res
    assert "vol_unsmoothed_ann" in res
    assert "sr_unsmoothed_ann" in res

    # Weights sum to 1.0 and are non-negative
    sum_theta = res["theta_0"] + res["theta_1"] + res["theta_2"]
    assert np.isclose(sum_theta, 1.0, atol=1e-2)
    assert res["theta_0"] >= -1e-5
    assert res["theta_1"] >= -1e-5
    assert res["theta_2"] >= -1e-5

    # xi = sum theta_j^2 is between 1/3 and 1.0
    assert 0.30 <= res["xi"] <= 1.01

    # Unsmoothed volatility should be greater than or equal to reported volatility
    assert res["vol_unsmoothed_ann"] >= res["vol_reported_ann"] * 0.95


def test_nonlinear_payoff_detection(dataset: dict[str, Any]) -> None:
    """Verify Treynor-Mazuy quadratic payoff detection identifies concave vs convex managers."""
    mkt = np.asarray(dataset["mkt_excess"], dtype=np.float64)
    returns = np.asarray(dataset["manager_returns"], dtype=np.float64)

    # Manager 2 is Apex VolCarry (short put -> concave)
    res_apex = student.detect_nonlinear_exposure(returns[:, 2], mkt)
    assert "gamma" in res_apex
    assert "t_gamma" in res_apex
    assert res_apex["gamma"] < 0.0
    assert res_apex["t_gamma"] < -2.0

    # Manager 3 is Beacon TrendCTA (trend following -> convex)
    res_beacon = student.detect_nonlinear_exposure(returns[:, 3], mkt)
    assert res_beacon["gamma"] > 0.0
    assert res_beacon["t_gamma"] > 2.0


def test_manager_universe_evaluation_and_ranking(dataset: dict[str, Any]) -> None:
    """Verify full evaluation pipeline, honest ranking, and penalty enforcement."""
    output = student.evaluate_manager_universe(dataset)
    validate_evaluation_output(output, n_expected=5)

    names_in_order = [str(x["name"]) for x in output]
    # Apex VolCarry must be ranked last due to severe short-volatility concavity penalty
    assert names_in_order[-1] == "Apex_VolCarry"

    # Beacon TrendCTA or AlphaStar Equity must be ranked first or second
    top_two = set(names_in_order[:2])
    assert "Beacon_TrendCTA" in top_two or "AlphaStar_Equity" in top_two
