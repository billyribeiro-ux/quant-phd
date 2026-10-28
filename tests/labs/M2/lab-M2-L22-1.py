"""M2 lab L22: the envelope theorem, checked on two maximization problems with closed-form answers.

SIMULATED: both objectives are test functions chosen for this lab. They are not market data.
Part A: maximize f(x, a) = a * ln(1 + x) - x over x in [0, 10], for a in {1.5, 2, 3, 4}. The maximizer is x* = a - 1
and the value function is V(a) = a ln a - (a - 1), so V'(a) = ln a. The lab finds x* by golden-section search, then
compares a central difference of V (step 1e-4) with ln a and with the partial derivative f_a(x*, a) = ln(1 + x*).
Part B: maximize x * y subject to x + y = a. The constraint is absorbed by substituting y = a - x, which leaves the
unconstrained problem F(x, a) = x * (a - x). The value is V(a) = a**2 / 4, so V'(a) = a / 2. The lab compares the
central difference of V with a / 2, and it prints the naive partial derivative of x * y with respect to a at fixed x
and y, which is 0, to show why the constraint cannot be ignored.
Standard library only; no randomness and no network access.
"""

from __future__ import annotations

import math
from collections.abc import Callable

PARAMETERS_A: tuple[float, ...] = (1.5, 2.0, 3.0, 4.0)
PARAMETERS_B: tuple[float, ...] = (1.0, 2.0, 3.0)
STEP = 1e-4
GOLDEN = (math.sqrt(5.0) - 1.0) / 2.0


def golden_max(fun: Callable[[float], float], lo: float, hi: float, tol: float = 1e-12) -> float:
    """The maximizer of a concave function fun on [lo, hi], by golden-section search to width tol.

    The interval must satisfy lo < hi and tol > 0; otherwise ValueError is raised.
    """
    if not lo < hi:
        raise ValueError(f"need lo < hi, got {lo} and {hi}")
    if tol <= 0.0:
        raise ValueError(f"the tolerance must be positive, got {tol}")
    a, b = lo, hi
    c = b - GOLDEN * (b - a)
    d = a + GOLDEN * (b - a)
    fc, fd = fun(c), fun(d)
    while b - a > tol:
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - GOLDEN * (b - a)
            fc = fun(c)
        else:
            a, c, fc = c, d, fd
            d = a + GOLDEN * (b - a)
            fd = fun(d)
    return (a + b) / 2.0


def objective_a(x: float, a: float) -> float:
    """f(x, a) = a * ln(1 + x) - x for x > -1."""
    return a * math.log(1.0 + x) - x


def maximizer_a(a: float) -> float:
    """The maximizer x* of f(x, a) over [0, 10], by golden-section search."""
    return golden_max(lambda x: objective_a(x, a), 0.0, 10.0)


def maximizer_b(a: float) -> float:
    """The maximizer x* of x * (a - x) over [0, a], by golden-section search."""
    return golden_max(lambda x: x * (a - x), 0.0, a)


def value_a(a: float) -> float:
    """V(a) = max over x in [0, 10] of f(x, a), computed numerically."""
    x_star = maximizer_a(a)
    return objective_a(x_star, a)


def value_b(a: float) -> float:
    """V(a) = max over x of x * (a - x), computed numerically on [0, a]; the constraint y = a - x is substituted."""
    x_star = maximizer_b(a)
    return x_star * (a - x_star)


def central_difference(v: Callable[[float], float], a: float, h: float) -> float:
    """The central difference (v(a + h) - v(a - h)) / (2 h). The step h must be positive."""
    if h <= 0.0:
        raise ValueError(f"the step must be positive, got {h}")
    return (v(a + h) - v(a - h)) / (2.0 * h)


def main() -> None:
    print("Part A: maximize a*ln(1 + x) - x over x in [0, 10]; V'(a) should equal ln(a)")
    for a in PARAMETERS_A:
        x_star = maximizer_a(a)
        fd = central_difference(value_a, a, STEP)
        partial = math.log(1.0 + x_star)
        error = max(abs(fd - math.log(a)), abs(partial - math.log(a)))
        print(
            f"a = {a:<4} x* = {x_star:.8f} (a - 1 = {a - 1.0:.1f}) V' central difference {fd:.8f} "
            f"ln(a) {math.log(a):.8f} f_a(x*, a) {partial:.8f} max error {error:.1e}"
        )
    print("Part B: maximize x*y subject to x + y = a; V'(a) should equal a/2")
    for a in PARAMETERS_B:
        x_star = maximizer_b(a)
        fd = central_difference(value_b, a, STEP)
        reduced_partial = x_star
        naive_partial = 0.0  # x * y has no a in it, so at fixed x and y its partial in a is zero
        print(
            f"a = {a:<4} x* = {x_star:.8f} V' central difference {fd:.8f} a/2 {a / 2.0:.8f} "
            f"reduced F_a(x*, a) {reduced_partial:.8f} naive partial of x*y in a {naive_partial:.8f} "
            f"error {abs(fd - a / 2.0):.1e}"
        )


main()
