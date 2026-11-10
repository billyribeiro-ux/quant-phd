"""Lab FI2-L05-1: State-space Kalman filter log-likelihood on simulated curve.

SIMULATED: formulates a 3-factor Gaussian ATSM in state-space form, runs the forward Kalman
filter on simulated monthly yield observations over 60 periods, computes prediction innovations,
evaluates the Gaussian log-likelihood, and verifies innovation whiteness.
"""

from __future__ import annotations

import numpy as np


def solve_riccati(
    tau_grid: np.ndarray,
    delta0: float,
    kappa: np.ndarray,
    sigma: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Analytical yield loadings for Gaussian ATSM."""
    n_tenors = len(tau_grid)
    a_vec = np.zeros(n_tenors, dtype=np.float64)
    b_mat = np.zeros((n_tenors, 3), dtype=np.float64)

    for m, tm in enumerate(tau_grid):
        for i in range(3):
            ki = kappa[i]
            si = sigma[i]
            b_mat[m, i] = -(1.0 - np.exp(-ki * tm)) / ki
            int_b2 = (1.0 / (ki**2)) * (
                tm - 2.0 * (1.0 - np.exp(-ki * tm)) / ki + (1.0 - np.exp(-2.0 * ki * tm)) / (2.0 * ki)
            )
            a_vec[m] += 0.5 * (si**2) * int_b2
        a_vec[m] -= delta0 * tm

    a_yield = -a_vec / tau_grid
    h_yield = -b_mat / tau_grid[:, np.newaxis]
    return a_yield, h_yield


def run_kalman(
    yields: np.ndarray,
    a_yield: np.ndarray,
    h_yield: np.ndarray,
    c_vec: np.ndarray,
    phi_mat: np.ndarray,
    q_cov: np.ndarray,
    r_cov: np.ndarray,
) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    """Execute Kalman filter recursion and return log-likelihood and diagnostics."""
    n_periods, n_maturities = yields.shape
    n_states = 3

    # Stationary initialization
    i_kron = np.eye(n_states * n_states) - np.kron(phi_mat, phi_mat)
    cov_x0 = np.linalg.solve(i_kron, q_cov.flatten()).reshape((n_states, n_states))
    cov_x0 = 0.5 * (cov_x0 + cov_x0.T)
    mean_x0 = np.linalg.solve(np.eye(n_states) - phi_mat, c_vec)

    x_curr = mean_x0.copy()
    p_curr = cov_x0.copy()

    log_likelihood = 0.0
    filtered_states = np.zeros((n_periods, n_states), dtype=np.float64)
    innovations = np.zeros((n_periods, n_maturities), dtype=np.float64)
    pricing_errors = np.zeros((n_periods, n_maturities), dtype=np.float64)

    two_pi_m = n_maturities * np.log(2.0 * np.pi)

    for t in range(n_periods):
        # 1. State prediction
        x_pred = c_vec + phi_mat @ x_curr
        p_pred = phi_mat @ p_curr @ phi_mat.T + q_cov

        # 2. Measurement prediction
        y_pred = a_yield + h_yield @ x_pred
        v_t = yields[t] - y_pred
        innovations[t] = v_t

        # 3. Innovation covariance & log-likelihood
        f_cov = h_yield @ p_pred @ h_yield.T + r_cov
        f_inv_v = np.linalg.solve(f_cov, v_t)
        _sign, logdet = np.linalg.slogdet(f_cov)

        step_ll = -0.5 * (two_pi_m + logdet + float(v_t @ f_inv_v))
        log_likelihood += step_ll

        # 4. State update
        k_gain = (np.linalg.solve(f_cov, h_yield @ p_pred.T)).T
        x_curr = x_pred + k_gain @ v_t
        p_curr = (np.eye(n_states) - k_gain @ h_yield) @ p_pred
        p_curr = 0.5 * (p_curr + p_curr.T)

        filtered_states[t] = x_curr
        pricing_errors[t] = yields[t] - (a_yield + h_yield @ x_curr)

    return log_likelihood, filtered_states, innovations, pricing_errors


def main() -> None:
    rng = np.random.default_rng(2026)
    n_periods = 60
    tenors = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0], dtype=np.float64)
    n_maturities = len(tenors)

    delta0 = 0.025
    kappa = np.array([0.06, 0.28, 0.85], dtype=np.float64)
    sigma = np.array([0.010, 0.014, 0.018], dtype=np.float64)

    a_yield, h_yield = solve_riccati(tenors, delta0, kappa, sigma)

    c_vec = np.zeros(3, dtype=np.float64)
    phi_mat = np.diag([0.98, 0.92, 0.80])
    dt = 1.0 / 12.0
    q_cov = np.diag(sigma**2 * dt)
    meas_std = 0.0005  # 5 bps
    r_cov = np.eye(n_maturities) * (meas_std**2)

    # Simulate true state trajectory and yields
    x_true = np.zeros((n_periods, 3), dtype=np.float64)
    yields = np.zeros((n_periods, n_maturities), dtype=np.float64)
    for t in range(1, n_periods):
        eta = rng.multivariate_normal(np.zeros(3), q_cov)
        x_true[t] = phi_mat @ x_true[t - 1] + eta
    for t in range(n_periods):
        noise = rng.normal(0.0, meas_std, size=n_maturities)
        yields[t] = a_yield + h_yield @ x_true[t] + noise

    ll, x_filt, innov, errors = run_kalman(yields, a_yield, h_yield, c_vec, phi_mat, q_cov, r_cov)

    rmse_bps = float(np.sqrt(np.mean(errors**2)) * 10_000.0)
    corr_factors = [round(float(np.corrcoef(x_filt[:, i], x_true[:, i])[0, 1]), 4) for i in range(3)]

    print("SIMULATED 3-Factor ATSM Kalman Filter Estimation Diagnostics:")
    print(f"  Sample length T = {n_periods} months, Maturities M = {n_maturities} tenors")
    print(f"  Total log-likelihood: {ll:.2f}")
    print(f"  Yield pricing RMSE: {rmse_bps:.2f} bps (injected noise: {meas_std * 10_000:.1f} bps)")
    print(f"  Latent factor correlations (filtered vs. true): {corr_factors}")
    print("Tenor | Mean Innov (bps) | Innov Std (bps) | Lag-1 Autocorr")
    print("-" * 55)
    for m, t in enumerate(tenors):
        v = innov[:, m]
        mean_bp = float(np.mean(v) * 10_000.0)
        std_bp = float(np.std(v, ddof=1) * 10_000.0)
        v_dm = v - np.mean(v)
        rho1 = float(np.sum(v_dm[:-1] * v_dm[1:]) / ((len(v) - 1) * np.var(v)))
        print(f" {t:5.2f}|     {mean_bp:+6.2f}     |     {std_bp:6.2f}    |     {rho1:+6.3f}")


main()
