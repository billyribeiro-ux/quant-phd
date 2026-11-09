"""M2 L07 lab 1: Taylor polynomials of f(x) = 1/(1 - x) at 0, by degree, in exact rational arithmetic.

Part A checks the closed form f^(k)(x) = k! / (1 - x)^(k+1) against the recursion f^(j+1) = (j+1) f^(j) / (1 - x)
that the quotient rule gives, at three rational points and for k = 0 to 8. Part B takes x = 3/10 and degrees
n = 0 to 10, and checks that the error f(x) - P_n(x) equals x^(n+1) / (1 - x) exactly, where P_n(x) is the Taylor
polynomial of degree n at 0 (the sum of x^k for k = 0 to n, because f^(k)(0) = k!). Part C takes x = 2, outside
the interval |x| < 1, and prints the errors for the same identity. Part D takes g(x) = x |x|. Its first derivative
at 0 is computed from the definition; for x != 0 the page derives g'(x) = 2|x|, and the second derivative at 0 is
tested through
that formula.

Exact arithmetic uses fractions.Fraction throughout. Standard library only; no randomness and no network access.
"""

from __future__ import annotations

from fractions import Fraction
from math import factorial

X_B = Fraction(3, 10)
N_MAX = 10
POINTS_A = (Fraction(3, 10), Fraction(-1, 2), Fraction(9, 10))
K_MAX_A = 8


def f(x: Fraction) -> Fraction:
    """f(x) = 1 / (1 - x) for x different from 1."""
    if x == 1:
        raise ValueError("f(x) = 1/(1 - x) is not defined at x = 1")
    return 1 / (1 - x)


def derivative_formula(k: int, x: Fraction) -> Fraction:
    """The k-th derivative of 1/(1 - x), namely k! / (1 - x)^(k+1), for x different from 1."""
    return Fraction(factorial(k)) / (1 - x) ** (k + 1)


def derivative_by_recursion(k: int, x: Fraction) -> Fraction:
    """The k-th derivative by the recursion f^(j+1) = (j+1) f^(j) / (1 - x), starting from f itself."""
    value = f(x)
    for j in range(k):
        value = (j + 1) * value / (1 - x)
    return value


def taylor_poly(x: Fraction, n: int) -> Fraction:
    """Taylor polynomial of degree n at 0: sum over k = 0..n of f^(k)(0) x^k / k!, with f^(k)(0) from the formula."""
    total = Fraction(0)
    for k in range(n + 1):
        total += derivative_formula(k, Fraction(0)) * x**k / factorial(k)
    return total


def part_a() -> None:
    checks = 0
    for x in POINTS_A:
        for k in range(K_MAX_A + 1):
            if derivative_formula(k, x) != derivative_by_recursion(k, x):
                raise AssertionError(f"derivative formula fails at x = {x}, k = {k}")
            checks += 1
    print(f"part A: formula equals recursion at all {checks} checks (x in 3/10, -1/2, 9/10; k = 0 to {K_MAX_A})")


def part_b() -> None:
    fx = f(X_B)
    print(f"part B: x = 3/10, f(x) = {fx} = {float(fx):.10f}")
    previous_error = None
    for n in range(N_MAX + 1):
        t = taylor_poly(X_B, n)
        error = fx - t
        if error != X_B ** (n + 1) / (1 - X_B):
            raise AssertionError(f"remainder identity fails at n = {n}")
        if previous_error is not None and error / previous_error != X_B:
            raise AssertionError(f"error ratio is not x at n = {n}")
        previous_error = error
        print(f"part B: n = {n:2d}  P_n(x) = {float(t):.10f}  error = {float(error):.10f}")
    print("part B: error equals x^(n+1)/(1-x) exactly at every degree, and each error is x times the one before")


def part_c() -> None:
    x = Fraction(2)
    fx = f(x)
    print(f"part C: x = 2, f(x) = {fx}; the partial sums P_n(2) are 2^(n+1) - 1, printed below")
    for n in range(N_MAX + 1):
        t = taylor_poly(x, n)
        error = fx - t
        if error != x ** (n + 1) / (1 - x):
            raise AssertionError(f"remainder identity fails at x = 2, n = {n}")
        print(f"part C: n = {n:2d}  P_n(2) = {int(t):6d}  error = {int(error):6d}")
    print("part C: the error at n = 10 grows in absolute value, so the degree does not help at x = 2")


def g(x: Fraction) -> Fraction:
    """g(x) = x * |x|."""
    return x * abs(x)


def g_prime_for_x_nonzero(x: Fraction) -> Fraction:
    """The derivative of g at x != 0, derived on the page: 2|x|."""
    return 2 * abs(x)


def part_d() -> None:
    print("part D: first derivative of g at 0 from the definition: (g(h) - g(0)) / h")
    for k in range(1, 7):
        h = Fraction(1, 10**k)
        quotient = (g(h) - g(Fraction(0))) / h
        if quotient != abs(h):
            raise AssertionError(f"quotient is not |h| at h = {h}")
        print(f"part D: h = 1e-{k}, quotient = {float(quotient):.1e}")
    print("part D: at the six steps printed the quotient equals |h|; Example 4.1 gives the limit 0, so g'(0) = 0")
    print("part D: second derivative at 0 from g'(x) = 2|x|: (g'(h) - g'(0)) / h")
    for k in range(1, 7):
        h = Fraction(1, 10**k)
        right = (g_prime_for_x_nonzero(h) - g_prime_for_x_nonzero(Fraction(0))) / h
        left = (g_prime_for_x_nonzero(-h) - g_prime_for_x_nonzero(Fraction(0))) / (-h)
        if right != 2 or left != -2:
            raise AssertionError(f"second-derivative quotients are not +2 and -2 at h = {h}")
        print(f"part D: h = 1e-{k}, right quotient = {int(right):2d}, left quotient = {int(left):2d}")
    print("part D: at the six steps printed, the right quotient is +2 and the left quotient is -2 (Proposition 4.2)")


def main() -> None:
    part_a()
    part_b()
    part_c()
    part_d()


main()
