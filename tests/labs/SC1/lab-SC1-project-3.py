"""Rung 3 reference numbers: the values the report quotes for the seed-0 instance. SIMULATED.

The instance is the one the project's generator gives seed 0, drawn in the same fixed order. For a grid of n steps
the lab draws N paths, each a sum of n Gaussian increments N(0, H / n), taken path by path and step by step from
random.Random(seed). The estimate is the fraction of paths whose grid maximum reaches the level a, and its standard
error is the sample standard deviation of the 0/1 indicators (divisor N - 1) divided by sqrt(N). The coarse grids in
the nested check are every (256 / n)-th point of the same 256-step paths, so each coarse maximum is at most the fine
one. The continuous tail erfc(a / sqrt(2 H)) is the reflection principle's value for the continuous maximum on [0, H].
Every printed number is rounded to six decimal places by Python's own formatting, from the unrounded value. The walk
line is an exact count. Standard library only.
"""

from __future__ import annotations

import itertools
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


def path_maxima(inst: Instance, n_fine: int, strides: tuple[int, ...]) -> dict[int, list[float]]:
    """For each stride s, the maximum over the grid points at every s-th step, one value per path.

    The paths are drawn with n_fine steps, so stride 1 is the fine grid. A stride s gives the grid with n_fine / s steps
    on the same paths.
    """
    rng = random.Random(inst.seed)
    sd = math.sqrt(inst.horizon / n_fine)
    maxima: dict[int, list[float]] = {s: [] for s in strides}
    for _ in range(inst.n_paths):
        position = 0.0
        best = dict.fromkeys(strides, -math.inf)
        for k in range(1, n_fine + 1):
            position += rng.gauss(0.0, sd)
            for s in strides:
                if k % s == 0 and position > best[s]:
                    best[s] = position
        for s in strides:
            maxima[s].append(best[s])
    return maxima


def estimate_and_se(hits: int, n: int) -> tuple[float, float]:
    """The fraction hits / n, and its standard error: the sample standard deviation of the indicators over sqrt(n)."""
    mean = hits / n
    variance = n * mean * (1.0 - mean) / (n - 1)
    return mean, math.sqrt(variance) / math.sqrt(n)


def walk_counts(n: int, a: int) -> tuple[int, int]:
    """Over all 2**n walks: (the number whose maximum is at least a, the number ending at least a)."""
    max_hits = 0
    end_hits = 0
    for steps in itertools.product((1, -1), repeat=n):
        sums = list(itertools.accumulate(steps))
        if max(sums) >= a:
            max_hits += 1
        if sums[-1] >= a:
            end_hits += 1
    return max_hits, end_hits


def main() -> None:
    """Print the continuous tail, the estimate and standard error for each grid, the nested counts and a walk count."""
    inst = make_instance(0)
    tail = reflection_tail(inst.level, inst.horizon)
    print(f"seed 0: H = {inst.horizon}, a = {inst.level}, N = {inst.n_paths}, continuous tail = {tail:.6f}")
    for n in (1, 4, 16, 64, 256):
        hits = sum(1 for m in path_maxima(inst, n, (1,))[1] if m >= inst.level)
        p, se = estimate_and_se(hits, inst.n_paths)
        print(
            f"grid n = {n}: hits {hits}, estimate {p:.6f}, standard error {se:.6f}, tail minus estimate {tail - p:.6f}"
        )
    strides = (1, 4, 16, 64, 256)
    nested = path_maxima(inst, 256, strides)
    fine = sum(1 for m in nested[1] if m >= inst.level)
    for coarse, stride in ((64, 4), (16, 16), (4, 64), (1, 256)):
        counted = sum(1 for m in nested[stride] if m >= inst.level)
        at_most = counted <= fine
        print(f"nested: fine n = 256 count {fine}, coarse n = {coarse} count {counted}, coarse at most fine: {at_most}")
    max_hits, end_hits = walk_counts(12, 3)
    print(f"walk n = 12, a = 3: walks with maximum >= 3: {max_hits}, walks ending at >= 3: {end_hits}")


main()
