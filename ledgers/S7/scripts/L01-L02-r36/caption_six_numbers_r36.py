"""Round-36 recomputation of the six numbers in the L01 section 3 figcaption (commit 47bac8d, line 133).

Caption: bound (1) sqrt(2 ln N) exceeds the exact expectation (computed by numerical integration) by 0.61 SD at N = 10
(2.146 against 1.539), 0.53 at N = 100 (3.035 against 2.508), 0.44 at N = 10,000 (4.292 against 3.852).
Exact expectation of the maximum of N iid N(0,1): integral over the real line of x * N phi(x) Phi(x)^(N-1) dx,
the integrand the figure's source line displays. Computed by scipy quad and by a trapezoid grid.
Run: .venv/bin/python -I ledgers/S7/scripts/L01-L02-r36/caption_six_numbers_r36.py
"""

from __future__ import annotations

import math

import numpy as np
from scipy import integrate, stats

PAGE = {10: (2.146, 1.539, 0.61), 100: (3.035, 2.508, 0.53), 10_000: (4.292, 3.852, 0.44)}


def exact_quad(n: int) -> float:
    def f(x: float) -> float:
        return x * n * stats.norm.pdf(x) * stats.norm.cdf(x) ** (n - 1)

    value, _ = integrate.quad(f, -40.0, 40.0, limit=500, epsabs=1e-13, epsrel=1e-13)
    return float(value)


X = np.linspace(-12.0, 14.0, 200_001)
DX = X[1] - X[0]
PHI = stats.norm.pdf(X)
CDF = stats.norm.cdf(X)


def exact_grid(n: int) -> float:
    g = X * n * PHI * CDF ** (n - 1)
    return float(np.sum((g[1:] + g[:-1]) * 0.5) * DX)


ok = True
print("N | bound sqrt(2 ln N) | exact (quad) | exact (grid) | gap unrounded | gap from 3-dp values | page")
for n, (pb, pe, pg) in PAGE.items():
    b = math.sqrt(2 * math.log(n))
    q = exact_quad(n)
    g = exact_grid(n)
    gap = b - q
    gap_rounded = round(b, 3) - round(q, 3)
    rb, rq = round(b, 3), round(q, 3)
    match = (rb == pb) and (rq == pe) and (round(gap, 2) == pg) and (round(gap_rounded, 2) == pg)
    ok &= match and abs(q - g) < 1e-9
    print(f"{n} | {b:.6f} -> {rb:.3f} (page {pb}) | {q:.10f} -> {rq:.3f} (page {pe}) | {g:.10f} | "
          f"{gap:.6f} -> {round(gap, 2):.2f} | {gap_rounded:.3f} -> {round(gap_rounded, 2):.2f} | page {pg}")
print("ALL SIX MATCH" if ok else "MISMATCH")
