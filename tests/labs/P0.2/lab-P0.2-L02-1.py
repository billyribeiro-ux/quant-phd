"""Lab 1 (L02): FSRS-family spaced retrieval scheduling and memory dynamics.

Standard library only. Implements the Free Spaced Repetition Scheduler (FSRS-4.5) memory model
derived from Ye, Su & Cao (2022). Verifies the exact mathematical identity R(S, S) = 0.90, calculates
optimal review intervals as a function of target retention, and simulates longitudinal memory retention
over a 180-day horizon comparing massed cramming, fixed linear spacing, and adaptive FSRS spaced retrieval.
"""

from __future__ import annotations

import math

# FSRS-4.5 power-forgetting curve constants
DECAY: float = -0.5
FACTOR: float = 19.0 / 81.0


def fsrs_retrievability(elapsed_days: float, stability: float) -> float:
    """Retrievability R(t, S) = (1 + (19/81) * (t / S))^(-0.5)."""
    if stability <= 0.0:
        return 0.0
    return math.pow(1.0 + FACTOR * (elapsed_days / stability), DECAY)


def fsrs_interval(stability: float, target_retention: float = 0.90) -> float:
    """Optimal review interval I(S, r) = (S / (19/81)) * (r^(1 / -0.5) - 1) = (81/19) * S * (r^(-2) - 1)."""
    if target_retention <= 0.0 or target_retention >= 1.0:
        raise ValueError("Target retention r must lie strictly in (0, 1)")
    return (stability / FACTOR) * (math.pow(target_retention, 1.0 / DECAY) - 1.0)


def update_stability_on_recall(stability: float, difficulty: float, retrievability: float) -> float:
    """Update stability after successful recall under standard FSRS parameters."""
    # Simplified standard FSRS-4.5 recall multiplier:
    # S' = S * (1 + exp(w8) * (11 - D) * S^(-w9) * (exp(w10 * (1 - R)) - 1))
    # Using default parameter magnitudes: w8 = 1.6474, w9 = 0.1367, w10 = 1.0461
    w8, w9, w10 = 1.6474, 0.1367, 1.0461
    factor = math.exp(w8) * (11.0 - difficulty) * math.pow(stability, -w9)
    gain = factor * (math.exp(w10 * (1.0 - retrievability)) - 1.0)
    return stability * (1.0 + max(gain, 0.1))


def simulate_massed_practice(initial_stability: float, horizon_days: int) -> tuple[int, float]:
    """Massed practice: reviews on Day 0 and Day 1, then no subsequent reviews."""
    # Day 0: card introduced
    s = initial_stability
    # Day 1: cramming review after 1 day
    r1 = fsrs_retrievability(1.0, s)
    s = update_stability_on_recall(s, difficulty=5.0, retrievability=r1)
    reviews_count = 2

    # Retrievability at Day horizon_days (elapsed = horizon_days - 1)
    final_r = fsrs_retrievability(float(horizon_days - 1), s)
    return reviews_count, final_r


def simulate_fixed_spacing(initial_stability: float, horizon_days: int, step_days: int = 7) -> tuple[int, float]:
    """Fixed spacing: reviews every fixed interval (e.g. 7 days)."""
    s = initial_stability
    reviews_count = 1  # Day 0 initial study
    current_day = 0

    while current_day + step_days <= horizon_days:
        current_day += step_days
        r = fsrs_retrievability(float(step_days), s)
        s = update_stability_on_recall(s, difficulty=5.0, retrievability=r)
        reviews_count += 1

    remaining = float(horizon_days - current_day)
    final_r = fsrs_retrievability(remaining, s) if remaining > 0 else 1.0
    return reviews_count, final_r


def simulate_fsrs_spacing(
    initial_stability: float,
    horizon_days: int,
    target_retention: float = 0.90,
) -> tuple[int, float]:
    """Adaptive FSRS spacing: review dynamically scheduled when R drops to target retention."""
    s = initial_stability
    reviews_count = 1  # Day 0 initial study
    current_day = 0.0

    while True:
        interval = max(1.0, round(fsrs_interval(s, target_retention)))
        if current_day + interval > horizon_days:
            break
        current_day += interval
        r = fsrs_retrievability(interval, s)
        s = update_stability_on_recall(s, difficulty=5.0, retrievability=r)
        reviews_count += 1

    remaining = float(horizon_days) - current_day
    final_r = fsrs_retrievability(remaining, s) if remaining > 0 else 1.0
    return reviews_count, final_r


def main() -> None:
    print("SIMULATED FSRS Memory Model Verification & Longitudinal Simulation")

    # 1. Closed-form identity checks
    test_stability = 24.5
    r_identity = fsrs_retrievability(elapsed_days=test_stability, stability=test_stability)
    i_identity = fsrs_interval(stability=test_stability, target_retention=0.90)

    print("\n--- Theoretical Identity Verifications ---")
    print(f"Test stability S:                        {test_stability:.1f} days")
    print(f"R(S, S) calculated:                      {r_identity:.12f}")
    print("Theoretical target R(S, S):              0.900000000000")
    print(f"Absolute residual |R(S, S) - 0.9|:       {abs(r_identity - 0.9):.2e}")
    print(f"I(S, 0.90) calculated:                   {i_identity:.12f} days")
    print(f"Absolute residual |I(S, 0.90) - S|:     {abs(i_identity - test_stability):.2e}")

    # 2. Sensitivity of optimal interval to target retention
    print("\n--- Optimal Interval Sensitivity vs Target Retention (S = 10.0 days) ---")
    print(f"{'Target Retention (r)':>20} | {'Optimal Interval I(S, r)':>25} | {'Interval / S Ratio':>20}")
    print("-" * 72)
    s_base = 10.0
    for r_target in [0.70, 0.80, 0.85, 0.90, 0.95]:
        interval = fsrs_interval(s_base, r_target)
        ratio = interval / s_base
        print(f"{r_target:20.2f} | {interval:23.2f} d | {ratio:20.2f}x")

    # 3. 180-Day longitudinal simulation across learning paradigms
    horizon = 180
    init_s = 2.0  # Initial stability of 2 days after first encounter

    reviews_massed, ret_massed = simulate_massed_practice(init_s, horizon)
    reviews_fixed, ret_fixed = simulate_fixed_spacing(init_s, horizon, step_days=7)
    reviews_fsrs, ret_fsrs = simulate_fsrs_spacing(init_s, horizon, target_retention=0.90)

    print(f"\n--- 180-Day Longitudinal Retention Simulation (S_0 = {init_s:.1f} days) ---")
    print(f"{'Strategy':>25} | {'Total Reviews':>15} | {'Day 180 Retention':>20} | {'Efficiency (Ret/Rev)':>22}")
    print("-" * 90)
    for name, revs, ret in [
        ("Massed Practice (Cramming)", reviews_massed, ret_massed),
        ("Fixed Spacing (7-Day)", reviews_fixed, ret_fixed),
        ("Adaptive FSRS-4.5 (r=0.90)", reviews_fsrs, ret_fsrs),
    ]:
        eff = ret / revs
        print(f"{name:>25} | {revs:15d} | {ret:19.1%} | {eff:22.4f}")


main()
