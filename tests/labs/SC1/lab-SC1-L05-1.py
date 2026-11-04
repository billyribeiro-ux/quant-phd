"""SC1 lab L05: the Chapman-Kolmogorov identity for the Gaussian transition density, by quadrature.

Standard library only. Nothing is random and nothing is read from a file, so every run prints the same lines.
The transition density is p_u(x, y) = (2 pi u)^(-1/2) exp(-(y - x)^2 / (2 u)) for u > 0. For each case the lab
approximates the integral over the intermediate point z of p_s(x, z) p_t(z, y) by a composite Simpson rule on
[-12, 12] and compares it with p_(s+t)(x, y). The mass of the integrand for 12 <= |z| <= 40 is computed and printed,
so the truncation can be compared with the gaps. The gaps are at the scale of double-precision rounding, not exact
values; the exact identity is proved on the page.
"""

from __future__ import annotations

import math
from collections.abc import Callable

LOWER = -12.0
UPPER = 12.0
INTERVALS = 2000
TIMES = (0.5, 1.0, 2.0)
POINTS = (-1.0, -0.25, 0.0, 0.5, 1.0)
TOLERANCE = 1e-6


def density(u: float, x: float, y: float) -> float:
    """The Gaussian transition density p_u(x, y) for u > 0: the N(x, u) density evaluated at y, in 1/length."""
    return math.exp(-((y - x) ** 2) / (2.0 * u)) / math.sqrt(2.0 * math.pi * u)


def simpson(g: Callable[[float], float], a: float, b: float, n: int) -> float:
    """Composite Simpson rule on [a, b] with n subintervals; n must be even."""
    h = (b - a) / n
    total = g(a) + g(b)
    for i in range(1, n):
        total += (4.0 if i % 2 == 1 else 2.0) * g(a + i * h)
    return total * h / 3.0


def chapman_kolmogorov_gap(s: float, t: float, x: float, y: float) -> float:
    """Quadrature of the integral of p_s(x, z) p_t(z, y) over z, minus p_(s+t)(x, y)."""
    integral = simpson(lambda z: density(s, x, z) * density(t, z, y), LOWER, UPPER, INTERVALS)
    return integral - density(s + t, x, y)


def tail_mass(s: float, t: float, x: float, y: float) -> float:
    """Integral of p_s(x, z) p_t(z, y) over 12 <= |z| <= 40, by Simpson on [12, 40] and [-40, -12]."""

    def integrand(z: float) -> float:
        return density(s, x, z) * density(t, z, y)

    return simpson(integrand, UPPER, 40.0, INTERVALS) + simpson(integrand, -40.0, LOWER, INTERVALS)


def mass_over_window(t: float) -> float:
    """Integral of the transition density p_t(0, y) over y in [-12, 12]; it is 1 up to quadrature error."""

    def integrand(y: float) -> float:
        return density(t, 0.0, y)

    return simpson(integrand, LOWER, UPPER, INTERVALS)


def main() -> None:
    cases = 0
    worst = 0.0
    worst_tail = 0.0
    for s in TIMES:
        for t in TIMES:
            for x in POINTS:
                for y in POINTS:
                    worst = max(worst, abs(chapman_kolmogorov_gap(s, t, x, y)))
                    worst_tail = max(worst_tail, tail_mass(s, t, x, y))
                    cases += 1
    print(f"Chapman-Kolmogorov cases checked: {cases}")
    print(f"largest absolute quadrature gap: {worst:.2e}")
    print(f"largest gap below the stated tolerance {TOLERANCE:g}: {worst < TOLERANCE}")
    print(f"largest mass of the integrand for 12 <= |z| <= 40: {worst_tail:.2e}")
    example = chapman_kolmogorov_gap(1.0, 2.0, 0.5, -0.25)
    print(f"example s = 1, t = 2, x = 0.5, y = -0.25: quadrature gap {example:+.2e}")
    for t in TIMES:
        mass = mass_over_window(t)
        print(f"integral of p_{t:g}(0, y) over y in [-12, 12]: {mass:.10f}")


main()
