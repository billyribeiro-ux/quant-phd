"""Lab X1-L03-1: Uncovered Interest Parity (UIP) empirical test.

Tests the uncovered interest parity condition E_t[s_{t+k} - s_t] = i_t - i_t^*,
computing realized forecast errors and verifying the short-horizon failure of UIP.
"""

from __future__ import annotations

import math
import random


def test_uip_empirical(
    seed: int = 42,
    n_periods: int = 120,
    true_beta: float = -0.80,
) -> dict[str, float]:
    """Simulate interest differentials and exchange rates to test the UIP condition.

    Under theoretical UIP, Delta s_{t+1} = (i_t - i_t^*) + epsilon_{t+1}, so beta = 1.0.
    In historical data, beta is consistently negative (Fama 1984), generating the UIP puzzle.

    Args:
        seed: Random seed.
        n_periods: Number of monthly periods.
        true_beta: DGP regression slope for Delta s on (i - i^*).

    Returns:
        dict containing estimated beta, alpha, R^2, and UIP test t-statistic.
    """
    rng = random.Random(seed)

    # Interest rate differential (i_t - i_t^*) in monthly percent, mean 0.1%, sd 0.15%
    i_diff: list[float] = [rng.gauss(0.001, 0.0015) for _ in range(n_periods)]

    # Realized exchange rate changes Delta s_{t+1}
    # Monthly FX volatility ~ 2.5% (0.025)
    delta_s: list[float] = []
    for d in i_diff:
        eps = rng.gauss(0.0, 0.025)
        ds = true_beta * d + eps
        delta_s.append(ds)

    mean_x = sum(i_diff) / n_periods
    mean_y = sum(delta_s) / n_periods

    var_x = sum((x - mean_x) ** 2 for x in i_diff)
    cov_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(i_diff, delta_s, strict=True))

    beta_hat = cov_xy / var_x
    alpha_hat = mean_y - beta_hat * mean_x

    residuals = [y - (alpha_hat + beta_hat * x) for x, y in zip(i_diff, delta_s, strict=True)]
    s2 = sum(r**2 for r in residuals) / (n_periods - 2)
    se_beta = math.sqrt(s2 / var_x)

    # Test hypothesis H_0: beta = 1.0 (Theoretical UIP)
    t_stat_uip = (beta_hat - 1.0) / se_beta

    tot_var = sum((y - mean_y) ** 2 for y in delta_s)
    r_squared = 1.0 - (sum(r**2 for r in residuals) / tot_var)

    return {
        "beta_hat": round(beta_hat, 4),
        "alpha_hat": round(alpha_hat, 6),
        "se_beta": round(se_beta, 4),
        "t_stat_uip": round(t_stat_uip, 2),
        "r_squared": round(r_squared, 4),
    }


def main() -> None:
    print("Lab X1-L03-1 | Uncovered Interest Parity (UIP) Empirical Test")
    print("---------------------------------------------------------------")

    # Simulation matching Fama (1984) empirical sample parameters
    res = test_uip_empirical(seed=42, n_periods=120, true_beta=-0.80)

    print("Estimated Fama UIP Regression: Delta s_{t+1} = alpha + beta * (i_t - i_t^*) + e_{t+1}")
    print(f"  Estimated beta (slope):         {res['beta_hat']:>8.4f}")
    print(f"  Standard error of beta:         {res['se_beta']:>8.4f}")
    print(f"  R-squared:                      {res['r_squared']:>8.4f}")
    print("Hypothesis Test H_0: beta = 1.0 (Theoretical UIP):")
    print(f"  t-statistic (vs beta = 1.0):   {res['t_stat_uip']:>8.2f}")
    print(f"  UIP Rejection (at 5% level):    {abs(res['t_stat_uip']) > 1.96}")


main()
