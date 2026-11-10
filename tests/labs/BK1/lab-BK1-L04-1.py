"""Lab BK1-L04-1: Repricing gap analysis and time bucket scheduling.

Repricing gap analysis groups rate-sensitive assets (RSA) and rate-sensitive liabilities (RSL)
into maturity/repricing time buckets:
    Bucket 0: 0 < m <= 3 months
    Bucket 1: 3 < m <= 6 months
    Bucket 2: 6 < m <= 12 months
    Bucket 3: 12 < m <= 60 months (1 to 5 years)
    Bucket 4: m > 60 months (> 5 years)

For each bucket b, the periodic repricing gap is G_b = RSA_b - RSL_b.
The cumulative gap through bucket k is CG_k = sum_{b=0}^k G_b.
The 1-year cumulative gap CG_2 is the primary indicator of short-term interest rate risk.

This lab simulates:
1. A multi-asset, multi-liability banking book (SIMULATED, in cents).
2. Calculation of periodic and cumulative gaps.
3. Verification of the gap summation identity and boundary conditions.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    name: str
    cents: int
    months: int | None
    side: str  # "asset" or "liability"


# SIMULATED bank positions in cents
POSITIONS: list[Position] = [
    # Assets
    Position("Cash & Reserves", 15_000_000, None, "asset"),  # Non-rate-sensitive
    Position("Fed Funds Sold", 20_000_000, 1, "asset"),  # Bucket 0
    Position("3-Month T-Bills", 30_000_000, 3, "asset"),  # Bucket 0 (boundary)
    Position("Floating CRE Loans", 40_000_000, 5, "asset"),  # Bucket 1
    Position("1-Year Fixed Auto Loans", 35_000_000, 12, "asset"),  # Bucket 2 (boundary)
    Position("3-Year Fixed Mortgages", 80_000_000, 36, "asset"),  # Bucket 3
    Position("10-Year Fixed Treasury", 50_000_000, 120, "asset"),  # Bucket 4
    # Liabilities
    Position("Non-interest Checking", 25_000_000, None, "liability"),  # Non-rate-sensitive
    Position("Wholesale Repo Funding", 50_000_000, 2, "liability"),  # Bucket 0
    Position("6-Month Term CDs", 45_000_000, 6, "liability"),  # Bucket 1 (boundary)
    Position("9-Month Brokered Deposits", 30_000_000, 9, "liability"),  # Bucket 2
    Position("3-Year Senior Bank Notes", 60_000_000, 36, "liability"),  # Bucket 3
    Position("10-Year Subordinated Debt", 40_000_000, 120, "liability"),  # Bucket 4
]


def bucket_index(months: int) -> int:
    """Map months to bucket index 0..4."""
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


def compute_gap_schedule(positions: list[Position]) -> list[dict[str, int]]:
    """Compute RSA, RSL, and Periodic Gap for each bucket 0..4."""
    rsa = [0] * 5
    rsl = [0] * 5

    for p in positions:
        if p.months is None:
            continue
        b = bucket_index(p.months)
        if p.side == "asset":
            rsa[b] += p.cents
        else:
            rsl[b] += p.cents

    schedule: list[dict[str, int]] = []
    cumulative = 0
    for b in range(5):
        gap = rsa[b] - rsl[b]
        cumulative += gap
        schedule.append(
            {
                "bucket": b,
                "rsa_cents": rsa[b],
                "rsl_cents": rsl[b],
                "gap_cents": gap,
                "cum_gap_cents": cumulative,
            }
        )
    return schedule


def main() -> None:
    print("A. Repricing Gap Schedule by Bucket (SIMULATED, in cents)")
    labels = ["0-3m", "3-6m", "6-12m", "1-5y", ">5y"]
    schedule = compute_gap_schedule(POSITIONS)

    for row in schedule:
        b = row["bucket"]
        print(
            f"Bucket {b} ({labels[b]:5s}) | RSA: {row['rsa_cents']:10d} | "
            f"RSL: {row['rsl_cents']:10d} | Periodic Gap: {row['gap_cents']:+11d} | "
            f"Cumulative Gap: {row['cum_gap_cents']:+11d} cents"
        )

    print()
    print("B. Key Gap Totals and 1-Year Repricing Risk")
    one_year_cum_gap = schedule[2]["cum_gap_cents"]
    print(f"1-Year Cumulative Repricing Gap (CG_2): {one_year_cum_gap:+11d} cents")
    # For a +100 bp rate rise, first-order estimated NII impact: CG_2 * 0.01
    approx_nii_100bp = one_year_cum_gap // 100
    print(f"First-order estimated NII change for +100 bp shock: {approx_nii_100bp:+10d} cents")

    print()
    print("C. Algebraic Invariant Checks")
    total_rsa = sum(p.cents for p in POSITIONS if p.months is not None and p.side == "asset")
    total_rsl = sum(p.cents for p in POSITIONS if p.months is not None and p.side == "liability")
    sum_periodic_gaps = sum(row["gap_cents"] for row in schedule)
    final_cum_gap = schedule[4]["cum_gap_cents"]

    print(f"Sum of periodic gaps equals total RSA minus total RSL: {sum_periodic_gaps == total_rsa - total_rsl}")
    print(f"Final cumulative gap equals sum of periodic gaps: {final_cum_gap == sum_periodic_gaps}")
    # Boundary tests
    print(f"3-month position placed in bucket 0 (0-3m): {bucket_index(3) == 0}")
    print(f"12-month position placed in bucket 2 (6-12m): {bucket_index(12) == 2}")


main()
