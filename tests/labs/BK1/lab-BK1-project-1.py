"""Lab BK1-project-1: Rung 1 worked example — Asset-Liability Management (ALM) Engine.

Demonstrates a fully solved, annotated evaluation of:
1. Repricing gap analysis across 5 time buckets.
2. 12-month Net Interest Income (NII) sensitivity to a +100 bp parallel shock.
3. Economic Value of Equity (EVE) and Delta EVE under parallel (+100 bp) and twist (+150/+50 bp) shocks.

Conventions:
- All money amounts are integer cents.
- Calculations use exact fractions and round half away from zero once at the end.
- Positions with months=None are non-rate-sensitive, omitted from gap analysis and carried at face in EVE.
- Core deposits are carried at face value in EVE and reprice with pass-through beta in NII.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Position:
    cents: int
    months: int | None
    side: str


@dataclass(frozen=True)
class DepositBook:
    cents: int
    beta_bp: int


@dataclass(frozen=True)
class ParallelShift:
    bp: int


@dataclass(frozen=True)
class TwistShift:
    short_bp: int
    long_bp: int


def round_cents(f: Fraction) -> int:
    if f >= 0:
        return (f.numerator * 2 + f.denominator) // (f.denominator * 2)
    else:
        return -((-f.numerator * 2 + f.denominator) // (f.denominator * 2))


def bucket_index(months: int) -> int:
    if months <= 0:
        raise ValueError("months must be positive")
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
    delta_nii_frac = Fraction(0, 1)
    shock_frac = Fraction(shock_bp, 10_000)

    for p in positions:
        if p.months is not None and 1 <= p.months <= 12:
            weight = Fraction(12 - p.months, 12)
            term = Fraction(p.cents, 1) * shock_frac * weight
            if p.side == "asset":
                delta_nii_frac += term
            else:
                delta_nii_frac -= term

    beta_frac = Fraction(deposits.beta_bp, 10_000)
    dep_expense = Fraction(deposits.cents, 1) * beta_frac * shock_frac
    delta_nii_frac -= dep_expense
    return round_cents(delta_nii_frac)


def shift_at_month(m: int, shift: ParallelShift | TwistShift | None) -> Fraction:
    if shift is None:
        return Fraction(0, 1)
    if isinstance(shift, ParallelShift):
        return Fraction(shift.bp, 1)
    if isinstance(shift, TwistShift):
        if m <= 3:
            return Fraction(shift.short_bp, 1)
        if m >= 120:
            return Fraction(shift.long_bp, 1)
        return Fraction(shift.short_bp, 1) + Fraction((shift.long_bp - shift.short_bp) * (m - 3), 117)
    raise TypeError(f"Unknown shift: {shift}")


def eve_cents(
    positions: list[Position],
    deposits: DepositBook,
    base_rate_bp: int,
    shift: ParallelShift | TwistShift | None = None,
) -> int:
    eve_frac = Fraction(0, 1)
    for p in positions:
        if p.months is None:
            pv = Fraction(p.cents, 1)
        else:
            s_bp = shift_at_month(p.months, shift)
            effective_bp = Fraction(base_rate_bp, 1) + s_bp
            denom = Fraction(120_000, 1) + effective_bp
            df = (Fraction(120_000, 1) / denom) ** p.months
            pv = Fraction(p.cents, 1) * df

        if p.side == "asset":
            eve_frac += pv
        else:
            eve_frac -= pv

    eve_frac -= Fraction(deposits.cents, 1)
    return round_cents(eve_frac)


def delta_eve_cents(
    positions: list[Position],
    deposits: DepositBook,
    base_rate_bp: int,
    shift: ParallelShift | TwistShift,
) -> int:
    return eve_cents(positions, deposits, base_rate_bp, shift) - eve_cents(
        positions, deposits, base_rate_bp, ParallelShift(0)
    )


def main() -> None:
    # 5-position SIMULATED banking book (cents)
    positions = [
        Position(2_000_000, None, "asset"),  # $20,000 cash (face)
        Position(5_000_000, 2, "asset"),  # $50,000 loan (2m, bucket 0)
        Position(15_000_000, 60, "asset"),  # $150,000 loan (60m, bucket 3)
        Position(4_000_000, 6, "liability"),  # $40,000 CD (6m, bucket 1)
        Position(6_000_000, 36, "liability"),  # $60,000 note (36m, bucket 3)
    ]
    deposits = DepositBook(cents=10_000_000, beta_bp=4000)  # $100,000 deposits, beta=0.40
    base_rate_bp = 300  # 3.00%
    shock_bp = 100  # +100 bp parallel shock
    twist = TwistShift(short_bp=150, long_bp=50)

    print("A. Repricing Gap by Bucket (SIMULATED, in cents)")
    gaps = repricing_gap(positions)
    labels = ["0-3m", "3-6m", "6-12m", "1-5y", ">5y"]
    for idx, (label, g) in enumerate(zip(labels, gaps, strict=False)):
        print(f"Bucket {idx} ({label:5s}): {g:+10d} cents")

    print()
    print("B. 12-Month Net Interest Income Sensitivity")
    nii_delta = nii_change_cents(positions, deposits, shock_bp)
    print(f"12-Month NII Change for +{shock_bp} bp shock: {nii_delta:+8d} cents")

    print()
    print("C. Economic Value of Equity (EVE)")
    base_eve = eve_cents(positions, deposits, base_rate_bp, None)
    par_delta = delta_eve_cents(positions, deposits, base_rate_bp, ParallelShift(shock_bp))
    twist_delta = delta_eve_cents(positions, deposits, base_rate_bp, twist)

    print(f"Base EVE (300 bp rate):             {base_eve:10d} cents")
    print(f"Delta EVE Parallel (+100 bp):       {par_delta:+10d} cents")
    print(f"Delta EVE Twist (+150/+50 bp):      {twist_delta:+10d} cents")


main()
