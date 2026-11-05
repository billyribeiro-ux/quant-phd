"""Alternative 1 (round 2): reflection_tail through statistics.NormalDist and 2 (1 - Phi(a / sqrt t)); the grid engine by per-path running max."""

from __future__ import annotations

import math
import random
import statistics
from typing import Any

_STD_NORMAL = statistics.NormalDist(0.0, 1.0)


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("level must be positive")
    if t <= 0:
        raise ValueError("time must be positive")
    return 2.0 * (1.0 - _STD_NORMAL.cdf(a / math.sqrt(t)))


def _paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_steps)
    out = []
    for _ in range(instance["n_paths"]):
        walk = []
        x = 0.0
        for _ in range(n_steps):
            x += rng.gauss(0.0, sd)
            walk.append(x)
        out.append(walk)
    return out


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if instance["n_paths"] < 2:
        raise ValueError("n_paths must be at least 2")
    hits = [1.0 if max(p) >= instance["a"] else 0.0 for p in _paths(instance, n_steps)]
    n = len(hits)
    p = sum(hits) / n
    var = sum((h - p) ** 2 for h in hits) / (n - 1)
    return p, math.sqrt(var / n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1:
        raise ValueError("n_coarse must be at least 1")
    if n_fine % n_coarse:
        raise ValueError("n_coarse must divide n_fine")
    step = n_fine // n_coarse
    fine = coarse = 0
    for p in _paths(instance, n_fine):
        if max(p) >= instance["a"]:
            fine += 1
        if max(p[step - 1 :: step]) >= instance["a"]:
            coarse += 1
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return sum(math.comb(n, k) for k in range(n + 1) if 2 * k - n >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
