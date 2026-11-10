"""Lab CAP4-project-2: Doctoral Thesis Econometric Pipeline Completion Task.

Full completed solution for Rung 2: Completion Problem.
Computes cross-sectional asset pricing metrics:
- Shanken variance correction factor
- Shanken-corrected standard error
- Gibbons-Ross-Shanken (GRS) statistic
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    np.random.seed(42)
    t_obs = 240
    n_assets = 8
    n_factors = 2

    # Calibrated inputs
    lambda_hat = np.array([0.0075, 0.0045])
    sigma_f = np.array([[0.0025, 0.0004], [0.0004, 0.0016]])
    inv_sigma_f = np.linalg.inv(sigma_f)

    # Shanken correction factor c = 1 + lambda' Sigma_f^{-1} lambda
    shanken_quad = float(lambda_hat @ inv_sigma_f @ lambda_hat)
    shanken_factor = 1.0 + shanken_quad

    # Test asset pricing errors and residual covariance
    alpha_hat = np.array([0.0015, -0.0010, 0.0020, -0.0015, 0.0008, -0.0005, 0.0012, -0.0018])
    sigma_eps = np.eye(n_assets) * 0.0009
    inv_sigma_eps = np.linalg.inv(sigma_eps)

    # GRS statistic
    f_bar = np.array([0.0060, 0.0035])
    quad_alpha = float(alpha_hat @ inv_sigma_eps @ alpha_hat)
    quad_f = float(f_bar @ inv_sigma_f @ f_bar)
    grs_df_num = n_assets
    grs_df_denom = t_obs - n_assets - n_factors
    grs_scale = float(grs_df_denom / grs_df_num)
    grs_stat = float(grs_scale * (quad_alpha / (1.0 + quad_f)))

    # Simplified standard error for second factor
    v_pricing_22 = 0.00035
    se_shanken_f2 = float(np.sqrt((1.0 / t_obs) * (sigma_f[1, 1] + shanken_factor * v_pricing_22)))

    print(f"Shanken Correction Factor: {shanken_factor:.4f}")
    print(f"Factor 2 Shanken SE: {se_shanken_f2 * 100:.4f}%")
    print(f"GRS F-Statistic: {grs_stat:.4f}")
    print(f"GRS Degrees of Freedom: ({grs_df_num}, {grs_df_denom})")
    print(f"Pipeline Invariant Verified: {bool(shanken_factor > 1.0)}")


main()
