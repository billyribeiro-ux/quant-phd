"""Lab F2-project-1: Project Rung 1 Worked Example - Factor-Model Horse Race.

Executes a complete factor model horse race comparing CAPM, Fama-French 3-Factor,
Carhart 4-Factor, Fama-French 5-Factor, and Hou-Xue-Zhang q-factor models across
25 size-value test portfolios, displaying GRS test statistics, p-values, maximum
squared Sharpe ratios Sh^2(f), and out-of-sample Root Mean Squared Pricing Errors.
"""

from __future__ import annotations

import numpy as np
import scipy.stats


def make_instance(seed: int) -> dict[str, object]:
    """Generate a deterministic factor horse race dataset from a single seed."""
    rng = np.random.default_rng(seed)
    n_months = 360  # 30 years
    n_assets = 25  # 25 test portfolios
    train_len = 240  # 20 years in-sample, 10 years out-of-sample

    mkt = rng.normal(0.065 / 12, 0.155 / np.sqrt(12), size=n_months)
    smb = rng.normal(0.025 / 12, 0.100 / np.sqrt(12), size=n_months)
    rmw = rng.normal(0.038 / 12, 0.080 / np.sqrt(12), size=n_months)
    cma = rng.normal(0.032 / 12, 0.070 / np.sqrt(12), size=n_months)

    e_hml = rng.normal(0.0, 0.045 / np.sqrt(12), size=n_months)
    hml = (0.015 / 12) + 0.08 * mkt + 0.05 * smb - 0.28 * rmw + 0.88 * cma + e_hml

    wml_raw = rng.normal(0.075 / 12, 0.135 / np.sqrt(12), size=n_months)
    wml = wml_raw + (0.075 / 12 - float(np.mean(wml_raw)))

    q_me = smb + rng.normal(0.0, 0.015 / np.sqrt(12), size=n_months)
    q_ia = cma + rng.normal(0.0, 0.015 / np.sqrt(12), size=n_months)
    q_roe = rmw + rng.normal(0.0, 0.018 / np.sqrt(12), size=n_months)

    factors_capm = np.column_stack([mkt]).astype(np.float64)
    factors_ff3 = np.column_stack([mkt, smb, hml]).astype(np.float64)
    factors_carhart = np.column_stack([mkt, smb, hml, wml]).astype(np.float64)
    factors_ff5 = np.column_stack([mkt, smb, hml, rmw, cma]).astype(np.float64)
    factors_q_factor = np.column_stack([mkt, q_me, q_ia, q_roe]).astype(np.float64)

    b_mkt = rng.uniform(0.75, 1.25, size=n_assets)
    b_smb = np.repeat(np.linspace(0.8, -0.3, 5), 5) + rng.normal(0.0, 0.05, size=n_assets)
    b_hml = np.tile(np.linspace(-0.4, 0.7, 5), 5) + rng.normal(0.0, 0.05, size=n_assets)
    b_rmw = rng.uniform(-0.3, 0.4, size=n_assets)
    b_cma = rng.uniform(-0.3, 0.5, size=n_assets)

    true_alphas = rng.normal(0.0, 0.012 / 12, size=n_assets)

    test_returns = np.zeros((n_months, n_assets), dtype=np.float64)
    for t in range(n_months):
        idio = rng.normal(0.0, 0.16 / np.sqrt(12), size=n_assets)
        test_returns[t, :] = (
            true_alphas + b_mkt * mkt[t] + b_smb * smb[t] + b_hml * hml[t] + b_rmw * rmw[t] + b_cma * cma[t] + idio
        )

    return {
        "seed": int(seed),
        "n_months": int(n_months),
        "n_assets": int(n_assets),
        "train_len": int(train_len),
        "test_returns": test_returns,
        "factors_capm": factors_capm,
        "factors_ff3": factors_ff3,
        "factors_carhart": factors_carhart,
        "factors_ff5": factors_ff5,
        "factors_q_factor": factors_q_factor,
    }


def fit_factor_model(returns: np.ndarray, factors: np.ndarray) -> dict[str, np.ndarray]:
    """Fit time-series asset pricing regressions for N test assets on K factors."""
    t_obs, _n_assets = returns.shape
    k_factors = factors.shape[1]
    x_des = np.column_stack([np.ones(t_obs, dtype=np.float64), factors])
    b_hat = np.linalg.lstsq(x_des, returns, rcond=None)[0]
    alphas = b_hat[0, :].copy()
    betas = b_hat[1:, :].T.copy()
    fitted = x_des @ b_hat
    residuals = returns - fitted
    dof_resid = t_obs - k_factors - 1
    sigma_eps = (residuals.T @ residuals) / float(dof_resid)
    tot_ss = np.sum((returns - np.mean(returns, axis=0)) ** 2, axis=0)
    res_ss = np.sum(residuals**2, axis=0)
    r2 = 1.0 - (res_ss / np.maximum(tot_ss, 1e-12))
    return {"alphas": alphas, "betas": betas, "residuals": residuals, "sigma_eps": sigma_eps, "r2": r2}


def compute_grs_statistic(alphas: np.ndarray, factors: np.ndarray, residuals: np.ndarray) -> dict[str, float | int]:
    """Compute the Gibbons, Ross, and Shanken (1989) exact F-test statistic."""
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
    """Compute Barillas-Shanken (2017) maximum squared Sharpe ratio Sh^2(f)."""
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
    """Evaluate candidate factor models across GRS, Max-Sharpe, and alpha metrics."""
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
    """Compute out-of-sample Root Mean Squared Pricing Error (RMSPE)."""
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
        rmspe_monthly = np.sqrt(float(np.mean(sq_errors)))
        rmspe_ann = float(rmspe_monthly * np.sqrt(12.0) * 100.0)
        rmspe_results[name] = rmspe_ann
    return rmspe_results


def run_worked_example(seed: int = 42) -> dict[str, object]:
    """Execute complete horse race on seeded instance."""
    inst = make_instance(seed)
    test_returns = np.asarray(inst["test_returns"], dtype=np.float64)
    models = {
        "CAPM": np.asarray(inst["factors_capm"], dtype=np.float64),
        "FF3": np.asarray(inst["factors_ff3"], dtype=np.float64),
        "Carhart": np.asarray(inst["factors_carhart"], dtype=np.float64),
        "FF5": np.asarray(inst["factors_ff5"], dtype=np.float64),
        "q_factor": np.asarray(inst["factors_q_factor"], dtype=np.float64),
    }
    raw_len = inst["train_len"]
    assert isinstance(raw_len, int)
    train_len = raw_len

    race_results = evaluate_model_horse_race(test_returns, models)
    oos_results = compute_out_of_sample_rmspe(test_returns, models, train_len=train_len)

    table: list[dict[str, object]] = []
    for model_name in ["CAPM", "FF3", "Carhart", "FF5", "q_factor"]:
        m = race_results[model_name]
        table.append(
            {
                "model": model_name,
                "grs_stat": round(m["grs_stat"], 2),
                "p_value": round(m["p_value"], 4),
                "max_sharpe_sq": round(m["max_sharpe_sq"], 4),
                "mean_abs_alpha": round(m["mean_abs_alpha_ann"], 2),
                "mean_r2": round(m["mean_r2"], 4),
                "oos_rmspe": round(oos_results[model_name], 2),
            }
        )

    return {"seed": seed, "table": table}


def main() -> None:
    print("Project Rung 1 | Factor-Model Horse Race (Worked Example)")
    print("================================================================================")
    res = run_worked_example(seed=42)
    rows = res["table"]
    assert isinstance(rows, list)
    header = (
        f"{'Model':<10} | {'GRS Stat':<9} | {'p-value':<8} | {'Sh^2(f)':<8} | "
        f"{'|Alpha| %':<9} | {'Mean R2':<8} | {'OOS RMSPE %':<11}"
    )
    print(header)
    print("-" * len(header))
    for r in rows:
        print(
            f"{r['model']:<10} | {r['grs_stat']:<9.2f} | {r['p_value']:<8.4f} | {r['max_sharpe_sq']:<8.4f} | "
            f"{r['mean_abs_alpha']:<9.2f} | {r['mean_r2']:<8.4f} | {r['oos_rmspe']:<11.2f}"
        )
    print("================================================================================")
    print("Carhart and FF5 deliver highest Sh^2(f); multi-factor models reduce pricing error.")


main()
