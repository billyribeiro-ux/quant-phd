"""Rung 1 worked example: the reflection tail for the seed-0 instance, checked three ways. SIMULATED.

The instance is the one the project's generator gives seed 0. This file draws the same four numbers in the same order,
so the two agree. The reflection principle gives P(M_t >= a) = 2 P(B_t >= a) for a standard Brownian motion M, so the
tail at level a and horizon H equals erfc(a / sqrt(2 H)). The lab prints that closed form, a Simpson's rule value of
2 P(B_H >= a) from the normal density with mean 0 and variance H, and a seeded simulation estimate of P(B_H >= a) on
N paths. With one grid step the grid maximum is B_H itself, so the estimate tests the half of the tail that needs no
grid. Every computed number is rounded to six decimal places by Python's own formatting, from the unrounded value,
except the Simpson difference, which is printed in exponent form to three significant digits. The horizon H and the
level a are printed as generated, to three decimals, and N is an integer. Standard library only.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Instance:
    """One generated instance: the seed, the horizon H in time units, the level a, the grid size and the path count."""

    seed: int
    horizon: float
    level: float
    n_steps: int
    n_paths: int


def make_instance(seed: int) -> Instance:
    """The project's instance for a seed, drawn in the fixed order: horizon, level, grid size, path count."""
    rng = random.Random(1_000_003 * seed + 54_321)
    horizon = round(rng.uniform(0.25, 4.0), 3)
    level = round(rng.uniform(0.25, 2.5), 3)
    n_steps = rng.randint(4, 256)
    n_paths = rng.randint(400, min(800, 200_000 // n_steps))
    return Instance(seed, horizon, level, n_steps, n_paths)


def reflection_tail(level: float, horizon: float) -> float:
    """P(M_H >= level) = erfc(level / sqrt(2 H)), for level > 0 and horizon > 0."""
    return math.erfc(level / math.sqrt(2.0 * horizon))


def gaussian_tail_simpson(level: float, horizon: float, intervals: int = 4000) -> float:
    """2 P(B_H >= level) by Simpson's rule on the N(0, H) density over [level, level + 12 sqrt(H)]."""
    top = level + 12.0 * math.sqrt(horizon)
    step = (top - level) / intervals

    def density(x: float) -> float:
        return math.exp(-x * x / (2.0 * horizon)) / math.sqrt(2.0 * math.pi * horizon)

    total = density(level) + density(top)
    for k in range(1, intervals):
        weight = 4.0 if k % 2 else 2.0
        total += weight * density(level + k * step)
    return 2.0 * total * step / 3.0


def one_step_estimate(inst: Instance) -> tuple[float, float]:
    """The fraction of the N seeded draws of B_H that reach the level, and its standard error with divisor N - 1."""
    rng = random.Random(inst.seed)
    sd = math.sqrt(inst.horizon)
    indicators: list[float] = []
    for _ in range(inst.n_paths):
        value = rng.gauss(0.0, sd)
        indicators.append(1.0 if value >= inst.level else 0.0)
    count = len(indicators)
    mean = sum(indicators) / count
    variance = sum((x - mean) ** 2 for x in indicators) / (count - 1)
    return mean, math.sqrt(variance) / math.sqrt(count)


def main() -> None:
    """Print the instance, the closed form, the quadrature, and the one-step estimate with its band."""
    inst = make_instance(0)
    tail = reflection_tail(inst.level, inst.horizon)
    quad = gaussian_tail_simpson(inst.level, inst.horizon)
    estimate, se = one_step_estimate(inst)
    target = tail / 2.0
    band = 5.0 * se + 1.0 / inst.n_paths
    print(f"seed {inst.seed} instance: label SIMULATED, H = {inst.horizon}, a = {inst.level}, N = {inst.n_paths}")
    print(f"closed form erfc(a / sqrt(2 H)) = {tail:.6f}")
    print(f"quadrature 2 P(B_H >= a) = {quad:.6f}, absolute difference from the closed form {abs(quad - tail):.2e}")
    print(f"one step: estimate of P(B_H >= a) = {estimate:.6f}, standard error {se:.6f}")
    print(f"target tail / 2 = {target:.6f}, band 5 se + 1/N = {band:.6f}, difference {abs(estimate - target):.6f}")
    print(f"inside the band: {abs(estimate - target) <= band}")


main()
