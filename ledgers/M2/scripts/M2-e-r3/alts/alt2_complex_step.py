"""Alternative 2 (complex step): ad_derivative is the imaginary part of f(x + i h) divided by h, for a real-analytic f."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from reference_core import bond_price_cents, fd_derivative, hessian_fd, sensitivities


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    step = 1e-20
    value = f(complex(float(x), step))
    return float(complex(value).imag / step)
