"""Round-17 alternative 1: reflection_tail by 1 - erf; the grid draws and maxima by a streaming loop; Welford SE; nested by stride test on k."""
from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a")
    if t <= 0:
        raise ValueError("t")
    return 1.0 - math.erf(a / math.sqrt(2.0 * t))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps")
    n_paths = int(instance["n_paths"])
    if n_paths < 2:
        raise ValueError("n_paths")
    level = float(instance["a"])
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    hits = 0
    count = 0
    mean = 0.0
    m2 = 0.0
    for _ in range(n_paths):
        pos = 0.0
        top = -math.inf
        for _k in range(n_steps):
            pos += rng.gauss(0.0, sd)
            if pos > top:
                top = pos
        x = 1.0 if top >= level else 0.0
        hits += int(x)
        count += 1
        delta = x - mean
        mean += delta / count
        m2 += delta * (x - mean)
    return hits / count, math.sqrt(m2 / (count - 1)) / math.sqrt(count)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_fine)
    fine = 0
    coarse = 0
    for _ in range(int(instance["n_paths"])):
        pos = 0.0
        top_f = -math.inf
        top_c = -math.inf
        for k in range(1, n_fine + 1):
            pos += rng.gauss(0.0, sd)
            top_f = max(top_f, pos)
            if k % stride == 0:
                top_c = max(top_c, pos)
        fine += int(top_f >= level)
        coarse += int(top_c >= level)
    return fine, coarse


def _pascal(n: int) -> list[int]:
    row = [1]
    for _ in range(n):
        row = [x + y for x, y in zip([0] + row, row + [0])]
    return row


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n")
    if a < 1:
        raise ValueError("a")
    row = _pascal(n)
    return sum(row[j] for j in range(n + 1) if 2 * j - n >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n")
    if a < 1:
        raise ValueError("a")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
