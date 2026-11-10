"""Lab S4-L07-1: Asymmetry and scale properties of QLIKE vs MSE loss.

Evaluates quasi-likelihood loss L(y, h) = y/h - ln(y/h) - 1 against MSE loss
across a spectrum of volatility forecast ratios y/h.
Demonstrates the severe penalty QLIKE imposes on under-predicting volatility.
"""

from __future__ import annotations

import math


def qlike_loss(realized: float, forecast: float) -> float:
    """Compute QLIKE loss."""
    ratio = realized / forecast
    return float(ratio - math.log(ratio) - 1.0)


def mse_loss(realized: float, forecast: float) -> float:
    """Compute MSE loss."""
    diff = realized - forecast
    return float(diff * diff)


def main() -> None:
    y = 1.00
    forecasts = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 2.00]

    print(f"Loss Evaluation for Target Realized Variance y = {y:.2f}:")
    print("Forecast h | Ratio y/h | QLIKE Loss | MSE Loss | QLIKE/MSE Ratio")
    print("-" * 65)

    for h in forecasts:
        q = qlike_loss(y, h)
        m = mse_loss(y, h)
        ratio_str = f"{q / m:.3f}" if m > 0.0 else "N/A (min)"
        print(f"   {h:4.2f}    |    {y / h:4.2f}   |   {q:.4f}   |  {m:.4f}  |    {ratio_str}")

    print("\nAsymmetry Demonstration:")
    q_under = qlike_loss(1.0, 0.50)  # 50% under-forecast
    q_over = qlike_loss(1.0, 1.50)  # 50% over-forecast
    m_under = mse_loss(1.0, 0.50)
    m_over = mse_loss(1.0, 1.50)
    print(f"50% Under-forecast (h=0.5): QLIKE = {q_under:.4f}, MSE = {m_under:.4f}")
    print(f"50% Over-forecast  (h=1.5): QLIKE = {q_over:.4f}, MSE = {m_over:.4f}")
    print(f"QLIKE Under/Over penalty ratio: {q_under / q_over:.2f}x (MSE ratio: {m_under / m_over:.2f}x)")


main()
