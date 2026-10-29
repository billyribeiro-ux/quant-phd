"""Alternative correct engine: Richardson-extrapolated central estimate, fsum forward, exact Fraction bond maths."""

from __future__ import annotations

import math
from collections.abc import Callable
from fractions import Fraction
from typing import Any


def _step(h: float) -> float:
    s = float(h)
    if not s > 0:
        raise ValueError("step must be above zero")
    return s


def _central(f: Callable[[float], float], x: float, h: float) -> float:
    return (f(x + h) - f(x - h)) / (2 * h)


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    step = _step(h)
    if scheme == "forward":
        return math.fsum([f(x + step), -f(x)]) / step
    if scheme == "central":
        half = step / 2
        return (4 * _central(f, x, half) - _central(f, x, step)) / 3
    raise ValueError("scheme must be forward or central")


class _D:
    __slots__ = ("v", "d")

    def __init__(self, v: float, d: float) -> None:
        self.v = v
        self.d = d

    def __add__(self, o: Any) -> _D:
        o = _L(o)
        return _D(self.v + o.v, self.d + o.d)

    def __radd__(self, o: Any) -> _D:
        return self.__add__(o)

    def __sub__(self, o: Any) -> _D:
        o = _L(o)
        return _D(self.v - o.v, self.d - o.d)

    def __rsub__(self, o: Any) -> _D:
        o = _L(o)
        return _D(o.v - self.v, o.d - self.d)

    def __mul__(self, o: Any) -> _D:
        o = _L(o)
        return _D(self.v * o.v, self.d * o.v + self.v * o.d)

    def __rmul__(self, o: Any) -> _D:
        return self.__mul__(o)


def _L(x: Any) -> _D:
    return x if isinstance(x, _D) else _D(float(x), 0.0)


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    return float(_L(f(_D(float(x), 1.0))).d)


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    step = _step(h)
    p = [float(v) for v in x]
    n = len(p)

    def at(d: dict[int, float]) -> float:
        q = list(p)
        for k, v in d.items():
            q[k] += v
        return f(q)

    f0 = at({})
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        out[i][i] = (at({i: step}) - 2 * f0 + at({i: -step})) / (step * step)
        for j in range(i + 1, n):
            m = math.fsum(
                [
                    at({i: step, j: step}),
                    -at({i: step, j: -step}),
                    -at({i: -step, j: step}),
                    at({i: -step, j: -step}),
                ]
            ) / (4 * step * step)
            out[i][j] = out[j][i] = m
    return out


def _yield(inst: dict[str, Any]) -> Fraction:
    b = inst["yield_bps"]
    if b <= -10_000:
        raise ValueError("yield must be above -1")
    return Fraction(b, 10_000)


def _flows(inst: dict[str, Any]) -> tuple[list[tuple[int, Fraction]], Fraction]:
    r = _yield(inst)
    face = Fraction(inst["face_cents"])
    coupon = face * Fraction(inst["coupon_bps"], 10_000)
    n = int(inst["maturity_years"])
    return [(t, coupon + (face if t == n else Fraction(0))) for t in range(1, n + 1)], r


def bond_price_cents(inst: dict[str, Any]) -> int:
    flows, r = _flows(inst)
    v = 1 / (1 + r)
    price = sum((c * v**t for t, c in flows), Fraction(0))
    return int(round(price))


def sensitivities(inst: dict[str, Any]) -> dict[str, float]:
    flows, r = _flows(inst)
    v = 1 / (1 + r)
    price = sum((c * v**t for t, c in flows), Fraction(0))
    first = -sum((t * c * v ** (t + 1) for t, c in flows), Fraction(0))
    second = sum((t * (t + 1) * c * v ** (t + 2) for t, c in flows), Fraction(0))
    return {
        "dprice_dy": float(first),
        "d2price_dy2": float(second),
        "duration_analytic": float(-first / price),
        "convexity_analytic": float(second / price),
    }
