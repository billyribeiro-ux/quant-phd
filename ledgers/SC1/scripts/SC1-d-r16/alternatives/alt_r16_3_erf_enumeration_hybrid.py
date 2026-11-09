"""Verifier alternative r16-3: erf normal cdf, enumeration to 12 steps and the identity beyond, index subsampling."""

from __future__ import annotations

import itertools
import math
import random
from typing import Any


def _phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a must be positive")
    if t <= 0:
        raise ValueError("t must be positive")
    return 2.0 * (1.0 - _phi(a / math.sqrt(t)))


def _paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    out = []
    for _ in range(int(instance["n_paths"])):
        values = []
        position = 0.0
        for _ in range(n_steps):
            position += rng.gauss(0.0, sd)
            values.append(position)
        out.append(values)
    return out


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if int(instance["n_paths"]) < 2:
        raise ValueError("n_paths must be at least 2")
    level = float(instance["a"])
    flags = [1.0 if max(values) >= level else 0.0 for values in _paths(instance, n_steps)]
    n = len(flags)
    mean = math.fsum(flags) / n
    ss = math.fsum((x - mean) ** 2 for x in flags)
    return mean, math.sqrt(ss / (n - 1)) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    fine = 0
    coarse = 0
    for values in _paths(instance, n_fine):
        fine += max(values) >= level
        indices = range(stride - 1, n_fine, stride)
        coarse += max(values[i] for i in indices) >= level
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    if n <= 12:
        return sum(1 for steps in itertools.product((1, -1), repeat=n) if sum(steps) >= a)
    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    if n <= 12:
        count = 0
        for steps in itertools.product((1, -1), repeat=n):
            running = list(itertools.accumulate(steps))
            count += max(running) >= a
        return count
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
