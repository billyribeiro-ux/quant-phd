from statistics import NormalDist

import numpy as np

# SIMULATED global null: m one-sided z-tests, all hypotheses true, pairwise correlation rho.
rng = np.random.default_rng(2002)
m, alpha, n_reps = 50, 0.05, 20000
quantile = NormalDist().inv_cdf
naive_cut = quantile(1 - alpha)  # reject when z exceeds this (p <= alpha)
bonferroni_cut = quantile(1 - alpha / m)  # p <= alpha / m
holm_cuts = np.array([quantile(1 - alpha / (m + 1 - b)) for b in range(1, m + 1)])

print("rho  naive_fwer  bonferroni_fwer  holm_fwer")
for rho in (0.0, 0.5, 0.9):
    w = rng.standard_normal((n_reps, 1))
    e = rng.standard_normal((n_reps, m))
    z = np.sqrt(rho) * w + np.sqrt(1 - rho) * e
    z_max = z.max(axis=1)
    naive = np.mean(z_max > naive_cut)
    bonferroni = np.mean(z_max > bonferroni_cut)
    # Holm's step-down, run in full: sort the statistics (smallest p first), stop at the first
    # failure. Every rejection is false under the global null.
    ordered = -np.sort(-z, axis=1)
    passes = ordered > holm_cuts
    n_rejected = np.where(passes.all(axis=1), m, np.argmin(passes, axis=1))
    holm = np.mean(n_rejected > 0)
    print(f"{rho:.1f} {naive:.4f} {bonferroni:.4f} {holm:.4f}")
