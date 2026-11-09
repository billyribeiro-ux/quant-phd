"""Alternative r15-3 (verifier-written, correct): erfc with a rescaled argument; Welford running mean and M2 for the
standard error; per-path coarse maxima by stride loops; walk counts by a position array with the reflection identity."""

from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level must be positive")
    if t <= 0:
        raise ValueError("the time must be positive")
    return math.erfc(a * math.sqrt(0.5 / t))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    n_paths = int(instance["n_paths"])
    if n_paths < 2:
        raise ValueError("n_paths must be at least 2")
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    level = float(instance["a"])
    count = 0
    mean = 0.0
    m2 = 0.0
    for_path = 0
    while for_path < n_paths:
        for_path += 1
        position = 0.0
        best = None
        for _ in range(n_steps):
            position += rng.gauss(0.0, sd)
            best = position if best is None or position > best else best
        x = 1.0 if best >= level else 0.0
        count += 1
        delta = x - mean
        mean += delta / count
        m2 += delta * (x - mean)
    se = math.sqrt(m2 / (count - 1)) / math.sqrt(count)
    return mean, se


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    stride = n_fine // n_coarse
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_fine)
    level = float(instance["a"])
    fine = 0
    coarse = 0
    for _ in range(int(instance["n_paths"])):
        position = 0.0
        fine_best = -math.inf
        coarse_best = -math.inf
        for k in range(n_fine):
            position += rng.gauss(0.0, sd)
            if position > fine_best:
                fine_best = position
            if (k + 1) % stride == 0 and position > coarse_best:
                coarse_best = position
        if fine_best >= level:
            fine += 1
        if coarse_best >= level:
            coarse += 1
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    ways = [0] * (n + 1)
    ways[0] = 1
    for _ in range(n):
        nxt = [0] * (n + 1)
        for j, w in enumerate(ways):
            if w:
                nxt[j + 1] += w
                nxt[j] += w
        ways = nxt
    return sum(ways[j] for j in range(n + 1) if 2 * j - n >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
