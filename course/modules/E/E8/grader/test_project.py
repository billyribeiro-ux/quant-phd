"""Acceptance test suite for E8 CIP-basis monitor project.

Tests implied dollar borrowing rates, cross-currency basis in basis points,
quarter-end date identification (including weekend roll rules),
and table monitoring with input validation.
"""

from __future__ import annotations

import math
import os
from typing import Any

import pytest
from instance import make_instance
from reference import (
    cross_currency_basis_bp,
    implied_usd_rate,
    is_quarter_end,
    monitor_table,
)

pytestmark = pytest.mark.filterwarnings("error")

_SEED = int(os.environ.get("QF_SEED", "0"))
_INST: dict[str, Any] = make_instance(_SEED)


def close(a: float, b: float, tol: float = 1e-7) -> bool:
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= tol * (1.0 + abs(b))


def test_cip_forward_identity() -> None:
    """T01: When forward equals theoretical CIP forward, implied rate equals cash USD rate."""
    __tracebackhide__ = True
    spot = 1.10
    usd_rate = 0.05
    foreign_rate = 0.03
    tau_usd = 90.0 / 360.0
    tau_foreign = 90.0 / 360.0

    # CIP forward
    f_cip = spot * (1.0 + foreign_rate * tau_foreign) / (1.0 + usd_rate * tau_usd)
    r_implied = implied_usd_rate(spot, f_cip, foreign_rate, tau_usd, tau_foreign)
    assert close(r_implied, usd_rate, tol=1e-9), (
        "implied_usd_rate must equal usd_rate when forward is theoretical CIP forward"
    )

    basis = cross_currency_basis_bp(spot, f_cip, usd_rate, foreign_rate, tau_usd, tau_foreign)
    assert abs(basis) < 1e-9, f"cross_currency_basis_bp must return 0.0 bp under frictionless CIP, got {basis}"


def test_basis_sign_and_units() -> None:
    """T02: Basis is returned in basis points with sign convention (usd_rate - implied_usd) * 10000."""
    __tracebackhide__ = True
    spot = 1.10
    usd_rate = 0.05
    foreign_rate = 0.03
    tau = 0.25

    # Case 1: Expensive synthetic dollars (forward dollar stronger -> F lower)
    # Target basis = -30.0 bp -> implied_usd = 0.05 - (-0.0030) = 0.0530
    target_basis_neg = -30.0
    r_implied_high = usd_rate - (target_basis_neg / 10000.0)
    f_high = spot * (1.0 + foreign_rate * tau) / (1.0 + r_implied_high * tau)

    basis_neg = cross_currency_basis_bp(spot, f_high, usd_rate, foreign_rate, tau, tau)
    assert close(basis_neg, target_basis_neg, tol=1e-5), (
        f"Negative basis of {target_basis_neg} bp must return approximately {target_basis_neg}, got {basis_neg}"
    )

    # Case 2: Cheap synthetic dollars (forward dollar weaker -> F higher)
    target_basis_pos = +25.0
    r_implied_low = usd_rate - (target_basis_pos / 10000.0)
    f_low = spot * (1.0 + foreign_rate * tau) / (1.0 + r_implied_low * tau)

    basis_pos = cross_currency_basis_bp(spot, f_low, usd_rate, foreign_rate, tau, tau)
    assert close(basis_pos, target_basis_pos, tol=1e-5), (
        f"Positive basis of {target_basis_pos} bp must return approximately {target_basis_pos}, got {basis_pos}"
    )

    # Units check: must be in basis points, not decimal
    assert abs(basis_neg) > 1.0, f"Basis must be in basis points (e.g. -30.0), not decimal: {basis_neg}"


def test_accrual_fraction_sensitivity() -> None:
    """T03: Basis computation correctly respects day count accrual fractions."""
    __tracebackhide__ = True
    spot = 1.20
    forward = 1.19
    usd_rate = 0.04
    foreign_rate = 0.02
    tau_90 = 90.0 / 360.0
    tau_91 = 91.0 / 360.0

    b_90 = cross_currency_basis_bp(spot, forward, usd_rate, foreign_rate, tau_90, tau_90)
    b_91 = cross_currency_basis_bp(spot, forward, usd_rate, foreign_rate, tau_91, tau_90)

    # Implied rate varies with tau_usd
    assert not close(b_90, b_91, tol=1e-4), "Varying USD accrual fraction must change the computed basis"


def test_quarter_end_rules() -> None:
    """T04: is_quarter_end flags last weekday of March, June, September, December."""
    __tracebackhide__ = True
    # 2024:
    # March 31, 2024 was Sunday -> last weekday Friday March 29, 2024
    assert is_quarter_end("2024-03-29") is True, "2024-03-29 (Friday before Easter Sunday 31st) must be quarter end"
    assert is_quarter_end("2024-03-31") is False, "2024-03-31 (Sunday) is not a weekday"
    assert is_quarter_end("2024-03-28") is False, "2024-03-28 (Thursday) is not the last weekday"

    # June 30, 2024 was Sunday -> Friday June 28, 2024
    assert is_quarter_end("2024-06-28") is True, "2024-06-28 (Friday) must be quarter end"
    assert is_quarter_end("2024-06-30") is False, "2024-06-30 (Sunday) is not a weekday"

    # September 30, 2024 was Monday
    assert is_quarter_end("2024-09-30") is True, "2024-09-30 (Monday) must be quarter end"
    assert is_quarter_end("2024-09-27") is False, "2024-09-27 (Friday before Monday 30th) is not quarter end"

    # December 31, 2024 was Tuesday
    assert is_quarter_end("2024-12-31") is True, "2024-12-31 (Tuesday) must be quarter end"

    # Non-quarter-end months
    assert is_quarter_end("2024-01-31") is False
    assert is_quarter_end("2024-02-29") is False
    assert is_quarter_end("2024-04-30") is False
    assert is_quarter_end("2024-05-31") is False
    assert is_quarter_end("2024-07-31") is False
    assert is_quarter_end("2024-08-30") is False
    assert is_quarter_end("2024-10-31") is False
    assert is_quarter_end("2024-11-29") is False


def test_input_validation_exceptions() -> None:
    """T05: Functions raise ValueError on non-positive quotes or tenors."""
    __tracebackhide__ = True
    valid_spot = 1.10
    valid_forward = 1.09
    valid_tau = 0.25

    # Non-positive spot
    with pytest.raises(ValueError):
        implied_usd_rate(0.0, valid_forward, 0.03, valid_tau, valid_tau)
    with pytest.raises(ValueError):
        implied_usd_rate(-1.10, valid_forward, 0.03, valid_tau, valid_tau)

    # Non-positive forward
    with pytest.raises(ValueError):
        implied_usd_rate(valid_spot, 0.0, 0.03, valid_tau, valid_tau)
    with pytest.raises(ValueError):
        implied_usd_rate(valid_spot, -1.09, 0.03, valid_tau, valid_tau)

    # Non-positive accrual
    with pytest.raises(ValueError):
        implied_usd_rate(valid_spot, valid_forward, 0.03, 0.0, valid_tau)
    with pytest.raises(ValueError):
        implied_usd_rate(valid_spot, valid_forward, 0.03, valid_tau, -0.25)

    # is_quarter_end invalid date
    with pytest.raises(ValueError):
        is_quarter_end("not-a-date")


def test_monitor_table_validation_and_output() -> None:
    """T06: monitor_table validates input rows and produces expected summary dictionaries."""
    __tracebackhide__ = True
    rows: list[dict[str, Any]] = _INST["rows"]
    table = monitor_table(rows)

    assert len(table) == len(rows), "monitor_table must produce one output record per input row"

    for idx, (in_row, out_rec) in enumerate(zip(rows, table, strict=True)):
        assert out_rec["date"] == in_row["date"]
        assert isinstance(out_rec["is_quarter_end"], bool)
        assert math.isfinite(float(out_rec["basis_bp"]))
        assert math.isfinite(float(out_rec["implied_usd_rate"]))

        # Verify exact calculation consistency
        expected_basis = cross_currency_basis_bp(
            float(in_row["spot"]),
            float(in_row["forward"]),
            float(in_row["usd_rate"]),
            float(in_row["foreign_rate"]),
            float(in_row["tau_usd"]),
            float(in_row["tau_foreign"]),
        )
        assert close(float(out_rec["basis_bp"]), expected_basis, tol=1e-8), (
            f"Row {idx} table basis {out_rec['basis_bp']} must match direct call {expected_basis}"
        )

    # Test rejection of missing keys
    bad_row_missing = dict(rows[0])
    del bad_row_missing["spot"]
    with pytest.raises(ValueError):
        monitor_table([bad_row_missing])

    # Test rejection of non-numeric field
    bad_row_str = dict(rows[0])
    bad_row_str["forward"] = "invalid_number"
    with pytest.raises(ValueError):
        monitor_table([bad_row_str])


def test_no_lookahead() -> None:
    """T07: Evaluating row t is completely independent of future rows."""
    __tracebackhide__ = True
    rows = [dict(r) for r in _INST["rows"][:5]]
    out_1 = monitor_table(rows)

    # Mutate row 2 (index 1) and future rows
    rows_mutated = [dict(r) for r in rows]
    rows_mutated[1]["forward"] = float(rows_mutated[1]["forward"]) * 1.05
    rows_mutated[2]["spot"] = float(rows_mutated[2]["spot"]) * 0.95
    out_2 = monitor_table(rows_mutated)

    # Row 0 must be byte-for-byte identical
    assert out_1[0]["basis_bp"] == out_2[0]["basis_bp"], "Row 0 basis must not change when mutating future rows"
    assert out_1[0]["implied_usd_rate"] == out_2[0]["implied_usd_rate"]
