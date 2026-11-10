"""Lab E7-project-2: Completion Problem Solution Twin for Monetary-Shock Identification.

Full working solution for Project Rung 2 completion problem:
Calculates target surprise scaling and computes single-horizon local projection coefficient.
"""

from __future__ import annotations


def solve_completion_rung2(
    f_post: float,
    f_pre: float,
    day: int,
    days_in_month: int,
    y_target: list[float],
    shock: list[float],
) -> tuple[float, float]:
    """Compute scaled surprise and univariate OLS regression coefficient."""
    if day < 1 or day >= days_in_month:
        raise ValueError("Invalid day for monthly contract scaling")

    scale = days_in_month / float(days_in_month - day)
    surprise = scale * (f_post - f_pre)

    n = len(shock)
    mean_s = sum(shock) / n
    mean_y = sum(y_target) / n

    cov = sum((shock[i] - mean_s) * (y_target[i] - mean_y) for i in range(n))
    var = sum((shock[i] - mean_s) ** 2 for i in range(n))

    beta = cov / var if var > 1e-12 else 0.0
    return surprise, beta


def main() -> None:
    f_pre = 3.50
    f_post = 3.58  # 8 bps futures jump
    day = 10
    days_in_month = 30

    # Synthetic 5-period test panel
    shocks = [0.10, -0.05, 0.20, -0.15, 0.05]
    y_diff = [-0.08, 0.03, -0.18, 0.12, -0.04]

    surp, beta = solve_completion_rung2(f_post, f_pre, day, days_in_month, y_diff, shocks)

    print("Project Rung 2 Completion Problem Check:")
    print(f"  Scaled target surprise: {surp * 100:+.2f} bps")
    print(f"  Estimated beta impact:  {beta:+.4f}")


main()
