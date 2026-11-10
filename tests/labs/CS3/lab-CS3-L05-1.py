"""CS3 Lesson 5 Inline Lab 1: Point-in-time data and revision history.

Demonstrates bitemporal point-in-time reads versus naive latest-value reads.
Counts look-ahead observations and measures distortion across historical decision dates.
Data: SIMULATED GDP growth revision history.
"""

from __future__ import annotations

from typing import NamedTuple


class MacroRevision(NamedTuple):
    ref_period: str
    release_date: str
    value_pct: float
    vintage: str


def get_point_in_time_value(revisions: list[MacroRevision], ref_period: str, as_of_date: str) -> float | None:
    """Return the most recent observation known as of as_of_date (release_date <= as_of_date)."""
    candidates = [r for r in revisions if r.ref_period == ref_period and r.release_date <= as_of_date]
    if not candidates:
        return None
    latest = max(candidates, key=lambda r: r.release_date)
    return latest.value_pct


def get_naive_latest_value(revisions: list[MacroRevision], ref_period: str) -> float | None:
    """Naive lookup returning the terminal revision regardless of decision date (look-ahead)."""
    candidates = [r for r in revisions if r.ref_period == ref_period]
    if not candidates:
        return None
    latest = max(candidates, key=lambda r: r.release_date)
    return latest.value_pct


def main() -> None:
    # SIMULATED macroeconomic revision history
    revisions = [
        MacroRevision("2020-Q1", "2020-04-30", 1.2, "advance"),
        MacroRevision("2020-Q1", "2020-05-28", 1.5, "second"),
        MacroRevision("2020-Q1", "2020-06-25", 1.4, "third"),
        MacroRevision("2020-Q2", "2020-07-30", -5.0, "advance"),
        MacroRevision("2020-Q2", "2020-08-27", -4.8, "second"),
        MacroRevision("2020-Q2", "2020-09-24", -4.9, "third"),
    ]

    decision_dates = [
        ("2020-04-15", "2020-Q1"),  # Before advance release -> None
        ("2020-05-15", "2020-Q1"),  # Between advance and second -> 1.2%
        ("2020-06-15", "2020-Q1"),  # Between second and third -> 1.5%
        ("2020-07-15", "2020-Q1"),  # After third release -> 1.4%
        ("2020-08-15", "2020-Q2"),  # Between advance and second for Q2 -> -5.0%
    ]

    lookahead_count = 0
    total_evals = len(decision_dates)

    print(f"Total historical revisions in database: {len(revisions)}")
    for decision_date, period in decision_dates:
        pit_val = get_point_in_time_value(revisions, period, decision_date)
        naive_val = get_naive_latest_value(revisions, period)

        is_lookahead = pit_val != naive_val
        if is_lookahead:
            lookahead_count += 1

        pit_str = f"{pit_val:+.1f}%" if pit_val is not None else "None"
        naive_str = f"{naive_val:+.1f}%" if naive_val is not None else "None"
        print(
            f"Decision Date: {decision_date} (Period: {period}) -> "
            f"PIT: {pit_str:>6} | Naive Latest: {naive_str:>6} | Look-ahead: {is_lookahead}"
        )

    print(f"Total evaluation dates: {total_evals}")
    print(f"Look-ahead contaminated dates: {lookahead_count} of {total_evals}")
    print(f"Look-ahead rate: {lookahead_count / total_evals:.1%}")

    # Invariants verification
    assert lookahead_count == 4
    print("Point-in-time discipline successfully prevented 4 look-ahead leaks: True")


if __name__ == "__main__":
    main()
