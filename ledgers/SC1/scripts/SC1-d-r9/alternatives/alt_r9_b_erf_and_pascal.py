"""Alternative correct engine (round 9, B): tail by 1 - erf, counts by a Pascal-row recurrence, sum-of-squares standard error."""

from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0 or t <= 0:
        raise ValueError("the level and the time must be positive")
    return 1.0 - math.erf(a / math.sqrt(2.0 * t))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("the grid needs at least one step")
    n_paths = int(instance["n_paths"])
    if n_paths < 2:
        raise ValueError("at least two paths")
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_steps)
    hits = 0
    for _ in range(n_paths):
        pos = 0.0
        top = -math.inf
        for _ in range(n_steps):
            pos = pos + rng.gauss(0.0, sd)
            top = pos if pos > top else top
        if top >= instance["a"]:
            hits += 1
    p = hits / n_paths
    s2 = hits  # for 0/1 indicators the sum of squares equals the sum
    var = (s2 - n_paths * p * p) / (n_paths - 1)
    return p, math.sqrt(var) / math.sqrt(n_paths)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1 or n_coarse < 1:
        raise ValueError("grid sizes must be at least 1")
    if n_fine % n_coarse:
        raise ValueError("the coarse grid must divide the fine grid")
    stride = n_fine // n_coarse
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_fine)
    fine = coarse = 0
    for _ in range(int(instance["n_paths"])):
        pos = 0.0
        top_fine = -math.inf
        top_coarse = -math.inf
        for k in range(1, n_fine + 1):
            pos += rng.gauss(0.0, sd)
            top_fine = max(top_fine, pos)
            if k % stride == 0:
                top_coarse = max(top_coarse, pos)
        fine += top_fine >= instance["a"]
        coarse += top_coarse >= instance["a"]
    return fine, coarse


def _pascal_row(n: int) -> list[int]:
    row = [1]
    for _ in range(n):
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return row


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    row = _pascal_row(n)
    return sum(c for j, c in enumerate(row) if 2 * j - n >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    row = _pascal_row(n)
    upper = sum(c for j, c in enumerate(row) if 2 * j - n >= a)
    upper_next = sum(c for j, c in enumerate(row) if 2 * j - n >= a + 1)
    return upper + upper_next
