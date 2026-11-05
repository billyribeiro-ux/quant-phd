"""Acceptance suite for the M2 project: the sensitivity engine (sensitivity_engine.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your sensitivity_engine.py next to this file. Warnings are failures, as in the browser.

Each test checks a property or a number against the definitions of the M2 lessons and the project specification. A
failing test names the property it checks and the idea to revisit. It never prints the expected value: helper
functions hide their frames, and every message names a property, not a number.

The three ValueError conditions the specification names each have their own tests, in both directions: a step of
zero or less, an unknown scheme, and a yield at or below -1. Every other input is outside the specification and no test
requires an exception for it.
"""

from __future__ import annotations

import contextlib
import io
import math
import os
import warnings
from collections.abc import Callable, Iterator
from fractions import Fraction
from functools import partial
from typing import Any

import pytest
import sensitivity_engine as sol
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
INST2: dict[str, Any] = make_instance(SEED + 7_919)  # a second instance: a fixed answer for one seed must also match
INSTANCES = (INST, INST2)

ANALYTIC_KEYS = ("dprice_dy", "d2price_dy2", "duration_analytic", "convexity_analytic")


def require(condition: bool, message: str) -> None:
    """Fail with the named property unless the condition holds."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(message)


@pytest.fixture(autouse=True)
def _test_run_prints_nothing() -> Iterator[None]:
    """Every test runs with stdout and stderr captured; a test during which the module printed fails at teardown."""
    __tracebackhide__ = True
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
        yield
    require(buffer.getvalue() == "", "the module must not print, on any branch of any function")


def close(a: float, b: float, rel: float, absolute: float = 0.0) -> bool:
    """True when a and b agree to rel relative to the larger of 1 and |b|, plus an absolute allowance."""
    return math.isfinite(a) and abs(a - b) <= rel * max(1.0, abs(b)) + absolute


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError. Used only for the three conditions the specification names."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError, and none was raised.")


def must_accept(call: Callable[[], object], condition: str) -> object:
    """Fail if call() raises; return its value when it does not."""
    __tracebackhide__ = True
    try:
        return call()
    except Exception:
        pytest.fail(f"{condition}: the specification accepts this input, and the call raised instead.")
        raise


# ---- the test functions, written so that floats and dual numbers both pass through them ----


def cubic(coeffs: list[float], x: Any) -> Any:
    """p0 + p1 x + p2 x^2 + p3 x^3 in Horner form, so that a dual number argument uses only + and * ."""
    p0, p1, p2, p3 = coeffs
    return p0 + x * (p1 + x * (p2 + x * p3))


def cubic_prime(coeffs: list[float], x: float) -> float:
    """The analytic first derivative of the cubic."""
    _, p1, p2, p3 = coeffs
    return p1 + x * (2 * p2 + 3 * p3 * x)


def cubic_second(coeffs: list[float], x: float) -> float:
    """The analytic second derivative of the cubic."""
    _, _, p2, p3 = coeffs
    return 2 * p2 + 6 * p3 * x


def surface(c: list[float], point: list[float]) -> float:
    """g(u, v) = c0 + c1 u + c2 v + c3 u^2 + c4 u v + c5 v^2 + c6 u^2 v."""
    u, v = point
    return c[0] + c[1] * u + c[2] * v + c[3] * u * u + c[4] * u * v + c[5] * v * v + c[6] * u * u * v


def surface_hessian(c: list[float], point: list[float]) -> list[list[float]]:
    """The analytic Hessian of the surface at the point."""
    u, v = point
    return [[2 * c[3] + 2 * c[6] * v, c[4] + 2 * c[6] * u], [c[4] + 2 * c[6] * u, 2 * c[5]]]


def bond(face: int, coupon_bps: int, years: int, yield_bps: int) -> dict[str, Any]:
    """A SIMULATED bond dictionary with the keys the specification names."""
    return {
        "seed": -1,
        "label": "SIMULATED",
        "face_cents": face,
        "coupon_bps": coupon_bps,
        "maturity_years": years,
        "yield_bps": yield_bps,
    }


def unrounded_price(inst: dict[str, Any], y: float) -> float:
    """The unrounded price in cents at the yield y, by the annual cash-flow sum, in floats."""
    face = inst["face_cents"]
    coupon = face * inst["coupon_bps"] / 10_000
    years = inst["maturity_years"]
    v = 1.0 / (1.0 + y)
    return float(sum((coupon + (face if t == years else 0)) * v**t for t in range(1, years + 1)))


def exact_price(inst: dict[str, Any]) -> Fraction:
    """The exact unrounded price in cents at the instance's yield, in rational arithmetic."""
    face = inst["face_cents"]
    coupon = Fraction(face * inst["coupon_bps"], 10_000)
    years = inst["maturity_years"]
    v = 1 / (1 + Fraction(inst["yield_bps"], 10_000))
    return sum(((coupon + (face if t == years else 0)) * v**t for t in range(1, years + 1)), Fraction(0))


def exact_sensitivities(inst: dict[str, Any]) -> tuple[Fraction, Fraction]:
    """dprice_dy and d2price_dy2 from the stated cash-flow formulas, in exact rational arithmetic."""
    face = inst["face_cents"]
    coupon = Fraction(face * inst["coupon_bps"], 10_000)
    years = inst["maturity_years"]
    v = 1 / (1 + Fraction(inst["yield_bps"], 10_000))
    flows = [(t, coupon + (face if t == years else 0)) for t in range(1, years + 1)]
    first = -sum((t * cash * v ** (t + 1) for t, cash in flows), Fraction(0))
    second = sum((t * (t + 1) * cash * v ** (t + 2) for t, cash in flows), Fraction(0))
    return first, second


def yield_of(inst: dict[str, Any]) -> float:
    return float(inst["yield_bps"]) / 10_000


# ---- finite differences: fd_derivative ----


@pytest.mark.parametrize("inst", INSTANCES)
def test_central_difference_matches_the_analytic_derivative(inst: dict[str, Any]) -> None:
    coeffs, x0 = inst["cubic"], inst["x0"]
    value = sol.fd_derivative(lambda x: cubic(coeffs, x), x0, 1e-5, "central")
    require(
        close(value, cubic_prime(coeffs, x0), 1e-6),
        "the central difference must approximate f'(x) to 1e-6 (hint: Lesson 13, the central difference and its error)",
    )


def forward_error_ratio(inst: dict[str, Any]) -> float:
    """The ratio of the forward-estimate errors at steps 1e-2 and 5e-3 for the instance's cubic."""
    coeffs, x0 = inst["cubic"], inst["x0"]
    exact = cubic_prime(coeffs, x0)

    def error(h: float) -> float:
        return float(abs(sol.fd_derivative(lambda x: float(cubic(coeffs, x)), x0, h, "forward") - exact))

    return error(1e-2) / error(5e-3)


@pytest.mark.parametrize("inst", INSTANCES)
def test_forward_error_is_not_of_order_h_squared(inst: dict[str, Any]) -> None:
    # The upper bound: a forward estimate that is central in disguise has a ratio near 4.
    require(
        forward_error_ratio(inst) <= 2.1,
        "the forward difference's error must not fall faster than its step: order "
        "h, not h squared (hint: Lesson 13, the forward error is of order h)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_forward_error_is_at_least_of_order_h(inst: dict[str, Any]) -> None:
    # The lower bound: an error that falls more slowly than h has a ratio below 2.
    require(
        forward_error_ratio(inst) >= 1.9,
        "the forward difference's error must halve with its step: order "
        "h (hint: Lesson 13, the forward error is of order h)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_forward_estimate_is_the_forward_quotient(inst: dict[str, Any]) -> None:
    # For a cubic the forward quotient is exact: (f(x+h) - f(x)) / h = f'(x) + h f''(x) / 2 + h^2 p3, p3 the x^3 term.
    coeffs, x0 = inst["cubic"], inst["x0"]
    h = 1e-3
    expected = cubic_prime(coeffs, x0) + h * cubic_second(coeffs, x0) / 2 + h * h * coeffs[3]
    value = sol.fd_derivative(lambda x: float(cubic(coeffs, x)), x0, h, "forward")
    require(
        close(value, expected, 1e-6),
        "the forward estimate must be the forward quotient (f(x+h) - f(x)) / h "
        "(hint: Lesson 13, the forward quotient and its first correction term)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_central_error_is_at_least_of_order_h_squared(inst: dict[str, Any]) -> None:
    # sin is not a polynomial, so its central error is h squared f'''/6 and not zero: the ratio is about 4 for the plain
    # quotient. A Richardson extrapolation of the central quotient is more accurate still, and its ratio is larger.
    x0 = inst["x0"]
    exact = math.cos(x0)

    def error(h: float) -> float:
        return float(abs(sol.fd_derivative(math.sin, x0, h, "central") - exact))

    ratio = error(1e-2) / error(5e-3)
    require(
        ratio >= 3.8,
        "the central error must fall by the factor that order h squared gives when its step halves: order "
        "at least h squared (hint: Lesson 13, the central error is of order h squared)",
    )


def test_zero_step_raises_value_error() -> None:
    coeffs, x0 = INST["cubic"], INST["x0"]
    for scheme in ("forward", "central"):
        must_raise(
            partial(sol.fd_derivative, lambda x: float(cubic(coeffs, x)), x0, 0.0, scheme),
            "a step of zero must be refused with ValueError "
            "(hint: Lesson 13, a finite difference needs a positive step)",
        )


def test_negative_step_raises_value_error() -> None:
    coeffs, x0 = INST["cubic"], INST["x0"]
    for scheme in ("forward", "central"):
        must_raise(
            partial(sol.fd_derivative, lambda x: float(cubic(coeffs, x)), x0, -1e-3, scheme),
            "a negative step must be refused with ValueError "
            "(hint: Lesson 13, a finite difference needs a positive step)",
        )


def test_negative_zero_step_raises_value_error() -> None:
    # -0.0 equals zero, so it is not above zero and is refused like 0.0.
    coeffs, x0 = INST["cubic"], INST["x0"]
    for scheme in ("forward", "central"):
        must_raise(
            partial(sol.fd_derivative, lambda x: float(cubic(coeffs, x)), x0, -0.0, scheme),
            "a step of negative zero is not above zero and must be refused with ValueError",
        )


def test_tiny_negative_step_raises_value_error() -> None:
    # The refusal covers every step below zero, however small in size: -1e-300 is refused as -1e-3 is.
    coeffs, x0 = INST["cubic"], INST["x0"]
    for scheme in ("forward", "central"):
        must_raise(
            partial(sol.fd_derivative, lambda x: float(cubic(coeffs, x)), x0, -1e-300, scheme),
            "a tiny negative step must be refused with ValueError, as any negative step is "
            "(hint: Lesson 13, a finite difference needs a positive step)",
        )


def test_nan_step_raises_value_error() -> None:
    # NaN is not above zero, so the specification refuses it with ValueError.
    coeffs, x0 = INST["cubic"], INST["x0"]
    for scheme in ("forward", "central"):
        must_raise(
            partial(sol.fd_derivative, lambda x: float(cubic(coeffs, x)), x0, float("nan"), scheme),
            "a NaN step is not above zero and must be refused with ValueError "
            "(hint: Lesson 13, a finite difference needs a positive step)",
        )


def test_negative_infinite_step_raises_value_error() -> None:
    # Negative infinity is below zero, so it is a negative step, however large its size: it is refused as -1e-3 is.
    coeffs, x0 = INST["cubic"], INST["x0"]
    for scheme in ("forward", "central"):
        must_raise(
            partial(sol.fd_derivative, lambda x: float(cubic(coeffs, x)), x0, -math.inf, scheme),
            "a step of negative infinity must be refused with ValueError, as any negative step is "
            "(hint: Lesson 13, a finite difference needs a positive step)",
        )


def test_large_positive_step_is_accepted() -> None:
    # Only a step that is not above zero is refused. A large step above zero is accepted: the suite draws 1, 5 and 1e6.
    # The forward estimate is fixed by the page, so at each large step its value must be the forward quotient at that
    # step, not the quotient at some other step. The central estimate is only required to be a finite float here.
    coeffs, x0 = INST["cubic"], INST["x0"]

    def f(x: float) -> float:
        return float(cubic(coeffs, x))

    for h in (1.0, 5.0, 1e6):
        for scheme in ("forward", "central"):
            value = must_accept(
                partial(sol.fd_derivative, f, x0, h, scheme),
                f"a step of {h} is above zero, so the specification accepts it",
            )
            require(isinstance(value, float) and math.isfinite(value), "a positive step must return a finite float")
        forward_want = (f(x0 + h) - f(x0)) / h
        forward_got = sol.fd_derivative(f, x0, h, "forward")
        require(
            close(forward_got, forward_want, 1e-9),
            "at a large positive step the forward estimate must be the forward quotient (f(x+h) - f(x)) / h at that "
            "step (hint: Lesson 13, the step is not capped)",
        )


def test_positive_step_is_accepted() -> None:
    coeffs, x0 = INST["cubic"], INST["x0"]
    for scheme in ("forward", "central"):
        value = must_accept(
            partial(sol.fd_derivative, lambda x: float(cubic(coeffs, x)), x0, 1e-3, scheme),
            "a positive step is inside the specification",
        )
        require(isinstance(value, float) and math.isfinite(value), "a positive step must return a finite float")


def test_very_small_positive_step_is_accepted() -> None:
    # Any step above zero is inside the specification, however small: only a step that is not above zero is refused.
    coeffs, x0 = INST["cubic"], INST["x0"]
    for scheme in ("forward", "central"):
        value = must_accept(
            partial(sol.fd_derivative, lambda x: float(cubic(coeffs, x)), x0, 1e-300, scheme),
            "a positive step, however small, is inside the specification",
        )
        require(isinstance(value, float) and math.isfinite(value), "a positive step must return a finite float")


def test_forward_quotient_at_a_tiny_step_is_the_quotient() -> None:
    # For f(x) = x*x at x = 0 the forward quotient at step h is (h*h - 0) / h = h. At h = 1e-9 it must be 1e-9: a step
    # above zero is used as given, not rounded up to a larger step (which would return 1e-8, ten times the value).
    value = sol.fd_derivative(lambda x: x * x, 0.0, 1e-9, "forward")
    require(
        close(value, 1e-9, 1e-9),
        "the forward estimate at a tiny positive step must be the forward quotient (f(x+h) - f(x)) / h at that step "
        "(hint: Lesson 13, the step is used as given)",
    )


def test_forward_zero_numerator_at_the_origin_returns_a_float() -> None:
    # For f(x) = 5 at x = 0 the forward numerator f(x+h) - f(x) is 0, so the quotient is 0. The page states that
    # fd_derivative returns a float, and a zero quotient is still a float: 0.0, not the int 0.
    value = sol.fd_derivative(lambda x: 5.0, 0.0, 1e-3, "forward")
    require(
        isinstance(value, float) and value == 0.0,
        "fd_derivative must return a float, as the page states, also for a zero forward quotient at x = 0 "
        "(hint: return the quotient as a float, 0.0 and not 0)",
    )


def test_forward_and_central_schemes_are_accepted() -> None:
    coeffs, x0 = INST["cubic"], INST["x0"]
    for scheme in ("forward", "central"):
        must_accept(
            partial(sol.fd_derivative, lambda x: float(cubic(coeffs, x)), x0, 1e-3, scheme),
            f"the scheme named {scheme!r} is in the specification",
        )


@pytest.mark.parametrize("scheme", ["backward", "Central", "Forward", "", " central", "central ", "forward "])
def test_unknown_scheme_raises_value_error(scheme: str) -> None:
    coeffs, x0 = INST["cubic"], INST["x0"]
    must_raise(
        lambda: sol.fd_derivative(lambda x: cubic(coeffs, x), x0, 1e-3, scheme),
        "a scheme outside forward and central must be refused with "
        "ValueError (hint: Lesson 13, the two schemes are forward and central)",
    )


@pytest.mark.parametrize("scheme", [None, 1, True, 1.0, b"central"])
def test_scheme_that_is_not_a_name_raises_value_error(scheme: Any) -> None:
    # A scheme other than "forward" or "central" is refused, whatever its type: None, an integer, a bool (True equals
    # 1), a float (1.0 equals 1) and bytes (b"central" is not the str "central") are not names.
    coeffs, x0 = INST["cubic"], INST["x0"]
    must_raise(
        lambda: sol.fd_derivative(lambda x: cubic(coeffs, x), x0, 1e-3, scheme),
        "a scheme that is not the name forward or central must be refused with ValueError "
        "(hint: Lesson 13, the two schemes are forward and central)",
    )


# ---- automatic differentiation: ad_derivative ----


@pytest.mark.parametrize("inst", INSTANCES)
def test_forward_mode_matches_the_analytic_derivative(inst: dict[str, Any]) -> None:
    coeffs, x0 = inst["cubic"], inst["x0"]
    value = sol.ad_derivative(lambda x: cubic(coeffs, x), x0)
    require(
        isinstance(value, float),
        "ad_derivative must return a float, as the page states (hint: return the dot part as a float)",
    )
    require(
        close(value, cubic_prime(coeffs, x0), 1e-9),
        "forward-mode AD must return f'(x) to 1e-9 relative (hint: Lesson 14, forward-mode automatic differentiation)",
    )


def test_forward_mode_is_exact_far_from_zero() -> None:
    # d/dx x^3 = 3x^2 is 3e10 at x = 1e5. Forward mode is exact up to round-off at any point, so it must return 3e10 to
    # 1e-9 relative. A difference quotient with a fixed step does not: its round-off grows as the function grows.
    value = sol.ad_derivative(lambda x: x * x * x, 1e5)
    require(
        close(value, 3e10, 1e-9),
        "forward-mode AD must return f'(x) to 1e-9 relative at a large point, as it does near zero "
        "(hint: Lesson 14, forward mode carries the derivative exactly, with no step)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_product_rule_holds_for_three_factors(inst: dict[str, Any]) -> None:
    x0 = inst["x0"]
    value = sol.ad_derivative(lambda x: x * (x + 1) * (x - 2), x0)
    require(
        close(value, 3 * x0 * x0 - 2 * x0 - 2, 1e-9),
        "the product rule must hold for a product of three factors (hint: Lesson 14, the product rule on dual numbers)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_reflected_operators_are_defined(inst: dict[str, Any]) -> None:
    # A number on the left of - and * (2.0 - 3.0 * x) uses the reflected operators of the dual number.
    x0 = inst["x0"]
    value = sol.ad_derivative(lambda x: 2.0 - 3.0 * x + x * x, x0)
    require(
        close(value, -3.0 + 2 * x0, 1e-9),
        "a number on the left of - or * must work with a dual number (hint: Lesson 14, the reflected operators)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_sum_of_two_quantities_that_depend_on_x(inst: dict[str, Any]) -> None:
    # x * x and x are both dual numbers, so their sum must carry both derivatives: d/dx (x*x + x) = 2x + 1.
    x0 = inst["x0"]
    value = sol.ad_derivative(lambda x: x * x + x, x0)
    require(
        close(value, 2 * x0 + 1, 1e-9),
        "the sum of two quantities that both depend on x must add both derivatives "
        "(hint: Lesson 14, the sum rule on dual numbers)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_difference_of_two_quantities_that_depend_on_x(inst: dict[str, Any]) -> None:
    # d/dx (x - x*x) = 1 - 2x: the derivative of the subtracted quantity must be subtracted, not dropped.
    x0 = inst["x0"]
    value = sol.ad_derivative(lambda x: x - x * x, x0)
    require(
        close(value, 1 - 2 * x0, 1e-9),
        "the difference of two quantities that both depend on x must subtract both derivatives "
        "(hint: Lesson 14, the difference rule on dual numbers)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_plain_numbers_on_either_side_of_plus_and_minus(inst: dict[str, Any]) -> None:
    # d/dx (2 + x*x - 0.5) = 2x: a number on the left of + and on the right of - leaves the derivative alone.
    x0 = inst["x0"]
    value = sol.ad_derivative(lambda x: 2.0 + x * x - 0.5, x0)
    require(
        close(value, 2 * x0, 1e-9),
        "a plain number on either side of + or - must not change the derivative "
        "(hint: Lesson 14, constants have zero derivative)",
    )


def test_constant_function_has_zero_derivative() -> None:
    # A function written with numbers only does not depend on x, so its derivative is 0 at every point.
    value = sol.ad_derivative(lambda x: 5.0, 0.7)
    require(
        isinstance(value, float),
        "ad_derivative must return a float, as the page states (hint: return the dot part as a float)",
    )
    require(
        value == 0.0,
        "the derivative of a constant function must be 0 (hint: Lesson 14, constants have zero derivative)",
    )


def test_ad_derivative_at_the_origin_returns_a_float() -> None:
    # d/dx x*x = 2x is 0 at x = 0. The page states that ad_derivative returns a float, so the zero derivative at the
    # origin must be 0.0, not the int 0.
    value = sol.ad_derivative(lambda x: x * x, 0.0)
    require(
        isinstance(value, float) and value == 0.0,
        "ad_derivative must return a float, as the page states, also for a zero derivative at x = 0 "
        "(hint: return the dot part as a float)",
    )


# ---- Hessians: hessian_fd ----


@pytest.mark.parametrize("inst", INSTANCES)
def test_hessian_is_a_square_list_of_lists_of_floats(inst: dict[str, Any]) -> None:
    c, point = inst["surface"], inst["point"]
    got = sol.hessian_fd(lambda p: surface(c, p), point, 1e-4)
    require(isinstance(got, list) and len(got) == 2, "the Hessian must be a list with one row per variable")
    for row in got:
        require(
            isinstance(row, list) and len(row) == 2 and all(isinstance(v, float) for v in row),
            "the Hessian must be a square list of lists of floats",
        )


@pytest.mark.parametrize("inst", INSTANCES)
def test_hessian_matches_the_analytic_hessian(inst: dict[str, Any]) -> None:
    c, point = inst["surface"], inst["point"]
    got = sol.hessian_fd(lambda p: surface(c, p), point, 1e-4)
    want = surface_hessian(c, point)
    for i in range(2):
        for j in range(2):
            require(
                close(got[i][j], want[i][j], 1e-5),
                "each Hessian entry must match its analytic value to "
                "1e-5 (hint: Lesson 19, the Hessian by second differences)",
            )


@pytest.mark.parametrize("inst", INSTANCES)
def test_hessian_is_symmetric(inst: dict[str, Any]) -> None:
    c, point = inst["surface"], inst["point"]
    got = sol.hessian_fd(lambda p: surface(c, p), point, 1e-4)
    scale = 1.0 + max(abs(got[0][1]), abs(got[1][0]))
    require(
        abs(got[0][1] - got[1][0]) <= 1e-6 * scale,
        "the Hessian must be symmetric (hint: Lesson 19, mixed second derivatives do not depend on the order)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_hessian_diagonal_matches_the_second_difference(inst: dict[str, Any]) -> None:
    c, point = inst["surface"], inst["point"]
    h = 1e-4
    got = sol.hessian_fd(lambda p: surface(c, p), point, h)
    for i in range(2):
        up = list(point)
        down = list(point)
        up[i] += h
        down[i] -= h
        second = (surface(c, up) - 2 * surface(c, point) + surface(c, down)) / (h * h)
        require(
            close(got[i][i], second, 1e-5),
            "each diagonal entry must equal the second difference "
            "along its axis (hint: Lesson 19, the diagonal of the Hessian)",
        )


def test_hessian_zero_or_negative_step_raises_value_error() -> None:
    c, point = INST["surface"], INST["point"]
    must_raise(
        lambda: sol.hessian_fd(lambda p: surface(c, p), point, 0.0),
        "a Hessian step of zero must raise (hint: Lesson 19, the Hessian needs a positive step)",
    )
    must_raise(
        lambda: sol.hessian_fd(lambda p: surface(c, p), point, -1e-4),
        "a negative Hessian step must raise (hint: Lesson 19, the Hessian needs a positive step)",
    )


def test_hessian_tiny_negative_or_negative_zero_step_raises_value_error() -> None:
    c, point = INST["surface"], INST["point"]
    for step in (-1e-300, -0.0):
        must_raise(
            partial(sol.hessian_fd, lambda p: surface(c, p), point, step),
            "a Hessian step that is not above zero must raise, however small "
            "(hint: Lesson 19, the Hessian needs a positive step)",
        )


def test_hessian_nan_step_raises_value_error() -> None:
    c, point = INST["surface"], INST["point"]
    must_raise(
        lambda: sol.hessian_fd(lambda p: surface(c, p), point, float("nan")),
        "a NaN Hessian step is not above zero and must raise (hint: Lesson 19, the Hessian needs a positive step)",
    )


def test_hessian_negative_infinite_step_raises_value_error() -> None:
    c, point = INST["surface"], INST["point"]
    must_raise(
        lambda: sol.hessian_fd(lambda p: surface(c, p), point, -math.inf),
        "a Hessian step of negative infinity is below zero and must raise (hint: Lesson 19, the Hessian needs a "
        "positive step)",
    )


def test_hessian_positive_step_is_accepted() -> None:
    # Steps from 1e-4 to 1 are accepted, and the entries are finite floats. At steps 1e-3 and 1 each entry must also be
    # the page's formula at that step: the diagonal second difference over h^2 and the mixed difference over 4h^2. The
    # function is not a polynomial, so a silently changed step shows in the entries.
    point = INST["point"]
    u0, v0 = point

    def g(p: list[float]) -> float:
        return math.sin(p[0]) * math.cos(p[1])

    def at(du: float, dv: float) -> float:
        return g([u0 + du, v0 + dv])

    for step in (1e-4, 1e-3, 1.0):
        got = must_accept(
            partial(sol.hessian_fd, g, point, step),
            f"a Hessian step of {step} is above zero, so the specification accepts it",
        )
        require(
            isinstance(got, list) and all(isinstance(v, float) and math.isfinite(v) for row in got for v in row),
            "a positive Hessian step must return a finite float in every entry",
        )
        if step == 1e-4:
            continue
        h = step
        centre = at(0.0, 0.0)
        want_uu = (at(h, 0.0) - 2 * centre + at(-h, 0.0)) / (h * h)
        want_vv = (at(0.0, h) - 2 * centre + at(0.0, -h)) / (h * h)
        want_uv = (at(h, h) - at(h, -h) - at(-h, h) + at(-h, -h)) / (4 * h * h)
        want = [[want_uu, want_uv], [want_uv, want_vv]]
        rows: Any = got  # must_accept returns an object; the require above has checked that it is a list of float rows
        for i in range(2):
            for j in range(2):
                tolerance = 1e-9 * max(1.0, abs(want[i][j])) + 1e-12 / (h * h)
                require(
                    abs(rows[i][j] - want[i][j]) <= tolerance,
                    "at a positive Hessian step each entry must be the second difference over h^2 (diagonal) or the "
                    "mixed difference over 4h^2 (off-diagonal) at that step (hint: Lesson 19, the step is not capped)",
                )


# ---- bond price in integer cents: bond_price_cents ----


@pytest.mark.parametrize("inst", INSTANCES)
def test_price_is_an_integer_number_of_cents(inst: dict[str, Any]) -> None:
    price = sol.bond_price_cents(inst)
    require(type(price) is int, "the bond price must be reported as an int number of cents")


@pytest.mark.parametrize("inst", INSTANCES)
def test_price_is_the_half_even_rounding_of_the_exact_price(inst: dict[str, Any]) -> None:
    require(
        sol.bond_price_cents(inst) == round(exact_price(inst)),
        "the price must be the exact price rounded half to even "
        "(hint: the price convention, cash flows and half-to-even rounding)",
    )


def test_exact_halves_round_to_the_even_cent() -> None:
    # A one-year bond at a 100 % yield has price face / 2: 3 cents gives 1.5, 5 cents gives 2.5, 7 cents gives 3.5.
    cases = {3: 2, 5: 2, 7: 4}
    for face, want in cases.items():
        got = sol.bond_price_cents(bond(face, 0, 1, 10_000))
        require(
            got == want,
            "an exact half cent must round to the even neighbour (hint: the half-to-even rule in the price convention)",
        )


def test_prices_just_off_a_half_cent_round_to_the_nearer_cent() -> None:
    # A one-year bond at a 0 % yield has price face * (1 + coupon). With face 1 cent: 1.4999 cents rounds down to 1, and
    # 1.5001 cents rounds up to 2. A rule that rounds twice, first to a tenth of a cent, rounds 1.4999 up to 2.
    got_below = sol.bond_price_cents(bond(1, 4999, 1, 0))
    got_above = sol.bond_price_cents(bond(1, 5001, 1, 0))
    require(got_below == 1, "a price just below a half cent must round down to the nearer cent")
    require(got_above == 2, "a price just above a half cent must round up to the nearer cent")


def test_price_at_par_equals_face() -> None:
    # When the yield equals the coupon rate, the bond prices at par: the price is the face value exactly.
    for face, coupon in ((1_000_000, 500), (12_345_678, 0), (4_000_000, 1000)):
        require(
            sol.bond_price_cents(bond(face, coupon, 7, coupon)) == face, "a bond with yield equal to coupon is at par"
        )


def test_prices_at_a_negative_yield_round_half_to_even() -> None:
    # A one-year bond at a yield of -50 % (-5000 basis points, above -1) has price 2 * (face + coupon) in cents, so an
    # exact half cent comes at a coupon of 2500 basis points. Face 1 gives 2.5, which rounds to 2; face 3 gives 7.5,
    # which rounds to 8; and the prices either side of a half cent round to the nearer cent.
    cases = {
        (1, 2500, 1, -5000): 2,
        (3, 2500, 1, -5000): 8,
        (1, 2499, 1, -5000): 2,
        (1, 2501, 1, -5000): 3,
    }
    for (face, coupon, years, yield_bps), want in cases.items():
        got = sol.bond_price_cents(bond(face, coupon, years, yield_bps))
        require(
            got == want,
            "a price at a yield above -1 must round half to even like any other price "
            "(hint: the price convention, half-to-even rounding of the unrounded price)",
        )


def test_price_falls_as_the_yield_rises() -> None:
    for inst in INSTANCES:
        low = sol.bond_price_cents(inst)
        higher = dict(inst, yield_bps=inst["yield_bps"] + 100)
        require(
            sol.bond_price_cents(higher) < low, "a higher yield must lower the price of a bond with positive cash flows"
        )


# ---- sensitivities: sensitivities ----


@pytest.mark.parametrize("inst", INSTANCES)
def test_sensitivities_have_the_named_keys_as_floats(inst: dict[str, Any]) -> None:
    result = sol.sensitivities(inst)
    for key in ANALYTIC_KEYS:
        require(key in result, f"the sensitivities must include the key {key!r}")
        require(isinstance(result[key], float), "every sensitivity must be a float")


@pytest.mark.parametrize("inst", INSTANCES)
def test_first_derivative_matches_the_central_difference_of_the_price(inst: dict[str, Any]) -> None:
    y, h = yield_of(inst), 1e-5
    numeric = (unrounded_price(inst, y + h) - unrounded_price(inst, y - h)) / (2 * h)
    got = sol.sensitivities(inst)["dprice_dy"]
    require(
        close(got, numeric, 1e-6),
        "dprice_dy must match the central difference of the unrounded "
        "price (hint: Lesson 5, the chain rule on each discount factor)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_second_derivative_matches_the_central_difference_of_the_price(inst: dict[str, Any]) -> None:
    y, h = yield_of(inst), 1e-5
    p0 = unrounded_price(inst, y)
    numeric = (unrounded_price(inst, y + h) - 2 * p0 + unrounded_price(inst, y - h)) / (h * h)
    got = sol.sensitivities(inst)["d2price_dy2"]
    require(
        close(got, numeric, 1e-4),
        "d2price_dy2 must match the second central difference of the unrounded "
        "price (hint: Lesson 5 and Lesson 13, second derivatives by differences)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_named_ratios_are_the_stated_formulas(inst: dict[str, Any]) -> None:
    result = sol.sensitivities(inst)
    price = unrounded_price(inst, yield_of(inst))
    require(
        close(result["duration_analytic"], -result["dprice_dy"] / price, 1e-9),
        "duration_analytic must be -dprice_dy / price (hint: the named ratios in the conventions)",
    )
    require(
        close(result["convexity_analytic"], result["d2price_dy2"] / price, 1e-9),
        "convexity_analytic must be d2price_dy2 / price (hint: the named ratios in the conventions)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_sensitivity_signs_follow_positive_cash_flows(inst: dict[str, Any]) -> None:
    result = sol.sensitivities(inst)
    require(
        result["dprice_dy"] < 0,
        "a bond with positive cash flows must fall in price as the "
        "yield rises (hint: the sign of a discount factor's derivative)",
    )
    require(
        result["d2price_dy2"] > 0,
        "a bond with positive cash flows must be convex in its "
        "yield (hint: the sign of a discount factor's second derivative)",
    )


# ---- the yield condition: a yield at or below -1 raises ValueError, a yield above -1 is accepted ----


def test_yield_at_minus_one_raises_for_price_and_sensitivities() -> None:
    inst = dict(INST, yield_bps=-10_000)
    must_raise(
        lambda: sol.bond_price_cents(inst),
        "a yield of -1 must be refused by bond_price_cents (hint: the yield condition in the conventions)",
    )
    must_raise(
        lambda: sol.sensitivities(inst),
        "a yield of -1 must be refused by sensitivities (hint: the yield condition in the conventions)",
    )


def test_yield_below_minus_one_raises_for_price_and_sensitivities() -> None:
    inst = dict(INST, yield_bps=-20_000)
    must_raise(
        lambda: sol.bond_price_cents(inst),
        "a yield below -1 must be refused by bond_price_cents (hint: the yield condition in the conventions)",
    )
    must_raise(
        lambda: sol.sensitivities(inst),
        "a yield below -1 must be refused by sensitivities (hint: the yield condition in the conventions)",
    )


def test_yield_one_basis_point_below_minus_one_raises() -> None:
    # -10001 basis points is a yield of -1.0001, below -1: the boundary is at -10000, so the refusal starts there.
    inst = dict(INST, yield_bps=-10_001)
    must_raise(
        lambda: sol.bond_price_cents(inst),
        "a yield one basis point below -1 must be refused by bond_price_cents "
        "(hint: the yield condition in the conventions)",
    )
    must_raise(
        lambda: sol.sensitivities(inst),
        "a yield one basis point below -1 must be refused by sensitivities "
        "(hint: the yield condition in the conventions)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_sensitivities_at_a_negative_yield_match_the_central_difference(inst: dict[str, Any]) -> None:
    # A yield of -0.5 is above -1, so it is inside the specification. Its sensitivities differ from those at +0.5.
    neg = dict(inst, yield_bps=-5_000)
    y, h = -0.5, 1e-5
    p0 = unrounded_price(neg, y)
    first_numeric = (unrounded_price(neg, y + h) - unrounded_price(neg, y - h)) / (2 * h)
    second_numeric = (unrounded_price(neg, y + h) - 2 * p0 + unrounded_price(neg, y - h)) / (h * h)
    result = sol.sensitivities(neg)
    require(
        close(result["dprice_dy"], first_numeric, 1e-6),
        "at a negative yield above -1, dprice_dy must match the central difference of the unrounded price "
        "(hint: the yield enters each discount factor as 1 + y, with its sign)",
    )
    require(
        close(result["d2price_dy2"], second_numeric, 1e-4),
        "at a negative yield above -1, d2price_dy2 must match the second central difference of the unrounded price "
        "(hint: the yield enters each discount factor as 1 + y, with its sign)",
    )


def test_yield_just_above_minus_one_is_accepted() -> None:
    inst = dict(INST, yield_bps=-9_999)
    price = must_accept(lambda: sol.bond_price_cents(inst), "a yield above -1 is inside the specification")
    require(type(price) is int, "the price at a yield above -1 must still be an int")
    result = must_accept(lambda: sol.sensitivities(inst), "a yield above -1 is inside the specification")
    require(isinstance(result, dict), "sensitivities must return a dictionary")


def test_sensitivities_near_minus_one_are_the_stated_formulas() -> None:
    # A yield of -0.99 is above -1, so it is inside the specification. The discount factor there is 100, so a central
    # difference at step 1e-5 is off by far more than 1e-9 relative, and only the stated formulas meet that tolerance.
    inst = bond(1_000_000, 500, 30, -9_900)
    first, second = exact_sensitivities(inst)
    result = sol.sensitivities(inst)
    require(
        close(result["dprice_dy"], float(first), 1e-9),
        "dprice_dy must be -sum t C_t (1+y)^(-t-1) near a yield of -1 "
        "(hint: the derivative of each discount factor, with its sign)",
    )
    require(
        close(result["d2price_dy2"], float(second), 1e-9),
        "d2price_dy2 must be sum t(t+1) C_t (1+y)^(-t-2) near a yield of -1 "
        "(hint: the second derivative of each discount factor)",
    )


# ---- the module is pure: no output ----


def test_module_prints_nothing_and_warns_nothing() -> None:
    # The five named functions, each on a branch the other tests reach: both schemes, a step above a thousand, the
    # constant and the non-constant case of ad_derivative, the price and the sensitivities at a positive and at a
    # negative yield above -1, and each named refusal. Output to stdout and stderr is captured.
    buffer = io.StringIO()
    coeffs, x0 = INST["cubic"], INST["x0"]
    poly = partial(cubic, coeffs)
    calls: list[Callable[[], object]] = [
        lambda: sol.bond_price_cents(INST),
        lambda: sol.sensitivities(INST),
        lambda: sol.bond_price_cents(dict(INST, yield_bps=-5_000)),
        lambda: sol.sensitivities(dict(INST, yield_bps=-5_000)),
        lambda: sol.fd_derivative(lambda x: float(poly(x)), x0, 1e-3, "central"),
        lambda: sol.fd_derivative(lambda x: float(poly(x)), x0, 1e-3, "forward"),
        lambda: sol.fd_derivative(lambda x: float(poly(x)), x0, 1e6, "central"),
        lambda: sol.fd_derivative(lambda x: float(poly(x)), x0, 1e6, "forward"),
        lambda: sol.hessian_fd(lambda p: surface(INST["surface"], p), INST["point"], 1e-4),
        lambda: sol.ad_derivative(poly, x0),
        lambda: sol.ad_derivative(lambda x: 5.0, x0),
        lambda: sol.fd_derivative(lambda x: float(poly(x)), x0, 0.0, "central"),
        lambda: sol.fd_derivative(lambda x: float(poly(x)), x0, 1e-3, "bogus"),
        lambda: sol.hessian_fd(lambda p: surface(INST["surface"], p), INST["point"], 0.0),
        lambda: sol.bond_price_cents(dict(INST, yield_bps=-10_000)),
        lambda: sol.sensitivities(dict(INST, yield_bps=-10_000)),
    ]
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            for call in calls:
                # A refusal is expected in five of the calls; its message is discarded, and only output matters here.
                with contextlib.suppress(ValueError):
                    call()
    require(buffer.getvalue() == "", "the module must not print, on any branch of any function")
    require(len(caught) == 0, "the module must not warn, on any branch of any function")
