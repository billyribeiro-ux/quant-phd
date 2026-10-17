import math
from statistics import NormalDist

import numpy as np

phi = NormalDist()
gamma_e = 0.5772156649015329
rng = np.random.default_rng(7)

print("N  simulated  approximation  bound  approx_error_pct")
for n, reps in ((10, 40000), (100, 20000), (1000, 4000)):
    simulated = rng.standard_normal((reps, n)).max(axis=1).mean()
    approx = (1 - gamma_e) * phi.inv_cdf(1 - 1 / n) + gamma_e * phi.inv_cdf(1 - 1 / (n * math.e))
    bound = math.sqrt(2 * math.log(n))
    print(f"{n} {simulated:.3f} {approx:.3f} {bound:.3f} {100 * (approx - simulated) / simulated:.1f}")
