"""Reference solution for E8 CIP-basis monitor project.

Implements cross-currency basis calculation, quarter-end identification, and table monitoring.
Standard library only. Fully typed.
"""

from __future__ import annotations

import datetime


def implied_usd_rate(
    spot: float,
    forward: float,
    foreign_rate: float,
    tau_usd: float,
    tau_foreign: float,
) -> float:
    """Compute the annual dollar rate implied by the spot, forward, and foreign interest rate.

    Convention:
    implied_usd = (1 / tau_usd) * [ (forward / spot) * (1 + foreign_rate * tau_foreign) - 1 ]
    Raises ValueError for non-positive spot, forward, or accrual fractions.
    """
    if spot <= 0.0 or forward <= 0.0:
        msg = f"Exchange rates must be strictly positive: spot={spot}, forward={forward}"
        raise ValueError(msg)
    if tau_usd <= 0.0 or tau_foreign <= 0.0:
        msg = f"Accrual fractions must be strictly positive: tau_usd={tau_usd}, tau_foreign={tau_foreign}"
        raise ValueError(msg)

    foreign_accrual = 1.0 + foreign_rate * tau_foreign
    return (1.0 / tau_usd) * ((forward / spot) * foreign_accrual - 1.0)


def cross_currency_basis_bp(
    spot: float,
    forward: float,
    usd_rate: float,
    foreign_rate: float,
    tau_usd: float,
    tau_foreign: float,
) -> float:
    """Compute the cross-currency basis in basis points.

    Convention:
    basis_bp = (usd_rate - implied_usd_rate) * 10,000.
    A negative basis indicates dollar funding stress (synthetic borrowing costs more than cash).
    """
    implied = implied_usd_rate(spot, forward, foreign_rate, tau_usd, tau_foreign)
    return (usd_rate - implied) * 10000.0


def is_quarter_end(date_iso: str) -> bool:
    """Return True if date_iso is the last weekday of a calendar quarter (Q1, Q2, Q3, Q4).

    Calendar quarter ends are March, June, September, and December.
    If the last calendar day falls on Saturday or Sunday, the last weekday is Friday.
    """
    try:
        dt = datetime.date.fromisoformat(date_iso)
    except (ValueError, TypeError) as err:
        msg = f"Invalid ISO date string: {date_iso}"
        raise ValueError(msg) from err

    if dt.month not in (3, 6, 9, 12):
        return False

    max_day = 31 if dt.month in (3, 12) else 30
    last_cal_day = datetime.date(dt.year, dt.month, max_day)

    # 0=Monday, 4=Friday, 5=Saturday, 6=Sunday
    if last_cal_day.weekday() == 5:  # Saturday
        last_weekday_day = max_day - 1
    elif last_cal_day.weekday() == 6:  # Sunday
        last_weekday_day = max_day - 2
    else:
        last_weekday_day = max_day

    return dt.day == last_weekday_day


def monitor_table(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Generate monitor records for a sequence of daily quote rows.

    Each row must contain 'date', 'spot', 'forward', 'usd_rate', 'foreign_rate', 'tau_usd', 'tau_foreign'.
    Raises ValueError on missing, non-numeric, or invalid fields.
    """
    results: list[dict[str, object]] = []

    required_keys = ("date", "spot", "forward", "usd_rate", "foreign_rate", "tau_usd", "tau_foreign")

    for idx, row in enumerate(rows):
        for key in required_keys:
            if key not in row:
                msg = f"Row {idx} missing required key: {key}"
                raise ValueError(msg)

        date_val = str(row["date"])
        try:
            spot_val = float(row["spot"])  # type: ignore[arg-type]
            forward_val = float(row["forward"])  # type: ignore[arg-type]
            usd_rate_val = float(row["usd_rate"])  # type: ignore[arg-type]
            foreign_rate_val = float(row["foreign_rate"])  # type: ignore[arg-type]
            tau_usd_val = float(row["tau_usd"])  # type: ignore[arg-type]
            tau_foreign_val = float(row["tau_foreign"])  # type: ignore[arg-type]
        except (ValueError, TypeError) as err:
            msg = f"Row {idx} contains non-numeric market quote"
            raise ValueError(msg) from err

        if spot_val <= 0.0 or forward_val <= 0.0 or tau_usd_val <= 0.0 or tau_foreign_val <= 0.0:
            msg = f"Row {idx} contains non-positive price or tenor"
            raise ValueError(msg)

        implied = implied_usd_rate(spot_val, forward_val, foreign_rate_val, tau_usd_val, tau_foreign_val)
        basis = (usd_rate_val - implied) * 10000.0
        qe_flag = is_quarter_end(date_val)

        results.append(
            {
                "date": date_val,
                "implied_usd_rate": implied,
                "basis_bp": basis,
                "is_quarter_end": qe_flag,
            }
        )

    return results
