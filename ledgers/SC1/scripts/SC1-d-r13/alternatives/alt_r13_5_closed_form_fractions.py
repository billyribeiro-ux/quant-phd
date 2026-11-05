"""Alternative 5: reflection_tail from math.erf as 1 - erf(a / (sqrt 2 sqrt t)); the grid estimate scanning each path once and recording a hit on the fine grid and on the coarse grid separately; srw endpoint count by a binomial sum, the maximum count by the reflection identity."""

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level a must be positive")
    if t <= 0:
        raise ValueError("the time t must be positive")
    return 1.0 - math.erf(a / (math.sqrt(2.0) * math.sqrt(t)))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if instance["n_paths"] < 2:
        raise ValueError("n_paths must be at least 2")
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_steps)
    n = instance["n_paths"]
    level = instance["a"]
    hits = 0
    for _ in range(n):
        pos = 0.0
        reached = False
        for _k in range(n_steps):
            pos += rng.gauss(0.0, sd)
            if pos >= level:
                reached = True
        hits += 1 if reached else 0
    p = hits / n
    variance = p * (1.0 - p) * n / (n - 1)
    return p, math.sqrt(variance) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must be at least 1 and divide n_fine")
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_fine)
    stride = n_fine // n_coarse
    fine = 0
    coarse = 0
    for _ in range(instance["n_paths"]):
        pos = 0.0
        fine_reached = False
        coarse_reached = False
        for k in range(1, n_fine + 1):
            pos += rng.gauss(0.0, sd)
            if pos >= instance["a"]:
                fine_reached = True
                if k % stride == 0:
                    coarse_reached = True
        fine += 1 if fine_reached else 0
        coarse += 1 if coarse_reached else 0
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
