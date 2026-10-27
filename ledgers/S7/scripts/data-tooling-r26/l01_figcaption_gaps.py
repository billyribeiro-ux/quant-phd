"""Re-derive the L01 Figure 1 caption numbers (course/modules/S/S7/L01.html line 133, reworded this cycle).

E[max of N iid N(0,1)] = integral of x * N * phi(x) * Phi(x)^(N-1) dx (the page's own integrand), by scipy quad.
The dependence-free bound (1) is sqrt(2 ln N) as printed on the page. Gap = bound - exact, in units of sigma = 1.
"""

from __future__ import annotations

import math
from statistics import NormalDist

from scipy import integrate, stats  # type: ignore[import-untyped]

PHI = NormalDist()


def expected_max(n: int) -> float:
    def integrand(x: float) -> float:
        return x * n * stats.norm.pdf(x) * stats.norm.cdf(x) ** (n - 1)

    value, _err = integrate.quad(integrand, -40.0, 40.0, limit=500)
    return float(value)


for n, printed_bound, printed_exact, printed_gap in ((10, 2.146, 1.539, 0.61), (100, 3.035, 2.508, 0.53), (10000, 4.292, 3.852, 0.44)):
    bound = math.sqrt(2 * math.log(n))
    exact = expected_max(n)
    gap = bound - exact
    print(
        f"N={n:>6}: bound sqrt(2 ln N)={bound:.6f} (page {printed_bound}) "
        f"exact={exact:.6f} (page {printed_exact}) gap={gap:.6f} (page {printed_gap}) "
        f"rounds-to-page: bound {round(bound, 3) == printed_bound}, exact {round(exact, 3) == printed_exact}, "
        f"gap {round(gap, 2) == printed_gap}"
    )
print("sanity: E[max] at N=2 =", round(expected_max(2), 6), "vs 1/sqrt(pi) =", round(1 / math.sqrt(math.pi), 6))
print("sanity: Phi(1.959964) =", round(PHI.cdf(1.959964), 6))
