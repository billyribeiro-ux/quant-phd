"""Reference implementation for Module AP5: Present Value & Return Predictability.

Implements Campbell-Shiller VAR estimation, return news decomposition,
dividend-yield variance decomposition, Stambaugh bias correction,
and recursive out-of-sample predictability evaluation.
"""

from __future__ import annotations

import numpy as np


def estimate_var(z: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Estimate a first-order VAR(1): z_{t+1} = c + Phi z_t + eps_{t+1}.

    Parameters
    ----------
    z : np.ndarray
        2D array of shape (T, K) containing multivariate time series.

    Returns
    -------
    phi : np.ndarray
        (K, K) transition / companion matrix.
    c : np.ndarray
        (K,) intercept vector.
    sigma : np.ndarray
        (K, K) residual covariance matrix with unbiased denominator (T - K - 1).
    """
    if z.ndim != 2:
        raise ValueError(f"z must be 2-dimensional, got {z.ndim}")
    n_obs, k_vars = z.shape
    if k_vars < 2:
        raise ValueError(f"z must have at least 2 variables, got {k_vars}")
    if n_obs < k_vars + 5:
        raise ValueError(f"Insufficient observations {n_obs} for {k_vars} variables")

    z_lag = z[:-1]
    z_lead = z[1:]
    t_est = n_obs - 1

    # Design matrix with constant: [1, z_lag]
    x_mat = np.column_stack([np.ones(t_est, dtype=np.float64), z_lag])
    b_mat = np.linalg.lstsq(x_mat, z_lead, rcond=None)[0]

    c = b_mat[0]
    phi = b_mat[1:].T
    residuals = z_lead - x_mat @ b_mat
    deg_free = t_est - k_vars - 1
    if deg_free <= 0:
        deg_free = 1
    sigma = (residuals.T @ residuals) / deg_free

    return phi, c, sigma


def campbell_shiller_news(phi: np.ndarray, residuals: np.ndarray, rho: float = 0.96) -> tuple[np.ndarray, np.ndarray]:
    """Compute Campbell-Shiller cash-flow news and discount-rate news.

    Parameters
    ----------
    phi : np.ndarray
        (K, K) VAR transition matrix.
    residuals : np.ndarray
        (T-1, K) array of VAR innovations.
    rho : float
        Discount factor parameter in (0, 1).

    Returns
    -------
    n_cf : np.ndarray
        (T-1,) array of cash-flow news.
    n_dr : np.ndarray
        (T-1,) array of discount-rate news.
    """
    if not (0.0 < rho < 1.0):
        raise ValueError(f"rho must lie in (0, 1), got {rho}")
    if phi.ndim != 2 or phi.shape[0] != phi.shape[1]:
        raise ValueError("phi must be a square matrix")
    k_vars = phi.shape[0]
    if residuals.ndim != 2 or residuals.shape[1] != k_vars:
        raise ValueError(f"residuals shape {residuals.shape} does not match phi dimension {k_vars}")

    eye_k = np.eye(k_vars, dtype=np.float64)
    inv_mat = np.linalg.inv(eye_k - rho * phi)

    e_r = np.zeros(k_vars, dtype=np.float64)
    e_r[0] = 1.0

    # lambda_dr = e_r^T rho Phi (I - rho Phi)^(-1)
    lambda_dr = e_r @ (rho * phi) @ inv_mat
    # lambda_cf = e_r^T (I - rho Phi)^(-1)
    lambda_cf = e_r @ inv_mat

    n_dr = residuals @ lambda_dr
    n_cf = residuals @ lambda_cf

    return n_cf, n_dr


def decompose_return_variance(n_cf: np.ndarray, n_dr: np.ndarray) -> dict[str, float]:
    """Decompose return innovation variance into cash-flow and discount-rate news shares.

    Parameters
    ----------
    n_cf : np.ndarray
        (T,) array of cash-flow news.
    n_dr : np.ndarray
        (T,) array of discount-rate news.

    Returns
    -------
    dict with var_eta, var_cf, var_dr, cov_cf_dr, share_dr, share_cf, share_cov.
    """
    if len(n_cf) != len(n_dr):
        raise ValueError("n_cf and n_dr must have identical length")
    if len(n_cf) < 3:
        raise ValueError("Need at least 3 observations for variance decomposition")

    eta = n_cf - n_dr
    var_eta = float(np.var(eta, ddof=1))
    var_cf = float(np.var(n_cf, ddof=1))
    var_dr = float(np.var(n_dr, ddof=1))
    cov_cf_dr = float(np.cov(n_cf, n_dr, ddof=1)[0, 1])

    if var_eta <= 1e-14:
        share_dr = 0.0
        share_cf = 0.0
        share_cov = 0.0
    else:
        share_dr = var_dr / var_eta
        share_cf = var_cf / var_eta
        share_cov = -2.0 * cov_cf_dr / var_eta

    return {
        "var_eta": var_eta,
        "var_cf": var_cf,
        "var_dr": var_dr,
        "cov_cf_dr": cov_cf_dr,
        "share_dr": share_dr,
        "share_cf": share_cf,
        "share_cov": share_cov,
    }


def dividend_yield_variance_decomposition(phi: np.ndarray, sigma: np.ndarray, rho: float = 0.96) -> dict[str, float]:
    """Decompose dividend-yield variance into long-horizon return and dividend components.

    Solves the population Lyapunov equation: Gamma_0 = Phi Gamma_0 Phi^T + Sigma,
    and computes long-horizon shares:
        b_r = [e_r^T (I - rho Phi)^(-1) Phi Gamma_0 e_dp] / [e_dp^T Gamma_0 e_dp]
        b_d = [(e_r^T Phi + rho e_dp^T Phi - e_dp^T)(I - rho Phi)^(-1) Gamma_0 e_dp] / [e_dp^T Gamma_0 e_dp]

    Parameters
    ----------
    phi : np.ndarray
        (K, K) VAR transition matrix.
    sigma : np.ndarray
        (K, K) residual covariance matrix.
    rho : float
        Discount parameter in (0, 1).

    Returns
    -------
    dict with b_r, b_d, identity_gap, share_discount_rate.
    """
    if not (0.0 < rho < 1.0):
        raise ValueError(f"rho must lie in (0, 1), got {rho}")
    k_vars = phi.shape[0]
    if k_vars != 2:
        raise ValueError("Standard present-value variance decomposition requires K=2 state vector [r, dp]")

    # Check stability
    eigvals = np.linalg.eigvals(phi)
    if np.any(np.abs(eigvals) >= 1.0):
        raise ValueError("VAR transition matrix Phi must be stationary (eigenvalues strictly inside unit circle)")

    eye_k = np.eye(k_vars, dtype=np.float64)
    inv_mat = np.linalg.inv(eye_k - rho * phi)

    # Solve discrete Lyapunov equation: vec(Gamma_0) = (I - Phi kron Phi)^(-1) vec(Sigma)
    eye_k2 = np.eye(k_vars * k_vars, dtype=np.float64)
    gamma_vec = np.linalg.inv(eye_k2 - np.kron(phi, phi)) @ sigma.flatten()
    gamma_0 = gamma_vec.reshape((k_vars, k_vars))

    e_r = np.array([1.0, 0.0], dtype=np.float64)
    e_dp = np.array([0.0, 1.0], dtype=np.float64)

    long_run_r_op = inv_mat @ phi
    long_run_d_op = (e_r @ phi + rho * e_dp @ phi - e_dp) @ inv_mat

    denom = float(e_dp @ gamma_0 @ e_dp)
    if abs(denom) <= 1e-14:
        raise ValueError("Degenerate dividend-price ratio variance")

    b_r = float((e_r @ long_run_r_op @ gamma_0 @ e_dp) / denom)
    b_d = float((long_run_d_op @ gamma_0 @ e_dp) / denom)
    identity_gap = abs(1.0 - (b_r - b_d))

    return {
        "b_r": b_r,
        "b_d": b_d,
        "identity_gap": identity_gap,
        "share_discount_rate": b_r,
    }


def predictive_regression(x: np.ndarray, y: np.ndarray, max_lags: int = 4) -> dict[str, float]:
    """Estimate predictive regression y_{t+1} = alpha + beta * x_t + eps_{t+1}.

    Parameters
    ----------
    x : np.ndarray
        (T,) predictor series.
    y : np.ndarray
        (T,) predicted return series.
    max_lags : int
        Lags for Newey-West standard error calculation.

    Returns
    -------
    dict with alpha, beta, r2, se_ols, se_nw, t_stat.
    """
    if len(x) != len(y):
        raise ValueError(f"Length mismatch: x has {len(x)}, y has {len(y)}")
    n_obs = len(x)
    if n_obs < 5:
        raise ValueError("Need at least 5 observations for predictive regression")

    x_m = float(np.mean(x))
    y_m = float(np.mean(y))
    x_dev = x - x_m
    y_dev = y - y_m

    sxx = float(np.sum(x_dev**2))
    if sxx <= 1e-14:
        raise ValueError("Predictor x has zero variance")

    sxy = float(np.sum(x_dev * y_dev))
    syy = float(np.sum(y_dev**2))

    beta = sxy / sxx
    alpha = y_m - beta * x_m
    r2 = (sxy**2) / (sxx * syy) if syy > 1e-14 else 0.0

    residuals = y - (alpha + beta * x)
    sigma2_e = float(np.sum(residuals**2) / (n_obs - 2))
    se_ols = float(np.sqrt(sigma2_e / sxx))

    # Newey-West HAC standard error
    u = x_dev * residuals
    omega = float(np.sum(u**2))
    for j in range(1, max_lags + 1):
        weight = 1.0 - j / (max_lags + 1.0)
        gamma = float(np.sum(u[j:] * u[:-j]))
        omega += 2.0 * weight * gamma

    var_nw = omega / (sxx**2)
    se_nw = float(np.sqrt(max(1e-14, var_nw)))
    t_stat = beta / se_nw

    return {
        "alpha": alpha,
        "beta": beta,
        "r2": r2,
        "se_ols": se_ols,
        "se_nw": se_nw,
        "t_stat": t_stat,
    }


def stambaugh_bias(phi_x: float, sigma_uv: float, sigma_v2: float, n_obs: int) -> float:
    """Calculate the first-order analytical Stambaugh (1999) small-sample bias.

    Bias = - (sigma_uv / sigma_v^2) * (1 + 3 * phi_x) / n_obs.
    """
    if sigma_v2 <= 0.0:
        raise ValueError("Predictor innovation variance sigma_v2 must be strictly positive")
    if n_obs <= 0:
        raise ValueError("Sample size n_obs must be strictly positive")

    return float(-(sigma_uv / sigma_v2) * ((1.0 + 3.0 * phi_x) / n_obs))


def out_of_sample_r2(y: np.ndarray, x: np.ndarray, n_init: int = 60, constrained: bool = False) -> float:
    """Compute recursive out-of-sample R^2 against prevailing historical mean benchmark.

    Parameters
    ----------
    y : np.ndarray
        (T,) target returns.
    x : np.ndarray
        (T,) predictor variable.
    n_init : int
        Burn-in window before forecasting starts.
    constrained : bool
        If True, applies Campbell & Thompson (2008) economic restrictions
        (beta >= 0 and predicted return >= 0).
    """
    if len(y) != len(x):
        raise ValueError("y and x must have equal length")
    n_obs = len(y)
    if n_init < 5 or n_init >= n_obs:
        raise ValueError(f"n_init {n_init} must be in [5, {n_obs - 1}]")

    bench_errors = []
    model_errors = []

    for t in range(n_init, n_obs):
        y_hist = y[:t]
        x_hist = x[:t]

        # 1. Benchmark: prevailing historical mean
        y_bench = float(np.mean(y_hist))
        bench_errors.append(y[t] - y_bench)

        # 2. Predictive regression model
        x_m = float(np.mean(x_hist))
        y_m = float(np.mean(y_hist))
        sxx = float(np.sum((x_hist - x_m) ** 2))
        sxy = float(np.sum((x_hist - x_m) * (y_hist - y_m)))
        b_hat = sxy / sxx if sxx > 1e-14 else 0.0

        if constrained:
            b_hat = max(0.0, b_hat)

        a_hat = y_m - b_hat * x_m
        y_pred = a_hat + b_hat * x[t]

        if constrained:
            y_pred = max(0.0, y_pred)

        model_errors.append(y[t] - y_pred)

    mse_bench = float(np.mean(np.array(bench_errors) ** 2))
    mse_model = float(np.mean(np.array(model_errors) ** 2))

    if mse_bench <= 1e-14:
        return 0.0

    return float(1.0 - (mse_model / mse_bench))
