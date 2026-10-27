"""Python recomputation of the readouts printed by the live figures (fig_states.log, fig_read.json)."""
import math
from scipy import stats
import numpy as np
g = 0.5772156649015329
def approx(n):
    return (1 - g) * stats.norm.ppf(1 - 1 / n) + g * stats.norm.ppf(1 - 1 / (n * math.e))
grid = np.linspace(-9, 10, 190001)
pdf = stats.norm.pdf(grid); cdf = stats.norm.cdf(grid)
def exact(n):
    return float(np.trapezoid(grid * n * pdf * cdf ** (n - 1), grid))
for years in (1, 5, 20):
    T = years * 252
    scale = math.sqrt(252 / T)
    vals = [round(scale * exact(n), 2) for n in (10, 100, 1000)]
    tail = 1 - stats.norm.cdf(1 / scale) ** 100
    print(f"years {years} T {T:,}: expected best {vals[0]:.2f} (N=10), {vals[1]:.2f} (N=100), {vals[2]:.2f} (N=1,000); P(best of 100 > 1.0) = {tail:.6f} -> {tail:.3f}")
print("fwer-growth: naive FWER 1-(0.95)^m >= 0.5 first at m =", next(m for m in range(1, 1001) if 1 - 0.95**m >= 0.5), "; 1-0.95^14 =", round(1 - 0.95**14, 5), "; 1-0.95^13 =", round(1 - 0.95**13, 5))
print("expected-max: approx - exact at N=2:", round(approx(2) - exact(2), 6), "; at N=3:", round(approx(3) - exact(3), 6))
print("power-family readout values:", [round(stats.norm.cdf(3.5 - stats.norm.ppf(1 - 0.05 / (2 * m))) + stats.norm.cdf(-3.5 - stats.norm.ppf(1 - 0.05 / (2 * m))), 3) for m in (1, 10, 100, 1000)])
