"""Alternative: object style. The feasible successors are precomputed once in a class; the result is a dataclass.

The operator is synchronous and the feasibility test is the exact k' <= k**alpha. The solver stops at the first sweep
whose certified error beta / (1 - beta) * sup-norm change is at most tol. Standard library only.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
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


@dataclass(frozen=True)
class SolveResult:
    """The four fields the specification names."""

    value: list[float]
    iterations: int
    certified_error: float
    converged: bool


class ContractionSolver:
    """The operator on one grid, with each state's feasible successor indices computed once."""

    def __init__(self, beta: float, alpha: float, grid: list[float]) -> None:
        self.beta = beta
        self.grid = grid
        self.resources = [k**alpha for k in grid]
        self.feasible = [[j for j, kp in enumerate(grid) if kp <= available] for available in self.resources]
        self.consumption = [
            [math.sqrt(self.resources[i] - grid[j]) for j in self.feasible[i]] for i in range(len(grid))
        ]

    def apply(self, values: list[float]) -> list[float]:
        """One synchronous sweep: each state reads the whole previous vector."""
        return [
            max(c + self.beta * values[j] for j, c in zip(self.feasible[i], self.consumption[i], strict=True))
            for i in range(len(self.grid))
        ]

    def iterate(self, tol: float, budget: int) -> SolveResult:
        """Sweeps from zero until the certified error is at most tol or the budget is spent."""
        factor = self.beta / (1 - self.beta)
        values = [0.0] * len(self.grid)
        sweeps = 0
        certified = math.inf
        while sweeps < budget:
            new = self.apply(values)
            sweeps += 1
            change = max(abs(a - b) for a, b in zip(new, values, strict=True))
            values = new
            certified = factor * change
            if certified <= tol:
                break
        return SolveResult(value=values, iterations=sweeps, certified_error=certified, converged=certified <= tol)


def bellman_operator(params: Mapping[str, Any], grid: list[float], values: list[float]) -> list[float]:
    """The discounted Bellman operator applied once to a vector of values on the grid."""
    beta, alpha = _params(params)
    points = _grid(grid)
    return ContractionSolver(beta, alpha, points).apply(_values(values, len(points)))


def solve(params: Mapping[str, Any], grid: list[float], tol: float, max_iter: int) -> dict[str, Any]:
    """Value-function iteration from zero, stopped by the certified error.

    Returns value (one float per grid point), iterations (the sweeps made, at least 1), certified_error
    (beta / (1 - beta) times the last change of the iterate) and converged (certified_error <= tol).
    """
    beta, alpha = _params(params)
    points = _grid(grid)
    target = _tolerance(tol)
    budget = _budget(max_iter)
    result = ContractionSolver(beta, alpha, points).iterate(target, budget)
    return {
        "value": result.value,
        "iterations": result.iterations,
        "certified_error": result.certified_error,
        "converged": result.converged,
    }
