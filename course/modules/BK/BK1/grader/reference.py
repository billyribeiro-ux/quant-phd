"""Reference solution for the BK1 ALM engine (alm.py).

The grader copies this file to alm.py in a temporary directory and runs the test suite.
Conventions, as stated on the project page:
* Every money amount is an int number of cents.
* Every calculation is evaluated exactly using fractions.Fraction.
* Rounding to integer cents is performed once at the end, half away from zero.
* Positions with months is None represent non-rate-sensitive assets or liabilities (carried at face value).
* Deposits are non-maturity core deposits, carried at face value in EVE and repricing immediately
  with pass-through beta_bp / 10000 in NII.
* Discount convention: monthly compounding of nominal annual rate (base_rate_bp + shift_bp) / 10000.
* Twist shift: short_bp for m <= 3, long_bp for m >= 120, linear interpolation in m between them.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


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


def round_cents(f: Fraction) -> int:
    """Round Fraction to nearest integer cent, half away from zero."""
    if f >= 0:
        return (f.numerator * 2 + f.denominator) // (f.denominator * 2)
    else:
        return -((-f.numerator * 2 + f.denominator) // (f.denominator * 2))


def bucket_index(months: int) -> int:
    """Map repricing/maturity months to one of 5 time buckets:

    0: 0 < m <= 3
    1: 3 < m <= 6
    2: 6 < m <= 12
    3: 12 < m <= 60
    4: m > 60
    """
    if months <= 0:
        raise ValueError(f"months must be positive: {months}")
    if months <= 3:
        return 0
    elif months <= 6:
        return 1
    elif months <= 12:
        return 2
    elif months <= 60:
        return 3
    else:
        return 4


def repricing_gap(positions: list[Position]) -> list[int]:
    """Compute the repricing gap in cents (Rate-Sensitive Assets minus Rate-Sensitive Liabilities)

    for each of the 5 time buckets [0..4]. Positions with months=None are excluded.
    """
    gaps_frac = [Fraction(0, 1) for _ in range(5)]
    for p in positions:
        if p.months is None:
            continue
        b = bucket_index(p.months)
        if p.side == "asset":
            gaps_frac[b] += Fraction(p.cents, 1)
        else:
            gaps_frac[b] -= Fraction(p.cents, 1)

    return [round_cents(g) for g in gaps_frac]


def nii_change_cents(positions: list[Position], deposits: DepositBook, shock_bp: int) -> int:
    """Calculate the 12-month Net Interest Income change in cents for a parallel rate shock of shock_bp.

    Over horizon h = 12 months:
    Rate-sensitive positions with 1 <= m <= 12 reprice at month m, earning/paying the new rate
    for the remaining (12 - m) / 12 of the annual horizon.
    Deposits reprice immediately at pass-through beta = beta_bp / 10000 for the full 12 months.
    """
    delta_nii_frac = Fraction(0, 1)
    shock_frac = Fraction(shock_bp, 10_000)

    for p in positions:
        if p.months is not None and 1 <= p.months <= 12:
            weight = Fraction(12 - p.months, 12)
            nii_term = Fraction(p.cents, 1) * shock_frac * weight
            if p.side == "asset":
                delta_nii_frac += nii_term
            else:
                delta_nii_frac -= nii_term

    # Deposit interest expense change
    beta_frac = Fraction(deposits.beta_bp, 10_000)
    dep_expense_change = Fraction(deposits.cents, 1) * beta_frac * shock_frac
    delta_nii_frac -= dep_expense_change

    return round_cents(delta_nii_frac)


def delta_nii_cents(positions: list[Position], deposits: DepositBook, shock_bp: int) -> int:
    """Alias for nii_change_cents."""
    return nii_change_cents(positions, deposits, shock_bp)


def _shift_at_month(m: int, shift: ParallelShift | TwistShift | None) -> Fraction:
    """Return the rate shift in basis points at tenor m months as a Fraction."""
    if shift is None:
        return Fraction(0, 1)
    if isinstance(shift, ParallelShift):
        return Fraction(shift.bp, 1)
    if isinstance(shift, TwistShift):
        if m <= 3:
            return Fraction(shift.short_bp, 1)
        if m >= 120:
            return Fraction(shift.long_bp, 1)
        # Linear interpolation between 3 and 120 months (117 months span)
        return Fraction(shift.short_bp, 1) + Fraction((shift.long_bp - shift.short_bp) * (m - 3), 117)
    raise TypeError(f"Unknown shift type: {type(shift)}")


def eve_cents(
    positions: list[Position],
    deposits: DepositBook,
    base_rate_bp: int,
    shift: ParallelShift | TwistShift | None = None,
) -> int:
    """Compute Economic Value of Equity (EVE) in integer cents.

    PV of assets minus PV of liabilities minus deposits (carried at face).
    Discount factor for m months: DF(m) = (1 + r(m)/12)^(-m) where r(m) = (base_rate_bp + shift_bp) / 10000.
    Positions with months=None are carried at face value.
    """
    if base_rate_bp < 0:
        raise ValueError(f"base_rate_bp cannot be negative: {base_rate_bp}")

    eve_frac = Fraction(0, 1)

    for p in positions:
        if p.months is None:
            pv = Fraction(p.cents, 1)
        else:
            s_bp = _shift_at_month(p.months, shift)
            effective_bp = Fraction(base_rate_bp, 1) + s_bp
            # 1 + r/12 = 1 + effective_bp / 120000 = (120000 + effective_bp) / 120000
            denom = Fraction(120_000, 1) + effective_bp
            if denom <= 0:
                raise ValueError("effective rate yields non-positive discount factor base")
            df = (Fraction(120_000, 1) / denom) ** p.months
            pv = Fraction(p.cents, 1) * df

        if p.side == "asset":
            eve_frac += pv
        else:
            eve_frac -= pv

    # Subtract non-maturity deposits (carried at face value)
    eve_frac -= Fraction(deposits.cents, 1)

    return round_cents(eve_frac)


def delta_eve_cents(
    positions: list[Position],
    deposits: DepositBook,
    base_rate_bp: int,
    shift: ParallelShift | TwistShift,
) -> int:
    """Compute change in Economic Value of Equity (shifted EVE minus base EVE) in cents."""
    eve_shifted = eve_cents(positions, deposits, base_rate_bp, shift)
    eve_base = eve_cents(positions, deposits, base_rate_bp, ParallelShift(0))
    return eve_shifted - eve_base
