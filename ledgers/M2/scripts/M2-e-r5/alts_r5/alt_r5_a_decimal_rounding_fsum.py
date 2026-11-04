"""Alternative correct engine (verifier round 5, A): decimal half-even rounding, fsum sums, counted powers."""

from __future__ import annotations

import math
from collections.abc import Callable
from decimal import ROUND_HALF_EVEN, Decimal, localcontext
from typing import Any


def _step(h: float) -> float:
    step = float(h)
    if not math.isfinite(step) or not step > 0.0:
        raise ValueError("the step h must be a finite number above zero")
    return step


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    step = _step(h)
    if scheme not in ("forward", "central"):
        raise ValueError("scheme must be 'forward' or 'central'")
    if scheme == "forward":
        return (f(x + step) - f(x)) / step
    return (f(x + step) - f(x - step)) / (2.0 * step)


class _D:
    """A (value, derivative) pair with the rules of forward mode."""

    def __init__(self, v: float, d: float) -> None:
        self.v = v
        self.d = d

    def __add__(self, o: Any) -> _D:
        o = o if isinstance(o, _D) else _D(float(o), 0.0)
        return _D(self.v + o.v, self.d + o.d)

    __radd__ = __add__

    def __sub__(self, o: Any) -> _D:
        o = o if isinstance(o, _D) else _D(float(o), 0.0)
        return _D(self.v - o.v, self.d - o.d)

    def __rsub__(self, o: Any) -> _D:
        o = o if isinstance(o, _D) else _D(float(o), 0.0)
        return o - self

    def __mul__(self, o: Any) -> _D:
        o = o if isinstance(o, _D) else _D(float(o), 0.0)
        return _D(self.v * o.v, self.v * o.d + self.d * o.v)

    __rmul__ = __mul__

    def __neg__(self) -> _D:
        return _D(-self.v, -self.d)


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    result = f(_D(float(x), 1.0))
    return float(result.d) if isinstance(result, _D) else 0.0


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    step = _step(h)
    base = [float(v) for v in x]
    n = len(base)

    def at(shifts: tuple[tuple[int, float], ...]) -> float:
        point = list(base)
        for index, amount in shifts:
            point[index] += amount
        return f(point)

    f0 = at(())
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        out[i][i] = (at(((i, step),)) - 2.0 * f0 + at(((i, -step),))) / (step * step)
        for j in range(i + 1, n):
            term = (
                at(((i, step), (j, step)))
                - at(((i, step), (j, -step)))
                - at(((i, -step), (j, step)))
                + at(((i, -step), (j, -step)))
            )
            out[i][j] = term / (4.0 * step * step)
            out[j][i] = out[i][j]
    return out


def _flows(instance: dict[str, Any]) -> tuple[list[tuple[int, float]], float]:
    bps = instance["yield_bps"]
    if bps <= -10_000:
        raise ValueError("the yield must be above -1 (-10000 basis points)")
    rate = float(bps) / 10_000
    face = float(instance["face_cents"])
    coupon = face * instance["coupon_bps"] / 10_000
    years = int(instance["maturity_years"])
    return [(t, coupon + (face if t == years else 0.0)) for t in range(1, years + 1)], rate


def bond_price_cents(instance: dict[str, Any]) -> int:
    flows, rate = _flows(instance)
    # Exact decimal value of the float price, rounded half to even to whole cents.
    price = math.fsum(cash * (1.0 / (1.0 + rate)) ** t for t, cash in flows)
    with localcontext() as ctx:
        ctx.prec = 400  # a float price can have up to about 310 integer digits
        return int(Decimal(price).quantize(Decimal(1), rounding=ROUND_HALF_EVEN))


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    flows, rate = _flows(instance)
    v = 1.0 / (1.0 + rate)
    price = math.fsum(cash * v**t for t, cash in flows)
    first = -math.fsum(t * cash * v ** (t + 1) for t, cash in flows)
    second = math.fsum(t * (t + 1) * cash * v ** (t + 2) for t, cash in flows)
    return {
        "dprice_dy": first,
        "d2price_dy2": second,
        "duration_analytic": -first / price,
        "convexity_analytic": second / price,
    }
