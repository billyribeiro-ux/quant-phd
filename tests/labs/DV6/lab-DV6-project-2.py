"""Lab Project 2 · Completion Problem: Autocallable Core Formulas.

This lab provides the complete solution for Rung 2 of the project ladder.
In project.html, key mathematical lines are replaced with '___' blanks
for the student to complete. Every non-blank line in project.html matches this twin.
"""

from __future__ import annotations

import math


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


def evaluate_autocall_step(
    spot_obs: float,
    autocall_level: float,
    coupon_barrier: float,
    coupon_rate: float,
    notional: float,
    unpaid_coupons: float,
) -> tuple[bool, float, float, float]:
    """Evaluate single-period autocall condition and memory coupon payout."""
    coupon_due = unpaid_coupons + coupon_rate * notional
    is_autocall = spot_obs >= autocall_level

    if spot_obs >= coupon_barrier:
        coupon_paid = coupon_due
        remaining_unpaid = 0.0
    else:
        coupon_paid = 0.0
        remaining_unpaid = coupon_due

    redemption_paid = notional if is_autocall else 0.0
    return is_autocall, coupon_paid, redemption_paid, remaining_unpaid


def calculate_dealer_gamma_exposure(
    client_gamma: float,
    spot: float,
    notional: float,
) -> tuple[float, float]:
    """Calculate dealer gamma and total dollar gamma exposure."""
    dealer_gamma = -client_gamma
    dealer_gex = dealer_gamma * notional
    return dealer_gamma, dealer_gex


def main() -> None:
    print("=== Rung 2 Completion Problem · Autocallable Core Formulas ===")

    # 1. Local Volatility Evaluation
    s, k, t = 105.0, 100.0, 0.5
    b_vol, sk, curv = 0.20, 0.15, 0.05
    vol = eval_local_vol(s, k, t, b_vol, sk, curv)
    print(f"Local Volatility at S={s:.1f}, K={k:.1f}, t={t:.1f}y: {vol * 100.0:.2f}%")

    # 2. Autocall Step Evaluation
    spot_obs = 95.0
    ac_level = 100.0
    cp_barrier = 80.0
    cp_rate = 0.03
    notional = 1000.0
    unpaid = 30.0  # 1 missed coupon in memory
    is_ac, cp_paid, red_paid, rem_unpaid = evaluate_autocall_step(
        spot_obs, ac_level, cp_barrier, cp_rate, notional, unpaid
    )
    print(
        f"Autocall Step: Is Autocall={is_ac}, Coupon Paid=${cp_paid:.2f}, "
        f"Redemption=${red_paid:.2f}, Unpaid=${rem_unpaid:.2f}"
    )

    # 3. Dealer Gamma Exposure
    cl_gamma = 0.0085
    d_gamma, d_gex = calculate_dealer_gamma_exposure(cl_gamma, s, notional)
    print(f"Dealer Gamma: {d_gamma:.6f}, Dealer GEX: ${d_gex:.2f}")


main()
