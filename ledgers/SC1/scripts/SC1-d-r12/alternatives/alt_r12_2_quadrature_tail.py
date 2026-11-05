"""Alternative 2: reflection_tail by Simpson's rule alone (no closed form); the rest is the reference route with a direct sum over the end-point counts."""
import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a must be positive")
    if t <= 0:
        raise ValueError("t must be positive")
    top = a + 12.0 * math.sqrt(t)
    n = 8000
    h = (top - a) / n

    def f(x: float) -> float:
        return math.exp(-x * x / (2.0 * t)) / math.sqrt(2.0 * math.pi * t)

    s = f(a) + f(top)
    for k in range(1, n):
        s += (4.0 if k % 2 else 2.0) * f(a + k * h)
    return 2.0 * s * h / 3.0


def _grid(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    paths = []
    for _ in range(int(instance["n_paths"])):
        pos = 0.0
        row = []
        for _ in range(n_steps):
            pos = pos + rng.gauss(0.0, sd)
            row.append(pos)
        paths.append(row)
    return paths


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps < 1")
    if instance["n_paths"] < 2:
        raise ValueError("n_paths < 2")
    hits = [max(row) >= instance["a"] for row in _grid(instance, n_steps)]
    n = len(hits)
    p = sum(hits) / n
    var = sum((int(h) - p) ** 2 for h in hits) / (n - 1)
    return p, math.sqrt(var) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine < 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    step = n_fine // n_coarse
    fine = 0
    coarse = 0
    for row in _grid(instance, n_fine):
        fine += max(row) >= instance["a"]
        coarse += max(row[i] for i in range(step - 1, n_fine, step)) >= instance["a"]
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
