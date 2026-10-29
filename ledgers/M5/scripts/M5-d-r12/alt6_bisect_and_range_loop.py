# Alternative correct implementation (verifier round 12, M5 slice d): bisect for the feasible prefix, range loop with break, factor computed as 1/((1-beta)/beta), max via map.
"""Alternative correct contraction_solver for the M5 project, used to test for over-constraint."""

from __future__ import annotations

import math
from bisect import bisect_right
from collections.abc import Mapping
from typing import Any


def _check(params: Mapping[str, Any], grid: list[float]) -> tuple[float, float, list[float]]:
    beta = params["beta"]
    alpha = params["alpha"]
    if isinstance(beta, bool) or not isinstance(beta, (int, float)) or not 0 < beta < 1:
        raise ValueError("beta")
    if isinstance(alpha, bool) or not isinstance(alpha, (int, float)) or not 0 < alpha < 1:
        raise ValueError("alpha")
    if not isinstance(grid, (list, tuple)) or not grid:
        raise ValueError("grid")
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) for x in grid):
        raise ValueError("grid point")
    pts = [float(x) for x in grid]
    if any(not math.isfinite(x) or x <= 0 for x in pts):
        raise ValueError("grid point")
    if any(b <= a for a, b in zip(pts, pts[1:])):
        raise ValueError("grid order")
    if pts[0] > 1:
        raise ValueError("first point")
    return float(beta), float(alpha), pts


def bellman_operator(params: Mapping[str, Any], grid: list[float], values: list[float]) -> list[float]:
    beta, alpha, pts = _check(params, grid)
    if not isinstance(values, (list, tuple)) or len(values) != len(pts):
        raise ValueError("values")
    out = []
    for k in pts:
        avail = k**alpha
        last = bisect_right(pts, avail)
        out.append(max(math.sqrt(avail - pts[j]) + beta * values[j] for j in range(last)))
    return out


def solve(params: Mapping[str, Any], grid: list[float], tol: float, max_iter: int) -> dict[str, Any]:
    beta, alpha, pts = _check(params, grid)
    if isinstance(tol, bool) or not isinstance(tol, (int, float)) or not math.isfinite(tol) or tol <= 0:
        raise ValueError("tol")
    if isinstance(max_iter, bool) or not isinstance(max_iter, int) or max_iter < 1:
        raise ValueError("max_iter")
    factor = 1 / ((1 - beta) / beta)
    v = [0.0] * len(pts)
    certified = math.inf
    made = 0
    for _ in range(max_iter):
        new = bellman_operator(params, pts, v)
        made += 1
        change = max(map(lambda a, b: abs(a - b), new, v))
        v = new
        certified = factor * change
        if certified <= tol:
            break
    return {"value": v, "iterations": made, "certified_error": certified, "converged": certified <= tol}
