"""Student error: Multiplies reported volatility by sqrt(xi) instead of dividing, understating unsmoothed risk."""

from __future__ import annotations

import numpy as np
import scipy.linalg
import scipy.optimize
import scipy.stats


def compute_factor_alpha(
    excess_returns: np.ndarray,
    factors: np.ndarray,
    bandwidth: int = 4,
) -> dict[str, float]:
    """Fit multi-factor regression with Newey-West (1987) HAC standard errors."""
    n_obs, k_factors = factors.shape
    ones = np.ones((n_obs, 1))
    x_mat = np.column_stack([ones, factors])
    xtx_inv = np.linalg.inv(x_mat.T @ x_mat)
    beta = xtx_inv @ (x_mat.T @ excess_returns)
    resid = excess_returns - x_mat @ beta

    diag_e2 = np.diag(resid**2)
    gamma_0 = (x_mat.T @ diag_e2 @ x_mat) / float(n_obs)
    gamma_sum = np.zeros_like(gamma_0)
    for lag in range(1, bandwidth + 1):
        weight = 1.0 - (lag / (bandwidth + 1.0))
        gamma_l = np.zeros_like(gamma_0)
        for t in range(lag, n_obs):
            x_t = x_mat[t : t + 1, :].T
            x_t_lag = x_mat[t - lag : t - lag + 1, :].T
            gamma_l += resid[t] * resid[t - lag] * (x_t @ x_t_lag.T + x_t_lag @ x_t.T)
        gamma_sum += weight * (gamma_l / float(n_obs))

    v_hac = float(n_obs) * (xtx_inv @ (gamma_0 + gamma_sum) @ xtx_inv)
    se_alpha = float(np.sqrt(max(v_hac[0, 0], 1e-12)))
    t_stat = float(beta[0] / se_alpha)
    p_val = float(2.0 * (1.0 - scipy.stats.t.cdf(np.abs(t_stat), df=n_obs - k_factors - 1)))
    ss_tot = float(np.sum((excess_returns - np.mean(excess_returns)) ** 2))
    ss_res = float(np.sum(resid**2))
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    return {
        "alpha_ann": float(beta[0] * 12.0),
        "alpha_monthly": float(beta[0]),
        "se_alpha_hac": se_alpha,
        "t_stat_hac": t_stat,
        "p_value_hac": p_val,
        "r_squared": float(r2),
    }


def compute_autocorrelation_adjusted_sharpe(
    returns: np.ndarray,
    q_horizon: int = 12,
) -> dict[str, float]:
    """Compute naive and Lo (2002) autocorrelation-adjusted Sharpe ratio."""
    mean_val = float(np.mean(returns))
    std_val = float(np.std(returns, ddof=1))
    sr_naive = (mean_val / std_val) * np.sqrt(q_horizon) if std_val > 1e-12 else 0.0

    demeaned = returns - mean_val
    var_denom = float(np.sum(demeaned**2))
    rhos = np.zeros(q_horizon - 1)
    if var_denom > 1e-12:
        for k in range(1, q_horizon):
            cov_k = float(np.sum(demeaned[k:] * demeaned[:-k]))
            rhos[k - 1] = cov_k / var_denom

    cross_sum = sum(2.0 * (q_horizon - k) * rhos[k - 1] for k in range(1, q_horizon))
    denom = max(float(q_horizon) + cross_sum, 0.1)
    eta_q = float(np.sqrt(float(q_horizon) / denom))

    return {
        "sr_naive_ann": sr_naive,
        "rho_1": float(rhos[0]),
        "eta_q": eta_q,
        "sr_adjusted_ann": float(eta_q * sr_naive),
    }


def unsmooth_returns_glm(reported_returns: np.ndarray) -> dict[str, float]:
    """MUTANT ERROR: Multiplies observed volatility by sqrt(xi), understating true volatility."""
    sample_vol = float(np.std(reported_returns, ddof=1))
    mean_val = float(np.mean(reported_returns))

    # Correct theta
    t0, t1, t2 = 0.55, 0.30, 0.15
    xi = float(t0**2 + t1**2 + t2**2)

    # BUG: multiplies instead of dividing: sigma* = sigma_R * sqrt(xi) < sigma_R!
    sig = sample_vol * np.sqrt(xi)

    return {
        "theta_0": t0,
        "theta_1": t1,
        "theta_2": t2,
        "xi": xi,
        "vol_reported_ann": sample_vol * np.sqrt(12.0),
        "vol_unsmoothed_ann": sig * np.sqrt(12.0),
        "sr_unsmoothed_ann": (mean_val / sig) * np.sqrt(12.0),
    }


def detect_nonlinear_exposure(returns: np.ndarray, mkt_excess: np.ndarray) -> dict[str, float]:
    """Fit Treynor-Mazuy quadratic payoff model to detect convexity or concavity."""
    n_obs = len(returns)
    ones = np.ones((n_obs, 1))
    mkt_sq = ((mkt_excess - np.mean(mkt_excess)) ** 2).reshape(-1, 1)
    x_mat = np.column_stack([ones, mkt_excess.reshape(-1, 1), mkt_sq])
    xtx_inv = np.linalg.inv(x_mat.T @ x_mat)
    b = xtx_inv @ (x_mat.T @ returns)
    resid = returns - x_mat @ b
    s2 = float(np.sum(resid**2) / (n_obs - 3))
    se = np.sqrt(np.diag(xtx_inv * s2))
    t_gamma = float(b[2] / se[2])

    return {
        "alpha_ann": float(b[0] * 12.0),
        "beta_mkt": float(b[1]),
        "gamma": float(b[2]),
        "t_gamma": t_gamma,
    }


def evaluate_manager_universe(instance: dict[str, object]) -> list[dict[str, object]]:
    """Evaluate all managers in the dataset and produce an honest ranking."""
    factors = np.asarray(instance["factors"], dtype=np.float64)
    mkt = np.asarray(instance["mkt_excess"], dtype=np.float64)
    ret_mat = np.asarray(instance["manager_returns"], dtype=np.float64)
    raw_names = instance["manager_names"]
    names = [str(x) for x in raw_names] if isinstance(raw_names, (list, tuple, np.ndarray)) else []

    evaluations: list[dict[str, object]] = []
    for i, name in enumerate(names):
        r_mgr = ret_mat[:, i]
        alpha_res = compute_factor_alpha(r_mgr, factors)
        lo_res = compute_autocorrelation_adjusted_sharpe(r_mgr)
        glm_res = unsmooth_returns_glm(r_mgr)
        quad_res = detect_nonlinear_exposure(r_mgr, mkt)

        alpha_val = float(alpha_res["alpha_ann"])
        t_alpha_val = float(alpha_res["t_stat_hac"])
        alpha_credit = alpha_val if t_alpha_val > 1.96 else min(alpha_val, 0.0)
        concavity_penalty = 0.08 * max(0.0, -float(quad_res["t_gamma"]) - 2.0)
        smoothing_penalty = 0.04 * (1.0 - float(glm_res["xi"]))

        dd_score = float(
            alpha_credit + 0.05 * float(glm_res["sr_unsmoothed_ann"]) - concavity_penalty - smoothing_penalty
        )

        evaluations.append({
            "name": name,
            "alpha_ann": alpha_val,
            "t_alpha": t_alpha_val,
            "sr_naive": float(lo_res["sr_naive_ann"]),
            "sr_adj": float(lo_res["sr_adjusted_ann"]),
            "xi": float(glm_res["xi"]),
            "vol_unsmoothed": float(glm_res["vol_unsmoothed_ann"]),
            "gamma": float(quad_res["gamma"]),
            "t_gamma": float(quad_res["t_gamma"]),
            "dd_score": dd_score,
        })

    evaluations.sort(key=lambda x: float(str(x["dd_score"])), reverse=True)
    for rank, ev in enumerate(evaluations, 1):
        ev["rank"] = rank

    return evaluations
