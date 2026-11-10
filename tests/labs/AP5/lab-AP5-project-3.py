"""Lab AP5-project-3 (Rung 3, Reference Run): Benchmark Outputs for Autograder Validation.

SIMULATED: runs the reference implementation on fixed benchmark inputs to establish
gold-standard test numbers for independent project verification.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # Fixed benchmark input matrix: 100 periods of [r_t, dp_t]
    rng = np.random.default_rng(2024)
    n_obs = 100
    rho = 0.96

    phi_bench = np.array([[0.01, 0.12], [-0.02, 0.91]])
    sigma_bench = np.array([[0.035, -0.018], [-0.018, 0.020]])
    c_bench = np.array([0.07, -0.28])

    eps = rng.multivariate_normal(mean=[0.0, 0.0], cov=sigma_bench, size=n_obs + 1)
    z = np.zeros((n_obs + 1, 2))
    z[0] = [0.07, -3.10]
    for t in range(n_obs):
        z[t + 1] = c_bench + phi_bench @ z[t] + eps[t + 1]

    # 1. Estimate VAR
    z_lag = z[:-1]
    z_lead = z[1:]
    x_mat = np.column_stack([np.ones(n_obs), z_lag])
    b_mat = np.linalg.lstsq(x_mat, z_lead, rcond=None)[0]
    c_hat = b_mat[0]
    phi_hat = b_mat[1:].T
    resids = z_lead - x_mat @ b_mat
    sigma_hat = (resids.T @ resids) / (n_obs - 3)

    # 2. Campbell-Shiller News
    e_r = np.array([1.0, 0.0])
    eye_2 = np.eye(2)
    inv_mat = np.linalg.inv(eye_2 - rho * phi_hat)
    lambda_dr = e_r @ (rho * phi_hat) @ inv_mat
    lambda_cf = e_r @ inv_mat

    n_dr = resids @ lambda_dr
    n_cf = resids @ lambda_cf
    eta = resids[:, 0]

    # Variances
    var_eta = float(np.var(eta, ddof=1))
    var_dr = float(np.var(n_dr, ddof=1))
    var_cf = float(np.var(n_cf, ddof=1))
    cov_news = float(np.cov(n_cf, n_dr, ddof=1)[0, 1])

    # 3. Dividend-yield variance shares
    eye_4 = np.eye(4)
    gamma_vec = np.linalg.inv(eye_4 - np.kron(phi_hat, phi_hat)) @ sigma_hat.flatten()
    gamma_0 = gamma_vec.reshape((2, 2))

    e_dp = np.array([0.0, 1.0])
    long_run_r = inv_mat @ phi_hat
    long_run_d = (e_r @ phi_hat + rho * e_dp @ phi_hat - e_dp) @ inv_mat

    b_r = float((e_r @ long_run_r @ gamma_0 @ e_dp) / (e_dp @ gamma_0 @ e_dp))
    b_d = float((long_run_d @ gamma_0 @ e_dp) / (e_dp @ gamma_0 @ e_dp))

    # 4. Stambaugh bias for predictive regression of r on dp
    phi_dp = phi_hat[1, 1]
    sigma_uv = float(sigma_hat[0, 1])
    sigma_v2 = float(sigma_hat[1, 1])
    stambaugh_bias = -(sigma_uv / sigma_v2) * ((1.0 + 3.0 * phi_dp) / n_obs)

    print("Project Rung 3: Benchmark Autograder Validation Output")
    print(f"Estimated c:                 [{c_hat[0]:.4f}, {c_hat[1]:.4f}]")
    print(f"Estimated Phi[0,1]:          {phi_hat[0, 1]:.4f}")
    print(f"Estimated Phi[1,1]:          {phi_hat[1, 1]:.4f}")
    print(f"Return innovation var:       {var_eta:.6f}")
    print(f"Discount-rate news var:      {var_dr:.6f}")
    print(f"Cash-flow news var:          {var_cf:.6f}")
    print(f"CF-DR covariance:            {cov_news:.6f}")
    print(f"DR variance share:           {var_dr / var_eta * 100:.2f}%")
    print(f"Long-horizon b_r:            {b_r * 100:.2f}%")
    print(f"Long-horizon b_d:            {b_d * 100:.2f}%")
    print(f"Identity b_r - b_d:          {(b_r - b_d) * 100:.2f}%")
    print(f"Stambaugh analytical bias:   {stambaugh_bias:.4f}")


main()
