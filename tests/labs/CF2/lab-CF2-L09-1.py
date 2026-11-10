"""CF2 lab L09-1: Leverage dynamics and partial target adjustment.

Model: Exact closed-form partial adjustment equation:
  L_t - L_{t-1} = lambda * (L* - L_{t-1}).
  L_t - L* = (1 - lambda)^t * (L_0 - L*).
Half-life of adjustment: t_{1/2} = ln(0.5) / ln(1 - lambda).
Demonstrates geometric convergence toward target leverage and verifies closed-form trajectory.
"""

from __future__ import annotations

import math


def main() -> None:
    print("CF2 Lab L09-1: Partial Target Adjustment Dynamics")
    print("------------------------------------------------")

    l_0 = 0.60  # Initial leverage 60.0%
    l_star = 0.35  # Target leverage 35.0%
    lambda_speed = 0.20  # Adjustment speed 20% per year
    n_years = 12

    # Theoretical half-life
    half_life = math.log(0.5) / math.log(1.0 - lambda_speed)

    print(f"Initial leverage (L_0):     {l_0:.1%}")
    print(f"Target leverage (L*):       {l_star:.1%}")
    print(f"Adjustment speed (lambda):   {lambda_speed:.1%}")
    print(f"Theoretical half-life:      {half_life:.2f} years")

    print("\nAdjustment Trajectory Over 12 Years:")
    hdr = (
        f"{'Yr':>3} | {'Simulated Lev (%)':>18} | {'Closed-Form Lev (%)':>20} | "
        f"{'Gap to Target (%)':>18} | {'Share Closed (%)':>17}"
    )
    print(hdr)
    print("-" * 84)

    curr_lev = l_0
    for t in range(n_years + 1):
        # Closed-form formula: L_t = L* + (1 - lambda)^t * (L_0 - L*)
        closed_form = l_star + ((1.0 - lambda_speed) ** t) * (l_0 - l_star)
        gap = curr_lev - l_star
        share_closed = 1.0 - (gap / (l_0 - l_star)) if l_0 != l_star else 1.0

        row_str = (
            f"{t:3d} | {curr_lev * 100:17.3f}% | {closed_form * 100:19.3f}% | "
            f"{gap * 100:17.3f}% | {share_closed * 100:16.1f}%"
        )
        print(row_str)
        assert abs(curr_lev - closed_form) < 1e-12, f"Discrepancy at t = {t}"

        # Update step: Delta L = lambda * (L* - L_t)
        curr_lev += lambda_speed * (l_star - curr_lev)

    print("-" * 84)

    print("\nHalf-Life Comparison Across Adjustment Speeds:")
    print(f"{'lambda (speed)':>15} | {'Half-Life (years)':>18} | {'Lev Remaining after 5 yrs':>26}")
    print("-" * 65)
    for speed in [0.05, 0.10, 0.15, 0.20, 0.30, 0.50, 1.00]:
        hl = math.log(0.5) / math.log(1.0 - speed) if speed < 1.0 else 0.0
        rem_5 = ((1.0 - speed) ** 5) * 100.0
        hl_str = f"{hl:8.2f}" if speed < 1.0 else "   Instant"
        print(f"{speed * 100:14.1f}% | {hl_str:>18} | {rem_5:24.2f}%")


main()
