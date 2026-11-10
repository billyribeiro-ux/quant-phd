"""Lab F7-project-1: Project Rung 1 Worked Example - Manager Due-Diligence Tool.

Executes a complete quantitative due-diligence evaluation across a multi-strategy
institutional manager universe. Diagnoses factor-adjusted alpha with HAC standard errors,
applies Lo (2002) serial correlation adjustments to Sharpe ratios, uncovers latent risk
via GLM (2004) econometric unsmoothing, detects nonlinear option-like exposures, and
constructs an honest ranking penalized for smoothing and hidden tail risk.
"""

from __future__ import annotations

import numpy as np
import scipy.linalg
import scipy.optimize
import scipy.stats


def make_instance(seed: int) -> dict[str, object]:
    """Generate a deterministic 5-manager due-diligence dataset from a seed."""
    rng = np.random.default_rng(seed)
    n_months = 180
    burn = 2

    # 4 Systematic benchmark factors: Mkt-RF, SMB, HML, MOM
    mkt_all = rng.normal(0.0065, 0.045, size=n_months + burn)
    smb_all = rng.normal(0.0020, 0.030, size=n_months + burn)
    hml_all = rng.normal(0.0025, 0.032, size=n_months + burn)
    mom_all = rng.normal(0.0050, 0.040, size=n_months + burn)

    mkt = mkt_all[burn:]
    smb = smb_all[burn:]
    hml = hml_all[burn:]
    mom = mom_all[burn:]
    factors = np.column_stack([mkt, smb, hml, mom])

    mkt_demeaned_sq = (mkt - np.mean(mkt)) ** 2

    # Manager 1: AlphaStar Equity (Genuine skill, liquid equity long/short)
    r1 = 0.0035 + 0.80 * mkt + 0.20 * smb - 0.10 * hml + 0.15 * mom + rng.normal(0.0, 0.018, size=n_months)

    # Manager 2: Harbor DirectLending (Illiquid private debt with return smoothing)
    r2_star = 0.0010 + 0.25 * mkt_all + rng.normal(0.0, 0.038, size=n_months + burn)
    th_harbor = np.array([0.55, 0.30, 0.15])
    r2 = np.zeros(n_months)
    for t in range(n_months):
        r2[t] = th_harbor[0] * r2_star[t + 2] + th_harbor[1] * r2_star[t + 1] + th_harbor[2] * r2_star[t]

    # Manager 3: Apex VolCarry (Short volatility / naked put seller; hidden tail risk)
    r3 = 0.0090 + 0.40 * mkt - 6.0 * mkt_demeaned_sq + rng.normal(0.0, 0.014, size=n_months)

    # Manager 4: Beacon TrendCTA (Trend following / long straddle; convex payoff)
    r4 = 0.0015 + 0.05 * mkt + 4.5 * mkt_demeaned_sq + rng.normal(0.0, 0.022, size=n_months)

    # Manager 5: Crestline BetaChaser (Zero true alpha, disguised high market beta)
    r5 = 0.0000 + 1.15 * mkt + rng.normal(0.0, 0.012, size=n_months)

    manager_returns = np.column_stack([r1, r2, r3, r4, r5])
    manager_names = [
        "AlphaStar_Equity",
        "Harbor_DirectLending",
        "Apex_VolCarry",
        "Beacon_TrendCTA",
        "Crestline_BetaChaser",
    ]

    return {
        "seed": int(seed),
        "n_months": int(n_months),
        "factor_names": ["Mkt-RF", "SMB", "HML", "MOM"],
        "factors": factors,
        "mkt_excess": mkt,
        "manager_names": manager_names,
        "manager_returns": manager_returns,
    }


def compute_factor_alpha(excess_returns: np.ndarray, factors: np.ndarray, bandwidth: int = 4) -> dict[str, float]:
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


def compute_autocorrelation_adjusted_sharpe(returns: np.ndarray, q_horizon: int = 12) -> dict[str, float]:
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
    denom = max(q_horizon + cross_sum, 0.1)
    eta_q = float(np.sqrt(q_horizon / denom))

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

        # Honest due diligence scoring model:
        # Base: Factor-adjusted alpha (if statistically significant at 5% level)
        # + 0.5 * Unsmoothed Sharpe ratio
        # - Concavity penalty for short volatility / tail risk
        # - Smoothing penalty for illiquidity / mark-to-model
        alpha_credit = alpha_res["alpha_ann"] if alpha_res["t_stat_hac"] > 1.96 else min(alpha_res["alpha_ann"], 0.0)
        concavity_penalty = 0.08 * max(0.0, -quad_res["t_gamma"] - 2.0)
        smoothing_penalty = 0.04 * (1.0 - glm_res["xi"])

        dd_score = float(alpha_credit + 0.05 * glm_res["sr_unsmoothed_ann"] - concavity_penalty - smoothing_penalty)

        evaluations.append(
            {
                "name": name,
                "alpha_ann": alpha_res["alpha_ann"],
                "t_alpha": alpha_res["t_stat_hac"],
                "sr_naive": lo_res["sr_naive_ann"],
                "sr_adj": lo_res["sr_adjusted_ann"],
                "xi": glm_res["xi"],
                "vol_unsmoothed": glm_res["vol_unsmoothed_ann"],
                "gamma": quad_res["gamma"],
                "t_gamma": quad_res["t_gamma"],
                "dd_score": dd_score,
            }
        )

    # Sort descending by honest score
    evaluations.sort(key=lambda x: float(str(x["dd_score"])), reverse=True)
    for rank, ev in enumerate(evaluations, 1):
        ev["rank"] = rank

    return evaluations


def main() -> None:
    print("Lab F7-project-1 | Manager Due-Diligence Tool (Worked Example)")
    print("================================================================================")
    inst = make_instance(seed=42)
    ranked = evaluate_manager_universe(inst)

    h1 = f"{'Rank':<4} | {'Manager':<22} | {'Alpha(HAC)':<10} | {'t(alpha)':<8}"
    h2 = f" | {'SR(Adj)':<8} | {'xi(GLM)':<8} | {'Gamma':<7} | {'DD Score':<8}"
    header = h1 + h2
    print(header)
    print("-" * len(header))
    for r in ranked:
        alpha_val = float(str(r["alpha_ann"]))
        t_val = float(str(r["t_alpha"]))
        sr_val = float(str(r["sr_adj"]))
        xi_val = float(str(r["xi"]))
        gamma_val = float(str(r["gamma"]))
        dd_val = float(str(r["dd_score"]))
        row1 = f"{r['rank']:<4} | {r['name']!s:<22} | {alpha_val * 100:+7.2f}% | {t_val:+7.2f}"
        row2 = f" | {sr_val:7.2f} | {xi_val:7.3f} | {gamma_val:+6.1f} | {dd_val:+8.4f}"
        print(row1 + row2)
    print("================================================================================")
    print("Diagnosis: TrendCTA and AlphaStar top ranking; Apex penalized for tail risk.")


main()
