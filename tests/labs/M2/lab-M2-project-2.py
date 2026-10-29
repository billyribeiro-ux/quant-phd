"""Rung 2 completed solution: a central second difference, and forward-mode AD on a dual number.

The completion problem shows the two blanked lines as ___. Both are checked here on a cubic with coefficients
(1, -2, 3, 0.5), a test function and not a bond: the second difference at x0 = 0.8 against its analytic value 8.4, and
the forward-mode derivative at x0 against its analytic value 3.76. Each line is printed with its analytic value and the
difference. Standard library only.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class Dual:
    """A dual number value + dot * eps, with eps squared equal to zero: the carrier of forward-mode AD."""

    def __init__(self, value: float, dot: float) -> None:
        self.value = value
        self.dot = dot

    def __add__(self, other: Any) -> Dual:
        o = lift(other)
        return Dual(self.value + o.value, self.dot + o.dot)

    __radd__ = __add__

    def __mul__(self, other: Any) -> Dual:
        o = lift(other)
        return Dual(self.value * o.value, self.value * o.dot + self.dot * o.value)

    __rmul__ = __mul__


def lift(x: Any) -> Dual:
    """A dual number unchanged, or a real number as a dual number with zero derivative."""
    return x if isinstance(x, Dual) else Dual(float(x), 0.0)


def second_difference(f: Callable[[float], float], x: float, h: float) -> float:
    """The central second difference (f(x+h) - 2f(x) + f(x-h)) / h**2 of f at x with step h."""
    return (f(x + h) - 2 * f(x) + f(x - h)) / h**2


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    """The derivative of f at x: f is evaluated on a dual number whose dot part is 1."""
    return float(lift(f(Dual(x, 1.0))).dot)


def cubic(x: Any) -> Any:
    """The test cubic 1 - 2x + 3x^2 + 0.5x^3 in Horner form, so that a dual number argument works."""
    return 1.0 + x * (-2.0 + x * (3.0 + x * 0.5))


def main() -> None:
    x0 = 0.8
    h = 1e-4
    second_numeric = second_difference(cubic, x0, h)
    second_analytic = 2 * 3.0 + 6 * 0.5 * x0
    print("second difference:", f"{second_numeric:.6f}", "| analytic:", f"{second_analytic:.6f}")
    print("difference:", f"{abs(second_numeric - second_analytic):.2e}")
    derivative = ad_derivative(cubic, x0)
    first_analytic = -2.0 + 2 * 3.0 * x0 + 3 * 0.5 * x0 * x0
    print("AD derivative:", f"{derivative:.6f}", "| analytic:", f"{first_analytic:.6f}")
    print("difference:", f"{abs(derivative - first_analytic):.2e}")


main()
