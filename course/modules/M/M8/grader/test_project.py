"""Pytest test suite for M8 robust implied-volatility solver."""

from __future__ import annotations

import math
import os
import time
from typing import Any

import pytest
from instance import make_instance  # type: ignore[import-not-found]
from pricing import bounds, bs_price  # type: ignore[import-not-found]
from solver import implied_vol, last_evaluations, region  # type: ignore[import-not-found]

_SEED = int(os.environ.get("QF_SEED", "0"))
_INST: dict[str, Any] = make_instance(_SEED)


def test_t1_kind_validation() -> None:
    """T1: kind not in {'call', 'put'} raises ValueError; valid kinds pass."""
    __tracebackhide__ = True
    s, k, tau, r = 100.0, 100.0, 1.0, 0.05
    c_p = bs_price(s, k, tau, r, 0.2, "call")
    p_p = bs_price(s, k, tau, r, 0.2, "put")

    assert implied_vol(c_p, s, k, tau, r, "call") > 0.0
    assert implied_vol(p_p, s, k, tau, r, "put") > 0.0

    for invalid_kind in ["forward", "straddle", "CALL", "", "binary"]:
        with pytest.raises(ValueError, match="kind"):
            implied_vol(c_p, s, k, tau, r, invalid_kind)


def test_t2_non_positive_and_non_finite() -> None:
    """T2: non-positive or non-finite inputs raise ValueError."""
    __tracebackhide__ = True
    s, k, tau, r = 100.0, 100.0, 1.0, 0.05
    p = bs_price(s, k, tau, r, 0.2, "call")

    with pytest.raises(ValueError):
        implied_vol(p, 0.0, k, tau, r, "call")
    with pytest.raises(ValueError):
        implied_vol(p, -10.0, k, tau, r, "call")
    with pytest.raises(ValueError):
        implied_vol(p, float("nan"), k, tau, r, "call")

    with pytest.raises(ValueError):
        implied_vol(p, s, 0.0, tau, r, "call")
    with pytest.raises(ValueError):
        implied_vol(p, s, -50.0, tau, r, "call")
    with pytest.raises(ValueError):
        implied_vol(p, s, float("inf"), tau, r, "call")

    with pytest.raises(ValueError):
        implied_vol(p, s, k, 0.0, r, "call")
    with pytest.raises(ValueError):
        implied_vol(p, s, k, -0.5, r, "call")

    with pytest.raises(ValueError):
        implied_vol(p, s, k, tau, float("nan"), "call")
    with pytest.raises(ValueError):
        implied_vol(float("nan"), s, k, tau, r, "call")


def test_t3_bounds_call() -> None:
    """T3: call price on or outside strict theoretical bounds raises ValueError; interior solves."""
    __tracebackhide__ = True
    s, k, tau, r = 100.0, 100.0, 1.0, 0.05
    lo, hi = bounds(s, k, tau, r, "call")

    with pytest.raises(ValueError):
        implied_vol(lo, s, k, tau, r, "call")
    with pytest.raises(ValueError):
        implied_vol(lo - 1.0, s, k, tau, r, "call")
    with pytest.raises(ValueError):
        implied_vol(hi, s, k, tau, r, "call")
    with pytest.raises(ValueError):
        implied_vol(hi + 1.0, s, k, tau, r, "call")

    # Just inside
    p_inside = lo + 0.1 * (hi - lo)
    v = implied_vol(p_inside, s, k, tau, r, "call")
    assert abs(bs_price(s, k, tau, r, v, "call") - p_inside) <= 1e-12 * s


def test_t4_bounds_put() -> None:
    """T4: put price on or outside strict theoretical bounds raises ValueError; interior solves."""
    __tracebackhide__ = True
    s, k, tau, r = 100.0, 100.0, 1.0, 0.05
    lo, hi = bounds(s, k, tau, r, "put")

    with pytest.raises(ValueError):
        implied_vol(lo, s, k, tau, r, "put")
    with pytest.raises(ValueError):
        implied_vol(lo - 0.5, s, k, tau, r, "put")
    with pytest.raises(ValueError):
        implied_vol(hi, s, k, tau, r, "put")
    with pytest.raises(ValueError):
        implied_vol(hi + 2.0, s, k, tau, r, "put")

    p_inside = lo + 0.2 * (hi - lo)
    v = implied_vol(p_inside, s, k, tau, r, "put")
    assert abs(bs_price(s, k, tau, r, v, "put") - p_inside) <= 1e-12 * s


def test_t5_upper_bracket_not_fixed() -> None:
    """T5: upper bracket expands dynamically for high volatility instances."""
    __tracebackhide__ = True
    s, k, tau, r = 100.0, 100.0, 1.0, 0.05
    p = 99.99995
    v = implied_vol(p, s, k, tau, r, "call")
    assert v > 10.0
    recalc = bs_price(s, k, tau, r, v, "call")
    assert abs(recalc - p) <= 1e-12 * s


def test_t6_valid_deep_itm_and_otm() -> None:
    """T6: deep ITM and deep OTM instances meet residual and forward accuracy."""
    __tracebackhide__ = True
    spots = _INST["spots"]
    strikes = _INST["strikes"]
    taus = _INST["taus"]
    rates = _INST["rates"]
    kinds = _INST["kinds"]
    prices = _INST["prices"]
    vols = _INST["vols"]
    vegas = _INST["vegas"]

    tested = 0
    for i in range(len(spots)):
        log_m = abs(math.log(spots[i] / strikes[i]))
        if log_m >= 1.5:
            tested += 1
            v_hat = implied_vol(prices[i], spots[i], strikes[i], taus[i], rates[i], kinds[i])
            res = abs(bs_price(spots[i], strikes[i], taus[i], rates[i], v_hat, kinds[i]) - prices[i])
            assert res <= 1e-12 * spots[i]
            if vegas[i] >= 0.01:
                assert abs(v_hat - vols[i]) <= 1e-7
    assert tested > 0


def test_t7_near_expiry() -> None:
    """T7: near-expiry instances meet residual and forward accuracy."""
    __tracebackhide__ = True
    spots = _INST["spots"]
    strikes = _INST["strikes"]
    taus = _INST["taus"]
    rates = _INST["rates"]
    kinds = _INST["kinds"]
    prices = _INST["prices"]
    vols = _INST["vols"]
    vegas = _INST["vegas"]

    tested = 0
    for i in range(len(spots)):
        if taus[i] <= 7.0 / 365.0:
            tested += 1
            v_hat = implied_vol(prices[i], spots[i], strikes[i], taus[i], rates[i], kinds[i])
            res = abs(bs_price(spots[i], strikes[i], taus[i], rates[i], v_hat, kinds[i]) - prices[i])
            assert res <= 1e-12 * spots[i]
            if vegas[i] >= 0.01:
                assert abs(v_hat - vols[i]) <= 1e-7
    assert tested > 0


def test_t8_put_round_trip() -> None:
    """T8: put instances invert without formula distortion."""
    __tracebackhide__ = True
    spots = _INST["spots"]
    strikes = _INST["strikes"]
    taus = _INST["taus"]
    rates = _INST["rates"]
    kinds = _INST["kinds"]
    prices = _INST["prices"]

    put_count = 0
    for i in range(min(100, len(spots))):
        if kinds[i] == "put":
            put_count += 1
            v_hat = implied_vol(prices[i], spots[i], strikes[i], taus[i], rates[i], "put")
            recalc = bs_price(spots[i], strikes[i], taus[i], rates[i], v_hat, "put")
            assert abs(recalc - prices[i]) <= 1e-12 * spots[i]
    assert put_count > 0


def test_t9_residual_everywhere() -> None:
    """T9: residual bound |C(sigma_hat) - price| <= 1e-12 * S holds across all grid inputs."""
    __tracebackhide__ = True
    spots = _INST["spots"]
    strikes = _INST["strikes"]
    taus = _INST["taus"]
    rates = _INST["rates"]
    kinds = _INST["kinds"]
    prices = _INST["prices"]

    for i in range(len(spots)):
        v_hat = implied_vol(prices[i], spots[i], strikes[i], taus[i], rates[i], kinds[i])
        recalc = bs_price(spots[i], strikes[i], taus[i], rates[i], v_hat, kinds[i])
        assert abs(recalc - prices[i]) <= 1e-12 * spots[i]


def test_t10_forward_bound() -> None:
    """T10: forward bound |sigma_hat - sigma*| <= 1e-7 holds wherever vega >= 0.01."""
    __tracebackhide__ = True
    spots = _INST["spots"]
    strikes = _INST["strikes"]
    taus = _INST["taus"]
    rates = _INST["rates"]
    kinds = _INST["kinds"]
    prices = _INST["prices"]
    vols = _INST["vols"]
    vegas = _INST["vegas"]

    checked = 0
    for i in range(len(spots)):
        if vegas[i] >= 0.01:
            checked += 1
            v_hat = implied_vol(prices[i], spots[i], strikes[i], taus[i], rates[i], kinds[i])
            assert abs(v_hat - vols[i]) <= 1e-7
    assert checked > 0


def test_t11_region_labels() -> None:
    """T11: region labels accurately reflect vega conditioning threshold."""
    __tracebackhide__ = True
    spots = _INST["spots"]
    strikes = _INST["strikes"]
    taus = _INST["taus"]
    rates = _INST["rates"]
    kinds = _INST["kinds"]
    prices = _INST["prices"]
    regions = _INST["regions"]

    for i in range(min(50, len(spots))):
        lbl = region(prices[i], spots[i], strikes[i], taus[i], rates[i], kinds[i])
        assert lbl == regions[i]

    with pytest.raises(ValueError):
        region(-1.0, 100.0, 100.0, 1.0, 0.05, "call")


def test_t12_region_counts() -> None:
    """T12: failure-region report counts match suite expectations."""
    __tracebackhide__ = True
    assert _INST["n_solved"] > 0
    assert _INST["n_ill_conditioned"] > 0
    assert _INST["n_solved"] + _INST["n_ill_conditioned"] == _INST["n_total"]


def test_t13_determinism() -> None:
    """T13: consecutive calls with identical inputs produce bit-identical floats."""
    __tracebackhide__ = True
    s, k, tau, r = 100.0, 105.0, 0.5, 0.03
    p = bs_price(s, k, tau, r, 0.25, "call")
    v1 = implied_vol(p, s, k, tau, r, "call")
    v2 = implied_vol(p, s, k, tau, r, "call")
    assert v1.hex() == v2.hex()


def test_t14_evaluation_budget() -> None:
    """T14: pricing calls do not exceed the evaluation budget B = 35."""
    __tracebackhide__ = True
    spots = _INST["spots"]
    strikes = _INST["strikes"]
    taus = _INST["taus"]
    rates = _INST["rates"]
    kinds = _INST["kinds"]
    prices = _INST["prices"]

    for i in range(min(100, len(spots))):
        implied_vol(prices[i], spots[i], strikes[i], taus[i], rates[i], kinds[i])
        cnt = last_evaluations()
        assert cnt <= 35


def test_t15_no_fabricated_answer() -> None:
    """T15: solver output is responsive to price changes and not fabricated."""
    __tracebackhide__ = True
    s, k, tau, r = 100.0, 100.0, 1.0, 0.05
    p1 = bs_price(s, k, tau, r, 0.20, "call")
    p2 = bs_price(s, k, tau, r, 0.30, "call")
    v1 = implied_vol(p1, s, k, tau, r, "call")
    v2 = implied_vol(p2, s, k, tau, r, "call")
    assert abs(v1 - 0.20) <= 1e-7
    assert abs(v2 - 0.30) <= 1e-7
    assert abs(v2 - v1) > 0.05


def test_t16_execution_time() -> None:
    """T16: entire seeded grid finishes within local suite limit."""
    __tracebackhide__ = True
    spots = _INST["spots"]
    strikes = _INST["strikes"]
    taus = _INST["taus"]
    rates = _INST["rates"]
    kinds = _INST["kinds"]
    prices = _INST["prices"]

    start = time.perf_counter()
    for i in range(len(spots)):
        implied_vol(prices[i], spots[i], strikes[i], taus[i], rates[i], kinds[i])
    elapsed = time.perf_counter() - start
    assert elapsed < 5.0


def test_t18_instance_validity() -> None:
    """T18: instance generation is valid and strictly bounded."""
    __tracebackhide__ = True
    inst = make_instance(_SEED)
    assert inst["seed"] == _SEED
    assert inst["label"] == "SIMULATED"
    assert inst["n_total"] == 2000
    assert len(inst["spots"]) == 2000
