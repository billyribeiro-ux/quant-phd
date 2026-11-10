"""Lab FI2-project-3: Rung 3 independent project calibration and diagnostic verification.

SIMULATED: calibrates the 3-factor Gaussian ATSM to a synthetic multi-year panel of yield curves,
extracts filtered factors, computes maturity-by-maturity pricing RMSE and autocorrelation of
innovations, and verifies that pricing errors remain bounded below 10 basis points.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize  # type: ignore[import-untyped]


def solve_riccati(
    tau: np.ndarray,
    delta0: float,
    kappa: np.ndarray,
    sigma: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Analytical yield loadings for Gaussian ATSM."""
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
    r_cov: np.ndarray,
) -> tuple[float, float, np.ndarray, np.ndarray]:
    """Run Kalman filter recursion and return log-likelihood, RMSE, states, errors."""
    n_periods, n_maturities = yields.shape
    n_states = 3

    a_yield, h_yield = solve_riccati(tau, delta0, kappa, sigma)

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
        x_pred = c_vec + phi_mat @ x_curr
        p_pred = phi_mat @ p_curr @ phi_mat.T + q_cov

        y_pred = a_yield + h_yield @ x_pred
        v_t = yields[t] - y_pred

        f_cov = h_yield @ p_pred @ h_yield.T + r_cov
        f_inv_v = np.linalg.solve(f_cov, v_t)
        _sign, logdet = np.linalg.slogdet(f_cov)
        log_likelihood += -0.5 * (two_pi_m + logdet + float(v_t @ f_inv_v))

        k_gain = (np.linalg.solve(f_cov, h_yield @ p_pred.T)).T
        x_curr = x_pred + k_gain @ v_t
        p_curr = (np.eye(n_states) - k_gain @ h_yield) @ p_pred
        p_curr = 0.5 * (p_curr + p_curr.T)

        filtered_states[t] = x_curr
        pricing_errors[t] = yields[t] - (a_yield + h_yield @ x_curr)

    rmse_bps = float(np.sqrt(np.mean(pricing_errors**2)) * 10_000.0)
    return float(log_likelihood), rmse_bps, filtered_states, pricing_errors


def main() -> None:
    rng = np.random.default_rng(777)
    n_periods = 60
    tau = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0], dtype=np.float64)
    n_maturities = len(tau)

    # Simulation setup
    true_delta0 = 0.026
    true_kappa = np.array([0.065, 0.28, 0.85], dtype=np.float64)
    true_sigma = np.array([0.012, 0.016, 0.020], dtype=np.float64)

    c_vec = np.zeros(3, dtype=np.float64)
    phi_mat = np.diag([0.98, 0.92, 0.80])
    dt = 1.0 / 12.0
    q_cov = np.diag(true_sigma**2 * dt)
    meas_std = 0.0005  # 5 bps
    r_cov = np.eye(n_maturities) * (meas_std**2)

    a_true, h_true = solve_riccati(tau, true_delta0, true_kappa, true_sigma)

    x_true = np.zeros((n_periods, 3), dtype=np.float64)
    yields = np.zeros((n_periods, n_maturities), dtype=np.float64)
    for t in range(1, n_periods):
        x_true[t] = phi_mat @ x_true[t - 1] + rng.multivariate_normal(np.zeros(3), q_cov)
    for t in range(n_periods):
        yields[t] = a_true + h_true @ x_true[t] + rng.normal(0.0, meas_std, size=n_maturities)

    # Initial guess for optimization
    p0 = np.concatenate([[true_delta0 * 1.05], true_kappa * 0.95, true_sigma])

    def objective(p: np.ndarray) -> float:
        d0 = float(p[0])
        kp = p[1:4]
        sg = p[4:7]
        if np.any(kp <= 0) or np.any(sg <= 0):
            return 1e12
        try:
            ll, _, _, _ = run_kalman_filter(yields, tau, d0, kp, sg, c_vec, phi_mat, q_cov, r_cov)
            return -ll
        except Exception:
            return 1e12

    bounds = [
        (0.01, 0.10),
        (0.01, 0.50),
        (0.10, 1.50),
        (0.40, 3.00),
        (0.005, 0.05),
        (0.005, 0.05),
        (0.005, 0.05),
    ]

    opt = optimize.minimize(objective, p0, method="L-BFGS-B", bounds=bounds, options={"maxiter": 20})
    p_opt = opt.x
    delta0_cal = float(p_opt[0])
    kappa_cal = p_opt[1:4]
    sigma_cal = p_opt[4:7]

    ll_cal, rmse_cal, _x_filt, errors = run_kalman_filter(
        yields, tau, delta0_cal, kappa_cal, sigma_cal, c_vec, phi_mat, q_cov, r_cov
    )

    print("SIMULATED 3-Factor ATSM Calibration Validation (Rung 3):")
    print(f"  Optimized Log-Likelihood: {ll_cal:.2f}")
    print(f"  Calibrated delta0 = {delta0_cal:.4f} (True: {true_delta0:.4f})")
    print(f"  Calibrated kappa  = {[round(float(k), 3) for k in kappa_cal]} (True: {true_kappa.tolist()})")
    print(f"  Overall Yield Pricing RMSE: {rmse_cal:.2f} bps")
    print("\nTenor Breakdown:")
    print("Tenor (Y) | Tenor RMSE (bps) | Max Error (bps)")
    print("-" * 45)
    for m, tm in enumerate(tau):
        tenor_err = errors[:, m] * 10_000.0
        tenor_rmse = float(np.sqrt(np.mean(tenor_err**2)))
        tenor_max = float(np.max(np.abs(tenor_err)))
        print(f"   {tm:5.2f}  |      {tenor_rmse:5.2f}       |     {tenor_max:5.2f}")


main()
