"""Acceptance test suite for FI2: Affine term-structure model calibration.

Verifies:
1. Riccati system boundary conditions (Duffie-Kan 1996).
2. Factor loadings monotonicity and asymptotic limits.
3. Unconditional state moments and Lyapunov equation exactness (Hamilton 1994).
4. Kalman filter pricing error RMSE bounds on simulated yields.
5. Innovation orthogonality and zero-mean properties.
6. Log-likelihood sensitivity to parameter perturbations.
7. MLE calibration recovery and factor dynamics.
"""

from __future__ import annotations

import os
from typing import Any, cast

import numpy as np
import pytest
from instance import make_instance

# The browser autograder loads the solution module as configured in project.html.
try:
    import affine_calibration as sol
except ImportError:
    import reference as sol

pytestmark = pytest.mark.filterwarnings("error")


@pytest.fixture
def current_instance() -> dict[str, Any]:
    seed = int(os.environ.get("QF_SEED", "0"))
    return cast(dict[str, Any], make_instance(seed))


def test_riccati_boundary_conditions(current_instance: dict[str, Any]) -> None:
    """Verify that A(0) = 0 and B(0) = 0, and that initial derivatives match theoretical rates."""
    delta0 = float(current_instance["delta0"])
    kappa = np.asarray(current_instance["kappa"], dtype=np.float64)
    sigma = np.asarray(current_instance["sigma"], dtype=np.float64)

    # Exact zero maturity
    tau_zero = np.array([0.0], dtype=np.float64)
    a_zero, b_zero = sol.solve_riccati_ode(tau_zero, delta0, kappa, sigma)
    assert abs(float(a_zero[0])) < 1e-12, "Boundary condition A(0) == 0 violated"
    assert np.all(np.abs(b_zero[0]) < 1e-12), "Boundary condition B(0) == 0 violated"

    # Limit derivative as tau -> 0+: dB_i/dtau(0) = -1.0, dA/dtau(0) = -delta0
    eps = 1e-6
    tau_eps = np.array([eps], dtype=np.float64)
    a_eps, b_eps = sol.solve_riccati_ode(tau_eps, delta0, kappa, sigma)

    deriv_a = float(a_eps[0]) / eps
    deriv_b = b_eps[0] / eps

    assert abs(deriv_a - (-delta0)) < 1e-4, f"dA/dtau(0) must equal -delta0; got {deriv_a} vs {-delta0}"
    for i in range(3):
        assert abs(deriv_b[i] - (-1.0)) < 1e-4, f"dB_{i}/dtau(0) must equal -1.0; got {deriv_b[i]}"


def test_yield_loadings_properties(current_instance: dict[str, Any]) -> None:
    """Verify factor loadings H(tau) are strictly positive and decay monotonically with maturity."""
    tau = np.asarray(current_instance["tau"], dtype=np.float64)
    delta0 = float(current_instance["delta0"])
    kappa = np.asarray(current_instance["kappa"], dtype=np.float64)
    sigma = np.asarray(current_instance["sigma"], dtype=np.float64)

    a_yield, h_yield = sol.yield_loadings(tau, delta0, kappa, sigma)

    assert len(a_yield) == len(tau), "Intercept length must match maturities"
    assert h_yield.shape == (len(tau), 3), "Factor loading matrix shape must be (M, 3)"

    # Loadings must be strictly positive
    assert np.all(h_yield > 0.0), "All Gaussian ATSM yield factor loadings must be strictly positive"

    # Factor 1 (slowest mean reversion) must decay slower than Factor 3 (fastest mean reversion)
    # At tau = 10Y, H_{10Y, 1} > H_{10Y, 2} > H_{10Y, 3}
    m_long = -1  # 10 year tenor
    assert h_yield[m_long, 0] > h_yield[m_long, 1] > h_yield[m_long, 2], (
        f"Factor loadings ordering violated at 10Y maturity: {h_yield[m_long]}"
    )


def test_unconditional_moments_lyapunov(current_instance: dict[str, Any]) -> None:
    """Verify unconditional covariance satisfies the discrete Lyapunov equation V = Phi V Phi^T + Q."""
    c_vec = np.asarray(current_instance["c"], dtype=np.float64)
    phi_mat = np.asarray(current_instance["phi"], dtype=np.float64)
    q_cov = np.asarray(current_instance["Q"], dtype=np.float64)

    mean_x, cov_x = sol.compute_unconditional_moments(c_vec, phi_mat, q_cov)

    assert mean_x.shape == (3,), "State mean must have shape (3,)"
    assert cov_x.shape == (3, 3), "State covariance must have shape (3, 3)"

    # Check Lyapunov equation residual: ||V - (Phi V Phi^T + Q)|| < 1e-9
    reconstructed_q = cov_x - phi_mat @ cov_x @ phi_mat.T
    diff = np.max(np.abs(reconstructed_q - q_cov))
    assert diff < 1e-9, f"Lyapunov equation violated: max absolute error = {diff}"

    # Verify symmetry and positive definiteness
    symm_err = np.max(np.abs(cov_x - cov_x.T))
    assert symm_err < 1e-12, "Unconditional covariance matrix must be exactly symmetric"
    eigvals = np.linalg.eigvalsh(cov_x)
    assert np.all(eigvals > 0.0), "Unconditional covariance matrix must be positive definite"


def test_kalman_filter_reconstruction_and_rmse(current_instance: dict[str, Any]) -> None:
    """Verify Kalman filter yields RMSE <= 15 bps and correlates with true simulated latent factors."""
    yields = np.asarray(current_instance["yields"], dtype=np.float64)
    tau = np.asarray(current_instance["tau"], dtype=np.float64)
    delta0 = float(current_instance["delta0"])
    kappa = np.asarray(current_instance["kappa"], dtype=np.float64)
    sigma = np.asarray(current_instance["sigma"], dtype=np.float64)
    c_vec = np.asarray(current_instance["c"], dtype=np.float64)
    phi_mat = np.asarray(current_instance["phi"], dtype=np.float64)
    q_cov = np.asarray(current_instance["Q"], dtype=np.float64)
    r_diag = np.asarray(current_instance["R_diag"], dtype=np.float64)
    true_states = np.asarray(current_instance["true_states"], dtype=np.float64)

    res = sol.kalman_filter(yields, tau, delta0, kappa, sigma, c_vec, phi_mat, q_cov, r_diag)

    rmse_bps = float(res["rmse_bps"])
    # Injected measurement noise is 5 bps; overall RMSE must be within 15 bps
    assert rmse_bps < 15.0, f"Kalman filter pricing RMSE too high: {rmse_bps:.2f} bps (expected < 15 bps)"

    filtered_states = np.asarray(res["filtered_states"], dtype=np.float64)
    assert filtered_states.shape == true_states.shape, "Filtered states shape mismatch"

    # Correlation between filtered factors and true simulated factors
    for i in range(3):
        corr = float(np.corrcoef(filtered_states[:, i], true_states[:, i])[0, 1])
        assert corr > 0.50, f"Factor {i} correlation between filtered and true states is {corr:.3f} (< 0.50)"


def test_kalman_innovations_orthogonality(current_instance: dict[str, Any]) -> None:
    """Verify Kalman innovations are approximately mean zero and have low lag-1 autocorrelation."""
    yields = np.asarray(current_instance["yields"], dtype=np.float64)
    tau = np.asarray(current_instance["tau"], dtype=np.float64)
    delta0 = float(current_instance["delta0"])
    kappa = np.asarray(current_instance["kappa"], dtype=np.float64)
    sigma = np.asarray(current_instance["sigma"], dtype=np.float64)
    c_vec = np.asarray(current_instance["c"], dtype=np.float64)
    phi_mat = np.asarray(current_instance["phi"], dtype=np.float64)
    q_cov = np.asarray(current_instance["Q"], dtype=np.float64)
    r_diag = np.asarray(current_instance["R_diag"], dtype=np.float64)

    res = sol.kalman_filter(yields, tau, delta0, kappa, sigma, c_vec, phi_mat, q_cov, r_diag)
    innovations = np.asarray(res["innovations"], dtype=np.float64)

    # Mean innovation across all tenors must be bounded in finite sample T=60 (< 50 bps)
    mean_innov = np.abs(np.mean(innovations, axis=0))
    assert np.all(mean_innov < 0.0050), f"Mean innovation exceeds tolerance: {mean_innov}"

    # Whiteness: lag-1 autocorrelation for each tenor should be small (|rho| < 0.50)
    for m in range(len(tau)):
        v_seq = innovations[:, m]
        v_dm = v_seq - np.mean(v_seq)
        var_v = np.var(v_seq)
        if var_v > 1e-12:
            rho1 = float(np.sum(v_dm[:-1] * v_dm[1:]) / ((len(v_seq) - 1) * var_v))
            assert abs(rho1) < 0.50, f"Tenor {tau[m]}Y innovation has high serial correlation: rho1={rho1:.3f}"


def test_kalman_log_likelihood_sensitivity(current_instance: dict[str, Any]) -> None:
    """Verify that true parameters achieve a strictly higher log-likelihood than perturbed parameters."""
    yields = np.asarray(current_instance["yields"], dtype=np.float64)
    tau = np.asarray(current_instance["tau"], dtype=np.float64)
    delta0 = float(current_instance["delta0"])
    kappa = np.asarray(current_instance["kappa"], dtype=np.float64)
    sigma = np.asarray(current_instance["sigma"], dtype=np.float64)
    c_vec = np.asarray(current_instance["c"], dtype=np.float64)
    phi_mat = np.asarray(current_instance["phi"], dtype=np.float64)
    q_cov = np.asarray(current_instance["Q"], dtype=np.float64)
    r_diag = np.asarray(current_instance["R_diag"], dtype=np.float64)

    true_params = np.concatenate([[delta0], kappa, sigma])
    ll_true = sol.kalman_log_likelihood(true_params, yields, tau, c_vec, phi_mat, q_cov, r_diag)

    # Distort mean-reversion speeds by doubling them
    distorted_params = np.concatenate([[delta0], kappa * 2.0, sigma])
    ll_distorted = sol.kalman_log_likelihood(distorted_params, yields, tau, c_vec, phi_mat, q_cov, r_diag)

    assert ll_true > ll_distorted, (
        f"Log-likelihood at true parameters ({ll_true:.2f}) must exceed distorted parameters ({ll_distorted:.2f})"
    )


def test_mle_calibration_fit(current_instance: dict[str, Any]) -> None:
    """Verify that MLE calibration produces valid parameters and low pricing RMSE."""
    yields = np.asarray(current_instance["yields"], dtype=np.float64)
    tau = np.asarray(current_instance["tau"], dtype=np.float64)
    delta0 = float(current_instance["delta0"])
    kappa = np.asarray(current_instance["kappa"], dtype=np.float64)
    sigma = np.asarray(current_instance["sigma"], dtype=np.float64)

    initial_guess = np.concatenate([[delta0], kappa, sigma])
    calib = sol.calibrate_mle(yields, tau, initial_guess)

    assert float(calib["delta0"]) > 0.0, "Calibrated delta0 must be positive"
    assert np.all(np.asarray(calib["kappa"]) > 0.0), "Calibrated kappa must be positive"
    assert np.all(np.asarray(calib["sigma"]) > 0.0), "Calibrated sigma must be positive"
    assert float(calib["rmse_bps"]) < 15.0, f"Calibrated pricing RMSE too high: {float(calib['rmse_bps']):.2f} bps"
