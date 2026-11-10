"""Reference implementation for Module F2 Project: Factor-Model Horse Race.

Implements multivariate time-series regressions, exact Gibbons-Ross-Shanken (1989)
F-test evaluation, Barillas-Shanken (2017) maximum squared Sharpe ratio metric Sh^2(f),
and out-of-sample root mean squared pricing error estimation across asset pricing models.
"""

from __future__ import annotations

import numpy as np
import scipy.stats  # type: ignore[import-untyped]


def fit_factor_model(returns: np.ndarray, factors: np.ndarray) -> dict[str, np.ndarray]:
    """Fit time-series asset pricing regressions for N test assets on K factors.

    Model: R_{i,t} = alpha_i + beta_i^T f_t + epsilon_{i,t}

    Parameters
    ----------
    returns : np.ndarray
        Array of shape (T, N) holding excess returns of N test assets.
    factors : np.ndarray
        Array of shape (T, K) holding returns of K candidate factors.

    Returns
    -------
    dict[str, np.ndarray]
        Contains:
        - "alphas": shape (N,) estimated pricing errors.
        - "betas": shape (N, K) factor loadings.
        - "residuals": shape (T, N) regression residuals.
        - "sigma_eps": shape (N, N) unbiased residual covariance matrix (ddof = T - K - 1).
        - "r2": shape (N,) coefficient of determination per asset.
    """
    t_obs, _n_assets = returns.shape
    k_factors = factors.shape[1]

    # Design matrix with intercept: X = [1, f_1, ..., f_K] of shape (T, K + 1)
    x_des = np.column_stack([np.ones(t_obs, dtype=np.float64), factors])

    # OLS coefficient matrix B_hat of shape (K + 1, N)
    # Row 0: alphas; Rows 1..K: factor betas
    b_hat = np.linalg.lstsq(x_des, returns, rcond=None)[0]

    alphas = b_hat[0, :].copy()
    betas = b_hat[1:, :].T.copy()  # shape (N, K)

    fitted = x_des @ b_hat
    residuals = returns - fitted

    # Unbiased residual covariance matrix dividing by (T - K - 1)
    dof_resid = t_obs - k_factors - 1
    if dof_resid <= 0:
        raise ValueError(f"Degrees of freedom non-positive: T={t_obs}, K={k_factors}")
    sigma_eps = (residuals.T @ residuals) / float(dof_resid)

    # R^2 calculation per test asset
    tot_ss = np.sum((returns - np.mean(returns, axis=0)) ** 2, axis=0)
    res_ss = np.sum(residuals**2, axis=0)
    r2 = 1.0 - (res_ss / np.maximum(tot_ss, 1e-12))

    return {
        "alphas": alphas,
        "betas": betas,
        "residuals": residuals,
        "sigma_eps": sigma_eps,
        "r2": r2,
    }


def compute_grs_statistic(alphas: np.ndarray, factors: np.ndarray, residuals: np.ndarray) -> dict[str, float | int]:
    """Compute the Gibbons, Ross, and Shanken (1989) exact F-test statistic.

    GRS formula:
    F = [(T - N - K) / N] * [1 / (1 + f_bar^T Sigma_f^{-1} f_bar)] * [alpha^T Sigma_eps^{-1} alpha]

    Parameters
    ----------
    alphas : np.ndarray
        Array of shape (N,) containing estimated pricing errors.
    factors : np.ndarray
        Array of shape (T, K) containing factor returns.
    residuals : np.ndarray
        Array of shape (T, N) containing time-series residuals.

    Returns
    -------
    dict[str, float | int]
        Contains:
        - "stat": GRS F-statistic.
        - "p_value": p-value from F(N, T - N - K).
        - "df_num": numerator degrees of freedom (N).
        - "df_denom": denominator degrees of freedom (T - N - K).
    """
    t_obs, k_factors = factors.shape
    n_assets = len(alphas)

    df_denom = t_obs - n_assets - k_factors
    if df_denom <= 0:
        raise ValueError(f"GRS denominator degrees of freedom non-positive: T={t_obs}, N={n_assets}, K={k_factors}")

    # Factor quadratic form: f_bar^T * Sigma_f^{-1} * f_bar
    f_bar = np.mean(factors, axis=0)
    sigma_f = np.cov(factors, rowvar=False, ddof=1)
    if k_factors == 1:
        sh2_factor = float((f_bar[0] ** 2) / float(sigma_f))
    else:
        sigma_f_inv = np.linalg.inv(sigma_f)
        sh2_factor = float(f_bar @ sigma_f_inv @ f_bar)

    # Unbiased residual covariance matrix
    sigma_eps = (residuals.T @ residuals) / float(t_obs - k_factors - 1)
    sigma_eps_inv = np.linalg.inv(sigma_eps)

    alpha_quad = float(alphas @ sigma_eps_inv @ alphas)

    scale = float(df_denom) / float(n_assets)
    grs_stat = scale * (1.0 / (1.0 + sh2_factor)) * alpha_quad
    p_val = float(1.0 - scipy.stats.f.cdf(grs_stat, n_assets, df_denom))

    return {
        "stat": float(grs_stat),
        "p_value": float(p_val),
        "df_num": int(n_assets),
        "df_denom": int(df_denom),
    }


def compute_max_sharpe(factors: np.ndarray, annualize: bool = True) -> float:
    """Compute Barillas-Shanken (2017) maximum squared Sharpe ratio Sh^2(f).

    Sh^2(f) = mu_f^T Sigma_f^{-1} mu_f

    Parameters
    ----------
    factors : np.ndarray
        Array of shape (T, K) containing factor returns.
    annualize : bool
        If True, multiplies monthly squared Sharpe ratio by 12.

    Returns
    -------
    float
        Maximum squared Sharpe ratio of the factor tangency portfolio.
    """
    k_factors = factors.shape[1]
    f_bar = np.mean(factors, axis=0)
    sigma_f = np.cov(factors, rowvar=False, ddof=1)

    if k_factors == 1:
        sh2 = float((f_bar[0] ** 2) / float(sigma_f))
    else:
        sigma_f_inv = np.linalg.inv(sigma_f)
        sh2 = float(f_bar @ sigma_f_inv @ f_bar)

    if annualize:
        sh2 *= 12.0

    return float(sh2)


def evaluate_model_horse_race(returns: np.ndarray, models_dict: dict[str, np.ndarray]) -> dict[str, dict[str, float]]:
    """Evaluate candidate factor models across GRS, Max-Sharpe, and alpha metrics.

    Parameters
    ----------
    returns : np.ndarray
        Array of shape (T, N) holding excess returns of test assets.
    models_dict : dict[str, np.ndarray]
        Mapping from model name to factor array of shape (T, K).

    Returns
    -------
    dict[str, dict[str, float]]
        Nested dictionary with evaluation metrics for each model:
        "grs_stat", "p_value", "max_sharpe_sq", "mean_abs_alpha_ann", "mean_r2".
    """
    results: dict[str, dict[str, float]] = {}

    for name, f_mat in models_dict.items():
        fit = fit_factor_model(returns, f_mat)
        grs = compute_grs_statistic(fit["alphas"], f_mat, fit["residuals"])
        max_sh2 = compute_max_sharpe(f_mat, annualize=True)

        mean_abs_alpha = float(np.mean(np.abs(fit["alphas"])) * 12.0 * 100.0)  # % per year
        mean_r2 = float(np.mean(fit["r2"]))

        results[name] = {
            "grs_stat": float(grs["stat"]),
            "p_value": float(grs["p_value"]),
            "max_sharpe_sq": float(max_sh2),
            "mean_abs_alpha_ann": float(mean_abs_alpha),
            "mean_r2": float(mean_r2),
        }

    return results


def compute_out_of_sample_rmspe(
    returns: np.ndarray, models_dict: dict[str, np.ndarray], train_len: int = 240
) -> dict[str, float]:
    """Compute out-of-sample Root Mean Squared Pricing Error (RMSPE).

    Trains factor betas on in-sample period [0 : train_len], predicts out-of-sample
    expected returns using realized out-of-sample factor means, and compares to
    realized average out-of-sample returns across the N test assets.

    RMSPE = sqrt( (1 / N) * sum_{i=1}^N (R_bar_{i,oos} - beta_{i,is}^T f_bar_{oos})^2 ) * sqrt(12) * 100

    Parameters
    ----------
    returns : np.ndarray
        Array of shape (T, N) holding excess returns.
    models_dict : dict[str, np.ndarray]
        Mapping from model name to factor array of shape (T, K).
    train_len : int
        Number of training periods (e.g. 240).

    Returns
    -------
    dict[str, float]
        Mapping from model name to annualized percentage RMSPE.
    """
    rmspe_results: dict[str, float] = {}

    r_train = returns[:train_len, :]
    r_test = returns[train_len:, :]

    # Realized out-of-sample average returns
    r_bar_oos = np.mean(r_test, axis=0)  # shape (N,)

    for name, f_mat in models_dict.items():
        f_train = f_mat[:train_len, :]
        f_test = f_mat[train_len:, :]

        # Fit in-sample betas
        fit_is = fit_factor_model(r_train, f_train)
        betas_is = fit_is["betas"]  # shape (N, K)

        # Out-of-sample factor means
        f_bar_oos = np.mean(f_test, axis=0)  # shape (K,)

        # Predicted expected return under the model (alpha constrained to 0)
        pred_mu_oos = betas_is @ f_bar_oos  # shape (N,)

        # Root mean squared pricing error across N test assets
        sq_errors = (r_bar_oos - pred_mu_oos) ** 2
        rmspe_monthly = np.sqrt(float(np.mean(sq_errors)))
        rmspe_ann = float(rmspe_monthly * np.sqrt(12.0) * 100.0)

        rmspe_results[name] = rmspe_ann

    return rmspe_results
