"""Acceptance test suite for PM1: Private Equity (PME Engine).

Runs identically in native pytest and in-browser Pyodide:
    pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import math
import os
from typing import Any

import numpy as np
import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]
from reference import (  # type: ignore[import-not-found, unused-ignore]
    compute_direct_alpha,
    compute_irr,
    compute_ks_pme,
    compute_long_nickels_pme,
    compute_moic,
    evaluate_fund,
)

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


# ============================================================================
# 1. Instance Structure and Determinism
# ============================================================================


def test_instance_structure() -> None:
    required_keys = {"seed", "times", "calls", "distributions", "nav", "benchmark_prices", "true_alpha", "beta"}
    assert required_keys.issubset(INST.keys()), f"Missing keys in instance: {required_keys - set(INST.keys())}"

    times = np.asarray(INST["times"], dtype=np.float64)
    calls = np.asarray(INST["calls"], dtype=np.float64)
    dist = np.asarray(INST["distributions"], dtype=np.float64)
    prices = np.asarray(INST["benchmark_prices"], dtype=np.float64)

    assert len(times) == 21, f"Expected 21 time points, got {len(times)}"
    assert len(calls) == 21, "Calls length mismatch"
    assert len(dist) == 21, "Distributions length mismatch"
    assert len(prices) == 21, "Benchmark prices length mismatch"
    assert np.all(prices > 0.0), "Benchmark prices must be strictly positive"
    assert np.all(calls >= 0.0), "Calls must be non-negative"
    assert np.all(dist >= 0.0), "Distributions must be non-negative"
    assert INST["nav"] >= 0.0, "NAV must be non-negative"


# ============================================================================
# 2. MOIC Articulation and Invariants
# ============================================================================


def test_moic_articulation() -> None:
    calls = np.asarray(INST["calls"], dtype=np.float64)
    dist = np.asarray(INST["distributions"], dtype=np.float64)
    nav = float(INST["nav"])

    dpi, rvpi, tvpi = compute_moic(calls, dist, nav)

    assert dpi >= 0.0, f"DPI must be non-negative, got {dpi}"
    assert rvpi >= 0.0, f"RVPI must be non-negative, got {rvpi}"
    assert tvpi > 0.0, f"TVPI must be strictly positive, got {tvpi}"
    assert abs(tvpi - (dpi + rvpi)) < 1e-9, f"TVPI articulation failure: {tvpi} != {dpi} + {rvpi}"

    # Explicit check with non-zero NAV: TVPI must include RVPI
    d_test, r_test, t_test = compute_moic(np.array([100.0]), np.array([40.0]), 80.0)
    assert abs(d_test - 0.40) < 1e-9
    assert abs(r_test - 0.80) < 1e-9
    assert abs(t_test - 1.20) < 1e-9, f"TVPI must be 1.20, got {t_test}"

    # Verify zero calls edge case
    assert compute_moic(np.zeros(5), np.ones(5), 10.0) == (0.0, 0.0, 0.0)


# ============================================================================
# 3. IRR Root Finding and Scale Invariance
# ============================================================================


def test_irr_properties() -> None:
    times = np.asarray(INST["times"], dtype=np.float64)
    calls = np.asarray(INST["calls"], dtype=np.float64)
    dist = np.asarray(INST["distributions"], dtype=np.float64)
    nav = float(INST["nav"])

    cf = dist - calls
    cf[-1] += nav

    irr = compute_irr(times, cf)
    assert np.isfinite(irr), f"IRR is non-finite: {irr}"
    assert -0.80 < irr < 5.0, f"IRR {irr} outside plausible economic bounds"

    # Invariant 1: NPV at IRR must be zero
    npv_at_irr = float(np.sum(cf * (1.0 + irr) ** (-times)))
    assert abs(npv_at_irr) < 1e-4, f"NPV at IRR is non-zero: {npv_at_irr}"

    # Invariant 2: Scale invariance (multiplying cash flows by positive constant preserves IRR)
    irr_scaled = compute_irr(times, cf * 3.75)
    assert abs(irr - irr_scaled) < 1e-6, f"IRR not scale-invariant: {irr} vs {irr_scaled}"


# ============================================================================
# 4. Kaplan & Schoar (2005) KS-PME Benchmarking
# ============================================================================


def test_ks_pme_properties() -> None:
    times = np.asarray(INST["times"], dtype=np.float64)
    calls = np.asarray(INST["calls"], dtype=np.float64)
    dist = np.asarray(INST["distributions"], dtype=np.float64)
    nav = float(INST["nav"])
    prices = np.asarray(INST["benchmark_prices"], dtype=np.float64)

    ks_pme = compute_ks_pme(times, calls, dist, nav, prices)
    assert np.isfinite(ks_pme), f"KS-PME is non-finite: {ks_pme}"
    assert ks_pme > 0.0, f"KS-PME must be positive, got {ks_pme}"

    # Invariant: NAV must be discounted by terminal benchmark price
    # Call 100 at t=0, price=100. Terminal NAV 200 at t=1, price=200.
    # KS-PME must be (200 / 200) / (100 / 100) = 1.0, not 200 / 1.0 = 200.0!
    pme_nav = compute_ks_pme(
        np.array([0.0, 1.0]), np.array([100.0, 0.0]), np.array([0.0, 0.0]), 200.0, np.array([100.0, 200.0])
    )
    assert abs(pme_nav - 1.0) < 1e-6, f"Terminal NAV must be discounted by benchmark price: got {pme_nav}"

    # Invariant: If fund perfectly matches benchmark index returns, KS-PME == 1.0
    # Create synthetic benchmark-matching distributions:
    # Each call at time t_i grows exactly to calls[i] * (prices[-1] / prices[i]) at termination
    perfect_dist = np.zeros_like(dist)
    perfect_dist[-1] = float(np.sum(calls * (prices[-1] / prices)))
    pme_perfect = compute_ks_pme(times, calls, perfect_dist, 0.0, prices)
    assert abs(pme_perfect - 1.0) < 1e-6, f"Benchmark-matching fund must have KS-PME = 1.0, got {pme_perfect}"


# ============================================================================
# 5. Direct Alpha (Gredil, Griffiths & Stucke 2014) Properties
# ============================================================================


def test_direct_alpha_properties() -> None:
    times = np.asarray(INST["times"], dtype=np.float64)
    calls = np.asarray(INST["calls"], dtype=np.float64)
    dist = np.asarray(INST["distributions"], dtype=np.float64)
    nav = float(INST["nav"])
    prices = np.asarray(INST["benchmark_prices"], dtype=np.float64)

    alpha = compute_direct_alpha(times, calls, dist, nav, prices)
    assert np.isfinite(alpha), f"Direct Alpha is non-finite: {alpha}"

    # Invariant 1: Discounted cash flows at alpha have zero NPV
    flows = (dist - calls) / prices
    npv_alpha = float(np.sum(flows * np.exp(-alpha * times)) + (nav / prices[-1]) * np.exp(-alpha * times[-1]))
    assert abs(npv_alpha) < 1e-5, f"NPV at Direct Alpha must be zero, got {npv_alpha}"

    # Invariant 2: Benchmark-matching cash flows yield alpha = 0.0
    perfect_dist = np.zeros_like(dist)
    perfect_dist[-1] = float(np.sum(calls * (prices[-1] / prices)))
    alpha_perfect = compute_direct_alpha(times, calls, perfect_dist, 0.0, prices)
    assert abs(alpha_perfect) < 1e-6, f"Direct Alpha must be 0 for market-matching fund, got {alpha_perfect}"

    # Invariant 3: Sign agreement between KS-PME and Direct Alpha
    ks_pme = compute_ks_pme(times, calls, dist, nav, prices)
    if abs(ks_pme - 1.0) > 0.02:
        assert (alpha > 0.0) == (ks_pme > 1.0), f"Sign mismatch: Direct Alpha={alpha}, KS-PME={ks_pme}"


# ============================================================================
# 6. Direct Alpha Recovery of True Alpha
# ============================================================================


def test_direct_alpha_recovery() -> None:
    # Test recovery of known true alpha on a controlled synthetic fund with beta=1.0
    times = np.linspace(0.0, 10.0, 21)
    prices = 100.0 * np.exp(0.07 * times)  # 7% deterministic market growth
    calls = np.zeros(21)
    calls[0] = 50.0
    calls[2] = 50.0  # t=1.0

    target_alpha = 0.035  # 3.50% continuous true alpha
    # Exits at t=5.0 and t=10.0
    dist = np.zeros(21)
    dist[10] = calls[0] * (prices[10] / prices[0]) * math.exp(target_alpha * 5.0)  # exit tranche 0 at t=5
    dist[20] = calls[2] * (prices[20] / prices[2]) * math.exp(target_alpha * 9.0)  # exit tranche 2 at t=10

    recovered_alpha = compute_direct_alpha(times, calls, dist, 0.0, prices)
    assert abs(recovered_alpha - target_alpha) < 1e-6, (
        f"Direct Alpha failed to recover known true alpha: {recovered_alpha} vs {target_alpha}"
    )


# ============================================================================
# 7. Long & Nickels (1996) Index Replication and Short Position Breakdown
# ============================================================================


def test_long_nickels_pme_properties() -> None:
    times = np.asarray(INST["times"], dtype=np.float64)
    calls = np.asarray(INST["calls"], dtype=np.float64)
    dist = np.asarray(INST["distributions"], dtype=np.float64)
    prices = np.asarray(INST["benchmark_prices"], dtype=np.float64)

    ln_irr, v_series, went_short = compute_long_nickels_pme(times, calls, dist, prices)
    if not went_short and v_series[-1] >= 0.0:
        assert np.isfinite(ln_irr), "LN-IRR should be finite when not short"

    # Invariant 1: Initial synthetic NAV equals net initial flow
    assert abs(v_series[0] - (calls[0] - dist[0])) < 1e-9

    # Invariant 2: Recurrence relation holds across all time steps
    for i in range(1, len(times)):
        expected_v = v_series[i - 1] * (prices[i] / prices[i - 1]) + calls[i] - dist[i]
        assert abs(v_series[i] - expected_v) < 1e-6, f"LN NAV step {i} failed recurrence: {v_series[i]} vs {expected_v}"

    # Invariant 3: Short position detection
    # If any intermediate NAV was negative, went_short must be True
    has_negative = bool(np.any(v_series < -1e-6))
    assert went_short == has_negative, f"went_short flag {went_short} disagrees with negative values {has_negative}"

    # Invariant 4: Controlled test case with intentional early over-distribution causing short position
    calls_stressed = np.array([100.0, 0.0, 0.0, 0.0])
    dist_stressed = np.array([0.0, 150.0, 0.0, 0.0])  # Huge early exit exceeding index growth
    prices_flat = np.array([100.0, 105.0, 110.0, 115.0])
    times_stressed = np.array([0.0, 1.0, 2.0, 3.0])

    _, _, went_short_stressed = compute_long_nickels_pme(times_stressed, calls_stressed, dist_stressed, prices_flat)
    assert went_short_stressed, "LN-PME failed to detect short index position caused by large early distributions"


# ============================================================================
# 8. Complete Fund Evaluation Articulation
# ============================================================================


def test_evaluate_fund_structure() -> None:
    summary = evaluate_fund(INST)

    required_keys = {"irr", "dpi", "rvpi", "tvpi", "ks_pme", "direct_alpha", "ln_irr", "ln_went_short", "ln_nav_series"}
    assert required_keys.issubset(summary.keys())

    assert abs(summary["tvpi"] - (summary["dpi"] + summary["rvpi"])) < 1e-9
    assert isinstance(summary["ln_went_short"], bool)
    assert len(summary["ln_nav_series"]) == len(INST["times"])


# ============================================================================
# 9. Subscription Line Distortion Mechanics
# ============================================================================


def test_subscription_line_mechanics() -> None:
    # A single $100M investment at t=0 exited at t=5.0 for $200M (2.0x MOIC)
    # Case A: Standard LP capital call at t=0
    times_a = np.array([0.0, 5.0])
    calls_a = np.array([100.0, 0.0])
    dist_a = np.array([0.0, 200.0])

    irr_a = compute_irr(times_a, dist_a - calls_a)
    _, _, tvpi_a = compute_moic(calls_a, dist_a, 0.0)

    # Case B: 1-year subscription credit line at 5% borrowing cost
    # LP capital called at t=1.0 for $105M (principal + interest)
    times_b = np.array([1.0, 5.0])
    calls_b = np.array([105.0, 0.0])
    dist_b = np.array([0.0, 200.0])

    irr_b = compute_irr(times_b, dist_b - calls_b)
    _, _, tvpi_b = compute_moic(calls_b, dist_b, 0.0)

    # Fundamental Private Equity Theorem:
    # Subscription line increases IRR due to holding period compression,
    # but reduces MOIC/TVPI due to credit facility interest drag!
    assert irr_b > irr_a + 0.02, f"Expected subscription line to boost IRR by >200 bps: {irr_b} vs {irr_a}"
    assert tvpi_b < tvpi_a, f"Expected subscription line interest expense to lower MOIC: {tvpi_b} vs {tvpi_a}"
