"""Round-9 independent check of the L05 Chapman-Kolmogorov quadrature (trapezoid rule, different grid).

Usage: python3 -I ledgers/SC1/scripts/SC1-b-r9/ck_independent_r9.py
Reports the worst absolute gap over the 225 cases with 6000 trapezoid intervals on [-12, 12], and the worst
mass of the integrand over 12 <= |z| <= 40 (trapezoid, 6000 intervals per side), and the printed-digit check
of the integral of p_t(0, y) over [-12, 12].
"""
import math
from itertools import product

TIMES = (0.5, 1.0, 2.0)
POINTS = (-1.0, -0.25, 0.0, 0.5, 1.0)


def p(u, x, y):
    return math.exp(-((y - x) ** 2) / (2.0 * u)) / math.sqrt(2.0 * math.pi * u)


def trap(f, a, b, n):
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h


worst = 0.0
worst_tail = 0.0
for s, t, x, y in product(TIMES, TIMES, POINTS, POINTS):
    integral = trap(lambda z: p(s, x, z) * p(t, z, y), -12.0, 12.0, 6000)
    worst = max(worst, abs(integral - p(s + t, x, y)))
    tail = trap(lambda z: p(s, x, z) * p(t, z, y), 12.0, 40.0, 6000) + trap(
        lambda z: p(s, x, z) * p(t, z, y), -40.0, -12.0, 6000
    )
    worst_tail = max(worst_tail, tail)
print(f"independent trapezoid, 6000 intervals: worst gap {worst:.3e}; worst tail mass 12<=|z|<=40 {worst_tail:.3e}")
for t in TIMES:
    print(f"integral of p_{t:g}(0,y) over [-12,12]: {trap(lambda y: p(t, 0.0, y), -12.0, 12.0, 6000):.10f}")
