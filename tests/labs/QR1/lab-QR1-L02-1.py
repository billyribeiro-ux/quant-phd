"""QR1 Lesson 2 Inline Lab 1: Data vintages and bitemporal point-in-time visibility.

Demonstrates tracking macroeconomic data revisions across historical publication vintages,
computes real-time revision gaps, and numerically verifies Proposition 2.1
(point-in-time visibility invariance).
Data: SIMULATED GDP revision trajectory.
"""

from __future__ import annotations

from typing import NamedTuple


class Vintage(NamedTuple):
    obs_date: str
    published: str  # YYYY-MM-DDTHH:MM:SSZ
    value: float
    description: str


def query_visible_vintage(vintages: list[Vintage], cutoff: str) -> Vintage | None:
    """Return the vintage with the latest publication timestamp at or before cutoff."""
    eligible = [v for v in vintages if v.published <= cutoff]
    if not eligible:
        return None
    return max(eligible, key=lambda v: v.published)


def main() -> None:
    # SIMULATED revision sequence for 2025-Q3 real annualized GDP growth rate (%)
    obs_date = "2025-Q3"
    revision_history: list[Vintage] = [
        Vintage(obs_date, "2025-10-30T12:30:00Z", 2.8, "Advance estimate"),
        Vintage(obs_date, "2025-11-26T13:30:00Z", 3.1, "Second estimate"),
        Vintage(obs_date, "2025-12-23T13:30:00Z", 2.9, "Third estimate"),
        Vintage(obs_date, "2026-07-30T12:30:00Z", 3.4, "Annual benchmark revision"),
    ]

    final_revised_value = revision_history[-1].value
    print(f"Tracking revision trajectory for {obs_date} GDP growth:")
    for v in revision_history:
        print(f"  Published {v.published}: {v.value:4.1f}% ({v.description})")

    # Evaluation decision cut-offs
    cutoffs = [
        ("2025-11-15T00:00:00Z", "Post-Advance (pre-Second)"),
        ("2025-12-01T00:00:00Z", "Post-Second (pre-Third)"),
        ("2026-01-15T00:00:00Z", "Post-Third (pre-Benchmark)"),
        ("2026-08-15T00:00:00Z", "Post-Benchmark"),
    ]

    print("\nPoint-in-time queries and revision gaps against final figure (3.4%):")
    for cutoff_ts, label in cutoffs:
        v_vis = query_visible_vintage(revision_history, cutoff_ts)
        assert v_vis is not None
        gap = v_vis.value - final_revised_value
        print(f"  Cut-off {cutoff_ts} [{label}]: visible={v_vis.value:.1f}% gap={gap:+.1f}%")

    # Proposition 2.1 Numerical Verification:
    # Visible value at cutoff T must be invariant under addition of vintages published after T.
    cutoff_t1 = "2025-11-15T00:00:00Z"
    sub_history_t1 = [v for v in revision_history if v.published <= cutoff_t1]
    val_before_add = query_visible_vintage(sub_history_t1, cutoff_t1)
    val_after_add = query_visible_vintage(revision_history, cutoff_t1)

    assert val_before_add is not None and val_after_add is not None
    invariance_holds = val_before_add.value == val_after_add.value
    print(f"\nProposition 2.1 Invariance Test at {cutoff_t1}:")
    print(f"  Value visible using only contemporaneous history: {val_before_add.value:.1f}%")
    print(f"  Value visible after appending subsequent revisions: {val_after_add.value:.1f}%")
    print(f"  Invariance property verified: {invariance_holds}")


main()
