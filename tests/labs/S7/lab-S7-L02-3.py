from statistics import NormalDist

import numpy as np

# SIMULATED: m independent one-sided z-tests; the first m1 hypotheses are false,
# with z-statistics centred at delta; the rest are true nulls.
rng = np.random.default_rng(3003)
m, delta, alpha, n_reps = 100, 3.5, 0.05, 4000
quantile = NormalDist().inv_cdf
holm_cuts = np.array([quantile(1 - alpha / (m + 1 - b)) for b in range(1, m + 1)])
bonferroni_cut = holm_cuts[0]

print("m1  method      power   fwer")
for m1 in (10, 50):
    is_false_null = np.arange(m) < m1
    z = rng.standard_normal((n_reps, m)) + np.where(is_false_null, delta, 0.0)
    bonferroni_reject = z > bonferroni_cut
    order = np.argsort(-z, axis=1)  # largest z first, i.e. smallest p first
    passes = np.take_along_axis(z, order, axis=1) > holm_cuts
    k = np.where(passes.all(axis=1), m, np.argmin(passes, axis=1))  # step-down stops at the first failure
    holm_reject = np.zeros_like(bonferroni_reject)
    for rep in range(n_reps):
        holm_reject[rep, order[rep, : k[rep]]] = True
    for name, rejected in (("bonferroni", bonferroni_reject), ("holm", holm_reject)):
        power = rejected[:, is_false_null].mean()
        fwer = rejected[:, ~is_false_null].any(axis=1).mean()
        print(f"{m1} {name:<11} {power:.4f} {fwer:.4f}")
