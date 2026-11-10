"""Student error: Omits quadratic curvature term in payoff regression, misclassifying short-volatility managers."""

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
    """Estimate Getmansky-Lo-Makarov MA(2) return unsmoothing parameters via MLE."""
    n_obs = len(reported_returns)
    sample_vol = float(np.std(reported_returns, ddof=1))
    mean_val = float(np.mean(reported_returns))
    demeaned = reported_returns - mean_val

    def neg_log_lik(p: np.ndarray) -> float:
        t0, t1, sig = float(p[0]), float(p[1]), float(p[2])
        t2 = 1.0 - t0 - t1
        if t2 < -1e-6 or t0 < 0.0 or t1 < 0.0 or sig <= 1e-6:
            return 1e10
        t2 = max(0.0, t2)
        th = np.array([t0, t1, t2])
        g0 = (sig**2) * float(np.sum(th**2))
        g1 = (sig**2) * float(th[0] * th[1] + th[1] * th[2])
        g2 = (sig**2) * float(th[0] * th[2])
        c = np.zeros(n_obs)
        c[0], c[1], c[2] = g0, g1, g2
        try:
            cov_mat = scipy.linalg.toeplitz(c) + np.eye(n_obs) * 1e-8
            chol_l = scipy.linalg.cholesky(cov_mat, lower=True)
            log_det = 2.0 * float(np.sum(np.log(np.diag(chol_l))))
            y_vec = scipy.linalg.solve_triangular(chol_l, demeaned, lower=True)
            return float(0.5 * (float(n_obs) * np.log(2.0 * np.pi) + log_det + float(np.sum(y_vec**2))))
        except Exception:
            return 1e10

    best_res = None
    best_f = 1e10
    bounds = [(0.05, 0.95), (0.00, 0.95), (1e-4, 1.0)]
    cons = ({"type": "ineq", "fun": lambda p: 1.0 - p[0] - p[1]},)

    for init_t0 in [0.75, 0.50]:
        init_t1 = (1.0 - init_t0) * 0.5
        init_sig = sample_vol / np.sqrt(init_t0**2 + init_t1**2 + (1.0 - init_t0 - init_t1) ** 2)
        res = scipy.optimize.minimize(
            neg_log_lik,
            np.array([init_t0, init_t1, init_sig]),
            bounds=bounds,
            constraints=cons,
            method="SLSQP",
        )
        if res.success and res.fun < best_f:
            best_f = float(res.fun)
            best_res = res

    if best_res is None:
        t0, t1, sig = 1.0, 0.0, sample_vol
        t2 = 0.0
    else:
        t0, t1 = float(best_res.x[0]), float(best_res.x[1])
        t2 = max(0.0, 1.0 - t0 - t1)
        sig = float(best_res.x[2])

    xi = float(t0**2 + t1**2 + t2**2)
    vol_reported_ann = sample_vol * np.sqrt(12.0)
    vol_unsmoothed_ann = sig * np.sqrt(12.0)
    sr_unsmoothed = (mean_val / sig) * np.sqrt(12.0) if sig > 1e-6 else 0.0

    return {
        "theta_0": t0,
        "theta_1": t1,
        "theta_2": t2,
        "xi": xi,
        "vol_reported_ann": vol_reported_ann,
        "vol_unsmoothed_ann": vol_unsmoothed_ann,
        "sr_unsmoothed_ann": sr_unsmoothed,
    }


def detect_nonlinear_exposure(returns: np.ndarray, mkt_excess: np.ndarray) -> dict[str, float]:
    """MUTANT ERROR: Disregards option/quadratic term, forcing gamma = 0.0."""
    n_obs = len(returns)
    ones = np.ones((n_obs, 1))
    x_mat = np.column_stack([ones, mkt_excess.reshape(-1, 1)])
    xtx_inv = np.linalg.inv(x_mat.T @ x_mat)
    b = xtx_inv @ (x_mat.T @ returns)

    # BUG: sets gamma = 0.0, ignoring concavity/convexity!
    return {
        "alpha_ann": float(b[0] * 12.0),
        "beta_mkt": float(b[1]),
        "gamma": 0.0,
        "t_gamma": 0.0,
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
