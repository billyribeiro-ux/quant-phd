"""Verifier alternative r16-2: erfc tail, binomial sums for walks, reflection identity for maxima, stdev."""

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
    return math.erfc(a * (2.0 * t) ** -0.5)


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if int(instance["n_paths"]) < 2:
        raise ValueError("n_paths must be at least 2")
    level = float(instance["a"])
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    indicators: list[float] = []
    for _ in range(int(instance["n_paths"])):
        position = 0.0
        peak = -math.inf
        for _ in range(n_steps):
            position += rng.gauss(0.0, sd)
            peak = max(peak, position)
        indicators.append(1.0 if peak >= level else 0.0)
    return statistics.fmean(indicators), statistics.stdev(indicators) / math.sqrt(len(indicators))


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_fine)
    fine = 0
    coarse = 0
    for _ in range(int(instance["n_paths"])):
        position = 0.0
        fine_peak = -math.inf
        coarse_peak = -math.inf
        for k in range(1, n_fine + 1):
            position += rng.gauss(0.0, sd)
            fine_peak = max(fine_peak, position)
            if k % stride == 0:
                coarse_peak = max(coarse_peak, position)
        fine += int(fine_peak >= level)
        coarse += int(coarse_peak >= level)
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    total = 0
    for j in range(n + 1):
        if 2 * j - n >= a:
            total += math.comb(n, j)
    return total


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
