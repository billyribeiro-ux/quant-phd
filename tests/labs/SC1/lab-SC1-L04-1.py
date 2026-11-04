"""SC1 lab L04: the exponential martingale of Brownian motion, checked by numerical quadrature.

Numerical, not simulated. Nothing is random and nothing is read from a file, so every run prints the same lines.
B_t is normal with mean zero and variance t, so B_t has the law of sqrt(t) times a standard normal variable. Hence
E[exp(theta * B_t)] is the integral of
exp(theta * sqrt(t) * z) against the standard normal density phi(z), over the real line. The lab evaluates each
integral by composite Simpson's rule with PANELS panels on [-LIMIT, LIMIT].

For each theta the lab prints two checks. First, the quadrature of E[exp(theta * B_t)] against the closed form
exp(theta**2 * t / 2). Second, the quadrature of E[Z_t] for Z_t = exp(theta * B_t - theta**2 * t / 2) against Z_0 = 1.
Agreement with the closed form also tests that the truncation at LIMIT is harmless for these integrands.

These are finite computations for three values of theta and one value of t. They are not a proof for all theta and t.
"""

from __future__ import annotations

import math
from collections.abc import Callable

THETAS = (-1.0, 0.5, 2.0)
TIME = 2.0
LIMIT = 12.0
PANELS = 20000
TOL = 1e-9


def standard_normal_density(z: float) -> float:
    """The standard normal density phi(z) = exp(-z**2 / 2) / sqrt(2 pi)."""
    return math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def simpson(f: Callable[[float], float], lower: float, upper: float, panels: int) -> float:
    """Composite Simpson's rule on [lower, upper] with `panels` panels; `panels` must be even."""
    width = (upper - lower) / panels
    total = f(lower) + f(upper)
    for i in range(1, panels):
        weight = 4.0 if i % 2 else 2.0
        total += weight * f(lower + i * width)
    return total * width / 3.0


def exp_quadrature(theta: float, t: float, shift: float) -> float:
    """The integral of exp(theta * sqrt(t) * z - shift) * phi(z) over [-LIMIT, LIMIT], with shift a constant."""
    scale = theta * math.sqrt(t)

    def integrand(z: float) -> float:
        return math.exp(scale * z - shift) * standard_normal_density(z)

    return simpson(integrand, -LIMIT, LIMIT, PANELS)


def main() -> None:
    print(f"B_t ~ N(0, t) with t = {TIME:g}; each integral over [-{LIMIT:g}, {LIMIT:g}] with {PANELS} Simpson panels")
    for theta in THETAS:
        closed = math.exp(theta * theta * TIME / 2.0)
        mgf = exp_quadrature(theta, TIME, 0.0)
        martingale = exp_quadrature(theta, TIME, theta * theta * TIME / 2.0)
        mgf_ok = abs(mgf - closed) <= TOL * closed
        martingale_ok = abs(martingale - 1.0) <= TOL
        print(
            f"theta = {theta:+.1f}: E[exp(theta B_t)] = {mgf:.9f}, exp(theta^2 t / 2) = {closed:.9f}, "
            f"agree within 1e-9 relative: {mgf_ok}"
        )
        print(f"  E[Z_t] = {martingale:.9f}, equal to Z_0 = 1 within 1e-9: {martingale_ok}")


main()
