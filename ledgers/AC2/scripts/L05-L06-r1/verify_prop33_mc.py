"""Monte Carlo check of Proposition 3.3 (mean error of OLS without intercept) with its Monte Carlo standard error.

Written by the L05-L06 verifier. Run: python -I verify_prop33_mc.py
"""

import numpy as np

rng = np.random.default_rng(1)
n = 4000
lagp = np.exp(rng.normal(np.log(1000.0), 0.6, n))
Xp = np.column_stack([1 / lagp, rng.normal(0, 0.1, n) / lagp, rng.uniform(0.2, 0.6, n)])
bstar = np.array([0.05, 0.10, -0.08])
d = 0.01 * (1 / lagp > np.median(1 / lagp)) * 1.0
formula = np.linalg.solve(Xp.T @ Xp, Xp.T @ d)
reps = []
for _ in range(2000):
    u = rng.normal(0, 0.005, n)
    yv = Xp @ bstar + d + u
    reps.append(np.linalg.solve(Xp.T @ Xp, Xp.T @ yv) - bstar)
reps = np.array(reps)
mc = reps.mean(axis=0)
mc_se = reps.std(axis=0, ddof=1) / np.sqrt(len(reps))
for j in range(3):
    print(f"coef{j + 1} formula {formula[j]:.6f} mc_mean {mc[j]:.6f} mc_se {mc_se[j]:.6f} z_diff {(mc[j] - formula[j]) / mc_se[j]:.2f}")
proj_len = np.linalg.norm(Xp @ formula)
print(f"shape_of_formula {formula.shape} shape_of_projection {(Xp @ formula).shape} projection_norm {proj_len:.6f}")
