"""Lab 3: Backtesting Risk Models via the Kupiec POF Test and Basel Traffic Lights.

Demonstrates unconditional coverage testing under Kupiec (1995) across
Basel capital compliance zones (Green, Yellow, Red) for a 99% 1-day VaR.
"""

from __future__ import annotations

import math


def kupiec_pof_test(exceptions: int, total_obs: int = 250, alpha: float = 0.99) -> tuple[float, float, str]:
    """Compute Kupiec POF Likelihood Ratio statistic and Basel traffic light."""
    p = 1.0 - alpha
    x = exceptions
    t = total_obs

    if x == 0:
        lr = -2.0 * t * math.log(1.0 - p)
    elif x == t:
        lr = -2.0 * t * math.log(p)
    else:
        p_hat = x / t
        lr = -2.0 * (
            (t - x) * math.log(1.0 - p) + x * math.log(p) - (t - x) * math.log(1.0 - p_hat) - x * math.log(p_hat)
        )

    lr = max(0.0, float(lr))
    # Chi-squared survival function with 1 degree of freedom
    p_val = float(math.erfc(math.sqrt(lr / 2.0)))

    # Basel Traffic Light zones for T = 250 at 99% confidence
    if x <= 4:
        zone = "Green (Accept Model, Multiplier k=3.0)"
    elif x <= 9:
        zone = "Yellow (Supervisory Discretion, Multiplier 3.0-3.85)"
    else:
        zone = "Red (Automatic Rejection, Multiplier k=4.0)"

    return lr, p_val, zone


def main() -> None:
    t_obs = 250
    alpha = 0.99
    print(f"Backtest Horizon: {t_obs} days | Confidence Level: {alpha * 100:.1f}%")
    print(f"Expected Violations: {t_obs * (1.0 - alpha):.1f}")
    print("-" * 65)

    test_exceptions = [1, 3, 5, 8, 11]

    for x in test_exceptions:
        lr, p_val, zone = kupiec_pof_test(x, total_obs=t_obs, alpha=alpha)
        status = "Reject H0 (p < 0.05)" if p_val < 0.05 else "Fail to Reject H0"
        print(f"Violations x={x:2d} | LR_POF={lr:7.4f} | p-value={p_val:6.4f} | {status}")
        print(f"  Regulatory Zone: {zone}")


main()
