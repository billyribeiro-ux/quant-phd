"""Alternative: functional style. The sweep is a pure map over tuples, and the sup-norm change is a reduction.

Synchronous sweeps from zero; the certified error is beta / (1 - beta) times the sup-norm change of the last sweep,
and the solver stops at the first sweep whose certified error is at most tol. Standard library only.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from functools import reduce
from itertools import pairwise
from typing import Any


def _real(name: str, value: object) -> float:
    """A finite real number that is not a boolean; anything else raises ValueError."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number, not a boolean")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _params(params: Mapping[str, Any]) -> tuple[float, float]:
    """beta and alpha, each in the open interval (0, 1)."""
    beta = _real("beta", params.get("beta"))
    alpha = _real("alpha", params.get("alpha"))
    if not 0 < beta < 1:
        raise ValueError("beta must lie in the open interval (0, 1)")
    if not 0 < alpha < 1:
        raise ValueError("alpha must lie in the open interval (0, 1)")
    return beta, alpha


def _grid(grid: object) -> tuple[float, ...]:
    """A non-empty, strictly increasing grid of positive points whose first point is at most 1."""
    if not isinstance(grid, (list, tuple)) or len(grid) == 0:
        raise ValueError("grid must be a non-empty list of capital values")
    points = tuple(_real("grid point", x) for x in grid)
    if any(point <= 0 for point in points):
        raise ValueError("every grid point must be positive")
    if any(a >= b for a, b in pairwise(points)):
        raise ValueError("grid must be strictly increasing")
    if points[0] > 1:
        raise ValueError("the first grid point must be at most 1")
    return points


def _values(values: object, size: int) -> tuple[float, ...]:
    """A vector with one real entry per grid point."""
    if not isinstance(values, (list, tuple)) or len(values) != size:
        raise ValueError("values must have one entry per grid point")
    return tuple(_real("a value", x) for x in values)


def _budget(max_iter: object) -> int:
    """A whole number of sweeps, one or more; a boolean or a float is refused."""
    if isinstance(max_iter, bool) or not isinstance(max_iter, int) or max_iter < 1:
        raise ValueError("max_iter must be a whole number of sweeps, one or more")
    return max_iter


def _tolerance(tol: object) -> float:
    """A finite tolerance greater than zero."""
    number = _real("tol", tol)
    if not number > 0:
        raise ValueError("tol must be greater than zero")
    return number


def _best_at(beta: float, alpha: float, grid: Sequence[float], values: Sequence[float], k: float) -> float:
    """The maximum over feasible successors of the utility of consumption plus the discounted continuation."""
    available = k**alpha
    return max(
        (math.sqrt(available - successor) + beta * continuation)
        for successor, continuation in zip(grid, values, strict=True)
        if successor <= available
    )


def _sweep(beta: float, alpha: float, grid: tuple[float, ...], values: tuple[float, ...]) -> tuple[float, ...]:
    """One synchronous application of the operator, as a pure map: the old vector is read in full."""
    return tuple(_best_at(beta, alpha, grid, values, k) for k in grid)


def _sup_change(new: Sequence[float], old: Sequence[float]) -> float:
    """The sup-norm distance between two vectors of equal length."""
    return reduce(max, (abs(a - b) for a, b in zip(new, old, strict=True)), 0.0)


def bellman_operator(params: Mapping[str, Any], grid: list[float], values: list[float]) -> list[float]:
    """The discounted Bellman operator applied once to a vector of values on the grid."""
    beta, alpha = _params(params)
    points = _grid(grid)
    return list(_sweep(beta, alpha, points, _values(values, len(points))))


def solve(params: Mapping[str, Any], grid: list[float], tol: float, max_iter: int) -> dict[str, Any]:
    """Value-function iteration from zero, stopped by the certified error.

    Returns value (one float per grid point), iterations (the sweeps made, at least 1), certified_error
    (beta / (1 - beta) times the last change of the iterate) and converged (certified_error <= tol).
    """
    beta, alpha = _params(params)
    points = _grid(grid)
    target = _tolerance(tol)
    budget = _budget(max_iter)
    factor = beta / (1 - beta)

    def step(state: tuple[tuple[float, ...], int, float]) -> tuple[tuple[float, ...], int, float]:
        values, count, _ = state
        new = _sweep(beta, alpha, points, values)
        return new, count + 1, factor * _sup_change(new, values)

    start: tuple[tuple[float, ...], int, float] = (tuple(0.0 for _ in points), 0, math.inf)
    state = start
    while state[1] < budget and not state[2] <= target:
        state = step(state)
    values, iterations, certified = state
    return {
        "value": list(values),
        "iterations": iterations,
        "certified_error": certified,
        "converged": certified <= target,
    }
