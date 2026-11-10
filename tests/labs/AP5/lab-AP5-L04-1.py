"""Lab AP5-L04-1: Vector Autoregression and News Decomposition.

SIMULATED: estimates a first-order VAR on returns and the log dividend-price ratio
to decompose unexpected stock returns into cash-flow news and discount-rate news
(Campbell & Shiller 1988, Campbell 1991).
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(888)
    n_obs = 250  # 250 annual observations
    rho = 0.96  # annual discount factor

    # True VAR(1) parameters: z_t = [r_t - E[r], dp_t - E[dp]]^T
    # dp_{t+1} = 0.92 * dp_t - 0.05 * r_t + v_{t+1}
    # r_{t+1}  = 0.12 * dp_t + u_{t+1}
    phi_true = np.array([[0.02, 0.12], [-0.03, 0.92]])
    sigma_u = 0.18
    sigma_v = 0.15
    cov_uv = -0.75 * sigma_u * sigma_v
    cov_true = np.array([[sigma_u**2, cov_uv], [cov_uv, sigma_v**2]])

    # Simulate VAR series
    eps = rng.multivariate_normal(mean=[0.0, 0.0], cov=cov_true, size=n_obs + 1)
    z = np.zeros((n_obs + 1, 2))
    for t in range(n_obs):
        z[t + 1] = phi_true @ z[t] + eps[t + 1]

    # Demean variables
    z_demean = z - np.mean(z, axis=0)
    z_lag = z_demean[:-1]
    z_lead = z_demean[1:]

    # OLS estimation of VAR(1): z_lead = z_lag @ Phi.T + residuals
    phi_hat = (np.linalg.inv(z_lag.T @ z_lag) @ (z_lag.T @ z_lead)).T
    resids = z_lead - (z_lag @ phi_hat.T)

    # News decomposition matrices
    # e_r = [1, 0]^T
    e_r = np.array([1.0, 0.0])
    eye_2 = np.eye(2)
    inv_matrix = np.linalg.inv(eye_2 - rho * phi_hat)

    # lambda_dr = e_r^T rho Phi (I - rho Phi)^(-1)
    lambda_dr = e_r @ (rho * phi_hat) @ inv_matrix
    # lambda_cf = e_r^T + lambda_dr = e_r^T (I - rho Phi)^(-1)
    lambda_cf = e_r @ inv_matrix

    # News series for each period t:
    n_dr = resids @ lambda_dr
    n_cf = resids @ lambda_cf
    eta_r = resids[:, 0]  # unexpected return = e_r^T resids

    # Verify return identity: eta_r = N_cf - N_dr
    identity_diff = np.max(np.abs(eta_r - (n_cf - n_dr)))

    # Compute variance-covariance decomposition
    var_eta = float(np.var(eta_r, ddof=1))
    var_cf = float(np.var(n_cf, ddof=1))
    var_dr = float(np.var(n_dr, ddof=1))
    cov_cf_dr = float(np.cov(n_cf, n_dr, ddof=1)[0, 1])

    # Algebraic variance identity: var(eta) = var(cf) + var(dr) - 2*cov(cf, dr)
    var_sum = var_cf + var_dr - 2.0 * cov_cf_dr
    var_diff = abs(var_eta - var_sum)

    # Share of return variance
    share_dr = var_dr / var_eta
    share_cf = var_cf / var_eta
    share_cov = -2.0 * cov_cf_dr / var_eta

    print("Campbell-Shiller (1988) VAR News Decomposition")
    print(f"Sample length T:             {n_obs} years")
    print(f"Discount factor rho:         {rho:.4f}")
    print(
        f"VAR eigenvalues:             {float(np.abs(np.linalg.eigvals(phi_hat))[0]):.4f}, "
        f"{float(np.abs(np.linalg.eigvals(phi_hat))[1]):.4f}"
    )
    print(f"Max identity discrepancy:    {identity_diff:.8e}")
    print(f"Return innovation var:       {var_eta:.6f}")
    print(f"Discount-rate news var:      {var_dr:.6f}")
    print(f"Cash-flow news var:          {var_cf:.6f}")
    print(f"CF-DR news covariance:       {cov_cf_dr:.6f}")
    print(f"Variance identity gap:       {var_diff:.8e}")
    print(f"DR news share of variance:   {share_dr * 100:.2f}%")
    print(f"CF news share of variance:   {share_cf * 100:.2f}%")
    print(f"Covariance share:            {share_cov * 100:.2f}%")


main()
