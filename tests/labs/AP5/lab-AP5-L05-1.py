"""Lab AP5-L05-1: Dividend-Yield Variance Decomposition and The Dog That Did Not Bark.

SIMULATED: evaluates Cochrane's (2008, 2011) variance decomposition of the dividend-price
ratio into expected return variation (b_r) and expected dividend growth variation (b_d)
to test whether 100% of price fluctuations come from discount rates.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(777)
    n_obs = 300
    rho = 0.96

    # 2-variable system: z_t = [r_t - E[r], dp_t - E[dp]]^T
    # Cochrane (2008, 2011) empirical calibration:
    # r_{t+1}  = 0.097 * dp_t + eps_r_{t+1}
    # dp_{t+1} = 0.940 * dp_t + eps_dp_{t+1}
    phi = np.array([[0.00, 0.097], [0.00, 0.940]])
    sigma_r = 0.19
    sigma_dp = 0.15
    cov_r_dp = -0.70 * sigma_r * sigma_dp
    cov_eps = np.array([[sigma_r**2, cov_r_dp], [cov_r_dp, sigma_dp**2]])

    # Simulate VAR
    eps = rng.multivariate_normal(mean=[0.0, 0.0], cov=cov_eps, size=n_obs + 1)
    z = np.zeros((n_obs + 1, 2))
    for t in range(n_obs):
        z[t + 1] = phi @ z[t] + eps[t + 1]

    # Reconstruct implied dividend growth: Delta d_{t+1} = r_{t+1} + rho * dp_{t+1} - dp_t
    r_series = z[1:, 0]
    dp_series = z[:-1, 1]
    dp_lead = z[1:, 1]
    delta_d = r_series + rho * dp_lead - dp_series

    # 1. Direct 1-period predictive regressions
    var_dp = float(np.var(dp_series, ddof=1))
    cov_r = float(np.cov(r_series, dp_series, ddof=1)[0, 1])
    beta_r_1 = cov_r / var_dp

    cov_d = float(np.cov(delta_d, dp_series, ddof=1)[0, 1])
    beta_d_1 = cov_d / var_dp

    cov_dp_lead = float(np.cov(dp_lead, dp_series, ddof=1)[0, 1])
    beta_dp_1 = cov_dp_lead / var_dp
    one_period_sum = beta_r_1 - beta_d_1 + rho * beta_dp_1

    # 2. Population VAR variance decomposition (exact infinite horizon)
    eye_2 = np.eye(2)
    long_run_r_op = np.linalg.inv(eye_2 - rho * phi) @ phi

    # Dividend operator: E_t[Delta d_{t+1}] = (e_r^T Phi + rho e_dp^T Phi - e_dp^T) z_t
    e_r = np.array([1.0, 0.0])
    e_dp = np.array([0.0, 1.0])
    long_run_d_op = (e_r @ phi + rho * e_dp @ phi - e_dp) @ np.linalg.inv(eye_2 - rho * phi)

    # Solve discrete Lyapunov equation for population covariance Gamma_0
    eye_4 = np.eye(4)
    gamma_pop = (np.linalg.inv(eye_4 - np.kron(phi, phi)) @ cov_eps.flatten()).reshape((2, 2))

    b_r_pop = float((e_r @ long_run_r_op @ gamma_pop @ e_dp) / (e_dp @ gamma_pop @ e_dp))
    b_d_pop = float((long_run_d_op @ gamma_pop @ e_dp) / (e_dp @ gamma_pop @ e_dp))
    decomp_sum = b_r_pop - b_d_pop

    print("Cochrane (2008, 2011) Dividend-Yield Variance Decomposition")
    print(f"Sample length T:             {n_obs} years")
    print(f"Discount factor rho:         {rho:.4f}")
    print(f"1-period return slope:       {beta_r_1:.4f}")
    print(f"1-period dividend slope:     {beta_d_1:.4f}")
    print(f"1-period persistence slope:  {beta_dp_1:.4f}")
    print(f"1-period identity sum:       {one_period_sum:.4f}")
    print(f"Long-run return share b_r:   {b_r_pop * 100:.2f}%")
    print(f"Long-run dividend share b_d: {b_d_pop * 100:.2f}%")
    print(f"Identity b_r - b_d:          {decomp_sum * 100:.2f}%")
    print("The dog that did not bark:   b_d approx 0 (dividend growth unforecastable)")


main()
