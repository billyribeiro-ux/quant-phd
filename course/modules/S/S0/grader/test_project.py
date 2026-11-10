"""Pytest test suite for Atlas A3 data-quality autograder.

Tests input validation, gap detection, split-adjusted log returns, corporate-action breaks,
MAD-based outlier detection, stale runs, and invariant properties across random seeds.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

# Ensure src/ is on sys.path to import atlas.dataquality
src_dir = Path(__file__).parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

import pytest  # noqa: E402

try:
    from atlas.dataquality import profile  # type: ignore[import-not-found]
except ImportError:
    from reference import profile  # type: ignore[import-not-found,no-redef]

from instance import make_instance  # type: ignore[import-not-found]  # noqa: E402


@pytest.fixture(scope="module")
def instance_payload() -> dict[str, Any]:
    seed = int(os.environ.get("QF_SEED", "0"))
    inst = make_instance(seed)
    payload_obj = json.loads(str(inst["payload"]))
    assert isinstance(payload_obj, dict)
    return payload_obj


def test_schema_and_types(instance_payload: dict[str, Any]) -> None:
    ds = instance_payload["dataset"]
    report = profile(ds)

    required_keys = {"name", "rows", "gaps", "stale_runs", "corporate_action_breaks", "outliers"}
    assert set(report.keys()) == required_keys, f"Expected keys {required_keys}, got {set(report.keys())}"

    assert isinstance(report["name"], str), "report['name'] must be a str"
    assert isinstance(report["rows"], int), "report['rows'] must be an int"
    assert report["rows"] == len(ds["date"]), f"report['rows'] {report['rows']} != date length {len(ds['date'])}"

    for list_key in ("gaps", "stale_runs", "corporate_action_breaks", "outliers"):
        lst = report[list_key]
        assert isinstance(lst, list), f"report[{list_key!r}] must be a list"

    # Sorted ascending and unique
    for list_key in ("gaps", "corporate_action_breaks", "outliers"):
        lst = report[list_key]
        for x in lst:
            assert isinstance(x, int), f"indices in report[{list_key!r}] must be ints"
        assert lst == sorted(set(lst)), f"report[{list_key!r}] must be strictly ascending with no duplicates"

    for item in report["stale_runs"]:
        assert isinstance(item, tuple) and len(item) == 2, f"stale run must be a 2-tuple (start, end), got {item!r}"
        assert isinstance(item[0], int) and isinstance(item[1], int), "stale run endpoints must be ints"
        assert item[0] <= item[1], f"stale run start ({item[0]}) must be <= end ({item[1]})"


def test_gaps_detection(instance_payload: dict[str, Any]) -> None:
    ds = instance_payload["dataset"]
    report = profile(ds)
    expected = instance_payload["expected_gaps"]
    assert report["gaps"] == expected, f"Gaps mismatch: detected {report['gaps']}, expected planted {expected}"


def test_stale_runs_detection(instance_payload: dict[str, Any]) -> None:
    ds = instance_payload["dataset"]
    report = profile(ds)
    expected = [tuple(x) for x in instance_payload["expected_stale_runs"]]
    assert report["stale_runs"] == expected, (
        f"Stale runs mismatch: detected {report['stale_runs']}, expected planted {expected}"
    )


def test_corporate_action_breaks_detection(instance_payload: dict[str, Any]) -> None:
    ds = instance_payload["dataset"]
    report = profile(ds)
    expected = instance_payload["expected_breaks"]
    assert report["corporate_action_breaks"] == expected, (
        f"Corporate action breaks mismatch: detected {report['corporate_action_breaks']}, expected {expected}"
    )


def test_outliers_detection(instance_payload: dict[str, Any]) -> None:
    ds = instance_payload["dataset"]
    report = profile(ds)
    expected = instance_payload["expected_outliers"]
    assert report["outliers"] == expected, f"Outliers mismatch: detected {report['outliers']}, expected {expected}"


def test_legitimate_split_handled(instance_payload: dict[str, Any]) -> None:
    ds = instance_payload["dataset"]
    report = profile(ds)
    split_row = instance_payload["split_row"]
    assert split_row not in report["corporate_action_breaks"], (
        f"Row {split_row} with valid split_ratio was incorrectly flagged as corporate-action break"
    )
    assert split_row not in report["outliers"], (
        f"Row {split_row} with valid split_ratio was incorrectly flagged as outlier"
    )


def test_invariants(instance_payload: dict[str, Any]) -> None:
    ds = instance_payload["dataset"]
    report = profile(ds)
    n_rows = report["rows"]

    # Bounds
    for idx in report["gaps"]:
        assert 0 <= idx < n_rows, f"Gap index {idx} out of range [0, {n_rows})"
    for idx in report["corporate_action_breaks"]:
        assert 0 <= idx < n_rows, f"Break index {idx} out of range [0, {n_rows})"
    for idx in report["outliers"]:
        assert 0 <= idx < n_rows, f"Outlier index {idx} out of range [0, {n_rows})"
    for start, end in report["stale_runs"]:
        assert 0 <= start <= end < n_rows, f"Stale run ({start}, {end}) out of range [0, {n_rows})"

    # Disjointness: breaks cannot be reported as outliers
    overlap = set(report["corporate_action_breaks"]) & set(report["outliers"])
    assert not overlap, f"A break is never also reported as an outlier; found overlapping indices: {overlap}"

    # Gaps cannot be inside a stale run (gap ends a run)
    for start, end in report["stale_runs"]:
        for g in report["gaps"]:
            assert not (start <= g <= end), f"Gap row {g} cannot sit inside stale run ({start}, {end})"


def test_clean_dataset_no_false_positives(instance_payload: dict[str, Any]) -> None:
    clean_ds = instance_payload["clean_dataset"]
    report = profile(clean_ds)
    assert report["gaps"] == [], f"Clean dataset produced false gap flags: {report['gaps']}"
    assert report["stale_runs"] == [], f"Clean dataset produced false stale run flags: {report['stale_runs']}"
    assert report["corporate_action_breaks"] == [], (
        f"Clean dataset produced false break flags: {report['corporate_action_breaks']}"
    )
    assert report["outliers"] == [], f"Clean dataset produced false outlier flags: {report['outliers']}"


def test_zero_scale_mad_raises_value_error(instance_payload: dict[str, Any]) -> None:
    zero_ds = instance_payload["zero_scale_dataset"]
    with pytest.raises(ValueError, match=r".*"):
        profile(zero_ds)


def test_invalid_inputs_raise_value_error(instance_payload: dict[str, Any]) -> None:
    invalid_cases = instance_payload["invalid_cases"]
    for case in invalid_cases:
        bad_ds = case["dataset"]
        with pytest.raises(ValueError):
            profile(bad_ds)


def test_parameter_validation(instance_payload: dict[str, Any]) -> None:
    ds = instance_payload["clean_dataset"]

    # Invalid stale_run (< 2 or not int)
    for bad_sr in (1, 0, -1, 3.5, True, False):
        with pytest.raises(ValueError):
            profile(ds, stale_run=bad_sr)

    # Invalid outlier_k (<= 0 or not finite)
    for bad_k in (0.0, -1.0, float("nan"), float("inf"), True, False):
        with pytest.raises(ValueError):
            profile(ds, outlier_k=bad_k)

    # Invalid break_log (<= 0 or not finite)
    for bad_bl in (0.0, -0.25, float("nan"), float("inf"), True, False):
        with pytest.raises(ValueError):
            profile(ds, break_log=bad_bl)
