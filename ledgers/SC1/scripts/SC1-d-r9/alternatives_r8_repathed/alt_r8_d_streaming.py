"""Alternative D (round 8): streaming single pass for the grid estimates (no stored paths); cumulative sums via itertools.accumulate."""
from __future__ import annotations

import itertools
import math
import random
import statistics
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a must be positive")
    if t <= 0:
        raise ValueError("t must be positive")
    return math.erfc(a / math.sqrt(2.0 * t))


def _increments(instance: dict[str, Any], n_steps: int) -> itertools.chain:  # type: ignore[type-arg]
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    for _ in range(int(instance["n_paths"])):
        yield list(itertools.accumulate(rng.gauss(0.0, sd) for _ in range(n_steps)))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if int(instance["n_paths"]) < 2:
        raise ValueError("n_paths must be at least 2")
    level = float(instance["a"])
    flags = [1.0 if max(path) >= level else 0.0 for path in _increments(instance, n_steps)]
    n = len(flags)
    mean = statistics.fmean(flags)
    return mean, statistics.stdev(flags) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1:
        raise ValueError("n_coarse must be at least 1")
    if n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    fine = coarse = 0
    for path in _increments(instance, n_fine):
        fine += max(path) >= level
        picked = [path[k * stride - 1] for k in range(1, n_coarse + 1)]
        coarse += max(picked) >= level
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    total = 0
    for j in range(n + 1):
        if 2 * j - n >= a:
            total += math.comb(n, j)
    return total


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
