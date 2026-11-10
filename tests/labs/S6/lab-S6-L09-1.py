"""Lab S6-L09-1: Synthetic control weight optimization and pre-intervention fit.

SIMULATED: solves the constrained synthetic control optimization over the unit simplex
for a treated unit using donor series, evaluating pre-intervention MSPE and estimating
the post-intervention causal path.
"""

from __future__ import annotations

import random


def main() -> None:
    rng = random.Random(123)
    t_pre = 8
    t_post = 4
    t_total = t_pre + t_post

    # Donor 1: upward trend + macro cycle
    d1 = [5.0 + 0.8 * t + 1.2 * rng.gauss(0.0, 0.5) for t in range(t_total)]
    # Donor 2: flatter level + different volatility
    d2 = [12.0 + 0.2 * t + 0.9 * rng.gauss(0.0, 0.5) for t in range(t_total)]

    # True latent weights: 0.65 for Donor 1, 0.35 for Donor 2
    true_w1 = 0.65
    true_w2 = 0.35
    true_tau_post = 4.00  # Intervention policy shock at t >= t_pre

    treated: list[float] = []
    for t in range(t_total):
        base = true_w1 * d1[t] + true_w2 * d2[t] + rng.gauss(0.0, 0.2)
        if t >= t_pre:
            base += true_tau_post
        treated.append(base)

    # Grid search over w1 in [0.00, 1.00] with step 0.005 (simplex constraint w1 + w2 = 1, w_j >= 0)
    best_w1 = 0.0
    best_mspe = float("inf")

    steps = 201
    for step in range(steps):
        w1_cand = step / (steps - 1)
        w2_cand = 1.0 - w1_cand

        mspe_cand = sum((treated[t] - (w1_cand * d1[t] + w2_cand * d2[t])) ** 2 for t in range(t_pre)) / t_pre
        if mspe_cand < best_mspe:
            best_mspe = mspe_cand
            best_w1 = w1_cand

    best_w2 = 1.0 - best_w1

    # Naive equal-weighted benchmark (w1 = 0.5, w2 = 0.5)
    naive_mspe = sum((treated[t] - (0.5 * d1[t] + 0.5 * d2[t])) ** 2 for t in range(t_pre)) / t_pre

    # Post-intervention estimated treatment gaps
    synth_post = [best_w1 * d1[t] + best_w2 * d2[t] for t in range(t_pre, t_total)]
    gaps_post = [treated[t] - synth_post[t - t_pre] for t in range(t_pre, t_total)]
    mean_post_tau = sum(gaps_post) / t_post

    print("Synthetic Control Simplex Optimization (SIMULATED):")
    print(f"  Pre-Intervention Periods (T_0):  {t_pre}")
    print(f"  Post-Intervention Periods (T_1): {t_post}")
    print(f"  True Latent Policy Effect:       +{true_tau_post:.2f}\n")
    print("Optimal Simplex Donor Weights:")
    print(f"  w_1* (Donor 1): {best_w1:6.4f} (latent target: {true_w1:.2f})")
    print(f"  w_2* (Donor 2): {best_w2:6.4f} (latent target: {true_w2:.2f})")
    print(f"  Sum of Weights: {best_w1 + best_w2:6.4f}\n")
    print("Pre-Intervention Fit Quality:")
    print(f"  Synthetic Control MSPE: {best_mspe:.6f}")
    print(f"  Equal-Weighted MSPE:    {naive_mspe:.6f}")
    print(f"  Fit Improvement:        {(1.0 - best_mspe / naive_mspe) * 100:.1f}%\n")
    print("Post-Intervention Treatment Effect Recovery:")
    for i, gap in enumerate(gaps_post, start=1):
        print(f"  Period T_0 + {i}: gap = {gap:+6.4f}")
    print(f"  Average Post-Treatment Effect: {mean_post_tau:+6.4f}")
    print(f"  Estimation Error vs True Jump: {abs(mean_post_tau - true_tau_post):.4f}")


main()
