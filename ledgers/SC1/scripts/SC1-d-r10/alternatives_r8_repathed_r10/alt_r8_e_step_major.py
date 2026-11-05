"""Alternative E (round 8): grid increments drawn step-major (all paths at step 1, then step 2, ...), same gauss call; rest by closed forms."""
from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a must be positive")
    if t <= 0:
        raise ValueError("t must be positive")
    return math.erfc(a / math.sqrt(2.0 * t))


def _step_major_max_and_coarse(instance: dict[str, Any], n_fine: int, strides: tuple[int, ...]) -> dict[int, list[float]]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_fine)
    n_paths = int(instance["n_paths"])
    pos = [0.0] * n_paths
    best: dict[int, list[float]] = {s: [-math.inf] * n_paths for s in strides}
    for k in range(1, n_fine + 1):
        for p in range(n_paths):
            pos[p] += rng.gauss(0.0, sd)
        for s in strides:
            if k % s == 0:
                for p in range(n_paths):
                    if pos[p] > best[s][p]:
                        best[s][p] = pos[p]
    return best


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if int(instance["n_paths"]) < 2:
        raise ValueError("n_paths must be at least 2")
    level = float(instance["a"])
    maxima = _step_major_max_and_coarse(instance, n_steps, (1,))[1]
    flags = [1.0 if m >= level else 0.0 for m in maxima]
    n = len(flags)
    mean = sum(flags) / n
    var = sum((x - mean) ** 2 for x in flags) / (n - 1)
    return mean, math.sqrt(var) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must be a positive divisor of n_fine")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    maxima = _step_major_max_and_coarse(instance, n_fine, (1, stride))
    fine = sum(1 for m in maxima[1] if m >= level)
    coarse = sum(1 for m in maxima[stride] if m >= level)
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    low = (n + a + 1) // 2
    return sum(math.comb(n, j) for j in range(low, n + 1))


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
