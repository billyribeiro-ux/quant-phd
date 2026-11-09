"""Starter template for the SC2 project: the Itô derivations engine, ito_checks.py.

Implement each function according to the project specification in project.html.
"""

from __future__ import annotations

from typing import Any


def value(transform: str, t: float, x: float, instance: dict[str, Any]) -> float:
    """Evaluate the transform function f(t, x) for the specified transform index (1 to 10)."""
    raise NotImplementedError("Implement value(transform, t, x, instance)")


def coefficients(transform: str, t: float, x: float, instance: dict[str, Any]) -> tuple[float, float]:
    """Compute the drift mu_Y(t, x) and diffusion sigma_Y(t, x) of the transformed process Y_t = f(t, X_t)."""
    raise NotImplementedError("Implement coefficients(transform, t, x, instance)")


def residual(transform: str, instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    """Compute the mean and standard error of the discrete Itô residual across simulated base paths."""
    raise NotImplementedError("Implement residual(transform, instance, n_steps)")
