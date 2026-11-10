"""Lab BK1-project-3: Rung 3 independent project check — ALM Engine on Seed 0.

Evaluates the deterministic SIMULATED bank balance sheet generated for seed 0:
- Repricing gaps across 5 buckets
- 12-month NII sensitivity under a parallel shock
- Economic Value of Equity (EVE) and Delta EVE under parallel and twist shocks
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
        return Fraction(shift.short_bp, 1) + Fraction(
            (shift.long_bp - shift.short_bp) * (m - 3), 117
        )
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
    # Seed 0 generated instance parameters
    positions = [
        Position(5_685_921, None, "asset"),
        Position(16_390_521, 2, "asset"),
        Position(30_117_888, 8, "asset"),
        Position(75_968_631, 60, "asset"),
        Position(16_326_909, 4, "liability"),
        Position(11_017_530, 18, "liability"),
    ]
    deposits = DepositBook(cents=80_347_599, beta_bp=3500)
    base_rate_bp = 517
    shock_bp = 150
    twist = TwistShift(short_bp=227, long_bp=52)

    print("A. Seed 0 ALM Simulation Outputs (SIMULATED, in cents)")
    gaps = repricing_gap(positions)
    print(f"Bucket Gaps [0..4]: {gaps}")

    nii_delta = nii_change_cents(positions, deposits, shock_bp)
    print(f"12-Month NII Change (+{shock_bp} bp): {nii_delta:+10d} cents")

    eve_base = eve_cents(positions, deposits, base_rate_bp, None)
    par_delta = delta_eve_cents(positions, deposits, base_rate_bp, ParallelShift(shock_bp))
    twist_delta = delta_eve_cents(positions, deposits, base_rate_bp, twist)

    print(f"Base EVE:                          {eve_base:10d} cents")
    print(f"Delta EVE (Parallel +{shock_bp} bp):       {par_delta:+10d} cents")
    print(f"Delta EVE (Twist +227/+52 bp):      {twist_delta:+10d} cents")

    # Invariants
    total_rs = sum(p.cents for p in positions if p.months is not None and p.side == "asset") - sum(
        p.cents for p in positions if p.months is not None and p.side == "liability"
    )
    print(f"Gap identity holds for seed 0: {sum(gaps) == total_rs}")


main()
