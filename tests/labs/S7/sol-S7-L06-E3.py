from statistics import NormalDist

import numpy as np

# SIMULATED literature: 400 tested predictors, a share pi1 real with t ~ N(3, 1), the rest null.
# "Published" means |t| > 1.96. Holm at 5% is applied to all 400 two-sided tests.
rng = np.random.default_rng(64)
phi = NormalDist()
m, reps, alpha = 400, 400, 0.05
holm_cut = np.array([alpha / (m - j) for j in range(m)])  # alpha / (m + 1 - k) for ranks k = 1..m

print("pi1  null_share_of_published  holm_unrejected_share_of_published  mean_holm_hurdle")
for pi1 in (0.1, 0.3, 0.6):
    null_share, unrejected, hurdle = [], [], []
    for _ in range(reps):
        real = rng.random(m) < pi1
        t = rng.standard_normal(m) + np.where(real, 3.0, 0.0)
        p = np.array([2.0 * (1.0 - phi.cdf(abs(float(x)))) for x in t])
        order = np.argsort(p)
        fail = np.nonzero(p[order] > holm_cut)[0]
        stop = int(fail[0]) if fail.size else m  # Holm rejects the `stop` smallest p-values
        rejected = np.zeros(m, dtype=bool)
        rejected[order[:stop]] = True
        published = np.abs(t) > 1.96
        null_share.append(np.mean(~real[published]))
        unrejected.append(np.mean(~rejected[published]))
        hurdle.append(phi.inv_cdf(1.0 - holm_cut[min(stop, m - 1)] / 2.0))
    print(f"{pi1} {np.mean(null_share):.3f} {np.mean(unrejected):.3f} {np.mean(hurdle):.2f}")
