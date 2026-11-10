"""Pytest suite for CAP3: Qualifying Examination Capstone Grader.

Verifies doctoral qualifying examination solvers across the three field prelims:
1. Field Prelim I: Asset Pricing & Continuous-Time Valuation
2. Field Prelim II: Cross-Sectional & Time-Series Econometrics
3. Field Prelim III: Dynamic General Equilibrium & Monetary Macro

Tests verify theoretical properties, comparative statics, econometric corrections,
and boundary conditions against deterministic seed instances.
"""

from __future__ import annotations

import copy
import os
from typing import Any

import numpy as np
import pytest
import reference as solution
from instance import make_instance

SEED = int(os.environ.get("QF_SEED", "0"))


@pytest.fixture
def exam_instance() -> dict[str, Any]:
    """Provide a reproducible exam instance for property and invariant checks."""
    return make_instance(seed=SEED)


def test_asset_pricing_prelim_properties(exam_instance: dict[str, Any]) -> None:
    """Verify Hansen-Jagannathan SDF bounds and Merton continuous-time portfolio properties."""
    sol = solution.solve_asset_pricing_prelim(exam_instance)
    ap = exam_instance.get("asset_pricing", exam_instance)

    # 1. Sharpe ratio must be strictly positive
    sr = sol["tangency_sharpe"]
    assert sr > 0.0, f"Tangency Sharpe ratio must be positive, got {sr}"

    # 2. Hansen-Jagannathan SDF volatility lower bound
    rf = float(ap["rf"])
    mean_sdf = 1.0 / (1.0 + rf)
    hj_bound = sol["hj_volatility_bound"]
    assert hj_bound > 0.0, f"HJ volatility bound must be positive, got {hj_bound}"
    assert hj_bound == pytest.approx(mean_sdf * sr, rel=1e-5), "HJ bound must equal E[m] * SR_tangency"

    # 3. Merton portfolio fraction
    merton_w = sol["merton_fraction"]
    assert merton_w > 0.0, f"Merton stock fraction must be positive for positive equity premium, got {merton_w}"

    # 4. Optimal consumption ratio
    c_ratio = sol["optimal_consumption_ratio"]
    assert c_ratio > 0.0, f"Optimal consumption ratio must be strictly positive, got {c_ratio}"


def test_hansen_jagannathan_bound_centering(exam_instance: dict[str, Any]) -> None:
    """Test that the Hansen-Jagannathan bound computes centered variance rather than uncentered second moments."""
    sol = solution.solve_asset_pricing_prelim(exam_instance)
    ap = exam_instance.get("asset_pricing", exam_instance)
    mu = np.array(ap["mu"], dtype=np.float64)
    sigma = np.array(ap["sigma"], dtype=np.float64)
    rf = float(ap["rf"])

    # Theoretical Sharpe ratio from centered covariance
    expected_sr = float(np.sqrt(mu @ np.linalg.inv(sigma) @ mu))
    expected_bound = (1.0 / (1.0 + rf)) * expected_sr
    assert sol["hj_volatility_bound"] == pytest.approx(expected_bound, rel=1e-6), (
        "HJ volatility bound does not match centered covariance matrix formulation"
    )


def test_merton_risk_aversion_scaling(exam_instance: dict[str, Any]) -> None:
    """Verify that the Merton fraction scales strictly linearly with 1/gamma."""
    sol = solution.solve_asset_pricing_prelim(exam_instance)
    ap = exam_instance.get("asset_pricing", exam_instance)

    # Double risk aversion
    modified_instance: dict[str, Any] = copy.deepcopy(exam_instance)
    modified_instance["gamma"] = float(ap["gamma"]) * 2.0
    if "asset_pricing" in modified_instance:
        modified_instance["asset_pricing"]["gamma"] = modified_instance["gamma"]

    sol_doubled = solution.solve_asset_pricing_prelim(modified_instance)
    ratio = sol["merton_fraction"] / sol_doubled["merton_fraction"]
    assert ratio == pytest.approx(2.0, rel=1e-5), (
        f"Merton fraction must scale as 1/gamma; expected ratio 2.0, got {ratio}"
    )


def test_econometrics_prelim_properties(exam_instance: dict[str, Any]) -> None:
    """Verify Fama-MacBeth, Shanken standard errors, GRS, and GMM Hansen J-test."""
    sol = solution.solve_econometrics_prelim(exam_instance)

    # 1. Fama-MacBeth risk premia and Shanken SEs
    lambdas = sol["risk_premia"]
    shanken_se = sol["shanken_se"]
    assert len(lambdas) == 2, f"Expected 2 factor risk premia, got {len(lambdas)}"
    assert len(shanken_se) == 2, f"Expected 2 Shanken standard errors, got {len(shanken_se)}"
    for se in shanken_se:
        assert se > 0.0, f"Shanken standard error must be strictly positive, got {se}"

    # 2. GRS test statistic
    grs = sol["grs_stat"]
    assert grs > 0.0, f"GRS F-statistic must be strictly positive, got {grs}"

    # 3. GMM Hansen J-test
    j_stat = sol["hansen_j_stat"]
    p_val = sol["j_pvalue"]
    assert j_stat >= 0.0, f"Hansen J-statistic must be non-negative, got {j_stat}"
    assert 0.0 <= p_val <= 1.0, f"Hansen J-test p-value must lie in [0, 1], got {p_val}"


def test_shanken_standard_error_correction_invariant(exam_instance: dict[str, Any]) -> None:
    """Verify that Shanken correction accounts for the quadratic factor risk premium term."""
    sol = solution.solve_econometrics_prelim(exam_instance)
    ec = exam_instance.get("econometrics", exam_instance)
    factors = np.array(ec["factors"], dtype=np.float64)
    t_obs = int(ec["t_obs"])

    # Compute raw factor covariance
    f_centered = factors - np.mean(factors, axis=0)
    sigma_f = (f_centered.T @ f_centered) / float(t_obs)
    pure_factor_se = np.sqrt(np.diag(sigma_f / float(t_obs)))

    # Shanken standard error must strictly exceed pure factor variation due to estimation error in betas
    shanken_se = np.array(sol["shanken_se"], dtype=np.float64)
    for i in range(len(shanken_se)):
        assert shanken_se[i] > pure_factor_se[i], (
            f"Shanken standard error ({shanken_se[i]}) must exceed pure factor SE ({pure_factor_se[i]})"
        )


def test_grs_curvature_denominator(exam_instance: dict[str, Any]) -> None:
    """Verify that GRS test incorporates factor curvature normalization in the denominator."""
    sol = solution.solve_econometrics_prelim(exam_instance)
    ec = exam_instance.get("econometrics", exam_instance)
    factors = np.array(ec["factors"], dtype=np.float64)
    returns = np.array(ec["returns"], dtype=np.float64)
    t_obs, n_assets = returns.shape
    _, n_factors = factors.shape

    f_mean = np.mean(factors, axis=0)
    factors_centered = factors - f_mean
    sigma_f = (factors_centered.T @ factors_centered) / float(t_obs)
    sigma_f_inv = np.linalg.inv(sigma_f)
    curvature = float(1.0 + f_mean @ sigma_f_inv @ f_mean)

    # Curvature must be strictly greater than 1 when mean factors are non-zero
    assert curvature > 1.0, f"Factor curvature must strictly exceed 1.0, got {curvature}"

    # Calculate exact expected GRS with curvature
    x_ts = np.column_stack([np.ones(t_obs), factors])
    x_ts_inv = np.linalg.inv(x_ts.T @ x_ts)
    alphas = np.zeros(n_assets)
    residuals = np.zeros((t_obs, n_assets))
    for i in range(n_assets):
        y = returns[:, i]
        coeff = x_ts_inv @ (x_ts.T @ y)
        alphas[i] = coeff[0]
        residuals[:, i] = y - x_ts @ coeff
    sigma_eps = (residuals.T @ residuals) / float(t_obs)
    alpha_quad = float(alphas @ np.linalg.inv(sigma_eps) @ alphas)
    expected_grs = (float(t_obs - n_assets - n_factors) / float(n_assets)) * (alpha_quad / curvature)

    assert sol["grs_stat"] == pytest.approx(expected_grs, rel=1e-5), (
        f"GRS statistic must incorporate factor curvature denominator {curvature}"
    )


def test_macro_prelim_properties(exam_instance: dict[str, Any]) -> None:
    """Verify Kuttner surprise scaling, New Keynesian determinacy, and local projections."""
    sol = solution.solve_macro_prelim(exam_instance)
    mc = exam_instance.get("macro", exam_instance)

    # 1. Kuttner surprise scaling invariant
    raw_jump = float(mc["futures_price_change"])
    surprise = sol["kuttner_surprise"]
    assert abs(surprise) >= abs(raw_jump), (
        f"Kuttner surprise magnitude ({abs(surprise)}) must exceed raw jump ({abs(raw_jump)})"
    )

    # 2. Taylor determinacy
    taylor_metric = sol["taylor_metric"]
    is_determinate = sol["is_determinate"]
    assert is_determinate == (taylor_metric > 1.0), (
        f"Determinacy flag ({is_determinate}) does not match Taylor criterion ({taylor_metric} > 1.0)"
    )

    # 3. Local projections impulse responses
    irf = sol["lp_impulse_responses"]
    max_h = int(mc["max_horizon"])
    assert len(irf) == max_h + 1, f"Expected {max_h + 1} impulse response horizons, got {len(irf)}"


def test_kuttner_scaling_invariants(exam_instance: dict[str, Any]) -> None:
    """Verify the exact Kuttner futures scaling factor M / (M - d)."""
    sol = solution.solve_macro_prelim(exam_instance)
    mc = exam_instance.get("macro", exam_instance)
    raw_jump = float(mc["futures_price_change"])
    day = int(mc["announcement_day"])
    days_in_month = int(mc["days_in_month"])

    expected_scale = float(days_in_month) / float(days_in_month - day)
    expected_surprise = expected_scale * raw_jump

    assert sol["kuttner_surprise"] == pytest.approx(expected_surprise, rel=1e-6), (
        f"Kuttner surprise {sol['kuttner_surprise']} does not match scaled target {expected_surprise}"
    )


def test_taylor_principle_boundary_case() -> None:
    """Verify New Keynesian determinacy right at the boundary condition."""
    instance: dict[str, Any] = {
        "futures_price_change": -0.01,
        "announcement_day": 15,
        "days_in_month": 30,
        "beta_discount": 0.99,
        "sigma_crra": 1.0,
        "kappa_slope": 0.10,
        "phi_pi": 0.90,
        "phi_y": 1.00,  # 0.90 + ((1 - 0.99)/0.10)*1.00 = 0.90 + 0.10 = 1.00 (indeterminate)
        "shocks": np.array([0.1, -0.2, 0.3, 0.0, -0.1] * 16),
        "outcomes": np.array([0.0, -0.1, 0.2, -0.1, 0.0] * 16),
        "max_horizon": 4,
    }
    sol = solution.solve_macro_prelim(instance)
    assert sol["taylor_metric"] == pytest.approx(1.00, rel=1e-6)
    assert sol["is_determinate"] is False, "Boundary metric == 1.00 must be evaluated as indeterminate (needs > 1.00)"
