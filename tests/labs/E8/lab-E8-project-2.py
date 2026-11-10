"""Project Lab 2 (Rung 2): Completion problem twin for basis calculation and quarter-end check.

Completed reference twin. Standard library only.
Computes the implied dollar borrowing rate, cross-currency basis, and tests quarter-end detection.
"""

import datetime


def compute_basis_and_flag(
    date_iso: str,
    spot: float,
    forward: float,
    usd_rate: float,
    foreign_rate: float,
    tau_usd: float,
    tau_foreign: float,
) -> tuple[float, float, bool]:
    """Compute implied dollar rate, basis in bp, and check if date is quarter end."""
    # 1. Foreign accrual
    foreign_accrual = 1.0 + foreign_rate * tau_foreign

    # 2. Implied dollar borrowing rate
    implied_usd = (1.0 / tau_usd) * ((spot / forward) * foreign_accrual - 1.0)

    # 3. Cross-currency basis in basis points
    basis_bp = (usd_rate - implied_usd) * 10000.0

    # 4. Quarter-end identification
    dt = datetime.date.fromisoformat(date_iso)
    if dt.month not in (3, 6, 9, 12):
        is_qe = False
    else:
        max_day = 31 if dt.month in (3, 12) else 30
        last_cal_day = datetime.date(dt.year, dt.month, max_day)
        # Saturday -> Friday (max_day - 1), Sunday -> Friday (max_day - 2)
        if last_cal_day.weekday() == 5:
            last_weekday_day = max_day - 1
        elif last_cal_day.weekday() == 6:
            last_weekday_day = max_day - 2
        else:
            last_weekday_day = max_day
        is_qe = dt.day == last_weekday_day

    return implied_usd, basis_bp, is_qe


def main() -> None:
    # Test on EUR/USD 3-month quote
    date_str = "2024-06-28"  # Friday before June 30 Sunday -> Quarter End
    s = 1.0710
    f = 1.0745
    r_usd = 0.0530
    r_eur = 0.0360
    tau = 90.0 / 360.0

    implied, basis, qe = compute_basis_and_flag(date_str, s, f, r_usd, r_eur, tau, tau)

    print("=== Rung 2: Completion Solution Verification ===")
    print(f"Date:               {date_str}")
    print(f"Implied USD Rate:   {implied * 100:.3f}%")
    print(f"Basis:              {basis:+.1f} bp")
    print(f"Is Quarter-End:     {qe}")

    assert qe is True, "2024-06-28 must be True for quarter end"
    assert basis > 0, "Forward higher than spot with this rate spread should yield positive basis"


main()
