"""Lab S5-project-1: Rung 1 worked example of two-pass asset pricing with Shanken correction.

SIMULATED: runs a fully solved, annotated execution of the two-pass Fama-MacBeth pipeline
on a seeded synthetic panel, printing factor loadings, monthly premia slopes, naive standard errors,
the Shanken errors-in-variables multiplier, and corrected inference.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    seed = 42
    rng = np.random.default_rng(seed)
    t_months = 140
    n_assets = 15
    k_factors = 1
    train = 80
    t2 = t_months - train

    # Generate synthetic factors and returns
    f_mean = 0.008
    f_sd = 0.040
    factors = rng.normal(f_mean, f_sd, size=(t_months, k_factors))
    betas_true = rng.uniform(0.6, 1.4, size=(n_assets, k_factors))
    resid_sd = rng.uniform(0.02, 0.05, size=n_assets)

    excess = np.empty((t_months, n_assets))
    for t in range(t_months):
        e_t = rng.normal(0.0, resid_sd, size=n_assets)
        excess[t] = (betas_true @ factors[t]).ravel() + e_t

    # Step 1: First-pass time-series regression on first train months
    x_ts = np.column_stack([np.ones(train), factors[:train]])
    betas_est = np.empty((n_assets, k_factors + 1))
    for i in range(n_assets):
        betas_est[i] = np.linalg.solve(x_ts.T @ x_ts, x_ts.T @ excess[:train, i])

    # Step 2: Second-pass cross-sectional regressions on test months
    z_cs = np.column_stack([np.ones(n_assets), betas_est[:, 1:]])
    slopes = np.empty((t2, k_factors + 1))
    for i in range(t2):
        month = train + i
        slopes[i] = np.linalg.solve(z_cs.T @ z_cs, z_cs.T @ excess[month])

    premia = np.mean(slopes, axis=0)
    naive_se = np.std(slopes, axis=0, ddof=1) / np.sqrt(t2)

    # Step 3: Shanken errors-in-variables correction
    factor_cov = np.cov(factors[train:], rowvar=False, ddof=1).reshape((k_factors, k_factors))
    lambda_f = premia[1:].reshape((k_factors, 1))
    q = float((lambda_f.T @ np.linalg.solve(factor_cov, lambda_f)).item())
    c = 1.0 + q
    shanken_se = naive_se * np.sqrt(c)

    t_naive = premia[1] / naive_se[1]
    t_shanken = premia[1] / shanken_se[1]

    print("Rung 1 Worked Example: Two-Pass Asset Pricing")
    print(f"  Sample size T: {t_months}, Assets N: {n_assets}, Training T1: {train}, Test T2: {t2} (seed {seed})")
    print(f"  First-pass mean factor loading beta: {np.mean(betas_est[:, 1]):.4f}")
    print(f"  Estimated factor risk premium: {premia[1]:.6f}")
    print(f"  Shanken correction factor c: {c:.4f} (Multiplier sqrt(c): {np.sqrt(c):.4f})")
    print(f"  Naive Fama-MacBeth SE: {naive_se[1]:.6f} (t-statistic: {t_naive:.3f})")
    print(f"  Shanken-corrected SE:  {shanken_se[1]:.6f} (t-statistic: {t_shanken:.3f})")
    print(f"  Standard error inflation: {((np.sqrt(c) - 1.0) * 100.0):.2f}%")


main()
