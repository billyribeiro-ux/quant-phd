"""Mutant 2: Fails to annualize maximum squared Sharpe ratio Sh^2(f) when annualize=True."""

from __future__ import annotations

import numpy as np
import scipy.stats


def fit_factor_model(returns: np.ndarray, factors: np.ndarray) -> dict[str, np.ndarray]:
    t_obs, n_assets = returns.shape
    k_factors = factors.shape[1]
    x_des = np.column_stack([np.ones(t_obs, dtype=np.float64), factors])
    b_hat = np.linalg.lstsq(x_des, returns, rcond=None)[0]
    alphas = b_hat[0, :].copy()
    betas = b_hat[1:, :].T.copy()
    fitted = x_des @ b_hat
    residuals = returns - fitted
    sigma_eps = (residuals.T @ residuals) / float(t_obs - k_factors - 1)
    tot_ss = np.sum((returns - np.mean(returns, axis=0)) ** 2, axis=0)
    res_ss = np.sum(residuals**2, axis=0)
    r2 = 1.0 - (res_ss / np.maximum(tot_ss, 1e-12))
    return {"alphas": alphas, "betas": betas, "residuals": residuals, "sigma_eps": sigma_eps, "r2": r2}


def compute_grs_statistic(
    alphas: np.ndarray, factors: np.ndarray, residuals: np.ndarray
) -> dict[str, float | int]:
    t_obs, k_factors = factors.shape
    n_assets = len(alphas)
    df_denom = t_obs - n_assets - k_factors
    f_bar = np.mean(factors, axis=0)
    sigma_f = np.cov(factors, rowvar=False, ddof=1)
    if k_factors == 1:
        sh2_factor = float((f_bar[0] ** 2) / float(sigma_f))
    else:
        sigma_f_inv = np.linalg.inv(sigma_f)
        sh2_factor = float(f_bar @ sigma_f_inv @ f_bar)
    sigma_eps = (residuals.T @ residuals) / float(t_obs - k_factors - 1)
    sigma_eps_inv = np.linalg.inv(sigma_eps)
    alpha_quad = float(alphas @ sigma_eps_inv @ alphas)
    scale = float(df_denom) / float(n_assets)
    grs_stat = scale * (1.0 / (1.0 + sh2_factor)) * alpha_quad
    p_val = float(1.0 - scipy.stats.f.cdf(grs_stat, n_assets, df_denom))
    return {"stat": float(grs_stat), "p_value": float(p_val), "df_num": int(n_assets), "df_denom": int(df_denom)}


def compute_max_sharpe(factors: np.ndarray, annualize: bool = True) -> float:
    k_factors = factors.shape[1]
    f_bar = np.mean(factors, axis=0)
    sigma_f = np.cov(factors, rowvar=False, ddof=1)
    if k_factors == 1:
        sh2 = float((f_bar[0] ** 2) / float(sigma_f))
    else:
        sigma_f_inv = np.linalg.inv(sigma_f)
        sh2 = float(f_bar @ sigma_f_inv @ f_bar)
    # Student error: ignores annualize flag, returns monthly Sh^2(f)
    return float(sh2)


def evaluate_model_horse_race(
    returns: np.ndarray, models_dict: dict[str, np.ndarray]
) -> dict[str, dict[str, float]]:
    results: dict[str, dict[str, float]] = {}
    for name, f_mat in models_dict.items():
        fit = fit_factor_model(returns, f_mat)
        grs = compute_grs_statistic(fit["alphas"], f_mat, fit["residuals"])
        max_sh2 = compute_max_sharpe(f_mat, annualize=True)
        mean_abs_alpha = float(np.mean(np.abs(fit["alphas"])) * 12.0 * 100.0)
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
    rmspe_results: dict[str, float] = {}
    r_train = returns[:train_len, :]
    r_test = returns[train_len:, :]
    r_bar_oos = np.mean(r_test, axis=0)
    for name, f_mat in models_dict.items():
        f_train = f_mat[:train_len, :]
        f_test = f_mat[train_len:, :]
        fit_is = fit_factor_model(r_train, f_train)
        betas_is = fit_is["betas"]
        f_bar_oos = np.mean(f_test, axis=0)
        pred_mu_oos = betas_is @ f_bar_oos
        sq_errors = (r_bar_oos - pred_mu_oos) ** 2
        rmspe_results[name] = float(np.sqrt(float(np.mean(sq_errors))) * np.sqrt(12.0) * 100.0)
    return rmspe_results
