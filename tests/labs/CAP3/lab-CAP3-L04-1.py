"""Lab CAP3-L04-1: Field Prelim III, Problem A: Kuttner Monetary Surprises.

Computes the Kuttner (2001) high-frequency surprise from Fed funds futures
and evaluates the boundary condition adjustment for month-end announcements.
"""

from __future__ import annotations


def compute_kuttner_surprise(
    spot_futures_jump: float,
    announcement_day: int,
    days_in_month: int,
    next_month_jump: float | None = None,
) -> tuple[float, str]:
    """Compute target surprise with boundary check for month-end announcements."""
    remaining_days = days_in_month - announcement_day
    if remaining_days <= 1:
        if next_month_jump is not None:
            return next_month_jump, "Unscaled next-month contract used (boundary rule d >= M-1)"
        # Default fallback
        return spot_futures_jump, "Raw jump fallback (next-month contract unquoted)"
    scale = float(days_in_month) / float(remaining_days)
    return scale * spot_futures_jump, f"Standard scaling applied (M / (M - d) = {scale:.4f})"


def main() -> None:
    cases = [
        {"day": 5, "m": 30, "jump": -0.010, "next": -0.010},
        {"day": 15, "m": 30, "jump": -0.010, "next": -0.018},
        {"day": 25, "m": 30, "jump": -0.010, "next": -0.045},
        {"day": 29, "m": 30, "jump": -0.010, "next": -0.025},
        {"day": 30, "m": 30, "jump": -0.010, "next": -0.025},
    ]

    print("--- Kuttner (2001) High-Frequency Surprise Identification ---")
    for c in cases:
        day_val = int(c["day"])
        m_val = int(c["m"])
        jump_val = float(c["jump"])
        next_val = float(c["next"]) if c["next"] is not None else None
        surprise, note = compute_kuttner_surprise(jump_val, day_val, m_val, next_val)
        print(
            f"Day {day_val:02d}/{m_val} | Raw Jump: {jump_val * 100:+.1f} bps -> "
            f"Surprise: {surprise * 100:+.2f} bps | {note}"
        )


main()
