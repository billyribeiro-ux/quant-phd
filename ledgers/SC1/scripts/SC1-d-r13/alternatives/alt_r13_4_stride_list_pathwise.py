"""Alternative 4: nested coarse maxima taken over the explicit positions k with k divisible by the stride (a list comprehension, not a slice); the one-step estimate by a list of draws; tail via NormalDist from statistics."""

import math
import random
from statistics import NormalDist
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level a must be positive")
    if t <= 0:
        raise ValueError("the time t must be positive")
    return 2.0 * (1.0 - NormalDist(0.0, 1.0).cdf(a / math.sqrt(t)))


def _paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_steps)
    out: list[list[float]] = []
    for _ in range(instance["n_paths"]):
        steps = [rng.gauss(0.0, sd) for _ in range(n_steps)]
        positions = []
        pos = 0.0
        for s in steps:
            pos += s
            positions.append(pos)
        out.append(positions)
    return out


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if instance["n_paths"] < 2:
        raise ValueError("n_paths must be at least 2")
    hits = [1.0 if max(p) >= instance["a"] else 0.0 for p in _paths(instance, n_steps)]
    n = len(hits)
    mean = sum(hits) / n
    sample_var = sum((x - mean) ** 2 for x in hits) / (n - 1)
    return mean, math.sqrt(sample_var) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must be at least 1 and divide n_fine")
    stride = n_fine // n_coarse
    fine = 0
    coarse = 0
    for p in _paths(instance, n_fine):
        fine += max(p) >= instance["a"]
        coarse += max(v for k, v in enumerate(p, start=1) if k % stride == 0) >= instance["a"]
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    total = 0
    for j in range(n + 1):
        if 2 * j - n >= a:
            total += math.comb(n, j)
    return total


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
