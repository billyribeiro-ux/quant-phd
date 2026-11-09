"""M2 lab L14: forward-mode automatic differentiation with dual numbers, checked against analytic derivatives.

Standard library only. A dual number a + b*eps (with eps*eps = 0) carries a value and a tangent.
Each primitive operation updates both, so evaluating a function on a dual number a + 1*eps returns
f(a) in the value part and f'(a) in the tangent part. No step size h appears anywhere. The test
functions are evaluated on a grid of 251 points from 0.5 to 3.0 and compared with closed-form
derivatives. Nothing is random and nothing is fetched, so repeated runs print the same output.
"""

from __future__ import annotations

import math
from collections.abc import Callable

Number = int | float


class Dual:
    """A dual number val + dot*eps with eps*eps = 0. val is the value; dot is the tangent (the derivative)."""

    __slots__ = ("dot", "val")

    def __init__(self, val: float, dot: float = 0.0) -> None:
        self.val = float(val)
        self.dot = float(dot)

    def __add__(self, other: Number | Dual) -> Dual:
        o = lift(other)
        return Dual(self.val + o.val, self.dot + o.dot)

    __radd__ = __add__

    def __neg__(self) -> Dual:
        return Dual(-self.val, -self.dot)

    def __sub__(self, other: Number | Dual) -> Dual:
        return self + (-lift(other))

    def __rsub__(self, other: Number | Dual) -> Dual:
        return lift(other) + (-self)

    def __mul__(self, other: Number | Dual) -> Dual:
        o = lift(other)
        return Dual(self.val * o.val, self.val * o.dot + self.dot * o.val)

    __rmul__ = __mul__

    def __truediv__(self, other: Number | Dual) -> Dual:
        o = lift(other)
        if o.val == 0.0:
            raise ZeroDivisionError("dual division by a zero value")
        return Dual(self.val / o.val, (self.dot * o.val - self.val * o.dot) / (o.val * o.val))

    def __rtruediv__(self, other: Number | Dual) -> Dual:
        return lift(other) / self

    def __pow__(self, n: int) -> Dual:
        """Integer power n >= 0 by repeated multiplication. Other exponents are not needed here."""
        if not isinstance(n, int) or n < 0:
            raise ValueError(f"Dual power needs an integer n >= 0, got {n!r}")
        result = Dual(1.0)
        for _ in range(n):
            result = result * self
        return result


def lift(x: Number | Dual) -> Dual:
    """A plain number becomes a dual number with zero tangent. A dual number is returned unchanged."""
    return x if isinstance(x, Dual) else Dual(float(x), 0.0)


def dexp(x: Dual) -> Dual:
    """exp with its chain-rule tangent: d/dt exp(v) = exp(v) * dv."""
    e = math.exp(x.val)
    return Dual(e, e * x.dot)


def dsin(x: Dual) -> Dual:
    """sin with its chain-rule tangent: d/dt sin(v) = cos(v) * dv."""
    return Dual(math.sin(x.val), math.cos(x.val) * x.dot)


def f1(x: Dual) -> Dual:
    """f1(x) = x exp(x) + sin(x) / x, defined for x != 0."""
    return x * dexp(x) + dsin(x) / x


def f1_exact(x: float) -> float:
    """The closed-form derivative of f1: exp(x) + x exp(x) + (x cos x - sin x) / x^2."""
    return math.exp(x) + x * math.exp(x) + (x * math.cos(x) - math.sin(x)) / (x * x)


def f2(x: Dual) -> Dual:
    """f2(x) = exp(sin(x^2)), a composition of three primitives."""
    return dexp(dsin(x**2))


def f2_exact(x: float) -> float:
    """The closed-form derivative of f2: exp(sin(x^2)) cos(x^2) 2x."""
    return math.exp(math.sin(x * x)) * math.cos(x * x) * 2.0 * x


def grid() -> list[float]:
    """The 251 points 0.5 + i/100 for integer i from 0 to 250, so the last point is 3.0."""
    return [0.5 + i / 100 for i in range(251)]


def max_error(ad: Callable[[Dual], Dual], exact: Callable[[float], float]) -> float:
    """The largest absolute difference between the dual-number tangent and the closed form on the grid."""
    worst = 0.0
    for x in grid():
        worst = max(worst, abs(ad(Dual(x, 1.0)).dot - exact(x)))
    return worst


def main() -> None:
    print(f"grid points: {len(grid())}")
    e1 = max_error(f1, f1_exact)
    e2 = max_error(f2, f2_exact)
    print(f"max error, f1: below 1e-12: {e1 < 1e-12}")
    print(f"max error, f2: below 1e-12: {e2 < 1e-12}")
    x = 2.0
    print(f"f1 at x = 2: value {f1(Dual(x)).val:.10f}")
    print(f"f1'(2) by dual numbers: {f1(Dual(x, 1.0)).dot:.10f}")
    print(f"f1'(2) closed form: {f1_exact(x):.10f}")
    print(f"f2'(1) by dual numbers: {f2(Dual(1.0, 1.0)).dot:.10f}")
    print(f"f2'(1) closed form: {f2_exact(1.0):.10f}")


main()
