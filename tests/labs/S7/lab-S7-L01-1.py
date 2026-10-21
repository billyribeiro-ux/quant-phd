import math
from statistics import NormalDist

import numpy as np

phi = NormalDist()
gamma_e = 0.5772156649015329
# SIMULATED: the simulated column draws iid standard normals; the exact columns come from numerical integration.
rng = np.random.default_rng(7)

# Exact E[max of N iid N(0,1)]: integrate x * N * pdf(x) * cdf(x)^(N-1) by the trapezoid rule on a fine grid.
grid = np.linspace(-9.0, 10.0, 190001)
pdf = np.exp(-0.5 * grid**2) / math.sqrt(2 * math.pi)
cdf = np.array([phi.cdf(float(x)) for x in grid])

print("N  simulated  exact  approximation  bound  approx_error_pct")
for n, reps in ((10, 40000), (100, 20000), (1000, 4000)):
    simulated = rng.standard_normal((reps, n)).max(axis=1).mean()
    exact = float(np.trapezoid(grid * n * pdf * cdf ** (n - 1), grid))
    approx = (1 - gamma_e) * phi.inv_cdf(1 - 1 / n) + gamma_e * phi.inv_cdf(1 - 1 / (n * math.e))
    bound = math.sqrt(2 * math.log(n))
    print(f"{n} {simulated:.3f} {exact:.4f} {approx:.3f} {bound:.3f} {100 * (approx - exact) / exact:.1f}")

# Problems M1 and E1 use the exact mean at N = 20 and the standard deviation of the maximum.
print("N  exact_mean  exact_sd")
for n in (10, 20, 100, 1000):
    density = n * pdf * cdf ** (n - 1)
    mean = float(np.trapezoid(grid * density, grid))
    sd = math.sqrt(float(np.trapezoid(grid**2 * density, grid)) - mean**2)
    print(f"{n} {mean:.4f} {sd:.4f}")
