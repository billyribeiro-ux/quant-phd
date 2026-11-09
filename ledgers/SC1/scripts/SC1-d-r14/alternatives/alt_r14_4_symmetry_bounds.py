"""Correct alternative 4 (round 14): binomial tail from the first up-count that reaches the level, a different
rounding path for the tail, and the instance draws written as a generator over paths."""

from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level must be positive")
    if t <= 0:
        raise ValueError("the time must be positive")
    return math.erfc(a / math.sqrt(2.0) / math.sqrt(t))


def _path_maxima(instance: dict[str, Any], n_fine: int, strides: tuple[int, ...]) -> list[dict[int, float]]:
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_fine)
    out = []
    for _ in range(instance["n_paths"]):
        pos = 0.0
        best = {s: -math.inf for s in strides}
        for k in range(1, n_fine + 1):
            pos += rng.gauss(0.0, sd)
            for s in strides:
                if k % s == 0 and pos > best[s]:
                    best[s] = pos
        out.append(best)
    return out


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if instance["n_paths"] < 2:
        raise ValueError("n_paths must be at least 2")
    rows = _path_maxima(instance, n_steps, (1,))
    hits = sum(1 for r in rows if r[1] >= instance["a"])
    n = instance["n_paths"]
    p = hits / n
    variance = (hits * (1 - p) ** 2 + (n - hits) * p * p) / (n - 1)
    return p, math.sqrt(variance) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1:
        raise ValueError("n_coarse must be at least 1")
    if n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    stride = n_fine // n_coarse
    rows = _path_maxima(instance, n_fine, (1, stride))
    fine = sum(1 for r in rows if r[1] >= instance["a"])
    coarse = sum(1 for r in rows if r[stride] >= instance["a"])
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    first_up = max(0, math.ceil((n + a) / 2))
    return sum(math.comb(n, j) for j in range(first_up, n + 1))


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
