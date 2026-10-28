"""M2 lab L23: the Taylor expansion of a bond price in its yield. Duration and convexity are previewed, not defined.

SIMULATED: the bond is a generated specification, not a quoted security. Face value 100000 cents, an annual coupon of
5 percent of face (5000 cents a year), ten annual coupons, and the face repaid with the last coupon. Yield compounds
annually, so the price at yield y is P(y) = sum over t = 1..10 of c_t / (1 + y)**t, with c_t the cash flow in cents.
The prices and their Taylor expansions are float calculations. Only the reported price is an integer number of cents:
it is the unrounded price rounded to the nearest cent with halves to even, which is Python's round() on a float.
Part A checks the closed-form first and second derivatives of P against central differences. Part B expands P about
the base yield 4 percent, and prints the errors of the first-order and the second-order expansions at steps of
0.01, 0.005 and 0.0025, with the ratio of successive errors. Part C prints the price in cents, exact and from the
second-order expansion. The two numbers printed as previews, -P'/P and P''/P, are only printed; this lab does not
define them.
Standard library only; no randomness and no network access.
"""

from __future__ import annotations

from collections.abc import Callable

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


def price(y: float) -> float:
    """The unrounded price P(y) in cents for yield y > -1, with annual compounding."""
    if y <= -1.0:
        raise ValueError(f"yield must exceed -1, got {y}")
    return sum(cash_flow_cents(t) / (1.0 + y) ** t for t in range(1, YEARS + 1))


def price_first_derivative(y: float) -> float:
    """P'(y) = minus the sum over t of t c_t (1 + y)**(-t - 1), in cents per unit of yield."""
    return -sum(t * cash_flow_cents(t) / (1.0 + y) ** (t + 1) for t in range(1, YEARS + 1))


def price_second_derivative(y: float) -> float:
    """P''(y) = the sum over t of t (t + 1) c_t (1 + y)**(-t - 2), in cents per unit of yield squared."""
    return sum(t * (t + 1) * cash_flow_cents(t) / (1.0 + y) ** (t + 2) for t in range(1, YEARS + 1))


def price_cents(y: float) -> int:
    """The price as an integer number of cents: the unrounded price rounded half to even."""
    return round(price(y))


def taylor_first(y0: float, dy: float) -> float:
    """First-order Taylor polynomial of P about y0, evaluated at y0 + dy."""
    return price(y0) + price_first_derivative(y0) * dy


def taylor_second(y0: float, dy: float) -> float:
    """Second-order Taylor polynomial of P about y0, evaluated at y0 + dy."""
    return taylor_first(y0, dy) + 0.5 * price_second_derivative(y0) * dy * dy


def central_difference(fun: Callable[[float], float], y: float, h: float) -> float:
    """The central difference (fun(y + h) - fun(y - h)) / (2 h) of a one-variable function; h must be positive."""
    if h <= 0.0:
        raise ValueError(f"the step must be positive, got {h}")
    return (fun(y + h) - fun(y - h)) / (2.0 * h)


def main() -> None:
    y0 = BASE_YIELD
    print("SIMULATED bond: face 100000 cents, 5000 cents a year for 10 years, face repaid at year 10")
    print(f"base yield {y0:.2%}; unrounded price {price(y0):.6f} cents")
    print(f"integer price in cents: {price_cents(y0)}")

    p1 = price_first_derivative(y0)
    p2 = price_second_derivative(y0)
    fd1 = central_difference(price, y0, 1e-5)
    fd2 = central_difference(price_first_derivative, y0, 1e-4)
    print(f"P'(y0) closed form {p1:.6f}, central difference {fd1:.6f}, difference {abs(p1 - fd1):.1e}")
    print(f"P''(y0) closed form {p2:.6f}, central difference {fd2:.6f}, difference {abs(p2 - fd2):.1e}")

    print(f"preview only, not defined here: -P'/P = {-p1 / price(y0):.6f}, P''/P = {p2 / price(y0):.6f}")

    previous_first = previous_second = 0.0
    for k, dy in enumerate(STEPS):
        exact = price(y0 + dy)
        e1 = exact - taylor_first(y0, dy)
        e2 = exact - taylor_second(y0, dy)
        line = f"shift dy = {dy:<7g} first-order error {e1: .6e} second-order error {e2: .6e}"
        if k > 0:
            line += f" ratios {previous_first / e1:.4f} {previous_second / e2:.4f}"
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
