"""Lab F7-L04-1: GLM (2004) Constrained Maximum Likelihood Return Unsmoothing.

Implements the Getmansky, Lo & Makarov (2004) econometric moving-average
return unsmoothing framework. Estimates smoothing coefficients theta_0, ..., theta_k
via constrained maximum likelihood, evaluates the illiquidity score xi, and recovers
unbiased true volatility and unsmoothed Sharpe ratios.
"""

from __future__ import annotations

import numpy as np
import scipy.linalg
import scipy.optimize


def run_glm_unsmoothing(seed: int = 42) -> dict[str, float]:
    """Estimate GLM (2004) MA(2) smoothing parameters via constrained MLE."""
    rng = np.random.default_rng(seed)
    n_months = 180  # 15 years

    # 1. Ground truth parameters:
    # theta = [0.60, 0.25, 0.15], sum(theta) = 1.0
    theta_true = np.array([0.60, 0.25, 0.15])
    true_sigma_mo = 0.045
    true_mu_mo = 0.0075
    xi_true = float(np.sum(theta_true**2))

    # 2. Simulate true latent returns and smoothed reported returns
    r_star = rng.normal(true_mu_mo, true_sigma_mo, size=n_months + 2)
    r_obs = np.zeros(n_months)
    for t in range(n_months):
        r_obs[t] = theta_true[0] * r_star[t + 2] + theta_true[1] * r_star[t + 1] + theta_true[2] * r_star[t]

    # 3. Reported statistics
    sample_mean = float(np.mean(r_obs))
    sample_vol_obs = float(np.std(r_obs, ddof=1))
    demeaned = r_obs - sample_mean

    # 4. Constrained Maximum Likelihood Estimation of MA(2):
    # theta_0, theta_1, sigma (with theta_2 = 1 - theta_0 - theta_1 >= 0)
    def neg_log_lik(params: np.ndarray) -> float:
        t0, t1, sig = float(params[0]), float(params[1]), float(params[2])
        t2 = 1.0 - t0 - t1
        if t2 < -1e-7 or t0 < 0.0 or t1 < 0.0 or sig <= 1e-6:
            return 1e10
        t2 = max(0.0, t2)
        th = np.array([t0, t1, t2])

        # Autocovariances for MA(2)
        g0 = (sig**2) * float(np.sum(th**2))
        g1 = (sig**2) * float(th[0] * th[1] + th[1] * th[2])
        g2 = (sig**2) * float(th[0] * th[2])

        c = np.zeros(n_months)
        c[0], c[1], c[2] = g0, g1, g2
        try:
            cov_mat = scipy.linalg.toeplitz(c) + np.eye(n_months) * 1e-8
            chol_l = scipy.linalg.cholesky(cov_mat, lower=True)
            log_det = 2.0 * float(np.sum(np.log(np.diag(chol_l))))
            y_vec = scipy.linalg.solve_triangular(chol_l, demeaned, lower=True)
            quad_form = float(np.sum(y_vec**2))
            return float(0.5 * (float(n_months) * np.log(2.0 * np.pi) + log_det + quad_form))
        except Exception:
            return 1e10

    # Optimization with multi-start search
    best_res = None
    best_nll = 1e10
    bounds = [(0.05, 0.95), (0.00, 0.95), (1e-4, 1.0)]
    cons = ({"type": "ineq", "fun": lambda p: 1.0 - p[0] - p[1]},)

    for init_t0 in [0.75, 0.55, 0.40]:
        init_t1 = (1.0 - init_t0) * 0.5
        init_sig = sample_vol_obs / np.sqrt(init_t0**2 + init_t1**2 + (1.0 - init_t0 - init_t1) ** 2)
        res = scipy.optimize.minimize(
            neg_log_lik,
            np.array([init_t0, init_t1, init_sig]),
            bounds=bounds,
            constraints=cons,
            method="SLSQP",
        )
        if res.success and res.fun < best_nll:
            best_nll = float(res.fun)
            best_res = res

    assert best_res is not None
    theta_0_hat = float(best_res.x[0])
    theta_1_hat = float(best_res.x[1])
    theta_2_hat = max(0.0, 1.0 - theta_0_hat - theta_1_hat)
    sigma_star_hat = float(best_res.x[2])

    # 5. Illiquidity concentration index xi = sum theta_j^2
    xi_hat = float(theta_0_hat**2 + theta_1_hat**2 + theta_2_hat**2)

    # Annualized metrics
    vol_reported_ann = float(sample_vol_obs * np.sqrt(12.0) * 100.0)
    vol_true_ann = float(true_sigma_mo * np.sqrt(12.0) * 100.0)
    vol_unsmoothed_ann = float(sigma_star_hat * np.sqrt(12.0) * 100.0)

    sr_reported = float((sample_mean / sample_vol_obs) * np.sqrt(12.0))
    sr_unsmoothed = float((sample_mean / sigma_star_hat) * np.sqrt(12.0))

    return {
        "theta_0_true": round(float(theta_true[0]), 3),
        "theta_1_true": round(float(theta_true[1]), 3),
        "theta_2_true": round(float(theta_true[2]), 3),
        "theta_0_hat": round(theta_0_hat, 3),
        "theta_1_hat": round(theta_1_hat, 3),
        "theta_2_hat": round(theta_2_hat, 3),
        "xi_true": round(xi_true, 4),
        "xi_hat": round(xi_hat, 4),
        "vol_reported_ann": round(vol_reported_ann, 2),
        "vol_true_ann": round(vol_true_ann, 2),
        "vol_unsmoothed_ann": round(vol_unsmoothed_ann, 2),
        "sr_reported": round(sr_reported, 4),
        "sr_unsmoothed": round(sr_unsmoothed, 4),
    }


def main() -> None:
    print("Lab F7-L04-1 | GLM (2004) Constrained Maximum Likelihood Unsmoothing")
    print("--------------------------------------------------------------------")
    res = run_glm_unsmoothing(seed=42)
    print(
        f"True Smoothing Weights:      theta = [{res['theta_0_true']}, "
        f"{res['theta_1_true']}, {res['theta_2_true']}] (xi = {res['xi_true']:.4f})"
    )
    print(
        f"GLM Estimated Weights:       theta = [{res['theta_0_hat']}, "
        f"{res['theta_1_hat']}, {res['theta_2_hat']}] (xi = {res['xi_hat']:.4f})"
    )
    print(f"Reported Annualized Vol:     {res['vol_reported_ann']:.2f}% (Sharpe: {res['sr_reported']:.4f})")
    print(f"True Latent Volatility:      {res['vol_true_ann']:.2f}%")
    print(f"GLM Unsmoothed Volatility:   {res['vol_unsmoothed_ann']:.2f}% (Sharpe: {res['sr_unsmoothed']:.4f})")


main()
