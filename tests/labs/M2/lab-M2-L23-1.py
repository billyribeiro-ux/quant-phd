"""M2 lab L23: the Taylor expansion of a bond price in its yield. Duration and convexity are previewed, not defined.

SIMULATED: the bond is a generated specification, not a quoted security. Face value 100000 cents, an annual coupon of
5 percent of face (5000 cents a year), ten annual coupons, and the face repaid with the last coupon. Yield compounds
annually, so the price at yield y is P(y) = sum over t = 1..10 of c_t / (1 + y)**t, with c_t the cash flow in cents.
The price is exact rational arithmetic (Fraction) on the float yields, so no rounding enters the price before it is
reported. The two sensitivities P'(y0) and P''(y0) are floats: each is the exact rational value rounded once to the
nearest double, so its relative error is at most 2**-53. The Taylor polynomials are exact given these two float
sensitivities, which they use as exact rationals. Only the reported price and the reported expansion are
integer numbers of cents: each is the unrounded value rounded to the nearest cent with halves to even, which is
Fraction's round(). Floats also appear in the
central-difference checks and in the printed values.
Part A checks the closed-form first and second derivatives of P against central differences. Part B expands P about
the base yield 4 percent, and prints the errors of the first-order and the second-order expansions at steps of
0.01, 0.005 and 0.0025, with the ratio of successive errors. Part C prints the price in cents, exact and from the
second-order expansion. The two numbers printed as previews, -P'/P and P''/P, are only printed; this lab does not
define them.
Standard library only; no randomness and no network access.
"""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction

FACE_CENTS = 100_000
COUPON_CENTS = 5_000
YEARS = 10
BASE_YIELD = 0.04
STEPS: tuple[float, ...] = (0.01, 0.005, 0.0025)


def cash_flow_cents(t: int) -> int:
    """The cash flow in cents at year t = 1..YEARS: a coupon each year, and the face at maturity."""
    if not 1 <= t <= YEARS:
        raise ValueError(f"year must be from 1 to {YEARS}, got {t}")
    return COUPON_CENTS + (FACE_CENTS if t == YEARS else 0)


def growth_factor(y: float) -> Fraction:
    """The exact rational 1 + y for a float yield y > -1; the float is taken as the exact value it stores."""
    if y <= -1.0:
        raise ValueError(f"yield must exceed -1, got {y}")
    return 1 + Fraction(y)


def price(y: float) -> Fraction:
    """The unrounded price P(y) in cents for yield y > -1, with annual compounding, as an exact rational."""
    v = growth_factor(y)
    return sum((Fraction(cash_flow_cents(t)) / v**t for t in range(1, YEARS + 1)), Fraction(0))


def price_first_derivative(y: float) -> float:
    """P'(y) = minus the sum over t of t c_t (1 + y)**(-t - 1), in cents per unit of yield, rounded once to a float."""
    v = growth_factor(y)
    return float(-sum((Fraction(t * cash_flow_cents(t)) / v ** (t + 1) for t in range(1, YEARS + 1)), Fraction(0)))


def price_second_derivative(y: float) -> float:
    """P''(y) = the sum over t of t (t + 1) c_t (1 + y)**(-t - 2), in cents per unit of yield squared, as a float."""
    v = growth_factor(y)
    exact = sum((Fraction(t * (t + 1) * cash_flow_cents(t)) / v ** (t + 2) for t in range(1, YEARS + 1)), Fraction(0))
    return float(exact)


def price_cents(y: float) -> int:
    """The price as an integer number of cents: the unrounded price rounded half to even."""
    return round(price(y))


def taylor_first(y0: float, dy: float) -> Fraction:
    """First-order Taylor polynomial of P about y0, at y0 + dy: exact for the float shift dy and float sensitivity."""
    return price(y0) + Fraction(price_first_derivative(y0)) * Fraction(dy)


def taylor_second(y0: float, dy: float) -> Fraction:
    """Second-order Taylor polynomial of P about y0, at y0 + dy: exact for the float shift dy and sensitivities."""
    return taylor_first(y0, dy) + Fraction(1, 2) * Fraction(price_second_derivative(y0)) * Fraction(dy) ** 2


def central_difference(fun: Callable[[float], float], y: float, h: float) -> float:
    """The central difference (fun(y + h) - fun(y - h)) / (2 h) of a one-variable function; h must be positive."""
    if h <= 0.0:
        raise ValueError(f"the step must be positive, got {h}")
    return (fun(y + h) - fun(y - h)) / (2.0 * h)


def main() -> None:
    y0 = BASE_YIELD
    print("SIMULATED bond: face 100000 cents, 5000 cents a year for 10 years, face repaid at year 10")
    print(f"base yield {y0:.2%}; unrounded price {float(price(y0)):.6f} cents")
    print(f"integer price in cents: {price_cents(y0)}")

    p1 = price_first_derivative(y0)
    p2 = price_second_derivative(y0)
    fd1 = central_difference(lambda y: float(price(y)), y0, 1e-5)
    fd2 = central_difference(price_first_derivative, y0, 1e-4)
    print(f"P'(y0) closed form {p1:.6f}, central difference {fd1:.6f}, difference {abs(p1 - fd1):.1e}")
    print(f"P''(y0) closed form {p2:.6f}, central difference {fd2:.6f}, difference {abs(p2 - fd2):.1e}")

    p0 = float(price(y0))
    print(f"preview only, not defined here: -P'/P = {-p1 / p0:.6f}, P''/P = {p2 / p0:.6f}")

    previous_first = previous_second = Fraction(0)
    for k, dy in enumerate(STEPS):
        exact = price(y0 + dy)
        e1 = exact - taylor_first(y0, dy)
        e2 = exact - taylor_second(y0, dy)
        line = f"shift dy = {dy:<7g} first-order error {float(e1): .6e} second-order error {float(e2): .6e}"
        if k > 0:
            line += f" ratios {float(previous_first / e1):.4f} {float(previous_second / e2):.4f}"
        print(line)
        previous_first, previous_second = e1, e2

    for dy in (0.01, -0.01):
        exact_cents = price_cents(y0 + dy)
        approx_cents = round(taylor_second(y0, dy))
        print(
            f"yield shift {dy:+.2f}: exact price {exact_cents} cents, second-order expansion {approx_cents} cents, "
            f"difference {exact_cents - approx_cents} cents"
        )


main()
