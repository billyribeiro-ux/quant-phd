"""Lab MS1-L04-1: Bid-ask spread decomposition by regression.

SIMULATED: generated trade prices with both order-processing cost and adverse-selection impact.
Recovers the half-spread, order-processing cost, and adverse-selection component from
a no-intercept regression of price changes on current and lagged trade signs.
"""

from __future__ import annotations

import random


def simulate_decomposition_sample(
    n_trades: int, theta: float, c: float, sigma: float, seed: int = 42
) -> tuple[list[float], list[int]]:
    """Simulate trade prices with order processing and adverse selection."""
    rng = random.Random(seed)
    m = 100.0
    prices: list[float] = []
    signs: list[int] = []
    for _ in range(n_trades):
        q = rng.choice([-1, 1])
        eta = rng.gauss(0.0, sigma)
        m += theta * q + eta
        prices.append(m + c * q)
        signs.append(q)
    return prices, signs


def decompose_spread(prices: list[float], signs: list[int]) -> tuple[float, float, float, float, float]:
    """Perform no-intercept OLS of price differences on current and lagged trade signs."""
    n = len(prices)
    if n < 3:
        raise ValueError("At least three trades are needed")
    if len(signs) != n:
        raise ValueError("Prices and signs must have the same length")

    d = [prices[t] - prices[t - 1] for t in range(1, n)]
    q_curr = [signs[t] for t in range(1, n)]
    q_lag = [signs[t - 1] for t in range(1, n)]

    s00 = sum(x * x for x in q_curr)
    s11 = sum(x * x for x in q_lag)
    s01 = sum(x * y for x, y in zip(q_curr, q_lag, strict=False))
    det = s00 * s11 - s01 * s01
    if det == 0:
        raise ValueError("Singular design matrix")

    y0 = sum(di * qi for di, qi in zip(d, q_curr, strict=False))
    y1 = sum(di * qi for di, qi in zip(d, q_lag, strict=False))

    b0 = (s11 * y0 - s01 * y1) / det
    b1 = (s00 * y1 - s01 * y0) / det

    half_spread = b0
    order_processing = -b1
    adverse_selection = b0 + b1
    adverse_share = adverse_selection / half_spread if half_spread != 0.0 else float("nan")
    identity_gap = abs(half_spread - (order_processing + adverse_selection))

    return half_spread, order_processing, adverse_selection, adverse_share, identity_gap


def main() -> None:
    n_trades = 5000
    theta_true = 0.1500
    c_true = 0.2000
    sigma = 0.05
    prices, signs = simulate_decomposition_sample(n_trades, theta_true, c_true, sigma, seed=42)

    half_s, order_proc, adv_sel, adv_share, id_gap = decompose_spread(prices, signs)

    print("Spread Decomposition Regression Results:")
    print(f"  Number of trades: {n_trades}")
    print(f"  True half-spread H = theta + c: {theta_true + c_true:.4f}")
    print(f"  Estimated half-spread H (b_0): {half_s:.4f}")
    print(f"  True order processing c: {c_true:.4f}")
    print(f"  Estimated order processing c (-b_1): {order_proc:.4f}")
    print(f"  True adverse selection theta: {theta_true:.4f}")
    print(f"  Estimated adverse selection theta (b_0 + b_1): {adv_sel:.4f}")
    print(f"  Adverse selection share: {adv_share:.4f} (true: {theta_true / (theta_true + c_true):.4f})")
    print(f"  Decomposition identity |H - (c + theta)|: {id_gap:.2e}")


main()
