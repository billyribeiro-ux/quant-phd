"""Lab F7-project-2: Project Rung 2 Completion Problem - Due-Diligence Econometric Engine.

Completed reference twin for the Project Rung 2 completion exercise. Implements
Lo (2002) serial correlation Sharpe ratio adjustments, Getmansky-Lo-Makarov (2004)
constrained MLE return unsmoothing, and Treynor-Mazuy nonlinear payoff detection.
"""

from __future__ import annotations

import numpy as np
import scipy.linalg
import scipy.optimize


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

    # Lo (2002) cross-correlation sum: 2 * sum_{k=1}^{q-1} (q - k) * rho_k
    cross_sum = sum(2.0 * (q_horizon - k) * rhos[k - 1] for k in range(1, q_horizon))
    denom = max(float(q_horizon) + cross_sum, 0.1)
    eta_q = float(np.sqrt(float(q_horizon) / denom))

    return {
        "sr_naive_ann": round(sr_naive, 4),
        "rho_1": round(float(rhos[0]), 4),
        "eta_q": round(eta_q, 4),
        "sr_adjusted_ann": round(float(eta_q * sr_naive), 4),
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
    vol_unsmoothed_ann = float(sig * np.sqrt(12.0) * 100.0)
    sr_unsmoothed = float((mean_val / sig) * np.sqrt(12.0) if sig > 1e-6 else 0.0)

    return {
        "theta_0": round(t0, 3),
        "theta_1": round(t1, 3),
        "theta_2": round(t2, 3),
        "xi": round(xi, 4),
        "vol_unsmoothed_ann": round(vol_unsmoothed_ann, 2),
        "sr_unsmoothed_ann": round(sr_unsmoothed, 4),
    }


def detect_nonlinear_exposure(
    returns: np.ndarray,
    mkt_excess: np.ndarray,
) -> dict[str, float]:
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
        "alpha_ann": round(float(b[0] * 12.0 * 100.0), 2),
        "beta_mkt": round(float(b[1]), 3),
        "gamma": round(float(b[2]), 2),
        "t_gamma": round(t_gamma, 2),
    }


def main() -> None:
    print("Project Rung 2 | Due-Diligence Econometric Engine (Completion Solution)")
    print("---------------------------------------------------------------------")
    # Quick deterministic check on synthetic series
    rng = np.random.default_rng(42)
    n_obs = 180
    mkt = rng.normal(0.007, 0.045, size=n_obs)
    # Smoothed series
    r_true = rng.normal(0.008, 0.040, size=n_obs + 2)
    r_smooth = 0.55 * r_true[2:] + 0.30 * r_true[1:-1] + 0.15 * r_true[:-2]

    lo_res = compute_autocorrelation_adjusted_sharpe(r_smooth)
    glm_res = unsmooth_returns_glm(r_smooth)
    nl_res = detect_nonlinear_exposure(r_smooth, mkt)

    print(f"Lo (2002) Adjusted Sharpe:   {lo_res['sr_adjusted_ann']:.4f} (eta: {lo_res['eta_q']:.4f})")
    print(f"GLM Illiquidity Score (xi):  {glm_res['xi']:.4f} (Unsmoothed Vol: {glm_res['vol_unsmoothed_ann']:.2f}%)")
    print(f"Nonlinear Curvature (gamma): {nl_res['gamma']:+.2f} (t = {nl_res['t_gamma']:+.2f})")


main()
