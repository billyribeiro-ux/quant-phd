"""Lab CAP3-L03-1: Field Prelim II, Problem A: Two-Step Efficient GMM & Hansen J-Test.

Estimates consumption Euler equation parameters via two-step GMM and tests
overidentifying restrictions using the Hansen (1982) J-test.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2


def main() -> None:
    # 1. Simulate consumption growth and gross return instruments
    np.random.seed(101)
    t_obs = 300
    true_beta = 0.98
    true_gamma = 2.5

    # Simulated log consumption growth and gross asset returns
    gc = np.random.normal(0.015, 0.020, size=t_obs)
    # R gross satisfying E[beta * (C_{t+1}/C_t)^{-gamma} * R_{t+1} - 1 | Z_t] = 0
    c_growth = np.exp(gc)
    sdf_true = true_beta * (c_growth ** (-true_gamma))
    r_equity = (1.0 + np.random.normal(0.025, 0.05, size=t_obs)) / np.mean(sdf_true)
    r_bond = (1.0 + np.random.normal(0.008, 0.02, size=t_obs)) / np.mean(sdf_true)

    # 4 moment conditions: [R_e * m - 1, R_b * m - 1, (R_e * m - 1) * z_t, (R_b * m - 1) * z_t]
    z_inst = np.random.normal(0.0, 1.0, size=t_obs)

    def moment_func(params: np.ndarray) -> np.ndarray:
        b, g = params
        m = b * (c_growth ** (-g))
        e1 = r_equity * m - 1.0
        e2 = r_bond * m - 1.0
        m1 = e1
        m2 = e2
        m3 = e1 * z_inst
        m4 = e2 * z_inst
        return np.column_stack([m1, m2, m3, m4])  # T x 4

    # Step 1: First-stage GMM with identity weighting
    w1 = np.eye(4)

    def gmm_obj(params: np.ndarray, w_mat: np.ndarray) -> float:
        f = moment_func(params)
        g_bar = np.mean(f, axis=0)
        return float(g_bar @ w_mat @ g_bar)

    res1 = minimize(gmm_obj, np.array([0.95, 2.0]), args=(w1,), method="Nelder-Mead")
    theta1 = res1.x

    # Step 2: Compute spectral density matrix S and efficient weighting matrix W = S^{-1}
    f_res1 = moment_func(theta1)
    s_mat = (f_res1.T @ f_res1) / float(t_obs)
    w_eff = np.linalg.inv(s_mat)

    res2 = minimize(gmm_obj, theta1, args=(w_eff,), method="Nelder-Mead")
    theta_eff = res2.x

    # Step 3: Hansen J-test
    f_res2 = moment_func(theta_eff)
    g_bar_eff = np.mean(f_res2, axis=0)
    j_stat = float(t_obs * (g_bar_eff @ w_eff @ g_bar_eff))
    df = 4 - 2  # 4 moments, 2 parameters
    p_val = float(chi2.sf(j_stat, df))

    print(f"Sample Size (T): {t_obs}")
    print(f"First-Stage Estimates: beta = {theta1[0]:.4f}, gamma = {theta1[1]:.4f}")
    print(f"Efficient Two-Step Estimates: beta = {theta_eff[0]:.4f}, gamma = {theta_eff[1]:.4f}")
    print(f"Hansen J-Statistic: {j_stat:.4f} (df = {df})")
    print(f"J-Test p-value: {p_val:.4f} (Model Valid: {p_val > 0.05})")


main()
