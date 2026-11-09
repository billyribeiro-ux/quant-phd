# Mutant m3-L03-closed-form-h3 (SC1 lab L03): Lab 3 closed form uses H cubed instead of H to the fourth; the exact-match column must print False.
"""SC1 lab L03: squared increments of a simulated Brownian path over dyadic partitions, and the same sums for t squared.

SIMULATED. The Brownian part draws Gaussian increments with variance equal to the step length, from
random.Random(SEED), so every run prints the same lines. For each horizon H and each dyadic partition of [0, H] into
N = 2**k steps, k = 0 to 7, the lab simulates PATHS independent paths and records the sum of squared increments of
each path. It prints the sample mean, the standard error (sample standard deviation divided by the square root of
PATHS, with divisor PATHS - 1) and z = (mean - H) / se.

The t-squared part is exact. It sums the squared increments of f(s) = s * s over the same partition points H * j / N,
using fractions.Fraction, so no randomness enters it. The lab checks each exact sum against the closed form
H**4 * (4 N**2 - 1) / (3 N**3).

A simulation is a finite sample on finitely many partitions. It illustrates the limit of Lesson 3; it does not verify
any statement about all partitions or about almost-sure behaviour.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction
from itertools import pairwise

SEED = 20260503
PATHS = 400
LEVELS = range(0, 8)
HORIZONS = (1.0, 2.0)
EXACT_HORIZONS = (Fraction(1), Fraction(2))


def squared_increment_sums(horizon: float, steps: int, paths: int, rng: random.Random) -> list[float]:
    """For each of `paths` simulated paths on [0, horizon], the sum of squared increments over `steps` equal steps.

    Each increment is Gaussian with mean 0 and variance horizon / steps, drawn from `rng`.
    """
    step_sd = math.sqrt(horizon / steps)
    sums: list[float] = []
    for _ in range(paths):
        total = 0.0
        for _ in range(steps):
            increment = rng.gauss(0.0, step_sd)
            total += increment * increment
        sums.append(total)
    return sums


def mean_and_standard_error(values: list[float]) -> tuple[float, float]:
    """The sample mean and the standard error sd / sqrt(n), with sd computed by divisor n - 1."""
    n = len(values)
    mean = sum(values) / n
    variance = sum((v - mean) ** 2 for v in values) / (n - 1)
    return mean, math.sqrt(variance / n)


def t_squared_sum(horizon: Fraction, steps: int) -> Fraction:
    """The sum of squared increments of f(s) = s * s over the equal partition of [0, horizon] into `steps` pieces."""
    points = [horizon * j / steps for j in range(steps + 1)]
    return sum(((b * b - a * a) ** 2 for a, b in pairwise(points)), Fraction(0))


def t_squared_closed_form(horizon: Fraction, steps: int) -> Fraction:
    """The closed form H**4 * (4 N**2 - 1) / (3 N**3) for the sum computed by t_squared_sum."""
    return horizon**3 * (4 * steps * steps - 1) / (3 * steps**3)


def main() -> None:
    rng = random.Random(SEED)
    for horizon in HORIZONS:
        print(f"H = {horizon:g}: mean of the sum of squared increments over {PATHS} simulated paths")
        for k in LEVELS:
            steps = 2**k
            mean, se = mean_and_standard_error(squared_increment_sums(horizon, steps, PATHS, rng))
            z = (mean - horizon) / se
            print(f"  N = {steps:3d} steps: mean {mean:.4f}, se {se:.4f}, z = {z:.2f}")
    print("t squared, exact sums over the same partitions of [0, H]:")
    for horizon_exact in EXACT_HORIZONS:
        for k in LEVELS:
            steps = 2**k
            exact = t_squared_sum(horizon_exact, steps)
            matches = exact == t_squared_closed_form(horizon_exact, steps)
            print(f"  H = {horizon_exact}, N = {steps:3d}: sum = {float(exact):.6f}, closed form matches: {matches}")


main()
