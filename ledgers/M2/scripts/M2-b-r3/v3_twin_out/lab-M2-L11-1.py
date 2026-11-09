"""M2 L11 lab 1: integration by parts and substitution checked by midpoint quadrature.

Part A checks the integration-by-parts identity for u(x) = x^2 and v'(x) = (1 - x)^3 on [0, 1], with the
antiderivative v(x) = -(1 - x)^4 / 4, so that the identity reads int_0^1 x^2 (1 - x)^3 dx = [u v]_0^1 - int_0^1 2x
v(x) dx. Part B checks the substitution identity with g(t) = t^3 + t on [0, 1] and f(x) = x^2: the integral of f over
[g(0), g(1)] = [0, 2] equals the integral of f(g(t)) g'(t) over [0, 1]. Part C prints the integral of x^2 over [0, 1],
the left side of Theorem 3.1 with the limits [g(0), g(1)] = [0, 2] replaced by [a, b] = [0, 1]; that value is
different. Each integral is evaluated by the midpoint rule with N = 100000 subintervals, and each result is compared
with the exact value from the page: 1/60 for part A and 8/3 for part B. Standard library only; no randomness and no
network access.
"""

from __future__ import annotations

from collections.abc import Callable

N = 100_000
TOL = 1e-6


def midpoint(f: Callable[[float], float], a: float, b: float, n: int = N) -> float:
    """Midpoint-rule approximation of the integral of f over [a, b] with n equal subintervals."""
    h = (b - a) / n
    return h * sum(f(a + (i + 0.5) * h) for i in range(n))


def part_a() -> None:
    lhs = midpoint(lambda x: x * x * (1 - x) ** 3, 0.0, 1.0)

    def u(x: float) -> float:
        return x * x

    def v(x: float) -> float:
        return -((1 - x) ** 4) / 4

    # The boundary term [uv]_0^1 = u(1) v(1) - u(0) v(0), computed from u and v.
    boundary = u(1.0) * v(1.0) - u(0.0) * v(0.0)
    # -int u' v with u'(x) = 2x, computed from the integrand.
    rhs = boundary + midpoint(lambda x: -2.0 * x * v(x), 0.0, 1.0)
    exact = 1 / 60
    print(f"part A: midpoint int_0^1 x^2 (1 - x)^3 dx = {lhs:.10f}, exact 1/60 = {exact:.10f}")
    print(f"part A: right side [uv] - int u'v = {rhs:.10f}")
    print(f"part A: left side equals right side to {TOL:g}: {abs(lhs - rhs) < TOL}")
    print(f"part A: left side equals 1/60 to {TOL:g}: {abs(lhs - exact) < TOL}")


def part_b() -> None:
    lhs = midpoint(lambda x: x * x, 0.0, 2.0)
    rhs = midpoint(lambda t: (t**3 + t) ** 2 * (3 * t * t + 1), 0.0, 1.0)
    exact = 8 / 3
    print(f"part B: int_0^2 x^2 dx (midpoint) = {lhs:.10f}, exact 8/3 = {exact:.10f}")
    print(f"part B: int_0^1 f(g(t)) g'(t) dt (midpoint) = {rhs:.10f}")
    print(f"part B: the two sides agree to {TOL:g}: {abs(lhs - rhs) < TOL}")
    print(f"part B: both equal 8/3 to {TOL:g}: {abs(lhs - exact) < TOL and abs(rhs - exact) < TOL}")


def part_c() -> None:
    unchanged = midpoint(lambda x: x * x, 0.0, 1.0)
    print(f"part C: int_0^1 x^2 dx with the limits unchanged (midpoint) = {unchanged:.10f}")
    print(f"part C: that value is 1/3, not 8/3: {abs(unchanged - 1 / 3) < TOL}")


def main() -> None:
    part_a()
    part_b()
    part_c()


main()
