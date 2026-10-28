"""M6 L05 lab 1: the two iterated integrals of f(x, y) = (x^2 - y^2) / (x^2 + y^2)^2 on the unit square.

Inputs are a fixed formula, not data, and no random draws are used, so every run prints the same lines.
Part A: the iterated integrals in closed form, from the antiderivatives in y and in x.
Part B: the same two iterated integrals by quadrature (a midpoint rule on the outer variable, and a composite Simpson
rule on the inner variable after the substitution y = s^2 (first order) or x = s^2 (second order)), with the error
against the closed form.
Part C: the closed-form integral of f over a dyadic block Q_k that lies inside the set where f >= 0, and the partial
sums over six blocks. The closed form gives the same value for every block (the scaling in Proposition 3.2), so the
partial sums grow in proportion to the number of blocks. Block 0 alone is checked by quadrature.

The closed forms are exact up to floating-point rounding. The quadrature values are numerical approximations, and
their error is printed. The lab does not decide integrability by quadrature; Proposition 3.2 proves it.
"""

import math
from collections.abc import Callable


def f(x: float, y: float) -> float:
    """The integrand (x^2 - y^2) / (x^2 + y^2)^2, for (x, y) other than (0, 0)."""
    denom = x * x + y * y
    return (x * x - y * y) / (denom * denom)


def simpson(g: Callable[[float], float], a: float, b: float, n: int) -> float:
    """Composite Simpson rule on [a, b] with n subintervals; n must be even."""
    h = (b - a) / n
    total = g(a) + g(b)
    for i in range(1, n):
        total += (4.0 if i % 2 == 1 else 2.0) * g(a + i * h)
    return total * h / 3.0


def inner_over_y(x: float, m: int) -> float:
    """The integral over y in [0, 1] of f(x, y) for a fixed x > 0, by Simpson on y = s^2, s in [0, 1]."""
    return simpson(lambda s: f(x, s * s) * 2.0 * s, 0.0, 1.0, m)


def inner_over_x(y: float, m: int) -> float:
    """The integral over x in [0, 1] of f(x, y) for a fixed y > 0, by Simpson on x = s^2, s in [0, 1]."""
    return simpson(lambda s: f(s * s, y) * 2.0 * s, 0.0, 1.0, m)


def block_integral_closed(a: float) -> float:
    """The integral of f over (a, 2a] x [0, a] for a > 0, by the substitution x = a t (Proposition 3.2).

    The value arctan 2 - arctan 1 does not depend on a > 0. For a <= 0 no block is defined, and the value is 0.
    """
    return math.atan(2.0) - math.atan(1.0) if a > 0 else 0.0


def main() -> None:
    """Print Parts A, B and C. Every line is a fixed closed form or a deterministic quadrature."""
    quarter_pi = math.pi / 4.0
    print("Part A: the two iterated integrals in closed form")
    print(f"dy_first_closed {quarter_pi:.10f}")
    print(f"dx_first_closed {-quarter_pi:.10f}")

    print("Part B: the same two iterated integrals by quadrature")
    outer_n = 400
    h = 1.0 / outer_n
    dy_first = sum(inner_over_y((i + 0.5) * h, 4000) for i in range(outer_n)) * h
    print(f"dy_first_quadrature {dy_first:.10f} error {dy_first - quarter_pi:+.2e}")
    dx_first = sum(inner_over_x((j + 0.5) * h, 4000) for j in range(outer_n)) * h
    print(f"dx_first_quadrature {dx_first:.10f} error {dx_first + quarter_pi:+.2e}")

    print("Part C: integral of the positive part of f over dyadic blocks where f >= 0")
    c = block_integral_closed(0.5)
    block_check = simpson(lambda x: simpson(lambda y: f(x, y), 0.0, 0.5, 200), 0.5, 1.0, 200)
    print(f"block_integral_closed {c:.10f}")
    print(f"block_0_quadrature {block_check:.10f} error {block_check - c:+.2e}")
    total = 0.0
    for k in range(6):
        a = 0.5 ** (k + 1)
        total += block_integral_closed(a)
        print(f"blocks_0_to_{k} partial_sum {total:.10f} block_count {k + 1}")
    print(f"partial_sums_equal_count_times_block {abs(total - 6 * c) < 1e-12}")


main()
