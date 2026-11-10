"""Lab S6-L07-1: Event study with correct abnormal-return variance vs naive variance.

SIMULATED: curriculum benchmark comparing empirical rejection rates under the null
hypothesis of no event response when using the naive residual variance versus
the correct analytical abnormal-return variance that includes parameter estimation error.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    rng = random.Random(1997)
    reps = 3000
    est_len = 30  # Relatively short estimation window to highlight estimation uncertainty

    # Critical value for two-sided 5% test with df = L - 2 = 28
    # Student t critical value for df=28 at alpha=0.05 is 2.0484
    crit_val = 2.0484

    rejections_naive = 0
    rejections_correct = 0

    true_alpha = 0.0003
    true_beta = 1.15
    true_sigma = 0.015

    for _ in range(reps):
        # 1. Estimation window (L days)
        mkt_est = [rng.gauss(0.0004, 0.014) for _ in range(est_len)]
        stk_est = [true_alpha + true_beta * m + rng.gauss(0.0, true_sigma) for m in mkt_est]

        # Market model OLS
        m_bar = sum(mkt_est) / est_len
        s_bar = sum(stk_est) / est_len
        ss_m = sum((m - m_bar) ** 2 for m in mkt_est)
        sp_ms = sum((m - m_bar) * (s - s_bar) for m, s in zip(mkt_est, stk_est, strict=True))

        beta_hat = sp_ms / ss_m
        alpha_hat = s_bar - beta_hat * m_bar
        ss_res = sum((s - (alpha_hat + beta_hat * m)) ** 2 for s, m in zip(stk_est, mkt_est, strict=True))
        sig2_hat = ss_res / (est_len - 2)

        # 2. Event day (Null hypothesis: true abnormal return is exactly 0.0)
        mkt_ev = rng.gauss(0.0004, 0.014)
        stk_ev = true_alpha + true_beta * mkt_ev + rng.gauss(0.0, true_sigma)  # shock = 0

        # Abnormal return
        ar = stk_ev - (alpha_hat + beta_hat * mkt_ev)

        # Naive variance: s^2 alone (omits sampling error of alpha and beta)
        var_naive = sig2_hat
        t_naive = ar / math.sqrt(var_naive)
        if abs(t_naive) > crit_val:
            rejections_naive += 1

        # Correct analytical variance: s^2 * (1 + 1/L + (R_m0 - mean)^2 / SS_m)
        dev_m = (mkt_ev - m_bar) ** 2
        var_correct = sig2_hat * (1.0 + 1.0 / est_len + dev_m / ss_m)
        t_correct = ar / math.sqrt(var_correct)
        if abs(t_correct) > crit_val:
            rejections_correct += 1

    rate_naive = rejections_naive / reps
    rate_correct = rejections_correct / reps

    print("Event Study Abnormal Return Variance Null Rejection Benchmark (SIMULATED):")
    print(f"  Monte Carlo Replications:      {reps}")
    print(f"  Estimation Window Length (L):  {est_len}")
    print("  Nominal Test Size (alpha):     0.0500 (5.00%)")
    print(f"  Two-sided Critical Value:      {crit_val:.4f}\n")
    print("Empirical False Rejection Rates Under H_0:")
    print(f"  Naive Residual Variance (s^2):      {rate_naive:6.4f} ({rate_naive * 100:4.2f}%)  <-- Size distortion!")
    print(
        f"  Correct Analytical Variance:        {rate_correct:6.4f} ({rate_correct * 100:4.2f}%)  <-- Nominal control"
    )
    print(f"  Excess False Rejections (Naive):    +{rate_naive - 0.0500:6.4f} ({(rate_naive - 0.0500) * 100:4.2f} pp)")
    print(f"  Absolute Size Error (Correct):       {abs(rate_correct - 0.0500):6.4f}")


main()
