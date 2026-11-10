"""Lab S5-project-2: Rung 2 completion challenge for two-pass asset pricing.

SIMULATED: interactive completion problem implementing the second-pass slope averaging
and the Shanken correction factor calculation.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    seed = 84
    rng = np.random.default_rng(seed)
    t_months = 150
    n_assets = 16
    k_factors = 1
    train = 90
    t2 = t_months - train

    factors = rng.normal(0.007, 0.042, size=(t_months, k_factors))
    betas_true = rng.uniform(0.7, 1.3, size=(n_assets, k_factors))
    resid_sd = rng.uniform(0.02, 0.05, size=n_assets)

    excess = np.empty((t_months, n_assets))
    for t in range(t_months):
        e_t = rng.normal(0.0, resid_sd, size=n_assets)
        excess[t] = (betas_true @ factors[t]).ravel() + e_t

    # Step 1: First pass
    x_ts = np.column_stack([np.ones(train), factors[:train]])
    betas_est = np.empty((n_assets, k_factors + 1))
    for i in range(n_assets):
        betas_est[i] = np.linalg.solve(x_ts.T @ x_ts, x_ts.T @ excess[:train, i])

    # Step 2: Second pass
    z_cs = np.column_stack([np.ones(n_assets), betas_est[:, 1:]])
    slopes = np.empty((t2, k_factors + 1))
    for i in range(t2):
        month = train + i
        slopes[i] = np.linalg.solve(z_cs.T @ z_cs, z_cs.T @ excess[month])

    # Blank 1 to complete on page: premia = np.mean(slopes, axis=0)
    premia = np.mean(slopes, axis=0)

    # Blank 2 to complete on page: naive_se = np.std(slopes, axis=0, ddof=1) / np.sqrt(t2)
    naive_se = np.std(slopes, axis=0, ddof=1) / np.sqrt(t2)

    # Blank 3 to complete on page: c = 1.0 + q
    factor_cov = np.cov(factors[train:], rowvar=False, ddof=1).reshape((k_factors, k_factors))
    lambda_f = premia[1:].reshape((k_factors, 1))
    q = float((lambda_f.T @ np.linalg.solve(factor_cov, lambda_f)).item())
    c = 1.0 + q

    shanken_se = naive_se * np.sqrt(c)

    print("Rung 2 Completion Challenge Check:")
    print(f"  Processed months: {t_months}, Assets: {n_assets} (seed {seed})")
    print(f"  Factor risk premium: {premia[1]:.6f}")
    print(f"  Naive standard error: {naive_se[1]:.6f}")
    print(f"  Shanken multiplier c: {c:.4f}")
    print(f"  Shanken standard error: {shanken_se[1]:.6f}")
    print(f"  Invariant verified (shanken_se >= naive_se): {shanken_se[1] >= naive_se[1]}")


main()
