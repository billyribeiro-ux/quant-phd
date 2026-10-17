import math
from statistics import NormalDist

import numpy as np

# One SIMULATED differential series with a t-statistic of exactly 2.3, copied
# into 10 identical columns. Resample whole dates (joint) or each column on its
# own (independent) and compare the first-step critical values.
rng = np.random.default_rng(5)
n_obs, n_copies, n_boot, alpha = 400, 10, 999, 0.05
z = rng.standard_normal(n_obs)
x = (z - z.mean()) / z.std(ddof=1) + 2.3 / math.sqrt(n_obs)
t_obs = x.mean() / (x.std(ddof=1) / math.sqrt(n_obs))
rank = math.ceil((1 - alpha) * n_boot)

joint = x[rng.integers(0, n_obs, size=(n_boot, n_obs))]  # every copy sees the same dates
t_joint = (joint.mean(axis=1) - x.mean()) / (joint.std(axis=1, ddof=1) / math.sqrt(n_obs))
c_joint = np.sort(t_joint)[rank - 1]  # the max over identical copies is the single statistic

apart = x[rng.integers(0, n_obs, size=(n_boot, n_copies, n_obs))]  # each copy draws its own dates
t_apart = (apart.mean(axis=2) - x.mean()) / (apart.std(axis=2, ddof=1) / math.sqrt(n_obs))
c_apart = np.sort(t_apart.max(axis=1))[rank - 1]

phi = NormalDist()
print(f"observed t-statistic of every copy: {t_obs:.3f}")
print(f"critical value, joint resampling: {c_joint:.3f}  rejects all copies: {t_obs > c_joint}")
print(f"critical value, independent resampling: {c_apart:.3f}  rejects all copies: {t_obs > c_apart}")
print(f"normal benchmarks: one statistic {phi.inv_cdf(0.95):.3f}, max of 10 independent {phi.inv_cdf(0.95**0.1):.3f}")
