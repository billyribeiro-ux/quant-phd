"""the parameters are read the wrong way round: beta is taken from the alpha key and alpha from the beta key"""

from __future__ import annotations

import math
from collections.abc import Mapping
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
    beta = _real("beta", params.get("alpha"))
    alpha = _real("alpha", params.get("beta"))
    if not 0 < beta < 1:
        raise ValueError("beta must lie in the open interval (0, 1)")
    if not 0 < alpha < 1:
        raise ValueError("alpha must lie in the open interval (0, 1)")
    return beta, alpha


def _grid(grid: object) -> list[float]:
    """A non-empty, strictly increasing grid of positive points whose first point is at most 1."""
    if not isinstance(grid, (list, tuple)) or len(grid) == 0:
        raise ValueError("grid must be a non-empty list of capital values")
    points = [_real("grid point", x) for x in grid]
    if any(point <= 0 for point in points):
        raise ValueError("every grid point must be positive")
    if any(points[i] >= points[i + 1] for i in range(len(points) - 1)):
        raise ValueError("grid must be strictly increasing")
    if points[0] > 1:
        raise ValueError("the first grid point must be at most 1")
    return points


def _values(values: object, size: int) -> list[float]:
    """A vector with one real entry per grid point."""
    if not isinstance(values, (list, tuple)) or len(values) != size:
        raise ValueError("values must have one entry per grid point")
    return [_real("a value", x) for x in values]


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


def _sweep(beta: float, alpha: float, grid: list[float], values: list[float]) -> list[float]:
    """One synchronous application of the Bellman operator."""
    out: list[float] = []
    for k in grid:
        available = k**alpha
        best = -math.inf
        for successor, continuation in zip(grid, values, strict=True):
            if successor <= available:
                best = max(best, math.sqrt(available - successor) + beta * continuation)
        out.append(best)
    return out


def bellman_operator(params: Mapping[str, Any], grid: list[float], values: list[float]) -> list[float]:
    """The discounted Bellman operator applied once to a vector of values on the grid."""
    beta, alpha = _params(params)
    points = _grid(grid)
    return _sweep(beta, alpha, points, _values(values, len(points)))


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
    values = [0.0] * len(points)
    iterations = 0
    certified = math.inf
    while iterations < budget:
        new = _sweep(beta, alpha, points, values)
        iterations += 1
        change = max(abs(a - b) for a, b in zip(new, values, strict=True))
        values = new
        certified = factor * change
        if certified <= target:
            break
    return {
        "value": values,
        "iterations": iterations,
        "certified_error": certified,
        "converged": certified <= target,
    }
