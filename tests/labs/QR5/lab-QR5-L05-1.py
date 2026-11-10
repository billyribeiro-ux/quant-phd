"""Lab QR5-L05-1: Whalley-Wilmott No-Trade Band Hedging vs. Black-Scholes Delta Hedging.

Demonstrates:
1. Verification of the Whalley & Wilmott (1997) O(epsilon^(1/3)) asymptotic boundary width.
2. Simulation of path-dependent option hedging under proportional transaction costs.
3. Quantifying turnover reduction and transaction cost savings of no-trade band hedging.
"""

from __future__ import annotations

import math

import numpy as np


def bs_call_delta_gamma(s: float, k: float, tau: float, sigma: float, r: float) -> tuple[float, float]:
    """Compute Black-Scholes call option delta and gamma."""
    if tau <= 1e-8:
        delta = 1.0 if s > k else (0.0 if s < k else 0.5)
        return delta, 0.0
    vol_sqrt = sigma * math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / vol_sqrt
    delta = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    phi = math.exp(-0.5 * d1**2) / math.sqrt(2.0 * math.pi)
    gamma = phi / (s * vol_sqrt)
    return delta, gamma


def main() -> None:
    s0 = 100.0
    k = 100.0
    t_exp = 0.25  # roughly 3 months
    n_steps = 63  # daily rebalancing
    dt = t_exp / n_steps
    sigma = 0.20
    r = 0.03
    cost_rate = 0.005  # 50 bps proportional friction
    risk_aversion = 1.0  # gamma parameter

    # 1. Scaling Law Check: h scales with eps^(1/3)
    _, gamma_0 = bs_call_delta_gamma(s0, k, t_exp, sigma, r)
    h_eps1 = np.cbrt(1.5 * cost_rate * math.exp(-r * t_exp) * s0 * (gamma_0**2) / risk_aversion)
    h_eps8 = np.cbrt(1.5 * (8.0 * cost_rate) * math.exp(-r * t_exp) * s0 * (gamma_0**2) / risk_aversion)
    scaling_ratio = float(h_eps8 / h_eps1)

    # 2. Path Simulation
    rng = np.random.default_rng(42)
    n_paths = 1000
    paths = np.zeros((n_paths, n_steps + 1))
    paths[:, 0] = s0

    shocks = rng.normal(0.0, 1.0, size=(n_paths, n_steps))
    drift = (r - 0.5 * sigma**2) * dt
    vol = sigma * math.sqrt(dt)
    for step in range(n_steps):
        paths[:, step + 1] = paths[:, step] * np.exp(drift + vol * shocks[:, step])

    # 3. Simulate Delta Hedging vs. Whalley-Wilmott Hedging
    costs_bs = np.zeros(n_paths)
    costs_ww = np.zeros(n_paths)
    trades_bs = np.zeros(n_paths)
    trades_ww = np.zeros(n_paths)

    for i in range(n_paths):
        curr_delta_bs = 0.0
        curr_delta_ww = 0.0

        for step in range(n_steps):
            tau = t_exp - step * dt
            s_t = paths[i, step]
            delta_target, gamma_t = bs_call_delta_gamma(s_t, k, tau, sigma, r)

            # Continuous delta rebalancing
            trade_bs = abs(delta_target - curr_delta_bs)
            if trade_bs > 1e-6:
                costs_bs[i] += cost_rate * s_t * trade_bs
                trades_bs[i] += 1
            curr_delta_bs = delta_target

            # Whalley-Wilmott Band
            inner = 1.5 * cost_rate * math.exp(-r * tau) * s_t * (gamma_t**2) / risk_aversion
            h_t = float(np.cbrt(max(inner, 0.0)))
            b_low = max(0.0, delta_target - h_t)
            b_high = min(1.0, delta_target + h_t)

            if curr_delta_ww < b_low:
                trade_ww = b_low - curr_delta_ww
                costs_ww[i] += cost_rate * s_t * trade_ww
                trades_ww[i] += 1
                curr_delta_ww = b_low
            elif curr_delta_ww > b_high:
                trade_ww = curr_delta_ww - b_high
                costs_ww[i] += cost_rate * s_t * trade_ww
                trades_ww[i] += 1
                curr_delta_ww = b_high

        # Terminal liquidation
        s_term = paths[i, -1]
        costs_bs[i] += cost_rate * s_term * curr_delta_bs
        costs_ww[i] += cost_rate * s_term * curr_delta_ww

    mean_cost_bs = float(np.mean(costs_bs))
    mean_cost_ww = float(np.mean(costs_ww))
    mean_trades_bs = float(np.mean(trades_bs))
    mean_trades_ww = float(np.mean(trades_ww))
    cost_savings = (mean_cost_bs - mean_cost_ww) / mean_cost_bs * 100.0

    print(f"Asymptotic scaling ratio h(8*eps) / h(eps): {scaling_ratio:.4f} (expected: 2.0000)")
    print(f"Mean trades per path (Delta Hedging): {mean_trades_bs:.1f}")
    print(f"Mean trades per path (Whalley-Wilmott): {mean_trades_ww:.1f}")
    print(f"Mean transaction cost (Delta Hedging): ${mean_cost_bs:.4f}")
    print(f"Mean transaction cost (Whalley-Wilmott): ${mean_cost_ww:.4f}")
    print(f"Transaction cost savings: {cost_savings:.2f}%")


main()
