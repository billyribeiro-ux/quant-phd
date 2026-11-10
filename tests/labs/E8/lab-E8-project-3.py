"""Project Lab 3 (Rung 3 check): CIP-Basis Monitor Summary Table.

SIMULATED 60-day panel. Standard library only.
Computes summary statistics of the cross-currency basis comparing quarter-end vs. non-quarter-end dates.
"""

import datetime
import math
import random

SEED = 42


def is_quarter_end(date_iso: str) -> bool:
    """Return True if date_iso is the last weekday of a calendar quarter."""
    dt = datetime.date.fromisoformat(date_iso)
    if dt.month not in (3, 6, 9, 12):
        return False
    max_day = 31 if dt.month in (3, 12) else 30
    last_cal_day = datetime.date(dt.year, dt.month, max_day)
    if last_cal_day.weekday() == 5:
        target_day = max_day - 1
    elif last_cal_day.weekday() == 6:
        target_day = max_day - 2
    else:
        target_day = max_day
    return dt.day == target_day


def generate_panel(seed: int = SEED) -> list[dict[str, object]]:
    """Generate 60 business days of synthetic market quotes."""
    rng = random.Random(seed)
    current_date = datetime.date(2024, 2, 1)
    rows: list[dict[str, object]] = []

    spot = 1.0950
    usd_rate = 0.0525
    foreign_rate = 0.0350
    tau = 90.0 / 360.0

    while len(rows) < 60:
        if current_date.weekday() < 5:
            date_str = current_date.isoformat()
            is_qe = is_quarter_end(date_str)

            # Random drift
            spot *= 1.0 + rng.gauss(0.0, 0.002)
            usd_rate = max(0.01, usd_rate + rng.gauss(0.0, 0.0003))
            foreign_rate = max(0.01, foreign_rate + rng.gauss(0.0, 0.0003))

            # Basis in basis points: -25 bp normal, -65 bp quarter end
            target_basis = (-65.0 + rng.gauss(0.0, 3.0)) if is_qe else (-25.0 + rng.gauss(0.0, 2.5))

            # Forward rate implied by basis
            implied_usd = usd_rate - (target_basis / 10000.0)
            forward = spot * (1.0 + foreign_rate * tau) / (1.0 + implied_usd * tau)

            rows.append(
                {
                    "date": date_str,
                    "spot": spot,
                    "forward": forward,
                    "usd_rate": usd_rate,
                    "foreign_rate": foreign_rate,
                    "tau_usd": tau,
                    "tau_foreign": tau,
                    "basis_bp": target_basis,
                    "is_quarter_end": is_qe,
                }
            )
        current_date += datetime.timedelta(days=1)

    return rows


def main() -> None:
    records = generate_panel(SEED)

    qe_bases: list[float] = [float(str(r["basis_bp"])) for r in records if r["is_quarter_end"]]
    normal_bases: list[float] = [float(str(r["basis_bp"])) for r in records if not r["is_quarter_end"]]

    mean_qe_basis = sum(qe_bases) / len(qe_bases) if qe_bases else 0.0
    mean_normal_basis = sum(normal_bases) / len(normal_bases) if normal_bases else 0.0

    std_qe = (
        math.sqrt(sum((x - mean_qe_basis) ** 2 for x in qe_bases) / (len(qe_bases) - 1)) if len(qe_bases) > 1 else 0.0
    )
    std_normal = (
        math.sqrt(sum((x - mean_normal_basis) ** 2 for x in normal_bases) / (len(normal_bases) - 1))
        if len(normal_bases) > 1
        else 0.0
    )

    print("=== Rung 3 Check: CIP-Basis Monitor Output Summary ===")
    print(f"Total Trading Days Processed: {len(records)}")
    print(f"Normal Trading Days (N={len(normal_bases)}):")
    print(f"  Mean Cross-Currency Basis: {mean_normal_basis:+.1f} bp")
    print(f"  Standard Deviation:        {std_normal:.1f} bp")
    print(f"Quarter-End Days (N={len(qe_bases)}):")
    print(f"  Mean Cross-Currency Basis: {mean_qe_basis:+.1f} bp")
    print(f"  Standard Deviation:        {std_qe:.1f} bp")
    print(f"\nQuarter-End Spread Discrepancy: {mean_qe_basis - mean_normal_basis:+.1f} bp")

    assert len(records) == 60, "Expected 60 records"
    assert len(qe_bases) >= 1, "Must contain at least 1 quarter end"


main()
