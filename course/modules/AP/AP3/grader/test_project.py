"""Autograder test suite for AP3 project: Euler-Equation GMM & Hansen-Jagannathan Engine.

Tests ccapm_engine.py against mathematical invariants, oracle values,
finite-difference gradients, Hansen J-test distributions, and input validation.
"""

from __future__ import annotations

import os
from typing import Any, cast

import numpy as np
import pytest
from ccapm_engine import (
    estimate_gmm,
    euler_residuals,
    evaluate_consumption_sdf,
    gmm_gradient,
    gmm_objective,
    hansen_jagannathan_bound,
    sample_moments,
    spectral_covariance,
)
from instance import make_instance


def _get_instance() -> dict[str, Any]:
    seed = int(os.environ.get("QF_SEED", "0"))
    return cast(dict[str, Any], make_instance(seed))


def test_euler_residuals_shape_and_values() -> None:
    """Check residual dimensions, exact algebraic formula, and pricing error logic."""
    inst = _get_instance()
    c_growth = cast(np.ndarray, inst["c_growth"])
    gross_returns = cast(np.ndarray, inst["gross_returns"])
    t_periods, n_assets = gross_returns.shape

    params = (0.98, 2.0)
    u = euler_residuals(params, c_growth, gross_returns)

    assert u.shape == (t_periods, n_assets), f"Expected shape ({t_periods}, {n_assets}), got {u.shape}"
    assert np.all(np.isfinite(u)), "Residuals must be finite"

    # Exact manual check for first observation
    beta, gamma = params
    expected_u00 = beta * (c_growth[0] ** (-gamma)) * gross_returns[0, 0] - 1.0
    assert np.isclose(u[0, 0], expected_u00, atol=1e-12), "Euler residual calculation does not match formula"

    # Test inverse monotonicity in gamma when c_growth > 1
    u_high_gamma = euler_residuals((beta, gamma + 1.0), np.array([1.05]), np.array([[1.05]]))
    u_low_gamma = euler_residuals((beta, gamma), np.array([1.05]), np.array([[1.05]]))
    assert u_high_gamma[0, 0] < u_low_gamma[0, 0], "Higher gamma should lower SDF and residual when c > 1"


def test_sample_moments_orthogonality() -> None:
    """Check Kronecker product alignment between residuals and instrument vector."""
    inst = _get_instance()
    c_growth = cast(np.ndarray, inst["c_growth"])
    gross_returns = cast(np.ndarray, inst["gross_returns"])
    instruments = cast(np.ndarray, inst["instruments"])
    n_assets = gross_returns.shape[1]
    l_instruments = instruments.shape[1]
    k_moments = n_assets * l_instruments

    params = (0.97, 2.2)
    g = sample_moments(params, c_growth, gross_returns, instruments)

    assert g.shape == (k_moments,), f"Expected moments length {k_moments}, got {len(g)}"

    u = euler_residuals(params, c_growth, gross_returns)
    for i in range(n_assets):
        for j in range(l_instruments):
            idx = i * l_instruments + j
            manual_moment = float(np.mean(u[:, i] * instruments[:, j]))
            assert np.isclose(g[idx], manual_moment, atol=1e-12), (
                f"Moment {idx} does not match manual Kronecker mean of u[:, {i}] * z[:, {j}]"
            )


def test_gmm_objective_properties() -> None:
    """Verify quadratic form non-negativity and scaling invariance."""
    inst = _get_instance()
    c_growth = cast(np.ndarray, inst["c_growth"])
    gross_returns = cast(np.ndarray, inst["gross_returns"])
    instruments = cast(np.ndarray, inst["instruments"])
    k_moments = gross_returns.shape[1] * instruments.shape[1]

    weight = np.eye(k_moments, dtype=np.float64)
    params = (0.98, 2.0)
    obj = gmm_objective(params, c_growth, gross_returns, instruments, weight)

    assert isinstance(obj, float), "GMM objective must be a float scalar"
    assert obj >= 0.0, "Quadratic GMM objective must be non-negative"

    # Scale weight matrix by factor of 3.5 -> objective scales exactly by 3.5
    obj_scaled = gmm_objective(params, c_growth, gross_returns, instruments, 3.5 * weight)
    assert np.isclose(obj_scaled, 3.5 * obj, rtol=1e-10), "GMM objective must scale linearly with weight matrix"


def test_gmm_gradient_accuracy() -> None:
    """Compare analytical gradient to central finite differences."""
    inst = _get_instance()
    c_growth = cast(np.ndarray, inst["c_growth"])
    gross_returns = cast(np.ndarray, inst["gross_returns"])
    instruments = cast(np.ndarray, inst["instruments"])
    k_moments = gross_returns.shape[1] * instruments.shape[1]
    weight = np.eye(k_moments, dtype=np.float64)

    beta_pt, gamma_pt = 0.97, 2.1
    analytical_grad = gmm_gradient((beta_pt, gamma_pt), c_growth, gross_returns, instruments, weight)

    assert analytical_grad.shape == (2,), f"Gradient must have shape (2,), got {analytical_grad.shape}"

    # Numerical gradient via central differences
    eps = 1e-6
    obj_plus_b = gmm_objective((beta_pt + eps, gamma_pt), c_growth, gross_returns, instruments, weight)
    obj_minus_b = gmm_objective((beta_pt - eps, gamma_pt), c_growth, gross_returns, instruments, weight)
    num_grad_beta = (obj_plus_b - obj_minus_b) / (2.0 * eps)

    obj_plus_g = gmm_objective((beta_pt, gamma_pt + eps), c_growth, gross_returns, instruments, weight)
    obj_minus_g = gmm_objective((beta_pt, gamma_pt - eps), c_growth, gross_returns, instruments, weight)
    num_grad_gamma = (obj_plus_g - obj_minus_g) / (2.0 * eps)

    assert np.isclose(analytical_grad[0], num_grad_beta, rtol=1e-4, atol=1e-5), (
        f"Analytical dJ/dbeta ({analytical_grad[0]:.6f}) diverges from numerical ({num_grad_beta:.6f})"
    )
    assert np.isclose(analytical_grad[1], num_grad_gamma, rtol=1e-4, atol=1e-5), (
        f"Analytical dJ/dgamma ({analytical_grad[1]:.6f}) diverges from numerical ({num_grad_gamma:.6f})"
    )


def test_spectral_covariance_properties() -> None:
    """Ensure spectral density matrix S_T is symmetric positive semi-definite."""
    inst = _get_instance()
    c_growth = cast(np.ndarray, inst["c_growth"])
    gross_returns = cast(np.ndarray, inst["gross_returns"])
    instruments = cast(np.ndarray, inst["instruments"])
    t_periods = gross_returns.shape[0]
    k_moments = gross_returns.shape[1] * instruments.shape[1]

    u = euler_residuals((0.98, 2.0), c_growth, gross_returns)
    h = np.empty((t_periods, k_moments), dtype=np.float64)
    l_instruments = instruments.shape[1]
    for i in range(gross_returns.shape[1]):
        for j in range(l_instruments):
            h[:, i * l_instruments + j] = u[:, i] * instruments[:, j]

    s_matrix = spectral_covariance(h)

    assert s_matrix.shape == (k_moments, k_moments)
    assert np.allclose(s_matrix, s_matrix.T, atol=1e-12), "Spectral covariance matrix must be symmetric"

    eigvals = np.linalg.eigvalsh(s_matrix)
    assert np.all(eigvals >= -1e-10), "Spectral covariance matrix must be positive semi-definite"


def test_estimate_gmm_two_step() -> None:
    """Verify full Hansen-Singleton estimation, J-test statistic, degrees of freedom, and standard errors."""
    inst = _get_instance()
    c_growth = cast(np.ndarray, inst["c_growth"])
    gross_returns = cast(np.ndarray, inst["gross_returns"])
    instruments = cast(np.ndarray, inst["instruments"])
    k_moments = gross_returns.shape[1] * instruments.shape[1]
    expected_df = k_moments - 2

    res = estimate_gmm(c_growth, gross_returns, instruments, initial_params=(0.95, 2.0), two_step=True)

    for field in ("beta", "gamma", "j_stat", "j_pvalue", "df", "standard_errors", "step1_params"):
        assert field in res, f"estimate_gmm result missing key: {field}"

    beta_hat = res["beta"]
    gamma_hat = res["gamma"]
    assert 0.60 < beta_hat < 1.40, f"Estimated discount factor {beta_hat:.4f} is economically implausible"
    assert -10.0 < gamma_hat < 20.0, f"Estimated risk aversion {gamma_hat:.4f} is outside reasonable bounds"

    assert res["df"] == expected_df, f"Expected J-test degrees of freedom {expected_df}, got {res['df']}"
    assert res["j_stat"] >= 0.0, "Hansen J-statistic must be non-negative"
    assert 0.0 <= res["j_pvalue"] <= 1.0, "J-test p-value must lie in [0, 1]"

    se_b, se_g = res["standard_errors"]
    assert se_b > 0.0 and np.isfinite(se_b), "Standard error for beta must be positive and finite"
    assert se_g > 0.0 and np.isfinite(se_g), "Standard error for gamma must be positive and finite"

    # Two-step estimates must update step 1 estimates via optimal weighting matrix
    step1_b, step1_g = res["step1_params"]
    assert not (np.isclose(step1_b, beta_hat, atol=1e-5) and np.isclose(step1_g, gamma_hat, atol=1e-5)), (
        "Two-step GMM estimates must update step-1 estimates via optimal weighting matrix"
    )

    # J-statistic must equal quadratic form weighted by inverted spectral covariance matrix S_T(theta_1)^-1
    u_step1 = euler_residuals(res["step1_params"], c_growth, gross_returns)
    h_step1 = np.empty((gross_returns.shape[0], k_moments), dtype=np.float64)
    l_inst = instruments.shape[1]
    for i in range(gross_returns.shape[1]):
        for j in range(l_inst):
            h_step1[:, i * l_inst + j] = u_step1[:, i] * instruments[:, j]
    s_step1 = spectral_covariance(h_step1)
    g_hat = sample_moments((beta_hat, gamma_hat), c_growth, gross_returns, instruments)
    expected_j = float(gross_returns.shape[0] * (g_hat.T @ np.linalg.pinv(s_step1) @ g_hat))
    assert np.isclose(res["j_stat"], expected_j, rtol=1e-2), (
        f"J-statistic {res['j_stat']:.4f} must be weighted by S_T(theta_1)^-1 (expected {expected_j:.4f})"
    )


def test_hansen_jagannathan_bound_convexity() -> None:
    """Verify HJ bound non-negativity and parabolic convexity across target means."""
    inst = _get_instance()
    gross_returns = cast(np.ndarray, inst["gross_returns"])
    nu_grid = cast(np.ndarray, inst["nu_grid"])

    bounds = hansen_jagannathan_bound(gross_returns, nu_grid)

    assert len(bounds) == len(nu_grid), "HJ bound length must match nu_grid"
    assert np.all(bounds >= 0.0), "Hansen-Jagannathan volatility lower bound must be non-negative"

    # HJ bound sigma(M*(nu)) is strictly convex: second difference of variance is positive
    vars_bound = bounds**2
    second_diffs = np.diff(vars_bound, n=2)
    assert np.all(second_diffs > 0.0), "Hansen-Jagannathan variance frontier must be strictly convex"

    # Must match centered covariance formula rather than uncentered moments
    mu_r = np.mean(gross_returns, axis=0)
    cov_r = np.cov(gross_returns, rowvar=False)
    target_nu = float(nu_grid[0])
    diff_target = np.ones(gross_returns.shape[1]) - target_nu * mu_r
    expected_vol = float(np.sqrt(diff_target.T @ np.linalg.pinv(cov_r) @ diff_target))
    assert np.isclose(bounds[0], expected_vol, rtol=1e-5), "HJ bound must use centered covariance matrix"


def test_evaluate_consumption_sdf() -> None:
    """Verify consumption SDF expectation and standard deviation."""
    inst = _get_instance()
    c_growth = cast(np.ndarray, inst["c_growth"])

    mean_m, std_m = evaluate_consumption_sdf(0.98, 2.0, c_growth)
    assert mean_m > 0.0 and np.isfinite(mean_m)
    assert std_m > 0.0 and np.isfinite(std_m)

    # Constant consumption growth gives zero volatility
    mean_const, std_const = evaluate_consumption_sdf(0.98, 2.0, np.ones(100))
    assert np.isclose(mean_const, 0.98, atol=1e-12)
    assert np.isclose(std_const, 0.0, atol=1e-12)


def test_invalid_inputs_raise_value_error() -> None:
    """Check robust input validation and clean exceptions."""
    c_good = np.array([1.01, 1.02, 0.99])
    r_good = np.array([[1.02, 1.05], [1.01, 1.04], [1.03, 1.02]])
    z_good = np.ones((3, 2))

    # Mismatched length
    with pytest.raises(ValueError, match=r"Length mismatch"):
        euler_residuals((0.98, 2.0), np.array([1.01, 1.02]), r_good)

    # Negative consumption growth
    with pytest.raises(ValueError, match=r"strictly positive"):
        euler_residuals((0.98, 2.0), np.array([1.01, -0.5, 1.02]), r_good)

    # Negative gross returns
    with pytest.raises(ValueError, match=r"strictly positive"):
        euler_residuals((0.98, 2.0), c_good, np.array([[1.02, -1.0], [1.01, 1.04], [1.03, 1.02]]))

    # NaN in inputs
    with pytest.raises(ValueError, match=r"finite"):
        euler_residuals((0.98, 2.0), np.array([1.01, np.nan, 1.02]), r_good)

    # Negative discount factor
    with pytest.raises(ValueError, match=r"strictly positive"):
        euler_residuals((-0.98, 2.0), c_good, r_good)

    # Mismatched instruments
    with pytest.raises(ValueError, match=r"Length mismatch"):
        sample_moments((0.98, 2.0), c_good, r_good, np.ones((2, 2)))

    # Valid evaluation check
    g_valid = sample_moments((0.98, 2.0), c_good, r_good, z_good)
    assert len(g_valid) == 4
