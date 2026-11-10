"""Lab Project 2 · Completion Problem: Short-Volatility Core Engine.

This lab provides the complete solution for Rung 2 of the project ladder.
In the lesson project page, key mathematical lines are replaced with '___' blanks
for the student to complete. Every non-blank line in project.html matches this twin.
"""

from __future__ import annotations

import math


def compute_variance_swap(
    realized_prices: list[float],
    strike_var: float,
    vega_notional: float,
) -> tuple[float, float, float]:
    """Compute realized variance, variance notional, and swap settlement PnL."""
    n = len(realized_prices) - 1
    sum_sq = sum(math.log(realized_prices[i] / realized_prices[i - 1]) ** 2 for i in range(1, len(realized_prices)))
    rv = (252.0 / float(n)) * sum_sq
    strike_vol = math.sqrt(strike_var)
    var_notional = vega_notional / (2.0 * strike_vol)
    variance_pnl = var_notional * (rv - strike_var)
    return rv, var_notional, variance_pnl


def compute_model_free_vix(
    strikes: list[float],
    quotes: list[float],
    forward: float,
    rate: float,
    maturity: float,
) -> float:
    """Compute discretized model-free implied volatility from OTM options."""
    k0 = max([k for k in strikes if k <= forward])
    m = len(strikes)
    exp_rt = math.exp(rate * maturity)
    integral_sum = 0.0

    for i in range(m):
        k = strikes[i]
        if i == 0:
            dk = strikes[1] - strikes[0]
        elif i == m - 1:
            dk = strikes[m - 1] - strikes[m - 2]
        else:
            dk = 0.5 * (strikes[i + 1] - strikes[i - 1])
        q = quotes[i]
        integral_sum += (dk / (k * k)) * exp_rt * q

    sigma_sq = (2.0 / maturity) * integral_sum - (1.0 / maturity) * ((forward / k0 - 1.0) ** 2)
    return 100.0 * math.sqrt(max(0.0, sigma_sq))


def compute_stress_loss(
    baseline_nav: float,
    spot_shock: float,
    vix_shock: float,
    leverage: float,
) -> tuple[float, float]:
    """Compute portfolio loss fraction and stressed NAV under acute market shock."""
    vol_loss_fraction = leverage * (vix_shock / 100.0)
    spot_loss_fraction = 0.3 * leverage * abs(spot_shock)
    total_loss_fraction = min(1.0, max(0.0, vol_loss_fraction + spot_loss_fraction))
    loss_amount = baseline_nav * total_loss_fraction
    stressed_nav = max(0.0, baseline_nav - loss_amount)
    return total_loss_fraction, stressed_nav


def main() -> None:
    print("=== Rung 2 Completion Problem · Short-Volatility Core Formulas ===")

    # 1. Variance Swap Settlement Check
    prices = [100.0, 101.2, 99.4, 102.1, 100.8, 103.5]
    k_var = 0.040  # 20% vol strike
    n_vega = 50000.0
    rv, n_var, pnl = compute_variance_swap(prices, k_var, n_vega)
    print(f"Variance Swap: RV={rv:.6f}, Var Notional={n_var:.2f}, PnL={pnl:.2f}")

    # 2. Model-Free VIX Replication Check
    strikes = [90.0, 95.0, 100.0, 105.0, 110.0]
    quotes = [1.25, 2.40, 4.10, 2.20, 0.95]
    fwd = 100.20
    r = 0.02
    t = 30.0 / 365.0
    vix_rep = compute_model_free_vix(strikes, quotes, fwd, r, t)
    print(f"Model-Free VIX: Forward={fwd:.2f}, Replicated VIX={vix_rep:.4f}")

    # 3. Crash Stress Test Check
    nav0 = 1000000.0
    s_shock = -0.15
    v_shock = 30.0
    lev = 1.5
    loss_pct, stressed_nav = compute_stress_loss(nav0, s_shock, v_shock, lev)
    print(f"Crash Stress: Loss={loss_pct * 100.0:.2f}%, Stressed NAV={stressed_nav:.2f}")


main()
