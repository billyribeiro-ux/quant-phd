"""Starter for the M2 project: sensitivity_engine.py, the sensitivity engine.

Implement every function to the contract in project.html, section "Rung 3 · Specification", then run the
autograder there, or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Use the standard library only. Every function must follow the specification. No function may print or warn.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    """A finite-difference estimate of f'(x) with step h, by the scheme "forward" or "central"."""
    raise NotImplementedError("fd_derivative is not written yet")


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    """The derivative of f at x by forward-mode automatic differentiation."""
    raise NotImplementedError("ad_derivative is not written yet")


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    """The Hessian of f at x, a square list of lists, by finite differences with step h."""
    raise NotImplementedError("hessian_fd is not written yet")


def bond_price_cents(instance: dict[str, Any]) -> int:
    """The bond price in integer cents, rounded half to even from the unrounded price."""
    raise NotImplementedError("bond_price_cents is not written yet")


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    """The analytic sensitivities of the unrounded bond price to its yield."""
    raise NotImplementedError("sensitivities is not written yet")
