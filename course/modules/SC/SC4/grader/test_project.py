"""Pytest test suite for SC4 PDE pricer autograder.

Tests finite-difference solvers, boundary conditions, Greek computations,
put-call parity, barrier option pricing, Rannacher smoothing, and convergence order certification.
"""

from __future__ import annotations

import math
import os
from typing import Any

import numpy as np
import pytest
from instance import make_instance  # type: ignore[import-not-found]
from reference import (  # type: ignore[import-not-found]
    bs_down_and_out_call,
    bs_price,
    estimate_convergence_order,
    norm_cdf,
    price_option,
    solve_pde,
    thomas_solve,
)

_SEED = int(os.environ.get("QF_SEED", "0"))
_INST: dict[str, Any] = make_instance(_SEED)


def test_t01_input_validation_negative_parameters() -> None:
    """T01: Non-positive or non-finite inputs raise ValueError."""
    __tracebackhide__ = True
    s, k, t, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.2

    with pytest.raises(ValueError):
        solve_pde(0.0, k, t, r, sigma, "call")
    with pytest.raises(ValueError):
        solve_pde(-10.0, k, t, r, sigma, "call")
    with pytest.raises(ValueError):
        solve_pde(s, 0.0, t, r, sigma, "call")
    with pytest.raises(ValueError):
        solve_pde(s, k, 0.0, r, sigma, "call")
    with pytest.raises(ValueError):
        solve_pde(s, k, t, -0.01, sigma, "call")
    with pytest.raises(ValueError):
        solve_pde(s, k, t, r, 0.0, "call")
    with pytest.raises(ValueError):
        solve_pde(float("nan"), k, t, r, sigma, "call")


def test_t02_input_validation_types_and_methods() -> None:
    """T02: Invalid option types, payoff types, or solver methods raise ValueError."""
    __tracebackhide__ = True
    s, k, t, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.2

    with pytest.raises(ValueError, match="option_type"):
        solve_pde(s, k, t, r, sigma, "straddle")
    with pytest.raises(ValueError, match="payoff_type"):
        solve_pde(s, k, t, r, sigma, "call", payoff_type="exotic")
    with pytest.raises(ValueError, match="method"):
        solve_pde(s, k, t, r, sigma, "call", method="runge_kutta")


def test_t03_input_validation_barrier_constraints() -> None:
    """T03: Barrier option validation: barrier must be positive and below spot for down-and-out."""
    __tracebackhide__ = True
    s, k, t, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.2

    with pytest.raises(ValueError):
        solve_pde(s, k, t, r, sigma, "call", payoff_type="barrier", barrier=None)
    with pytest.raises(ValueError):
        solve_pde(s, k, t, r, sigma, "call", payoff_type="barrier", barrier=110.0, barrier_type="down_and_out")
    with pytest.raises(ValueError):
        solve_pde(s, k, t, r, sigma, "call", payoff_type="barrier", barrier=-5.0, barrier_type="down_and_out")


def test_t04_thomas_algorithm_known_system() -> None:
    """T04: Thomas algorithm correctly solves a known tridiagonal linear system."""
    __tracebackhide__ = True
    # Matrix:
    # [ 2  -1   0 ] [ x0 ]   [ 1 ]
    # [-1   2  -1 ] [ x1 ] = [ 0 ]
    # [ 0  -1   2 ] [ x2 ]   [ 1 ]
    # Solution is x = [1, 1, 1]
    a = np.array([0.0, -1.0, -1.0])
    b = np.array([2.0, 2.0, 2.0])
    c = np.array([-1.0, -1.0, 0.0])
    d = np.array([1.0, 0.0, 1.0])

    x = thomas_solve(a, b, c, d)
    assert np.allclose(x, np.array([1.0, 1.0, 1.0]), atol=1e-12)


def test_t05_put_call_parity_vanilla() -> None:
    """T05: European options computed via Crank-Nicolson satisfy discrete Put-Call Parity."""
    __tracebackhide__ = True
    s0 = float(_INST["spot"])
    k = float(_INST["strike"])
    t = float(_INST["maturity"])
    r = float(_INST["rate"])
    sigma = float(_INST["vol"])

    c = price_option(s0, k, t, r, sigma, "call", n_space=160, n_time=80)
    p = price_option(s0, k, t, r, sigma, "put", n_space=160, n_time=80)

    theoretical_diff = s0 - k * math.exp(-r * t)
    numerical_diff = c - p
    assert abs(numerical_diff - theoretical_diff) < 0.08 * (1.0 + abs(s0))


def test_t06_vanilla_call_accuracy_black_scholes() -> None:
    """T06: Crank-Nicolson European call price agrees with analytical Black-Scholes formula."""
    __tracebackhide__ = True
    s0 = float(_INST["spot"])
    k = float(_INST["strike"])
    t = float(_INST["maturity"])
    r = float(_INST["rate"])
    sigma = float(_INST["vol"])

    pde_c = price_option(s0, k, t, r, sigma, "call", n_space=200, n_time=100)
    exact_c = bs_price(s0, k, t, r, sigma, "call")
    assert abs(pde_c - exact_c) < 0.05


def test_t07_vanilla_put_accuracy_black_scholes() -> None:
    """T07: Crank-Nicolson European put price agrees with analytical Black-Scholes formula."""
    __tracebackhide__ = True
    s0 = float(_INST["spot"])
    k = float(_INST["strike"])
    t = float(_INST["maturity"])
    r = float(_INST["rate"])
    sigma = float(_INST["vol"])

    pde_p = price_option(s0, k, t, r, sigma, "put", n_space=200, n_time=100)
    exact_p = bs_price(s0, k, t, r, sigma, "put")
    assert abs(pde_p - exact_p) < 0.05


def test_t08_delta_and_gamma_accuracy() -> None:
    """T08: Finite-difference Greeks Delta and Gamma agree with analytical Black-Scholes Greeks."""
    __tracebackhide__ = True
    s0 = float(_INST["spot"])
    k = float(_INST["strike"])
    t = float(_INST["maturity"])
    r = float(_INST["rate"])
    sigma = float(_INST["vol"])

    sol = solve_pde(s0, k, t, r, sigma, "call", n_space=240, n_time=120)
    delta_pde = float(sol["delta"])
    gamma_pde = float(sol["gamma"])

    d1 = (math.log(s0 / k) + (r + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))
    exact_delta = norm_cdf(d1)
    exact_gamma = math.exp(-0.5 * d1**2) / (math.sqrt(2.0 * math.pi) * s0 * sigma * math.sqrt(t))

    assert abs(delta_pde - exact_delta) < 0.01
    assert abs(gamma_pde - exact_gamma) < 0.005


def test_t09_down_and_out_call_arbitrage_bounds() -> None:
    """T09: Down-and-out call satisfies strict no-arbitrage bounds 0 <= C_do <= C_vanilla."""
    __tracebackhide__ = True
    s0 = float(_INST["spot"])
    k = float(_INST["strike"])
    t = float(_INST["maturity"])
    r = float(_INST["rate"])
    sigma = float(_INST["vol"])
    b = float(_INST["barrier"])

    c_vanilla = price_option(s0, k, t, r, sigma, "call", n_space=160, n_time=80)
    c_do = price_option(
        s0,
        k,
        t,
        r,
        sigma,
        "call",
        payoff_type="barrier",
        barrier=b,
        barrier_type="down_and_out",
        n_space=160,
        n_time=80,
    )

    assert c_do >= -1e-8
    assert c_do <= c_vanilla + 0.05


def test_t10_down_and_out_call_accuracy_analytical() -> None:
    """T10: Down-and-out call price agrees with analytical Merton (1973) reflection formula."""
    __tracebackhide__ = True
    s0 = float(_INST["spot"])
    k = float(_INST["strike"])
    t = float(_INST["maturity"])
    r = float(_INST["rate"])
    sigma = float(_INST["vol"])
    b = float(_INST["barrier"])

    pde_do = price_option(
        s0,
        k,
        t,
        r,
        sigma,
        "call",
        payoff_type="barrier",
        barrier=b,
        barrier_type="down_and_out",
        n_space=240,
        n_time=120,
    )
    exact_do = bs_down_and_out_call(s0, k, b, t, r, sigma)
    assert abs(pde_do - exact_do) < 0.06


def test_t11_barrier_absorption_at_boundary() -> None:
    """T11: Down-and-out call option value approaches zero as spot S0 approaches barrier B."""
    __tracebackhide__ = True
    k = float(_INST["strike"])
    t = float(_INST["maturity"])
    r = float(_INST["rate"])
    sigma = float(_INST["vol"])
    b = float(_INST["barrier"])

    near_barrier_spot = b * 1.002
    pde_val = price_option(
        near_barrier_spot,
        k,
        t,
        r,
        sigma,
        "call",
        payoff_type="barrier",
        barrier=b,
        barrier_type="down_and_out",
        n_space=200,
        n_time=80,
    )
    assert 0.0 <= pde_val < 0.25


def test_t12_digital_call_price_bounds() -> None:
    """T12: Digital call price lies strictly within theoretical bounds (0, e^{-rT})."""
    __tracebackhide__ = True
    s0 = float(_INST["spot"])
    k = float(_INST["strike"])
    t = float(_INST["maturity"])
    r = float(_INST["rate"])
    sigma = float(_INST["vol"])

    p_dig = price_option(s0, k, t, r, sigma, "call", payoff_type="digital", n_space=160, n_time=80)
    disc = math.exp(-r * t)
    assert 0.0 < p_dig < disc


def test_t13_digital_call_rannacher_smoothing_monotonicity() -> None:
    """T13: Rannacher smoothing preserves monotonicity of digital call values across the strike."""
    __tracebackhide__ = True
    s0 = float(_INST["spot"])
    k = float(_INST["strike"])
    t = float(_INST["maturity"])
    r = float(_INST["rate"])
    sigma = float(_INST["vol"])

    sol = solve_pde(
        s0,
        k,
        t,
        r,
        sigma,
        "call",
        payoff_type="digital",
        method="crank_nicolson",
        rannacher=True,
        n_space=200,
        n_time=50,
    )
    grid_v = sol["grid_v"]
    # Option value must be monotonically non-decreasing in spot price for a call
    diffs = np.diff(grid_v)
    # Check that any negative gradient is within numerical tolerance
    assert np.min(diffs) > -1e-5


def test_t14_implicit_euler_stability_large_timestep() -> None:
    """T14: Fully implicit scheme remains strictly stable and non-oscillatory with very few time steps."""
    __tracebackhide__ = True
    s0 = float(_INST["spot"])
    k = float(_INST["strike"])
    t = float(_INST["maturity"])
    r = float(_INST["rate"])
    sigma = float(_INST["vol"])

    # 4 time steps with 200 spatial points gives huge mesh ratio lambda
    sol = solve_pde(s0, k, t, r, sigma, "call", method="implicit", n_space=200, n_time=4)
    price = float(sol["price"])
    assert math.isfinite(price)
    assert price > 0.0
    assert price < s0


def test_t15_crank_nicolson_convergence_order() -> None:
    """T15: Crank-Nicolson with Rannacher smoothing exhibits asymptotic second-order convergence."""
    __tracebackhide__ = True
    order = estimate_convergence_order(
        100.0,
        100.0,
        1.0,
        0.05,
        0.20,
        option_type="call",
        method="crank_nicolson",
        rannacher=True,
        grids=[(100, 50), (200, 100), (400, 200)],
    )
    # Theoretical order is 2.0; certify asymptotic second order (alpha >= 1.8)
    assert order >= 1.8
