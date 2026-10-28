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
from collections.abc import Callable
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


@pytest.mark.parametrize("inst", INSTANCES)
def test_forward_error_is_of_order_h(inst: dict[str, Any]) -> None:
    coeffs, x0 = inst["cubic"], inst["x0"]
    exact = cubic_prime(coeffs, x0)

    def error(h: float) -> float:
        return float(abs(sol.fd_derivative(lambda x: float(cubic(coeffs, x)), x0, h, "forward") - exact))

    ratio = error(1e-2) / error(5e-3)
    require(
        1.9 <= ratio <= 2.1,
        "the forward difference's error must halve with its step: order "
        "h, not h squared (hint: Lesson 13, the forward error is of order h)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_central_error_is_of_order_h_squared(inst: dict[str, Any]) -> None:
    coeffs, x0 = inst["cubic"], inst["x0"]
    exact = cubic_prime(coeffs, x0)

    def error(h: float) -> float:
        return float(abs(sol.fd_derivative(lambda x: float(cubic(coeffs, x)), x0, h, "central") - exact))

    ratio = error(1e-2) / error(5e-3)
    require(
        3.8 <= ratio <= 4.2,
        "the central error must fall four-fold when its step halves: order "
        "h squared (hint: Lesson 13, the central error is of order h squared)",
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


def test_positive_step_is_accepted() -> None:
    coeffs, x0 = INST["cubic"], INST["x0"]
    for scheme in ("forward", "central"):
        value = must_accept(
            partial(sol.fd_derivative, lambda x: float(cubic(coeffs, x)), x0, 1e-3, scheme),
            "a positive step is inside the specification",
        )
        require(isinstance(value, float) and math.isfinite(value), "a positive step must return a finite float")


def test_forward_and_central_schemes_are_accepted() -> None:
    coeffs, x0 = INST["cubic"], INST["x0"]
    for scheme in ("forward", "central"):
        must_accept(
            partial(sol.fd_derivative, lambda x: float(cubic(coeffs, x)), x0, 1e-3, scheme),
            f"the scheme named {scheme!r} is in the specification",
        )


@pytest.mark.parametrize("scheme", ["backward", "Central", ""])
def test_unknown_scheme_raises_value_error(scheme: str) -> None:
    coeffs, x0 = INST["cubic"], INST["x0"]
    must_raise(
        lambda: sol.fd_derivative(lambda x: cubic(coeffs, x), x0, 1e-3, scheme),
        "a scheme outside forward and central must be refused with "
        "ValueError (hint: Lesson 13, the two schemes are forward and central)",
    )


# ---- automatic differentiation: ad_derivative ----


@pytest.mark.parametrize("inst", INSTANCES)
def test_forward_mode_matches_the_analytic_derivative(inst: dict[str, Any]) -> None:
    coeffs, x0 = inst["cubic"], inst["x0"]
    value = sol.ad_derivative(lambda x: cubic(coeffs, x), x0)
    require(
        close(value, cubic_prime(coeffs, x0), 1e-9),
        "forward-mode AD must return f'(x) to 1e-9 relative (hint: Lesson 14, forward-mode automatic differentiation)",
    )


@pytest.mark.parametrize("inst", INSTANCES)
def test_product_rule_holds_for_three_factors(inst: dict[str, Any]) -> None:
    x0 = inst["x0"]
    value = sol.ad_derivative(lambda x: x * (x + 1) * (x - 2), x0)
    require(
        close(value, 3 * x0 * x0 - 2 * x0 - 2, 1e-9),
        "the product rule must hold for a product of three factors (hint: Lesson 14, the product rule on dual numbers)",
    )


# ---- Hessians: hessian_fd ----


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
        "the Hessian must be symmetric (Schwarz's theorem) (hint: "
        "Lesson 19, mixed second derivatives do not depend on the order)",
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


def test_hessian_positive_step_is_accepted() -> None:
    c, point = INST["surface"], INST["point"]
    must_accept(lambda: sol.hessian_fd(lambda p: surface(c, p), point, 1e-4), "a positive step is in the specification")


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


def test_price_at_par_equals_face() -> None:
    # When the yield equals the coupon rate, the bond prices at par: the price is the face value exactly.
    for face, coupon in ((1_000_000, 500), (12_345_678, 0), (4_000_000, 1000)):
        require(
            sol.bond_price_cents(bond(face, coupon, 7, coupon)) == face, "a bond with yield equal to coupon is at par"
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


def test_yield_just_above_minus_one_is_accepted() -> None:
    inst = dict(INST, yield_bps=-9_999)
    price = must_accept(lambda: sol.bond_price_cents(inst), "a yield above -1 is inside the specification")
    require(type(price) is int, "the price at a yield above -1 must still be an int")
    result = must_accept(lambda: sol.sensitivities(inst), "a yield above -1 is inside the specification")
    require(isinstance(result, dict), "sensitivities must return a dictionary")


# ---- the module is pure: no output ----


def test_module_prints_nothing() -> None:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        sol.bond_price_cents(INST)
        sol.sensitivities(INST)
        sol.fd_derivative(lambda x: cubic(INST["cubic"], x), INST["x0"], 1e-3, "central")
        sol.hessian_fd(lambda p: surface(INST["surface"], p), INST["point"], 1e-4)
    require(buffer.getvalue() == "", "the module must not print")
