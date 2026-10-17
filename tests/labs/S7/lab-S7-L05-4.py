import math
from statistics import NormalDist

import numpy as np

# SIMULATED returns version of Lab 1's universe: 20 strategies over 250 serially independent periods,
# unit-variance differentials with pairwise correlation rho, and eight true alphas whose expected
# t-statistics are Lab 1's drifts. Three 95% bands for the 20 means: pointwise, Bonferroni, and the
# sup-t band from the joint bootstrap draws of Definition 1.1 (block length 1, as in Lab 2).
rng = np.random.default_rng(506)
n_obs, n_strat, n_boot, n_reps, alpha = 250, 20, 199, 400, 0.05
drift = np.zeros(n_strat)
drift[:8] = [4.5, 4.0, 3.6, 3.3, 3.1, 2.9, 2.8, 2.7]
mu = drift / math.sqrt(n_obs)  # true mean differentials, per period
normal = NormalDist()
z_pointwise = normal.inv_cdf(1 - alpha / 2)
z_bonferroni = normal.inv_cdf(1 - alpha / (2 * n_strat))
rank = math.ceil((1 - alpha) * n_boot)
cells = n_obs * np.arange(n_boot)[:, None]  # offsets that place draw b's dates in row b of a (B, T) table

print("rho  band  mean_critical_value  simultaneous_coverage")
for rho in (0.3, 0.9):
    covered = np.zeros(3)
    one_interval = 0.0
    c_band = np.empty(n_reps)
    c_stepm = np.empty(n_reps)
    for rep in range(n_reps):
        d = (
            mu
            + math.sqrt(rho) * rng.standard_normal((n_obs, 1))
            + math.sqrt(1 - rho) * rng.standard_normal((n_obs, n_strat))
        )
        means, se = d.mean(axis=0), d.std(axis=0, ddof=1) / math.sqrt(n_obs)
        # Joint bootstrap of whole dates: weight[b, t] is the share of draw b's rows that are date t,
        # so one matrix product gives every strategy's resampled mean and second moment.
        dates = rng.integers(0, n_obs, size=(n_boot, n_obs))
        weight = np.bincount((dates + cells).ravel(), minlength=n_boot * n_obs).reshape(n_boot, n_obs) / n_obs
        boot_mean = weight @ d
        boot_se = np.sqrt((weight @ (d * d) - boot_mean**2) / (n_obs - 1))  # s*/sqrt(T), divisor T - 1
        t_star = (boot_mean - means) / boot_se
        c_band[rep] = np.sort(np.abs(t_star).max(axis=1))[rank - 1]  # two-sided, over all 20 strategies
        c_stepm[rep] = np.sort(t_star.max(axis=1))[rank - 1]  # StepM's first-step critical value
        tau = np.abs(means - mu) / se
        covered += [tau.max() <= z_pointwise, tau.max() <= z_bonferroni, tau.max() <= c_band[rep]]
        one_interval += float(np.mean(tau <= z_pointwise))
    print(f"{rho:.1f} pointwise {z_pointwise:.3f} {covered[0] / n_reps:.3f}")
    print(f"{rho:.1f} Bonferroni {z_bonferroni:.3f} {covered[1] / n_reps:.3f}")
    print(f"{rho:.1f} sup-t {c_band.mean():.3f} {covered[2] / n_reps:.3f}")
    print(f"{rho:.1f} coverage of one pointwise interval: {one_interval / n_reps:.3f}")
    print(f"{rho:.1f} StepM first-step critical value: {c_stepm.mean():.3f}")
