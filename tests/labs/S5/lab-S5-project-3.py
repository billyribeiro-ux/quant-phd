"""Lab S5-project-3: Rung 3 independent verification check.

SIMULATED: runs the two-pass Fama-MacBeth pipeline with Shanken correction
on the public demonstration instance (seed 0), printing the replication table
and verifying mathematical invariants.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # Public demonstration parameters (seed 0)
    seed = 0
    rng = np.random.default_rng(seed)
    t_months = 130
    n_assets = 14
    k_factors = 1
    train = int(t_months * 0.60)  # 78
    t2 = t_months - train  # 52

    # Factor dynamics
    sigma_f = np.array([[0.0025]])
    mu_f = np.array([0.008])
    factors = rng.multivariate_normal(mu_f, sigma_f, size=t_months)

    true_loadings = rng.uniform(0.5, 1.5, size=(n_assets, k_factors))
    true_alphas = rng.normal(0.0, 0.001, size=n_assets)
    resid_sd = rng.uniform(0.02, 0.05, size=n_assets)

    excess = np.empty((t_months, n_assets), dtype=np.float64)
    for t in range(t_months):
        e_t = rng.normal(0.0, resid_sd, size=n_assets)
        excess[t] = true_alphas + true_loadings @ factors[t] + e_t

    # Step 1: First-pass OLS
    x_ts = np.column_stack([np.ones(train), factors[:train]])
    x_inv = np.linalg.inv(x_ts.T @ x_ts)
    betas = np.empty((n_assets, k_factors + 1))
    for i in range(n_assets):
        betas[i] = x_inv @ (x_ts.T @ excess[:train, i])

    # Step 2: Second-pass cross-sectional OLS
    z_cs = np.column_stack([np.ones(n_assets), betas[:, 1:]])
    z_inv = np.linalg.inv(z_cs.T @ z_cs)
    slopes = np.empty((t2, k_factors + 1))
    for i in range(t2):
        slopes[i] = z_inv @ (z_cs.T @ excess[train + i])

    premia = np.mean(slopes, axis=0)
    naive_se = np.std(slopes, axis=0, ddof=1) / np.sqrt(t2)

    # Shanken correction
    factor_cov = np.cov(factors[train:], rowvar=False, ddof=1).reshape((k_factors, k_factors))
    lambda_f = premia[1:].reshape((k_factors, 1))
    q = float((lambda_f.T @ np.linalg.solve(factor_cov, lambda_f)).item())
    c = 1.0 + q
    shanken_se = naive_se * np.sqrt(c)

    # Invariant checks
    assert premia.shape == (k_factors + 1,), "premia dimension mismatch"
    assert np.all(shanken_se >= naive_se), "Shanken SE must be >= naive SE"
    assert c >= 1.0, "Shanken correction multiplier c must be >= 1.0"

    print("Rung 3 Independent Verification Table (Seed 0)")
    print(f"  Configuration: T={t_months}, N={n_assets}, K={k_factors}, T1={train}, T2={t2}")
    print("  Parameter | Estimated Premium | Naive SE    | Shanken SE  | Ratio Shanken/Naive")
    print("  " + "-" * 75)
    names = ["Zero-Beta Intercept", "Factor 1 Premium"]
    for idx, name in enumerate(names):
        ratio = shanken_se[idx] / naive_se[idx]
        p_str = f"{premia[idx]:+.6f}"
        nse_str = f"{naive_se[idx]:.6f}"
        sse_str = f"{shanken_se[idx]:.6f}"
        print(f"  {name:<20} | {p_str}        | {nse_str}   | {sse_str}   | {ratio:.4f}")
    print(f"  Shanken multiplier c: {c:.6f}")
    print("  Status: All mathematical invariants satisfied.")


main()
