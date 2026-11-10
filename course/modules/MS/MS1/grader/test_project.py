"""Acceptance suite for the MS1 project: trade-level spread decomposition (decompose.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Checks contract, input validation, NaN handling, regression identities, scale/location invariance,
and numeric oracle agreement across instances.
"""

from __future__ import annotations

import importlib
import math
import os
from collections.abc import Callable
from typing import Any

import pytest

sol: Any = importlib.import_module("decompose")
make_instance: Callable[[int], dict[str, Any]] = importlib.import_module("instance").make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
INST2 = make_instance(SEED + 7919)

KEYS = {"roll_spread", "half_spread", "order_processing", "adverse_selection", "adverse_share"}


def expect(ok: bool, hint: str) -> None:
    """Fail with a descriptive hint if condition is not satisfied."""
    __tracebackhide__ = True
    if not ok:
        pytest.fail(hint, pytrace=False)


def must_raise(call: Callable[[], object], condition: str, *, contains: tuple[str, ...] = ()) -> None:
    """Check that call() raises ValueError with specified substring."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError as err:
        for text in contains:
            expect(text in str(err), f"{condition}: ValueError message must contain '{text}' (got: {err})")
        return
    except Exception as exc:
        pytest.fail(f"{condition}: expected ValueError, got {type(exc).__name__}: {exc}", pytrace=False)
    pytest.fail(f"{condition}: expected ValueError, none was raised", pytrace=False)


def oracle_decompose(prices: list[float], signs: list[int]) -> dict[str, float]:
    """Independent oracle computation for trade decomposition."""
    n = len(prices)
    d = [prices[i] - prices[i - 1] for i in range(1, n)]
    mean_d = sum(d) / len(d)
    cov1 = sum((d[i] - mean_d) * (d[i - 1] - mean_d) for i in range(1, len(d))) / (len(d) - 1)
    roll = 2.0 * math.sqrt(-cov1) if cov1 < 0.0 else float("nan")

    q_curr = [float(signs[i]) for i in range(1, n)]
    q_lag = [float(signs[i - 1]) for i in range(1, n)]

    s00 = sum(x * x for x in q_curr)
    s11 = sum(x * x for x in q_lag)
    s01 = sum(x * y for x, y in zip(q_curr, q_lag, strict=False))
    det = s00 * s11 - s01 * s01
    if det == 0.0:
        raise ValueError("singular design matrix")

    y0 = sum(di * qi for di, qi in zip(d, q_curr, strict=False))
    y1 = sum(di * qi for di, qi in zip(d, q_lag, strict=False))

    b0 = (s11 * y0 - s01 * y1) / det
    b1 = (s00 * y1 - s01 * y0) / det

    h = b0
    c_val = -b1
    theta_val = b0 + b1
    share = theta_val / h if h != 0.0 else float("nan")

    return {
        "roll_spread": roll,
        "half_spread": h,
        "order_processing": c_val,
        "adverse_selection": theta_val,
        "adverse_share": share,
    }


def test_interface_contract() -> None:
    """decompose_trades must be callable and return exactly the required keys."""
    prices: list[float] = list(INST["prices"])
    signs: list[int] = list(INST["signs"])
    res = sol.decompose_trades(prices, signs)
    expect(isinstance(res, dict), "decompose_trades must return a dictionary")
    expect(set(res.keys()) == KEYS, f"returned keys must be exactly {KEYS}")
    for k in KEYS:
        expect(isinstance(res[k], float), f"value for {k} must be float")


def test_validation_too_few_trades() -> None:
    """Fewer than three trades must raise ValueError with named message."""
    must_raise(
        lambda: sol.decompose_trades([100.0, 100.1], [1, -1]),
        "fewer than 3 trades",
        contains=("at least three trades are needed",),
    )
    # 3 trades must not raise
    p3 = [100.0, 100.2, 99.9]
    s3 = [1, 1, -1]
    res = sol.decompose_trades(p3, s3)
    expect(isinstance(res, dict), "valid 3-trade sequence must succeed")


def test_validation_invalid_sign() -> None:
    """Any sign not in {-1, +1} must raise ValueError with named message."""
    must_raise(
        lambda: sol.decompose_trades([100.0, 100.1, 100.2], [1, 0, -1]),
        "sign equal to 0",
        contains=("each sign must be -1 or +1",),
    )
    must_raise(
        lambda: sol.decompose_trades([100.0, 100.1, 100.2], [1, 2, -1]),
        "sign equal to 2",
        contains=("each sign must be -1 or +1",),
    )


def test_validation_all_signs_equal() -> None:
    """All signs identical must raise ValueError for singular regression."""
    must_raise(
        lambda: sol.decompose_trades([100.0, 100.1, 100.2, 100.3], [1, 1, 1, 1]),
        "all signs +1",
        contains=("signs must vary: the regression is singular",),
    )
    must_raise(
        lambda: sol.decompose_trades([100.0, 99.9, 99.8, 99.7], [-1, -1, -1, -1]),
        "all signs -1",
        contains=("signs must vary: the regression is singular",),
    )


def test_nan_rules() -> None:
    """Positive lag-1 autocovariance produces NaN for Roll spread; H=0 produces NaN for share."""
    # Constant price increments -> cov1 = 0 >= 0, and H = 0
    p_flat = [100.0, 101.0, 102.0, 103.0, 104.0]
    s_mix = [1, 1, -1, -1, 1]
    res = sol.decompose_trades(p_flat, s_mix)
    expect(math.isnan(res["roll_spread"]), "Roll spread must be NaN when cov1 >= 0")
    expect(math.isnan(res["adverse_share"]), "Adverse share must be NaN when half_spread is zero")


def test_oracle_agreement_instance() -> None:
    """Outputs must match oracle within 1e-9 relative tolerance."""
    prices: list[float] = list(INST["prices"])
    signs: list[int] = list(INST["signs"])
    expected = oracle_decompose(prices, signs)
    actual = sol.decompose_trades(prices, signs)

    for k in KEYS:
        exp_val = expected[k]
        act_val = actual[k]
        if math.isnan(exp_val):
            expect(math.isnan(act_val), f"{k} should be NaN")
        else:
            tol = 1e-9 * max(1.0, abs(exp_val))
            diff = abs(act_val - exp_val)
            expect(diff <= tol, f"{k} differs from oracle by {diff:.2e} (tol {tol:.2e})")


def test_oracle_agreement_instance2() -> None:
    """Outputs on second independent instance must also match oracle."""
    prices: list[float] = list(INST2["prices"])
    signs: list[int] = list(INST2["signs"])
    expected = oracle_decompose(prices, signs)
    actual = sol.decompose_trades(prices, signs)

    for k in KEYS:
        exp_val = expected[k]
        act_val = actual[k]
        if math.isnan(exp_val):
            expect(math.isnan(act_val), f"{k} should be NaN")
        else:
            tol = 1e-9 * max(1.0, abs(exp_val))
            diff = abs(act_val - exp_val)
            expect(diff <= tol, f"{k} differs from oracle on second instance by {diff:.2e}")


def test_structural_identity() -> None:
    """Half-spread must equal order processing plus adverse selection."""
    prices: list[float] = list(INST["prices"])
    signs: list[int] = list(INST["signs"])
    res = sol.decompose_trades(prices, signs)

    h = res["half_spread"]
    c = res["order_processing"]
    th = res["adverse_selection"]
    id_gap = abs(h - (c + th))
    tol = 1e-12 * max(1.0, abs(h))
    expect(id_gap <= tol, f"Decomposition identity violated: |H - (c + theta)| = {id_gap:.2e}")


def test_invariance_location() -> None:
    """Adding a constant to all prices leaves all 5 outputs invariant."""
    prices: list[float] = list(INST["prices"])
    signs: list[int] = list(INST["signs"])
    base = sol.decompose_trades(prices, signs)

    shifted_prices = [p + 45.75 for p in prices]
    shifted = sol.decompose_trades(shifted_prices, signs)

    for k in KEYS:
        if math.isnan(base[k]):
            expect(math.isnan(shifted[k]), f"{k} should be NaN under price shift")
        else:
            diff = abs(shifted[k] - base[k])
            expect(diff <= 1e-9 * max(1.0, abs(base[k])), f"{k} is not shift-invariant")


def test_invariance_scale() -> None:
    """Multiplying all prices by positive factor scales components and preserves share."""
    prices: list[float] = list(INST["prices"])
    signs: list[int] = list(INST["signs"])
    base = sol.decompose_trades(prices, signs)

    k_scale = 2.5
    scaled_prices = [p * k_scale for p in prices]
    scaled = sol.decompose_trades(scaled_prices, signs)

    for k in ("roll_spread", "half_spread", "order_processing", "adverse_selection"):
        if math.isnan(base[k]):
            expect(math.isnan(scaled[k]), f"{k} should be NaN under scale")
        else:
            diff = abs(scaled[k] - k_scale * base[k])
            expect(diff <= 1e-9 * max(1.0, abs(k_scale * base[k])), f"{k} is not scale-covariant")

    if not math.isnan(base["adverse_share"]):
        diff_share = abs(scaled["adverse_share"] - base["adverse_share"])
        expect(diff_share <= 1e-9, "adverse_share must be scale-invariant")


def test_no_input_mutation() -> None:
    """decompose_trades must not mutate the input lists."""
    prices: list[float] = list(INST["prices"])
    signs: list[int] = list(INST["signs"])
    prices_copy = list(prices)
    signs_copy = list(signs)

    _ = sol.decompose_trades(prices, signs)
    expect(prices == prices_copy, "prices list was mutated by decompose_trades")
    expect(signs == signs_copy, "signs list was mutated by decompose_trades")
