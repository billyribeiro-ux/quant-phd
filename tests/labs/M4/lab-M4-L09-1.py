"""M4 lab L09: a fair die, its running sample mean, and the standardized sample mean against Phi(1).

SIMULATED: the draws come from seeded generators; no data is used.
Standard library only (fractions, math, random, statistics). The law is a fair die: values 1 to 6, each with
probability 1/6, so mu = 7/2 and sigma^2 = 35/12. Part A computes P(S_n <= 3.5 n + sqrt(35 n / 12)) exactly for
the sum S_n of n independent dice. It convolves the exact probability mass function of the sum, with Fraction
arithmetic, and takes the threshold to the largest integer not above it (math.floor). The exact values are
compared with Phi(1), the standard normal distribution function, from statistics.NormalDist. Part B draws one
seeded path of 10000 dice (seed 2026) and prints its running sample mean at n = 10, 100, 1000 and 10000, with the
Chebyshev bound sigma^2 / (n eps^2) for eps = 0.5. Part C draws 4000 seeded samples (seed 2026) for each size
n = 5, 30 and 200, estimates P(Z_n <= 1) for the standardized sample mean Z_n = (Xbar_n - mu) / (sigma / sqrt(n)),
and prints the gap to Phi(1) with the Monte Carlo standard error of the estimate. A sample is one random run.
"""

from __future__ import annotations

import math
import random
import statistics
from fractions import Fraction

FACES = range(1, 7)
MU = 3.5
SIGMA2 = 35 / 12
SIGMA = math.sqrt(SIGMA2)
SEED = 2026
EXACT_SIZES = (1, 5, 10, 20, 40)
PATH_LENGTH = 10000
PATH_CHECKPOINTS = (10, 100, 1000, 10000)
REPLICATIONS = 4000
MC_SIZES = (5, 30, 200)


def die_sum_mass(n: int) -> list[Fraction]:
    """Exact probability mass function of S_n, the sum of n independent fair dice, indexed by the sum."""
    mass = [Fraction(1)]
    for _ in range(n):
        new = [Fraction(0)] * (len(mass) + 6)
        for total, p in enumerate(mass):
            if p:
                for face in FACES:
                    new[total + face] += p / 6
        mass = new
    return mass


def exact_cdf_at(mass: list[Fraction], m: int) -> Fraction:
    """P(S_n <= m) from the exact mass function; m may be below 0 or above the largest sum."""
    if m < 0:
        return Fraction(0)
    return sum(mass[: m + 1], Fraction(0))


def standardized_threshold(n: int) -> int:
    """The largest integer not above 3.5 n + sqrt(35 n / 12), so that S_n <= threshold iff Z_n <= 1."""
    return math.floor(MU * n + math.sqrt(SIGMA2 * n))


def main() -> None:
    phi1 = statistics.NormalDist().cdf(1.0)
    print(f"part A: Phi(1) = {phi1:.6f}")
    for n in EXACT_SIZES:
        mass = die_sum_mass(n)
        if sum(mass) != 1:
            raise AssertionError("the mass function does not sum to 1")
        m = standardized_threshold(n)
        exact = exact_cdf_at(mass, m)
        print(
            f"part A: n = {n:2d}, P(S_n <= {m:3d}) = P(Z_n <= 1) exactly = {float(exact):.6f}, "
            f"gap to Phi(1) = {float(exact) - phi1:+.6f}"
        )

    rng = random.Random(SEED)
    path = [rng.randint(1, 6) for _ in range(PATH_LENGTH)]
    bound_eps = 0.5
    for n in PATH_CHECKPOINTS:
        running = sum(path[:n]) / n
        bound = SIGMA2 / (n * bound_eps**2)
        print(
            f"part B: n = {n:5d}, running sample mean = {running:.4f}, gap to 3.5 = {running - MU:+.4f}, "
            f"Chebyshev bound on P(|Xbar_n - 3.5| >= 0.5) = {bound:.4f}"
        )

    for n in MC_SIZES:
        rng = random.Random(SEED)
        hits = 0
        for _ in range(REPLICATIONS):
            total = sum(rng.randint(1, 6) for _ in range(n))
            z = (total / n - MU) / (SIGMA / math.sqrt(n))
            if z <= 1.0:
                hits += 1
        estimate = hits / REPLICATIONS
        standard_error = math.sqrt(estimate * (1 - estimate) / REPLICATIONS)
        print(
            f"part C: n = {n:3d}, estimated P(Z_n <= 1) = {estimate:.4f} (standard error {standard_error:.4f}), "
            f"gap to Phi(1) = {estimate - phi1:+.4f}"
        )


main()
