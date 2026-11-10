"""Lab AP5-project-1 (Rung 1, Worked Example): Fully Solved VAR Variance Decomposition.

SIMULATED: complete end-to-end Campbell-Shiller VAR variance decomposition pipeline
estimating return innovations, cash-flow news, discount-rate news, and long-horizon shares.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(42)
    n_obs = 200
    rho = 0.96

    # 1. Simulate calibrated return and dividend-price system
    # z_t = [r_t, dp_t]^T
    phi_true = np.array([[0.00, 0.10], [0.00, 0.93]])
    c_true = np.array([0.08, -3.20 * (1.0 - 0.93)])
    sigma_u = 0.18
    sigma_v = 0.14
    cov_uv = -0.72 * sigma_u * sigma_v
    cov_matrix = np.array([[sigma_u**2, cov_uv], [cov_uv, sigma_v**2]])

    eps = rng.multivariate_normal(mean=[0.0, 0.0], cov=cov_matrix, size=n_obs + 1)
    z = np.zeros((n_obs + 1, 2))
    z[0] = [0.08, -3.20]
    for t in range(n_obs):
        z[t + 1] = c_true + phi_true @ z[t] + eps[t + 1]

    # 2. OLS VAR(1) Estimation
    z_lag = z[:-1]
    z_lead = z[1:]
    x_mat = np.column_stack([np.ones(n_obs), z_lag])
    b_mat = np.linalg.lstsq(x_mat, z_lead, rcond=None)[0]
    phi_hat = b_mat[1:].T
    residuals = z_lead - x_mat @ b_mat
    sigma_hat = (residuals.T @ residuals) / (n_obs - 3)

    # 3. Campbell-Shiller News Vectors
    e_r = np.array([1.0, 0.0])
    eye_2 = np.eye(2)
    inv_mat = np.linalg.inv(eye_2 - rho * phi_hat)

    # lambda_dr = e_r^T rho Phi (I - rho Phi)^(-1)
    lambda_dr = e_r @ (rho * phi_hat) @ inv_mat
    # lambda_cf = e_r^T (I - rho Phi)^(-1)
    lambda_cf = e_r @ inv_mat

    n_dr = residuals @ lambda_dr
    n_cf = residuals @ lambda_cf
    eta_r = residuals[:, 0]

    # Check return innovation identity: eta_r = n_cf - n_dr
    max_id_err = float(np.max(np.abs(eta_r - (n_cf - n_dr))))

    # 4. Return Innovation Variance Decomposition
    var_eta = float(np.var(eta_r, ddof=1))
    var_cf = float(np.var(n_cf, ddof=1))
    var_dr = float(np.var(n_dr, ddof=1))
    cov_cf_dr = float(np.cov(n_cf, n_dr, ddof=1)[0, 1])

    share_dr = var_dr / var_eta
    share_cf = var_cf / var_eta
    share_cov = -2.0 * cov_cf_dr / var_eta

    # 5. Dividend-Yield Variance Decomposition
    # Solve discrete Lyapunov equation for population state covariance
    eye_4 = np.eye(4)
    gamma_vec = np.linalg.inv(eye_4 - np.kron(phi_hat, phi_hat)) @ sigma_hat.flatten()
    gamma_0 = gamma_vec.reshape((2, 2))

    e_dp = np.array([0.0, 1.0])
    long_run_r_op = inv_mat @ phi_hat
    long_run_d_op = (e_r @ phi_hat + rho * e_dp @ phi_hat - e_dp) @ inv_mat

    b_r = float((e_r @ long_run_r_op @ gamma_0 @ e_dp) / (e_dp @ gamma_0 @ e_dp))
    b_d = float((long_run_d_op @ gamma_0 @ e_dp) / (e_dp @ gamma_0 @ e_dp))
    identity_b = b_r - b_d

    print("Project Rung 1: VAR Variance Decomposition Worked Example")
    print(f"Sample length T:             {n_obs}")
    print(f"Estimated rho:               {rho:.4f}")
    print(f"VAR Phi[0,1] (return slope): {phi_hat[0, 1]:.4f}")
    print(f"VAR Phi[1,1] (persistence):  {phi_hat[1, 1]:.4f}")
    print(f"Max return news discrepancy: {max_id_err:.8e}")
    print(f"Unexpected return var:       {var_eta:.6f}")
    print(f"Discount-rate news var:      {var_dr:.6f} ({share_dr * 100:.2f}%)")
    print(f"Cash-flow news var:          {var_cf:.6f} ({share_cf * 100:.2f}%)")
    print(f"News covariance share:       {share_cov * 100:.2f}%")
    print(f"Long-horizon return share b_r:   {b_r * 100:.2f}%")
    print(f"Long-horizon dividend share b_d: {b_d * 100:.2f}%")
    print(f"Identity b_r - b_d:              {identity_b * 100:.2f}%")


main()
