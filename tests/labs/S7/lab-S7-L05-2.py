import math
from statistics import NormalDist

import numpy as np

# SIMULATED global null: 8 strategies with zero mean differentials, correlated
# through a common factor. Compare a per-test 5% rule with the studentized
# bootstrap max-t critical value (whole dates resampled jointly, block length 1
# because these SIMULATED returns are serially independent).
rng = np.random.default_rng(55)
n_obs, n_strat, n_boot, n_reps, alpha = 200, 8, 199, 400, 0.05
per_test = NormalDist().inv_cdf(1 - alpha)
rank = math.ceil((1 - alpha) * n_boot)

naive_false = boot_false = 0
for _ in range(n_reps):
    d = 0.6 * rng.standard_normal((n_obs, 1)) + 0.8 * rng.standard_normal((n_obs, n_strat))
    means = d.mean(axis=0)
    t = means / (d.std(axis=0, ddof=1) / math.sqrt(n_obs))
    sample = d[rng.integers(0, n_obs, size=(n_boot, n_obs))]  # (B, T, K): one date vector per draw
    t_star = (sample.mean(axis=1) - means) / (sample.std(axis=1, ddof=1) / math.sqrt(n_obs))
    critical = np.sort(t_star.max(axis=1))[rank - 1]
    naive_false += int((t > per_test).any())
    boot_false += int((t > critical).any())

print(f"per-test critical value: {per_test:.3f}")
print(f"FWER with per-test 5% rule: {naive_false / n_reps:.3f}")
print(f"FWER with bootstrap max-t (first step of StepM): {boot_false / n_reps:.3f}")
