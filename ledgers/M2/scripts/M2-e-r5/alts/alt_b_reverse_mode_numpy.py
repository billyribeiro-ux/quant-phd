"""Alternative B: reverse-mode automatic differentiation on a tape, NumPy vector sums for the price and sensitivities."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np


def _step(h: float) -> float:
    if not (h > 0):
        raise ValueError("step must be above zero")
    return float(h)


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    s = _step(h)
    if scheme == "forward":
        return float((f(x + s) - f(x)) / s)
    if scheme == "central":
        return float((f(x + s) - f(x - s)) / (2 * s))
    raise ValueError("scheme must be forward or central")


class _Node:
    def __init__(self, value: float, parents: list[tuple[_Node, float]]) -> None:
        self.value = value
        self.parents = parents
        self.adj = 0.0

    def __add__(self, other: Any) -> _Node:
        o = _as(other)
        return _Node(self.value + o.value, [(self, 1.0), (o, 1.0)])

    __radd__ = __add__

    def __sub__(self, other: Any) -> _Node:
        o = _as(other)
        return _Node(self.value - o.value, [(self, 1.0), (o, -1.0)])

    def __rsub__(self, other: Any) -> _Node:
        o = _as(other)
        return _Node(o.value - self.value, [(o, 1.0), (self, -1.0)])

    def __mul__(self, other: Any) -> _Node:
        o = _as(other)
        return _Node(self.value * o.value, [(self, o.value), (o, self.value)])

    __rmul__ = __mul__


def _as(x: Any) -> _Node:
    return x if isinstance(x, _Node) else _Node(float(x), [])


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    root = _Node(float(x), [])
    out = _as(f(root))
    order: list[_Node] = []
    seen: set[int] = set()

    def visit(n: _Node) -> None:
        if id(n) in seen:
            return
        seen.add(id(n))
        for p, _ in n.parents:
            visit(p)
        order.append(n)

    visit(out)
    out.adj = 1.0
    for n in reversed(order):
        for p, w in n.parents:
            p.adj += n.adj * w
    return float(root.adj)


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    s = _step(h)
    base = np.asarray([float(v) for v in x])
    n = len(base)
    H = np.zeros((n, n))
    f0 = f(list(base))
    for i in range(n):
        e = np.zeros(n)
        e[i] = s
        H[i, i] = (f(list(base + e)) - 2 * f0 + f(list(base - e))) / (s * s)
        for j in range(i + 1, n):
            ej = np.zeros(n)
            ej[j] = s
            m = (
                f(list(base + e + ej)) - f(list(base + e - ej)) - f(list(base - e + ej)) + f(list(base - e - ej))
            ) / (4 * s * s)
            H[i, j] = H[j, i] = m
    return [[float(H[i, j]) for j in range(n)] for i in range(n)]


def _flows(instance: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, float]:
    if instance["yield_bps"] <= -10_000:
        raise ValueError("yield must be above -1")
    face = float(instance["face_cents"])
    coupon = face * instance["coupon_bps"] / 10_000
    years = int(instance["maturity_years"])
    t = np.arange(1, years + 1, dtype=float)
    cash = np.full(years, coupon)
    cash[-1] += face
    return t, cash, instance["yield_bps"] / 10_000


def bond_price_cents(instance: dict[str, Any]) -> int:
    t, cash, y = _flows(instance)
    p = float(np.sum(cash * (1.0 + y) ** (-t)))
    return round(p)


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    t, cash, y = _flows(instance)
    v = 1.0 / (1.0 + y)
    p = float(np.sum(cash * v**t))
    first = float(-np.sum(t * cash * v ** (t + 1)))
    second = float(np.sum(t * (t + 1) * cash * v ** (t + 2)))
    return {
        "dprice_dy": first,
        "d2price_dy2": second,
        "duration_analytic": -first / p,
        "convexity_analytic": second / p,
    }
