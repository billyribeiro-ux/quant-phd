"""Alternative correct engine (round 9, D): list-comprehension draws, the grid maximum by max over slices, a per-call cache of the paths."""

from __future__ import annotations

import math
import random
from functools import lru_cache
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a must be positive")
    if t <= 0:
        raise ValueError("t must be positive")
    return math.erfc(a / math.sqrt(2 * t))


@lru_cache(maxsize=None)
def _cached(seed: int, n_paths: int, n_steps: int, sd_key: float) -> tuple[tuple[float, ...], ...]:
    rng = random.Random(seed)
    return tuple(tuple(_running(rng, n_steps, sd_key)) for _ in range(n_paths))


def _running(rng: random.Random, n_steps: int, sd: float) -> list[float]:
    out: list[float] = []
    pos = 0.0
    for _ in range(n_steps):
        pos += rng.gauss(0.0, sd)
        out.append(pos)
    return out


def _paths(instance: dict[str, Any], n_steps: int) -> tuple[tuple[float, ...], ...]:
    return _cached(int(instance["seed"]), int(instance["n_paths"]), n_steps, math.sqrt(float(instance["H"]) / n_steps))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if int(instance["n_paths"]) < 2:
        raise ValueError("n_paths must be at least 2")
    a = float(instance["a"])
    hits = [1.0 if max(p) >= a else 0.0 for p in _paths(instance, n_steps)]
    count = len(hits)
    mean = math.fsum(hits) / count
    variance = math.fsum((x - mean) ** 2 for x in hits) / (count - 1)
    return mean, math.sqrt(variance / count)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse:
        raise ValueError("n_coarse must divide n_fine")
    a = float(instance["a"])
    stride = n_fine // n_coarse
    paths = _paths(instance, n_fine)
    fine = sum(1 for p in paths if max(p) >= a)
    coarse = sum(1 for p in paths if max(p[stride - 1 :: stride]) >= a)
    return fine, coarse


def _count_upper(n: int, level: int) -> int:
    """#{S_n >= level} by the explicit sum over the number of up steps j, with S_n = 2j - n."""
    total = 0
    for j in range(n + 1):
        if 2 * j - n >= level:
            total += math.comb(n, j)
    return total


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _count_upper(n, a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _count_upper(n, a) + _count_upper(n, a + 1)
