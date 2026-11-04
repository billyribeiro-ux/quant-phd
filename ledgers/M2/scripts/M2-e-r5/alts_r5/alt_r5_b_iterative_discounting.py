"""Alternative correct engine (verifier round 5, B): iterative discounting, Horner-style sums, lifted constants."""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import Any


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    if isinstance(h, bool) or not isinstance(h, (int, float)):
        raise ValueError("the step must be a real number")
    step = float(h)
    if math.isnan(step) or step <= 0.0:
        raise ValueError("the step h must be above zero")
    if scheme == "forward":
        return (f(x + step) - f(x)) / step
    if scheme == "central":
        return (f(x + step) - f(x - step)) / (2.0 * step)
    raise ValueError("scheme must be 'forward' or 'central'")


class _Dual:
    __slots__ = ("val", "dot")

    def __init__(self, val: float, dot: float) -> None:
        self.val = val
        self.dot = dot

    def _lift(self, o: Any) -> _Dual:
        return o if isinstance(o, _Dual) else _Dual(float(o), 0.0)

    def __add__(self, o: Any) -> _Dual:
        p = self._lift(o)
        return _Dual(self.val + p.val, self.dot + p.dot)

    def __radd__(self, o: Any) -> _Dual:
        return self + o

    def __sub__(self, o: Any) -> _Dual:
        p = self._lift(o)
        return _Dual(self.val - p.val, self.dot - p.dot)

    def __rsub__(self, o: Any) -> _Dual:
        return self._lift(o) - self

    def __mul__(self, o: Any) -> _Dual:
        p = self._lift(o)
        return _Dual(self.val * p.val, self.dot * p.val + self.val * p.dot)

    def __rmul__(self, o: Any) -> _Dual:
        return self * o


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    out = f(_Dual(float(x), 1.0))
    return out.dot if isinstance(out, _Dual) else 0.0


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    step = float(h)
    if math.isnan(step) or step <= 0.0:
        raise ValueError("the step h must be above zero")
    base = [float(v) for v in x]
    n = len(base)
    f0 = f(base)
    rows: list[list[float]] = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                up = list(base)
                dn = list(base)
                up[i] += step
                dn[i] -= step
                row.append((f(up) - 2.0 * f0 + f(dn)) / step**2)
            else:
                pp, pm, mp, mm = (list(base) for _ in range(4))
                pp[i] += step
                pp[j] += step
                pm[i] += step
                pm[j] -= step
                mp[i] -= step
                mp[j] += step
                mm[i] -= step
                mm[j] -= step
                row.append((f(pp) - f(pm) - f(mp) + f(mm)) / (4.0 * step**2))
        rows.append(row)
    return rows


def _cashflows(instance: dict[str, Any]) -> tuple[list[float], float]:
    bps = instance["yield_bps"]
    if bps <= -10_000:
        raise ValueError("the yield must be above -1 (-10000 basis points)")
    rate = float(bps) / 10_000
    face = float(instance["face_cents"])
    coupon = face * instance["coupon_bps"] / 10_000
    years = int(instance["maturity_years"])
    return [coupon + (face if t == years else 0.0) for t in range(1, years + 1)], rate


def bond_price_cents(instance: dict[str, Any]) -> int:
    cash, rate = _cashflows(instance)
    v = 1.0 / (1.0 + rate)
    total = 0.0
    factor = 1.0
    for c in cash:
        factor *= v
        total += c * factor
    # Python's round() on a float is round-half-to-even, as the project requires.
    return round(total)


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    cash, rate = _cashflows(instance)
    v = 1.0 / (1.0 + rate)
    price = 0.0
    first = 0.0
    second = 0.0
    for t, c in enumerate(cash, start=1):
        d_t = v**t
        price += c * d_t
        first += -t * c * d_t / (1.0 + rate)
        second += t * (t + 1) * c * d_t / (1.0 + rate) ** 2
    return {
        "dprice_dy": first,
        "d2price_dy2": second,
        "duration_analytic": -first / price,
        "convexity_analytic": second / price,
    }
