"""Alternative correct engine: NumPy vector sums for the price and sensitivities, np.round for the cent."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np

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


class _Dual:
    __slots__ = ("dot", "value")

    def __init__(self, value: float, dot: float) -> None:
        self.value = value
        self.dot = dot

    def __add__(self, other: Any) -> _Dual:
        o = _lift(other)
        return _Dual(self.value + o.value, self.dot + o.dot)

    __radd__ = __add__

    def __sub__(self, other: Any) -> _Dual:
        o = _lift(other)
        return _Dual(self.value - o.value, self.dot - o.dot)

    def __rsub__(self, other: Any) -> _Dual:
        o = _lift(other)
        return _Dual(o.value - self.value, o.dot - self.dot)

    def __mul__(self, other: Any) -> _Dual:
        o = _lift(other)
        return _Dual(self.value * o.value, self.value * o.dot + self.dot * o.value)

    __rmul__ = __mul__


def _lift(x: Any) -> _Dual:
    if isinstance(x, _Dual):
        return x
    return _Dual(float(x), 0.0)


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    result = _lift(f(_Dual(float(x), 1.0)))
    return float(result.dot)


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


def _vectors(instance: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, float]:
    if instance["yield_bps"] <= -10_000:
        raise ValueError("the yield must be above -1")
    years = int(instance["maturity_years"])
    face = float(instance["face_cents"])
    coupon = face * instance["coupon_bps"] / 10_000
    t = np.arange(1, years + 1, dtype=np.float64)
    cash = np.full(years, coupon)
    cash[-1] += face
    return t, cash, instance["yield_bps"] / 10_000


def bond_price_cents(instance: dict[str, Any]) -> int:
    t, cash, rate = _vectors(instance)
    price = float(np.sum(cash * (1.0 + rate) ** (-t)))
    return int(np.round(price))


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    t, cash, rate = _vectors(instance)
    v = 1.0 / (1.0 + rate)
    price = float(np.sum(cash * v**t))
    first = float(-np.sum(t * cash * v ** (t + 1)))
    second = float(np.sum(t * (t + 1) * cash * v ** (t + 2)))
    return {
        "dprice_dy": first,
        "d2price_dy2": second,
        "duration_analytic": -first / price,
        "convexity_analytic": second / price,
    }
