"""Lab MS1-L01-1: Roll spread estimator on a simulated trade-price path.

SIMULATED: generated trade prices with bid-ask bounce and random walk efficient price.
Demonstrates that negative serial covariance in transaction price changes recovers
the underlying bid-ask spread.
"""

from __future__ import annotations

import math
import random


def simulate_roll_path(
    n_trades: int, half_spread: float, sigma: float, seed: int = 42
) -> tuple[list[float], list[int]]:
    """Simulate efficient price and transaction prices under bid-ask bounce."""
    rng = random.Random(seed)
    m = 100.0
    prices: list[float] = []
    signs: list[int] = []
    for _ in range(n_trades):
        m += rng.gauss(0.0, sigma)
        q = rng.choice([-1, 1])
        prices.append(m + half_spread * q)
        signs.append(q)
    return prices, signs


def compute_roll_spread(prices: list[float]) -> tuple[float, float, str]:
    """Compute sample lag-1 covariance of price differences and the Roll spread."""
    n = len(prices)
    if n < 3:
        raise ValueError("At least three prices required.")
    d = [prices[i] - prices[i - 1] for i in range(1, n)]
    mean_d = sum(d) / len(d)
    cov1 = sum((d[i] - mean_d) * (d[i - 1] - mean_d) for i in range(1, len(d))) / (len(d) - 1)
    if cov1 < 0:
        spread = 2.0 * math.sqrt(-cov1)
        sign_status = "negative (valid)"
    else:
        spread = float("nan")
        sign_status = "non-negative (undefined)"
    return cov1, spread, sign_status


def main() -> None:
    n_trades = 2000
    true_c = 0.25
    true_spread = 2.0 * true_c
    sigma = 0.05
    prices, _ = simulate_roll_path(n_trades, true_c, sigma, seed=42)
    cov1, est_spread, sign_status = compute_roll_spread(prices)

    print(f"Number of trades: {n_trades}")
    print(f"True half-spread c: {true_c:.4f}")
    print(f"True full spread 2c: {true_spread:.4f}")
    print(f"Sample lag-1 covariance: {cov1:.6f}")
    print(f"Covariance sign check: {sign_status}")
    print(f"Roll spread estimate: {est_spread:.4f}")
    print(f"Estimation error: {abs(est_spread - true_spread):.4f}")


main()
