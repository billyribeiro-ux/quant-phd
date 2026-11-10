"""Lab S5-L03-1: Hansen's J-test of overidentifying restrictions.

SIMULATED: generates synthetic samples for an over-identified GMM system (q=4, k=1, df=3),
evaluates Hansen's J-statistic on a primary sample, and computes the empirical rejection rate
at the nominal 5% significance level across 1000 Monte Carlo replications under the null hypothesis.
"""

from __future__ import annotations

import numpy as np
import scipy.stats


def compute_j_stat(z: np.ndarray, x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    """Compute two-step GMM estimator, Hansen J-statistic, and p-value."""
    n = len(y)
    q = z.shape[1]
    s_zx = (z.T @ x) / n  # (q,)
    s_zy = (z.T @ y) / n  # (q,)

    # Step 1: Identity weight
    theta1 = float((s_zx.T @ s_zy) / (s_zx.T @ s_zx))

    # Step 2: Efficient weight S_inv
    resid1 = y - x * theta1
    g_mat = z * resid1[:, np.newaxis]
    s_hat = (g_mat.T @ g_mat) / n
    s_inv = np.linalg.inv(s_hat)

    denom2 = float(s_zx.T @ s_inv @ s_zx)
    theta2 = float((s_zx.T @ s_inv @ s_zy) / denom2)

    # Hansen J-statistic: n * g_bar(theta2)' * S_inv * g_bar(theta2)
    resid2 = y - x * theta2
    g_bar = (z.T @ resid2) / n  # (q,)
    j_stat = float(n * (g_bar.T @ s_inv @ g_bar))

    df = q - 1
    p_val = float(scipy.stats.chi2.sf(j_stat, df=df))
    return theta2, j_stat, p_val


def main() -> None:
    seed = 202
    rng = np.random.default_rng(seed)
    n = 500
    q = 4
    k = 1
    df = q - k
    theta_true = 1.60
    gamma = np.array([0.7, -0.9, 1.1, 0.5])
    reps = 1000

    # Primary realization
    z0 = rng.normal(0.0, 1.0, size=(n, q))
    u0 = rng.normal(0.0, 0.5, size=n)
    eps0 = 0.4 * u0 + rng.normal(0.0, 0.7, size=n)
    x0 = z0 @ gamma + u0
    y0 = theta_true * x0 + eps0

    th0, j0, p0 = compute_j_stat(z0, x0, y0)
    crit_95 = float(scipy.stats.chi2.ppf(0.95, df=df))

    # Monte Carlo simulation of size under null
    rejections = 0
    for _ in range(reps):
        z_r = rng.normal(0.0, 1.0, size=(n, q))
        u_r = rng.normal(0.0, 0.5, size=n)
        eps_r = 0.4 * u_r + rng.normal(0.0, 0.7, size=n)
        x_r = z_r @ gamma + u_r
        y_r = theta_true * x_r + eps_r

        _, j_r, _ = compute_j_stat(z_r, x_r, y_r)
        if j_r > crit_95:
            rejections += 1

    emp_size = rejections / reps
    mc_se = float(np.sqrt(emp_size * (1.0 - emp_size) / reps))

    print("Lab S5-L03-1: Hansen's J-Test Under the Null Hypothesis")
    print(f"  Sample size T: {n}, Moments q: {q}, Regressors k: {k}, df: {df} (SIMULATED, seed {seed})")
    print(f"  Primary sample GMM estimate: {th0:.6f}")
    print(f"  Primary sample J-statistic: {j0:.4f} (p-value: {p0:.4f})")
    print(f"  Chi-squared(3) 95% critical threshold: {crit_95:.4f}")
    print(f"  Primary sample null accepted (J <= crit): {j0 <= crit_95}")
    print(f"  Monte Carlo empirical size (R={reps}): {emp_size:.4f} (MC SE: {mc_se:.4f})")
    print(f"  Nominal 5% coverage within 2 SEs: {abs(emp_size - 0.05) <= 2.0 * mc_se}")


main()
