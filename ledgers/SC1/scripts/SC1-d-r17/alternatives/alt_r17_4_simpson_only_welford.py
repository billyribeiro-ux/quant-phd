"""Round-17 alternative 4: reflection_tail by Simpson quadrature only (8000 intervals, no closed form); srw by Pascal row over j with strict-in-S threshold; Welford SE; nested by stride over enumerate."""
from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a")
    if t <= 0:
        raise ValueError("t")
    intervals = 8000
    top = a + 12.0 * math.sqrt(t)
    step = (top - a) / intervals

    def density(x: float) -> float:
        return math.exp(-x * x / (2.0 * t)) / math.sqrt(2.0 * math.pi * t)

    total = density(a) + density(top)
    for k in range(1, intervals):
        total += (4.0 if k % 2 else 2.0) * density(a + k * step)
    return 2.0 * total * step / 3.0


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps")
    n = int(instance["n_paths"])
    if n < 2:
        raise ValueError("n_paths")
    level = float(instance["a"])
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    mean = 0.0
    m2 = 0.0
    hits = 0
    for i in range(1, n + 1):
        pos = 0.0
        best = -math.inf
        for _ in range(n_steps):
            pos += rng.gauss(0.0, sd)
            best = max(best, pos)
        x = float(best >= level)
        hits += int(x)
        delta = x - mean
        mean += delta / i
        m2 += delta * (x - mean)
    return hits / n, math.sqrt(m2 / (n - 1)) / math.sqrt(n)


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
        best_f = -math.inf
        best_c = -math.inf
        pos = 0.0
        for k, _ in enumerate(range(n_fine), start=1):
            pos += rng.gauss(0.0, sd)
            best_f = max(best_f, pos)
            if k % stride == 0:
                best_c = max(best_c, pos)
        fine += best_f >= level
        coarse += best_c >= level
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n")
    if a < 1:
        raise ValueError("a")
    total = 0
    c = 1
    for j in range(n + 1):
        if 2 * j - n >= a:
            total += c
        c = c * (n - j) // (j + 1)
    return total


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n")
    if a < 1:
        raise ValueError("a")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
