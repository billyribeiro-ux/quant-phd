"""Alternative correct engine (round 9, C): tail with a scaled erfc, counts by a binomial-sum closed form with a parity split."""

from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a must be positive")
    if t <= 0:
        raise ValueError("t must be positive")
    return math.erfc(a * math.sqrt(0.5 / t))


def _draws(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    paths = []
    for _ in range(int(instance["n_paths"])):
        pos = 0.0
        row = []
        for _ in range(n_steps):
            pos += rng.gauss(0.0, sd)
            row.append(pos)
        paths.append(row)
    return paths


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if int(instance["n_paths"]) < 2:
        raise ValueError("n_paths must be at least 2")
    a = float(instance["a"])
    flags = [1 if max(row) >= a else 0 for row in _draws(instance, n_steps)]
    n = len(flags)
    p = sum(flags) / n
    ss = sum((f - p) ** 2 for f in flags)
    return p, math.sqrt(ss / (n - 1)) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    a = float(instance["a"])
    stride = n_fine // n_coarse
    fine = 0
    coarse = 0
    for row in _draws(instance, n_fine):
        fine += 1 if max(row) >= a else 0
        coarse += 1 if max(row[stride - 1 :: stride]) >= a else 0
    return fine, coarse


def _tail_count(n: int, level: int) -> int:
    """#{S_n >= level}: the sum of binomial coefficients over the upper half, split by parity of n."""
    lo = (n + level + 1) // 2 if (n + level) % 2 else (n + level) // 2
    lo = max(lo, 0)
    return sum(math.comb(n, j) for j in range(lo, n + 1))


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _tail_count(n, a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _tail_count(n, a) + _tail_count(n, a + 1)
