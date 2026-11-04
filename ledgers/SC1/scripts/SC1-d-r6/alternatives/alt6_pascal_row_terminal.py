"""Alternative: srw_terminal_count by an iterative Pascal-row recurrence (no math.comb); max by the reflection identity."""

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


def _paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    out = []
    for _ in range(int(instance["n_paths"])):
        pos = 0.0
        vals = []
        for _ in range(n_steps):
            pos += rng.gauss(0.0, sd)
            vals.append(pos)
        out.append(vals)
    return out


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("the grid needs at least one step")
    if int(instance["n_paths"]) < 2:
        raise ValueError("the estimate needs at least two paths for a standard error")
    level = float(instance["a"])
    ind = [1.0 if max(v) >= level else 0.0 for v in _paths(instance, n_steps)]
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
    s = n_fine // n_coarse
    paths = _paths(instance, n_fine)
    fine = sum(1 for v in paths if max(v) >= level)
    coarse = sum(1 for v in paths if max(v[s - 1 :: s]) >= level)
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("the walk needs at least one step")
    if a < 1:
        raise ValueError("the level a must be at least 1")
    row = [1]
    for _ in range(n):
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return sum(c for j, c in enumerate(row) if 2 * j - n >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("the walk needs at least one step")
    if a < 1:
        raise ValueError("the level a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
