"""Autograder test suite for the E7 Monetary-Shock Identification project."""

from __future__ import annotations

import json
import math
import os
from typing import Any

# The learner solution is imported as monetary_shocks
import monetary_shocks as mod
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
CASE: dict[str, Any] = json.loads(make_instance(SEED)["payload"])


def test_calculate_fed_funds_surprise_scaling() -> None:
    # On day 10 of a 30-day month, scale is 30 / (30 - 10) = 1.5
    f_pre = 2.50
    f_post = 2.60
    surp = mod.calculate_fed_funds_surprise(f_post, f_pre, 10, 30)
    expected = 1.5 * 0.10
    assert abs(surp - expected) < 1e-6


def test_calculate_fed_funds_surprise_zero_jump() -> None:
    surp = mod.calculate_fed_funds_surprise(3.25, 3.25, 15, 31)
    assert abs(surp) < 1e-12


def test_calculate_fed_funds_surprise_boundary_validation() -> None:
    with pytest.raises(ValueError):
        mod.calculate_fed_funds_surprise(2.0, 2.1, 0, 30)
    with pytest.raises(ValueError):
        mod.calculate_fed_funds_surprise(2.0, 2.1, 30, 30)
    with pytest.raises(ValueError):
        mod.calculate_fed_funds_surprise(2.0, 2.1, 32, 31)


def test_clean_high_frequency_surprises_length() -> None:
    n_months = CASE["n_months"]
    announcements = CASE["announcements"]
    monthly = mod.clean_high_frequency_surprises(announcements, n_months)
    assert len(monthly) == n_months
    assert any(abs(x) > 1e-4 for x in monthly)


def test_local_projection_shapes() -> None:
    y = CASE["output_gap"]
    shock = mod.clean_high_frequency_surprises(CASE["announcements"], CASE["n_months"])
    horizon = 6
    lags = 2
    betas, ses = mod.estimate_local_projection(y, shock, None, horizon, lags)
    assert len(betas) == horizon + 1
    assert len(ses) == horizon + 1
    assert all(math.isfinite(b) for b in betas)
    assert all(se > 0.0 for se in ses)


def test_local_projection_monetary_transmission_direction() -> None:
    # A contractionary monetary surprise should reduce the output gap dynamically
    y = CASE["output_gap"]
    shock = mod.clean_high_frequency_surprises(CASE["announcements"], CASE["n_months"])
    horizon = CASE["max_horizon"]
    lags = CASE["lags"]
    betas, _ = mod.estimate_local_projection(y, shock, None, horizon, lags)
    # The minimum output gap response over horizon h=1..6 should be negative
    min_response = min(betas[1:7])
    assert min_response < 0.0, f"Expected contractionary policy impact on output gap, got {min_response}"


def test_compare_monetary_shocks() -> None:
    sh_hf = mod.clean_high_frequency_surprises(CASE["announcements"], CASE["n_months"])
    sh_narrative = CASE["shock_narrative"]
    comp = mod.compare_monetary_shocks(sh_hf, sh_narrative)
    assert -1.0 <= comp["correlation"] <= 1.0
    assert comp["std_a"] > 0.0
    assert comp["std_b"] > 0.0
    assert comp["ratio_a_to_b"] > 0.0


def test_test_information_effect() -> None:
    shock = mod.clean_high_frequency_surprises(CASE["announcements"], CASE["n_months"])
    y2 = CASE["yield_2y"]
    growth_rev = [0.1 * y2[i] + 0.05 * shock[i] for i in range(len(shock))]
    res = mod.test_information_effect(shock, y2, growth_rev)
    assert "information_slope" in res
    assert "has_positive_information_effect" in res
    assert res["has_positive_information_effect"] in (0.0, 1.0)


def test_invalid_local_projection_inputs() -> None:
    with pytest.raises(ValueError):
        mod.estimate_local_projection([1.0, 2.0], [1.0], None, 1, 1)
    with pytest.raises(ValueError):
        mod.estimate_local_projection([1.0, 2.0, 3.0], [1.0, 2.0, 3.0], None, -1, 1)
    with pytest.raises(ValueError):
        mod.estimate_local_projection([1.0, 2.0, 3.0], [1.0, 2.0, 3.0], None, 1, 0)
