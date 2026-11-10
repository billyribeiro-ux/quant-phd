"""Lab 10: Cross-Currency Basis Quarter-End Spikes and Dealer Leverage Constraints.

SIMULATED panel. Standard library only.
Tests the Du, Tepper & Verdelhan (2018) regulatory window-dressing hypothesis:
Dealer balance-sheet constraints under Basel III SLR cause cross-currency bases
to widen (become significantly more negative) at regulatory quarter-ends.
"""

import math
import random
from typing import cast

SEED = 888


def is_quarter_end(date_str: str) -> bool:
    """Check if date (YYYY-MM-DD) is the last weekday of a calendar quarter (Q1, Q2, Q3, Q4)."""
    # Quarter ends: March (03), June (06), September (09), December (12)
    # Days in month: March 31, June 30, September 30, December 31
    year, month, day = (int(x) for x in date_str.split("-"))
    if month not in (3, 6, 9, 12):
        return False

    max_day = 31 if month in (3, 12) else 30
    # Day of week: 0=Mon, 1=Tue, ..., 4=Fri, 5=Sat, 6=Sun
    # Sakamoto's algorithm or Zeller
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    y = year if month >= 3 else year - 1
    weekday = (y + y // 4 - y // 100 + y // 400 + t[month - 1] + max_day) % 7
    # Adjust python weekday (where 0=Sunday in some, but let's standardise: 0=Sun, 1=Mon... 6=Sat)
    # Let's verify standard weekday formula:
    # 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday
    # If last day is Saturday (6), last weekday is max_day - 1 (Friday)
    # If last day is Sunday (0), last weekday is max_day - 2 (Friday)
    # Else last weekday is max_day
    if weekday == 6:  # Saturday
        last_weekday = max_day - 1
    elif weekday == 0:  # Sunday
        last_weekday = max_day - 2
    else:
        last_weekday = max_day

    return day == last_weekday


def simulate_basis_panel(seed: int = SEED) -> list[dict[str, object]]:
    """Simulate 252 business days of EUR/USD cross-currency basis (in bp).

    Baseline normal trading days: mean basis around -25 bp with noise.
    Quarter-end dates: regulatory window-dressing causes spike widening by -40 to -70 bp.
    """
    rng = random.Random(seed)

    # 252 business days across 2024 (approx 21 days per month)
    days_per_month = [21, 20, 21, 22, 21, 20, 22, 22, 20, 22, 21, 20]
    records: list[dict[str, object]] = []

    for month_idx in range(1, 13):
        m_days = days_per_month[month_idx - 1]
        for d in range(1, m_days + 1):
            date_str = f"2024-{month_idx:02d}-{d:02d}"
            # For the last trading day of the quarter, mark as quarter end
            is_qe = (month_idx in (3, 6, 9, 12)) and (d == m_days)

            baseline_basis = -24.5 + rng.gauss(0.0, 4.0)
            if is_qe:
                # Regulatory balance sheet squeeze
                spike = rng.uniform(-65.0, -45.0)
                basis = baseline_basis + spike
            else:
                basis = baseline_basis

            records.append(
                {
                    "date": date_str,
                    "is_quarter_end": is_qe,
                    "basis_bp": basis,
                }
            )

    return records


def analyze_quarter_end_effect(records: list[dict[str, object]]) -> dict[str, float]:
    """Compare cross-currency basis between quarter-end and non-quarter-end dates."""
    qe_bases = [float(cast(float, r["basis_bp"])) for r in records if r["is_quarter_end"]]
    normal_bases = [float(cast(float, r["basis_bp"])) for r in records if not r["is_quarter_end"]]

    mean_qe = sum(qe_bases) / len(qe_bases)
    mean_normal = sum(normal_bases) / len(normal_bases)

    var_qe = sum((x - mean_qe) ** 2 for x in qe_bases) / (len(qe_bases) - 1)
    var_normal = sum((x - mean_normal) ** 2 for x in normal_bases) / (len(normal_bases) - 1)

    spread_widening = mean_qe - mean_normal  # Negative value = wider basis

    # Welch's t-statistic
    se_diff = math.sqrt(var_qe / len(qe_bases) + var_normal / len(normal_bases))
    t_stat = (mean_qe - mean_normal) / se_diff

    return {
        "count_normal": len(normal_bases),
        "mean_normal": mean_normal,
        "std_normal": math.sqrt(var_normal),
        "count_qe": len(qe_bases),
        "mean_qe": mean_qe,
        "std_qe": math.sqrt(var_qe),
        "widening_bp": spread_widening,
        "t_stat": t_stat,
    }


def main() -> None:
    records = simulate_basis_panel(SEED)
    stats = analyze_quarter_end_effect(records)

    print("=== CIP Basis Quarter-End Window-Dressing Analysis ===")
    print(f"Total Trading Days: {len(records)}")
    n_cnt = int(stats["count_normal"])
    n_mean = stats["mean_normal"]
    n_std = stats["std_normal"]
    print(f"Normal Trading Days (N={n_cnt}): Mean = {n_mean:+.1f} bp (std = {n_std:.1f} bp)")
    qe_cnt = int(stats["count_qe"])
    qe_mean = stats["mean_qe"]
    qe_std = stats["std_qe"]
    print(f"Quarter-End Days    (N={qe_cnt}):   Mean = {qe_mean:+.1f} bp (std = {qe_std:.1f} bp)")
    print(f"\nQuarter-End Basis Widening: {stats['widening_bp']:+.1f} bp")
    print(f"Welch t-statistic:          {stats['t_stat']:+.2f}")

    print("\nInterpretation (Du, Tepper & Verdelhan 2018):")
    print(f"The cross-currency basis widens by {abs(stats['widening_bp']):.1f} bp at quarter ends.")
    print("Under Basel III SLR, global banks contract FX swap provision to shrink leverage,")
    print("forcing dollar borrowers to pay an extreme premium at regulatory reporting dates.")

    assert stats["count_qe"] == 4, "Must have exactly 4 quarter ends in a 1-year sample"
    assert stats["widening_bp"] < -30.0, f"Expected widening > 30 bp, got {stats['widening_bp']}"
    assert stats["t_stat"] < -10.0, f"Expected highly significant t-stat, got {stats['t_stat']}"


main()
