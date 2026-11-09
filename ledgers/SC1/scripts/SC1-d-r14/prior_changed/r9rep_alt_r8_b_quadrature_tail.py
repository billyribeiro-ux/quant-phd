"""Alternative B (round 8): reflection_tail by Simpson quadrature of the normal density only (no erfc).

Every function is written out in this file. It does not import the reference, so it runs from any checkout.
"""
from __future__ import annotations

import math
import random
import statistics
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a must be positive")
    if t <= 0:
        raise ValueError("t must be positive")
    top = a + 14.0 * math.sqrt(t)
    n = 20000
    h = (top - a) / n

    def dens(x: float) -> float:
        return math.exp(-x * x / (2.0 * t)) / math.sqrt(2.0 * math.pi * t)

    s = dens(a) + dens(top)
    for k in range(1, n):
        s += (4.0 if k % 2 else 2.0) * dens(a + k * h)
    return 2.0 * s * h / 3.0


def _grid_paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    paths = []
    for _ in range(int(instance["n_paths"])):
        position = 0.0
        values = []
        for _ in range(n_steps):
            position += rng.gauss(0.0, sd)
            values.append(position)
        paths.append(values)
    return paths


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if int(instance["n_paths"]) < 2:
        raise ValueError("n_paths must be at least 2")
    level = float(instance["a"])
    hits = [1.0 if max(v) >= level else 0.0 for v in _grid_paths(instance, n_steps)]
    p = statistics.fmean(hits)
    se = statistics.stdev(hits) / math.sqrt(len(hits))
    return p, se


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse:
        raise ValueError("n_coarse must be a positive divisor of n_fine")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    fine = coarse = 0
    for v in _grid_paths(instance, n_fine):
        fine += max(v) >= level
        coarse += max(v[i] for i in range(stride - 1, n_fine, stride)) >= level
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    low = (n + a + 1) // 2  # smallest number of up-steps j with 2j - n >= a
    return sum(math.comb(n, j) for j in range(low, n + 1))


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
