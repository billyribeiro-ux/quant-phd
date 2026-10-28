"""E2 L04 lab 1: separating signals in a two-type education model.

Inputs are illustrative, not data: a low type with productivity 40,000 CU and a high type with productivity
60,000 CU, and education costs of 10,000 CU per year (low type) and 5,000 CU per year (high type). All money is
in integer cents, with 1 CU = 100 cents. Education is measured in whole years on the grid 0..6.

The firm pays the threshold wage of Assumption 3 on the page: it pays the high-type productivity at or above the
threshold t and the low-type productivity below it. For each threshold t on the grid, the lab checks the two weak
incentive constraints by enumeration over the grid: the high type's utility at signal t is at least its utility at
every other grid signal, and the low type's utility at signal 0 is at least its utility at every other grid signal.
A threshold t > 0 with both constraints holding is a separating profile. The closed-form interval
(Y_HIGH - Y_LOW) / COST_LOW <= t <= (Y_HIGH - Y_LOW) / COST_HIGH is printed beside the enumeration.

No random draws are used, so every run prints the same lines.
"""

from __future__ import annotations

from fractions import Fraction

Y_LOW = 4_000_000  # productivity of a low type, in cents per year (40,000 CU)
Y_HIGH = 6_000_000  # productivity of a high type, in cents per year (60,000 CU)
COST_LOW = 1_000_000  # cost of one year of education for a low type, in cents (10,000 CU)
COST_HIGH = 500_000  # cost of one year of education for a high type, in cents (5,000 CU)
GRID = range(0, 7)  # whole years of education checked


def wage(e: int, threshold: int) -> int:
    """Wage in cents for e whole years of education under the threshold schedule (Assumption 3)."""
    return Y_HIGH if e >= threshold else Y_LOW


def utility(cost: int, e: int, threshold: int) -> int:
    """Net utility in cents: the wage in cents minus the education cost, cost * e cents."""
    return wage(e, threshold) - cost * e


def classify(threshold: int) -> tuple[str, int, int, int, int]:
    """Return the label and the four utilities in cents for one threshold on the grid."""
    u_high = utility(COST_HIGH, threshold, threshold)
    best_high = max(utility(COST_HIGH, e, threshold) for e in GRID)
    u_low = utility(COST_LOW, 0, threshold)
    best_low = max(utility(COST_LOW, e, threshold) for e in GRID)
    high_ok = u_high == best_high
    low_ok = u_low == best_low
    if threshold == 0:
        label = "same signal for both types"
    elif high_ok and low_ok:
        label = "separating"
    elif not low_ok:
        label = "low type mimics"
    else:
        label = "high type prefers another signal"
    return label, u_high, best_high, u_low, best_low


def main() -> None:
    print("Part A: the closed-form interval, in whole years of education")
    lower = Fraction(Y_HIGH - Y_LOW, COST_LOW)
    upper = Fraction(Y_HIGH - Y_LOW, COST_HIGH)
    print(f"lower bound (Y_HIGH - Y_LOW) / COST_LOW = {lower}")
    print(f"upper bound (Y_HIGH - Y_LOW) / COST_HIGH = {upper}")

    print("Part B: each threshold on the grid 0..6, checked by enumeration (cents)")
    print("threshold | high utility at t | best high utility | low utility at 0 | best low utility | outcome")
    separating: list[int] = []
    for threshold in GRID:
        label, u_high, best_high, u_low, best_low = classify(threshold)
        if label == "separating":
            separating.append(threshold)
        print(f"{threshold:9d} | {u_high:17d} | {best_high:17d} | {u_low:17d} | {best_low:16d} | {label}")

    print("Part C: agreement between the interval and the enumeration")
    interval = [t for t in GRID if lower <= t <= upper and t > 0]
    print(f"separating thresholds on the grid by enumeration: {separating}")
    print(f"thresholds inside the closed-form interval: {interval}")
    print(f"the two lists agree: {separating == interval}")

    print("Part D: the least-cost separating signal")
    least = min(separating)
    print(f"least-cost separating threshold, in whole years: {least}")
    print(f"education cost to the high type at that threshold, in cents: {least * COST_HIGH}")
    print(f"high type utility at that threshold, in cents: {utility(COST_HIGH, least, least)}")


main()
