"""Round-17 alternative 5: reflection_tail by statistics-free erfc of the standardised level; cumulative sums per path with running max via max(); SE by statistics.stdev; srw counts by a recurrence on the walk's terminal position with binomial weights built from a running product."""
from __future__ import annotations

import itertools
import math
import random
import statistics
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a")
    if t <= 0:
        raise ValueError("t")
    z = a / math.sqrt(t)
    return math.erfc(z / math.sqrt(2.0))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps")
    n = int(instance["n_paths"])
    if n < 2:
        raise ValueError("n_paths")
    level = float(instance["a"])
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    indicators = []
    for _ in range(n):
        draws = [rng.gauss(0.0, sd) for _ in range(n_steps)]
        indicators.append(1.0 if max(itertools.accumulate(draws)) >= level else 0.0)
    return sum(indicators) / n, statistics.stdev(indicators) / math.sqrt(n)


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
        draws = [rng.gauss(0.0, sd) for _ in range(n_fine)]
        partial = list(itertools.accumulate(draws))
        fine += max(partial) >= level
        coarse += max(partial[stride - 1 :: stride]) >= level
    return fine, coarse


def _terminal(n: int, a: int) -> int:
    weights = [1]
    for i in range(n):
        weights = [1] + [weights[k] + weights[k - 1] for k in range(1, len(weights))] + [1]
    return sum(weights[j] for j in range(n + 1) if 2 * j - n >= a)


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n")
    if a < 1:
        raise ValueError("a")
    return _terminal(n, a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n")
    if a < 1:
        raise ValueError("a")
    return _terminal(n, a) + _terminal(n, a + 1)
