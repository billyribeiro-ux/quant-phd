"""Acceptance suite for the SC5 project: Lévy model calibration engine (levy_calibration.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your levy_calibration.py next to this file. Warnings are failures, as in the browser.

Each test checks mathematical properties, exact invariants, numerical bounds,
or contract-pinned recovery values. Failing tests name the property violated and provide a concept hint.
They never reveal expected private numerical values.
"""

from __future__ import annotations

import math
import os
from collections.abc import Callable, Iterator
from typing import Any

import levy_calibration as sol  # type: ignore[import-not-found]
import pytest
from instance import make_instance, make_surface  # type: ignore[import-not-found]

pytestmark = pytest.mark.filterwarnings("error")


@pytest.fixture(autouse=True)
def _no_stray_output(capsys: pytest.CaptureFixture[str]) -> Iterator[None]:
    """After every test, no output may have been printed by the engine."""
    yield
    expect(capsys.readouterr().out == "", "no function may print to stdout")


SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


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
# Instance properties
# ---------------------------------------------------------------------------


def test_make_instance_properties() -> None:
    """The instance generator must be deterministic, valid, and exhibit high parameter variance across seeds."""
    inst_a = make_instance(SEED)
    inst_b = make_instance(SEED)
    expect(inst_a == inst_b, "make_instance must be deterministic for the same seed")
    expect(inst_a["label"] == "SIMULATED", "instance must carry label SIMULATED")
    expect(inst_a["spot"] == 100.0, "spot price must be 100.0")
    expect(0.01 <= inst_a["r"] <= 0.06, "risk-free rate r must lie in [0.01, 0.06]")
    expect(len(inst_a["merton_prices"]) >= 10, "merton_prices must contain at least 10 option quotes")
    expect(len(inst_a["vg_prices"]) >= 10, "vg_prices must contain at least 10 option quotes")

    sigmas = {make_instance(s)["m_sigma"] for s in range(50)}
    expect(len(sigmas) >= 40, "seeds 0-49 must generate diverse parameters across instances")


# ---------------------------------------------------------------------------
# Characteristic function properties at u = 0 and u = -i (martingale condition)
# ---------------------------------------------------------------------------


def test_characteristic_function_at_zero() -> None:
    """At frequency u = 0, the characteristic function E[exp(i*0*ln S_t)] must equal 1 identically."""
    spot = INST["spot"]
    r = INST["r"]
    t = 0.5

    # Merton
    cf_m = sol.merton_characteristic_function(
        0.0, t, spot, r, INST["m_sigma"], INST["m_lam"], INST["m_mu_j"], INST["m_sigma_j"]
    )
    val_m = complex(cf_m)
    within(val_m.real, 1.0, 1e-7, "Merton CF real part at u=0 must equal 1.0 (total probability axiom)")
    within(val_m.imag, 0.0, 1e-7, "Merton CF imaginary part at u=0 must vanish")

    # Variance Gamma
    cf_vg = sol.vg_characteristic_function(
        0.0, t, spot, r, INST["vg_sigma"], INST["vg_nu"], INST["vg_theta"]
    )
    val_vg = complex(cf_vg)
    within(val_vg.real, 1.0, 1e-7, "VG CF real part at u=0 must equal 1.0 (total probability axiom)")
    within(val_vg.imag, 0.0, 1e-7, "VG CF imaginary part at u=0 must vanish")


def test_characteristic_function_martingale_condition() -> None:
    """At u = -i, E[exp(i*(-i)*ln S_t)] = E[S_t] must equal S_0 * exp(r*t) under the risk-neutral measure Q."""
    spot = INST["spot"]
    r = INST["r"]
    t = 0.5
    expected_forward = spot * math.exp(r * t)

    # Merton
    cf_m = sol.merton_characteristic_function(
        -1.0j, t, spot, r, INST["m_sigma"], INST["m_lam"], INST["m_mu_j"], INST["m_sigma_j"]
    )
    val_m = complex(cf_m)
    within(
        val_m.real,
        expected_forward,
        1e-4,
        "Merton CF at u=-i must equal forward price S_0*exp(r*t) (martingale condition)",
    )
    within(val_m.imag, 0.0, 1e-5, "Merton CF imaginary part at u=-i must vanish")

    # Variance Gamma
    cf_vg = sol.vg_characteristic_function(
        -1.0j, t, spot, r, INST["vg_sigma"], INST["vg_nu"], INST["vg_theta"]
    )
    val_vg = complex(cf_vg)
    within(
        val_vg.real,
        expected_forward,
        1e-4,
        "VG CF at u=-i must equal forward price S_0*exp(r*t) (martingale condition)",
    )
    within(val_vg.imag, 0.0, 1e-5, "VG CF imaginary part at u=-i must vanish")


def test_vg_admissibility_condition() -> None:
    """Variance Gamma requires 1 - theta*nu - 0.5*sigma^2*nu > 0; invalid parameters must raise ValueError."""
    spot = INST["spot"]
    r = INST["r"]
    must_raise(
        lambda: sol.vg_characteristic_function(1.0, 0.5, spot, r, sigma=0.5, nu=2.0, theta=1.5),
        "VG CF must reject parameters where 1 - theta*nu - 0.5*sigma^2*nu <= 0",
    )


# ---------------------------------------------------------------------------
# Option pricing and no-arbitrage invariants
# ---------------------------------------------------------------------------


def test_option_pricing_put_call_parity() -> None:
    """Option prices under Merton and VG must satisfy put-call parity: C - P = S_0 - K*exp(-r*tau)."""
    spot = INST["spot"]
    r = INST["r"]
    tau = 0.5
    strikes = [90.0, 100.0, 110.0]

    m_params = {
        "sigma": INST["m_sigma"],
        "lam": INST["m_lam"],
        "mu_j": INST["m_mu_j"],
        "sigma_j": INST["m_sigma_j"],
    }
    vg_params = {
        "sigma": INST["vg_sigma"],
        "nu": INST["vg_nu"],
        "theta": INST["vg_theta"],
    }

    for model, params in [("merton", m_params), ("vg", vg_params)]:
        for k in strikes:
            call = sol.price_european_option(spot, k, tau, r, model, params, is_call=True)
            put = sol.price_european_option(spot, k, tau, r, model, params, is_call=False)
            parity_target = spot - k * math.exp(-r * tau)
            within(
                call - put,
                parity_target,
                1e-3,
                f"Put-call parity violated for model {model} at strike {k}",
            )


def test_option_pricing_monotonicity_and_bounds() -> None:
    """European call prices must be strictly decreasing in strike and bounded below by intrinsic value."""
    spot = INST["spot"]
    r = INST["r"]
    tau = 0.5
    strikes = [90.0, 95.0, 100.0, 105.0, 110.0]

    m_params = {
        "sigma": INST["m_sigma"],
        "lam": INST["m_lam"],
        "mu_j": INST["m_mu_j"],
        "sigma_j": INST["m_sigma_j"],
    }
    vg_params = {
        "sigma": INST["vg_sigma"],
        "nu": INST["vg_nu"],
        "theta": INST["vg_theta"],
    }

    for model, params in [("merton", m_params), ("vg", vg_params)]:
        prices = [sol.price_european_option(spot, k, tau, r, model, params, is_call=True) for k in strikes]
        for i in range(len(prices) - 1):
            expect(
                prices[i] > prices[i + 1],
                f"Call price must be strictly decreasing in strike for {model}",
            )
        for k, p in zip(strikes, prices, strict=True):
            intrinsic = max(0.0, spot - k * math.exp(-r * tau))
            expect(p >= intrinsic - 1e-4, f"Call price below intrinsic lower bound for {model}")


# ---------------------------------------------------------------------------
# Implied volatility inversion
# ---------------------------------------------------------------------------


def test_implied_volatility_recovery() -> None:
    """The implied volatility solver must accurately invert known Black-Scholes prices and enforce no-arbitrage."""
    spot = 100.0
    r = 0.03
    tau = 0.5
    k = 100.0
    true_vol = 0.22

    # Black-Scholes call price at true_vol
    d1 = (math.log(spot / k) + (r + 0.5 * true_vol**2) * tau) / (true_vol * math.sqrt(tau))
    d2 = d1 - true_vol * math.sqrt(tau)
    cdf1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    cdf2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
    call_price = spot * cdf1 - k * math.exp(-r * tau) * cdf2

    recovered_vol = sol.implied_volatility(call_price, spot, k, tau, r, is_call=True)
    within(recovered_vol, true_vol, 1e-5, "Implied volatility solver must invert call price to within 1e-5")

    # Arbitrage bounds violation must raise ValueError
    must_raise(
        lambda: sol.implied_volatility(0.01, spot, 80.0, tau, r, is_call=True),
        "Implied volatility solver must reject prices below intrinsic value",
    )


# ---------------------------------------------------------------------------
# Calibration recovery
# ---------------------------------------------------------------------------


def test_merton_calibration_recovery() -> None:
    """Calibrating the Merton model to the SIMULATED instance surface must achieve low RMSE (< 0.02)."""
    spot = INST["spot"]
    r = INST["r"]
    market_surface = make_surface(INST, "merton")

    result = sol.calibrate_model(market_surface, "merton", spot, r)
    expect("params" in result, "Calibration result must contain 'params' dictionary")
    expect("rmse" in result, "Calibration result must contain 'rmse' value")
    expect(result["rmse"] < 0.02, f"Merton calibration RMSE must be below 0.02, got {result['rmse']}")

    calibrated_sigma = result["params"]["sigma"]
    expect(0.05 <= calibrated_sigma <= 0.40, "Calibrated Merton sigma must lie in reasonable domain")


def test_vg_calibration_recovery() -> None:
    """Calibrating the Variance Gamma model to the SIMULATED instance surface must achieve low RMSE (< 0.02)."""
    spot = INST["spot"]
    r = INST["r"]
    market_surface = make_surface(INST, "vg")

    result = sol.calibrate_model(market_surface, "vg", spot, r)
    expect("params" in result, "Calibration result must contain 'params' dictionary")
    expect("rmse" in result, "Calibration result must contain 'rmse' value")
    expect(result["rmse"] < 0.02, f"VG calibration RMSE must be below 0.02, got {result['rmse']}")

    calibrated_nu = result["params"]["nu"]
    expect(0.05 <= calibrated_nu <= 0.60, "Calibrated VG variance rate nu must lie in reasonable domain")
