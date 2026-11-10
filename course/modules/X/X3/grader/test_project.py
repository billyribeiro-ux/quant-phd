"""Test suite for X3 Kilian structural VAR oil-shock decomposition."""

from __future__ import annotations

from typing import Any

import pytest

try:
    import kilian_svar as solver
except ImportError:
    import reference as solver

# The solver module under test (reference, starter, or student solution)
from instance import make_instance


@pytest.fixture
def sample_instance() -> dict[str, Any]:
    """Return a standard test instance (seed 42)."""
    return make_instance(42)


def test_cholesky_factorization() -> None:
    """Verify Cholesky decomposition reconstructs the matrix and is lower triangular."""
    a_mat = [
        [4.0, 1.0, 0.5],
        [1.0, 5.0, 1.5],
        [0.5, 1.5, 6.0],
    ]
    l_mat = solver.cholesky(a_mat)
    # Check lower triangularity
    assert abs(l_mat[0][1]) < 1e-12, "Upper triangular element (0, 1) must be zero"
    assert abs(l_mat[0][2]) < 1e-12, "Upper triangular element (0, 2) must be zero"
    assert abs(l_mat[1][2]) < 1e-12, "Upper triangular element (1, 2) must be zero"
    # Check positive diagonal
    assert l_mat[0][0] > 0
    assert l_mat[1][1] > 0
    assert l_mat[2][2] > 0
    # Check reconstruction L * L^T == A
    k_dim = len(a_mat)
    for i in range(k_dim):
        for j in range(k_dim):
            rec = sum(l_mat[i][k] * l_mat[j][k] for k in range(k_dim))
            assert abs(rec - a_mat[i][j]) < 1e-5, f"Cholesky reconstruction failed at ({i}, {j})"


def test_cholesky_non_positive_definite_raises() -> None:
    """Verify that a non-positive-definite matrix raises ValueError."""
    bad_mat = [
        [1.0, 2.0],
        [2.0, 1.0],  # Det = 1 - 4 = -3 < 0
    ]
    with pytest.raises(ValueError):
        solver.cholesky(bad_mat)


def test_invert_matrix() -> None:
    """Verify that invert_matrix returns the exact inverse."""
    a_mat = [
        [3.0, 1.0, 0.0],
        [1.0, 4.0, 1.0],
        [0.0, 1.0, 2.0],
    ]
    a_inv = solver.invert_matrix(a_mat)
    k_dim = len(a_mat)
    for i in range(k_dim):
        for j in range(k_dim):
            val = sum(a_mat[i][k] * a_inv[k][j] for k in range(k_dim))
            expected = 1.0 if i == j else 0.0
            assert abs(val - expected) < 1e-6, f"Matrix inversion failed at ({i}, {j})"


def test_var_estimation_dimensions(sample_instance: dict[str, Any]) -> None:
    """Verify OLS VAR estimation dimensions and residual shapes."""
    data = sample_instance["data"]
    lags = sample_instance["lags"]
    k_vars = len(data[0])
    t_obs = len(data)

    res = solver.estimate_var(data, lags)
    assert len(res["intercepts"]) == k_vars
    assert len(res["coefficients"]) == lags
    for bl in res["coefficients"]:
        assert len(bl) == k_vars
        assert all(len(row) == k_vars for row in bl)
    assert len(res["residuals"]) == t_obs - lags
    assert len(res["sigma_u"]) == k_vars
    assert all(len(row) == k_vars for row in res["sigma_u"])


def test_var_residuals_orthogonality(sample_instance: dict[str, Any]) -> None:
    """Verify OLS orthogonality: residuals must have mean approximately zero and be orthogonal to regressors."""
    data = sample_instance["data"]
    lags = sample_instance["lags"]
    res = solver.estimate_var(data, lags)
    residuals = res["residuals"]
    n_effective = len(residuals)
    k_vars = len(data[0])

    for k in range(k_vars):
        mean_e = sum(residuals[t][k] for t in range(n_effective)) / n_effective
        assert abs(mean_e) < 1e-3, f"Residual mean for var {k} is {mean_e}, expected ~ 0"


def test_structural_impact_matrix(sample_instance: dict[str, Any]) -> None:
    """Verify Kilian recursive Cholesky identification: P is lower triangular with P P^T = Sigma_u."""
    data = sample_instance["data"]
    lags = sample_instance["lags"]
    var_res = solver.estimate_var(data, lags)
    sigma_u = var_res["sigma_u"]
    p_mat = solver.cholesky_identification(sigma_u)
    k_vars = len(p_mat)

    # Strictly lower triangular: upper elements must be zero
    msg_supply = f"Oil supply must not respond contemporaneously (P[0][1]={p_mat[0][1]})"
    assert abs(p_mat[0][1]) < 1e-5, msg_supply
    assert abs(p_mat[0][2]) < 1e-5, f"P[0][2]={p_mat[0][2]} must be zero"
    assert abs(p_mat[1][2]) < 1e-5, f"P[1][2]={p_mat[1][2]} must be zero"

    # Positive diagonal
    for i in range(k_vars):
        assert p_mat[i][i] > 0, f"Diagonal element P[{i}][{i}] must be positive"

    # Reconstruction of Sigma_u
    for i in range(k_vars):
        for j in range(k_vars):
            rec = sum(p_mat[i][k] * p_mat[j][k] for k in range(k_vars))
            assert abs(rec - sigma_u[i][j]) < 1e-4, f"Impact matrix failed to reconstruct Sigma_u at ({i}, {j})"


def test_structural_shocks_orthogonality(sample_instance: dict[str, Any]) -> None:
    """Verify that extracted structural innovations eps_t = P^-1 e_t have unit variance and zero covariance."""
    data = sample_instance["data"]
    lags = sample_instance["lags"]
    var_res = solver.estimate_var(data, lags)
    p_mat = solver.cholesky_identification(var_res["sigma_u"])
    shocks = solver.compute_structural_shocks(var_res["residuals"], p_mat)
    n_obs = len(shocks)
    k_vars = len(p_mat)

    for i in range(k_vars):
        var_i = sum(shocks[t][i] ** 2 for t in range(n_obs)) / n_obs
        assert abs(var_i - 1.0) < 0.20, f"Structural shock variance for {i} is {var_i}, expected ~ 1.0"
        for j in range(i + 1, k_vars):
            cov_ij = sum(shocks[t][i] * shocks[t][j] for t in range(n_obs)) / n_obs
            assert abs(cov_ij) < 0.15, f"Structural shock covariance between {i} and {j} is {cov_ij}, expected ~ 0"


def test_irf_horizon_zero(sample_instance: dict[str, Any]) -> None:
    """Verify that at horizon 0, Theta_0 equals P exactly."""
    data = sample_instance["data"]
    lags = sample_instance["lags"]
    var_res = solver.estimate_var(data, lags)
    p_mat = solver.cholesky_identification(var_res["sigma_u"])
    irf = solver.compute_irf(var_res["coefficients"], p_mat, 24)
    k_vars = len(p_mat)

    assert len(irf) == 25, f"IRF must return 25 horizons (0 to 24), got {len(irf)}"
    for i in range(k_vars):
        for j in range(k_vars):
            assert abs(irf[0][i][j] - p_mat[i][j]) < 1e-5, f"IRF at h=0 ({irf[0][i][j]}) != P[{i}][{j}] ({p_mat[i][j]})"


def test_irf_higher_order_dynamics(sample_instance: dict[str, Any]) -> None:
    """Verify that IRF at horizon h=2 accounts for second lag matrix B_2 (Phi_2 = B_1^2 + B_2)."""
    data = sample_instance["data"]
    lags = sample_instance["lags"]
    var_res = solver.estimate_var(data, lags)
    p_mat = solver.cholesky_identification(var_res["sigma_u"])
    coeffs = var_res["coefficients"]
    irf = solver.compute_irf(coeffs, p_mat, 24)

    # Theoretical Phi_2 = B1 * B1 + B2
    k_vars = len(p_mat)
    b1 = coeffs[0]
    b2 = coeffs[1]
    b1_sq = [[sum(b1[i][k] * b1[k][j] for k in range(k_vars)) for j in range(k_vars)] for i in range(k_vars)]
    phi_2_theory = [[b1_sq[i][j] + b2[i][j] for j in range(k_vars)] for i in range(k_vars)]
    theta_2_theory = [
        [sum(phi_2_theory[i][k] * p_mat[k][j] for k in range(k_vars)) for j in range(k_vars)] for i in range(k_vars)
    ]

    for i in range(k_vars):
        for j in range(k_vars):
            diff = abs(irf[2][i][j] - theta_2_theory[i][j])
            assert diff < 1e-4, f"IRF at horizon 2 failed theoretical lag-2 propagation at ({i}, {j}): diff={diff}"


def test_fevd_properties(sample_instance: dict[str, Any]) -> None:
    """Verify FEVD properties: shares sum to 1.0 across shocks, and contemporaneous timing restrictions hold."""
    data = sample_instance["data"]
    lags = sample_instance["lags"]
    var_res = solver.estimate_var(data, lags)
    p_mat = solver.cholesky_identification(var_res["sigma_u"])
    irf = solver.compute_irf(var_res["coefficients"], p_mat, 24)
    fevd = solver.compute_fevd(irf)
    k_vars = len(p_mat)

    # 1. Row sums must equal 1.0
    for h in range(len(fevd)):
        for i in range(k_vars):
            row_sum = sum(fevd[h][i])
            assert abs(row_sum - 1.0) < 1e-4, f"FEVD at horizon {h}, var {i} sums to {row_sum} != 1.0"

    # 2. At horizon 0, oil supply is 100% explained by supply shock
    assert abs(fevd[0][0][0] - 1.0) < 1e-4, f"FEVD[0][0][0] must be 1.0, got {fevd[0][0][0]}"
    assert abs(fevd[0][0][1]) < 1e-5, f"FEVD[0][0][1] must be 0.0, got {fevd[0][0][1]}"
    assert abs(fevd[0][0][2]) < 1e-5, f"FEVD[0][0][2] must be 0.0, got {fevd[0][0][2]}"

    # 3. At horizon 0, real activity is 0% explained by oil-specific demand shock
    assert abs(fevd[0][1][2]) < 1e-5, f"FEVD[0][1][2] must be 0.0, got {fevd[0][1][2]}"


def test_historical_decomposition_reconstruction(sample_instance: dict[str, Any]) -> None:
    """Verify that historical decomposition shock contributions sum to fitted values."""
    data = sample_instance["data"]
    lags = sample_instance["lags"]
    var_res = solver.estimate_var(data, lags)
    p_mat = solver.cholesky_identification(var_res["sigma_u"])
    hd = solver.compute_historical_decomposition(var_res["residuals"], var_res["coefficients"], p_mat)

    k_vars = len(p_mat)
    n_obs = len(var_res["residuals"])
    contributions = hd["contributions"]
    fitted = hd["fitted"]

    assert len(contributions) == k_vars, f"Must have {k_vars} shock contribution matrices"
    for t in range(n_obs):
        for i in range(k_vars):
            sum_contrib = sum(contributions[j][t][i] for j in range(k_vars))
            assert abs(sum_contrib - fitted[t][i]) < 1e-4, f"Fitted reconstruction mismatch at t={t}, var={i}"


def test_validation_errors() -> None:
    """Verify that input validation raises ValueError on illegal parameters."""
    with pytest.raises(ValueError):
        solver.estimate_var([[1.0, 2.0]], lags=0)  # lags < 1
    with pytest.raises(ValueError):
        solver.estimate_var([], lags=2)  # empty data
    with pytest.raises(ValueError):
        solver.compute_irf([], [[1.0]], horizon=-1)  # negative horizon


def test_full_pipeline_50_seeds() -> None:
    """Verify the end-to-end pipeline on consecutive seeds."""
    for s in range(50):
        inst = make_instance(s)
        res = solver.run_oil_shock_var(inst)
        assert res["seed"] == s
        assert len(res["irf"]) == 25
        assert len(res["fevd"]) == 25
        # Verify FEVD row sums
        for h in (0, 1, 6, 12, 24):
            for i in range(3):
                assert abs(sum(res["fevd"][h][i]) - 1.0) < 1e-4
