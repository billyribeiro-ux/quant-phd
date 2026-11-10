"""Lab X2-L01-1: Currency Carry Trade Backtest & UIP Breakdown Simulator.

Simulates a multi-currency carry strategy across funding and target currencies,
computing realized excess returns, annualized Sharpe ratios, and Fama regression beta.
"""

from __future__ import annotations

import math
import random


def simulate_carry_trade(
    n_months: int = 60,
    seed: int = 42,
) -> dict[str, float]:
    """Simulate a multi-currency carry trade portfolio over n_months.

    Args:
        n_months: Sample length in months.
        seed: Random seed for reproducibility.

    Returns:
        Summary metrics dictionary including annualized mean return, volatility,
        Sharpe ratio, and UIP regression beta.
    """
    rng = random.Random(seed)

    # 4 currencies: 2 funding (low rate), 2 target (high rate)
    # Interest rate differentials (i_j^* - i_USD) annualized
    spreads = [-0.030, -0.020, 0.035, 0.050]
    n_cur = len(spreads)

    # Initial log spot rates
    log_spots = [0.0] * n_cur

    carry_excess_returns: list[float] = []
    depreciation_series: list[float] = []
    interest_diff_series: list[float] = []

    for _ in range(n_months):
        # Monthly interest rate differential per month
        monthly_diffs = [s / 12.0 for s in spreads]

        # Exchange rate innovations: UIP failure implies spot changes do not
        # offset interest differentials in sample (random walk with noise)
        delta_spots: list[float] = []
        for j in range(n_cur):
            # Spot innovation: small noise, beta_UIP approx -0.5
            u = rng.gauss(0.0, 0.025)
            # Spot depreciation: beta * (i_USD - i_j^*) = -beta * diff
            # With beta = -0.4, high rate currency slightly appreciates!
            ds = -0.4 * (-monthly_diffs[j]) + u
            delta_spots.append(ds)
            log_spots[j] += ds

        # Log currency excess return: rx_{t+1, j} = Delta s_{t+1, j} + (i_j^* - i_USD)/12
        rx_j = [delta_spots[j] + monthly_diffs[j] for j in range(n_cur)]

        # Carry strategy: long top 2 target currencies, short bottom 2 funding currencies
        # Target: indices 2, 3; Funding: indices 0, 1
        long_ret = 0.5 * (rx_j[2] + rx_j[3])
        short_ret = 0.5 * (rx_j[0] + rx_j[1])
        carry_ret = long_ret - short_ret
        carry_excess_returns.append(carry_ret)

        for j in range(n_cur):
            depreciation_series.append(delta_spots[j])
            interest_diff_series.append(-monthly_diffs[j])  # (i_USD - i_j^*)

    # Compute annualized portfolio metrics
    t_len = len(carry_excess_returns)
    mean_monthly = sum(carry_excess_returns) / t_len
    var_monthly = sum((r - mean_monthly) ** 2 for r in carry_excess_returns) / (t_len - 1)
    std_monthly = math.sqrt(var_monthly)

    ann_mean = mean_monthly * 12.0
    ann_std = std_monthly * math.sqrt(12.0)
    ann_sr = ann_mean / ann_std if ann_std > 1e-8 else 0.0

    # Fama UIP regression: Delta s_{t+1} = alpha + beta * (f_t - s_t) + eps
    # where (f_t - s_t) approx (i_USD - i_j^*)
    mean_x = sum(interest_diff_series) / len(interest_diff_series)
    mean_y = sum(depreciation_series) / len(depreciation_series)
    cov_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(interest_diff_series, depreciation_series, strict=True))
    var_x = sum((x - mean_x) ** 2 for x in interest_diff_series)
    fama_beta = cov_xy / var_x if var_x > 1e-12 else 0.0

    return {
        "n_months": float(n_months),
        "ann_mean": round(ann_mean, 4),
        "ann_std": round(ann_std, 4),
        "sharpe_ratio": round(ann_sr, 4),
        "fama_beta": round(fama_beta, 4),
    }


def main() -> None:
    res = simulate_carry_trade(n_months=60, seed=42)
    print("=== Currency Carry Trade & UIP Simulation ===")
    print(f"Sample length: {int(res['n_months'])} months")
    print(f"Annualized mean excess return: {res['ann_mean'] * 100:.2f}%")
    print(f"Annualized volatility: {res['ann_std'] * 100:.2f}%")
    print(f"Annualized Sharpe ratio: {res['sharpe_ratio']:.3f}")
    print(f"Fama UIP regression beta: {res['fama_beta']:.3f}")


main()
