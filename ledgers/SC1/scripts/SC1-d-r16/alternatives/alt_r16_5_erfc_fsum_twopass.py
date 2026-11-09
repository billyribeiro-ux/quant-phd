"""Verifier alternative r16-5: erfc tail, two-pass fsum variance, two-pass nested counts, binomial walk counts."""

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


def _maxima(instance: dict[str, Any], n_steps: int, strides: tuple[int, ...]) -> dict[int, list[float]]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    result: dict[int, list[float]] = {s: [] for s in strides}
    for _ in range(int(instance["n_paths"])):
        grid = []
        position = 0.0
        for _ in range(n_steps):
            position += rng.gauss(0.0, sd)
            grid.append(position)
        for s in strides:
            result[s].append(max(grid[s - 1 :: s]))
    return result


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if int(instance["n_paths"]) < 2:
        raise ValueError("n_paths must be at least 2")
    level = float(instance["a"])
    maxima = _maxima(instance, n_steps, (1,))[1]
    flags = [1.0 if m >= level else 0.0 for m in maxima]
    n = len(flags)
    mean = math.fsum(flags) / n
    var = math.fsum((f - mean) ** 2 for f in flags) / (n - 1)
    return mean, math.sqrt(var) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    maxima = _maxima(instance, n_fine, tuple(sorted({1, stride})))
    fine = sum(1 for m in maxima[1] if m >= level)
    coarse = sum(1 for m in maxima[stride] if m >= level)
    return fine, coarse


def _ends_and_maxima(n: int, a: int) -> tuple[int, int]:
    # Reflection identity with integer binomial sums: #{S_n >= b} for b = a and a + 1.
    def at_least(b: int) -> int:
        return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= b)

    return at_least(a) + at_least(a + 1), at_least(a)


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _ends_and_maxima(n, a)[1]


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _ends_and_maxima(n, a)[0]
