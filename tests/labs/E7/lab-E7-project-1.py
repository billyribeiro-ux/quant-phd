"""Lab E7-project-1: Project Rung 1 Worked Example for Monetary-Shock Identification.

Walkthrough of:
1. Converting FOMC event-window futures quotes to high-frequency surprises.
2. Estimating Jordà (2005) local projections for output gap responses over H = 4 horizons.
3. Interpreting impulse response coefficients and standard errors.
"""

from __future__ import annotations


def calculate_fed_funds_surprise(f_post: float, f_pre: float, day: int, days_in_month: int) -> float:
    scale = days_in_month / float(days_in_month - day)
    return scale * (f_post - f_pre)


def main() -> None:
    print("Rung 1 Worked Example: High-Frequency Monetary Surprise & Local Projections")

    # Step 1: High-Frequency Surprise
    # An announcement on day 12 of a 30-day month
    f_pre = 4.25
    f_post = 4.31  # 6 bps raw futures jump
    day = 12
    days_in_month = 30

    scale = days_in_month / float(days_in_month - day)
    surprise = calculate_fed_funds_surprise(f_post, f_pre, day, days_in_month)

    print(f"Step 1: Event window on day {day}/{days_in_month}:")
    print(f"  Raw futures jump:  {(f_post - f_pre) * 100:+.2f} bps")
    print(f"  Scaling factor:    {scale:.4f}")
    print(f"  Target surprise:   {surprise * 100:+.2f} bps")

    # Step 2: Local Projection Estimation over H = 4
    # Synthetic 5-period illustrative response
    # y_{t+h} - y_{t-1} = beta^(h) * shock_t
    betas = [-0.12, -0.38, -0.65, -0.48, -0.25]
    ses = [0.04, 0.09, 0.14, 0.12, 0.10]

    print("\nStep 2: Jordà Local Projection Impulse Responses for Output Gap:")
    print("  Horizon h | Response beta(h) | Standard Error | 95% Confidence Interval")
    for h in range(len(betas)):
        lower = betas[h] - 1.96 * ses[h]
        upper = betas[h] + 1.96 * ses[h]
        print(f"     h={h}   |      {betas[h]:+6.3f}      |      {ses[h]:.3f}     |     [{lower:+6.3f}, {upper:+6.3f}]")


main()
