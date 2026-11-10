"""Acceptance test suite for X1 project: Meese-Rogoff re-run (meese_rogoff.py).

Dual-mode: runs identically in the browser (Pyodide) and locally:
    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error grader/test_project.py
"""

from __future__ import annotations

import importlib
import math
import os
from collections.abc import Callable
from typing import Any

import pytest

sol: Any = importlib.import_module(os.environ.get("QF_SOL", "meese_rogoff"))
make_instance: Callable[[int], dict[str, Any]] = importlib.import_module("instance").make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)


def expect(condition: bool, hint: str) -> None:
    """Fail with a descriptive hint if condition is false."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(hint, pytrace=False)


def must_raise(call: Callable[[], object], condition: str, *, substring: str = "") -> None:
    """Check that call() raises ValueError with optional required substring."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError as err:
        if substring and substring not in str(err):
            pytest.fail(
                f"{condition}: ValueError message must contain '{substring}' (got: {err})",
                pytrace=False,
            )
        return
    except Exception as exc:
        pytest.fail(f"{condition}: expected ValueError, got {type(exc).__name__}: {exc}", pytrace=False)
    pytest.fail(f"{condition}: expected ValueError, none was raised", pytrace=False)


def test_input_validation() -> None:
    """Test required ValueError exceptions on invalid inputs."""
    s_valid = [0.1 * i for i in range(50)]
    f_valid = [0.05 * i for i in range(50)]
    i_valid = [0.001 * i for i in range(50)]

    must_raise(
        lambda: sol.rolling_forecast_rw(s_valid, 0, 20),
        "horizon <= 0 in RW",
        substring="horizon must be positive",
    )
    must_raise(
        lambda: sol.rolling_forecast_rw(s_valid, 1, 5),
        "window_size < 10 in RW",
        substring="window_size must be at least 10",
    )
    must_raise(
        lambda: sol.rolling_forecast_rw(s_valid[:15], 10, 12),
        "insufficient observations in RW",
        substring="insufficient observations",
    )

    must_raise(
        lambda: sol.rolling_forecast_fundamentals(s_valid, f_valid[:40], 1, 20),
        "mismatched series lengths in fundamentals",
        substring="series lengths must match",
    )
    must_raise(
        lambda: sol.rolling_forecast_uip(s_valid, i_valid[:30], 1, 20),
        "mismatched series lengths in UIP",
        substring="series lengths must match",
    )

    bad_inst = dict(INST)
    bad_inst["initial_price"] = -1.0
    must_raise(
        lambda: sol.run_meese_rogoff(bad_inst),
        "negative initial price in run_meese_rogoff",
        substring="initial_price must be positive",
    )


def test_rw_forecast_properties() -> None:
    """Verify that driftless random-walk forecast equals current spot exchange rate s_t."""
    s_series = INST["s_series"]
    window_size = INST["window_size"]
    h = 3

    preds = sol.rolling_forecast_rw(s_series, h, window_size)
    expected_count = len(s_series) - window_size - h
    expect(
        len(preds) == expected_count,
        f"RW forecast count should be {expected_count}, got {len(preds)}",
    )

    # In a driftless random walk, the forecast for step t + h made at step t is s_t
    # Check that predictions match s_series[t] for each evaluation step t
    for idx, t in enumerate(range(window_size, len(s_series) - h)):
        expect(
            abs(preds[idx] - s_series[t]) < 1e-4,
            f"RW forecast at eval index {idx} (t={t}) should be {s_series[t]}, got {preds[idx]}",
        )


def test_fundamentals_forecast_properties() -> None:
    """Verify that fundamentals regression forecast uses OLS on window and realized f_{t+h}."""
    s_series = INST["s_series"]
    f_series = INST["f_series"]
    window_size = INST["window_size"]
    h = 1

    preds = sol.rolling_forecast_fundamentals(s_series, f_series, h, window_size)
    expected_count = len(s_series) - window_size - h
    expect(
        len(preds) == expected_count,
        f"Fundamentals forecast count should be {expected_count}, got {len(preds)}",
    )

    # Manual verification of first prediction at t = window_size
    t = window_size
    s_win = s_series[t - window_size : t]
    f_win = f_series[t - window_size : t]
    mean_s = sum(s_win) / window_size
    mean_f = sum(f_win) / window_size
    var_f = sum((f - mean_f) ** 2 for f in f_win)
    cov_sf = sum((f - mean_f) * (s - mean_s) for s, f in zip(s_win, f_win, strict=True))
    beta = cov_sf / var_f
    alpha = mean_s - beta * mean_f
    expected_pred = alpha + beta * f_series[t + h]

    expect(
        abs(preds[0] - expected_pred) < 1e-4,
        f"First fundamentals forecast should match manual OLS {expected_pred:.4f}, got {preds[0]:.4f}",
    )


def test_metrics_and_theil_u_properties() -> None:
    """Verify RMSE, MAE, and Theil's U calculation."""
    actual = [1.0, 1.2, 0.9, 1.1, 1.05]
    pred_good = [1.02, 1.18, 0.92, 1.08, 1.03]  # close
    pred_bad = [1.20, 1.40, 0.70, 1.30, 1.25]  # further away

    m_good = sol.compute_metrics(actual, pred_good)
    m_bad = sol.compute_metrics(actual, pred_bad)

    # Manual calculation for good:
    # errors: [-0.02, 0.02, -0.02, 0.02, 0.02]
    # sq errors: 5 * 0.0004 = 0.0020; mean = 0.0004; sqrt = 0.02
    expect(
        abs(m_good["rmse"] - 0.02) < 1e-4,
        f"RMSE should be 0.02, got {m_good['rmse']}",
    )
    expect(
        abs(m_good["mae"] - 0.02) < 1e-4,
        f"MAE should be 0.02, got {m_good['mae']}",
    )

    # Invertibility check: Theil's U must be RMSE_model / RMSE_benchmark
    # When model is bad and bench is good, U > 1.0
    theil_u = m_bad["rmse"] / m_good["rmse"]
    expect(
        theil_u > 1.0,
        f"Theil's U for bad model against good benchmark must be > 1.0, got {theil_u}",
    )

    # Manual test vector ensuring RMSE != MAE
    v_act = [0.0, 0.0, 0.0, 0.0]
    v_pred = [1.0, 2.0, 3.0, 4.0]
    m_v = sol.compute_metrics(v_act, v_pred)
    # MAE = (1 + 2 + 3 + 4)/4 = 2.5
    # RMSE = sqrt((1 + 4 + 9 + 16)/4) = sqrt(30/4) = sqrt(7.5) = 2.7386
    expect(
        abs(m_v["mae"] - 2.5) < 1e-4,
        f"MAE must be 2.5, got {m_v['mae']}",
    )
    expect(
        abs(m_v["rmse"] - math.sqrt(7.5)) < 1e-4,
        f"RMSE must be sqrt(7.5), got {m_v['rmse']}",
    )
    expect(
        abs(m_v["rmse"] - m_v["mae"]) > 0.1,
        "RMSE and MAE must be distinct on non-uniform errors",
    )


def test_diebold_mariano_test() -> None:
    """Verify Diebold-Mariano test statistic and Bartlett HAC weighting for h > 1."""
    actual = [1.0, 1.1, 1.05, 0.95, 1.0, 1.08, 0.98, 1.02, 1.06, 1.01]
    # Identical predictions should have DM stat = 0.0
    dm_zero = sol.compute_diebold_mariano(actual, actual, actual, 1)
    expect(
        abs(dm_zero) < 1e-6,
        f"DM stat for identical forecasts should be 0.0, got {dm_zero}",
    )

    # Model with higher errors than benchmark should have positive DM stat
    pred_model = [a + (0.05 + 0.02 * (i % 3)) for i, a in enumerate(actual)]
    pred_bench = [a + 0.01 for a in actual]
    dm_pos = sol.compute_diebold_mariano(actual, pred_model, pred_bench, 1)
    expect(
        dm_pos > 0.0,
        f"DM stat should be positive when model has higher loss, got {dm_pos}",
    )

    # For multi-step horizon h=3, Bartlett weighting should yield different variance than h=1
    dm_h1 = sol.compute_diebold_mariano(actual, pred_model, pred_bench, 1)
    dm_h3 = sol.compute_diebold_mariano(actual, pred_model, pred_bench, 3)
    expect(
        abs(dm_h3 - dm_h1) > 0.1,
        f"Bartlett HAC adjustment must modify DM stat for h=3 ({dm_h3}) vs h=1 ({dm_h1})",
    )


def test_full_horse_race_execution() -> None:
    """Verify run_meese_rogoff executes across all seeded horizons and generates valid stats."""
    res = sol.run_meese_rogoff(INST)

    expect("results" in res, "run_meese_rogoff must return 'results' dictionary")
    results = res["results"]

    for h in INST["horizons"]:
        expect(h in results, f"Horizon {h} must be present in results")
        h_res = results[h]
        expected_evals = INST["n_obs"] - INST["window_size"] - h
        expect(
            h_res["eval_count"] == expected_evals,
            f"Eval count for h={h} should be {expected_evals}, got {h_res['eval_count']}",
        )
        expect(h_res["rw_rmse"] > 0.0, "RW RMSE must be positive")
        expect(h_res["fund_rmse"] > 0.0, "Fundamentals RMSE must be positive")
        expect(h_res["uip_rmse"] > 0.0, "UIP RMSE must be positive")

        # Theil's U = RMSE_model / RMSE_RW
        expected_theil_u = round(h_res["fund_rmse"] / h_res["rw_rmse"], 4)
        expect(
            abs(h_res["fund_theil_u"] - expected_theil_u) < 1e-3,
            f"Theil's U should match ratio of RMSEs {expected_theil_u}, got {h_res['fund_theil_u']}",
        )
