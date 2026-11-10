"""Lab FI2-project-1: 3-Factor Gaussian ATSM Kalman filter worked example (Rung 1).

SIMULATED: end-to-end implementation of the 3-factor Gaussian Affine Term-Structure Model
Kalman filter pipeline on a simulated curve of monthly yields over 60 periods across 6 tenors.
"""

from __future__ import annotations

import numpy as np


def solve_loadings(
    tau: np.ndarray,
    delta0: float,
    kappa: np.ndarray,
    sigma: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute yield intercept and factor loadings."""
    n_maturities = len(tau)
    b_mat = np.zeros((n_maturities, 3), dtype=np.float64)
    a_vec = np.zeros(n_maturities, dtype=np.float64)

    for m in range(n_maturities):
        tm = float(tau[m])
        for i in range(3):
            ki = float(kappa[i])
            si = float(sigma[i])
            b_mat[m, i] = -(1.0 - np.exp(-ki * tm)) / ki
            int_b2 = (1.0 / (ki**2)) * (
                tm - 2.0 * (1.0 - np.exp(-ki * tm)) / ki + (1.0 - np.exp(-2.0 * ki * tm)) / (2.0 * ki)
            )
            a_vec[m] += 0.5 * (si**2) * int_b2
        a_vec[m] -= delta0 * tm

    a_yield = -a_vec / tau
    h_yield = -b_mat / tau[:, np.newaxis]
    return a_yield, h_yield


def run_kalman_filter(
    yields: np.ndarray,
    tau: np.ndarray,
    delta0: float,
    kappa: np.ndarray,
    sigma: np.ndarray,
    c_vec: np.ndarray,
    phi_mat: np.ndarray,
    q_cov: np.ndarray,
    meas_std: float,
) -> tuple[float, float, np.ndarray]:
    """Run Kalman filter recursion and return log-likelihood, pricing RMSE, and filtered states."""
    n_periods, n_maturities = yields.shape
    n_states = 3

    a_yield, h_yield = solve_loadings(tau, delta0, kappa, sigma)
    r_cov = np.eye(n_maturities) * (meas_std**2)

    # Stationary covariance: V0 = Phi V0 Phi^T + Q
    i_kron = np.eye(n_states * n_states) - np.kron(phi_mat, phi_mat)
    cov_x0 = np.linalg.solve(i_kron, q_cov.flatten()).reshape((n_states, n_states))
    cov_x0 = 0.5 * (cov_x0 + cov_x0.T)
    mean_x0 = np.linalg.solve(np.eye(n_states) - phi_mat, c_vec)

    x_curr = mean_x0.copy()
    p_curr = cov_x0.copy()

    log_likelihood = 0.0
    filtered_states = np.zeros((n_periods, n_states), dtype=np.float64)
    pricing_errors = np.zeros((n_periods, n_maturities), dtype=np.float64)
    two_pi_m = n_maturities * np.log(2.0 * np.pi)

    for t in range(n_periods):
        # 1. Predict
        x_pred = c_vec + phi_mat @ x_curr
        p_pred = phi_mat @ p_curr @ phi_mat.T + q_cov

        # 2. Measurement
        y_pred = a_yield + h_yield @ x_pred
        v_t = yields[t] - y_pred

        # 3. Covariance & likelihood
        f_cov = h_yield @ p_pred @ h_yield.T + r_cov
        f_inv_v = np.linalg.solve(f_cov, v_t)
        _sign, logdet = np.linalg.slogdet(f_cov)
        log_likelihood += -0.5 * (two_pi_m + logdet + float(v_t @ f_inv_v))

        # 4. Update
        k_gain = (np.linalg.solve(f_cov, h_yield @ p_pred.T)).T
        x_curr = x_pred + k_gain @ v_t
        p_curr = (np.eye(n_states) - k_gain @ h_yield) @ p_pred
        p_curr = 0.5 * (p_curr + p_curr.T)

        filtered_states[t] = x_curr
        pricing_errors[t] = yields[t] - (a_yield + h_yield @ x_curr)

    rmse_bps = float(np.sqrt(np.mean(pricing_errors**2)) * 10_000.0)
    return float(log_likelihood), rmse_bps, filtered_states


def main() -> None:
    rng = np.random.default_rng(101)
    n_periods = 60
    tau = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0], dtype=np.float64)
    n_maturities = len(tau)

    # True ATSM parameters
    delta0 = 0.024
    kappa = np.array([0.055, 0.26, 0.82], dtype=np.float64)
    sigma = np.array([0.011, 0.015, 0.019], dtype=np.float64)

    c_vec = np.zeros(3, dtype=np.float64)
    phi_mat = np.diag([0.98, 0.92, 0.80])
    dt = 1.0 / 12.0
    q_cov = np.diag(sigma**2 * dt)
    meas_std = 0.0005  # 5 bps

    a_yield, h_yield = solve_loadings(tau, delta0, kappa, sigma)

    # Generate synthetic observations
    x_sim = np.zeros((n_periods, 3), dtype=np.float64)
    yields = np.zeros((n_periods, n_maturities), dtype=np.float64)
    for t in range(1, n_periods):
        x_sim[t] = phi_mat @ x_sim[t - 1] + rng.multivariate_normal(np.zeros(3), q_cov)
    for t in range(n_periods):
        yields[t] = a_yield + h_yield @ x_sim[t] + rng.normal(0.0, meas_std, size=n_maturities)

    ll, rmse_bps, x_filt = run_kalman_filter(yields, tau, delta0, kappa, sigma, c_vec, phi_mat, q_cov, meas_std)

    print("SIMULATED 3-Factor ATSM Kalman Pipeline (Worked Example Rung 1):")
    print(f"  Observed yield curve: {n_periods} periods x {n_maturities} tenors")
    print(f"  Short rate baseline delta0: {delta0:.4f}")
    print(f"  Mean reversion speeds kappa: {[round(float(k), 3) for k in kappa]}")
    print(f"  Volatilities sigma: {[round(float(s), 4) for s in sigma]}")
    print(f"  Log-likelihood: {ll:.2f}")
    print(f"  Pricing error RMSE: {rmse_bps:.2f} bps")
    print("Factor | True Mean | Filtered Mean | Correlation")
    print("-" * 50)
    for i in range(3):
        corr = float(np.corrcoef(x_filt[:, i], x_sim[:, i])[0, 1])
        s_m = float(np.mean(x_sim[:, i]))
        f_m = float(np.mean(x_filt[:, i]))
        print(f"   {i + 1}   |  {s_m:+.4f}   |    {f_m:+.4f}     |   {corr:.4f}")


main()
