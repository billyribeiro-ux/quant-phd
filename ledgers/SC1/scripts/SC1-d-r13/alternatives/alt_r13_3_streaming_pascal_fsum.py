"""Alternative 3: srw counts from a Pascal-triangle row built without math.comb, using #{max >= a} = 2 #{S_n > a} + #{S_n = a}; the standard error by math.fsum of squared deviations; reflection_tail through math.erfc with argument a * sqrt(1 / (2 t))."""

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level a must be positive")
    if t <= 0:
        raise ValueError("the time t must be positive")
    return math.erfc(a * math.sqrt(1.0 / (2.0 * t)))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if instance["n_paths"] < 2:
        raise ValueError("n_paths must be at least 2")
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_steps)
    n = instance["n_paths"]
    indicators = []
    for _ in range(n):
        pos = 0.0
        top = -math.inf
        for _k in range(n_steps):
            pos = pos + rng.gauss(0.0, sd)
            top = max(top, pos)
        indicators.append(1.0 if top >= instance["a"] else 0.0)
    mean = math.fsum(indicators) / n
    ss = math.fsum((x - mean) ** 2 for x in indicators)
    return mean, math.sqrt(ss / (n - 1)) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must be at least 1 and divide n_fine")
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_fine)
    stride = n_fine // n_coarse
    fine = 0
    coarse = 0
    for _ in range(instance["n_paths"]):
        pos = 0.0
        fine_top = -math.inf
        coarse_top = -math.inf
        for k in range(1, n_fine + 1):
            pos = pos + rng.gauss(0.0, sd)
            fine_top = max(fine_top, pos)
            if k % stride == 0:
                coarse_top = max(coarse_top, pos)
        if fine_top >= instance["a"]:
            fine += 1
        if coarse_top >= instance["a"]:
            coarse += 1
    return fine, coarse


def _pascal_row(n: int) -> list[int]:
    row = [1]
    for _ in range(n):
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return row


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    row = _pascal_row(n)
    return sum(row[j] for j in range(n + 1) if 2 * j - n >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    row = _pascal_row(n)
    strictly_above = sum(row[j] for j in range(n + 1) if 2 * j - n > a)
    exactly = sum(row[j] for j in range(n + 1) if 2 * j - n == a)
    return 2 * strictly_above + exactly
