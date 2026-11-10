"""Acceptance suite for DV2 project: Arbitrage-Free Surface Builder (surface_builder.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Each test verifies mathematical properties, exact invariants, asymptotic slope limits,
or contract-pinned calibration statistics. Failing tests name the property violated and provide
a concept hint. They never reveal the expected numerical value.
"""

from __future__ import annotations

import math
import os
from collections.abc import Callable, Iterator
from typing import Any

import pytest
import surface_builder as sol
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")


@pytest.fixture(autouse=True)
def _no_stray_output(capsys: pytest.CaptureFixture[str]) -> Iterator[None]:
    """After every test, no output may have been printed by the engine."""
    yield
    expect(capsys.readouterr().out == "", "no function may print to stdout")


SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def get_slice_params(i: int) -> dict[str, float]:
    return {
        "a": float(INST["svi_a"][i]),
        "b": float(INST["svi_b"][i]),
        "rho": float(INST["svi_rho"][i]),
        "m": float(INST["svi_m"][i]),
        "sigma": float(INST["svi_sigma"][i]),
    }


def get_slices() -> list[dict[str, Any]]:
    return [
        {
            "expiry": float(INST["expiries"][i]),
            "forward": float(INST["forwards"][i]),
            "params": get_slice_params(i),
        }
        for i in range(len(INST["expiries"]))
    ]


def get_market_chains() -> list[dict[str, Any]]:
    chains: list[dict[str, Any]] = []
    for i in range(len(INST["expiries"])):
        quotes: list[dict[str, float]] = []
        for j in range(len(INST["market_strikes"][i])):
            quotes.append(
                {
                    "strike": float(INST["market_strikes"][i][j]),
                    "log_moneyness": float(INST["market_log_moneyness"][i][j]),
                    "implied_vol": float(INST["market_implied_vol"][i][j]),
                    "total_variance": float(INST["market_total_variance"][i][j]),
                }
            )
        chains.append(
            {
                "expiry": float(INST["expiries"][i]),
                "forward": float(INST["forwards"][i]),
                "quotes": quotes,
            }
        )
    return chains


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
    # SVI total variance parameter bounds
    must_raise(lambda: sol.svi_total_variance(0.0, 0.04, -0.1, -0.3, 0.0, 0.1), "b < 0")
    must_raise(lambda: sol.svi_total_variance(0.0, 0.04, 0.1, 1.0, 0.0, 0.1), "rho >= 1")
    must_raise(lambda: sol.svi_total_variance(0.0, 0.04, 0.1, -1.05, 0.0, 0.1), "rho <= -1")
    must_raise(lambda: sol.svi_total_variance(0.0, 0.04, 0.1, -0.3, 0.0, 0.0), "sigma <= 0")
    must_raise(lambda: sol.svi_total_variance(0.0, -0.05, 0.1, 0.0, 0.0, 0.1), "negative min variance")

    # Calendar checks parameter bounds
    dummy_p = {"a": 0.04, "b": 0.1, "rho": -0.2, "m": 0.0, "sigma": 0.1}
    must_raise(lambda: sol.check_calendar_arbitrage([0.0], 0.5, dummy_p, 0.3, dummy_p), "t2 <= t1")
    must_raise(lambda: sol.check_calendar_arbitrage([], 0.2, dummy_p, 0.5, dummy_p), "empty k_grid")

    # Butterfly checks parameter bounds
    must_raise(lambda: sol.check_butterfly_arbitrage([], dummy_p), "empty k_grid")

    # Calibration bounds
    must_raise(lambda: sol.fit_svi_slice([0.0, 0.1], [0.04, 0.05]), "fewer than 5 observations")
    must_raise(lambda: sol.fit_svi_slice([0.0, 0.1, 0.2, 0.3, 0.4], [0.04, -0.01, 0.05, 0.06, 0.07]), "w <= 0")

    # Local volatility extraction bounds
    must_raise(lambda: sol.extract_local_volatility(0.0, 0.5, []), "empty slices")


def test_svi_total_variance_properties() -> None:
    """Check mathematical properties and exact values of SVI total variance."""
    p = get_slice_params(0)
    a, b, rho, m, sigma = p["a"], p["b"], p["rho"], p["m"], p["sigma"]

    # Minimum value at vertex k* = m - rho * sigma / sqrt(1 - rho^2)
    k_star = m - (rho * sigma) / math.sqrt(max(1e-6, 1.0 - rho**2))
    w_min_analytical = a + b * sigma * math.sqrt(max(0.0, 1.0 - rho**2))
    w_min_eval = sol.svi_total_variance(k_star, a, b, rho, m, sigma)

    expect(
        abs(w_min_eval - w_min_analytical) < 1e-6,
        "SVI minimum total variance formula must match evaluation at vertex",
    )
    expect(w_min_eval >= 0.0, "SVI total variance must be non-negative everywhere")

    # Value at k = m
    w_m = sol.svi_total_variance(m, a, b, rho, m, sigma)
    expect(abs(w_m - (a + b * sigma)) < 1e-9, "w(m) must equal a + b * sigma")


def test_svi_derivatives_consistency() -> None:
    """Verify analytical derivatives against central finite differences."""
    p = get_slice_params(1)
    a, b, rho, m, sigma = p["a"], p["b"], p["rho"], p["m"], p["sigma"]

    for k in [-0.5, -0.2, 0.0, 0.2, 0.5]:
        w, w_p, w_pp = sol.svi_derivatives(k, a, b, rho, m, sigma)
        h = 1e-5
        w_plus = sol.svi_total_variance(k + h, a, b, rho, m, sigma)
        w_minus = sol.svi_total_variance(k - h, a, b, rho, m, sigma)
        fd_p = (w_plus - w_minus) / (2.0 * h)
        fd_pp = (w_plus - 2.0 * w + w_minus) / (h**2)

        expect(abs(w_p - fd_p) < 1e-4, f"First derivative w' mismatch at k={k}")
        expect(abs(w_pp - fd_pp) < 1e-4, f"Second derivative w'' mismatch at k={k}")


def test_density_factor_and_butterfly_check() -> None:
    """Check Gatheral-Jacquier density factor g(k) and butterfly arbitrage detection."""
    p = get_slice_params(0)
    k_grid = INST["k_eval_grid"]

    # Verify exact analytical density factor formula at ATM
    w0, wp0, wpp0 = sol.svi_derivatives(0.0, p["a"], p["b"], p["rho"], p["m"], p["sigma"])
    g_expected = (1.0 - (0.0 * wp0) / (2.0 * w0)) ** 2 - (wp0**2 / 4.0) * (1.0 / w0 + 0.25) + 0.5 * wpp0
    g_actual = sol.svi_density_factor(0.0, p["a"], p["b"], p["rho"], p["m"], p["sigma"])
    expect(abs(g_actual - g_expected) < 1e-7, "Gatheral-Jacquier density factor must match exact formula")

    is_free, min_g = sol.check_butterfly_arbitrage(k_grid, p)
    expect(is_free, "Benchmark slice must be certified free of butterfly arbitrage")
    expect(min_g > 0.0, "Gatheral-Jacquier density factor g(k) must be strictly positive on benchmark")

    # Parameter set with butterfly arbitrage (large wing slope b and small sigma causing negative density)
    bad_p = {"a": 0.05, "b": 0.8, "rho": -0.7, "m": 0.0, "sigma": 0.01}
    is_bad_free, min_bad_g = sol.check_butterfly_arbitrage(k_grid, bad_p)
    expect(not is_bad_free, "Extreme curvature parameters with negative density must trigger butterfly arbitrage")
    expect(
        min_bad_g < 0.0,
        "Gatheral-Jacquier density factor g(k) must be strictly negative for butterfly arbitrage slice",
    )


def test_calendar_arbitrage_detection() -> None:
    """Check total variance monotonicity between consecutive maturities."""
    s1_t = float(INST["expiries"][0])
    s2_t = float(INST["expiries"][1])
    p1 = get_slice_params(0)
    p2 = get_slice_params(1)
    k_grid = INST["k_eval_grid"]

    is_free, min_diff = sol.check_calendar_arbitrage(k_grid, s1_t, p1, s2_t, p2)
    expect(is_free, "Consecutive benchmark slices must have w2(k) >= w1(k)")
    expect(min_diff > 0.0, "Calendar spread w2(k) - w1(k) must be strictly positive")

    # Inverted calendar slices (later expiry has strictly lower total variance)
    crossed_p2 = dict(p1)
    crossed_p2["a"] = max(0.001, p1["a"] - 0.005)
    is_cross_free, min_cross = sol.check_calendar_arbitrage(k_grid, s1_t, p1, s2_t, crossed_p2)
    expect(not is_cross_free, "Inverted calendar slices must be detected as calendar arbitrage")
    expect(min_cross < 0.0, "Calendar spread difference must be negative for crossing slices")


def test_svi_slice_calibration() -> None:
    """Verify SVI slice calibration to simulated market quotes."""
    k_data = [float(k) for k in INST["market_log_moneyness"][0]]
    w_data = [float(w) for w in INST["market_total_variance"][0]]

    fitted = sol.fit_svi_slice(k_data, w_data)
    expect("a" in fitted and "b" in fitted and "rho" in fitted, "Calibration output missing parameter keys")
    expect(fitted["b"] >= 0.0, "Calibrated wing slope b must be non-negative")
    expect(abs(fitted["rho"]) < 1.0, "Calibrated skew parameter rho must satisfy |rho| < 1")
    expect(fitted["sigma"] > 0.0, "Calibrated curvature sigma must be positive")
    expect(fitted["rmse"] < 0.025, f"Calibration RMSE {fitted['rmse']} exceeds 0.025 threshold")


def test_local_volatility_extraction() -> None:
    """Check Dupire local volatility extraction from SVI slices."""
    slices = get_slices()
    t_eval = float(slices[0]["expiry"])

    # Evaluate ATM local volatility
    loc_vol_atm = sol.extract_local_volatility(0.0, t_eval, slices)
    expect(loc_vol_atm > 0.0, "ATM local volatility must be strictly positive")
    expect(0.05 < loc_vol_atm < 1.0, f"ATM local volatility {loc_vol_atm} outside reasonable financial bounds")

    # Smile exaggeration: check that out-of-the-money put wing has higher local vol than ATM
    loc_vol_otm = sol.extract_local_volatility(-0.5, t_eval, slices)
    expect(
        loc_vol_otm > loc_vol_atm,
        "Negative equity skew must produce higher local vol in down-wing (smile exaggeration)",
    )


def test_asymptotic_wing_slopes() -> None:
    """Verify Lee's moment formula asymptotic slope bounds b * (1 + |rho|) <= 2."""
    for i in range(len(INST["expiries"])):
        p = get_slice_params(i)
        slope_bound = p["b"] * (1.0 + abs(p["rho"]))
        expect(slope_bound < 2.0, f"Asymptotic slope bound b*(1+|rho|) = {slope_bound} must be strictly less than 2")


def test_surface_builder_full_pipeline() -> None:
    """Run full end-to-end arbitrage-free surface builder pipeline."""
    chains = get_market_chains()
    result = sol.build_arbitrage_free_surface(chains, INST["k_eval_grid"])

    expect("calibrated_slices" in result, "Surface builder output missing calibrated_slices")
    expect("is_arbitrage_free" in result, "Surface builder output missing is_arbitrage_free flag")
    expect("local_vol_grid" in result, "Surface builder output missing local_vol_grid")
    expect(result["is_arbitrage_free"] is True, "Calibrated surface must be certified arbitrage-free")
    expect(result["min_density"] >= 0.0, "Surface minimum density factor must be non-negative")
    expect(result["min_calendar_spread"] >= 0.0, "Surface minimum calendar spread must be non-negative")
    expect(
        len(result["local_vol_grid"]) == len(INST["expiries"]) - 1,
        "Local vol grid row count must match expiries - 1",
    )
    expect(
        len(result["local_vol_grid"][0]) == len(INST["k_eval_grid"]),
        "Local vol grid col count must match k_eval_grid",
    )
