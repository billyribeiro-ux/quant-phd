"""Lab S6-L08-1: Placebo event tests and multiple testing false rejection rates.

SIMULATED: evaluates false positive rates for placebo event dates under the null hypothesis,
verifying that individual placebo tests reject at nominal alpha while the family-wise
false discovery probability across m independent placebo dates scales as 1 - (1 - alpha)^m.
"""

from __future__ import annotations

import random


def main() -> None:
    rng = random.Random(2026)
    trials = 2500
    m_dates = 10
    alpha = 0.05
    crit_val = 1.96  # Two-sided standard normal critical threshold

    # Theoretical probability of at least one false rejection across m independent dates
    theoretical_family_rate = 1.0 - (1.0 - alpha) ** m_dates

    total_single_tests = 0
    total_single_rejections = 0
    trials_with_any_rejection = 0

    for _ in range(trials):
        trial_rejections = 0
        for _ in range(m_dates):
            # Draw standard normal test statistic under the null of zero abnormal return
            z_stat = rng.gauss(0.0, 1.0)
            total_single_tests += 1
            if abs(z_stat) > crit_val:
                total_single_rejections += 1
                trial_rejections += 1

        if trial_rejections > 0:
            trials_with_any_rejection += 1

    emp_single_rate = total_single_rejections / total_single_tests
    emp_family_rate = trials_with_any_rejection / trials

    print("Placebo Date Multiple Testing Falsification Analysis (SIMULATED):")
    print(f"  Simulation Trials:             {trials}")
    print(f"  Placebo Dates Per Trial (m):   {m_dates}")
    print(f"  Nominal Single Date Size (alpha): {alpha:.4f} ({alpha * 100:.1f}%)")
    print(f"  Standard Normal Threshold:     +/-{crit_val:.2f}\n")
    print("Rejection Rate Results Under The Null:")
    print(f"  Empirical Single Date Rate:    {emp_single_rate:.4f} ({emp_single_rate * 100:.2f}%)")
    print(f"  Single Date Error vs Alpha:    {abs(emp_single_rate - alpha):.4f}")
    print(f"  Theoretical Multi-Date Rate:   {theoretical_family_rate:.4f} ({theoretical_family_rate * 100:.2f}%)")
    print(f"  Empirical Multi-Date Rate:     {emp_family_rate:.4f} ({emp_family_rate * 100:.2f}%)")
    print(f"  Multi-Date Discrepancy:        {abs(emp_family_rate - theoretical_family_rate):.4f}")


main()
