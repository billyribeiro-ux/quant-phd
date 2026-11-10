"""Lab S6-project-2: Rung 2 completion problem for Policy-Shock Event Study.

SIMULATED: completion twin containing the full solution for abnormal-return variance
and cumulative abnormal return aggregation.
"""

from __future__ import annotations

import random


def main() -> None:
    rng = random.Random(77)

    # Synthetic estimation parameters
    n_est = 50
    mkt_est = [rng.gauss(0.0004, 0.010) for _ in range(n_est)]
    stk_est = [0.0002 + 1.05 * m + rng.gauss(0.0, 0.015) for m in mkt_est]

    m_bar = sum(mkt_est) / n_est
    s_bar = sum(stk_est) / n_est
    ss_m = sum((m - m_bar) ** 2 for m in mkt_est)
    sp_ms = sum((m - m_bar) * (s - s_bar) for m, s in zip(mkt_est, stk_est, strict=True))

    beta_hat = sp_ms / ss_m
    alpha_hat = s_bar - beta_hat * m_bar
    ss_res = sum((s - (alpha_hat + beta_hat * m)) ** 2 for s, m in zip(stk_est, mkt_est, strict=True))
    sigma2_hat = ss_res / (n_est - 2)

    # Event day observation
    event_mkt = 0.0080
    event_stk = 0.0250

    # Step 1: Complete abnormal return and analytical variance
    ar = event_stk - (alpha_hat + beta_hat * event_mkt)
    dev2 = (event_mkt - m_bar) ** 2
    var_ar = sigma2_hat * (1.0 + 1.0 / n_est + dev2 / ss_m)

    # Multi-day event window abnormal returns
    window_ars = [0.0040, ar, -0.0020]

    # Step 2: Complete CAR evaluation
    car_val = sum(window_ars)

    print("Rung 2 Completion Audit Check (SIMULATED):")
    print(f"  Event Day Abnormal Return (AR): {ar:+7.4f}")
    print(f"  Residual Variance (s^2):        {sigma2_hat:.6f}")
    print(f"  Analytical AR Variance:         {var_ar:.6f}")
    print(f"  Variance Inflation Ratio:       {var_ar / sigma2_hat:.4f}")
    print(f"  Window CAR:                     {car_val:+7.4f}")
    print(f"  Analytical Variance Check:      {var_ar > sigma2_hat}")


main()
