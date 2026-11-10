"""Acceptance suite for the DV1 project: Hedging-Error Study (hedging_simulator.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Each test verifies mathematical properties, exact invariants, asymptotic scaling laws,
or contract-pinned simulation statistics. Failing tests name the property violated and provide
a concept hint. They never reveal the expected numerical value.
"""

from __future__ import annotations

import math
import os
from collections.abc import Callable, Iterator
from typing import Any

import hedging_simulator as sol  # type: ignore[import-not-found]
import pytest
from instance import make_instance  # type: ignore[import-not-found]

pytestmark = pytest.mark.filterwarnings("error")


@pytest.fixture(autouse=True)
def _no_stray_output(capsys: pytest.CaptureFixture[str]) -> Iterator[None]:
    """After every test, no output may have been printed by the engine."""
    yield
    expect(capsys.readouterr().out == "", "no function may print to stdout")


SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
INST2: dict[str, Any] = make_instance(SEED + 7_919)


def expect(condition: bool, message: str) -> None:
    """Fail with message when condition is false."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(message)


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError, but none was raised.")


def test_input_validation() -> None:
    """Validate that invalid parameters raise ValueError."""
    must_raise(lambda: sol.bs_price(-10.0, 100.0, 0.05, 0.2, 1.0), "spot <= 0")
    must_raise(lambda: sol.bs_price(100.0, -10.0, 0.05, 0.2, 1.0), "strike <= 0")
    must_raise(lambda: sol.bs_price(100.0, 100.0, 0.05, -0.2, 1.0), "vol <= 0")
    must_raise(lambda: sol.bs_delta(-5.0, 100.0, 0.05, 0.2, 1.0), "delta spot <= 0")
    must_raise(lambda: sol.bs_gamma(100.0, 100.0, 0.05, -0.1, 1.0), "gamma vol <= 0")
    must_raise(lambda: sol.simulate_paths(100.0, 0.05, 0.2, 1.0, 0, 10, 1), "steps <= 0")
    must_raise(lambda: sol.delta_hedging_pnl([[100.0]], 100.0, 0.05, 0.2, 1.0), "path length < 2")
    must_raise(lambda: sol.delta_hedging_pnl([[100.0, 105.0]], 100.0, 0.05, 0.2, 1.0, -0.01), "cost_rate < 0")
    must_raise(lambda: sol.gamma_theta_attribution([100.0], 100.0, 0.05, 0.2, 1.0), "single point path")


def test_put_call_parity() -> None:
    """Check put-call parity C - P = S - K * exp(-r * T) across instances."""
    s = float(INST["spot"])
    k = float(INST["strike"])
    r = float(INST["rate"])
    v = float(INST["vol"])
    t = float(INST["maturity"])

    call = sol.bs_price(s, k, r, v, t, is_call=True)
    put = sol.bs_price(s, k, r, v, t, is_call=False)
    lhs = call - put
    rhs = s - k * math.exp(-r * t)
    expect(abs(lhs - rhs) < 1e-7, "put-call parity C - P = S - K*exp(-rT) must hold to 1e-7")


def test_greeks_invariants() -> None:
    """Check Delta bounds, Call-Put delta identity, and Gamma positivity."""
    s = float(INST["spot"])
    k = float(INST["strike"])
    r = float(INST["rate"])
    v = float(INST["vol"])
    t = float(INST["maturity"])

    c_delta = sol.bs_delta(s, k, r, v, t, is_call=True)
    p_delta = sol.bs_delta(s, k, r, v, t, is_call=False)
    gamma = sol.bs_gamma(s, k, r, v, t)

    expect(0.0 < c_delta < 1.0, "European call delta must lie strictly in (0, 1)")
    expect(-1.0 < p_delta < 0.0, "European put delta must lie strictly in (-1, 0)")
    expect(abs(c_delta - p_delta - 1.0) < 1e-7, "Call Delta - Put Delta must equal 1.0")
    expect(gamma > 0.0, "Option Gamma must be strictly positive")


def test_simulate_paths_properties() -> None:
    """Verify geometric Brownian motion path simulation invariants."""
    s = float(INST["spot"])
    r = float(INST["rate"])
    v = float(INST["vol"])
    t = float(INST["maturity"])
    steps = 20
    n_paths = 500

    paths = sol.simulate_paths(s, r, v, t, steps, n_paths, seed=SEED + 11)
    expect(len(paths) == n_paths, "number of generated paths must match n_paths")
    expect(all(len(p) == steps + 1 for p in paths), "each path length must equal steps + 1")
    expect(all(abs(p[0] - s) < 1e-12 for p in paths), "all paths must begin exactly at spot")
    expect(all(all(x > 0.0 for x in p) for p in paths), "asset price paths must remain strictly positive")

    # Martingale property of discounted stock price under Q: E[S_T] * exp(-r*T) ~= S_0
    term_vals = [p[-1] for p in paths]
    mean_term = sum(term_vals) / n_paths
    std_term = math.sqrt(sum((x - mean_term) ** 2 for x in term_vals) / (n_paths - 1))
    se_term = std_term / math.sqrt(n_paths)
    expected_mean = s * math.exp(r * t)
    expect(
        abs(mean_term - expected_mean) <= 4.0 * se_term,
        "sample mean of S_T under Q must equal S_0 * exp(r*T) within 4 standard errors",
    )


def test_frictionless_delta_hedging_unbiasedness() -> None:
    """Frictionless delta hedging of short option must be unbiased (mean tracking error ~= 0)."""
    s = float(INST["spot"])
    k = float(INST["strike"])
    r = float(INST["rate"])
    v = float(INST["vol"])
    t = float(INST["maturity"])
    steps = 52
    n_paths = 1000

    paths = sol.simulate_paths(s, r, v, t, steps, n_paths, seed=SEED + 29)
    out = sol.delta_hedging_pnl(paths, k, r, v, t, cost_rate=0.0, is_call=True)

    mean_pnl = float(out["mean_pnl"])
    std_pnl = float(out["std_pnl"])
    se_pnl = std_pnl / math.sqrt(n_paths)

    expect(
        abs(mean_pnl) <= 2.5 * se_pnl,
        "mean frictionless delta-hedged P&L must be centered at 0 within 2.5 standard errors",
    )
    expect(out["mean_costs"] == 0.0, "transaction costs must be zero when cost_rate = 0.0")


def test_asymptotic_hedging_error_scaling() -> None:
    """Hedging error standard deviation must decrease monotonically with rebalancing frequency."""
    s = float(INST["spot"])
    k = float(INST["strike"])
    r = float(INST["rate"])
    v = float(INST["vol"])
    t = float(INST["maturity"])
    step_list = [12, 52, 252]
    n_paths = 800

    results = sol.hedging_error_scaling(s, k, r, v, t, step_list, n_paths, seed=SEED + 53)
    std_12 = float(results["12"]["std_error"])
    std_52 = float(results["52"]["std_error"])
    std_252 = float(results["252"]["std_error"])

    expect(
        std_12 > std_52 > std_252,
        "hedging error standard deviation must decrease strictly monotonically with rebalancing frequency",
    )
    slope = float(results["slope"])
    expect(
        -0.75 <= slope <= -0.25,
        "log-log scaling slope must be close to theoretical -0.50 (between -0.75 and -0.25)",
    )


def test_transaction_costs_impact() -> None:
    """Proportional transaction costs must reduce mean net P&L and incur strictly positive costs."""
    s = float(INST["spot"])
    k = float(INST["strike"])
    r = float(INST["rate"])
    v = float(INST["vol"])
    t = float(INST["maturity"])
    cost_rate = float(INST["cost_rate"])
    steps = 52
    n_paths = 600

    paths = sol.simulate_paths(s, r, v, t, steps, n_paths, seed=SEED + 97)
    out_zero = sol.delta_hedging_pnl(paths, k, r, v, t, cost_rate=0.0, is_call=True)
    out_cost = sol.delta_hedging_pnl(paths, k, r, v, t, cost_rate=cost_rate, is_call=True)

    mean_zero = float(out_zero["mean_pnl"])
    mean_cost = float(out_cost["mean_pnl"])
    costs = float(out_cost["mean_costs"])

    expect(costs > 0.0, "total transaction costs must be strictly positive when cost_rate > 0")
    expect(mean_cost < mean_zero, "net P&L under transaction costs must be strictly lower than frictionless P&L")


def test_gamma_theta_attribution_identity() -> None:
    """Single-path Gamma-Theta expansion must closely approximate actual hedged P&L."""
    s = float(INST["spot"])
    k = float(INST["strike"])
    r = float(INST["rate"])
    v = float(INST["vol"])
    t = float(INST["maturity"])

    paths = sol.simulate_paths(s, r, v, t, steps=200, n_paths=1, seed=SEED + 101)
    path = paths[0]

    attr = sol.gamma_theta_attribution(path, k, r, v, t, is_call=True)
    actual = attr["actual_hedged_pnl"]
    taylor = attr["taylor_pnl"]
    disc = attr["discrepancy"]

    expect(
        abs(disc) <= 0.25,
        "discrepancy between actual hedged P&L and Taylor (Gamma+Theta) attribution must be <= 0.25 on fine grid",
    )
    expect(
        abs(actual - taylor) < 1e-12 or abs(disc) == abs(actual - taylor),
        "discrepancy must equal actual_hedged_pnl - taylor_pnl",
    )


def test_second_instance_diversity() -> None:
    """Check that pricing on INST2 produces valid non-trivial results."""
    s = float(INST2["spot"])
    k = float(INST2["strike"])
    r = float(INST2["rate"])
    v = float(INST2["vol"])
    t = float(INST2["maturity"])

    price = sol.bs_price(s, k, r, v, t, is_call=True)
    delta = sol.bs_delta(s, k, r, v, t, is_call=True)
    gamma = sol.bs_gamma(s, k, r, v, t)

    expect(price > 0.0, "call price on INST2 must be positive")
    expect(0.0 < delta < 1.0, "call delta on INST2 must be in (0, 1)")
    expect(gamma > 0.0, "gamma on INST2 must be positive")
