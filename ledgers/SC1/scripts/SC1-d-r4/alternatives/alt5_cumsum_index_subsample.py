"""Alternative 5 (round 2): paths by itertools.accumulate of the reference-order gauss draws; the coarse grid by an explicit index list, not a slice; srw counts by the reflection identity."""

from __future__ import annotations

import itertools
import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("level must be positive")
    if t <= 0:
        raise ValueError("time must be positive")
    return math.erfc(a / math.sqrt(2.0 * t))


def _paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(instance["H"] / n_steps)
    return [
        list(itertools.accumulate(rng.gauss(0.0, sd) for _ in range(n_steps)))
        for _ in range(int(instance["n_paths"]))
    ]


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if instance["n_paths"] < 2:
        raise ValueError("n_paths must be at least 2")
    hits = [1 if max(path) >= instance["a"] else 0 for path in _paths(instance, n_steps)]
    n = len(hits)
    p = sum(hits) / n
    var = p * (1.0 - p) * n / (n - 1)
    return p, math.sqrt(var) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1:
        raise ValueError("n_coarse must be at least 1")
    if n_fine % n_coarse:
        raise ValueError("n_coarse must divide n_fine")
    keep = [k for k in range(n_fine) if (k + 1) % (n_fine // n_coarse) == 0]
    fine = 0
    coarse = 0
    for path in _paths(instance, n_fine):
        fine += max(path) >= instance["a"]
        coarse += max(path[k] for k in keep) >= instance["a"]
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
