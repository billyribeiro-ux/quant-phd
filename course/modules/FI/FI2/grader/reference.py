"""Reference solution for FI2: Affine term-structure model calibration.

Implements:
1. Exact analytical solvers for Gaussian ATSM Riccati ODEs (Duffie-Kan 1996).
2. Yield factor loadings mapping latent factors to zero-coupon yields.
3. Unconditional state moments via discrete Lyapunov equation (Hamilton 1994).
4. Full Kalman filter recursion: prediction, measurement update, log-likelihood,
   and yield pricing error decomposition.
5. Maximum-likelihood estimation (MLE) parameter calibration routines.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy import optimize  # type: ignore[import-untyped]


def solve_riccati_ode(
    tau: np.ndarray,
    delta0: float,
    kappa: np.ndarray,
    sigma: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Solve the Duffie-Kan Riccati ODE system for a 3-factor Gaussian ATSM.

    The model under Q has short-rate r_t = delta0 + sum_i X_{t,i} and factor SDE
    dX_t = -diag(kappa) X_t dt + diag(sigma) dW_t^Q.

    Bond prices satisfy P(t, tau) = exp(A(tau) + B(tau)^T X_t) with ODEs:
        dB_i/dtau = -kappa_i B_i - 1,              B_i(0) = 0
        dA/dtau   = -delta0 + 0.5 sum_i sigma_i^2 B_i(tau)^2, A(0) = 0

    Parameters
    ----------
    tau : np.ndarray
        Array of maturities in years, shape (M,).
    delta0 : float
        Instantaneous short-rate baseline intercept.
    kappa : np.ndarray
        Mean-reversion vector of shape (3,).
    sigma : np.ndarray
        Factor volatility vector of shape (3,).

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        (A, B) where A has shape (M,) and B has shape (M, 3).
    """
    tau = np.asarray(tau, dtype=np.float64)
    kappa = np.asarray(kappa, dtype=np.float64)
    sigma = np.asarray(sigma, dtype=np.float64)

    n_maturities = len(tau)
    b_mat = np.zeros((n_maturities, 3), dtype=np.float64)
    a_vec = np.zeros(n_maturities, dtype=np.float64)

    for m in range(n_maturities):
        tm = float(tau[m])
        # Check boundary condition at tau = 0
        if abs(tm) < 1e-12:
            a_vec[m] = 0.0
            b_mat[m, :] = 0.0
            continue

        for i in range(3):
            ki = float(kappa[i])
            si = float(sigma[i])
            # B_i(tau) = -(1 - exp(-kappa_i * tau)) / kappa_i
            b_mat[m, i] = -(1.0 - np.exp(-ki * tm)) / ki

            # Integral of B_i(s)^2 from 0 to tm
            int_b2 = (1.0 / (ki**2)) * (
                tm - 2.0 * (1.0 - np.exp(-ki * tm)) / ki + (1.0 - np.exp(-2.0 * ki * tm)) / (2.0 * ki)
            )
            a_vec[m] += 0.5 * (si**2) * int_b2

        a_vec[m] -= delta0 * tm

    return a_vec, b_mat


def yield_loadings(
    tau: np.ndarray,
    delta0: float,
    kappa: np.ndarray,
    sigma: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute yield intercept a(tau) and factor loadings H(tau).

    Yields are y(t, tau) = -ln(P(t, tau)) / tau = a(tau) + H(tau) * X_t
    where a(tau) = -A(tau) / tau and H(tau) = -B(tau) / tau.

    Parameters
    ----------
    tau : np.ndarray
        Array of maturities in years, shape (M,).
    delta0 : float
        Instantaneous short-rate intercept.
    kappa : np.ndarray
        Mean-reversion vector of shape (3,).
    sigma : np.ndarray
        Factor volatility vector of shape (3,).

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        (a, H) where a has shape (M,) and H has shape (M, 3).
    """
    tau = np.asarray(tau, dtype=np.float64)
    a_vec, b_mat = solve_riccati_ode(tau, delta0, kappa, sigma)

    # Handle tau -> 0 limit cleanly
    safe_tau = np.where(tau == 0.0, 1.0, tau)
    a_yield = -a_vec / safe_tau
    h_yield = -b_mat / safe_tau[:, np.newaxis]

    # At tau = 0: a(0) = delta0, H(0) = [1.0, 1.0, 1.0]
    zero_mask = tau == 0.0
    if np.any(zero_mask):
        a_yield[zero_mask] = delta0
        h_yield[zero_mask, :] = 1.0

    return a_yield, h_yield


def compute_unconditional_moments(
    c: np.ndarray,
    phi: np.ndarray,
    q_cov: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute unconditional mean and covariance of discrete VAR(1) state process.

    X_{t+1} = c + Phi * X_t + eta_{t+1},  eta ~ N(0, Q)
    Mean: bar{X} = (I - Phi)^{-1} c
    Covariance: vec(V0) = (I - Phi (x) Phi)^{-1} vec(Q)

    Parameters
    ----------
    c : np.ndarray
        State transition intercept vector of shape (K,).
    phi : np.ndarray
        Transition autoregression matrix of shape (K, K).
    q_cov : np.ndarray
        Transition shock covariance matrix of shape (K, K).

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        (mean_X, cov_X) of shapes (K,) and (K, K).
    """
    c = np.asarray(c, dtype=np.float64)
    phi = np.asarray(phi, dtype=np.float64)
    q_cov = np.asarray(q_cov, dtype=np.float64)

    n_dim = len(c)
    i_mat = np.eye(n_dim, dtype=np.float64)

    mean_x = np.linalg.solve(i_mat - phi, c)

    i_kron = np.eye(n_dim * n_dim, dtype=np.float64) - np.kron(phi, phi)
    cov_vec = np.linalg.solve(i_kron, q_cov.flatten())
    cov_x = cov_vec.reshape((n_dim, n_dim))
    # Guarantee exact symmetry
    cov_x = 0.5 * (cov_x + cov_x.T)

    return mean_x, cov_x


def kalman_filter(
    yields: np.ndarray,
    tau: np.ndarray,
    delta0: float,
    kappa: np.ndarray,
    sigma: np.ndarray,
    c: np.ndarray,
    phi: np.ndarray,
    q_cov: np.ndarray,
    r_diag: np.ndarray,
) -> dict[str, Any]:
    """Run Kalman filter on zero-coupon yields to evaluate log-likelihood and filtered states.

    Parameters
    ----------
    yields : np.ndarray
        Observed yield matrix of shape (T, M).
    tau : np.ndarray
        Maturities in years of shape (M,).
    delta0 : float
        Short-rate baseline.
    kappa : np.ndarray
        Mean-reversion vector of shape (3,).
    sigma : np.ndarray
        Volatility vector of shape (3,).
    c : np.ndarray
        State intercept of shape (3,).
    phi : np.ndarray
        State transition matrix of shape (3, 3).
    q_cov : np.ndarray
        State transition covariance of shape (3, 3).
    r_diag : np.ndarray
        Measurement error variance vector of shape (M,).

    Returns
    -------
    dict[str, Any]
        Dictionary with keys:
        - 'log_likelihood': float
        - 'filtered_states': np.ndarray of shape (T, 3)
        - 'predicted_yields': np.ndarray of shape (T, M)
        - 'innovations': np.ndarray of shape (T, M)
        - 'pricing_errors': np.ndarray of shape (T, M)
        - 'rmse_bps': float (root mean square pricing error in basis points)
    """
    yields = np.asarray(yields, dtype=np.float64)
    tau = np.asarray(tau, dtype=np.float64)
    kappa = np.asarray(kappa, dtype=np.float64)
    sigma = np.asarray(sigma, dtype=np.float64)
    c = np.asarray(c, dtype=np.float64)
    phi = np.asarray(phi, dtype=np.float64)
    q_cov = np.asarray(q_cov, dtype=np.float64)
    r_diag = np.asarray(r_diag, dtype=np.float64)

    n_periods, n_maturities = yields.shape
    n_states = 3

    # Yield measurement equation: y_t = a + H * X_t + v_t
    a_vec, h_mat = yield_loadings(tau, delta0, kappa, sigma)
    r_cov = np.diag(r_diag)

    # Initial state moments from stationary distribution
    mean_x0, cov_x0 = compute_unconditional_moments(c, phi, q_cov)

    x_curr = mean_x0.copy()
    p_curr = cov_x0.copy()

    log_likelihood = 0.0
    filtered_states = np.zeros((n_periods, n_states), dtype=np.float64)
    predicted_yields = np.zeros((n_periods, n_maturities), dtype=np.float64)
    innovations = np.zeros((n_periods, n_maturities), dtype=np.float64)
    pricing_errors = np.zeros((n_periods, n_maturities), dtype=np.float64)

    two_pi_m = n_maturities * np.log(2.0 * np.pi)

    for t in range(n_periods):
        # 1. State prediction step
        x_pred = c + phi @ x_curr
        p_pred = phi @ p_curr @ phi.T + q_cov

        # 2. Measurement prediction step
        y_pred = a_vec + h_mat @ x_pred
        predicted_yields[t] = y_pred

        # 3. Innovation
        v_t = yields[t] - y_pred
        innovations[t] = v_t

        # 4. Innovation covariance
        f_cov = h_mat @ p_pred @ h_mat.T + r_cov
        f_inv_v = np.linalg.solve(f_cov, v_t)
        sign, logdet = np.linalg.slogdet(f_cov)
        if sign <= 0:
            logdet = 1e6

        # Contribution to log-likelihood
        quad_form = float(v_t @ f_inv_v)
        step_ll = -0.5 * (two_pi_m + logdet + quad_form)
        log_likelihood += step_ll

        # 5. Kalman gain
        k_gain = (np.linalg.solve(f_cov, h_mat @ p_pred.T)).T

        # 6. State measurement update
        x_curr = x_pred + k_gain @ v_t
        p_curr = (np.eye(n_states, dtype=np.float64) - k_gain @ h_mat) @ p_pred
        p_curr = 0.5 * (p_curr + p_curr.T)

        filtered_states[t] = x_curr

        # Pricing error with filtered state: y_t - (a + H * x_{t|t})
        fitted_y = a_vec + h_mat @ x_curr
        pricing_errors[t] = yields[t] - fitted_y

    # Pricing RMSE in basis points (1 bp = 0.0001 = 1e-4)
    mse = float(np.mean(pricing_errors**2))
    rmse_bps = float(np.sqrt(mse) * 10_000.0)

    return {
        "log_likelihood": float(log_likelihood),
        "filtered_states": filtered_states,
        "predicted_yields": predicted_yields,
        "innovations": innovations,
        "pricing_errors": pricing_errors,
        "rmse_bps": rmse_bps,
    }


def kalman_log_likelihood(
    params: np.ndarray,
    yields: np.ndarray,
    tau: np.ndarray,
    c: np.ndarray,
    phi: np.ndarray,
    q_cov: np.ndarray,
    r_diag: np.ndarray,
) -> float:
    """Evaluate Kalman log-likelihood for parameter vector.

    params : [delta0, kappa1, kappa2, kappa3, sigma1, sigma2, sigma3]
    """
    delta0 = float(params[0])
    kappa = np.asarray(params[1:4], dtype=np.float64)
    sigma = np.asarray(params[4:7], dtype=np.float64)

    # Penalize negative or non-ordered kappa
    if np.any(kappa <= 0.0) or np.any(sigma <= 0.0):
        return -1e12

    try:
        res = kalman_filter(yields, tau, delta0, kappa, sigma, c, phi, q_cov, r_diag)
        ll = float(res["log_likelihood"])
        if np.isnan(ll):
            return -1e12
        return ll
    except np.linalg.LinAlgError, ValueError:
        return -1e12


def calibrate_mle(
    yields: np.ndarray,
    tau: np.ndarray,
    initial_params: np.ndarray | None = None,
) -> dict[str, Any]:
    """Calibrate 3-factor Gaussian ATSM parameters by Kalman-filter MLE.

    Parameters
    ----------
    yields : np.ndarray
        Observed yield curves of shape (T, M).
    tau : np.ndarray
        Maturities in years of shape (M,).
    initial_params : np.ndarray | None
        Initial guess [delta0, kappa1, kappa2, kappa3, sigma1, sigma2, sigma3].

    Returns
    -------
    dict[str, Any]
        Dictionary of calibrated parameters, log-likelihood, and pricing RMSE.
    """
    yields = np.asarray(yields, dtype=np.float64)
    tau = np.asarray(tau, dtype=np.float64)
    _n_periods, n_maturities = yields.shape

    # Default initial parameters if not provided
    if initial_params is None:
        delta0_init = float(yields[:, 0].mean())
        kappa_init = np.array([0.05, 0.25, 0.80], dtype=np.float64)
        sigma_init = np.array([0.010, 0.015, 0.020], dtype=np.float64)
        p0 = np.concatenate([[delta0_init], kappa_init, sigma_init])
    else:
        p0 = np.asarray(initial_params, dtype=np.float64)

    # Fixed physical state dynamics for benchmark calibration
    c_vec = np.zeros(3, dtype=np.float64)
    phi_mat = np.diag([0.98, 0.92, 0.80])
    dt = 1.0 / 12.0
    sigma_p = p0[4:7]
    q_cov = np.diag(sigma_p**2 * dt)
    meas_std = 0.0005  # 5 bps
    r_diag = np.full(n_maturities, meas_std**2, dtype=np.float64)

    def neg_ll(p: np.ndarray) -> float:
        return -kalman_log_likelihood(p, yields, tau, c_vec, phi_mat, q_cov, r_diag)

    # Bounded optimization
    bounds = [
        (0.001, 0.15),  # delta0
        (0.01, 0.50),  # kappa1
        (0.10, 1.50),  # kappa2
        (0.40, 3.00),  # kappa3
        (0.002, 0.050),  # sigma1
        (0.002, 0.050),  # sigma2
        (0.002, 0.050),  # sigma3
    ]

    opt_res = optimize.minimize(
        neg_ll,
        p0,
        method="L-BFGS-B",
        bounds=bounds,
        options={"maxiter": 25, "ftol": 1e-4},
    )

    p_opt = opt_res.x
    delta0_opt = float(p_opt[0])
    kappa_opt = p_opt[1:4]
    sigma_opt = p_opt[4:7]

    kf_res = kalman_filter(yields, tau, delta0_opt, kappa_opt, sigma_opt, c_vec, phi_mat, q_cov, r_diag)

    return {
        "delta0": delta0_opt,
        "kappa": kappa_opt,
        "sigma": sigma_opt,
        "log_likelihood": kf_res["log_likelihood"],
        "rmse_bps": kf_res["rmse_bps"],
        "filtered_states": kf_res["filtered_states"],
        "pricing_errors": kf_res["pricing_errors"],
    }
