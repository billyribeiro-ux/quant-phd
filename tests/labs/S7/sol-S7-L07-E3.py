import math

import numpy as np

# The maximum Q of 50 independent standard normals has density 50 phi(x) Phi(x)^49; its mean and
# variance by the trapezoidal rule on [-9, 10] (no simulation).
x = np.linspace(-9.0, 10.0, 38001)
weights = np.full(x.size, x[1] - x[0])
weights[[0, -1]] /= 2.0
phi = np.exp(-0.5 * x**2) / math.sqrt(2.0 * math.pi)
cdf = 0.5 * (1.0 + np.array([math.erf(v / math.sqrt(2.0)) for v in x]))
density = 50 * phi * cdf**49
mean = float(np.sum(weights * x * density))
variance = float(np.sum(weights * (x - mean) ** 2 * density))
print(f"mass {float(np.sum(weights * density)):.6f}")
print(f"mean_of_max {mean:.3f}")
print(f"variance_of_max {variance:.3f}")
