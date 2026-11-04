"""Round 7 alternative A (verifier D7): exact-decimal price, fsum sensitivities, Richardson-extrapolated central estimate.

A different correct engine: the price is a 50-digit Decimal sum quantized half-to-even; sensitivities are fsum of the
cash-flow terms; fd_derivative 'central' is the Richardson combination (4 D(h/2) - D(h)) / 3, which cancels the h^2
term; the step and scheme checks use explicit type tests. Standard library only.
"""
from __future__ import annotations

import math
from collections.abc import Callable
from decimal import ROUND_HALF_EVEN, Decimal, localcontext
from typing import Any


def _positive_step(h: float) -> float:
    if isinstance(h, bool) or not isinstance(h, (int, float)):
        raise ValueError("the step h must be a number above zero")
    step = float(h)
    if math.isnan(step) or not step > 0.0:
        raise ValueError("the step h must be above zero")
    return step


def _central_raw(f: Callable[[float], float], x: float, step: float) -> float:
    return (f(x + step) - f(x - step)) / (2 * step)


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    step = _positive_step(h)
    if type(scheme) is not str or scheme not in ("forward", "central"):
        raise ValueError("scheme must be 'forward' or 'central'")
    if scheme == "forward":
        return (f(x + step) - f(x)) / step
    return (4.0 * _central_raw(f, x, step / 2) - _central_raw(f, x, step)) / 3.0


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
    return x if isinstance(x, _Dual) else _Dual(float(x), 0.0)


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    return float(_lift(f(_Dual(float(x), 1.0))).dot)


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    step = _positive_step(h)
    base = [float(v) for v in x]
    n = len(base)

    def at(changes: dict[int, float]) -> float:
        point = list(base)
        for k, amount in changes.items():
            point[k] += amount
        return f(point)

    f0 = f(list(base))
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        out[i][i] = math.fsum([at({i: step}), -2.0 * f0, at({i: -step})]) / (step * step)
        for j in range(i + 1, n):
            mixed = math.fsum(
                [
                    at({i: step, j: step}),
                    -at({i: step, j: -step}),
                    -at({i: -step, j: step}),
                    at({i: -step, j: -step}),
                ]
            )
            out[i][j] = out[j][i] = mixed / (4.0 * step * step)
    return out


def _rate(instance: dict[str, Any]) -> float:
    yield_bps = instance["yield_bps"]
    if yield_bps <= -10_000:
        raise ValueError("the yield must be above -1 (-10000 basis points)")
    return float(yield_bps) / 10_000


def _flows(instance: dict[str, Any]) -> list[tuple[int, float]]:
    face = float(instance["face_cents"])
    coupon = face * instance["coupon_bps"] / 10_000
    years = int(instance["maturity_years"])
    return [(t, coupon + (face if t == years else 0.0)) for t in range(1, years + 1)]


def bond_price_cents(instance: dict[str, Any]) -> int:
    if int(instance["yield_bps"]) <= -10_000:
        raise ValueError("the yield must be above -1 (-10000 basis points)")
    flows = _flows(instance)
    with localcontext() as ctx:
        ctx.prec = 400
        rate = Decimal(int(instance["yield_bps"])) / Decimal(10_000)
        v = Decimal(1) / (Decimal(1) + rate)
        total = sum((Decimal(cash) * v ** t for t, cash in flows), Decimal(0))
        return int(total.quantize(Decimal(1), rounding=ROUND_HALF_EVEN))


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    rate = _rate(instance)
    flows = _flows(instance)
    v = 1 / (1 + rate)
    price = math.fsum(cash * v**t for t, cash in flows)
    first = -math.fsum(t * cash * v ** (t + 1) for t, cash in flows)
    second = math.fsum(t * (t + 1) * cash * v ** (t + 2) for t, cash in flows)
    return {
        "dprice_dy": first,
        "d2price_dy2": second,
        "duration_analytic": -first / price,
        "convexity_analytic": second / price,
    }
