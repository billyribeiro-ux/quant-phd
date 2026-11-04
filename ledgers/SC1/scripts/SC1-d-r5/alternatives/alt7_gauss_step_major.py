"""Alternative: Gaussian increments drawn step-major (step 1 for every path, then step 2, ...) from random.Random(seed).gauss."""

from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level a must be positive for the reflection tail")
    if t <= 0:
        raise ValueError("the time t must be positive for the reflection tail")
    return math.erfc(a / math.sqrt(2.0 * t))


def _maxima(instance: dict[str, Any], n_fine: int, stride: int) -> list[float]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_fine)
    n = int(instance["n_paths"])
    pos = [0.0] * n
    best = [-math.inf] * n
    for k in range(1, n_fine + 1):
        for p in range(n):
            pos[p] += rng.gauss(0.0, sd)
        if k % stride == 0:
            for p in range(n):
                if pos[p] > best[p]:
                    best[p] = pos[p]
    return best


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("the grid needs at least one step")
    if int(instance["n_paths"]) < 2:
        raise ValueError("the estimate needs at least two paths for a standard error")
    level = float(instance["a"])
    ind = [1.0 if m >= level else 0.0 for m in _maxima(instance, n_steps, 1)]
    n = len(ind)
    mean = sum(ind) / n
    var = sum((x - mean) ** 2 for x in ind) / (n - 1)
    return mean, math.sqrt(var) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("the fine grid needs at least one step")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("the coarse grid size must divide the fine grid size")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    rng_seed_fine = _maxima(instance, n_fine, 1)
    rng_seed_coarse = _maxima(instance, n_fine, stride)
    fine = sum(1 for m in rng_seed_fine if m >= level)
    coarse = sum(1 for m in rng_seed_coarse if m >= level)
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("the walk needs at least one step")
    if a < 1:
        raise ValueError("the level a must be at least 1")
    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("the walk needs at least one step")
    if a < 1:
        raise ValueError("the level a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
