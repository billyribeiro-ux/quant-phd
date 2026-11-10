"""Starter template for Module F2 Project: Factor-Model Horse Race.

Implement the five core asset pricing functions to pass the grader test suite.
"""

from __future__ import annotations

import numpy as np


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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError
