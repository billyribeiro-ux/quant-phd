"""Alternative 4: complex-step AD, Richardson central difference, exact rational price, closed-form sensitivities."""

from __future__ import annotations

import math
from collections.abc import Callable
from fractions import Fraction
from typing import Any


def _check_step(h: float) -> None:
    if not h > 0:
        raise ValueError("step must be above zero")


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    _check_step(h)
    if scheme == "forward":
        return (f(x + h) - f(x)) / h
    if scheme == "central":
        d1 = (f(x + h) - f(x - h)) / (2 * h)
        d2 = (f(x + h / 2) - f(x - h / 2)) / h
        return (4 * d2 - d1) / 3  # Richardson: cancels the leading h squared term
    raise ValueError("scheme must be forward or central")


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    step = 1e-30
    value = f(complex(x, step))
    return complex(value).imag / step


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    _check_step(h)
    n = len(x)

    def at(dx: dict[int, float]) -> float:
        p = list(x)
        for i, d in dx.items():
            p[i] += d
        return f(p)

    f0 = f(list(x))
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        out[i][i] = (at({i: h}) - 2 * f0 + at({i: -h})) / (h * h)
        for j in range(n):
            if j == i:
                continue
            out[i][j] = (at({i: h, j: h}) - at({i: h, j: -h}) - at({i: -h, j: h}) + at({i: -h, j: -h})) / (4 * h * h)
    return out


def bond_price_cents(instance: dict[str, Any]) -> int:
    y = Fraction(instance["yield_bps"], 10_000)
    if y <= -1:
        raise ValueError("yield must be above -1")
    face = instance["face_cents"]
    coupon = Fraction(face * instance["coupon_bps"], 10_000)
    years = instance["maturity_years"]
    v = 1 / (1 + y)
    total = sum((coupon + (face if t == years else 0)) * v**t for t in range(1, years + 1))
    return int(round(total))  # round() on a Fraction is half to even


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    y = instance["yield_bps"] / 10_000
    if y <= -1:
        raise ValueError("yield must be above -1")
    face = instance["face_cents"]
    coupon = face * instance["coupon_bps"] / 10_000
    years = instance["maturity_years"]
    v = 1.0 / (1.0 + y)
    flows = [(t, coupon + (face if t == years else 0)) for t in range(1, years + 1)]
    price = math.fsum(c * v**t for t, c in flows)
    d1 = -math.fsum(t * c * v ** (t + 1) for t, c in flows)
    d2 = math.fsum(t * (t + 1) * c * v ** (t + 2) for t, c in flows)
    return {
        "dprice_dy": d1,
        "d2price_dy2": d2,
        "duration_analytic": -d1 / price,
        "convexity_analytic": d2 / price,
    }
