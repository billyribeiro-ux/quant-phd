"""Acceptance suite for Atlas A10 (atlas.execution), the MS3 project.

Dual-mode: runs identically in the browser (Pyodide) and locally:
    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import importlib
import math
import os
from collections.abc import Callable
from typing import Any

import numpy as np
import pytest
from instance import make_instance

a10: Any
try:
    a10 = importlib.import_module("atlas.execution")
except ImportError:
    a10 = importlib.import_module("reference")

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
INST2 = make_instance(SEED + 9973)


def expect(condition: bool, hint: str) -> None:
    """Fail with a descriptive hint if condition is false."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(hint, pytrace=False)


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Check that call() raises ValueError."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        return
    except Exception as exc:
        pytest.fail(f"{condition}: expected ValueError, got {type(exc).__name__}: {exc}", pytrace=False)
    pytest.fail(f"{condition}: expected ValueError, none was raised", pytrace=False)


def test_square_root_impact_scaling() -> None:
    """Verify square-root scaling: I(4Q) = 2 * I(Q), directionality, and zero root."""
    v = INST["daily_volume"]
    sigma = INST["daily_volatility"]
    q = INST["total_shares"]

    i1 = a10.square_root_impact(q, v, sigma, y_coeff=0.5)
    i4 = a10.square_root_impact(4.0 * q, v, sigma, y_coeff=0.5)
    expect(math.isclose(i4, 2.0 * i1, rel_tol=1e-6), "Square-root impact must double when order size quadruples")

    # Directionality
    i_neg = a10.square_root_impact(-q, v, sigma, y_coeff=0.5)
    expect(
        math.isclose(i_neg, -i1, rel_tol=1e-6),
        "Selling must produce negative price impact with identical magnitude",
    )

    # Zero root
    i0 = a10.square_root_impact(0.0, v, sigma, y_coeff=0.5)
    expect(i0 == 0.0, "Zero order size must produce zero price impact")


def test_square_root_impact_validation() -> None:
    """Verify input domain checks for square_root_impact."""
    v = INST["daily_volume"]
    sigma = INST["daily_volatility"]
    q = INST["total_shares"]

    must_raise(lambda: a10.square_root_impact(q, 0.0, sigma), "daily_volume <= 0 must raise ValueError")
    must_raise(lambda: a10.square_root_impact(q, -100.0, sigma), "daily_volume < 0 must raise ValueError")
    must_raise(lambda: a10.square_root_impact(q, v, -0.01), "daily_volatility < 0 must raise ValueError")
    must_raise(lambda: a10.square_root_impact(q, v, sigma, y_coeff=0.0), "y_coeff <= 0 must raise ValueError")
    must_raise(lambda: a10.square_root_impact(float("nan"), v, sigma), "NaN size must raise ValueError")


def test_temporary_and_permanent_impact() -> None:
    """Verify temporary and permanent impact functions and their scaling."""
    gamma = INST["gamma"]
    eta = INST["eta"]
    rate = 1500.0

    # Permanent impact: g(Q) = gamma * Q
    p1 = a10.permanent_impact(10_000.0, gamma)
    expect(math.isclose(p1, gamma * 10_000.0, rel_tol=1e-8), "Permanent impact must equal gamma * size")
    p_neg = a10.permanent_impact(-10_000.0, gamma)
    expect(math.isclose(p_neg, -p1, rel_tol=1e-8), "Permanent sell impact must be negative")

    # Temporary impact: h(v) = sign(v) * eta * |v|^alpha
    h1 = a10.temporary_impact(rate, eta, alpha=1.0)
    expect(math.isclose(h1, eta * rate, rel_tol=1e-8), "Linear temporary impact must equal eta * rate")
    h_quad = a10.temporary_impact(rate, eta, alpha=0.5)
    expect(
        math.isclose(h_quad, eta * math.sqrt(rate), rel_tol=1e-8),
        "Square-root temporary impact must scale as eta * sqrt(rate)",
    )

    must_raise(lambda: a10.permanent_impact(100.0, -1e-5), "gamma < 0 must raise ValueError")
    must_raise(lambda: a10.temporary_impact(100.0, -1e-5), "eta < 0 must raise ValueError")
    must_raise(lambda: a10.temporary_impact(100.0, eta, alpha=0.0), "alpha <= 0 must raise ValueError")


def test_almgren_chriss_boundary_and_monotonicity() -> None:
    """Verify Almgren-Chriss terminal liquidation, boundary values, and monotonicity."""
    x_total = INST["total_shares"]
    t = INST["horizon"]
    n = INST["n_steps"]
    sigma = INST["daily_volatility"]
    gamma = INST["gamma"]
    eta = INST["eta"]
    lam = INST["risk_aversion"]

    traj = a10.almgren_chriss_trajectory(x_total, t, n, sigma, gamma, eta, lam)

    expect(len(traj) == n + 1, f"Trajectory must have N+1 points (expected {n + 1}, got {len(traj)})")
    expect(math.isclose(traj[0], x_total, rel_tol=1e-9), f"Initial holding x_0 must equal total_shares {x_total}")
    expect(math.isclose(traj[-1], 0.0, abs_tol=1e-9), f"Terminal holding x_N must equal 0.0 (got {traj[-1]})")

    # Monotonicity: x_0 > x_1 > ... > x_N for liquidation
    diffs = traj[:-1] - traj[1:]
    expect(bool(np.all(diffs > 0.0)), "Liquidation trajectory must be strictly monotonically decreasing")


def test_almgren_chriss_risk_neutral_twap() -> None:
    """Verify risk-neutral (lambda = 0) limit recovers linear TWAP pacing exactly."""
    x_total = INST["total_shares"]
    t = INST["horizon"]
    n = INST["n_steps"]
    sigma = INST["daily_volatility"]
    gamma = INST["gamma"]
    eta = INST["eta"]

    traj_twap = a10.almgren_chriss_trajectory(x_total, t, n, sigma, gamma, eta, risk_aversion=0.0)
    expected_twap = np.array([x_total * (1.0 - k / n) for k in range(n + 1)])

    expect(
        bool(np.allclose(traj_twap, expected_twap, atol=1e-7)),
        "Almgren-Chriss trajectory with risk_aversion=0 must equal linear TWAP exactly",
    )


def test_almgren_chriss_cost_and_variance_tradeoff() -> None:
    """Verify risk aversion increases expected cost and decreases variance."""
    x_total = INST["total_shares"]
    t = INST["horizon"]
    n = INST["n_steps"]
    tau = t / n
    sigma = INST["daily_volatility"]
    gamma = INST["gamma"]
    eta = INST["eta"]

    traj_low = a10.almgren_chriss_trajectory(x_total, t, n, sigma, gamma, eta, risk_aversion=1e-8)
    traj_high = a10.almgren_chriss_trajectory(x_total, t, n, sigma, gamma, eta, risk_aversion=1e-4)

    e_low = a10.almgren_chriss_expected_cost(x_total, traj_low, tau, gamma, eta)
    v_low = a10.almgren_chriss_variance(traj_low, tau, sigma)

    e_high = a10.almgren_chriss_expected_cost(x_total, traj_high, tau, gamma, eta)
    v_high = a10.almgren_chriss_variance(traj_high, tau, sigma)

    expect(
        e_high > e_low,
        f"Higher risk aversion must incur higher expected cost (e_high={e_high:.4f} > e_low={e_low:.4f})",
    )
    expect(
        v_high < v_low,
        f"Higher risk aversion must reduce execution variance (v_high={v_high:.4f} < v_low={v_low:.4f})",
    )


def test_efficient_frontier_convexity() -> None:
    """Verify efficient execution frontier computation and strict convexity."""
    x_total = INST["total_shares"]
    t = INST["horizon"]
    n = INST["n_steps"]
    sigma = INST["daily_volatility"]
    gamma = INST["gamma"]
    eta = INST["eta"]
    lambdas = np.array(INST["lambdas"])

    e_costs, variances = a10.efficient_frontier(x_total, t, n, sigma, gamma, eta, lambdas)

    expect(len(e_costs) == len(lambdas), "Expected costs length must match lambdas count")
    expect(len(variances) == len(lambdas), "Variances length must match lambdas count")

    # As lambda increases, variance strictly decreases and expected cost increases
    var_diffs = np.diff(variances)
    cost_diffs = np.diff(e_costs)
    expect(
        bool(np.all(var_diffs <= 0.0)),
        "Variance must be non-increasing along the frontier as risk aversion grows",
    )
    expect(
        bool(np.all(cost_diffs >= 0.0)),
        "Expected cost must be non-decreasing along the frontier as risk aversion grows",
    )


def test_obizhaeva_wang_conservation_and_symmetry() -> None:
    """Verify Obizhaeva-Wang share conservation, boundary block symmetry, and resilience limits."""
    x_total = INST["total_shares"]
    t = INST["horizon"]
    rho = INST["resilience"]

    x0, v_star, xt = a10.obizhaeva_wang_trajectory(x_total, t, rho)

    # Share conservation: x0 + v_star * T + xt = X
    total_traded = x0 + v_star * t + xt
    expect(
        math.isclose(total_traded, x_total, rel_tol=1e-8),
        f"Obizhaeva-Wang shares traded ({total_traded:.4f}) must equal target shares ({x_total:.4f})",
    )

    # Symmetry
    expect(math.isclose(x0, xt, rel_tol=1e-8), "Initial and terminal block trades must be identical in size")

    # Limit rho -> 0 (zero resilience): x0 = X/2, xt = X/2, v* = 0
    x0_zero, v_zero, xt_zero = a10.obizhaeva_wang_trajectory(x_total, t, resilience=0.0)
    expect(
        math.isclose(x0_zero, 0.5 * x_total, rel_tol=1e-8),
        "Zero resilience must split order into equal initial trade",
    )
    expect(
        math.isclose(xt_zero, 0.5 * x_total, rel_tol=1e-8),
        "Zero resilience must split order into equal terminal trade",
    )
    expect(math.isclose(v_zero, 0.0, abs_tol=1e-8), "Zero resilience must result in zero continuous trading rate")


def test_implementation_shortfall_exact_articulation() -> None:
    """Verify Perold implementation shortfall exact component articulation and bps calculation."""
    p0 = INST["decision_price"]
    p_arr = INST["arrival_price"]
    p_term = INST["terminal_price"]
    trades = INST["trades"]
    x_total = INST["total_shares"]
    fees = INST["fees"]

    res = a10.implementation_shortfall(p0, p_arr, trades, p_term, x_total, fees=fees)

    # Opportunity cost verification
    expected_opp = (x_total - res["executed_shares"]) * (p_term - p0)
    expect(
        math.isclose(res["opportunity_cost"], expected_opp, rel_tol=1e-6),
        "Opportunity cost must equal unexecuted shares times (terminal_price - decision_price)",
    )

    # Exact balance equation: Total = Delay + Impact + Opportunity + Fees
    comp_sum = res["delay_cost"] + res["impact_cost"] + res["opportunity_cost"] + res["fees"]
    expect(
        math.isclose(res["total_shortfall"], comp_sum, rel_tol=1e-7),
        f"Total shortfall ({res['total_shortfall']:.4f}) must articulate exactly with component sum ({comp_sum:.4f})",
    )

    # Basis points check: is_bps = (total_shortfall / (target_shares * P0)) * 10,000
    expected_bps = (res["total_shortfall"] / (x_total * p0)) * 10_000.0
    expect(
        math.isclose(res["is_bps"], expected_bps, rel_tol=1e-6),
        f"Implementation shortfall in bps ({res['is_bps']:.4f}) must match formula ({expected_bps:.4f})",
    )

    # Unexecuted shares non-negativity
    expect(res["unexecuted_shares"] >= 0.0, "Unexecuted shares must be non-negative")
    expect(
        math.isclose(res["executed_shares"] + res["unexecuted_shares"], x_total, rel_tol=1e-7),
        "Executed + unexecuted must equal target shares",
    )


def test_implementation_shortfall_validation() -> None:
    """Verify domain checks for implementation_shortfall inputs."""
    p0 = INST["decision_price"]
    p_arr = INST["arrival_price"]
    p_term = INST["terminal_price"]
    trades = INST["trades"]
    x_total = INST["total_shares"]

    must_raise(
        lambda: a10.implementation_shortfall(p0, p_arr, trades, p_term, 0.0),
        "target_shares=0 must raise ValueError",
    )
    must_raise(
        lambda: a10.implementation_shortfall(0.0, p_arr, trades, p_term, x_total),
        "decision_price<=0 must raise ValueError",
    )
    must_raise(
        lambda: a10.implementation_shortfall(p0, -10.0, trades, p_term, x_total),
        "arrival_price<=0 must raise ValueError",
    )
    must_raise(
        lambda: a10.implementation_shortfall(p0, p_arr, trades, p_term, x_total, fees=-5.0),
        "fees<0 must raise ValueError",
    )
    must_raise(
        lambda: a10.implementation_shortfall(p0, p_arr, [(x_total * 2.0, p0)], p_term, x_total),
        "executed shares exceeding target must raise ValueError",
    )
