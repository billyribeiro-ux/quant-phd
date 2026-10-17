import math
from statistics import NormalDist

import numpy as np

# SIMULATED: N = 100 skill-free trials whose daily returns share a common component,
# pairwise correlation rho = 0.5, five years of daily data, 300 replications.
rng = np.random.default_rng(3707)
phi, gamma_e = NormalDist(), 0.5772156649015329
n_trials, n_obs, rho, n_reps = 100, 1260, 0.5, 300


def expected_max_z(n: float) -> float:
    return (1 - gamma_e) * phi.inv_cdf(1 - 1 / n) + gamma_e * phi.inv_cdf(1 - 1 / (n * math.e))


cross_var = np.empty(n_reps)
max_minus_mean = np.empty(n_reps)
for rep in range(n_reps):
    r = math.sqrt(rho) * rng.standard_normal((n_obs, 1)) + math.sqrt(1 - rho) * rng.standard_normal((n_obs, n_trials))
    sr = r.mean(axis=0) / r.std(axis=0, ddof=1)
    cross_var[rep] = sr.var(ddof=1)
    max_minus_mean[rep] = sr.max() - sr.mean()  # removes the common component; same expectation as the maximum

eigenvalues = np.linalg.eigvalsh(np.corrcoef(r, rowvar=False))
participation = float(eigenvalues.sum() ** 2 / (eigenvalues**2).sum())
mean_var = float(cross_var.mean())
target = math.sqrt(1 - rho) * expected_max_z(n_trials)
lo, hi = 2.0, float(n_trials)
for _ in range(60):  # bisection: the N whose expected maximum, at variance 1/T, matches the correlated case
    mid = 0.5 * (lo + hi)
    lo, hi = (mid, hi) if expected_max_z(mid) < target else (lo, mid)

print(f"T * cross-sectional variance of trial Sharpe ratios: {n_obs * mean_var:.4f} (1 - rho = {1 - rho:.4f})")
print(f"simulated expected maximum Sharpe ratio (daily): {max_minus_mean.mean():.5f}")
print(f"SR0 with raw N and cross-sectional variance: {math.sqrt(mean_var) * expected_max_z(n_trials):.5f}")
print(f"participation-ratio effective N: {participation:.2f}")
double_counted = math.sqrt(mean_var) * expected_max_z(participation)
print(f"SR0 with that effective N and cross-sectional variance: {double_counted:.5f}")
print(f"matching effective N at variance 1/T: {0.5 * (lo + hi):.2f}")
