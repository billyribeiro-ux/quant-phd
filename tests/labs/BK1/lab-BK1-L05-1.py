"""Lab BK1-L05-1: Economic value of equity under parallel and twist shocks.

Economic Value of Equity (EVE) measures the long-term, economic solvency of a bank:
    EVE = PV(Assets) - PV(Liabilities) - Deposits(face value)

Under interest rate shocks, duration mismatch between long-term assets and short-term
funding causes EVE to fluctuate:
    Delta EVE ≈ - (D_assets * PV(Assets) - D_liab * PV(Liabilities)) * Delta r

This lab evaluates:
1. SIMULATED bank balance sheet with long-term assets (duration ~6 years) funded
   by short liabilities & core deposits (duration ~1 year).
2. Base EVE under monthly compounding at base rate r_0 = 200 bp.
3. EVE change under parallel rate shock (+100 bp).
4. EVE change under twist rate shock using observed 2022 US Treasury tightening
   from data/ust_daily.csv (3m T-bill +421 bp, 10y Treasury +225 bp).
5. Identity check: TwistShift(s, s) == ParallelShift(s).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


@dataclass(frozen=True)
class Position:
    cents: int
    months: int | None
    side: str


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
    raise TypeError(f"Unknown shift type: {type(shift)}")


def compute_eve(
    positions: list[Position],
    deposits_cents: int,
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

    eve_frac -= Fraction(deposits_cents, 1)
    return round_cents(eve_frac)


def load_observed_2022_twist(csv_path: Path) -> tuple[int, int]:
    """Read 3m T-bill and 10y Treasury yield change in 2022 from ust_daily.csv."""
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = {r["date"]: r for r in reader if r["date"] in ("2022-01-03", "2022-12-30")}

    r_start = records["2022-01-03"]
    r_end = records["2022-12-30"]

    # Multiply percent by 100 to get basis points
    # Round half-away-from-zero on float readings
    t3m_start = round(float(r_start["tbill_3m"]) * 100)
    t3m_end = round(float(r_end["tbill_3m"]) * 100)
    c10y_start = round(float(r_start["cmt_10y"]) * 100)
    c10y_end = round(float(r_end["cmt_10y"]) * 100)

    short_shift_bp = t3m_end - t3m_start
    long_shift_bp = c10y_end - c10y_start
    return short_shift_bp, long_shift_bp


def main() -> None:
    # 1. Load real rate twist from ust_daily.csv
    csv_file = Path("data") / "ust_daily.csv"
    short_bp, long_bp = load_observed_2022_twist(csv_file)

    print("A. Historical 2022 Yield Curve Move (ust_daily.csv, H.15 Fed Release)")
    print(f"Observed 3-Month T-Bill yield change:  {short_bp:+4d} bp")
    print(f"Observed 10-Year Treasury yield change: {long_bp:+4d} bp")
    print("Yield curve underwent severe bear flattening / inversion (short rate rose faster).")

    # 2. SIMULATED Bank Book
    # Assets: $100M total ($10M cash, $20M 1y loans, $70M 10y mortgages)
    # Liabilities: $85M ($60M core deposits at face, $25M 2y term notes)
    # Equity: $15M ($15,000,000 cents face net worth)
    positions: list[Position] = [
        Position(10_000_000, None, "asset"),  # Cash & reserves (face)
        Position(20_000_000, 12, "asset"),  # 1-year loan
        Position(70_000_000, 120, "asset"),  # 10-year mortgage
        Position(25_000_000, 24, "liability"),  # 2-year term funding
    ]
    deposits_cents = 60_000_000  # $600,000 core deposits
    base_rate_bp = 200  # 2.00% base rate

    print()
    print("B. Economic Value of Equity under Rate Shocks (SIMULATED Book, in cents)")
    base_eve = compute_eve(positions, deposits_cents, base_rate_bp, None)
    print(f"Base EVE (0 bp shift):            {base_eve:10d} cents")

    # Parallel shock +100 bp
    eve_par100 = compute_eve(positions, deposits_cents, base_rate_bp, ParallelShift(100))
    delta_par100 = eve_par100 - base_eve
    print(f"Parallel +100 bp EVE:             {eve_par100:10d} cents (Delta: {delta_par100:+10d} cents)")

    # Parallel shock +200 bp
    eve_par200 = compute_eve(positions, deposits_cents, base_rate_bp, ParallelShift(200))
    delta_par200 = eve_par200 - base_eve
    print(f"Parallel +200 bp EVE:             {eve_par200:10d} cents (Delta: {delta_par200:+10d} cents)")

    # Observed 2022 historical twist shock
    hist_twist = TwistShift(short_bp=short_bp, long_bp=long_bp)
    eve_hist = compute_eve(positions, deposits_cents, base_rate_bp, hist_twist)
    delta_hist = eve_hist - base_eve
    print(f"Observed 2022 Twist EVE:          {eve_hist:10d} cents (Delta: {delta_hist:+10d} cents)")

    print()
    print("C. Mathematical Invariants and Properties")
    # Identity: TwistShift(s, s) must equal ParallelShift(s)
    twist_equal = compute_eve(positions, deposits_cents, base_rate_bp, TwistShift(100, 100))
    print(f"TwistShift(100, 100) equals ParallelShift(100): {twist_equal == eve_par100}")

    # Monotonicity: Asset duration exceeds liability duration -> loss under rate rise
    print(f"EVE loss under +100 bp parallel shock: {delta_par100 < 0}")
    print(f"EVE loss increases monotonically with shock size: {delta_par200 < delta_par100}")


main()
