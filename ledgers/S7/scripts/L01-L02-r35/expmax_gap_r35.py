"""Round-35 recomputation of the expected maximum of N iid standard normals (S7 L01 section 3 caption).

Exact E[max] = integral of x * N * phi(x) * Phi(x)^(N-1) dx (the integrand the L01 figure source line names).
Computed by two independent methods: (a) scipy.integrate.quad at N = 2, 10, 100, 10000; (b) a trapezoid
grid over [-12, 14] with 200001 points for every N = 2..10000. Also computes bound (1) = sqrt(2 ln N),
the gap bound - exact (in SD units of each Z_n, which is 1), approximation (3) minus exact, and the
two caption values 1/sqrt(pi) and (3) at N = 2.
Run: .venv/bin/python -I ledgers/S7/scripts/L01-L02-r35/expmax_gap_r35.py
"""

from __future__ import annotations

import math

import numpy as np
from scipy import integrate, stats

EULER_GAMMA = 0.5772156649015329  # the page writes \emgamma ~ 0.5772; the exact constant is used here


def exact_quad(n: int) -> float:
    f = lambda x: x * n * stats.norm.pdf(x) * stats.norm.cdf(x) ** (n - 1)  # noqa: E731
    value, err = integrate.quad(f, -40.0, 40.0, limit=500, epsabs=1e-13, epsrel=1e-13)
    return float(value)


X = np.linspace(-12.0, 14.0, 200_001)
DX = X[1] - X[0]
PHI = stats.norm.pdf(X)
CDF = stats.norm.cdf(X)


def exact_grid(n: int) -> float:
    g = X * n * PHI * CDF ** (n - 1)
    return float(np.sum((g[1:] + g[:-1]) * 0.5) * DX)


def approx3(n: int) -> float:
    return (1 - EULER_GAMMA) * stats.norm.ppf(1 - 1 / n) + EULER_GAMMA * stats.norm.ppf(1 - 1 / (n * math.e))


def bound(n: int) -> float:
    return math.sqrt(2 * math.log(n))


print("N, exact (quad), exact (grid), bound sqrt(2 ln N), bound - exact (SD units), (3) - exact")
for n in (2, 3, 10, 100, 10_000):
    q = exact_quad(n)
    g = exact_grid(n)
    print(f"{n:>6} {q:.10f} {g:.10f} {bound(n):.10f} {bound(n) - q:.6f} {approx3(n) - q:+.6f}")

print()
print("caption checks at N = 2:")
print(f"  1/sqrt(pi) = {1 / math.sqrt(math.pi):.6f} (exact E[max of 2] by quad = {exact_quad(2):.10f})")
print(f"  (3) at N = 2 = gamma * Phi^-1(1 - 1/(2e)) = {EULER_GAMMA * stats.norm.ppf(1 - 1 / (2 * math.e)):.6f}")
print(f"  (3) at N = 2 by the full formula = {approx3(2):.6f}")

max_dev = 0.0
for n in range(2, 10_001):
    max_dev = max(max_dev, abs(exact_quad(n) - exact_grid(n)) if n in (2, 10, 100, 1000, 10_000) else 0.0)
print()
print(f"quad vs grid agreement at N in (2, 10, 100, 1000, 10000): max abs diff = {max_dev:.3e}")

# Sweep: exact (grid) and the sign of (3) - exact for every N = 2..10000
sign_ok_from_3 = True
first_fail = None
gaps = {}
for n in range(2, 10_001):
    ex = exact_grid(n)
    diff = approx3(n) - ex
    if n >= 3 and diff <= 0 and sign_ok_from_3:
        sign_ok_from_3 = False
        first_fail = n
    if n in (2, 3, 10, 100, 1000, 10_000):
        gaps[n] = (bound(n) - ex, diff)
print()
print(f"(3) - exact > 0 for every N = 3..10000: {sign_ok_from_3} (first N with diff <= 0: {first_fail})")
for n, (gb, ga) in gaps.items():
    print(f"  N={n}: bound - exact = {gb:.6f} SD; (3) - exact = {ga:+.6f}")
