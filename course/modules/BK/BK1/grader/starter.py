"""Starter implementation for the BK1 ALM engine project (alm.py).

Implement each class and function according to the project specification, then run the
autograder in the browser or locally:

    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    """A bank balance sheet position in cents, repricing/maturity tenor, and side."""

    cents: int
    months: int | None
    side: str  # "asset" or "liability"

    def __post_init__(self) -> None:
        if self.cents < 0:
            raise ValueError(f"cents cannot be negative: {self.cents}")
        if self.months is not None and self.months <= 0:
            raise ValueError(f"months must be positive if specified: {self.months}")
        if self.side not in ("asset", "liability"):
            raise ValueError(f"side must be 'asset' or 'liability', not {self.side!r}")


@dataclass(frozen=True)
class DepositBook:
    """Non-maturity core deposits: volume in cents and pass-through beta in basis points."""

    cents: int
    beta_bp: int

    def __post_init__(self) -> None:
        if self.cents < 0:
            raise ValueError(f"deposit cents cannot be negative: {self.cents}")
        if not (0 <= self.beta_bp <= 10_000):
            raise ValueError(f"beta_bp must be in [0, 10000], not {self.beta_bp}")


@dataclass(frozen=True)
class ParallelShift:
    """A parallel yield curve shock across all tenors, in basis points."""

    bp: int


@dataclass(frozen=True)
class TwistShift:
    """A yield curve twist: short rate shift (m <= 3) and long rate shift (m >= 120) in basis points."""

    short_bp: int
    long_bp: int


def bucket_index(months: int) -> int:
    """Map repricing/maturity months to one of 5 time buckets."""
    raise NotImplementedError("bucket_index")


def repricing_gap(positions: list[Position]) -> list[int]:
    """Compute the repricing gap in cents (RSA minus RSL) for each of 5 time buckets."""
    raise NotImplementedError("repricing_gap")


def nii_change_cents(positions: list[Position], deposits: DepositBook, shock_bp: int) -> int:
    """Calculate the 12-month Net Interest Income change in cents for a parallel shock."""
    raise NotImplementedError("nii_change_cents")


def delta_nii_cents(positions: list[Position], deposits: DepositBook, shock_bp: int) -> int:
    """Alias for nii_change_cents."""
    raise NotImplementedError("delta_nii_cents")


def eve_cents(
    positions: list[Position],
    deposits: DepositBook,
    base_rate_bp: int,
    shift: ParallelShift | TwistShift | None = None,
) -> int:
    """Compute Economic Value of Equity (EVE) in integer cents."""
    raise NotImplementedError("eve_cents")


def delta_eve_cents(
    positions: list[Position],
    deposits: DepositBook,
    base_rate_bp: int,
    shift: ParallelShift | TwistShift,
) -> int:
    """Compute change in Economic Value of Equity in cents."""
    raise NotImplementedError("delta_eve_cents")
