"""Student error: uses unweighted identity matrix in step 2 instead of inverting spectral density matrix S."""

from __future__ import annotations

from typing import Any, cast

import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaincc


def _validate_inputs(
    c_growth: np.ndarray,
    gross_returns: np.ndarray,
    instruments: np.ndarray | None = None,
) -> tuple[int, int, int]:
    """Validate shapes, positivity, and finiteness of asset pricing inputs."""
    if c_growth.ndim != 1:
        raise ValueError("c_growth must be a 1-dimensional array of shape (T,)")
    if gross_returns.ndim != 2:
        raise ValueError("gross_returns must be a 2-dimensional array of shape (T, N)")

    t_periods, n_assets = gross_returns.shape
    if len(c_growth) != t_periods:
        raise ValueError(
            f"Length mismatch: c_growth has length {len(c_growth)}, but gross_returns has {t_periods} rows"
        )

    if not np.all(np.isfinite(c_growth)) or not np.all(np.isfinite(gross_returns)):
        raise ValueError("Inputs must contain only finite real numbers (no NaNs or Infs)")

    if np.any(c_growth <= 0.0):
        raise ValueError("c_growth must be strictly positive (consumption growth ratio)")
    if np.any(gross_returns <= 0.0):
        raise ValueError("gross_returns must be strictly positive (gross returns)")

    l_instruments = 0
    if instruments is not None:
        if instruments.ndim != 2:
            raise ValueError("instruments must be a 2-dimensional array of shape (T, L)")
        if instruments.shape[0] != t_periods:
            raise ValueError(f"Length mismatch: instruments has {instruments.shape[0]} rows, expected {t_periods}")
        if not np.all(np.isfinite(instruments)):
            raise ValueError("instruments must contain only finite numbers")
        l_instruments = instruments.shape[1]

    return t_periods, n_assets, l_instruments


def euler_residuals(
    params: tuple[float, float],
    c_growth: np.ndarray,
    gross_returns: np.ndarray,
) -> np.ndarray:
    """Compute nonlinear consumption Euler equation pricing errors.

    u_{t+1, i}(beta, gamma) = beta * (c_{t+1} / c_t)^{-gamma} * R_{i, t+1} - 1.0

    Parameters:
        params: (beta, gamma) where beta is subjective discount factor and gamma is CRRA risk aversion.
        c_growth: (T,) array of consumption growth ratios c_{t+1}/c_t.
        gross_returns: (T, N) array of gross returns for N assets.

    Returns:
        (T, N) ndarray of pricing errors.
    """
    beta, gamma = params
    if not (np.isfinite(beta) and np.isfinite(gamma)):
        raise ValueError("Parameters (beta, gamma) must be finite")
    if beta <= 0.0:
        raise ValueError("Subjective discount factor beta must be strictly positive")

    _validate_inputs(c_growth, gross_returns)

    # SDF: M_{t+1} = beta * (c_{t+1}/c_t)^(-gamma)
    sdf = beta * (c_growth ** (-gamma))
    # Euler pricing errors: u_{t, i} = M_t * R_{t, i} - 1.0
    return cast(np.ndarray, sdf[:, None] * gross_returns - 1.0)


def sample_moments(
    params: tuple[float, float],
    c_growth: np.ndarray,
    gross_returns: np.ndarray,
    instruments: np.ndarray,
) -> np.ndarray:
    """Compute empirical moment conditions g_T(beta, gamma) = (1/T) sum_t (u_t (x) z_t).

    Parameters:
        params: (beta, gamma) tuple.
        c_growth: (T,) array of consumption growth ratios.
        gross_returns: (T, N) array of gross returns.
        instruments: (T, L) array of predetermined instruments known at time t.

    Returns:
        (N * L,) ndarray of sample orthogonality conditions.
    """
    t_periods, n_assets, l_instruments = _validate_inputs(c_growth, gross_returns, instruments)
    u = euler_residuals(params, c_growth, gross_returns)

    # h_t is Kronecker product u_t (x) z_t of dimension (N * L)
    h = np.empty((t_periods, n_assets * l_instruments), dtype=np.float64)
    for i in range(n_assets):
        for j in range(l_instruments):
            h[:, i * l_instruments + j] = u[:, i] * instruments[:, j]

    return cast(np.ndarray, np.mean(h, axis=0))


def spectral_covariance(residuals_kron: np.ndarray) -> np.ndarray:
    """Compute the zero-lag spectral covariance matrix S_T = (1/T) * H^T * H.

    Parameters:
        residuals_kron: (T, K) array of instrumented moment residuals h_t.

    Returns:
        (K, K) ndarray spectral density matrix.
    """
    if residuals_kron.ndim != 2:
        raise ValueError("residuals_kron must be a 2D array of shape (T, K)")
    t_periods = residuals_kron.shape[0]
    if t_periods == 0:
        raise ValueError("residuals_kron cannot be empty")
    return cast(np.ndarray, (residuals_kron.T @ residuals_kron) / float(t_periods))


def gmm_objective(
    params: tuple[float, float],
    c_growth: np.ndarray,
    gross_returns: np.ndarray,
    instruments: np.ndarray,
    weight_matrix: np.ndarray,
) -> float:
    """Compute the quadratic GMM criterion J_T(theta) = g_T(theta)^T * W * g_T(theta).

    Parameters:
        params: (beta, gamma) tuple.
        c_growth: (T,) array of consumption growth ratios.
        gross_returns: (T, N) array of gross returns.
        instruments: (T, L) array of instruments.
        weight_matrix: (N*L, N*L) symmetric positive semi-definite weighting matrix.

    Returns:
        Scalar GMM objective value.
    """
    g = sample_moments(params, c_growth, gross_returns, instruments)
    k = len(g)
    if weight_matrix.shape != (k, k):
        raise ValueError(f"weight_matrix must have shape ({k}, {k}), got {weight_matrix.shape}")
    return float(g.T @ weight_matrix @ g)


def gmm_gradient(
    params: tuple[float, float],
    c_growth: np.ndarray,
    gross_returns: np.ndarray,
    instruments: np.ndarray,
    weight_matrix: np.ndarray,
) -> np.ndarray:
    """Compute the analytical gradient of the GMM objective: nabla J_T = 2 * G_T^T * W * g_T.

    G_T = d g_T / d theta^T is the (K x 2) Jacobian matrix of moment conditions.
    """
    beta, gamma = params
    _t_periods, n_assets, l_instruments = _validate_inputs(c_growth, gross_returns, instruments)
    k = n_assets * l_instruments

    m = beta * (c_growth ** (-gamma))
    log_c = np.log(c_growth)

    # Derivatives of u_{t, i} with respect to beta and gamma
    # du / dbeta = c^(-gamma) * R
    # du / dgamma = -beta * c^(-gamma) * log(c) * R = -m * log(c) * R
    du_dbeta = (c_growth[:, None] ** (-gamma)) * gross_returns  # (T, N)
    du_dgamma = -m[:, None] * log_c[:, None] * gross_returns  # (T, N)

    jacobian = np.empty((k, 2), dtype=np.float64)
    for i in range(n_assets):
        for j in range(l_instruments):
            idx = i * l_instruments + j
            jacobian[idx, 0] = np.mean(du_dbeta[:, i] * instruments[:, j])
            jacobian[idx, 1] = np.mean(du_dgamma[:, i] * instruments[:, j])

    g = sample_moments(params, c_growth, gross_returns, instruments)
    return cast(np.ndarray, 2.0 * (jacobian.T @ weight_matrix @ g))


def estimate_gmm(
    c_growth: np.ndarray,
    gross_returns: np.ndarray,
    instruments: np.ndarray,
    initial_params: tuple[float, float] = (0.95, 2.0),
    two_step: bool = True,
) -> dict[str, Any]:
    """Perform two-step nonlinear GMM estimation of Hansen & Singleton (1982).

    Parameters:
        c_growth: (T,) array of consumption growth ratios.
        gross_returns: (T, N) array of gross asset returns.
        instruments: (T, L) array of predetermined instruments.
        initial_params: initial guess (beta_0, gamma_0).
        two_step: whether to perform the efficient second step using inverse spectral matrix.

    Returns:
        dict containing:
            beta: estimated subjective discount factor
            gamma: estimated relative risk aversion
            j_stat: Hansen J-test statistic T * g_T^T * S_T^(-1) * g_T
            j_pvalue: p-value from chi-square distribution with df = (N*L - 2)
            df: degrees of freedom (N*L - 2)
            standard_errors: asymptotic standard errors (se_beta, se_gamma)
            step1_params: first-step parameter estimates (beta_1, gamma_1)
    """
    t_periods, n_assets, l_instruments = _validate_inputs(c_growth, gross_returns, instruments)
    k = n_assets * l_instruments
    bounds = [(0.40, 1.60), (-10.0, 20.0)]

    # Step 1: Identity weighting matrix
    w1 = np.eye(k, dtype=np.float64)

    def obj_step1(p: np.ndarray) -> float:
        return gmm_objective((float(p[0]), float(p[1])), c_growth, gross_returns, instruments, w1)

    def grad_step1(p: np.ndarray) -> np.ndarray:
        return gmm_gradient((float(p[0]), float(p[1])), c_growth, gross_returns, instruments, w1)

    res1 = minimize(
        obj_step1,
        np.array([initial_params[0], initial_params[1]], dtype=np.float64),
        jac=grad_step1,
        method="L-BFGS-B",
        bounds=bounds,
    )
    p1 = (float(res1.x[0]), float(res1.x[1]))

    if not two_step:
        return {"beta": p1[0], "gamma": p1[1], "step1_params": p1}

    # Step 2: Optimal weighting matrix W2 = S_T^(-1)
    u1 = euler_residuals(p1, c_growth, gross_returns)
    h1 = np.empty((t_periods, k), dtype=np.float64)
    for i in range(n_assets):
        for j in range(l_instruments):
            h1[:, i * l_instruments + j] = u1[:, i] * instruments[:, j]

    _s_matrix = spectral_covariance(h1)
    w2 = np.eye(k, dtype=np.float64)

    def obj_step2(p: np.ndarray) -> float:
        return gmm_objective((float(p[0]), float(p[1])), c_growth, gross_returns, instruments, w2)

    def grad_step2(p: np.ndarray) -> np.ndarray:
        return gmm_gradient((float(p[0]), float(p[1])), c_growth, gross_returns, instruments, w2)

    res2 = minimize(
        obj_step2,
        np.array([p1[0], p1[1]], dtype=np.float64),
        jac=grad_step2,
        method="L-BFGS-B",
        bounds=bounds,
    )
    p2 = (float(res2.x[0]), float(res2.x[1]))

    g2 = sample_moments(p2, c_growth, gross_returns, instruments)
    j_stat = float(t_periods * (g2.T @ w2 @ g2))
    df = k - 2
    j_pvalue = float(gammaincc(df / 2.0, j_stat / 2.0)) if df > 0 else 1.0

    # Asymptotic standard errors via sandwich formula (G^T W G)^(-1) / T
    beta, gamma = p2
    m = beta * (c_growth ** (-gamma))
    log_c = np.log(c_growth)
    du_dbeta = (c_growth[:, None] ** (-gamma)) * gross_returns
    du_dgamma = -m[:, None] * log_c[:, None] * gross_returns
    jacobian = np.empty((k, 2), dtype=np.float64)
    for i in range(n_assets):
        for j in range(l_instruments):
            idx = i * l_instruments + j
            jacobian[idx, 0] = np.mean(du_dbeta[:, i] * instruments[:, j])
            jacobian[idx, 1] = np.mean(du_dgamma[:, i] * instruments[:, j])

    bread = np.linalg.pinv(jacobian.T @ w2 @ jacobian)
    cov_params = bread / float(t_periods)
    se_beta = float(np.sqrt(max(0.0, cov_params[0, 0])))
    se_gamma = float(np.sqrt(max(0.0, cov_params[1, 1])))

    return {
        "beta": p2[0],
        "gamma": p2[1],
        "j_stat": j_stat,
        "j_pvalue": j_pvalue,
        "df": df,
        "standard_errors": (se_beta, se_gamma),
        "step1_params": p1,
    }


def hansen_jagannathan_bound(
    gross_returns: np.ndarray,
    nu_grid: np.ndarray,
) -> np.ndarray:
    """Compute the Hansen-Jagannathan (1991) minimum SDF volatility frontier.

    For gross returns R with price vector 1_N, and target expectation nu = E[M]:
    sigma_{HJ}(nu) = sqrt((1_N - nu * mu_R)^T * Sigma_R^(-1) * (1_N - nu * mu_R))

    Parameters:
        gross_returns: (T, N) array of gross returns.
        nu_grid: (K,) array of candidate expectations E[M].

    Returns:
        (K,) ndarray of minimum SDF volatilities.
    """
    if gross_returns.ndim != 2:
        raise ValueError("gross_returns must be a 2D array of shape (T, N)")
    if nu_grid.ndim != 1:
        raise ValueError("nu_grid must be a 1D array of shape (K,)")

    t_periods, n_assets = gross_returns.shape
    if t_periods < n_assets:
        raise ValueError(f"Sample size T={t_periods} must be strictly greater than number of assets N={n_assets}")

    mu_r = np.mean(gross_returns, axis=0)
    sigma_r = np.cov(gross_returns, rowvar=False)
    sigma_inv = np.linalg.pinv(sigma_r)
    ones = np.ones(n_assets, dtype=np.float64)

    frontier = np.empty(len(nu_grid), dtype=np.float64)
    for k, nu in enumerate(nu_grid):
        diff = ones - float(nu) * mu_r
        variance = float(diff.T @ sigma_inv @ diff)
        frontier[k] = np.sqrt(max(0.0, variance))

    return frontier


def evaluate_consumption_sdf(
    beta: float,
    gamma: float,
    c_growth: np.ndarray,
) -> tuple[float, float]:
    """Compute the sample expectation and volatility of the power utility SDF M = beta * (c')^(-gamma).

    Returns:
        (mean_m, std_m) tuple.
    """
    if not (np.isfinite(beta) and np.isfinite(gamma)):
        raise ValueError("Parameters must be finite")
    if beta <= 0.0:
        raise ValueError("Subjective discount factor beta must be strictly positive")
    if c_growth.ndim != 1 or np.any(c_growth <= 0.0):
        raise ValueError("c_growth must be a 1D strictly positive array")

    sdf = beta * (c_growth ** (-gamma))
    return float(np.mean(sdf)), float(np.std(sdf))
