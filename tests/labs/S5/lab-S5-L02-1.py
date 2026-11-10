"""Lab S5-L02-1: Identity versus efficient weighting in over-identified GMM.

SIMULATED: generates synthetic samples for an over-identified linear model (q=3, k=1)
with conditional heteroskedasticity, computes two-step GMM with identity weighting and
efficient weighting W = S^(-1), and verifies variance reduction under optimal weighting.
"""

from __future__ import annotations

import numpy as np


def estimate_two_step(z: np.ndarray, x: np.ndarray, y: np.ndarray) -> tuple[float, float, float, float]:
    """Perform two-step GMM estimation and return estimates and asymptotic variances."""
    n = len(y)
    s_zx = (z.T @ x) / n  # (q,)
    s_zy = (z.T @ y) / n  # (q,)

    # Step 1: Identity weight W1 = I
    denom1 = float(s_zx.T @ s_zx)
    theta1 = float(s_zx.T @ s_zy) / denom1

    # Residuals and moment covariance estimator S_hat
    resid1 = y - x * theta1
    g_mat = z * resid1[:, np.newaxis]  # (n, q)
    s_hat = (g_mat.T @ g_mat) / n  # (q, q)
    s_inv = np.linalg.inv(s_hat)

    # Asymptotic variance for Step 1 (sandwich formula)
    # D = -s_zx => (D' W D)^(-1) D' W S W D (D' W D)^(-1)
    avar1 = float((s_zx.T @ s_hat @ s_zx) / (denom1**2))

    # Step 2: Efficient weight W2 = S_inv
    denom2 = float(s_zx.T @ s_inv @ s_zx)
    theta2 = float(s_zx.T @ s_inv @ s_zy) / denom2
    avar2 = float(1.0 / denom2)

    return theta1, theta2, avar1, avar2


def main() -> None:
    seed = 101
    rng = np.random.default_rng(seed)
    n = 600
    q = 3
    theta_true = 2.50

    # True instrument coefficients
    gamma = np.array([0.5, 1.0, 1.5])
    reps = 800

    estimates_step1 = np.empty(reps)
    estimates_step2 = np.empty(reps)

    # Run Monte Carlo replications with conditional heteroskedasticity
    for r in range(reps):
        z_r = rng.normal(0.0, 1.0, size=(n, q))
        u_r = rng.normal(0.0, 0.4, size=n)
        # Conditional heteroskedasticity: variance scales with z_1
        vol_r = 0.4 + 1.2 * np.abs(z_r[:, 0])
        eps_r = vol_r * rng.normal(0.0, 1.0, size=n)
        x_r = z_r @ gamma + u_r
        y_r = theta_true * x_r + eps_r

        t1, t2, _, _ = estimate_two_step(z_r, x_r, y_r)
        estimates_step1[r] = t1
        estimates_step2[r] = t2

    # Point estimate and asymptotic variances on the primary sample (rep 0)
    z0 = rng.normal(0.0, 1.0, size=(n, q))
    u0 = rng.normal(0.0, 0.4, size=n)
    vol0 = 0.4 + 1.2 * np.abs(z0[:, 0])
    eps0 = vol0 * rng.normal(0.0, 1.0, size=n)
    x0 = z0 @ gamma + u0
    y0 = theta_true * x0 + eps0

    th1, th2, avar1, avar2 = estimate_two_step(z0, x0, y0)

    mc_var1 = float(np.var(estimates_step1, ddof=1))
    mc_var2 = float(np.var(estimates_step2, ddof=1))
    mc_se_diff = float(np.sqrt(2.0 / reps) * mc_var2)

    efficiency_gain_pct = (1.0 - avar2 / avar1) * 100.0
    empirical_gain_pct = (1.0 - mc_var2 / mc_var1) * 100.0

    print("Lab S5-L02-1: Efficient GMM Weighting vs Identity Weighting")
    print(f"  Sample size T: {n}, Moments q: {q}, Parameter k: 1 (SIMULATED, seed {seed})")
    print(f"  Step 1 (Identity W=I) estimate: {th1:.6f}, Asymptotic Var: {avar1:.6f}")
    print(f"  Step 2 (Efficient W=S^-1) estimate: {th2:.6f}, Asymptotic Var: {avar2:.6f}")
    print(f"  Analytical asymptotic variance reduction: {efficiency_gain_pct:.2f}%")
    print(f"  Monte Carlo empirical Var(theta_1): {mc_var1:.6f}")
    print(f"  Monte Carlo empirical Var(theta_2): {mc_var2:.6f} (MC SE: {mc_se_diff:.6f})")
    print(f"  Monte Carlo empirical variance reduction: {empirical_gain_pct:.2f}%")
    print(f"  Efficiency condition Var(theta_2) < Var(theta_1): {avar2 < avar1 and mc_var2 < mc_var1}")


main()
