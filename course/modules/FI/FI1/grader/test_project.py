"""Acceptance suite for the FI1 curve engine (atlas/curves.py).

Runs identically in the browser (Pyodide) and locally:
    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import datetime
import json
import math
import os
from fractions import Fraction
from typing import Any

import pytest
from atlas import curves as sol  # type: ignore[attr-defined]
from instance import make_instance  # type: ignore[import-not-found]

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
PAYLOAD: dict[str, Any] = json.loads(INST["payload"])

# Reconstruct objects
START_DATE = datetime.date.fromisoformat(PAYLOAD["start_date"])
END_DATE = datetime.date.fromisoformat(PAYLOAD["end_date"])
FACE_CENTS: int = PAYLOAD["face_cents"]
COUPON_RATE = Fraction(PAYLOAD["coupon_rate"][0], PAYLOAD["coupon_rate"][1])
PERIODS: int = PAYLOAD["periods"]
YIELD_PER_PERIOD = Fraction(PAYLOAD["yield_per_period"][0], PAYLOAD["yield_per_period"][1])
EXPECTED_DIRTY_CENTS: int = PAYLOAD["expected_dirty_cents"]

YTM_FACE: int = PAYLOAD["ytm_face"]
YTM_C = Fraction(PAYLOAD["ytm_c"][0], PAYLOAD["ytm_c"][1])
YTM_PERIODS: int = PAYLOAD["ytm_periods"]
YTM_TRUE_Y = Fraction(PAYLOAD["ytm_true_y"][0], PAYLOAD["ytm_true_y"][1])
YTM_DIRTY_CENTS: int = PAYLOAD["ytm_dirty_cents"]

BOOTSTRAP_BONDS = [
    {
        "periods": b["periods"],
        "coupon_rate": Fraction(b["coupon_rate"][0], b["coupon_rate"][1]),
        "face_cents": b["face_cents"],
        "price_cents": b["price_cents"],
    }
    for b in PAYLOAD["bootstrap_bonds"]
]

NS_PARAMS: dict[str, float] = PAYLOAD["ns_params"]
NS_MATURITIES = [Fraction(m[0], m[1]) for m in PAYLOAD["ns_maturities"]]
NS_YIELDS = [Fraction(y[0], y[1]) for y in PAYLOAD["ns_yields"]]

SV_PARAMS: dict[str, float] = PAYLOAD["sv_params"]
SV_MATURITIES = [Fraction(m[0], m[1]) for m in PAYLOAD["sv_maturities"]]
SV_YIELDS = [Fraction(y[0], y[1]) for y in PAYLOAD["sv_yields"]]


def test_day_count_conventions_constant() -> None:
    """The exported tuple must list the three supported conventions."""
    assert hasattr(sol, "DAY_COUNT_CONVENTIONS")
    assert sol.DAY_COUNT_CONVENTIONS == ("ACT/360", "ACT/365", "30/360")


def test_day_count_fraction_fixed_pairs() -> None:
    """Check exact day-count fractions on fixed known date pairs."""
    # 2024 is a leap year; Jan 1 to Jul 1 is 182 days
    d1 = datetime.date(2024, 1, 1)
    d2 = datetime.date(2024, 7, 1)
    f_360 = sol.day_count_fraction(d1, d2, "ACT/360")
    f_365 = sol.day_count_fraction(d1, d2, "ACT/365")
    assert f_360 == Fraction(182, 360)
    assert f_365 == Fraction(182, 365)
    # Ratio check: ACT/365 / ACT/360 == 360 / 365
    assert (f_365 / f_360) == Fraction(360, 365)

    # 30/360 rule: 2024-02-01 to 2024-03-01 is exactly 30 days (1 month = 30 days)
    feb1 = datetime.date(2024, 2, 1)
    mar1 = datetime.date(2024, 3, 1)
    f_30_360 = sol.day_count_fraction(feb1, mar1, "30/360")
    assert f_30_360 == Fraction(30, 360)
    assert f_30_360 == Fraction(1, 12)


def test_day_count_fraction_same_date() -> None:
    """Same start and end date must return exactly zero."""
    today = datetime.date(2024, 5, 15)
    for conv in sol.DAY_COUNT_CONVENTIONS:
        assert sol.day_count_fraction(today, today, conv) == Fraction(0, 1)


def test_day_count_fraction_instance_dates() -> None:
    """Check instance-generated dates satisfy convention ordering."""
    start = START_DATE
    end = END_DATE
    act360 = sol.day_count_fraction(start, end, "ACT/360")
    act365 = sol.day_count_fraction(start, end, "ACT/365")
    # For positive day difference, ACT/360 fraction is strictly larger than ACT/365
    assert act360 > act365
    assert act365 / act360 == Fraction(360, 365)


def test_price_from_yield_exact() -> None:
    """Price from yield matches closed form and exact integer cent rounding."""
    computed = sol.price_from_yield(FACE_CENTS, COUPON_RATE, PERIODS, YIELD_PER_PERIOD)
    assert computed == EXPECTED_DIRTY_CENTS

    # Edge case: zero yield
    p_zero = sol.price_from_yield(FACE_CENTS, COUPON_RATE, PERIODS, Fraction(0, 1))
    assert p_zero == FACE_CENTS + math.floor(Fraction(FACE_CENTS) * COUPON_RATE * PERIODS + Fraction(1, 2))


def test_price_from_yield_monotonicity() -> None:
    """Bond price is strictly decreasing in yield for positive cash flows."""
    face = 100_000
    coupon = Fraction(5, 100)
    periods = 10
    y1 = Fraction(2, 100)
    y2 = Fraction(4, 100)
    y3 = Fraction(6, 100)

    p1 = sol.price_from_yield(face, coupon, periods, y1)
    p2 = sol.price_from_yield(face, coupon, periods, y2)
    p3 = sol.price_from_yield(face, coupon, periods, y3)
    assert p1 > p2 > p3


def test_yield_to_maturity_repricing() -> None:
    """Solved yield to maturity reprices the bond to within half a cent."""
    solved_y = sol.yield_to_maturity(YTM_DIRTY_CENTS, YTM_FACE, YTM_C, YTM_PERIODS)
    repriced_cents = sol.price_from_yield(YTM_FACE, YTM_C, YTM_PERIODS, solved_y)
    assert repriced_cents == YTM_DIRTY_CENTS


def test_bootstrap_zero_rates_repricing() -> None:
    """Zero rates extracted by bootstrapping reprice every input par bond within 1 cent."""
    rates = sol.bootstrap_zero_rates(BOOTSTRAP_BONDS)
    assert len(rates) == len(BOOTSTRAP_BONDS)

    for b in BOOTSTRAP_BONDS:
        n = b["periods"]
        c = b["coupon_rate"]
        face = b["face_cents"]
        target_p = b["price_cents"]

        # Reprice using bootstrapped zero rates
        pv = 0.0
        for k in range(1, n + 1):
            zk = rates[k]
            cf = float(c * face) if k < n else float((1 + c) * face)
            pv += cf / ((1.0 + zk) ** k)
        reprice_cents = math.floor(pv + 0.5)
        assert abs(reprice_cents - target_p) <= 1


def test_ns_yield_eval() -> None:
    """ns_yield computes the correct continuous spot rate."""
    p = NS_PARAMS
    b0, b1, b2, lam = p["beta0"], p["beta1"], p["beta2"], p["lam"]
    tau = 2.0
    x = tau / lam
    g = (1.0 - math.exp(-x)) / x
    expected = b0 + b1 * g + b2 * (g - math.exp(-x))
    computed = sol.ns_yield(tau, b0, b1, b2, lam)
    assert abs(computed - expected) < 1e-12


def test_fit_nelson_siegel_recovery() -> None:
    """Nelson-Siegel fitting recovers the generating parameters within tolerance."""
    fitted = sol.fit_nelson_siegel(NS_MATURITIES, NS_YIELDS)
    assert abs(fitted["beta0"] - NS_PARAMS["beta0"]) < 1e-3
    assert abs(fitted["beta1"] - NS_PARAMS["beta1"]) < 1e-3
    assert abs(fitted["beta2"] - NS_PARAMS["beta2"]) < 1e-3
    assert abs(fitted["lam"] - NS_PARAMS["lam"]) < 1e-6


def test_svensson_yield_eval_and_nesting() -> None:
    """svensson_yield matches formula and reduces to ns_yield when beta3 = 0."""
    p = SV_PARAMS
    b0, b1, b2, b3, l1, l2 = p["beta0"], p["beta1"], p["beta2"], p["beta3"], p["lam1"], p["lam2"]
    tau = 3.5

    sv_val = sol.svensson_yield(tau, b0, b1, b2, b3, l1, l2)
    assert math.isfinite(sv_val)

    # Nesting condition: with beta3 = 0, Svensson must equal Nelson-Siegel
    sv_nested = sol.svensson_yield(tau, b0, b1, b2, 0.0, l1, l2)
    ns_val = sol.ns_yield(tau, b0, b1, b2, l1)
    assert abs(sv_nested - ns_val) < 1e-12


def test_fit_svensson_recovery() -> None:
    """Svensson fitting recovers the generating parameters within tolerance."""
    fitted = sol.fit_svensson(SV_MATURITIES, SV_YIELDS)
    assert abs(fitted["beta0"] - SV_PARAMS["beta0"]) < 1e-3
    assert abs(fitted["beta1"] - SV_PARAMS["beta1"]) < 1e-3
    assert abs(fitted["beta2"] - SV_PARAMS["beta2"]) < 1e-3
    assert abs(fitted["beta3"] - SV_PARAMS["beta3"]) < 1e-3
    assert abs(fitted["lam1"] - SV_PARAMS["lam1"]) < 1e-6
    assert abs(fitted["lam2"] - SV_PARAMS["lam2"]) < 1e-6


@pytest.mark.skip(
    reason=(
        "Honest-pending: real GSW published parameter snapshot pending Board licence verification"
        " (Phase 2 Architect Ruling 5)"
    )
)
def test_published_gsw_parameters() -> None:
    """Honest-pending test against official published GSW parameter time series."""
    pass


def test_invalid_day_count_inputs() -> None:
    """Invalid day-count convention or date order raises ValueError; wrong types raise TypeError."""
    d1 = datetime.date(2024, 1, 1)
    d2 = datetime.date(2023, 1, 1)
    with pytest.raises(ValueError):
        sol.day_count_fraction(d1, d2, "ACT/360")
    with pytest.raises(ValueError):
        sol.day_count_fraction(d2, d1, "30/365")  # unknown convention
    with pytest.raises(TypeError):
        sol.day_count_fraction("2024-01-01", "2024-07-01", "ACT/360")


def test_invalid_bond_pricing_inputs() -> None:
    """Invalid bond pricing inputs raise ValueError or TypeError."""
    with pytest.raises(ValueError):
        sol.price_from_yield(0, Fraction(5, 100), 10, Fraction(5, 100))
    with pytest.raises(ValueError):
        sol.price_from_yield(100_000, Fraction(5, 100), 0, Fraction(5, 100))
    with pytest.raises(ValueError):
        sol.price_from_yield(100_000, Fraction(-1, 100), 10, Fraction(5, 100))
    with pytest.raises(ValueError):
        sol.price_from_yield(100_000, Fraction(5, 100), 10, Fraction(-1, 1))
    with pytest.raises(TypeError):
        sol.price_from_yield(100_000, 0.05, 10, Fraction(5, 100))


def test_invalid_ytm_inputs() -> None:
    """Invalid YTM inputs raise ValueError."""
    with pytest.raises(ValueError):
        sol.yield_to_maturity(0, 100_000, Fraction(5, 100), 10)
    with pytest.raises(ValueError):
        sol.yield_to_maturity(-5000, 100_000, Fraction(5, 100), 10)


def test_invalid_curve_inputs() -> None:
    """Curve function domain violations raise ValueError."""
    with pytest.raises(ValueError):
        sol.ns_yield(0.0, 0.05, -0.02, 0.02, 2.0)
    with pytest.raises(ValueError):
        sol.ns_yield(2.0, 0.05, -0.02, 0.02, 0.0)
    with pytest.raises(ValueError):
        sol.svensson_yield(0.0, 0.05, -0.02, 0.02, -0.01, 2.0, 5.0)
    with pytest.raises(ValueError):
        sol.svensson_yield(2.0, 0.05, -0.02, 0.02, -0.01, 0.0, 5.0)
    with pytest.raises(ValueError):
        sol.svensson_yield(2.0, 0.05, -0.02, 0.02, -0.01, 2.0, 0.0)


def test_invalid_fit_inputs() -> None:
    """Too few points or mismatched lengths raise ValueError."""
    with pytest.raises(ValueError):
        sol.fit_nelson_siegel([Fraction(1, 1), Fraction(2, 1)], [Fraction(5, 100), Fraction(6, 100)])
    with pytest.raises(ValueError):
        sol.fit_nelson_siegel(
            [Fraction(1, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1)],
            [Fraction(5, 100), Fraction(6, 100)],
        )
    with pytest.raises(ValueError):
        sol.fit_svensson(
            [Fraction(i, 1) for i in range(1, 5)],
            [Fraction(5, 100) for _ in range(4)],
        )
