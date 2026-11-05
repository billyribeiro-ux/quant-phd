"""Alternative 5: srw counts from Fraction-exact binomial rows (Pascal's triangle), reflection_tail by the normal-density integral closed form via erfc, discrete estimate by a generator pipeline."""
import math
import random
from fractions import Fraction
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level must be positive")
    if t <= 0:
        raise ValueError("the time must be positive")
    return math.erfc(a / math.sqrt(2.0 * t))


def _gauss_path(rng: random.Random, sd: float, n_steps: int):
    pos = 0.0
    for _ in range(n_steps):
        pos += rng.gauss(0.0, sd)
        yield pos


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("the grid must have a step")
    if instance["n_paths"] < 2:
        raise ValueError("the estimate needs two paths")
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_steps)
    flags = [max(_gauss_path(rng, sd, n_steps)) >= instance["a"] for _ in range(instance["n_paths"])]
    n = len(flags)
    mean = Fraction(sum(flags), n)
    mean_f = float(mean)
    sample_var = Fraction(sum((int(f) - mean) ** 2 for f in flags), n - 1)
    return mean_f, math.sqrt(float(sample_var)) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("the fine grid must have a step")
    if n_coarse < 1 or n_fine % n_coarse:
        raise ValueError("the coarse grid must divide the fine grid")
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_fine)
    stride = n_fine // n_coarse
    fine = 0
    coarse = 0
    for _ in range(instance["n_paths"]):
        seq = list(_gauss_path(rng, sd, n_fine))
        fine += max(seq) >= instance["a"]
        coarse += max(seq[j] for j in range(stride - 1, n_fine, stride)) >= instance["a"]
    return fine, coarse


def _binomial_row(n: int) -> list[int]:
    row = [1]
    for _ in range(n):
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return row


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    row = _binomial_row(n)
    return sum(row[j] for j in range(n + 1) if 2 * j - n >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    row = _binomial_row(n)
    return sum(row[j] for j in range(n + 1) if 2 * j - n >= a) + sum(row[j] for j in range(n + 1) if 2 * j - n >= a + 1)
