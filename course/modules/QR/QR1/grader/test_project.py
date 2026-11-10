"""Pytest test suite for QR1 research data engineering autograder.

Tests vintage-aware ingestion, point-in-time no-look-ahead queries,
UTC timestamp normalization, prevailing tick selection, and split adjustments.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

# Ensure workspace root is importable
workspace_dir = Path(__file__).parent
if str(workspace_dir) not in sys.path:
    sys.path.insert(0, str(workspace_dir))

import pytest  # noqa: E402

try:
    from vintages import (  # type: ignore[import-not-found]
        VintageIndex,
        adjust_closes,
        et_to_utc,
        last_trade_at,
    )
except ImportError:
    from reference import (  # type: ignore[import-not-found]
        VintageIndex,
        adjust_closes,
        et_to_utc,
        last_trade_at,
    )

from instance import make_instance  # type: ignore[import-not-found]  # noqa: E402


@pytest.fixture(scope="module")
def instance_data() -> dict[str, Any]:
    seed = int(os.environ.get("QF_SEED", "0"))
    inst = make_instance(seed)
    payload: dict[str, Any] = json.loads(str(inst["payload"]))
    return payload


# --- T1 & T2 & T3: Vintage Indexing & No-Look-Ahead Queries ---


def test_t1_t2_t3_vintage_queries_and_no_lookahead(
    instance_data: dict[str, Any],
    tmp_path: Path,
) -> None:
    db_path = str(tmp_path / "vintages_test.db")
    vindex = VintageIndex(db_path)

    vintages = instance_data["vintages"]
    # Record all vintages
    for v in vintages:
        vindex.record(
            v["source"],
            v["series"],
            v["obs_date"],
            v["value"],
            v["published"],
            v["retrieved"],
        )

    # T2: Visible query equals brute-force oracle
    for cutoff in instance_data["cutoffs"]:
        for v in vintages:
            actual = vindex.visible(v["source"], v["series"], v["obs_date"], cutoff)
            # Brute force oracle
            eligible = [
                x
                for x in vintages
                if x["source"] == v["source"]
                and x["series"] == v["series"]
                and x["obs_date"] == v["obs_date"]
                and x["published"] <= cutoff
            ]
            expected = eligible[-1]["value"] if eligible else None
            assert actual == expected, (
                f"visible({v['source']}, {v['series']}, {v['obs_date']}, {cutoff}) returned {actual!r}, "
                f"expected oracle {expected!r}. Check point-in-time publication filtering."
            )

    # T3: visible_series equals map of visible over observation dates
    for cutoff in instance_data["cutoffs"]:
        series_map = vindex.visible_series("fred", "CORE_CPI", cutoff)
        all_obs_dates = {v["obs_date"] for v in vintages if v["source"] == "fred" and v["series"] == "CORE_CPI"}
        for od in all_obs_dates:
            single_val = vindex.visible("fred", "CORE_CPI", od, cutoff)
            if single_val is None:
                assert od not in series_map, f"Observation date {od} should not appear in visible_series at {cutoff}"
            else:
                assert series_map.get(od) == single_val, (
                    f"visible_series({od}) is {series_map.get(od)!r}, expected {single_val!r}"
                )

    # T1: Invariance: adding a vintage published in the future does not alter queries at cutoff
    test_cutoff = instance_data["cutoffs"][1]
    val_before = vindex.visible("fred", "CORE_CPI", vintages[0]["obs_date"], test_cutoff)

    # Record a future revision published long after test_cutoff
    vindex.record(
        "fred",
        "CORE_CPI",
        vintages[0]["obs_date"],
        "999.99",
        "2099-01-01T00:00:00Z",
        "2099-01-01T00:01:00Z",
    )
    val_after = vindex.visible("fred", "CORE_CPI", vintages[0]["obs_date"], test_cutoff)
    assert val_before == val_after, (
        "Look-ahead contamination: visible value at past cutoff changed after adding future vintage!"
    )

    vindex.close()


# --- T4 & T5: Timestamp Normalization & DST Transitions ---


def test_t4_et_to_utc_anchors() -> None:
    anchors = [
        ("2026-01-15 12:00", "2026-01-15T17:00:00Z"),  # Standard time (UTC-5)
        ("2026-07-01 12:00", "2026-07-01T16:00:00Z"),  # Daylight time (UTC-4)
        ("2026-03-08 01:59", "2026-03-08T06:59:00Z"),  # Pre-spring gap (EST)
        ("2026-03-08 03:00", "2026-03-08T07:00:00Z"),  # Post-spring gap (EDT)
        ("2026-11-01 01:30", "2026-11-01T05:30:00Z"),  # Fall overlap earlier instant (EDT)
    ]
    for wall_in, expected_utc in anchors:
        actual_utc = et_to_utc(wall_in)
        assert actual_utc == expected_utc, f"et_to_utc({wall_in}) = {actual_utc}, expected {expected_utc}"


def test_t5_et_to_utc_spring_gap() -> None:
    # 2026-03-08 02:00 through 02:59 does not exist in Eastern time
    with pytest.raises(ValueError, match=r"gap|exist|invalid"):
        et_to_utc("2026-03-08 02:00")
    with pytest.raises(ValueError, match=r"gap|exist|invalid"):
        et_to_utc("2026-03-08 02:30")
    # Surrounding times are valid
    assert et_to_utc("2026-03-08 01:59") == "2026-03-08T06:59:00Z"
    assert et_to_utc("2026-03-08 03:00") == "2026-03-08T07:00:00Z"


# --- T6: Prevailing Tick Resolution ---


def test_t6_last_trade_at(instance_data: dict[str, Any]) -> None:
    ticks = instance_data["ticks"]
    cutoffs = instance_data["tick_cutoffs"]

    for cutoff in cutoffs:
        actual = last_trade_at(ticks, cutoff)
        eligible = [t for t in ticks if t[0] <= cutoff]
        expected = max(eligible, key=lambda t: (t[0], t[1]))[2] if eligible else None
        assert actual == expected, (
            f"last_trade_at for cutoff {cutoff} returned {actual}, expected {expected}. "
            f"Verify ordering on (timestamp, seq)."
        )


# --- T7: Corporate Action Split Adjustment ---


def test_t7_adjust_closes(instance_data: dict[str, Any]) -> None:
    dates = instance_data["stock_dates"]
    closes = instance_data["stock_closes"]
    splits = instance_data["stock_splits"]

    adjusted = adjust_closes(dates, closes, splits)
    assert len(adjusted) == len(closes), "Adjusted closes length mismatch"

    # Split invariance: adjusted simple return across split ex-date must be 0 within 1e-12 relative
    split_ex_date = splits[0][0]
    split_idx = dates.index(split_ex_date)
    adj_ret = (adjusted[split_idx] / adjusted[split_idx - 1]) - 1.0
    assert abs(adj_ret) <= 1e-12, f"Split return invariance failed: adjusted return across split is {adj_ret:+.2e}"

    # Ex-date boundary: close on ex-date is unadjusted by this split event
    assert abs(adjusted[split_idx] - closes[split_idx]) < 1e-9

    # Length mismatch raises ValueError (E6)
    with pytest.raises(ValueError, match=r"length|mismatch"):
        adjust_closes(dates[:-1], closes, splits)

    # Non-positive ratio raises ValueError (E6)
    with pytest.raises(ValueError, match=r"ratio|positive"):
        adjust_closes(dates, closes, [(split_ex_date, 0.0)])
    with pytest.raises(ValueError, match=r"ratio|positive"):
        adjust_closes(dates, closes, [(split_ex_date, -1.5)])


# --- T8 & T9 & T10: Error Handling & Invariants ---


def test_t8_record_invariants(tmp_path: Path) -> None:
    db_path = str(tmp_path / "invariants.db")
    vindex = VintageIndex(db_path)

    # Valid record
    vindex.record("fred", "GDP", "2026-01-01", "100.0", "2026-02-01T12:00:00Z", "2026-02-01T12:05:00Z")

    # Idempotent re-record
    vindex.record("fred", "GDP", "2026-01-01", "100.0", "2026-02-01T12:00:00Z", "2026-02-01T12:05:00Z")

    # Retrieved < published raises ValueError (E3)
    with pytest.raises(ValueError, match=r"retrieved|precede"):
        vindex.record("fred", "GDP", "2026-01-01", "100.0", "2026-02-01T12:00:00Z", "2026-02-01T11:00:00Z")

    # Conflicting value for same (source, series, obs_date, published) raises ValueError (E3)
    with pytest.raises(ValueError, match=r"conflict|existing"):
        vindex.record("fred", "GDP", "2026-01-01", "999.0", "2026-02-01T12:00:00Z", "2026-02-01T12:05:00Z")

    # Source not in SOURCES raises ValueError (E3)
    with pytest.raises(ValueError, match=r"source"):
        vindex.record("bloomberg", "GDP", "2026-01-01", "100.0", "2026-02-01T12:00:00Z", "2026-02-01T12:05:00Z")

    # Timestamp without Z raises ValueError (E3)
    with pytest.raises(ValueError, match=r"timestamp|ISO"):
        vindex.record("fred", "GDP", "2026-01-01", "100.0", "2026-02-01 12:00:00", "2026-02-01T12:05:00Z")

    vindex.close()


def test_t9_visible_naive_timestamp_and_missing_series(tmp_path: Path) -> None:
    db_path = str(tmp_path / "visible_err.db")
    vindex = VintageIndex(db_path)

    # Naive timestamp raises ValueError (E4)
    with pytest.raises(ValueError, match=r"timestamp|ISO"):
        vindex.visible("fred", "GDP", "2026-01-01", "2026-02-01 12:00:00")
    with pytest.raises(ValueError, match=r"timestamp|ISO"):
        vindex.visible_series("fred", "GDP", "2026-02-01 12:00:00")

    # Missing series returns None or empty dict
    assert vindex.visible("fred", "NONEXISTENT", "2026-01-01", "2026-02-01T12:00:00Z") is None
    assert vindex.visible_series("fred", "NONEXISTENT", "2026-02-01T12:00:00Z") == {}

    vindex.close()


def test_t10_last_trade_naive_timestamp() -> None:
    ticks = [("2026-01-01T09:30:00Z", 1, 100.0)]
    with pytest.raises(ValueError, match=r"timestamp|ISO"):
        last_trade_at(ticks, "2026-01-01 09:30:00")
    assert last_trade_at([], "2026-01-01T09:30:00Z") is None


def test_t11_instance_invalid_case(instance_data: dict[str, Any], tmp_path: Path) -> None:
    inv = instance_data["invalid"]
    func_name = inv["func"]
    kwargs = inv["kwargs"]

    if func_name == "VintageIndex":
        with pytest.raises(ValueError):
            VintageIndex(**kwargs)
    elif func_name == "et_to_utc":
        with pytest.raises(ValueError):
            et_to_utc(**kwargs)
    elif func_name == "last_trade_at":
        with pytest.raises(ValueError):
            last_trade_at(**kwargs)
    elif func_name == "adjust_closes":
        with pytest.raises(ValueError):
            adjust_closes(**kwargs)
    elif func_name in ("record", "visible"):
        db_path = str(tmp_path / "inv_case.db")
        vindex = VintageIndex(db_path)
        try:
            with pytest.raises(ValueError):
                getattr(vindex, func_name)(**kwargs)
        finally:
            vindex.close()
