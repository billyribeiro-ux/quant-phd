"""Acceptance suite for the SC3 project: Numeraire Toolkit (numeraire_toolkit.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your numeraire_toolkit.py next to this file. Warnings are failures, as in the browser.

Each test verifies mathematical properties, exact invariants, numeraire transformations,
or contract-pinned simulation values. Failing tests name the property violated and provide a concept hint.
They never reveal the expected numerical value.
"""

from __future__ import annotations

import math
import os
from collections.abc import Callable, Iterator
from typing import Any

import numeraire_toolkit as sol  # type: ignore[import-not-found]
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
    """Fail with message when condition is false. The message never displays expected values."""
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


def within(value: float, target: float, tolerance: float, message: str) -> None:
    """Fail unless |value - target| is at most the tolerance."""
    __tracebackhide__ = True
    expect(abs(value - target) <= tolerance, message)


# ---------------------------------------------------------------------------
# 1. Instance generator validation
# ---------------------------------------------------------------------------


def test_make_instance_properties() -> None:
    """The instance generator must be deterministic, valid, and exhibit high variance across seeds."""
    inst_a = make_instance(SEED)
    inst_b = make_instance(SEED)
    expect(inst_a == inst_b, "make_instance must be deterministic for identical seeds")

    inst_diff = make_instance(SEED + 1)
    expect(inst_a != inst_diff, "make_instance must generate distinct instances across distinct seeds")

    expect(inst_a["s1"] > 0.0 and inst_a["s2"] > 0.0, "asset prices must be positive")
    expect(inst_a["sig1"] > 0.0 and inst_a["sig2"] > 0.0, "volatilities must be positive")
    expect(-1.0 <= inst_a["rho"] <= 1.0, "correlation must be within [-1, 1]")
    expect(inst_a["t"] > 0.0, "maturity must be positive")


# ---------------------------------------------------------------------------
# 2. Margrabe mathematical invariants
# ---------------------------------------------------------------------------


def test_margrabe_homogeneity() -> None:
    """Margrabe price must be linearly homogeneous of degree 1: V(c*S1, c*S2) = c*V(S1, S2)."""
    s1, s2 = float(INST["s1"]), float(INST["s2"])
    sig1, sig2 = float(INST["sig1"]), float(INST["sig2"])
    rho = float(INST["rho"])
    q1, q2 = float(INST["q1"]), float(INST["q2"])
    t = float(INST["t"])

    base_price = sol.margrabe_price(s1, s2, sig1, sig2, rho, q1, q2, t)
    expect(base_price >= 0.0, "option price must be non-negative")

    for scale in [0.5, 1.5, 3.0]:
        scaled_price = sol.margrabe_price(scale * s1, scale * s2, sig1, sig2, rho, q1, q2, t)
        within(
            scaled_price,
            scale * base_price,
            1e-8,
            f"Margrabe price violates homogeneity of degree 1 at scale {scale}",
        )


def test_margrabe_exchange_parity() -> None:
    """Put-call exchange parity: Call(S1, S2) - Call(S2, S1) = S1*exp(-q1*T) - S2*exp(-q2*T)."""
    s1, s2 = float(INST["s1"]), float(INST["s2"])
    sig1, sig2 = float(INST["sig1"]), float(INST["sig2"])
    rho = float(INST["rho"])
    q1, q2 = float(INST["q1"]), float(INST["q2"])
    t = float(INST["t"])

    call_12 = sol.margrabe_price(s1, s2, sig1, sig2, rho, q1, q2, t)
    call_21 = sol.margrabe_price(s2, s1, sig2, sig1, rho, q2, q1, t)

    forward_diff = s1 * math.exp(-q1 * t) - s2 * math.exp(-q2 * t)
    within(
        call_12 - call_21,
        forward_diff,
        1e-8,
        "Margrabe price violates put-call exchange symmetry parity Call(S1, S2) - Call(S2, S1) = F1 - F2",
    )


def test_margrabe_correlation_monotonicity() -> None:
    """Margrabe option value is strictly decreasing in correlation rho."""
    s1, s2 = float(INST["s1"]), float(INST["s2"])
    sig1, sig2 = float(INST["sig1"]), float(INST["sig2"])
    q1, q2 = float(INST["q1"]), float(INST["q2"])
    t = float(INST["t"])

    price_low_rho = sol.margrabe_price(s1, s2, sig1, sig2, -0.80, q1, q2, t)
    price_mid_rho = sol.margrabe_price(s1, s2, sig1, sig2, 0.00, q1, q2, t)
    price_high_rho = sol.margrabe_price(s1, s2, sig1, sig2, 0.80, q1, q2, t)

    expect(
        price_low_rho > price_mid_rho > price_high_rho,
        "Margrabe option price must be strictly decreasing in correlation rho",
    )


def test_margrabe_mc_concordance() -> None:
    """Closed-form Margrabe price must match 2D Monte Carlo within statistical error."""
    s1, s2 = float(INST["s1"]), float(INST["s2"])
    sig1, sig2 = float(INST["sig1"]), float(INST["sig2"])
    rho = float(INST["rho"])
    q1, q2 = float(INST["q1"]), float(INST["q2"])
    t = float(INST["t"])
    r = float(INST["r"])
    n_paths = 3000
    seed = int(INST["seed"])

    closed = sol.margrabe_price(s1, s2, sig1, sig2, rho, q1, q2, t)
    mc_val, mc_se = sol.margrabe_mc(s1, s2, sig1, sig2, rho, q1, q2, t, r, n_paths, seed)

    expect(mc_se > 0.0, "Monte Carlo standard error must be strictly positive")
    within(
        mc_val,
        closed,
        4.0 * mc_se + 0.05,
        "Margrabe closed-form price differs from 2D Monte Carlo estimate beyond 4 standard errors",
    )


# ---------------------------------------------------------------------------
# 3. Quanto European call mathematical properties
# ---------------------------------------------------------------------------


def test_quanto_correlation_sensitivity() -> None:
    """A positive correlation between foreign asset and FX rate reduces the domestic quanto drift."""
    s_f = float(INST["s_f"])
    k_quanto = float(INST["k_quanto"])
    r_d = float(INST["r_d"])
    r_f = float(INST["r_f"])
    sig_s = float(INST["sig_s"])
    sig_x = float(INST["sig_x"])
    t = float(INST["t"])

    price_pos_rho = sol.quanto_call_price(s_f, k_quanto, r_d, r_f, sig_s, sig_x, 0.50, t)
    price_zero_rho = sol.quanto_call_price(s_f, k_quanto, r_d, r_f, sig_s, sig_x, 0.00, t)
    price_neg_rho = sol.quanto_call_price(s_f, k_quanto, r_d, r_f, sig_s, sig_x, -0.50, t)

    expect(
        price_neg_rho > price_zero_rho > price_pos_rho,
        "Quanto call price must decrease with positive correlation rho_SX due to negative drift adjustment",
    )


def test_quanto_mc_concordance() -> None:
    """Closed-form quanto call price must match domestic Monte Carlo within statistical error."""
    s_f = float(INST["s_f"])
    x0 = float(INST["x0"])
    k_quanto = float(INST["k_quanto"])
    r_d = float(INST["r_d"])
    r_f = float(INST["r_f"])
    sig_s = float(INST["sig_s"])
    sig_x = float(INST["sig_x"])
    rho_sx = float(INST["rho_sx"])
    t = float(INST["t"])
    n_paths = 3000
    seed = int(INST["seed"])

    closed = sol.quanto_call_price(s_f, k_quanto, r_d, r_f, sig_s, sig_x, rho_sx, t)
    mc_val, mc_se = sol.quanto_call_mc(s_f, x0, k_quanto, r_d, r_f, sig_s, sig_x, rho_sx, t, n_paths, seed)

    expect(mc_se > 0.0, "Quanto Monte Carlo standard error must be positive")
    within(
        mc_val,
        closed,
        4.0 * mc_se + 0.05,
        "Quanto closed-form price differs from domestic Monte Carlo estimate beyond 4 standard errors",
    )


def test_verify_invariance_function() -> None:
    """verify_invariance must evaluate successfully and return valid concordance flags."""
    res = sol.verify_invariance(INST)
    expect(isinstance(res, dict), "verify_invariance must return a dictionary")
    expect(res.get("status") == "PASS", "verify_invariance status must be PASS")
    expect(res.get("homogeneity_valid") is True, "homogeneity_valid flag must be True")
    expect(res.get("parity_valid") is True, "parity_valid flag must be True")


# ---------------------------------------------------------------------------
# 4. Input validation and error handling
# ---------------------------------------------------------------------------


def test_input_validation() -> None:
    """Functions must raise ValueError on non-positive prices, volatilities, or invalid correlations."""
    must_raise(
        lambda: sol.margrabe_price(-10.0, 100.0, 0.2, 0.2, 0.0, 0.0, 0.0, 1.0),
        "negative price S1 in margrabe_price",
    )
    must_raise(
        lambda: sol.margrabe_price(100.0, 100.0, -0.2, 0.2, 0.0, 0.0, 0.0, 1.0),
        "negative volatility sig1 in margrabe_price",
    )
    must_raise(
        lambda: sol.margrabe_price(100.0, 100.0, 0.2, 0.2, 1.5, 0.0, 0.0, 1.0),
        "correlation rho > 1 in margrabe_price",
    )
    must_raise(
        lambda: sol.quanto_call_price(-10.0, 100.0, 0.05, 0.02, 0.2, 0.1, 0.0, 1.0),
        "negative price S_f in quanto_call_price",
    )
    must_raise(
        lambda: sol.quanto_call_price(100.0, 100.0, 0.05, 0.02, 0.2, 0.1, -1.2, 1.0),
        "correlation rho < -1 in quanto_call_price",
    )
