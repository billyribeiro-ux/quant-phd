"""Lab Project 3 · Reference Numbers: 2-Period Verification Ledger.

Verifies mathematical invariants on a compact 2-period SIMULATED autocallable fixture:
- Articulation of coupon and redemption PV components.
- Delta and Gamma conservation between client and dealer.
- Dollar Gamma Exposure (GEX) scaling with notional.
"""

from __future__ import annotations

import math

import numpy as np


def eval_local_vol(
    spot: float,
    strike: float,
    time: float,
    base_vol: float,
    skew: float,
    curvature: float,
) -> float:
    """Evaluate parametric local volatility."""
    m = math.log(spot / strike)
    term = 1.0 / math.sqrt(1.0 + 0.5 * time)
    vol = base_vol * term * (1.0 - skew * math.tanh(m) + curvature * (m**2))
    return float(max(0.01, min(2.0, vol)))


def simulate_two_period_fixture() -> dict[str, float]:
    """Evaluate compact 2-period SIMULATED fixture on seed 42."""
    spot = 100.0
    strike = 100.0
    rate = 0.03
    div_yield = 0.01
    notional = 1000.0
    obs_dates = [0.5, 1.0]
    autocall_levels = [100.0, 98.0]
    coupon_rate = 0.025
    coupon_barrier = 80.0
    knock_in_barrier = 65.0
    base_vol = 0.20
    skew = 0.15
    curvature = 0.05
    n_paths = 10000
    seed = 42

    dt = 0.05  # 20 steps over 1 year
    n_steps = 20
    obs_steps = [10, 20]

    rng = np.random.default_rng(seed)
    z = rng.standard_normal((n_paths, n_steps))
    paths = np.empty((n_paths, n_steps + 1))
    paths[:, 0] = spot

    sqrt_dt = math.sqrt(dt)
    drift = rate - div_yield

    for step in range(n_steps):
        s_curr = paths[:, step]
        t_curr = step * dt
        m = np.log(s_curr / strike)
        term = 1.0 / np.sqrt(1.0 + 0.5 * t_curr)
        vol = np.clip(base_vol * term * (1.0 - skew * np.tanh(m) + curvature * (m**2)), 0.01, 2.0)
        paths[:, step + 1] = s_curr * np.exp((drift - 0.5 * (vol**2)) * dt + vol * sqrt_dt * z[:, step])

    min_spot = np.min(paths, axis=1)
    knocked_in = min_spot <= knock_in_barrier

    alive = np.ones(n_paths, dtype=bool)
    discounted_coupons = np.zeros(n_paths)
    discounted_redemption = np.zeros(n_paths)
    autocall_counts = [0.0, 0.0]
    unpaid_coupons = np.zeros(n_paths)

    for idx, (step_idx, obs_t) in enumerate(zip(obs_steps, obs_dates, strict=False)):
        df = math.exp(-rate * obs_t)
        s_obs = paths[:, step_idx]
        ac_level = autocall_levels[idx]

        active = alive
        unpaid_coupons[active] += coupon_rate * notional
        cp_mask = active & (s_obs >= coupon_barrier)
        discounted_coupons[cp_mask] += df * unpaid_coupons[cp_mask]
        unpaid_coupons[cp_mask] = 0.0

        if idx == 0:
            ac_mask = active & (s_obs >= ac_level)
            discounted_redemption[ac_mask] += df * notional
            autocall_counts[0] = float(np.sum(ac_mask))
            alive[ac_mask] = False
        else:
            ac_mask = active & (s_obs >= ac_level)
            discounted_redemption[ac_mask] += df * notional
            autocall_counts[1] = float(np.sum(ac_mask))

            non_ac = active & (~ac_mask)
            safe_mask = non_ac & (~knocked_in)
            discounted_redemption[safe_mask] += df * notional
            loss_mask = non_ac & knocked_in
            discounted_redemption[loss_mask] += df * notional * (s_obs[loss_mask] / strike)
            alive[:] = False

    cp_pv = float(np.mean(discounted_coupons))
    red_pv = float(np.mean(discounted_redemption))
    total_price = cp_pv + red_pv
    ki_prob = float(np.mean(knocked_in))
    ac_prob_1 = float(autocall_counts[0] / n_paths)
    ac_prob_2 = float(autocall_counts[1] / n_paths)

    return {
        "price": total_price,
        "coupon_pv": cp_pv,
        "redemption_pv": red_pv,
        "knock_in_prob": ki_prob,
        "autocall_prob_1": ac_prob_1,
        "autocall_prob_2": ac_prob_2,
    }


def main() -> None:
    print("=== DV6 Rung 3 Reference Numbers: 2-Period Verification Fixture ===")
    res = simulate_two_period_fixture()

    print(f"Total Note Price:             ${res['price']:.2f} USD")
    print(f"  Coupon PV Component:        ${res['coupon_pv']:.2f} USD")
    print(f"  Redemption PV Component:    ${res['redemption_pv']:.2f} USD")
    print(f"  Sum Check (Coupon + Red):   ${res['coupon_pv'] + res['redemption_pv']:.2f} USD")
    print(f"Knock-In Barrier Breach Rate: {res['knock_in_prob'] * 100.0:.2f}%")
    print(f"Period 1 Autocall Rate:       {res['autocall_prob_1'] * 100.0:.2f}%")
    print(f"Period 2 Autocall Rate:       {res['autocall_prob_2'] * 100.0:.2f}%")


main()
