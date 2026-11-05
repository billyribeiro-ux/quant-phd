"""Alternative 4: discrete estimate by index subsampling of one vectorless cumulative-sum path build, with the SE from the closed form p(1-p)/(N-1); reflection_tail from the closed form."""
import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level must be positive")
    if t <= 0:
        raise ValueError("the time must be positive")
    return math.erfc(a / math.sqrt(2 * t))


def _paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_steps)
    out = []
    for _ in range(instance["n_paths"]):
        steps = [rng.gauss(0.0, sd) for _ in range(n_steps)]
        walk = []
        total = 0.0
        for s in steps:
            total += s
            walk.append(total)
        out.append(walk)
    return out


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be positive")
    if instance["n_paths"] < 2:
        raise ValueError("n_paths must be at least 2")
    hits = sum(1 for w in _paths(instance, n_steps) if max(w) >= instance["a"])
    n = instance["n_paths"]
    p = hits / n
    return p, math.sqrt(p * (1 - p) / (n - 1))


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be positive")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    stride = n_fine // n_coarse
    fine = 0
    coarse = 0
    for w in _paths(instance, n_fine):
        fine += max(w) >= instance["a"]
        sub = [w[i] for i in range(stride - 1, n_fine, stride)]
        coarse += max(sub) >= instance["a"]
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j > n + a - 1)


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
