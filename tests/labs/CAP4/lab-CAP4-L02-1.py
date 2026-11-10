"""Lab CAP4-L02-1: SDF Theoretical Euler Invariant & Pricing Error Diagnostic.

Evaluates theoretical framing by deriving Hansen-Jagannathan SDF bounds,
evaluating Euler equation pricing errors E[m R^e] = 0, and computing Hansen-Jagannathan distance.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    np.random.seed(42)
    n_assets = 5
    rf = 0.02
    mean_sdf = 1.0 / (1.0 + rf)

    # 1. Calibrated cross-sectional excess returns and covariance
    mu_excess = np.array([0.05, 0.07, 0.04, 0.08, 0.06])
    volatilities = np.array([0.16, 0.22, 0.14, 0.25, 0.18])
    corr = np.array(
        [
            [1.00, 0.50, 0.35, 0.60, 0.45],
            [0.50, 1.00, 0.40, 0.65, 0.50],
            [0.35, 0.40, 1.00, 0.40, 0.30],
            [0.60, 0.65, 0.40, 1.00, 0.55],
            [0.45, 0.50, 0.30, 0.55, 1.00],
        ]
    )
    cov_excess = np.outer(volatilities, volatilities) * corr
    inv_cov = np.linalg.inv(cov_excess)

    # 2. Maximum Sharpe ratio of the tangency portfolio
    sr_tangency = float(np.sqrt(mu_excess @ inv_cov @ mu_excess))
    hj_vol_bound = float(mean_sdf * sr_tangency)

    # 3. Candidate affine SDF: m = mean_sdf * (1 - b^T (f - E[f]))
    # For a correctly specified single-factor model tracking tangency: b = inv_cov @ mu_excess
    b_optimal = inv_cov @ mu_excess
    var_f = float(mu_excess @ inv_cov @ mu_excess)
    sdf_vol = float(mean_sdf * np.sqrt(var_f))

    # 4. Misspecified candidate SDF: naive equal-weighted factor
    b_misspec = np.ones(n_assets) * 0.2
    # Implied pricing errors: alpha = mu_excess - Cov(R^e, m) / E[m]
    # Here Cov(R^e, m) = -mean_sdf * cov_excess @ b
    cov_re_m = -mean_sdf * (cov_excess @ b_misspec)
    pricing_errors = mu_excess + (cov_re_m / mean_sdf)

    # 5. Hansen-Jagannathan Distance: HJ = sqrt(alpha^T E[R R^T]^{-1} alpha)
    # Using second-moment matrix for excess returns: Omega = cov_excess + outer(mu, mu)
    second_moment = cov_excess + np.outer(mu_excess, mu_excess)
    inv_second_moment = np.linalg.inv(second_moment)
    hj_distance = float(np.sqrt(pricing_errors @ inv_second_moment @ pricing_errors))

    # Perfect SDF Euler error
    cov_re_m_opt = -mean_sdf * (cov_excess @ b_optimal)
    optimal_pricing_errors = mu_excess + (cov_re_m_opt / mean_sdf)
    max_euler_error = float(np.max(np.abs(optimal_pricing_errors)))

    print(f"Tangency Sharpe Ratio: {sr_tangency:.4f}")
    print(f"Hansen-Jagannathan Volatility Bound: {hj_vol_bound:.4f}")
    print(f"Optimal SDF Volatility: {sdf_vol:.4f}")
    print(f"Optimal Model Max Euler Error: {max_euler_error:.2e}")
    print(f"Misspecified Mean Abs Pricing Error: {float(np.mean(np.abs(pricing_errors))):.4f}")
    print(f"Misspecified Hansen-Jagannathan Distance: {hj_distance:.4f}")


main()
