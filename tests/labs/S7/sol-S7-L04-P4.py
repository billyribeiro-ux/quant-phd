import math
from statistics import NormalDist

import numpy as np

# SIMULATED global tests of K = 100 independent one-sided z-statistics at level 0.05: the maximum, the
# normalized sum and Fisher's combination, against a sparse and a dense alternative.
rng = np.random.default_rng(4042)
K, alpha, n_reps = 100, 0.05, 20000
nd = NormalDist()
c_max = nd.inv_cdf((1 - alpha) ** (1 / K))  # exact critical value of max_k Z_k (Problem P1)
c_sum = nd.inv_cdf(1 - alpha)  # sum_k Z_k / sqrt(K) is N(0, 1) under the null
c_fisher = float(np.quantile(rng.chisquare(2 * K, 400000), 1 - alpha))  # -2 sum_k log p_k is chi-square(2K)
log_p = np.frompyfunc(lambda z: math.log(0.5 * math.erfc(z / math.sqrt(2.0))), 1, 1)
print(f"critical values: max {c_max:.4f}  sum {c_sum:.4f}  fisher {c_fisher:.2f}")

sparse, dense = np.zeros(K), np.full(K, 0.3)
sparse[0] = 4.0
print("alternative  max_exact  max_simulated  sum_exact  fisher_simulated")
for name, theta in (("sparse_a=4", sparse), ("dense_delta=0.3", dense)):
    max_exact = 1.0 - math.prod(nd.cdf(c_max - t) for t in theta)
    sum_exact = 1.0 - nd.cdf(c_sum - float(theta.sum()) / math.sqrt(K))
    z = rng.standard_normal((n_reps, K)) + theta
    max_sim = float(np.mean(z.max(axis=1) > c_max))
    fisher = -2.0 * log_p(z).astype(float).sum(axis=1)
    print(f"{name} {max_exact:.4f} {max_sim:.4f} {sum_exact:.4f} {np.mean(fisher > c_fisher):.4f}")
