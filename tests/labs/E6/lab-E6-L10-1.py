"""Lab E6-L10-1: Exact Gaussian likelihood via the Kalman filter vs direct multivariate density.

Simulates a stationary scalar AR(1) state-space observation sequence (SIMULATED data, seed 42).
Computes the exact log-likelihood using the sequential Kalman prediction-error decomposition.
Compares the result against the full joint multivariate normal log-density with Toeplitz
covariance, verifying exact numerical agreement to floating-point precision.
"""

from __future__ import annotations

import numpy as np


def kalman_filter_loglik(y: np.ndarray, rho: float, sigma_w: float, sigma_v: float) -> float:
    """Compute exact log-likelihood via Kalman recursion."""
    # Stationary prior variance: P_{1|0} = sigma_w^2 / (1 - rho^2)
    p_prior = (sigma_w**2) / (1.0 - rho**2)
    s_prior = 0.0
    loglik = 0.0

    for yt in y:
        nu = yt - s_prior
        f_val = p_prior + sigma_v**2
        loglik += -0.5 * (np.log(2.0 * np.pi) + np.log(f_val) + (nu**2) / f_val)

        # Update step
        k_gain = p_prior / f_val
        s_post = s_prior + k_gain * nu
        p_post = (1.0 - k_gain) * p_prior

        # Predict step for next period
        s_prior = rho * s_post
        p_prior = (rho**2) * p_post + sigma_w**2

    return float(loglik)


def direct_gaussian_loglik(y: np.ndarray, rho: float, sigma_w: float, sigma_v: float) -> float:
    """Compute exact log-likelihood via full T x T Toeplitz covariance matrix."""
    t_len = len(y)
    cov_y = np.zeros((t_len, t_len), dtype=np.float64)
    gamma_0 = (sigma_w**2) / (1.0 - rho**2)

    for i in range(t_len):
        for j in range(t_len):
            k = abs(i - j)
            cov_y[i, j] = gamma_0 * (rho**k) + (sigma_v**2 if k == 0 else 0.0)

    chol = np.linalg.cholesky(cov_y)
    log_det = 2.0 * np.sum(np.log(np.diag(chol)))
    sol_y = np.linalg.solve(chol, y)
    quad_form = np.sum(sol_y**2)
    loglik = -0.5 * (t_len * np.log(2.0 * np.pi) + log_det + quad_form)
    return float(loglik)


def main() -> None:
    # Seeded SIMULATED data generation (not market data)
    seed = 42
    rng = np.random.default_rng(seed)
    t_len = 40
    rho = 0.7
    sigma_w = 0.5
    sigma_v = 0.3

    s = np.zeros(t_len)
    w = rng.normal(0, sigma_w, t_len)
    v = rng.normal(0, sigma_v, t_len)
    s_prev = rng.normal(0, sigma_w / np.sqrt(1.0 - rho**2))
    for t in range(t_len):
        s[t] = rho * s_prev + w[t]
        s_prev = s[t]
    y = s + v

    loglik_kalman = kalman_filter_loglik(y, rho, sigma_w, sigma_v)
    loglik_direct = direct_gaussian_loglik(y, rho, sigma_w, sigma_v)
    discrepancy = abs(loglik_kalman - loglik_direct)

    print(f"DSGE State-Space Likelihood Evaluation (SIMULATED path, seed={seed}, T={t_len}):")
    print(f"Parameters: rho={rho}, sigma_w={sigma_w}, sigma_v={sigma_v}")
    print(f"  Kalman filter log-likelihood:       {loglik_kalman:14.8f}")
    print(f"  Direct multivariate log-likelihood: {loglik_direct:14.8f}")
    print(f"  Absolute discrepancy:               {discrepancy:14.2e}")


main()
