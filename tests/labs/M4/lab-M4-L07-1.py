"""M4 L07 lab 1: the normal MGF by numerical integration against its closed form, and a two-point characteristic
function.

Inputs are illustrative, not data. Part A uses X ~ N(mu, sigma^2) with mu = 0.5 and sigma = 1.5. Part B and Part C use
a two-point law that takes the value A = 0 with probability P_A = 0.25 and the value B = 2 otherwise. Part C draws
100000 observations of that law from random.Random(20260701), and each observation uses one uniform draw.

Part A: M(t) = E[exp(tX)] at t in {-1, 0, 0.5, 1, 2}. Each value is a Simpson's rule sum of exp(t x) times the normal
density over [mu - 12 sigma, mu + 12 sigma] with 20000 intervals. The closed form is exp(mu t + sigma^2 t^2 / 2). The
line prints both values and their absolute difference.
Part B: phi(t) = P_A exp(i t A) + (1 - P_A) exp(i t B) at t in {0, 1, pi}, printed as real and imaginary parts, with
the modulus |phi(t)|.
Part C: the sample mean of cos(tX) and of sin(tX) at t = 1 over the 100000 draws, beside the real and imaginary
parts of phi(1) from Part B.
"""

from __future__ import annotations

import cmath
import math
import random

MU = 0.5
SIGMA = 1.5
P_A = 0.25
VALUE_A = 0.0
VALUE_B = 2.0
SEED = 20260701
N_DRAWS = 100000
INTERVALS = 20000


def normal_density(x: float, mu: float, sigma: float) -> float:
    """The normal density exp(-(x - mu)^2 / (2 sigma^2)) / (sigma sqrt(2 pi)) at x, for sigma > 0."""
    return math.exp(-((x - mu) ** 2) / (2.0 * sigma * sigma)) / (sigma * math.sqrt(2.0 * math.pi))


def mgf_numerical(t: float, mu: float, sigma: float) -> float:
    """E[exp(tX)] for X ~ N(mu, sigma^2), by Simpson's rule over mu +/- 12 sigma with INTERVALS (even) intervals."""
    lo = mu - 12.0 * sigma
    hi = mu + 12.0 * sigma
    h = (hi - lo) / INTERVALS
    total = 0.0
    for k in range(INTERVALS + 1):
        x = lo + k * h
        weight = 1.0 if k in (0, INTERVALS) else (4.0 if k % 2 == 1 else 2.0)
        total += weight * math.exp(t * x) * normal_density(x, mu, sigma)
    return total * h / 3.0


def mgf_closed(t: float, mu: float, sigma: float) -> float:
    """The closed form exp(mu t + sigma^2 t^2 / 2) of the normal MGF."""
    return math.exp(mu * t + sigma * sigma * t * t / 2.0)


def phi_two_point(t: float) -> complex:
    """The characteristic function P_A exp(i t A) + (1 - P_A) exp(i t B) of the two-point law."""
    return P_A * cmath.exp(1j * t * VALUE_A) + (1.0 - P_A) * cmath.exp(1j * t * VALUE_B)


def main() -> None:
    """Print Parts A, B and C. The seed is fixed, so every run prints the same lines."""
    print("Part A: normal MGF, Simpson's rule against the closed form")
    for t in (-1.0, 0.0, 0.5, 1.0, 2.0):
        numerical = mgf_numerical(t, MU, SIGMA)
        closed = mgf_closed(t, MU, SIGMA)
        print(
            f"t {t:.1f} numerical {numerical:.8f} closed {closed:.8f} absolute_difference {abs(numerical - closed):.2e}"
        )

    print("Part B: characteristic function of the two-point law")
    for t in (0.0, 1.0, math.pi):
        phi = phi_two_point(t)
        print(f"t {t:.6f} real {phi.real:.8f} imag {phi.imag:.8f} modulus {abs(phi):.8f}")

    print("Part C: seeded sample means of cos(tX) and sin(tX) at t = 1, against phi(1)")
    rng = random.Random(SEED)
    cos_sum = 0.0
    sin_sum = 0.0
    for _ in range(N_DRAWS):
        x = VALUE_A if rng.random() < P_A else VALUE_B
        cos_sum += math.cos(x)
        sin_sum += math.sin(x)
    phi1 = phi_two_point(1.0)
    print(f"sample_mean_cos {cos_sum / N_DRAWS:.6f} real_part_phi {phi1.real:.6f}")
    print(f"sample_mean_sin {sin_sum / N_DRAWS:.6f} imag_part_phi {phi1.imag:.6f}")


main()
