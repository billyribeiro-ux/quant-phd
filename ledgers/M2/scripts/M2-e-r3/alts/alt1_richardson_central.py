"""Alternative 1 (Richardson): the central estimate is a Richardson extrapolation of the central quotient at h and h/2."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from reference_core import ad_derivative, bond_price_cents, hessian_fd, sensitivities

_SCHEMES = ("forward", "central")


def _positive_step(h: float) -> float:
    step = float(h)
    if not step > 0:
        raise ValueError("the step h must be above zero")
    return step


def _central(f: Callable[[float], float], x: float, step: float) -> float:
    return (f(x + step) - f(x - step)) / (2 * step)


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    step = _positive_step(h)
    if scheme == "forward":
        return (f(x + step) - f(x)) / step
    if scheme == "central":
        half = step / 2
        return (4.0 * _central(f, x, half) - _central(f, x, step)) / 3.0
    raise ValueError("scheme must be 'forward' or 'central'")
