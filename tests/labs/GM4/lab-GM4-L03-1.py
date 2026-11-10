"""Lab GM4-L03-1: Convexity of Expression and Payoff Asymmetry: Options vs Delta-One.

Simulates terminal payoffs of delta-one, outright call, call spread, and straddle
under heavy-tailed macroeconomic shocks (Student-t distribution), demonstrating
convexity benefits and empirical risk-reward asymmetry ratios.
"""

from __future__ import annotations

import math

import numpy as np


def bsm_call_price(s: float, k: float, v: float, t: float, r: float) -> float:
    sqt = v * math.sqrt(t)
    d1 = (math.log(s / k) + (r + 0.5 * v * v) * t) / sqt
    d2 = d1 - sqt
    c1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    c2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
    return s * c1 - k * math.exp(-r * t) * c2


def bsm_put_price(s: float, k: float, v: float, t: float, r: float) -> float:
    c = bsm_call_price(s, k, v, t, r)
    return c + k * math.exp(-r * t) - s


def compute_asymmetry(pnl: np.ndarray) -> float:
    upside = np.maximum(0.0, pnl)
    downside = np.maximum(0.0, -pnl)
    mu_up = float(np.mean(upside))
    mu_down = float(np.mean(downside))
    return mu_up / mu_down if mu_down > 1e-12 else float("inf")


def main() -> None:
    rng = np.random.default_rng(42)
    s0 = 100.0
    vol = 0.22
    t = 0.5  # 6-month expiry
    r = 0.04
    n_sims = 20_000

    # Heavy-tailed macro shock distribution: Student-t with df=4, scaled to match annualized vol
    df = 4
    scale = vol * math.sqrt(t) * math.sqrt((df - 2) / df)
    log_shocks = rng.standard_t(df, size=n_sims) * scale
    terminal_spots = s0 * np.exp(log_shocks)

    # Instrument 1: Delta-One long position (scaled to 1.0 delta)
    pnl_delta_one = terminal_spots - s0

    # Instrument 2: Long ATM Call (K=100)
    c_atm = bsm_call_price(s0, 100.0, vol, t, r)
    payoff_call = np.maximum(0.0, terminal_spots - 100.0)
    pnl_call = payoff_call - c_atm

    # Instrument 3: Call Spread (Long 100 Call, Short 110 Call)
    c_otm = bsm_call_price(s0, 110.0, vol, t, r)
    spread_cost = c_atm - c_otm
    payoff_spread = np.maximum(0.0, terminal_spots - 100.0) - np.maximum(0.0, terminal_spots - 110.0)
    pnl_spread = payoff_spread - spread_cost

    # Instrument 4: Long Straddle (Long 100 Call + Long 100 Put)
    p_atm = bsm_put_price(s0, 100.0, vol, t, r)
    straddle_cost = c_atm + p_atm
    payoff_straddle = np.maximum(0.0, terminal_spots - 100.0) + np.maximum(0.0, 100.0 - terminal_spots)
    pnl_straddle = payoff_straddle - straddle_cost

    # Asymmetry and skewness metrics
    def stats(pnl: np.ndarray) -> tuple[float, float, float, float]:
        mean_val = float(np.mean(pnl))
        std_val = float(np.std(pnl))
        skew_val = float(np.mean(((pnl - mean_val) / std_val) ** 3))
        asym = compute_asymmetry(pnl)
        return mean_val, std_val, skew_val, asym

    m_d1, s_d1, sk_d1, as_d1 = stats(pnl_delta_one)
    m_c, s_c, sk_c, as_c = stats(pnl_call)
    m_cs, s_cs, sk_cs, as_cs = stats(pnl_spread)
    m_st, s_st, sk_st, as_st = stats(pnl_straddle)

    print("--- 1. Delta-One Underlying ---")
    print(f"Mean P&L: {m_d1:.2f} | Std: {s_d1:.2f} | Skewness: {sk_d1:.2f} | Asymmetry Ratio: {as_d1:.3f}")
    print(f"Max Loss: {float(np.min(pnl_delta_one)):.2f} | Max Gain: {float(np.max(pnl_delta_one)):.2f}")

    print("\n--- 2. Long ATM Call Option ---")
    print(f"Mean P&L: {m_c:.2f} | Std: {s_c:.2f} | Skewness: {sk_c:.2f} | Asymmetry Ratio: {as_c:.3f}")
    print(f"Max Loss: {float(np.min(pnl_call)):.2f} | Max Gain: {float(np.max(pnl_call)):.2f}")

    print("\n--- 3. Bull Call Spread (100/110) ---")
    print(f"Mean P&L: {m_cs:.2f} | Std: {s_cs:.2f} | Skewness: {sk_cs:.2f} | Asymmetry Ratio: {as_cs:.3f}")
    print(f"Max Loss: {float(np.min(pnl_spread)):.2f} | Max Gain: {float(np.max(pnl_spread)):.2f}")

    print("\n--- 4. Long ATM Straddle ---")
    print(f"Mean P&L: {m_st:.2f} | Std: {s_st:.2f} | Skewness: {sk_st:.2f} | Asymmetry Ratio: {as_st:.3f}")
    print(f"Max Loss: {float(np.min(pnl_straddle)):.2f} | Max Gain: {float(np.max(pnl_straddle)):.2f}")


main()
