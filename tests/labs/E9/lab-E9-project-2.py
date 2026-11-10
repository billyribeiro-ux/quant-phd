"""Project Lab 2 (Rung 2): Completion problem twin for debt dynamics step and primary gap.

Completed reference twin. Standard library only.
Implements exact discrete-time debt-to-GDP step, debt-stabilizing primary balance,
and breach probability calculation over simulated paths.
"""

from __future__ import annotations


def debt_dynamics_step(b_prev: float, r: float, g: float, s: float) -> float:
    """Compute one-period exact discrete-time debt-to-GDP ratio."""
    if g <= -1.0 or r <= -1.0:
        msg = f"Rates must exceed -1.0: r={r}, g={g}"
        raise ValueError(msg)
    if b_prev < 0.0:
        msg = f"Debt ratio cannot be negative: {b_prev}"
        raise ValueError(msg)
    growth_factor = (1.0 + r) / (1.0 + g)
    return growth_factor * b_prev - s


def primary_gap(b_target: float, r: float, g: float, s_actual: float) -> float:
    """Compute primary gap s* - s required to stabilize debt at b_target."""
    s_star = ((r - g) / (1.0 + g)) * b_target
    return s_star - s_actual


def breach_probability(paths: list[list[float]], debt_ceiling: float) -> float:
    """Compute empirical probability of exceeding debt ceiling at any point."""
    if not paths:
        return 0.0
    breached_count = sum(1 for path in paths if any(val > debt_ceiling for val in path))
    return breached_count / len(paths)


def main() -> None:
    # Test case 1: Single-step debt accumulation
    b_prev = 0.85
    r = 0.04
    g = 0.02
    s = -0.01  # 1% primary deficit

    b_next = debt_dynamics_step(b_prev, r, g, s)
    gap = primary_gap(b_prev, r, g, s)

    # Test case 2: Three paths over 3 years
    ceiling = 1.00
    sample_paths = [
        [0.85, 0.88, 0.92, 0.95],
        [0.85, 0.91, 0.98, 1.04],
        [0.85, 0.86, 0.87, 0.89],
        [0.85, 0.94, 1.01, 1.08],
    ]
    p_breach = breach_probability(sample_paths, ceiling)

    print("=== Rung 2 Completion Problem Reference Verification ===")
    print(f"b_next:            {b_next:.4f}")
    print(f"Primary Gap:       {gap:.4f}")
    print(f"Breach Probability: {p_breach:.4f}")

    assert abs(b_next - 0.8767) < 1e-3, "b_next must match (1.04/1.02)*0.85 - (-0.01) = 0.8767"
    assert abs(gap - 0.0267) < 1e-3, "gap must match (0.02/1.02)*0.85 - (-0.01) = 0.0267"
    assert p_breach == 0.50, "2 out of 4 paths exceed 1.00 ceiling"


main()
