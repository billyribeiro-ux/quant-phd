"""Correct alternative 2 (round 14): streaming maxima, a count-based standard error, and a stride over accumulate."""

from __future__ import annotations

import itertools
import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0 or t <= 0:
        raise ValueError("the level and the time must be positive")
    return math.erfc(a / math.sqrt(2.0 * t))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    n = instance["n_paths"]
    if n < 2:
        raise ValueError("need at least two paths")
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_steps)
    hits = 0
    for _ in range(n):
        steps = [rng.gauss(0.0, sd) for _ in range(n_steps)]
        if max(itertools.accumulate(steps)) >= instance["a"]:
            hits += 1
    # sum of (x - mean)^2 over 0/1 values is h (N - h) / N, so the sample variance with divisor N - 1 is h (N - h) / (N (N - 1)).
    se = math.sqrt(hits * (n - hits) / (n * n * (n - 1)))
    return hits / n, se


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    stride = n_fine // n_coarse
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_fine)
    fine = coarse = 0
    for _ in range(instance["n_paths"]):
        path = list(itertools.accumulate(rng.gauss(0.0, sd) for _ in range(n_fine)))
        if max(path) >= instance["a"]:
            fine += 1
        if max(path[k] for k in range(stride - 1, n_fine, stride)) >= instance["a"]:
            coarse += 1
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    total = 0
    for j in range(n + 1):
        if 2 * j - n >= a:
            total += math.comb(n, j)
    return total


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
