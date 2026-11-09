"""Correct alternative 5 (round 14): the grid standard deviation written as sqrt(H) / sqrt(n) (one rounding more than
sqrt(H / n)), fsum-based sums for the indicator variance, and nested counts from a single pass over each path."""

from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0 or t <= 0:
        raise ValueError("the level and the time must be positive")
    return math.erfc(a / math.sqrt(2.0 * t))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("the grid needs at least one step")
    n = int(instance["n_paths"])
    if n < 2:
        raise ValueError("the standard error needs at least two paths")
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"]) / math.sqrt(n_steps)
    ind = []
    for _ in range(n):
        pos = 0.0
        top = -math.inf
        for _ in range(n_steps):
            pos = pos + rng.gauss(0.0, sd)
            if pos > top:
                top = pos
        ind.append(1.0 if top >= instance["a"] else 0.0)
    mean = math.fsum(ind) / n
    var = math.fsum((x - mean) ** 2 for x in ind) / (n - 1)
    return mean, math.sqrt(var) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("the fine grid needs at least one step")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("the coarse grid must be at least one step and divide the fine grid")
    stride = n_fine // n_coarse
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"]) / math.sqrt(n_fine)
    fine = coarse = 0
    for _ in range(int(instance["n_paths"])):
        pos = 0.0
        ftop = ctop = -math.inf
        for k in range(1, n_fine + 1):
            pos = pos + rng.gauss(0.0, sd)
            ftop = max(ftop, pos)
            if k % stride == 0:
                ctop = max(ctop, pos)
        fine += ftop >= instance["a"]
        coarse += ctop >= instance["a"]
    return fine, coarse


def _ends_at_least(n: int, a: int) -> int:
    total = 0
    for j in range(n + 1):
        if 2 * j - n >= a:
            total += math.comb(n, j)
    return total


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return _ends_at_least(n, a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return _ends_at_least(n, a) + _ends_at_least(n, a + 1)
