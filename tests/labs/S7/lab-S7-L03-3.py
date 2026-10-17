import math

import numpy as np

# SIMULATED equicorrelated one-sided z-tests: z_i = sqrt(rho) W + sqrt(1 - rho) e_i + mu_i.
rng = np.random.default_rng(304)
m, m1, q, n_reps, effect = 500, 50, 0.10, 1000, 3.0
upper_tail = np.frompyfunc(lambda z: 0.5 * math.erfc(z / math.sqrt(2.0)), 1, 1)
mu = np.zeros(m)
mu[:m1] = effect

print("rho  mean_FDP  sd_FDP  p95_FDP  P(FDP>0.2)")
for rho in (0.0, 0.5, 0.8):
    w = rng.standard_normal((n_reps, 1))
    z = math.sqrt(rho) * w + math.sqrt(1.0 - rho) * rng.standard_normal((n_reps, m)) + mu
    p = upper_tail(z).astype(float)
    ordered = np.sort(p, axis=1)
    passing = ordered <= q * np.arange(1, m + 1) / m
    r = np.where(passing.any(axis=1), m - np.argmax(passing[:, ::-1], axis=1), 0)
    rejected = p <= (q * r / m)[:, None]
    fdp = rejected[:, m1:].sum(axis=1) / np.maximum(r, 1)
    print(f"{rho:.1f} {fdp.mean():.4f} {fdp.std():.4f} {np.quantile(fdp, 0.95):.4f} {np.mean(fdp > 0.2):.4f}")
