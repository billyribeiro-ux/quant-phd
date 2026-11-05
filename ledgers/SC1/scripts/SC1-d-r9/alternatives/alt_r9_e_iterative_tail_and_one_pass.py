"""Alternative correct engine (round 9, E): tail by a midpoint-free Simpson-free series for erfc via erf, one-pass Welford standard error."""

from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a must be positive")
    if t <= 0:
        raise ValueError("t must be positive")
    return 1.0 - math.erf(a / math.sqrt(2.0 * t))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    n = int(instance["n_paths"])
    if n < 2:
        raise ValueError("n_paths must be at least 2")
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    level = float(instance["a"])
    mean = 0.0
    m2 = 0.0
    seen = 0
    for _ in range(n):
        running = -math.inf
        pos = 0.0
        for _ in range(n_steps):
            pos += rng.gauss(0.0, sd)
            if pos > running:
                running = pos
        x = 1.0 if running >= level else 0.0
        seen += 1
        delta = x - mean
        mean += delta / seen
        m2 += delta * (x - mean)
    variance = m2 / (seen - 1)
    return mean, math.sqrt(variance) / math.sqrt(seen)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse:
        raise ValueError("n_coarse must divide n_fine")
    stride = n_fine // n_coarse
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_fine)
    level = float(instance["a"])
    fine = 0
    coarse = 0
    for _ in range(int(instance["n_paths"])):
        pos = 0.0
        best_fine = -math.inf
        best_coarse = -math.inf
        for k in range(1, n_fine + 1):
            pos += rng.gauss(0.0, sd)
            best_fine = max(best_fine, pos)
            if k % stride == 0:
                best_coarse = max(best_coarse, pos)
        fine += best_fine >= level
        coarse += best_coarse >= level
    return fine, coarse


def _binom_tail(n: int, level: int) -> int:
    count = 0
    row = 1
    for j in range(n + 1):
        if j > 0:
            row = row * (n - j + 1) // j
        if 2 * j - n >= level:
            count += row
    return count


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _binom_tail(n, a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _binom_tail(n, a) + _binom_tail(n, a + 1)
