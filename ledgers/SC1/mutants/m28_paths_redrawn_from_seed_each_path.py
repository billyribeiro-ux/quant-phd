"""Generator reseeded per path: _grid_paths calls random.Random(seed) inside the path loop, so every path repeats the same increments.

Single-change copy of grader/reference.py, written by the verifier (round 4).
"""

from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    """P(M_t >= a) for a standard Brownian motion, with M_t the running maximum on [0, t], for a > 0 and t > 0.

    The value is erfc(a / sqrt(2 t)), which equals 2 * P(B_t >= a) by the reflection principle.
    """
    if a <= 0:
        raise ValueError("the level a must be positive for the reflection tail")
    if t <= 0:
        raise ValueError("the time t must be positive for the reflection tail")
    return math.erfc(a / math.sqrt(2.0 * t))


def _grid_paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    """The partial sums of the seeded Gaussian increments on the grid t_k = k H / n_steps, one list per path."""
    sd = math.sqrt(float(instance["H"]) / n_steps)
    paths: list[list[float]] = []
    for _ in range(int(instance["n_paths"])):
        rng = random.Random(int(instance["seed"]))
        position = 0.0
        values: list[float] = []
        for _ in range(n_steps):
            position += rng.gauss(0.0, sd)
            values.append(position)
        paths.append(values)
    return paths


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    """Estimate and standard error of P(max over k <= n_steps of B_{t_k} >= a) on the instance's seeded paths.

    The estimate is the fraction of paths whose grid maximum reaches the level a. The standard error is the sample
    standard deviation of the N indicators, with divisor N - 1, divided by sqrt(N).
    """
    if n_steps < 1:
        raise ValueError("the grid needs at least one step")
    if int(instance["n_paths"]) < 2:
        raise ValueError("the estimate needs at least two paths for a standard error")
    level = float(instance["a"])
    paths = _grid_paths(instance, n_steps)
    indicators = [1.0 if max(values) >= level else 0.0 for values in paths]
    count = len(indicators)
    mean = sum(indicators) / count
    variance = sum((x - mean) ** 2 for x in indicators) / (count - 1)
    return mean, math.sqrt(variance) / math.sqrt(count)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    """Exceedance counts on the same paths for the fine grid (n_fine steps) and the coarse grid (n_coarse steps).

    The coarse grid is the subset of the fine grid at every (n_fine / n_coarse)-th step, so each coarse maximum is at
    most the fine maximum on the same path, and the coarse count is never larger than the fine count.
    """
    if n_fine < 1:
        raise ValueError("the fine grid needs at least one step")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("the coarse grid size must divide the fine grid size")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    paths = _grid_paths(instance, n_fine)
    fine = sum(1 for values in paths if max(values) >= level)
    coarse = sum(1 for values in paths if max(values[stride - 1 :: stride]) >= level)
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    """The number of simple random walk paths of length n with S_n >= a, as an exact integer."""
    if n < 1:
        raise ValueError("the walk needs at least one step")
    if a < 1:
        raise ValueError("the level a must be at least 1")
    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)


def srw_max_count(n: int, a: int) -> int:
    """The number of simple random walk paths of length n whose maximum reaches a, as an exact integer.

    By the reflection identity, #{max >= a} = #{S_n >= a} + #{S_n >= a + 1} for a >= 1.
    """
    if n < 1:
        raise ValueError("the walk needs at least one step")
    if a < 1:
        raise ValueError("the level a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
