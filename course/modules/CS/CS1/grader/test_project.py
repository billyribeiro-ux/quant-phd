"""Pytest test suite for Atlas A1 returns autograder.

Tests simple_return, log_return, invariants, edge cases, and error handling across per-learner seeds.
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

# Ensure src/ is on sys.path to import atlas.returns
src_dir = Path(__file__).parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

import pytest  # noqa: E402
from atlas.returns import log_return, simple_return  # type: ignore[import-not-found]  # noqa: E402
from instance import make_instance  # type: ignore[import-not-found]  # noqa: E402


@pytest.fixture(scope="module")
def instance_data() -> dict[str, object]:
    seed = int(os.environ.get("QF_SEED", "0"))
    inst = make_instance(seed)
    payload = json.loads(str(inst["payload"]))
    return payload  # type: ignore[no-any-return]


def test_simple_return_accuracy(instance_data: dict[str, object]) -> None:
    prices = instance_data["prices"]
    assert isinstance(prices, list)
    expected_simple = instance_data["ref_simple"]
    assert isinstance(expected_simple, list)

    computed = simple_return(prices)
    assert isinstance(computed, list), "simple_return must return a list"
    assert len(computed) == len(prices) - 1, f"Expected {len(prices) - 1} returns, got {len(computed)}"

    for t in range(len(computed)):
        assert math.isclose(computed[t], expected_simple[t], rel_tol=1e-12, abs_tol=1e-15), (
            f"simple_return mismatch at index {t}: got {computed[t]}, expected {expected_simple[t]}"
        )


def test_log_return_accuracy(instance_data: dict[str, object]) -> None:
    prices = instance_data["prices"]
    assert isinstance(prices, list)
    expected_log = instance_data["ref_log"]
    assert isinstance(expected_log, list)

    computed = log_return(prices)
    assert isinstance(computed, list), "log_return must return a list"
    assert len(computed) == len(prices) - 1, f"Expected {len(prices) - 1} returns, got {len(computed)}"

    for t in range(len(computed)):
        assert math.isclose(computed[t], expected_log[t], rel_tol=1e-12, abs_tol=1e-15), (
            f"log_return mismatch at index {t}: got {computed[t]}, expected {expected_log[t]}"
        )


def test_return_mathematical_invariant(instance_data: dict[str, object]) -> None:
    prices = instance_data["prices"]
    assert isinstance(prices, list)
    r = simple_return(prices)
    ell = log_return(prices)

    for t in range(len(r)):
        expected_log = math.log(1.0 + r[t])
        assert math.isclose(ell[t], expected_log, rel_tol=1e-12), (
            f"Invariant ell_t == ln(1 + r_t) violated at t={t}: ell={ell[t]}, ln(1+r)={expected_log}"
        )


def test_compounding_identities(instance_data: dict[str, object]) -> None:
    prices = instance_data["prices"]
    assert isinstance(prices, list)
    r = simple_return(prices)
    ell = log_return(prices)

    # Multi-period product: prod(1 + r_t) == P_T / P_0
    prod_r = math.prod(1.0 + ret for ret in r)
    expected_ratio = prices[-1] / prices[0]
    assert math.isclose(prod_r, expected_ratio, rel_tol=1e-12), (
        f"Multi-period compounding product {prod_r} != price ratio {expected_ratio}"
    )

    # Multi-period sum: sum(ell_t) == ln(P_T / P_0)
    sum_ell = sum(ell)
    expected_log_ratio = math.log(prices[-1] / prices[0])
    assert math.isclose(sum_ell, expected_log_ratio, rel_tol=1e-12), (
        f"Multi-period log return sum {sum_ell} != ln(price ratio) {expected_log_ratio}"
    )


def test_sequence_types_and_immutability(instance_data: dict[str, object]) -> None:
    prices = instance_data["prices"]
    assert isinstance(prices, list)
    prices_copy = list(prices)
    prices_tuple = tuple(prices)

    r_list = simple_return(prices)
    r_tuple = simple_return(prices_tuple)

    assert r_list == r_tuple, "simple_return must handle any Sequence[float]"
    assert prices == prices_copy, "simple_return must not mutate input sequence"

    ell_list = log_return(prices)
    ell_tuple = log_return(prices_tuple)

    assert ell_list == ell_tuple, "log_return must handle any Sequence[float]"
    assert prices == prices_copy, "log_return must not mutate input sequence"


def test_invalid_inputs_raise_value_error(instance_data: dict[str, object]) -> None:
    invalid_cases = instance_data["invalid_cases"]
    assert isinstance(invalid_cases, list)

    for case in invalid_cases:
        assert isinstance(case, dict)
        bad_prices = case["prices"]
        with pytest.raises(ValueError):
            simple_return(bad_prices)
        with pytest.raises(ValueError):
            log_return(bad_prices)


def test_non_numeric_type_error() -> None:
    bad_inputs: list[object] = [["100.0", "105.0"], [None, 100.0]]
    for bad in bad_inputs:
        with pytest.raises(TypeError):
            simple_return(bad)
        with pytest.raises(TypeError):
            log_return(bad)
