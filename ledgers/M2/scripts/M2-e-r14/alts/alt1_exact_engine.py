"""Reference solution for the M2 project: sensitivity_engine.py, the sensitivity engine.

It implements the contract in project.html, section "Rung 3 · Specification". Standard library only.

Conventions (binding, from the project specification):

* a step h is a positive real number, in the units of the variable it differentiates;
* a bond is priced in annual periods: a cash flow of coupon cents at each year end, and the face value in cents added
  at the final year; the yield is an annual rate, so the discount factor of year t is 1 / (1 + yield) ** t;
* the bond price is returned as an integer number of cents, rounded half to even from the unrounded price;
* the sensitivities are derivatives of the unrounded price in cents: they are floats, not money.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

_SCHEMES = ("forward", "central")


from fractions import Fraction


def _positive_step(h: float) -> float:
    step = float(h)
    if not step > 0:
        raise ValueError("the step h must be above zero")
    return step


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    step = _positive_step(h)
    inv = 1.0 / step
    if scheme == "forward":
        return (f(x + step) - f(x)) * inv
    if scheme == "central":
        return (f(x + step) - f(x - step)) * (0.5 * inv)
    raise ValueError("scheme must be 'forward' or 'central'")


class _Dual:
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
    result = f(_Dual(float(x), 1.0))
    return float(_lift(result).dot)


def _moved(base: list[float], changes: dict[int, float]) -> list[float]:
    out = list(base)
    for k, d in changes.items():
        out[k] = out[k] + d
    return out


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    step = _positive_step(h)
    base = [float(v) for v in x]
    n = len(base)
    f0 = f(base)
    scale = 1.0 / (step * step)
    rows: list[list[float]] = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                up = f(_moved(base, {i: step}))
                down = f(_moved(base, {i: -step}))
                row.append((up - 2 * f0 + down) * scale)
            else:
                mixed = (
                    f(_moved(base, {i: step, j: step}))
                    - f(_moved(base, {i: step, j: -step}))
                    - f(_moved(base, {i: -step, j: step}))
                    + f(_moved(base, {i: -step, j: -step}))
                )
                row.append(mixed * 0.25 * scale)
        rows.append(row)
    return rows


def _yield_rate(instance: dict[str, Any]) -> Fraction:
    yield_bps = instance["yield_bps"]
    if yield_bps <= -10_000:
        raise ValueError("the yield must be above -1 (-10000 basis points)")
    return Fraction(yield_bps, 10_000)


def _cash_flows(instance: dict[str, Any]) -> tuple[list[tuple[int, Fraction]], Fraction]:
    rate = _yield_rate(instance)
    face = Fraction(instance["face_cents"])
    coupon = face * Fraction(instance["coupon_bps"], 10_000)
    years = int(instance["maturity_years"])
    flows = [(t, coupon + (face if t == years else Fraction(0))) for t in range(1, years + 1)]
    return flows, rate


def bond_price_cents(instance: dict[str, Any]) -> int:
    flows, rate = _cash_flows(instance)
    v = 1 / (1 + rate)
    price = sum((cash * v**t for t, cash in flows), Fraction(0))
    q, r = divmod(price.numerator, price.denominator)
    if 2 * r > price.denominator or (2 * r == price.denominator and q % 2 == 1):
        q += 1
    return q


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    flows, rate = _cash_flows(instance)
    v = 1 / (1 + rate)
    price = sum((cash * v**t for t, cash in flows), Fraction(0))
    first = -sum((t * cash * v ** (t + 1) for t, cash in flows), Fraction(0))
    second = sum((t * (t + 1) * cash * v ** (t + 2) for t, cash in flows), Fraction(0))
    return {
        "dprice_dy": float(first),
        "d2price_dy2": float(second),
        "duration_analytic": float(-first / price),
        "convexity_analytic": float(second / price),
    }
