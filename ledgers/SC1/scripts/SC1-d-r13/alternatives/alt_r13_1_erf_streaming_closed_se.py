"""Alternative 1: reflection_tail as 2(1 - Phi) with Phi from math.erf; the estimate by a streaming pass that stores no paths; the standard error in closed form, sqrt(p(1-p)/(N-1))."""

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level a must be positive")
    if t <= 0:
        raise ValueError("the time t must be positive")
    phi = 0.5 * (1.0 + math.erf((a / math.sqrt(t)) / math.sqrt(2.0)))
    return 2.0 * (1.0 - phi)


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
        best = -math.inf
        for _k in range(n_steps):
            pos += rng.gauss(0.0, sd)
            if pos > best:
                best = pos
        if best >= level:
            hits += 1
    p = hits / n
    return p, math.sqrt(p * (1.0 - p) / (n - 1))


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse:
        raise ValueError("n_coarse must be at least 1 and divide n_fine")
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_fine)
    stride = n_fine // n_coarse
    fine = 0
    coarse = 0
    for _ in range(instance["n_paths"]):
        pos = 0.0
        best_fine = -math.inf
        best_coarse = -math.inf
        for k in range(1, n_fine + 1):
            pos += rng.gauss(0.0, sd)
            best_fine = max(best_fine, pos)
            if k % stride == 0:
                best_coarse = max(best_coarse, pos)
        fine += best_fine >= instance["a"]
        coarse += best_coarse >= instance["a"]
    return fine, coarse


def _terminal(n: int, a: int) -> int:
    total = 0
    for j in range(n + 1):
        if 2 * j - n >= a:
            total += math.comb(n, j)
    return total


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _terminal(n, a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _terminal(n, a) + _terminal(n, a + 1)
