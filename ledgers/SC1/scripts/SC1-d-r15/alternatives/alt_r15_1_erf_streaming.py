"""Alternative r15-1 (verifier-written, correct): reflection tail by 1 - erf, streaming running maxima, binomial sums.

Draw order: path by path, step by step, random.Random(seed).gauss(0, sqrt(H / n)), as the page states.
"""

from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level must be positive")
    if t <= 0:
        raise ValueError("the time must be positive")
    return 1.0 - math.erf(a / math.sqrt(2.0 * t))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    n_paths = int(instance["n_paths"])
    if n_paths < 2:
        raise ValueError("n_paths must be at least 2")
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    level = float(instance["a"])
    hits = 0
    for _ in range(n_paths):
        position = 0.0
        running = -math.inf
        for _ in range(n_steps):
            position += rng.gauss(0.0, sd)
            if position > running:
                running = position
        if running >= level:
            hits += 1
    p = hits / n_paths
    variance_times_n_minus_1 = hits * (n_paths - hits) / n_paths
    se = math.sqrt(variance_times_n_minus_1 / (n_paths - 1)) / math.sqrt(n_paths)
    return p, se


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse:
        raise ValueError("n_coarse must be a positive divisor of n_fine")
    stride = n_fine // n_coarse
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_fine)
    level = float(instance["a"])
    fine = 0
    coarse = 0
    for _ in range(int(instance["n_paths"])):
        position = 0.0
        fine_max = -math.inf
        coarse_max = -math.inf
        for k in range(1, n_fine + 1):
            position += rng.gauss(0.0, sd)
            fine_max = max(fine_max, position)
            if k % stride == 0:
                coarse_max = max(coarse_max, position)
        fine += fine_max >= level
        coarse += coarse_max >= level
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
