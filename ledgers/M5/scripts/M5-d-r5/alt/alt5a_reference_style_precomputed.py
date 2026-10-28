"""Alternative correct solver (verifier, round 5): precomputed feasible index lists, x**0.5 for the square root, sup change, sweep certificate."""
from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any


def _check(params: Mapping[str, Any], grid: Any) -> tuple[float, float, list[float]]:
    for name in ("beta", "alpha"):
        v = params.get(name)
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(float(v)) or not 0 < float(v) < 1:
            raise ValueError(f"{name} must lie in (0, 1)")
    beta, alpha = float(params["beta"]), float(params["alpha"])
    if not isinstance(grid, (list, tuple)) or len(grid) == 0:
        raise ValueError("empty grid")
    pts = []
    for x in grid:
        if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(float(x)) or float(x) <= 0:
            raise ValueError("grid point must be a positive real number")
        pts.append(float(x))
    for a, b in zip(pts, pts[1:]):
        if not a < b:
            raise ValueError("grid must be strictly increasing")
    if pts[0] > 1:
        raise ValueError("first grid point must be at most 1")
    return beta, alpha, pts


def _feasible_table(alpha: float, pts: list[float]) -> list[list[int]]:
    return [[j for j, kp in enumerate(pts) if kp <= k**alpha] for k in pts]


def _apply(beta: float, alpha: float, pts: list[float], table: list[list[int]], values: list[float]) -> list[float]:
    out = []
    for i, k in enumerate(pts):
        res = k**alpha
        out.append(max((res - pts[j]) ** 0.5 + beta * values[j] for j in table[i]))
    return out


def bellman_operator(params: Mapping[str, Any], grid: list[float], values: list[float]) -> list[float]:
    beta, alpha, pts = _check(params, grid)
    if not isinstance(values, (list, tuple)) or len(values) != len(pts):
        raise ValueError("values must match the grid length")
    vals = [float(v) for v in values]
    return _apply(beta, alpha, pts, _feasible_table(alpha, pts), vals)


def solve(params: Mapping[str, Any], grid: list[float], tol: float, max_iter: int) -> dict[str, Any]:
    beta, alpha, pts = _check(params, grid)
    if isinstance(tol, bool) or not isinstance(tol, (int, float)) or not math.isfinite(float(tol)) or float(tol) <= 0:
        raise ValueError("tol must be finite and greater than zero")
    if isinstance(max_iter, bool) or not isinstance(max_iter, int) or max_iter < 1:
        raise ValueError("max_iter must be a whole number of sweeps, one or more")
    table = _feasible_table(alpha, pts)
    vals = [0.0] * len(pts)
    sweeps = 0
    cert = math.inf
    while sweeps < max_iter:
        new = _apply(beta, alpha, pts, table, vals)
        sweeps += 1
        change = max(abs(x - y) for x, y in zip(new, vals))
        vals = new
        cert = beta / (1.0 - beta) * change
        if cert <= float(tol):
            break
    return {"value": vals, "iterations": sweeps, "certified_error": cert, "converged": cert <= float(tol)}
