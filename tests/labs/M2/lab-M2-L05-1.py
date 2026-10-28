"""M2 lab L05: the product, quotient and chain rules at x = 1.5, against central differences.

Standard library only. No randomness and no network. The three functions are p(x) = (x^2 + 1)(x^3), the quotient
q(x) = (x^2 + 1)/(x + 2) and the composite c(x) = (x^2 + 1)^3. For each one, the script prints the derivative from the
rule of this lesson (the analytic value) and the central difference (f(x + h) - f(x - h))/(2h) with h = 10^-4, with
the absolute difference between them. The central difference has error of order h^2, and at this step
each printed absolute difference is below 1e-6 (the table gives the three values). The agreement is a numerical
check at one point and step, not a proof of the rules; the proofs are on the page.
"""

from __future__ import annotations

from collections.abc import Callable

H = 1e-4
X = 1.5


def p(x: float) -> float:
    """The product (x^2 + 1) * x^3."""
    return (x * x + 1.0) * x**3


def p_prime(x: float) -> float:
    """The product rule u'v + uv' with u = x^2 + 1 and v = x^3, giving 2x * x^3 + (x^2 + 1) * 3x^2."""
    return 2.0 * x * x**3 + (x * x + 1.0) * 3.0 * x * x


def q(x: float) -> float:
    """The quotient (x^2 + 1)/(x + 2), defined for x != -2."""
    return (x * x + 1.0) / (x + 2.0)


def q_prime(x: float) -> float:
    """The quotient rule: (u'v - uv')/v^2 with u = x^2 + 1 and v = x + 2, simplified to (x^2 + 4x - 1)/(x + 2)^2."""
    return (x * x + 4.0 * x - 1.0) / (x + 2.0) ** 2


def c(x: float) -> float:
    """The composite (x^2 + 1)^3, the outer function u^3 at the inner function u = x^2 + 1."""
    return (x * x + 1.0) ** 3


def c_prime(x: float) -> float:
    """The chain rule: (outer') at the inner value times the inner derivative, 3(x^2 + 1)^2 * 2x."""
    return 3.0 * (x * x + 1.0) ** 2 * 2.0 * x


def central(f: Callable[[float], float], x: float, h: float) -> float:
    """The central difference (f(x + h) - f(x - h)) / (2h)."""
    return (f(x + h) - f(x - h)) / (2.0 * h)


def main() -> None:
    print("function, analytic derivative, central difference, absolute difference")
    cases = (
        ("product p", p, p_prime),
        ("quotient q", q, q_prime),
        ("composite c", c, c_prime),
    )
    for name, f, df in cases:
        analytic = df(X)
        numeric = central(f, X, H)
        print(f"{name}, {analytic:.9f}, {numeric:.9f}, {abs(analytic - numeric):.3e}")


main()
