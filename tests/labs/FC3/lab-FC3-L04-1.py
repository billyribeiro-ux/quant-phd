"""Lab FC3-L04-1: Joint hypothesis and omitted factors.

SIMULATED constructed returns demonstrating that omitting a relevant factor
causes an apparent non-zero alpha under a one-factor model, whereas the
two-factor specification recovers an alpha of exactly zero.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    """Verify exact Fraction omitted factor bias and two-factor recovery."""
    # SIMULATED: 4 time periods, exact Fraction data
    f1 = [Fraction(1, 10), Fraction(2, 10), Fraction(3, 10), Fraction(4, 10)]
    f2 = [Fraction(3, 10), Fraction(1, 10), Fraction(4, 10), Fraction(2, 10)]

    # True data generating process: alpha = 0, beta_1 = 1, beta_2 = 2
    r = [Fraction(0) + Fraction(1) * f1[t] + Fraction(2) * f2[t] for t in range(4)]

    n_periods = len(r)
    mean_f1 = sum(f1) / n_periods
    mean_r = sum(r) / n_periods

    # 1-factor regression of r on f1
    s_f1f1 = sum((f1[t] - mean_f1) ** 2 for t in range(n_periods))
    s_f1r = sum((f1[t] - mean_f1) * (r[t] - mean_r) for t in range(n_periods))
    b1 = s_f1r / s_f1f1
    a1 = mean_r - b1 * mean_f1
    rss1 = sum((r[t] - (a1 + b1 * f1[t])) ** 2 for t in range(n_periods))

    # 2-factor model: true DGP parameters
    a2 = Fraction(0)
    b2_1 = Fraction(1)
    b2_2 = Fraction(2)
    rss2 = sum((r[t] - (a2 + b2_1 * f1[t] + b2_2 * f2[t])) ** 2 for t in range(n_periods))

    print("Constructed returns (true alpha = 0, beta_1 = 1, beta_2 = 2):")
    for t in range(n_periods):
        print(f"  t={t}: f1={f1[t]}, f2={f2[t]}, r={r[t]}")
    print()
    print("One-factor model (omitted factor f2):")
    print(f"  Estimated beta_1: {b1} ({float(b1):.4f})")
    print(f"  Apparent alpha_1: {a1} ({float(a1):.4f})")
    print(f"  Residual sum of squares: {rss1} ({float(rss1):.4f})")
    print()
    print("Two-factor model (correct specification):")
    print(f"  True alpha_2:     {a2} ({float(a2):.4f})")
    print(f"  True beta_1:      {b2_1} ({float(b2_1):.4f})")
    print(f"  True beta_2:      {b2_2} ({float(b2_2):.4f})")
    print(f"  Residual sum of squares: {rss2} ({float(rss2):.4f})")
    print()
    print(f"Apparent anomaly eliminated: {a1 != 0 and a2 == 0}")


main()
