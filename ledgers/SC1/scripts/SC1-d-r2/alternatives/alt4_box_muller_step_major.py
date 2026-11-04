"""Alternative 4 (round 2): grid draws by Box-Muller from rng.random(), in step-major order (all paths at step 1, then step 2, ...); a different draw order whose numbers differ from Lab 3."""

from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("level must be positive")
    if t <= 0:
        raise ValueError("time must be positive")
    return math.erfc(a / math.sqrt(2.0 * t))


def _maxima(instance: dict[str, Any], n_steps: int) -> list[float]:
    """Running maxima for each path, with draws in step-major order and Box-Muller normals."""
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    n_paths = int(instance["n_paths"])
    pos = [0.0] * n_paths
    top = [-math.inf] * n_paths
    for _step in range(n_steps):
        for j in range(n_paths):
            u1 = 1.0 - rng.random()
            u2 = rng.random()
            z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
            pos[j] += sd * z
            if pos[j] > top[j]:
                top[j] = pos[j]
    return top


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if instance["n_paths"] < 2:
        raise ValueError("n_paths must be at least 2")
    flags = [1.0 if m >= instance["a"] else 0.0 for m in _maxima(instance, n_steps)]
    n = len(flags)
    mean = sum(flags) / n
    variance = sum((f - mean) ** 2 for f in flags) / (n - 1)
    return mean, math.sqrt(variance / n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must be a positive divisor of n_fine")
    # The coarse counts use the same step-major draws: rerun the fine grid, tracking the coarse maxima too.
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_fine)
    n_paths = int(instance["n_paths"])
    stride = n_fine // n_coarse
    pos = [0.0] * n_paths
    fine_top = [-math.inf] * n_paths
    coarse_top = [-math.inf] * n_paths
    for step in range(1, n_fine + 1):
        for j in range(n_paths):
            u1 = 1.0 - rng.random()
            u2 = rng.random()
            pos[j] += sd * math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
            fine_top[j] = max(fine_top[j], pos[j])
            if step % stride == 0:
                coarse_top[j] = max(coarse_top[j], pos[j])
    fine = sum(1 for m in fine_top if m >= instance["a"])
    coarse = sum(1 for m in coarse_top if m >= instance["a"])
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return sum(math.comb(n, k) for k in range(n + 1) if 2 * k - n >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
