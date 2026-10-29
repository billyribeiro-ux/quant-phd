"""Starter for the M5 project: contraction_solver.py, the discounted Bellman operator and its solver.

Implement every function to the contract in project.html, section "Rung 3 · Specification", then run the
autograder there, or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Use the standard library only. Every input the specification names must raise ValueError. No function may print
or warn.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def bellman_operator(params: Mapping[str, Any], grid: list[float], values: list[float]) -> list[float]:
    """The discounted Bellman operator applied once to a vector of values on the grid."""
    raise NotImplementedError("bellman_operator is not written yet")


def solve(params: Mapping[str, Any], grid: list[float], tol: float, max_iter: int) -> dict[str, Any]:
    """Value-function iteration from zero, stopped by the certified error. Returns value, iterations,
    certified_error and converged."""
    raise NotImplementedError("solve is not written yet")
