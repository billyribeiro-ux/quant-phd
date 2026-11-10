"""Lab AP5-project-2 (Rung 2, Completion): News Multipliers and Return Variance Shares.

SIMULATED: complete solution for the Rung 2 completion problem calculating
Campbell-Shiller discount-rate and cash-flow news variance shares from a fitted VAR.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # Given estimated VAR(1) parameters on annual data: z_t = [r_t, dp_t]^T
    phi = np.array([[0.015, 0.112], [-0.025, 0.935]])
    sigma = np.array([[0.0324, -0.0185], [-0.0185, 0.0210]])
    rho = 0.96

    # Step 1: Compute the Campbell-Shiller discount-rate news multiplier
    # lambda_dr = e_r^T rho Phi (I - rho Phi)^(-1)
    e_r = np.array([1.0, 0.0])
    eye_2 = np.eye(2)
    inv_mat = np.linalg.inv(eye_2 - rho * phi)
    lambda_dr = e_r @ (rho * phi) @ inv_mat

    # Step 2: Compute the cash-flow news multiplier
    # lambda_cf = e_r^T (I - rho Phi)^(-1)
    lambda_cf = e_r @ inv_mat

    # Step 3: Compute theoretical variances of return news
    var_dr = float(lambda_dr @ sigma @ lambda_dr)
    var_cf = float(lambda_cf @ sigma @ lambda_cf)
    cov_cf_dr = float(lambda_cf @ sigma @ lambda_dr)
    var_eta = float(e_r @ sigma @ e_r)

    # Step 4: Compute variance shares
    share_dr = var_dr / var_eta
    share_cf = var_cf / var_eta
    var_identity_err = abs(var_eta - (var_cf + var_dr - 2.0 * cov_cf_dr))

    print("Project Rung 2: Completion Problem Reference Output")
    print(f"DR multiplier lambda_dr:     [{lambda_dr[0]:.4f}, {lambda_dr[1]:.4f}]")
    print(f"CF multiplier lambda_cf:     [{lambda_cf[0]:.4f}, {lambda_cf[1]:.4f}]")
    print(f"Unexpected return var:       {var_eta:.6f}")
    print(f"Discount-rate news var:      {var_dr:.6f}")
    print(f"Cash-flow news var:          {var_cf:.6f}")
    print(f"CF-DR news covariance:       {cov_cf_dr:.6f}")
    print(f"Variance identity gap:       {var_identity_err:.8e}")
    print(f"DR news share of variance:   {share_dr * 100:.2f}%")
    print(f"CF news share of variance:   {share_cf * 100:.2f}%")


main()
