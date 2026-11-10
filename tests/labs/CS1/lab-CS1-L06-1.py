"""CS1 lab L06: Unit testing with pytest assertions and exception checks.

Uses pytest to demonstrate test fixtures, invariant assertions, and pytest.raises.
SIMULATED financial instruments.
"""

from __future__ import annotations

import math
from collections.abc import Callable

import pytest


def calculate_yield(face: float, price: float, maturity: float) -> float:
    """Calculate annualized zero-coupon yield: (face / price)**(1/maturity) - 1."""
    if price <= 0.0 or face <= 0.0:
        raise ValueError("Price and face value must be strictly positive")
    if maturity <= 0.0:
        raise ValueError("Maturity must be strictly positive")
    return float((face / price) ** (1.0 / maturity) - 1.0)


# --- Unit Tests ---


def test_calculate_yield_positive() -> None:
    """Check standard yield value on annual zero."""
    y = calculate_yield(100.0, 95.0, 1.0)
    expected = 100.0 / 95.0 - 1.0
    assert math.isclose(y, expected, rel_tol=1e-12)


def test_calculate_yield_multiyear() -> None:
    """Check compounding over multiyear maturity."""
    y = calculate_yield(100.0, 80.0, 2.0)
    expected = (100.0 / 80.0) ** 0.5 - 1.0
    assert math.isclose(y, expected, rel_tol=1e-12)


def test_calculate_yield_invalid_price() -> None:
    """Check that nonpositive price raises ValueError with pytest.raises."""
    with pytest.raises(ValueError, match="strictly positive"):
        calculate_yield(100.0, -95.0, 1.0)


def test_calculate_yield_invalid_maturity() -> None:
    """Check that nonpositive maturity raises ValueError with pytest.raises."""
    with pytest.raises(ValueError, match="strictly positive"):
        calculate_yield(100.0, 95.0, 0.0)


def test_deliberate_assertion_failure() -> None:
    """Deliberately failing assertion to inspect failure reporting."""
    assert 2 + 2 == 5, "deliberate math mismatch"


def main() -> None:
    # Run test suite programmatically
    suite: list[tuple[str, Callable[[], None]]] = [
        ("test_calculate_yield_positive", test_calculate_yield_positive),
        ("test_calculate_yield_multiyear", test_calculate_yield_multiyear),
        ("test_calculate_yield_invalid_price", test_calculate_yield_invalid_price),
        ("test_calculate_yield_invalid_maturity", test_calculate_yield_invalid_maturity),
    ]

    passed = 0
    for name, test_func in suite:
        try:
            test_func()
            passed += 1
            print(f"RUN {name}: PASS")
        except Exception as exc:
            print(f"RUN {name}: FAIL ({exc})")

    print(f"passed: {passed} of {len(suite)}")

    # Verify that the failing test raises AssertionError
    caught_assertion = False
    try:
        test_deliberate_assertion_failure()
    except AssertionError as exc:
        caught_assertion = True
        print(f"caught expected AssertionError: '{exc}'")

    print(f"deliberate failure caught: {caught_assertion}")


main()
