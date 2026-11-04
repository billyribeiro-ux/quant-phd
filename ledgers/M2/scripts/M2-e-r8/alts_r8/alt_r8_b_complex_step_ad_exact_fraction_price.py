"""Alternative correct engine: complex-step ad_derivative, exact Fraction price and sensitivities, plain quotients."""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction
from typing import Any

_SCHEMES = ("forward", "central")


def _positive_step(h: float) -> float:
    step = float(h)
    if not step > 0:
        raise ValueError("the step h must be above zero")
    return step


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    step = _positive_step(h)
    if scheme == "forward":
        return (f(x + step) - f(x)) / step
    if scheme == "central":
        return (f(x + step) - f(x - step)) / (2 * step)
    raise ValueError("scheme must be 'forward' or 'central'")


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    h = 1e-20
    value = f(complex(float(x), h))
    return float(complex(value).imag / h)


def _moved(base: list[float], changes: dict[int, float]) -> list[float]:
    point = list(base)
    for index, amount in changes.items():
        point[index] += amount
    return point


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    step = _positive_step(h)
    base = [float(v) for v in x]
    n = len(base)
    hessian = [[0.0] * n for _ in range(n)]
    f0 = f(base)
    for i in range(n):
        up = f(_moved(base, {i: step}))
        down = f(_moved(base, {i: -step}))
        hessian[i][i] = (up - 2 * f0 + down) / (step * step)
        for j in range(i + 1, n):
            mixed = (
                f(_moved(base, {i: step, j: step}))
                - f(_moved(base, {i: step, j: -step}))
                - f(_moved(base, {i: -step, j: step}))
                + f(_moved(base, {i: -step, j: -step}))
            )
            hessian[i][j] = mixed / (4 * step * step)
            hessian[j][i] = hessian[i][j]
    return hessian


def _exact(instance: dict[str, Any]) -> tuple[int, Fraction, Fraction, Fraction]:
    if instance["yield_bps"] <= -10_000:
        raise ValueError("the yield must be above -1")
    face = Fraction(instance["face_cents"])
    coupon = face * instance["coupon_bps"] / 10_000
    v = 1 / (1 + Fraction(instance["yield_bps"], 10_000))
    return int(instance["maturity_years"]), face, coupon, v


def bond_price_cents(instance: dict[str, Any]) -> int:
    years, face, coupon, v = _exact(instance)
    price = sum((coupon + (face if t == years else 0)) * v**t for t in range(1, years + 1))
    return round(price)


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    years, face, coupon, v = _exact(instance)
    flows = [(t, coupon + (face if t == years else 0)) for t in range(1, years + 1)]
    price = sum((cash * v**t for t, cash in flows), Fraction(0))
    first = -sum((t * cash * v ** (t + 1) for t, cash in flows), Fraction(0))
    second = sum((t * (t + 1) * cash * v ** (t + 2) for t, cash in flows), Fraction(0))
    return {
        "dprice_dy": float(first),
        "d2price_dy2": float(second),
        "duration_analytic": float(-first / price),
        "convexity_analytic": float(second / price),
    }
