"""Autograder test suite for BK1 ALM engine (alm.py).

Verifies:
* Repricing gap bucket boundary rules and algebraic summation invariant.
* Zero-shock invariants for EVE and NII sensitivity.
* Twist shock with equal short and long shifts equals parallel shock.
* Monotonicity of EVE losses under duration mismatch (maturity transformation).
* Monotonicity of NII sensitivity with respect to deposit beta.
* All money values are integer cents.
* Robustness, determinism, and mathematical consistency across seeds.
"""

from __future__ import annotations

import os

import pytest
from alm import (
    DepositBook,
    ParallelShift,
    Position,
    TwistShift,
    bucket_index,
    delta_eve_cents,
    delta_nii_cents,
    eve_cents,
    nii_change_cents,
    repricing_gap,
)
from instance import make_instance


def get_seed() -> int:
    return int(os.environ.get("QF_SEED", "0"))


def positions_from_instance(inst: dict[str, object]) -> list[Position]:
    cents_list = inst["position_cents"]
    months_list = inst["position_months"]
    sides_list = inst["position_sides"]
    assert isinstance(cents_list, list)
    assert isinstance(months_list, list)
    assert isinstance(sides_list, list)
    return [
        Position(
            cents=c,
            months=m if m > 0 else None,
            side=s,
        )
        for c, m, s in zip(cents_list, months_list, sides_list, strict=True)
    ]


def test_instance_valid() -> None:
    seed = get_seed()
    inst = make_instance(seed)
    assert isinstance(inst["position_cents"], list)
    assert isinstance(inst["position_months"], list)
    assert isinstance(inst["position_sides"], list)
    assert isinstance(inst["deposits_cents"], int)
    assert isinstance(inst["beta_bp"], int)
    assert 0 <= inst["beta_bp"] <= 10_000
    assert isinstance(inst["base_rate_bp"], int)
    assert inst["base_rate_bp"] >= 0
    assert isinstance(inst["shock_bp"], int)
    assert inst["shock_bp"] > 0


def test_bucket_boundaries() -> None:
    # Bucket 0: 0 < m <= 3
    assert bucket_index(1) == 0
    assert bucket_index(2) == 0
    assert bucket_index(3) == 0

    # Bucket 1: 3 < m <= 6
    assert bucket_index(4) == 1
    assert bucket_index(5) == 1
    assert bucket_index(6) == 1

    # Bucket 2: 6 < m <= 12
    assert bucket_index(7) == 2
    assert bucket_index(11) == 2
    assert bucket_index(12) == 2

    # Bucket 3: 12 < m <= 60
    assert bucket_index(13) == 3
    assert bucket_index(36) == 3
    assert bucket_index(60) == 3

    # Bucket 4: m > 60
    assert bucket_index(61) == 4
    assert bucket_index(120) == 4

    # Invalid
    with pytest.raises(ValueError):
        bucket_index(0)
    with pytest.raises(ValueError):
        bucket_index(-5)


def test_repricing_gap_identity() -> None:
    seed = get_seed()
    inst = make_instance(seed)
    positions = positions_from_instance(inst)

    gaps = repricing_gap(positions)
    assert len(gaps) == 5
    assert all(isinstance(g, int) for g in gaps)

    # Invariant: sum of bucket gaps must equal total RSA minus total RSL
    expected_rsa_minus_rsl = 0
    for p in positions:
        if p.months is not None:
            if p.side == "asset":
                expected_rsa_minus_rsl += p.cents
            else:
                expected_rsa_minus_rsl -= p.cents

    assert sum(gaps) == expected_rsa_minus_rsl, (
        f"Gap identity violated: sum of gaps {sum(gaps)} != RSA - RSL {expected_rsa_minus_rsl}"
    )


def test_non_rate_sensitive_omission() -> None:
    # Positions with months=None must not alter repricing gap
    p_core = [
        Position(cents=100_000, months=2, side="asset"),
        Position(cents=60_000, months=5, side="liability"),
    ]
    p_with_cash = [
        *p_core,
        Position(cents=500_000, months=None, side="asset"),
        Position(cents=200_000, months=None, side="liability"),
    ]

    gap_core = repricing_gap(p_core)
    gap_with_cash = repricing_gap(p_with_cash)
    assert gap_core == gap_with_cash


def test_nii_zero_shock_and_hand_fixture() -> None:
    seed = get_seed()
    inst = make_instance(seed)
    positions = positions_from_instance(inst)
    assert isinstance(inst["deposits_cents"], int)
    assert isinstance(inst["beta_bp"], int)
    deposits = DepositBook(cents=inst["deposits_cents"], beta_bp=inst["beta_bp"])

    # Zero shock yields 0 NII change
    assert nii_change_cents(positions, deposits, 0) == 0
    assert delta_nii_cents(positions, deposits, 0) == 0

    # Hand fixture from lesson:
    # 1 asset of 1,000,000 cents resetting at month 6 (12 - 6)/12 = 1/2 weight
    # deposits of 500,000 cents at beta 5000 bp (0.50), shock +100 bp (0.01)
    # Asset interest income gain: 1,000,000 * 0.01 * (6/12) = +5,000 cents
    # Deposit interest expense increase: 500,000 * 0.5 * 0.01 = +2,500 cents
    # Net NII change = +5,000 - 2,500 = +2,500 cents
    fixture_pos = [Position(cents=1_000_000, months=6, side="asset")]
    fixture_dep = DepositBook(cents=500_000, beta_bp=5000)
    assert nii_change_cents(fixture_pos, fixture_dep, 100) == 2500


def test_nii_beta_monotonicity() -> None:
    # For a positive rate shock, higher deposit beta must increase interest expense,
    # lowering NII change
    pos = [
        Position(cents=1_000_000, months=3, side="asset"),
        Position(cents=400_000, months=6, side="liability"),
    ]
    shock = 100
    dep_low_beta = DepositBook(cents=1_000_000, beta_bp=2000)  # beta = 0.20
    dep_high_beta = DepositBook(cents=1_000_000, beta_bp=8000)  # beta = 0.80

    nii_low = nii_change_cents(pos, dep_low_beta, shock)
    nii_high = nii_change_cents(pos, dep_high_beta, shock)
    assert nii_low > nii_high, f"Monotonicity failed: {nii_low} not > {nii_high}"


def test_eve_zero_shock_and_twist_equivalence() -> None:
    seed = get_seed()
    inst = make_instance(seed)
    positions = positions_from_instance(inst)
    assert isinstance(inst["deposits_cents"], int)
    assert isinstance(inst["beta_bp"], int)
    assert isinstance(inst["base_rate_bp"], int)
    assert isinstance(inst["shock_bp"], int)
    deposits = DepositBook(cents=inst["deposits_cents"], beta_bp=inst["beta_bp"])
    base_rate = inst["base_rate_bp"]

    # Zero shock gives delta EVE = 0
    delta_zero = delta_eve_cents(positions, deposits, base_rate, ParallelShift(0))
    assert delta_zero == 0

    base_eve = eve_cents(positions, deposits, base_rate, None)
    base_eve_par0 = eve_cents(positions, deposits, base_rate, ParallelShift(0))
    assert base_eve == base_eve_par0

    # Invariant: TwistShift(s, s) must produce exact same result as ParallelShift(s)
    shift_val = inst["shock_bp"]
    eve_parallel = eve_cents(positions, deposits, base_rate, ParallelShift(shift_val))
    eve_twist_equal = eve_cents(positions, deposits, base_rate, TwistShift(shift_val, shift_val))
    assert eve_parallel == eve_twist_equal, (
        f"Twist with short==long failed to equal parallel: {eve_twist_equal} != {eve_parallel}"
    )


def test_duration_mismatch_loss_monotonicity() -> None:
    # A classic bank: Long assets (e.g. 60 months), funded by short liabilities (6 months) & deposits.
    # Positive rate shocks must reduce EVE, and larger shocks must induce larger losses.
    pos = [
        Position(cents=10_000_000, months=60, side="asset"),
        Position(cents=2_000_000, months=6, side="liability"),
    ]
    dep = DepositBook(cents=7_000_000, beta_bp=4000)
    base_rate = 300

    delta_100 = delta_eve_cents(pos, dep, base_rate, ParallelShift(100))
    delta_200 = delta_eve_cents(pos, dep, base_rate, ParallelShift(200))
    delta_300 = delta_eve_cents(pos, dep, base_rate, ParallelShift(300))

    assert delta_100 < 0, f"Expected loss for +100bp shock under asset duration mismatch, got {delta_100}"
    assert delta_200 < delta_100, f"Loss monotonicity failed: {delta_200} not < {delta_100}"
    assert delta_300 < delta_200, f"Loss monotonicity failed: {delta_300} not < {delta_200}"


def test_instance_full_run() -> None:
    seed = get_seed()
    inst = make_instance(seed)
    positions = positions_from_instance(inst)
    assert isinstance(inst["deposits_cents"], int)
    assert isinstance(inst["beta_bp"], int)
    assert isinstance(inst["base_rate_bp"], int)
    assert isinstance(inst["shock_bp"], int)
    assert isinstance(inst["twist_short_bp"], int)
    assert isinstance(inst["twist_long_bp"], int)
    deposits = DepositBook(cents=inst["deposits_cents"], beta_bp=inst["beta_bp"])

    gaps = repricing_gap(positions)
    assert len(gaps) == 5

    nii_delta = nii_change_cents(positions, deposits, inst["shock_bp"])
    assert isinstance(nii_delta, int)

    eve_base = eve_cents(positions, deposits, inst["base_rate_bp"])
    assert isinstance(eve_base, int)

    eve_par_delta = delta_eve_cents(positions, deposits, inst["base_rate_bp"], ParallelShift(inst["shock_bp"]))
    assert isinstance(eve_par_delta, int)

    twist = TwistShift(short_bp=inst["twist_short_bp"], long_bp=inst["twist_long_bp"])
    eve_twist_delta = delta_eve_cents(positions, deposits, inst["base_rate_bp"], twist)
    assert isinstance(eve_twist_delta, int)


def test_invalid_input_exceptions() -> None:
    with pytest.raises(ValueError):
        Position(cents=-100, months=6, side="asset")
    with pytest.raises(ValueError):
        Position(cents=100, months=0, side="asset")
    with pytest.raises(ValueError):
        Position(cents=100, months=6, side="other")

    with pytest.raises(ValueError):
        DepositBook(cents=-10, beta_bp=5000)
    with pytest.raises(ValueError):
        DepositBook(cents=1000, beta_bp=-1)
    with pytest.raises(ValueError):
        DepositBook(cents=1000, beta_bp=10001)

    valid_pos = [Position(cents=1000, months=6, side="asset")]
    valid_dep = DepositBook(cents=500, beta_bp=5000)
    with pytest.raises(ValueError):
        eve_cents(valid_pos, valid_dep, -100)
