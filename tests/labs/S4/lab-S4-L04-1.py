"""Lab S4-L04-1: The EGARCH news-impact curve and asymmetric leverage effect.

Evaluates Nelson (1991) news-impact curve across standardized shocks,
quantifying the asymmetric volatility response to negative versus positive returns.
"""

from __future__ import annotations

import math


def egarch_news_impact(z: float, alpha: float, gamma: float) -> float:
    """Compute EGARCH news impact function g(z) = alpha * (|z| - E[|z|]) + gamma * z."""
    expected_abs_z = math.sqrt(2.0 / math.pi)
    return float(alpha * (abs(z) - expected_abs_z) + gamma * z)


def main() -> None:
    alpha = 0.20
    gamma = -0.15
    expected_abs_z = math.sqrt(2.0 / math.pi)

    shocks = [-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0]

    print(f"EGARCH(1,1) News Impact: alpha={alpha:.2f}, gamma={gamma:.2f}, E[|z|]={expected_abs_z:.4f}")
    print("Shock z | News Impact g(z) | Negative Slope | Positive Slope | Asymmetry Ratio")
    print("-" * 75)

    neg_slope = alpha - gamma  # 0.20 - (-0.15) = 0.35
    pos_slope = alpha + gamma  # 0.20 + (-0.15) = 0.05
    asym_ratio = neg_slope / pos_slope

    for z in shocks:
        val = egarch_news_impact(z, alpha, gamma)
        print(
            f"  {z:+4.1f}  |       {val:+8.4f}   |"
            f"          {neg_slope:.2f}  |          {pos_slope:.2f}  |          {asym_ratio:.1f}x"
        )


main()
