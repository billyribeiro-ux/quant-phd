"""Acceptance suite for Atlas milestone A6: Numerical Pricing Library (atlas.pricing).

Runs identically in the browser (Pyodide) and locally:
    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Each test checks mathematical invariants, no-arbitrage bounds, early-exercise conditions,
asymptotic convergence, and cross-method consistency.
"""

from __future__ import annotations

import math
import os
from collections.abc import Callable, Iterator
from typing import Any

import pytest
from atlas import pricing as sol  # type: ignore[attr-defined]
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")


@pytest.fixture(autouse=True)
def _no_stray_output(capsys: pytest.CaptureFixture[str]) -> Iterator[None]:
    """Ensure no pricing routine prints stray text to stdout."""
    yield
    captured = capsys.readouterr()
    expect(captured.out == "", "Pricing engine must not print to stdout")


SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


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
    pytest.fail(f"{condition}: expected ValueError, but none was raised.")


def test_input_validation() -> None:
    """Verify that invalid inputs raise ValueError across all pricers."""
    must_raise(lambda: sol.bsm_price(-100.0, 100.0, 0.05, 0.20, 1.0), "spot <= 0")
    must_raise(lambda: sol.bsm_price(100.0, -100.0, 0.05, 0.20, 1.0), "strike <= 0")
    must_raise(lambda: sol.bsm_price(100.0, 100.0, 0.05, -0.20, 1.0), "vol <= 0")
    must_raise(lambda: sol.bsm_price(100.0, 100.0, 0.05, 0.20, -1.0), "maturity <= 0")
    must_raise(lambda: sol.bsm_price(100.0, 100.0, 0.05, 0.20, 1.0, dividend_yield=-0.01), "dividend_yield < 0")

    must_raise(lambda: sol.binomial_tree_price(100.0, 100.0, 0.05, 0.20, 1.0, n_steps=0), "binomial n_steps <= 0")
    must_raise(lambda: sol.trinomial_tree_price(100.0, 100.0, 0.05, 0.20, 1.0, n_steps=1), "trinomial n_steps < 2")

    must_raise(lambda: sol.pde_price(100.0, 100.0, 0.05, 0.20, 1.0, n_time_steps=0), "pde n_time_steps <= 0")
    must_raise(lambda: sol.pde_price(100.0, 100.0, 0.05, 0.20, 1.0, n_spot_steps=2), "pde n_spot_steps < 3")
    must_raise(lambda: sol.pde_price(100.0, 100.0, 0.05, 0.20, 1.0, scheme="unknown"), "invalid pde scheme")

    must_raise(lambda: sol.monte_carlo_price(100.0, 100.0, 0.05, 0.20, 1.0, n_paths=0), "mc n_paths <= 0")
    must_raise(lambda: sol.lsmc_price(100.0, 100.0, 0.05, 0.20, 1.0, degree=0), "lsmc degree < 1")
    must_raise(lambda: sol.lsmc_price(100.0, 100.0, 0.05, 0.20, 1.0, basis="spline"), "invalid lsmc basis")
    must_raise(
        lambda: sol.cross_method_consistency_check(100.0, 100.0, 0.05, 0.20, 1.0, tolerance=-0.01), "tolerance <= 0"
    )


def test_bsm_analytical_put_call_parity() -> None:
    """Verify exact European put-call parity: C - P = S * exp(-qT) - K * exp(-rT)."""
    s = float(INST["spot"])
    k = float(INST["strike"])
    r = float(INST["rate"])
    v = float(INST["vol"])
    t = float(INST["maturity"])
    q = float(INST["dividend_yield"])

    call = sol.bsm_price(s, k, r, v, t, is_call=True, dividend_yield=q)
    put = sol.bsm_price(s, k, r, v, t, is_call=False, dividend_yield=q)

    lhs = call.price - put.price
    rhs = s * math.exp(-q * t) - k * math.exp(-r * t)
    expect(abs(lhs - rhs) < 1e-10, f"BSM put-call parity discrepancy: {abs(lhs - rhs)}")


def test_lattice_put_call_parity() -> None:
    """Verify European put-call parity on binomial and trinomial lattices."""
    s = float(INST["spot"])
    k = float(INST["strike"])
    r = float(INST["rate"])
    v = float(INST["vol"])
    t = float(INST["maturity"])

    bin_c = sol.binomial_tree_price(s, k, r, v, t, n_steps=100, is_call=True, is_american=False)
    bin_p = sol.binomial_tree_price(s, k, r, v, t, n_steps=100, is_call=False, is_american=False)
    rhs = s - k * math.exp(-r * t)
    expect(abs((bin_c.price - bin_p.price) - rhs) < 0.06, "Binomial European parity violated")

    tri_c = sol.trinomial_tree_price(s, k, r, v, t, n_steps=80, is_call=True, is_american=False)
    tri_p = sol.trinomial_tree_price(s, k, r, v, t, n_steps=80, is_call=False, is_american=False)
    expect(abs((tri_c.price - tri_p.price) - rhs) < 0.04, "Trinomial European parity violated")


def test_american_early_exercise_premium() -> None:
    """Verify American put premium and call early exercise properties."""
    s = float(INST["american_spot"])
    k = float(INST["american_strike"])
    r = float(INST["american_rate"])
    v = float(INST["american_vol"])
    t = float(INST["american_maturity"])

    eur_put = sol.bsm_price(s, k, r, v, t, is_call=False)
    bin_amer_put = sol.binomial_tree_price(s, k, r, v, t, n_steps=120, is_call=False, is_american=True)
    tri_amer_put = sol.trinomial_tree_price(s, k, r, v, t, n_steps=100, is_call=False, is_american=True)
    pde_amer_put = sol.pde_price(s, k, r, v, t, n_time_steps=60, n_spot_steps=70, is_call=False, is_american=True)

    intrinsic = max(k - s, 0.0)
    expect(bin_amer_put.price >= intrinsic - 1e-4, "American put must exceed intrinsic value")
    expect(tri_amer_put.price >= intrinsic - 1e-4, "American trinomial put must exceed intrinsic value")
    expect(pde_amer_put.price >= intrinsic - 1e-4, "American PDE put must exceed intrinsic value")
    expect(bin_amer_put.price > eur_put.price, "American put must exceed European put for r > 0")

    eur_call = sol.bsm_price(s, k, r, v, t, is_call=True, dividend_yield=0.0)
    amer_call = sol.binomial_tree_price(s, k, r, v, t, n_steps=100, is_call=True, is_american=True, dividend_yield=0.0)
    expect(abs(amer_call.price - eur_call.price) < 0.08, "American call without dividends must equal European call")


def test_pde_schemes_agreement() -> None:
    """Verify Crank-Nicolson and Implicit schemes converge to analytical BSM."""
    s = float(INST["spot"])
    k = float(INST["strike"])
    r = float(INST["rate"])
    v = float(INST["vol"])
    t = float(INST["maturity"])

    bsm = sol.bsm_price(s, k, r, v, t, is_call=True)
    pde_cn = sol.pde_price(s, k, r, v, t, n_time_steps=60, n_spot_steps=70, is_call=True, scheme="crank_nicolson")
    pde_imp = sol.pde_price(s, k, r, v, t, n_time_steps=60, n_spot_steps=70, is_call=True, scheme="implicit")

    expect(abs(pde_cn.price - bsm.price) < 0.15, f"Crank-Nicolson PDE error too large: {abs(pde_cn.price - bsm.price)}")
    expect(abs(pde_imp.price - bsm.price) < 0.25, f"Implicit PDE error too large: {abs(pde_imp.price - bsm.price)}")


def test_greeks_numerical_consistency() -> None:
    """Verify analytical BSM Greeks match numerical finite-difference bumps."""
    s = float(INST["spot"])
    k = float(INST["strike"])
    r = float(INST["rate"])
    v = float(INST["vol"])
    t = float(INST["maturity"])

    base = sol.bsm_price(s, k, r, v, t, is_call=True)

    ds = 0.001 * s
    p_up = sol.bsm_price(s + ds, k, r, v, t, is_call=True).price
    p_dn = sol.bsm_price(s - ds, k, r, v, t, is_call=True).price

    num_delta = (p_up - p_dn) / (2.0 * ds)
    num_gamma = (p_up - 2.0 * base.price + p_dn) / (ds * ds)
    expect(abs(base.delta - num_delta) < 1e-4, "Analytical Delta diverges from central difference")
    expect(abs(base.gamma - num_gamma) < 1e-3, "Analytical Gamma diverges from central difference")

    dv = 0.0005
    p_v_up = sol.bsm_price(s, k, r, v + dv, t, is_call=True).price
    p_v_dn = sol.bsm_price(s, k, r, v - dv, t, is_call=True).price
    num_vega = (p_v_up - p_v_dn) / (2.0 * dv)
    expect(abs(base.vega - num_vega) < 1e-3, "Analytical Vega diverges from numerical bump")


def test_monte_carlo_european_confidence() -> None:
    """Verify Monte Carlo price falls within 3 standard errors of analytical BSM."""
    s = float(INST["spot"])
    k = float(INST["strike"])
    r = float(INST["rate"])
    v = float(INST["vol"])
    t = float(INST["maturity"])

    bsm = sol.bsm_price(s, k, r, v, t, is_call=True)
    mc = sol.monte_carlo_price(s, k, r, v, t, n_paths=15_000, seed=INST["seed"], antithetic=True)

    expect(mc.se is not None and mc.se > 0.0, "Monte Carlo must report positive standard error")
    assert mc.se is not None
    z_score = abs(mc.price - bsm.price) / mc.se
    expect(z_score < 3.5, f"Monte Carlo estimate diverges beyond 3.5 SE: z={z_score:.2f}")


def test_longstaff_schwartz_american_pricing() -> None:
    """Verify Longstaff-Schwartz LSMC prices American put and respects early exercise."""
    s = float(INST["american_spot"])
    k = float(INST["american_strike"])
    r = float(INST["american_rate"])
    v = float(INST["american_vol"])
    t = float(INST["american_maturity"])

    lsmc_res = sol.lsmc_price(
        s, k, r, v, t, n_paths=4000, n_steps=25, degree=3, is_call=False, seed=INST["seed"], basis="laguerre"
    )
    eur_bsm = sol.bsm_price(s, k, r, v, t, is_call=False)
    tri_amer = sol.trinomial_tree_price(s, k, r, v, t, n_steps=80, is_call=False, is_american=True)

    expect(lsmc_res.price >= max(k - s, 0.0) - 0.05, "LSMC price must satisfy intrinsic lower bound")
    expect(lsmc_res.price > eur_bsm.price - 0.05, "LSMC American put should exceed European BSM put")
    expect(abs(lsmc_res.price - tri_amer.price) < 0.60, "LSMC price should closely approximate American tree")


def test_cross_method_consistency() -> None:
    """Verify all 5 pricing methodologies agree within theoretical consistency bounds."""
    s = float(INST["spot"])
    k = float(INST["strike"])
    r = float(INST["rate"])
    v = float(INST["vol"])
    t = float(INST["maturity"])

    report = sol.cross_method_consistency_check(s, k, r, v, t, is_call=True, tolerance=0.06)
    expect(bool(report["consistent"]), f"Cross method inconsistency: max error {report['max_abs_error']:.4f}")
